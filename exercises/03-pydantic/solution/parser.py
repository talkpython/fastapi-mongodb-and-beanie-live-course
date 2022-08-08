import json
from pathlib import Path


from models import PackageModel


def main():
    file = Path(__file__).parent / 'pydantic.json'
    with open(file, 'r', encoding='utf-8') as fin:
        data = json.load(fin)

    package = PackageModel(**data)

    print(f"We've loaded {package.info.name}.")
    print(f"It has had {len(package.releases)} releases.")
    print(f"And is maintained by {package.info.author}.")


if __name__ == '__main__':
    main()
