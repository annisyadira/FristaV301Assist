import os, time, argparse, base64
from pywinauto import Application, mouse, findwindows, keyboard

parser = argparse.ArgumentParser(description="Process arguments.")

parser.add_argument('--fristainput', type=int, help="Input No BPJS / No KTP")
args = parser.parse_args()

config_file = 'config.txt'

config = {}
with open(config_file, 'r') as f:
    for line in f:
        if '==' in line:
            key, value = line.strip().split('==', 1)
            config[key] = value

destination = config.get("destination")

def click_relative(window, x_gap, y_gap):
    window_rect = window.rectangle()
    window_x = window_rect.left
    window_y = window_rect.top

    # Calculate the screen position based on the window's position
    screen_x = window_x + x_gap
    screen_y = window_y + y_gap

    # Click at the calculated position
    mouse.click(coords=(screen_x, screen_y))

def login(login_windows_dlg):
    # Click within the rectangle (adjust coordinates to center of rectangle)
    click_relative(login_windows_dlg, 575, 307)  # Username field
    login_windows_dlg.type_keys(config.get("username"))

    base64_string = config.get("password")
    base64_bytes = base64_string.encode("ascii")
    password_string_bytes = base64.b64decode(base64_bytes)
    password_string = password_string_bytes.decode("ascii")

    click_relative(login_windows_dlg, 575, 392)  # Password field
    login_windows_dlg.type_keys(password_string)

    # Click login button
    click_relative(login_windows_dlg, 504, 498)
    time.sleep(2)

if destination.endswith("txt"):
    with open(destination, 'w') as file:
        file.write(f"{args.fristainput}")

    print(f"Data written to file: {destination}")

    # Open the file after writing
    if os.name == 'nt':
        os.system(f'start {destination}')  # For Windows
    elif os.name == 'posix':
        os.system(f'xdg-open {destination}')  # For Linux/MacOS

elif destination.endswith("exe"):
    try:
        try:
            home_windows = Application(backend="win32").connect(title="Frista (Face Recognition BPJS Kesehatan)")
            home_windows_dlg = home_windows.window(title="Frista (Face Recognition BPJS Kesehatan)")
        except findwindows.ElementNotFoundError:  
            try:              
                login_windows = Application(backend="win32").connect(title="Login Frista (Face Recognition BPJS Kesehatan)")
                login_windows_dlg = login_windows.window(title="Login Frista (Face Recognition BPJS Kesehatan)")
            except findwindows.ElementNotFoundError:
                login_windows = Application().start(destination)
                login_windows = Application(backend="win32").connect(title="Login Frista (Face Recognition BPJS Kesehatan)")
                login_windows_dlg = login_windows.window(title="Login Frista (Face Recognition BPJS Kesehatan)")
            finally:
                login(login_windows_dlg)

                home_windows = Application(backend="win32").connect(title="Frista (Face Recognition BPJS Kesehatan)")
                home_windows_dlg = home_windows.window(title="Frista (Face Recognition BPJS Kesehatan)")
        finally:
            click_relative(home_windows_dlg, 1199, 178)
            # keyboard.send_keys("^a{DELETE}")
            home_windows_dlg.type_keys(args.fristainput)

        print(f".exe file '{destination}' launched with data.")
    except Exception as e:
        print(f"Failed to launch .exe file. Error: {e}")