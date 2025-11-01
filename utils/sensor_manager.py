# utils/sensor_manager.py
import threading
import time
from pyfingerprint.pyfingerprint import PyFingerprint

# Configure ports you expect to use here (or set dynamically)
DEFAULT_PORTS = ["/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3"]

class SensorManager:
    def __init__(self):
        # lock for each port
        self._locks = {p: threading.Lock() for p in DEFAULT_PORTS}
        # cached sensor instances
        self._sensors = {}
        # connection parameters (change if needed)
        self._baudrate = 57600
        self._address = 0xFFFFFFFF
        self._password = 0x00000000

    def register_port(self, port):
        """Ensure a lock exists for a given port (safe to call multiple times)."""
        if port not in self._locks:
            self._locks[port] = threading.Lock()

    def get_lock(self, port):
        self.register_port(port)
        return self._locks[port]

    def init_sensor(self, port, force_reinit=False):
        """
        Initialize and cache a PyFingerprint instance for the port.
        Returns a PyFingerprint object.
        """
        if not force_reinit and port in self._sensors:
            return self._sensors[port]

        # create new instance (may raise)
        sensor = PyFingerprint(port, self._baudrate, self._address, self._password)
        if not sensor.verifyPassword():
            raise RuntimeError(f"Sensor password verification failed for {port}")

        self._sensors[port] = sensor
        return sensor

    def get_sensor(self, port):
        """
        Returns tuple (sensor_instance, lock) for use.
        Will attempt to init sensor on first call.
        """
        lock = self.get_lock(port)
        sensor = self.init_sensor(port)
        return sensor, lock

    def try_cancel(self, port):
        """Attempt to cancel any ongoing operation on the sensor (safe)."""
        try:
            sensor = self.init_sensor(port)
            # different libraries use different names; try both.
            if hasattr(sensor, "cancel"):
                sensor.cancel()
            elif hasattr(sensor, "cancelOperation"):
                sensor.cancelOperation()
        except Exception:
            # ignore errors when cancelling (sensor may be unplugged)
            pass

# singleton manager
sensor_manager = SensorManager()

# convenience functions
def get_sensor(port):
    return sensor_manager.get_sensor(port)

def init_sensor(port, force_reinit=False):
    return sensor_manager.init_sensor(port, force_reinit=force_reinit)

def stop_sensor(port):
    return sensor_manager.try_cancel(port)
