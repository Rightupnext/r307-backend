from pyfingerprint.pyfingerprint import PyFingerprint
import time

def init_sensor():
    try:
        f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

        if (f.verifyPassword() == False):
            raise ValueError('Fingerprint sensor password is wrong!')

        print('? Sensor connected')
        print('Templates used: ' + str(f.getTemplateCount()))
        print('Capacity: ' + str(f.getStorageCapacity()))
        return f

    except Exception as e:
        print('? Failed to initialize sensor: ' + str(e))
        exit(1)

def enroll(f):
    print('?? Put finger to enroll...')

    # Wait for finger
    while f.readImage() == False:
        pass

    f.convertImage(0x01)

    # Check if already exists
    result = f.searchTemplate()
    position = result[0]

    if position >= 0:
        print(f'?? Finger already exists at ID {position}')
        return

    print('? Remove finger...')
    time.sleep(2)

    print('?? Place same finger again...')
    while f.readImage() == False:
        pass

    f.convertImage(0x02)

    if f.compareCharacteristics() == 0:
        print('? Fingers do not match')
        return

    f.createTemplate()
    position = f.storeTemplate()

    print(f'? Enrolled successfully! Template ID: {position}')

def verify(f):
    print('?? Place finger to verify')

    while f.readImage() == False:
        pass

    f.convertImage(0x01)
    result = f.searchTemplate()
    position = result[0]
    score = result[1]

    if position == -1:
        print('? No match found')
    else:
        print(f'? Match found! ID = {position}, Score = {score}')

if __name__ == '__main__':
    f = init_sensor()

    print("\n--- R307 Fingerprint Menu ---")
    print("1: Enroll Finger")
    print("2: Verify Finger")
    print("------------------------------\n")

    choice = input("Select (1/2): ")

    if choice == '1':
        enroll(f)
    elif choice == '2':
        verify(f)
    else:
        print("Invalid choice")
