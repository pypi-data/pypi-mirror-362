# PySQLiteFS Bindings

This project provide bindigs for sqlitefs project. You can create a file system inside sqlite database. With key you can encript the whole database including sqlite headers.

## Supported functions

- pwd - print working directory
- mkdir - create a new folder
- cd - change wirking directory
- ls - list files and folders
- cp - copy file. (Works with files only)
- mv - move node (file or folder)
- rm - remove node
- write - write file to the db. (1 GB max size for one file in database)
- read - read file from the db
- stats - recursively gets the count of all files in a directory, indicating the total size in compressed and raw form.

## Read/write algorithms

To add your own modifications check `Custom save and load functions` section below. You can modify your data as you want, for example you can encrypt/compress and decrypt/decompress in save and load respectively.

## Examples

A simple example

```python
from pysqlitefs import SQLiteFS

fs = SQLiteFS("test.db", "secret")
raw_content = "Raw data content"
fs.write("file.txt", raw_content.encode())
content = fs.read("file.txt")
print(f"Content of file.txt: {content}")
assert content.decode() == raw_content, "Content mismatch after save and load"
```

### Custom save and load functions

> NOTE: you can specify only one of them if you want to read or write only. So you can write data at your own pc with registered write function and send file with load function only. In this case user can read the data, but cannot modify it (only remove).

```python
from pysqlitefs import SQLiteFS


def save(data: bytes) -> bytes:
    return data[-1::-1]


def load(data: bytes) -> bytes:
    return data[-1::-1]


with open("file.dat", "rb") as f:
    raw_content = f.read()

fs = SQLiteFS("test.db")
fs.register_save_func("reverse", save)
fs.register_load_func("reverse", load)

for name in fs.getSaveFuncs():
    print(f"Test function: {name}")
    fs.write(f"{name}.dat", raw_content, name)
    content = fs.read(f"{name}.dat")
    assert content == raw_content, "Content mismatch after save and load"
```
