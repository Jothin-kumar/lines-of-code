"""
MIT License

Copyright (c) 2021 B.Jothin kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Author: Jothin kumar (https://jothin.tech)
Github repository of this project: https://github.com/Jothin-kumar/lines-of-code
"""
from sys import argv
from os import system

if '-h' in argv or '--help' in argv:
    print("""Lines of code. (https://github.com/Jothin-kumar/lines-of-code)
- Run "lines-of-code --GUI" for GUI version.
- Run "lines-of-code --CLI" or "lines-of-code --CLI" for CLI version.""")
elif '--GUI' in argv:
    system('cd /lines-of-code && python3 GUI.py')
elif '--CLI' in argv or '--terminal' in argv:
    system('cd /lines-of-code && python3 CLI.py')
elif 'setup' in argv or 'troubleshoot' in argv:
    system('sudo apt-get install python3')
    system('sudo apt-get install python3-pip')
    system('sudo apt-get install python3-tk')
    system('cd /lines-of-code && python3 -m pip install -r requirements.txt')
else:
    system('cd /lines-of-code && python3 GUI.py')
