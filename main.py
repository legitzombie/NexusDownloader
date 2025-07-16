import pyautogui
import mss
from PIL import Image
import time
import pyscreeze
import threading
import keyboard

stop_flag = False

def monitor_stop_key():
    global stop_flag
    while True:
        if keyboard.read_event().name == "f10":
            stop_flag = True
            print("F10 pressed. Stopping.\n")
            break

def find_button(image_path, confidence=0.98):
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            screenshot = sct.grab(monitor)
            haystack = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
            needle = Image.open(image_path)
            box = pyscreeze.locate(needle, haystack, confidence=confidence)
            if box:
                return pyautogui.center(box)
    except Exception:
        pass
    return None

def wait_until_disappears(image_path, timeout=10, confidence=0.98):
    start = time.time()
    while time.time() - start < timeout and not stop_flag:
        if not find_button(image_path, confidence):
            return True
        time.sleep(0.2)
    return False  # Timed out

def wait_until_appears(image_path, timeout=10, confidence=0.98):
    start = time.time()
    while time.time() - start < timeout and not stop_flag:
        loc = find_button(image_path, confidence)
        if loc:
            return loc
        time.sleep(0.2)
    return None

def click_button_if_found(image_path, confidence=0.98):
    location = find_button(image_path, confidence)
    if location:
        pyautogui.click(location)
        print(f"Clicked {image_path} at {location}\n")
        return True
    return False

# Start key monitoring thread
threading.Thread(target=monitor_stop_key, daemon=True).start()

print("Running.\nPress F10 to stop.\n")

while not stop_flag:

    loc = find_button("assets/resumebtn.png")
    if loc:
        pyautogui.click(loc)
                
    loc = find_button("assets/downloadbtn.png")
    if loc:
        pyautogui.click(loc)
        print(f"Clicked downloadbtn at {loc}")

        # Wait for it to disappear to confirm it worked
        print("Waiting for downloadbtn to disappear...\n")
        if wait_until_disappears("assets/downloadbtn.png", timeout=10):
            print("Confirmed downloadbtn disappeared.\n")
            # Now wait for slowdownloadbtn to appear
            print("Waiting for slowdownloadbtn to appear...\n")
            slow_loc = wait_until_appears("assets/slowdownloadbtn.png", timeout=10)
            if slow_loc:
                pyautogui.click(slow_loc)
                print(f"Clicked slowdownloadbtn at {slow_loc}\n")
                time.sleep(6)
            else:
                print("Timeout waiting for slowdownloadbtn.\n")
        else:
            print("Download button didn't disappear. Likely misclick.\n")
            time.sleep(1)
    else:
        time.sleep(0.2)

print("Stopped.")
