from tamil.PowerFullInterpreter import PowerFullInterpreter
import sys

def main():
    if len(sys.argv) < 2:
        print("பயன்பாடு: tamil <கோப்பு>")
        sys.exit(1)
    filename = sys.argv[1]
    with open(filename, encoding="utf-8") as f:
        source = f.read()

    interpreter = PowerFullInterpreter()
    interpreter.execute(source)

if __name__ == "__main__":
    main()
