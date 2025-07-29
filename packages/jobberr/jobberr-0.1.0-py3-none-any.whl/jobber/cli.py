import sys
import os

def main():
    command, raw_path = sys.argv[1] ,sys.argv[2]
    directory = os.path.abspath(os.path.expanduser(raw_path))

    if not os.path.isdir(directory):
        print(f"not a directory")
        sys.exit(1)

    if command == "list":
        for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
            print(f"Directory Path: {dirpath}")
            print(f"Subdirectories: {dirnames}")
            print(f"Files: {filenames}")
            print()

    elif command == "run":
        for name in os.listdir(directory):
            full_path = os.path.join(directory, name)
            if os.path.isfile(full_path):
                print("Executing file : " + full_path)
                exec(open(full_path).read())


if __name__ == "__main__":
    main()