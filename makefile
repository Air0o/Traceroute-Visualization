# Name of your main Python script
MAIN_SCRIPT = main.py

# Name of the output executable (without extension)
APP_NAME = main

# Resource folder you want to copy
RESOURCE_DIR = resources

# Default target
all: build copy-resources

# Run PyInstaller to build the executable
build:
    pyinstaller -F $(MAIN_SCRIPT)

# Copy resource folder into dist directory
copy-resources:
    @if [ -d "$(RESOURCE_DIR)" ]; then \
        cp -r $(RESOURCE_DIR) dist/$(RESOURCE_DIR); \
        echo "Copied $(RESOURCE_DIR) into dist/"; \
    else \
        echo "Resource directory $(RESOURCE_DIR) not found."; \
    fi

# Clean build artifacts
clean:
    rm -rf build dist *.spec
