def read_lines(file_path: str) -> list[str]:
    with open(file_path, 'r') as file:
        content = [line[:-1] if line[-1] == '\n' else line for line in file]
    return content


if __name__ == "__main__":
    print("This is lower library file. Import, but don't run.")
