from pyfingerprint.pyfingerprint import PyFingerprint
import base64, time
from models.user import User
def init_sensor():
    f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise Exception("Fingerprint sensor password wrong")
    return f

sensor = init_sensor()

def capture_finger_template():
    while not sensor.readImage():
        pass
    
    sensor.convertImage(0x01)
    sensor.createTemplate()
    chars = sensor.downloadCharacteristics(0x01)
    
    return base64.b64encode(bytes(chars)).decode("utf-8")
def verify_fingerprint():
    # Capture Live Finger
    live_template = capture_finger_template()

    # Loop through all Users in DB
    users = User.objects()  

    for user in users:
        for stored in [user.finger1, user.finger2]:

            if not stored:
                continue

            # Convert DB binary ? list of ints
            stored_template = list(stored)

            # Upload stored template into charbuffer2
            sensor.uploadCharacteristics(0x02, stored_template)

            # Compare with live charbuffer1
            score = sensor.compareCharacteristics()

            if score > 40:  # matching threshold
                return True, user

    return False, None

def stop_fingerprint_scan():
    """ ? Stop current capture & reset sensor """
    global stop_scan
    stop_scan = True
    try:
        sensor.cancel()        # Stop internal process
    except:
        pass
    return True