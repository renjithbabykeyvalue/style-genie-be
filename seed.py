from mongoengine import *
from src.models.models import User, UserProfile, Designer, Fabric, Outfit, UserMeasurement, DefaultOption, CustomisedOption, Order
from datetime import datetime  # Import datetime module


def seed_database():
    userOne = User(
        email="anagha123@gmail.com",
        firstName="Anagha",
        lastName="Suresh",
        dob=datetime(2000, 11, 26)
    )
    userOne.save()

    userTwo = User(
        email="swathi321@gmail.com",
        firstName="Sreedivya",
        lastName="Nambiar",
        dob=datetime(1997, 10, 18)
    )
    userTwo.save()


if __name__ == "__main__":
    seed_database()
