# Run with --help option to receive instructions for parameters


# WARNING: It is recommended to make venv before installing dependecies
### To make venv, run:

### If Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate

### If Windows:
python -m venv .venv
.venv\Scripts\activate


# To install dependencies, run:
pip install -r requirements.txt

# If you need to build executable file, go through following steps:

### 1. Install pyinstaller:
pip install pyinstaller

### 2. Build:
pyinstaller telemetry_parse.py --onefile

### 3. You will now have executable file at ./dist/telemetry_parse/telemetry_parse if you have Linux/macOS or ./dist/telemetry_parse/telemetry_parse.exe if you have Windows