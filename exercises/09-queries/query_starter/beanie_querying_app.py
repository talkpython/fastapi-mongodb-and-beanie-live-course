def main():
    # TODO: Setup DB
    print("--------------------------")
    print(" PyPI CLI ")
    print("--------------------------")
    print()

    pc = 1  # TODO: package_count
    rc = 2  # TODO: release_count
    print(f"We have {pc:,} packages with {rc:,} releases.")

    latest = []  # TODO: latest_packages
    print("The latest 5 packages are:")
    for p in latest:
        r: "Release|None" = None  # TODO: get_latest_release_for_package
        if not r:
            print(f'* {p.id}')
        else:
            print(f'* {p.id:<10} with latest release on {r.created_date.isoformat().replace("T", " ")}')
    print()
    print("Boto package:")
    # TODO: get_package_by_id('boto3')
    print(p := "PACKAGE")
    print()
    # TODO: user_count
    print(f"We have {0:,} users.")

    print("Let's create one more:")
    name = input("What's there name? ").strip()
    email = name.replace(' ', '-') + '@gmail.com'
    # TODO: create_account(name, email, "a")
    # TODO: Catch duplicate account errors, pymongo.errors.DuplicateKeyError

    # TODO: Count users again
    print(f"Now there are {0:,} users.")
    # TODO: get_user_by_email
    user = None
    print(f"We added {user}!")




if __name__ == '__main__':
    main()
