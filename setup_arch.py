import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == 'win32':
    base = "Win32GUI"


executables = [Executable("facerecog.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
    },

}

setup(
    name = "ConProfile",
    options = options,
    version = "0.01",
    description = 'face recognition and searching for you.',
    executables = executables
)
