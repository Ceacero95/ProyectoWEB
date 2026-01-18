
import os

def read_log():
    if os.path.exists("run_error.log"):
        with open("run_error.log", "r", encoding="utf-8", errors="replace") as f:
            print(f.read())
    else:
        print("Log file not found.")

if __name__ == "__main__":
    read_log()
