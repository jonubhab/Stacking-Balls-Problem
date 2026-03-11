import os
import io
import atexit
import sys
import datetime

def encrypt(**kwargs):
    code = ""
    for i, j in kwargs.items():
        code += str(int(j)) if type(j) is bool else str(j)
    return code,kwargs

def Data(code,kwargs):
    folder_path = 'Data'

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'r') as file:
                    c = file.readlines()[0].strip()
                    if c == code:
                        return file_path
            except Exception as e:
                print(f"Error reading {filename}: {e}")


    file_path = os.path.join(folder_path, f"Experiment {len(os.listdir(folder_path))}- {code}")
    with open(file_path, 'w') as f:
        f.write(code + "\n")
        for i, j in kwargs.items():
            f.write(f"{i:<9}: {j}\n")
        f.write("_" * 100 + "\n")
    return file_path



class DualLogger:
    def __init__(self, original_stream):
        self.terminal = original_stream
        self.buffer = io.StringIO()

    def write(self, message):
        self.terminal.write(message)
        self.buffer.write(message)   

    def flush(self):
        self.terminal.flush()

    def get_captured_text(self):
        return self.buffer.getvalue()


def save(file):
    stdout_logger = DualLogger(sys.stdout)
    stderr_logger = DualLogger(sys.stderr)

    sys.stdout = stdout_logger
    sys.stderr = stderr_logger

    def save_session_to_file():
        with open(file, "a") as f:
            s = stdout_logger.get_captured_text()
            f.write("\n--- TRANSCRIPT ---\n")
            f.write(s)
            s = stderr_logger.get_captured_text()
            if len(s) != 0:
                f.write("\n--- ERROR LOG ---\n")
                f.write(s)
            f.write("_" * 100 + "\n")

    atexit.register(save_session_to_file)

def saveShape(balls,file):
    with open(file,'a') as f:
        for i in balls:

            f.write(str(i.position())+"\n")
