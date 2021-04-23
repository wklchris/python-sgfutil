# Modified from: https://stackoverflow.com/questions/59078333
import code
import enum
import sys
from io import StringIO
import pyperclip
import re

with open('demo.py', 'r', encoding='utf8') as f:
    filestr = f.read()
splits = re.split(r'("""[\s\S]*?""")', filestr)
cmd_str = ''.join([f"READMEAUTO={i}" if s.startswith('"""') else s for i, s in enumerate(splits)])

file = StringIO(cmd_str)
def readfunc(prompt):
    try:
        line = next(file).rstrip()
    except StopIteration:
        raise EOFError
    print(prompt, line, sep='')
    return line

stdout = sys.stdout
sys.stdout = StringIO()
code.interact(readfunc=readfunc)
output = sys.stdout.getvalue()
sys.stdout = stdout

# Post-process: replace back Readme paragraphs
for i, s in enumerate(splits):
    if s.startswith('"""'):
        output = output.replace(f">>> READMEAUTO={i}", "```" + s.strip('"') + "```")
output = output.strip("`") + "```"
print(output)
pyperclip.copy(output)