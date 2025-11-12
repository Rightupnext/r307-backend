# models/counter.py
from mongoengine import Document, StringField, IntField

class Counter(Document):
    key = StringField(required=True, unique=True)   # Name of counter, e.g., "bioMetricID"
    value = IntField(default=0)                     # Last used number
