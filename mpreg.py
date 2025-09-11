

def mpreg(file_path: str, diversity: bool):

    lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()               
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(e)

    for i in range(len(lines)):
        lines[i] = ''.join('🫃' if c == '—' or c == '-' else c for c in lines[i])

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in lines:
                file.write(line)
    except Exception as e:
        print(e)

if __name__=="__main__":
    print("MPREG")
    mpreg(r'/Users/logan/Documents/Visual Studio Projects/Code Scrap/mpreg.txt', diversity=False)
    print("MPREG Out")
