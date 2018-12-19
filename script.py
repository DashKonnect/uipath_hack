import ctypes

def read_file(file):
    text = "It runs Bitches!"
    ctypes.windll.user32.MessageBoxW(0, text, "DATA", 3)
