import time, base64
from models.user import User
from utils.sensor_manager import get_sensor, stop_sensor

READ_POLL_INTERVAL = 0.08
MIN_COMPARE_SCORE_ENROLL = 50
MIN_COMPARE_SCORE_VERIFY = 60


def _wait_for_image(sensor, timeout=None):
    start = time.time()
    while True:
        try:
            if sensor.readImage():
                return True
        except:
            return False

        time.sleep(READ_POLL_INTERVAL)
        if timeout and time.time() - start >= timeout:
            return False


def enroll_fingerprint(port, timeout=20):
    try:
        sensor, lock = get_sensor(port)
    except Exception as e:
        return {"status": "error", "message": f"Sensor init failed: {e}"}

    with lock:
        if not _wait_for_image(sensor, timeout):
            return {"status": "error", "message": "Timeout waiting for finger"}

        sensor.convertImage(0x01)
        time.sleep(0.3)

        if not _wait_for_image(sensor, timeout):
            return {"status": "error", "message": "Timeout second scan"}

        sensor.convertImage(0x02)

        try:
            score = sensor.compareCharacteristics()
        except:
            return {"status": "error", "message": "Compare failed"}

        if score < MIN_COMPARE_SCORE_ENROLL:
            return {"status": "error", "message": f"Mismatch score={score}"}

        sensor.createTemplate()
        chars = sensor.downloadCharacteristics()

        # Convert fingerprint to bytes
        try:
            template_bytes = bytes(chars)
        except:
            template_bytes = bytes([int(x) & 0xFF for x in chars])

        # ? Convert to Base64 to send to frontend safely
        base64_template = base64.b64encode(template_bytes).decode()

        return {"status": "success", "template_bytes": template_bytes, "template_b64": base64_template}
        

def _to_list(data):
    if isinstance(data, (bytes, bytearray)):
        return list(data)
    if isinstance(data, list):
        return [int(x) & 0xFF for x in data]
    try:
        return list(bytes(data))
    except:
        return None


def verify_fingerprint(port, timeout=10):
    try:
        sensor, lock = get_sensor(port)
    except:
        return False, None, 0

    with lock:
        if not _wait_for_image(sensor, timeout):
            return False, None, 0

        sensor.convertImage(0x01)
        sensor.createTemplate()
        live = sensor.downloadCharacteristics()

        users = User.objects.only("firstName", "rollNo", "chestNo", "finger1", "finger2")

        for user in users:
            for field in ["finger1", "finger2"]:
                stored = getattr(user, field, None)
                if not stored:
                    continue

                stored_list = _to_list(stored)
                if not stored_list:
                    continue

                try:
                    sensor.uploadCharacteristics(0x01, list(live))
                    sensor.uploadCharacteristics(0x02, list(stored_list))
                    score = sensor.compareCharacteristics()
                except:
                    continue

                if score >= MIN_COMPARE_SCORE_VERIFY:
                    return True, user, score

        return False, None, 0


def stop_fingerprint_scan(port):
    try: stop_sensor(port)
    except: pass
    return True
