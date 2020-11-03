#!python3

import os
import subprocess

EXE_PATH = r"D:\My Docs\Programming\_Loose Files\pdfParser\xpdf-tools-win-4.02\bin64\pdftotext.exe"

filename = input('Which pdf (filename) to convert?')
subprocess.call(f'"{EXE_PATH}" -layout "{filename}" "out.txt"', shell=True)