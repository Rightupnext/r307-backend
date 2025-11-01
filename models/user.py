import datetime
from mongoengine import Document, StringField, IntField, DateTimeField

class User(Document):
    # Personal details
    firstName = StringField()
    middleName = StringField()
    lastName = StringField()
    fatherName = StringField()
    chestNo = StringField()
    rollNo = StringField()
    email = StringField()
    mobileNumber = StringField()
    eduQualification = StringField()
    aadharNumber = StringField()
    identificationMarks_1 = StringField()
    identificationMarks_2 = StringField()
    village = StringField()
    post = StringField()
    tehsil = StringField()
    district = StringField()
    state = StringField()
    pincode = StringField()

    # Physical details
    height = StringField()
    weight = StringField()
    chest = StringField()

    run = StringField()
    pullUp = StringField()
    balance = StringField()
    ditch = StringField()
    medical = StringField()
    tradeTest = StringField()

    # Scoring
    centerName = StringField()
    totalPhysical = StringField()
    totalMarks = StringField()

    # Files
    photo = StringField()
    finger_Template_id = StringField()
    finger_Template_id_2 = StringField()

    # System fields
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

