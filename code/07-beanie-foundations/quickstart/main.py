import asyncio

import beanie
import motor.motor_asyncio
import pydantic
import pymongo


async def main():
    await init_db()
    await insert_data()
    await list_data()
    print("Done")


class Student(beanie.Document):
    name: str
    years_exp: int
    languages: list[str]

    class Collection:
        name = "students"

        indexes = [
            pymongo.IndexModel(keys=[("years_exp", pymongo.ASCENDING)], name="years_exp_ascend"),
            pymongo.IndexModel(keys=[("languages", pymongo.ASCENDING)], name="languages_ascend"),
        ]


async def list_data():
    lang = input("What language do you want to hire for? ")
    # What about a cursor?
    students = Student.find(Student.languages == lang).sort("-years_exp")
    # students = await Student.find(Student.languages == lang).sort((Student.years_exp, -1)).to_list()

    async for s in students:
        print(f'{s.name} knows {lang} and has {s.years_exp} years experience.')


async def insert_data():
    if await Student.count() > 0:
        print("We already have students, no import!")
        return

    s1 = Student(name="Michael", years_exp=20, languages=['C++', 'C#', 'JavaScript', 'Python'])
    s2 = Student(name="Roller", years_exp=5, languages=['Python', 'Ruby'])
    s3 = Student(name="Doug", years_exp=20, languages=['C', 'C++', 'APL', 'Python'])
    await s1.save()
    await s2.save()
    await s3.save()


async def init_db():
    conn_str = 'mongodb://localhost:27017'
    db_client = motor.motor_asyncio.AsyncIOMotorClient(conn_str)

    await beanie.init_beanie(db_client['maven_class'], document_models=[Student])


if __name__ == '__main__':
    asyncio.run(main())
