# MXF Batch Converter

A simple Python tool with a GUI for converting **MXF files** using **VLC's transcoding engine**.

---

## Features
- Batch conversion of MXF files to formats supported by VLC.
- Uses VLC's built-in transcoding profiles.
- Allows editing of VLC profile strings through a simple editor.
- Customizable output file names.
- Progress bar and log display in the GUI.
- Cross-platform (Windows, macOS, Linux).

---

## Project Structure
```
MXFBatchConverter/
│
├── main.py             # Application entry point
├── gui.py              # Main GUI code
├── converter.py        # Conversion logic
├── vlc_utils.py        # VLC detection and profile handling
├── profile_editor.py   # Profile string editor popup
├── helpers.py          # Utility functions
└── README.md           # Project documentation
```

---

## Requirements
- Python 3.7+
- VLC installed and accessible in your system path
- Python packages:
  ```bash
  pip install tk

---

## How to Run
- Clone this repository:
  ```bash
  pip install tk
  git clone https://github.com/ioniced/MXFBatchConverter
  cd MXFBatchConverter
- Run the application:
  ```bash
  python main.py

---

## Usage
Select an input folder containing MXF files.

Select an output folder.

Choose a VLC transcoding profile or edit the profile string.

Set an output base name for the files.

Click Start Conversion.

