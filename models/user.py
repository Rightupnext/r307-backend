from mongoengine import Document, StringField, DateTimeField, IntField
import datetime

class User(Document):

    # Finger Template
    finger_Template_id = StringField()
    finger_Template_id_2 = StringField()

    # Basic Details
    rollNo = StringField()
    chestNo = StringField()
    firstName = StringField(required=True, max_length=100)
    lastName = StringField()
    middleName = StringField()
    fatherName = StringField()
    dateOfBirth = DateTimeField()

    # Contact
    email = StringField()
    mobileNumber = StringField()
    aadharNumber = StringField(max_length=16)
    address = StringField()
    pincode = StringField()

    # Education & Trade
    eduQualification = StringField()
    trade = StringField()
    centerName = StringField()

    # Location
    village = StringField()
    post = StringField()
    tehsil = StringField()
    district = StringField()
    state = StringField()
    police_station = StringField()

    # Identification
    identificationMarks_1 = StringField()
    identificationMarks_2 = StringField()
    photo = StringField()

    # Physical Test
    height = IntField()
    weight = IntField()
    chest = StringField()
    run = StringField()
    pullUp = IntField()
    balance = StringField()
    ditch = StringField()
    medical = StringField()

    # Marks
    tradeTest = IntField()
    totalPhysical = IntField()
    totalMarks = IntField()

    # Extra
    remarks = StringField()
    exam_centre = StringField()
    mod_status = StringField()

    # System fields
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)
