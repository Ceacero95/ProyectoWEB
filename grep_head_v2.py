
def grep_head_v2():
    try:
        with open("run_error.log", "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "First row raw" in line:
                    print("FOUND HEAD:")
                    print(line.strip())
                    # Print next 3 lines which contain the dataframe string representation
                    for j in range(1, 4):
                        if i+j < len(lines):
                            print(lines[i+j].rstrip())
                    break
    except Exception as e:
        print(e)

if __name__ == "__main__":
    grep_head_v2()
