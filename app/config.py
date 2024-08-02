import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'sxFRqyXN2l9JrjSnA-384AvcrQEXXIgM6IfyqR0gccw')
    API_KEYS = {
        'nsw': os.getenv('API_KEY_NSW'),
        'vic': os.getenv('API_KEY_VIC'),
        'qld': os.getenv('API_KEY_QLD'),
        'wa': os.getenv('API_KEY_WA')
    }