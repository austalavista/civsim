from cx_Freeze import setup, Executable
import os
import sys

base = None    

executables = [Executable("main.py", base=base)]

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR,'tcl','tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
packages = ["idna", "pyglet", "math", "random","numpy","config","cvsmr","core","cvsmm","cvsms","cvsmgmt","tripy"]
options = {
    'build_exe': {    
        'packages':packages,
        'include_files': ["C:/Users/Austa Jiang/AppData/Local/Programs/Python/Python36-32/DLLs/tcl86t.dll", "C:/Users/Austa Jiang/AppData/Local/Programs/Python/Python36-32/DLLs/tk86t.dll"]
    },    
}

setup(
    name = "<any name>",
    options = options,
    version = "<any number>",
    description = '<any description>',
    executables = executables
)
