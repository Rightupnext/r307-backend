# controllers/fingerprint_controller.py
import time
from models.user import User
from utils.sensor_manager import get_sensor, init_sensor, stop_sensor

# tunables
READ_POLL_INTERVAL = 0.08  # seconds between readImage polls
MIN_COMPARE_SCORE_ENROLL = 50
MIN_COMPARE_SCORE_VERIFY = 60

def _wait_for_image(sensor, timeout=None):
    """
    Wait until sensor.readImage() returns True.
    If timeout is None, waits indefinitely. Returns True if image read, False if timed out.
    """
    start = time.time()
    while True:
        try:
            if sensor.readImage():
                return True
        except Exception:
            # sometimes readImage raises when connection is flaky
            return False

        time.sleep(READ_POLL_INTERVAL)
        if timeout is not None and (time.time() - start) >= timeout:
            return False

def enroll_fingerprint(port, read_timeout=20):
    """
    Enroll fingerprint on given port. Returns dict:
      {"status": "success", "template": bytes([...])} or
      {"status": "error", "message": "..."}
    """
    try:
        sensor, lock = get_sensor(port)
    except Exception as e:
        return {"status": "error", "message": f"Could not initialize sensor: {e}"}

    with lock:
        # 1st scan
        if not _wait_for_image(sensor, timeout=read_timeout):
            return {"status": "error", "message": "Timeout waiting for first scan"}

        sensor.convertImage(0x01)

        time.sleep(0.3)  # short settle

        # 2nd scan (for match)
        if not _wait_for_image(sensor, timeout=read_timeout):
            return {"status": "error", "message": "Timeout waiting for second scan"}

        sensor.convertImage(0x02)

        try:
            score = sensor.compareCharacteristics()
        except Exception as e:
            return {"status": "error", "message": f"Failed to compare characteristics: {e}"}

        if score < MIN_COMPARE_SCORE_ENROLL:
            return {"status": "error", "message": f"Two scans mismatch (score={score})"}

        try:
            sensor.createTemplate()
            characteristics = sensor.downloadCharacteristics()  # list of ints
        except Exception as e:
            return {"status": "error", "message": f"Failed to create/download template: {e}"}

        # convert to bytes for storage (common pattern). DB field should accept binary.
        try:
            template_bytes = bytes(characteristics)
        except Exception:
            # characteristics may already be bytes or other type
            if isinstance(characteristics, (bytes, bytearray)):
                template_bytes = bytes(characteristics)
            else:
                # fallback: convert each item to int then bytes
                template_bytes = bytes(int(x) & 0xFF for x in characteristics)

        return {"status": "success", "template": template_bytes}

def _to_int_list_from_stored(data):
    """
    Convert stored template (bytes, bytearray, list[int]) to list[int] suitable for uploadCharacteristics.
    """
    if data is None:
        return None
    if isinstance(data, (bytes, bytearray)):
        return list(data)
    if isinstance(data, list):
        return [int(x) & 0xFF for x in data]
    # If DB stored as memoryview or pymongo Binary
    try:
        return list(bytes(data))
    except Exception:
        raise ValueError("Unsupported fingerprint data type")

def verify_fingerprint(port, read_timeout=10):
    """
    Verify live finger against stored templates.
    Returns (match_bool, user_obj_or_None, score_int)
    """
    try:
        sensor, lock = get_sensor(port)
    except Exception:
        return False, None, 0

    with lock:
        # wait for user to place finger
        if not _wait_for_image(sensor, timeout=read_timeout):
            return False, None, 0

        sensor.convertImage(0x01)
        # create template for live (slot 1)
        try:
            sensor.createTemplate()
            live_chars = sensor.downloadCharacteristics()
        except Exception:
            return False, None, 0

        # iterate over users and compare
        users = User.objects()  # may be large - consider indexing or limiting in production

        for user in users:
            for fp_field in ("finger1", "finger2"):
                stored = getattr(user, fp_field, None)
                if not stored:
                    continue

                try:
                    stored_list = _to_int_list_from_stored(stored)
                except Exception:
                    # skip templates that can't be interpreted
                    continue

                try:
                    # upload live into slot 0x01 and stored into slot 0x02
                    sensor.uploadCharacteristics(0x01, list(live_chars))
                    sensor.uploadCharacteristics(0x02, list(stored_list))
                    score = sensor.compareCharacteristics()
                except Exception:
                    # if upload/compare fails for any user/template, continue
                    continue

                if score >= MIN_COMPARE_SCORE_VERIFY:
                    # matched
                    return True, user, score

        return False, None, 0

def stop_fingerprint_scan(port):
    """
    Try to cancel any ongoing operation on the sensor.
    """
    try:
        stop_sensor(port)
    except Exception:
        pass
    return True
