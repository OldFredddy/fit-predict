from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["numpy", "pandas", "sklearn", "joblib", "PyQt5", "openpyxl"]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name="MyApp",
    options=options,
    version="1.0.0",
    description='My application description',
    executables=executables
)
