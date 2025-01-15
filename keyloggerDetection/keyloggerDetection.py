import psutil
import os
import time

def detect_keylogger():
    print("Starting keylogger detection... Press Ctrl+C to stop.")
    while True:
        try:
            keylogger_detected = False
            for process in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # Retrieve process details
                    pid = process.info['pid']
                    name = process.info['name']
                    cmdline = process.info.get('cmdline', [])

                    # Ensure cmdline is iterable
                    if not isinstance(cmdline, list):
                        cmdline = []

                    cmdline_str = ' '.join(cmdline).lower()

                    # Identify Python processes running specific scripts
                    if 'python' in name.lower() or 'python' in cmdline_str:
                        if 'keylogger.py' in cmdline_str or 'listener' in cmdline_str:
                            print(f"[ALERT] Keylogger detected! PID={pid}, Command={cmdline_str}")
                            keylogger_detected = True

                            # Ask user if they want to terminate the process
                            terminate = input("Do you want to terminate this process? (yes/no): ").strip().lower()
                            if terminate == 'yes':
                                os.kill(pid, 9)  # Forcefully terminate the process
                                print(f"Process with PID={pid} terminated.")
                            else:
                                print("Keylogger process left running.")
                            return  # Exit after detection for this demo

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Skip processes that are no longer available or accessible
                    continue

            # Check if no keylogger was detected in this cycle
            if not keylogger_detected:
                print("No keylogger detected.")

            time.sleep(5)  # Check every 5 seconds

        except KeyboardInterrupt:
            print("\nDetection stopped by the user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    detect_keylogger()
