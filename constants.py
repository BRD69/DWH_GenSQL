import os
import sys

if getattr(sys, 'frozen', False):
    Current_Path = os.path.dirname(sys.executable)
else:
    Current_Path = str(os.path.dirname(__file__))

TR_FOLDER = os.path.join(Current_Path, os.getcwd(), "tr")
BIN_FOLDER = os.path.join(Current_Path, os.getcwd(), "bin")
LOG_FOLDER = os.path.join(Current_Path, os.getcwd(), "log")