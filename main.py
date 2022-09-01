import sqlite3
from pydantic.typing import Literal

from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn

#
app = FastAPI()

connection = sqlite3.connect("survey.db")
# creates the table
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS covid19 ("
               "wardNum TEXT, "
               "gender TEXT, "
               "age TEXT, "
               "highestLevelEducation TEXT, "
               "income TEXT, "
               "receivedVaccine TEXT, "
               "livingConditionsRating TEXT, "
               "mentalHealthRating TEXT, "
               "isUnemployed TEXT, "
               "basicNecessitiesAccessible TEXT, "
               "email TEXT, "
               "signature TEXT)")
connection.commit()


# this makes the values that each object can accept
class Data(BaseModel):
    wardNum: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    gender: Literal['Male', 'Female', 'Other']
    ageRange: Literal['0 - 17', '18 - 25', '26 - 30', '30 - 40', '41 - 50', '51 - 60', '61 - 70', '71 - 80', '81+']
    highestLevelEducation: Literal[
        'below highschool diploma', 'highschool diploma', 'college diploma', 'undergraduate degree', 'graduate degree']
    incomeRange: Literal[
        '0 - 25k', '25k - 40k', '40k - 50k', '50k - 60k', '60k - 70k', '70k - 80k', '80k - 90k', '90k - 100k', '100k+']
    receivedVaccine: Literal["yes", "no"]
    livingConditionsRating: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    mentalHealthRating: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    isUnemployed: Literal["yes", "no"]
    basicNecessitiesAccessible: Literal["yes", "no"]
    email: str
    signature: str


# Enter values in to the database
@app.post("/add")
async def covid19(data: Data):
    print(data)
    cursor.execute("INSERT INTO covid19 VALUES (?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data.wardNum,
                                                                                      data.gender,
                                                                                      data.ageRange,
                                                                                      data.highestLevelEducation,
                                                                                      data.incomeRange,
                                                                                      data.receivedVaccine,
                                                                                      data.livingConditionsRating,
                                                                                      data.mentalHealthRating,
                                                                                      data.isUnemployed,
                                                                                      data.basicNecessitiesAccessible,
                                                                                      data.email,
                                                                                      data.signature))
    connection.commit()

    return {"success": 200}