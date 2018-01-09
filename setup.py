import sys
from cx_Freeze import setup, Executable

setup(
	name = "ConProfile",
	version = "1.0",
	description = "The face recognition and searching for you.",
	executables = [Executable("facerecog.py", base = "Win32GUI")])