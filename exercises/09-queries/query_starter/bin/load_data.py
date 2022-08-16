import asyncio
import json
import os
import sys
import time
from typing import List, Optional, Dict

# noinspection PyPackageRequirements
import progressbar
from dateutil.parser import parse

from bin.bin_utils import package_svc, user_svc
from models import mongo_setup
from models.package import Package
from models.release import Release
from models.user import User

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..")))


async def main():
    print("Importing PYPI data.")
    print()
    print("Make sure you have downloaded and unzipped the pypi data set from:")
    print("https://talk-python-course-videos.nyc3.digitaloceanspaces.com/resources/pypi-top-5k.zip")
    print()
    print("Enter the data folder path, e.g. '/Users/mk/Desktop/pypi-raw-data/pypi-top-5k'")
    data_folder = input("Data folder path: ").strip()

    await mongo_setup.global_init(database='pypi')
    await User.delete_all()
    await Package.delete_all()
    await package_svc.reset_release_count()
    user_count = await user_svc.user_count()
    if user_count == 0:
        file_data = do_load_files(data_folder)
        users = find_users(file_data)

        await do_user_import(users)
        await do_import_packages(file_data)

    await do_summary()


async def do_summary():
    print("Final numbers:")
    print(f"Users: {await user_svc.user_count():,}")
    print(f"Packages: {await package_svc.package_count():,}")
    print(f"Releases: {await package_svc.release_count():,}")


async def do_user_import(user_lookup: Dict[str, str]) -> Dict[str, User]:
    print("Importing users ... ", flush=True)
    with progressbar.ProgressBar(max_value=len(user_lookup)) as bar:
        for idx, (email, name) in enumerate(user_lookup.items()):
            user = User(email=email, name=name)
            await user.save()
            bar.update(idx)

    print()
    sys.stderr.flush()
    sys.stdout.flush()

    return {u.email: u for u in await User.find().to_list()}


async def do_import_packages(file_data: List[dict]):
    errored_packages = []
    print("Importing packages and releases ... ", flush=True)
    with progressbar.ProgressBar(max_value=len(file_data)) as bar:
        for idx, p in enumerate(file_data):
            try:
                await load_package(p)
                bar.update(idx)
            except Exception as x:
                errored_packages.append((p, " *** Errored out for package {}, {}".format(p.get('package_name'), x)))
                raise
    sys.stderr.flush()
    sys.stdout.flush()
    print()
    print("Completed packages with {} errors.".format(len(errored_packages)))
    for (p, txt) in errored_packages:
        print(txt)


def do_load_files(data_folder: str) -> List[dict]:
    print("Loading files from {}".format(data_folder))
    files = get_file_names(data_folder)
    print("Found {:,} files, loading ...".format(len(files)), flush=True)
    time.sleep(.1)

    file_data = []
    with progressbar.ProgressBar(max_value=len(files)) as bar:
        for idx, f in enumerate(files):
            file_data.append(load_file_data(f))
            bar.update(idx)

    sys.stderr.flush()
    sys.stdout.flush()
    print()
    return file_data


def find_users(data: List[dict]) -> dict:
    print("Discovering users...", flush=True)
    found_users = {}

    with progressbar.ProgressBar(max_value=len(data)) as bar:
        for idx, p in enumerate(data):
            info = p.get('info')
            found_users.update(get_email_and_name_from_text(info.get('author'), info.get('author_email')))
            found_users.update(get_email_and_name_from_text(info.get('maintainer'), info.get('maintainer_email')))
            bar.update(idx)

    sys.stderr.flush()
    sys.stdout.flush()
    print()
    print("Discovered {:,} users".format(len(found_users)))
    print()

    return found_users


def get_email_and_name_from_text(name: str, email: str) -> dict:
    data = {}

    if not name or not email:
        return data

    emails = email.strip().lower().split(',')
    names = name
    if len(email) > 1:
        names = name.strip().split(',')

    for n, e in zip(names, emails):
        if not n or not e:
            continue

        data[e.strip()] = n.strip()

    return data


def load_file_data(filename: str) -> dict:
    try:
        with open(filename, 'r', encoding='utf-8') as fin:
            data = json.load(fin)
    except Exception as x:
        print("ERROR in file: {}, details: {}".format(filename, x), flush=True)
        raise

    return data


async def load_package(data: dict):
    try:
        info = data.get('info', {})

        package_name = data.get('info', {}).get('name', '').strip()
        if not package_name:
            return

        summary = info.get('summary') or ''
        description = info.get('description') or ''
        try:
            p = Package(id=package_name, summary=summary, description=description)
        except Exception:
            raise

        p.author_name = info.get('author')
        p.author_email = info.get('author_email')

        releases = build_releases(data.get("releases", {}))

        if releases:
            p.created_date = releases[0].created_date
            p.last_updated = releases[-1].created_date

        p.releases.extend(releases)
        p.home_page = info.get('home_page')
        p.docs_url = info.get('docs_url')
        p.package_url = info.get('package_url')

        p.author_name = info.get('author')
        p.author_email = info.get('author_email')
        p.license = detect_license(info.get('license'))

        await p.save()

        await package_svc.increment_release_count(len(p.releases))
    except OverflowError:
        # What the heck, people just putting fake data in here
        # Size is terabytes...
        raise
        pass
    except Exception:
        raise


def detect_license(license_text: str) -> Optional[str]:
    if not license_text:
        return None

    license_text = license_text.strip()

    if len(license_text) > 100 or '\n' in license_text:
        return "CUSTOM"

    license_text = license_text \
        .replace('Software License', '') \
        .replace('License', '')

    if '::' in license_text:
        # E.g. 'License :: OSI Approved :: Apache Software License'
        return license_text \
            .split(':')[-1] \
            .replace('  ', ' ') \
            .strip()

    return license_text.strip()


def build_releases(releases: dict) -> List[Release]:
    db_releases = []
    for k in releases.keys():
        all_releases_for_version = releases.get(k)
        if not all_releases_for_version:
            continue

        v = all_releases_for_version[-1]

        major_ver, minor_ver, build_ver = make_version_num(k)

        release = Release(major_ver=major_ver, minor_ver=minor_ver, build_ver=build_ver)
        release.created_date = parse(v.get('upload_time'))
        release.comment = v.get('comment_text')
        release.url = v.get('url')
        release.size = int(v.get('size', 0))

        db_releases.append(release)

    db_releases.sort(key=lambda r: (r.major_ver, r.minor_ver, r.build_ver))

    return db_releases


def make_version_num(version_text):
    major, minor, build = 0, 0, 0
    if version_text:
        version_text = version_text.split('b')[0]
        parts = version_text.split('.')
        if len(parts) == 1:
            major = try_int(parts[0])
        elif len(parts) == 2:
            major = try_int(parts[0])
            minor = try_int(parts[1])
        elif len(parts) == 3:
            major = try_int(parts[0])
            minor = try_int(parts[1])
            build = try_int(parts[2])

        return major, minor, build


def try_int(text) -> int:
    try:
        return int(text)
    except ValueError:
        return 0


def get_file_names(data_path: str) -> List[str]:
    files = []
    for f in os.listdir(data_path):
        if f.endswith('.json'):
            files.append(
                os.path.abspath(os.path.join(data_path, f))
            )

    files.sort()
    return files


if __name__ == '__main__':
    asyncio.run(main())
