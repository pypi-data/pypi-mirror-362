# tamil/__main__.py

import sys
from tamil.Interpreter import main as tamil_main

def main():
    if len(sys.argv) < 2:
        print("❌ கோப்பு பெயரை கொடுக்கவும்! (Please provide a Tamil source file.)")
        print("உதாரணம் (Example): python -m tamil myfile.tamil")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        tamil_main(filename)
    except Exception as e:
        print(f"⚡ கோப்பை இயக்க முடியவில்லை! (Error running file: {e})")
        sys.exit(1)

if __name__ == "__main__":
    main()
