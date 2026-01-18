
def grep_head():
    try:
        with open("run_error.log", "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            printing = False
            for line in lines:
                if "First row raw" in line:
                    printing = True
                if printing:
                    print(line.strip())
                    if "Parsed DataFrame shape" in line: # Stop after next log
                        break
    except Exception as e:
        print(e)

if __name__ == "__main__":
    grep_head()
