import readline
import sys

def complete(text, state):
    #print(f"text: {text}", file=sys.stderr)
    options = ["$hello", "$world"]
    #options = ["hello", "world"]
    matches = [option for option in options if option.startswith(text)]
    #print(f"text: {text}, state: {state}", file=sys.stderr)
    return matches[state]

readline.set_completer_delims(' \t\n;')
readline.set_completer(complete)
readline.parse_and_bind("tab: complete")

while True:
    line = input(">>> ")
    print(line)

