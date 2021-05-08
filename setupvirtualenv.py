import os
import sys

def _exe(cmd):
    print(f'Executing "{cmd}"')
    os.system(cmd)

HERE = os.path.dirname(__file__)
os.chdir(HERE)

if not os.path.exists('venv'):
    _exe(f'virtualenv -p python3 venv')
    # Linux/MacOS uses bin and Windows uses Script, so create
    # a soft link in order to always refer to bin for all
    # platforms.
    if sys.platform == 'win32':
        import _winapi
        target = os.path.join(HERE, 'venv', 'Scripts')
        link = os.path.join(HERE, 'venv', 'bin')
        _winapi.CreateJunction(os.path.abspath(target), link)
else:
    print(f'{os.path.abspath("venv")} already exists')

print(f'Now use ". venv/bin/activate" to enter into the environment.')


    