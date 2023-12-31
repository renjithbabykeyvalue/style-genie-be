from mongoengine import *


class User(Document):
    email = StringField(default="")
    firstName = StringField(default="")
    lastName = StringField(default="")
    dob = DateTimeField()


class UserProfile(Document):
    nickname = StringField(default="")
    gender = StringField(default="")
    user = ReferenceField(User)


class Designer(Document):
    name = StringField(default="")
    email = StringField(default="")
    phoneNumber = StringField(default="")
    location = StringField(default="")


class Fabric(Document):
    name = StringField(default="")
    designer = ReferenceField(Designer)
    image_url = StringField(default="")
    price_per_meter = IntField(required=True)


class Outfit(Document):
    name = StringField(default="")
    designer = ReferenceField(Designer)
    image_url = StringField(default="")
    default_price = IntField(required=True)
    category = StringField(default="")
    description = StringField(default="")
    tags = ListField(StringField())


class UserMeasurement(Document):
    userProfile = ReferenceField(UserProfile)
    height = FloatField()
    inseamLength = FloatField()
    hipSize = FloatField()
    chestSize = FloatField()
    shoulder = FloatField()


class DefaultOption(Document):
    outfit = ReferenceField(Outfit)
    fabric = ReferenceField(Fabric)
    neckPattern = StringField(default="")
    sleevePattern = StringField(default="")
    dyeable = StringField(default="")
    image_url = StringField(default="")


class CustomisedOption(Document):
    userProfile = ReferenceField(UserProfile)
    outfit = ReferenceField(Outfit)
    fabric = ReferenceField(Fabric)
    neckPattern = StringField(default="")
    sleevePattern = StringField(default="")


class Order(Document):
    user = ReferenceField(User)
    UserProfile = ReferenceField(UserProfile)
    outfit = ReferenceField(Outfit)
    customisedOption = ReferenceField(CustomisedOption)
    totalPrice = StringField(default="")
    status = StringField(default="")
