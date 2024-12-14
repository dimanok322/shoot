PYTHON=python3
PYINSTALLER=pyinstaller
FILE_NAME=shoot.py
WINDOWS_SOURCE=.\shoot.py
LINUX_SOURCE=`pwd`/shoot.py
WINDOWS_OUTPUT=.\output\windows
LINUX_OUTPUT=`pwd`/output/linux
WINDOWS_OPTIONS=--onefile --console
LINUX_OPTIONS=--onefile --console
CLEANING_FILE=clear.py
HTML_FILE = index.html
all: windows linux web

windows:
	pip install -r requirements.txt
	@echo "Building for Windows..."
	$(PYINSTALLER) $(WINDOWS_OPTIONS) $(WINDOWS_SOURCE) --distpath $(WINDOWS_OUTPUT)
	$(WINDOWS_OUTPUT)\shoot.exe

web:
	@echo "Setting up Web version..."
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Starting Flask server..."
	@py app.py

linux:
	@echo "Building for Linux..."
	@echo
	@echo "Installing python, pip, PyInstaller...\n"
	@apt install -y python3 python3-pip make
	@pip install --break-system-packages -r requirements.txt
	@echo "Done\n"
	@echo "Building Binary file..."
	@$(PYINSTALLER) $(LINUX_OPTIONS) $(LINUX_SOURCE) --distpath $(LINUX_OUTPUT)
	@echo "Done\n"
	@echo
	@echo "Built file located in $(LINUX_OUTPUT)"
	@echo

clean:
	@echo "Cleaning..."
	python $(CLEANING_FILE)