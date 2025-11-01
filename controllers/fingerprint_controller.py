from pyfingerprint.pyfingerprint import PyFingerprint
import base64, time
from models.user import User
def init_sensor():
    sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)
    if not sensor.verifyPassword():
        raise Exception("Fingerprint sensor password wrong")
    return sensor

sensor = init_sensor()

# Convert template list -> base64
def template_to_base64(template_list):
    return base64.b64encode(bytes(template_list)).decode('utf-8')

# Convert base64 -> template list
def base64_to_template(b64):
    data = base64.b64decode(b64)
    return list(data)

def capture_finger_template(min_quality=60):
    # Wait for finger
    while not sensor.readImage():
        pass
    
    # Convert to characteristics
    sensor.convertImage(0x01)

    # Read quality (if sensor supports)
    try:
        quality = sensor.getImageQuality()
    except:
        quality = 100

    if quality < min_quality:
        return {
            "status": "low_quality",
            "quality": quality,
            "message": "Please scan again, fingerprint quality is too low"
        }

    # Create template & download as list
    sensor.createTemplate()
    template = sensor.downloadCharacteristics(0x01)

    # Convert template list to base64 string for DB
    template_b64 = template_to_base64(template)

    return {
        "status": "success",
        "quality": quality,
        "template": template_b64,  # ?? Base64
        "sensor": "R307",
        "format": "raw_template"
    }

def verify_fingerprint():
    live = capture_finger_template()

    if live["status"] == "low_quality":
        return False, live

    live_template = base64_to_template(live["template"])
    users = User.objects()

    for user in users:
        for stored_template_bin in [user.finger1, user.finger2]:
            if not stored_template_bin:
                continue

            # Convert binary -> base64 -> list
            stored_template_b64 = base64.b64encode(stored_template_bin).decode('utf-8')
            stored_template = base64_to_template(stored_template_b64)

            sensor.uploadCharacteristics(0x01, live_template)
            sensor.uploadCharacteristics(0x02, stored_template)

            score = sensor.compareCharacteristics()

            if score > 40:
                return True, user

    return False, None

def stop_fingerprint_scan():
    try:
        sensor.cancel()
    except:
        pass
    return True