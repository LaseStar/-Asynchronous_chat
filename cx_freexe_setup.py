import sys
from cx_Freeze import setup, Executable

# Зависимости определяются автоматически, но может потребоваться настройка.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}
setup(
    name="Asynchronous_chat",
    version="0.0.1",
    description="A simple asynchronous chat",
    options={
        "build_exe": build_exe_options
    },
    executables=[Executable("server.py")]
)
