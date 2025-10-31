#!/usr/bin/env python3
from pyfingerprint.pyfingerprint import PyFingerprint
import os, time, glob

SAVE_PATH = "/home/siva/fingerprint"
os.makedirs(SAVE_PATH, exist_ok=True)

def init_sensor():
    try:
        f = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError("Sensor password wrong")

        print("✅ Sensor Connected")
        print("📦 Templates in sensor:", f.getTemplateCount())
        return f

    except Exception as e:
        print("❌ Sensor init failed:", e)
        exit(1)


def safe_convert(f, buffer_id):
    tries = 0
    while True:
        try:
            f.convertImage(buffer_id)
            return True
        except:
            tries += 1
            if tries > 3:
                return False
            print("⚠️ Weak finger image, place again...")
            while not f.readImage():
                pass


def enroll(f):
    username = input("Enter user name for this fingerprint: ").strip()
    print(f"👉 Place finger to enroll for user: {username}")

    # First scan
    while not f.readImage():
        pass

    if not safe_convert(f, 0x01):
        print("❌ Failed to capture first finger image")
        return

    # Check if finger exists already
    pos, score = f.searchTemplate()
    if pos >= 0:
        print(f"⚠️ Finger already exists at ID {pos}")
        return

    print("✋ Remove finger...")
    time.sleep(1)

    print("👉 Place same finger again...")
    while not f.readImage():
        pass

    if not safe_convert(f, 0x02):
        print("❌ Second finger image weak. Try again.")
        return

    # Validate match between scans
    if f.compareCharacteristics() == 0:
        print("❌ Fingerprints do not match. Retry enrollment.")
        return

    # Create final template and store in sensor
    f.createTemplate()
    position = f.storeTemplate()

    # Save template to file
    f.loadTemplate(position, 0x01)
    data = f.downloadCharacteristics(0x01)

    file_path = f"{SAVE_PATH}/finger_{position}_{username}.txt"
    with open(file_path, "w") as file:
        file.write(",".join(map(str, data)))

    print(f"✅ Enrolled Successfully!")
    print(f"🆔 Template ID: {position}")
    print(f"💾 Saved as: {file_path}")


def verify(f):
    print("👉 Place finger to verify...")
    while not f.readImage():
        pass

    f.convertImage(0x01)

    result = f.searchTemplate()
    position = result[0]
    score = result[1]

    if position == -1:
        print("❌ No match found")
        return

    print(f"✅ Finger matched!")
    print(f"🆔 ID: {position} | Score: {score}")

    # Get username from saved file
    file_list = glob.glob(f"{SAVE_PATH}/finger_{position}_*.txt")
    if file_list:
        username = file_list[0].split("_")[-1].replace(".txt", "")
        print(f"👤 User: {username}")
    else:
        print("⚠️ Username file missing")


def delete_all(f):
    print("⚠️ WARNING: This will delete ALL fingerprints!")
    confirm = input("Type YES: ").strip().lower()
    if confirm not in ["yes", "y"]:
        print("❌ Cancelled")
        return

    f.clearDatabase()
    print("🗑️ Sensor memory cleared")

    for file in glob.glob(f"{SAVE_PATH}/*.txt"):
        os.remove(file)

    print("✅ Local fingerprint files deleted!")


if __name__ == "__main__":
    f = init_sensor()

    print("\n--- R307 Fingerprint Menu ---")
    print("1️⃣  Enroll Finger")
    print("2️⃣  Verify Finger")
    print("3️⃣  Delete ALL fingerprints")
    print("------------------------------")

    choice = input("Select option: ")

    if choice == "1":
        enroll(f)
    elif choice == "2":
        verify(f)
    elif choice == "3":
        delete_all(f)
    else:
        print("Invalid option")
