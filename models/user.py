import datetime
from mongoengine import Document, StringField, IntField, DateTimeField,BinaryField 

class User(Document):
    # Personal details
    firstName = StringField()
    middleName = StringField()
    lastName = StringField()
    fatherName = StringField()
    chestNo = StringField()
    rollNo = StringField()
    email = StringField()
    dateOfBirth = DateTimeField()
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
    trade = StringField()
    police_station = StringField()

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
    finger1 = BinaryField()
    finger2 = BinaryField()

    # System fields
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

