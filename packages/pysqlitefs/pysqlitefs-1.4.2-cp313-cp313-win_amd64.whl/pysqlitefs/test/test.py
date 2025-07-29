from pysqlitefs import SQLiteFS
import os


def save(data: bytes) -> bytes:
    return data[-1::-1]


def load(data: bytes) -> bytes:
    return data[-1::-1]


file_path = os.path.join(os.path.dirname(__file__), "test_file.dat")
with open(file_path, "rb") as f:
    raw_content = f.read()

fs = SQLiteFS("test.db")
fs.register_save_func("reverse", save)
fs.register_load_func("reverse", load)

for name in fs.getSaveFuncs():
    print(f"Test function: {name}")
    fs.write(f"{name}.txt", raw_content, name)
    content = fs.read(f"{name}.txt")
    print(f"Content: {content}")
    assert content == raw_content, "Content mismatch after save and load"
