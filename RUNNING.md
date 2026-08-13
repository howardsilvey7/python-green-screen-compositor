# Running the Project

## Requirements

- Python 3.10 or newer
- pip

## 1. Create a virtual environment

### Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
py -m venv .venv
.venv\Scripts\activate.bat
```

### Git Bash

```bash
python -m venv .venv
source .venv/Scripts/activate
```

### macOS / Linux Bash

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2. Install the project

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

To run the automated tests, install the development extras instead:

```bash
python -m pip install -e ".[dev]"
```

## 3. Run the compositor

Recommended module form:

```bash
python -m green_screen
```

Installed console command:

```bash
green-screen
```

The program lists the supplied background images, asks how many foreground images to place, lets you choose each foreground, accepts center coordinates anywhere on the selected background, safely clips any foreground portion that extends beyond an edge, and writes the result to:

```text
outputs/output.bmp
```


## 4. Run the test suite

```bash
python -m pytest
```

## 5. Optional lint check

```bash
python -m ruff check .
```

## Asset directories

Backgrounds:

```text
assets/backgrounds/
```

Foreground green-screen bitmaps:

```text
assets/foregrounds/
```

Generated images:

```text
outputs/
```
