
def grep_log():
    try:
        with open("run_error.log", "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if "Normalized columns" in line:
                    print(line.strip())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    grep_log()
