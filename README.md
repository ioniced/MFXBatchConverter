🎬 MXF Batch Converter (VLC-based)
This is a Python GUI tool for batch converting MXF files using VLC's transcoding engine.
It leverages VLC profiles, allows editing of transcode profile strings, and provides a user-friendly interface with logging and progress tracking.

✅ Features
Batch Convert MXF to MP4 (or other muxers) using VLC.

Auto-detect VLC installation path on Windows/macOS/Linux.

Loads VLC Transcoding Profiles from VLC config.

Profile String Editor: Modify every parameter easily via a popup editor.

Custom Output Naming with base name + counter.

Progress Bar and Log Output in the GUI.

Cross-platform (Windows, macOS, Linux).

📂 Project Structure
pgsql
Copy
Edit
mxf_to_mp4_converter/
│
├── main.py               # Entry point - starts the GUI
├── gui.py                # GUI code (Tkinter)
├── vlc_utils.py          # VLC profile handling and path detection
├── converter.py          # Core batch conversion logic
├── profile_editor.py     # Profile string editor popup logic
├── helpers.py            # Common utility functions
└── README.md             # This file
🔍 Module Breakdown
1. main.py
Entry point for the application.

Imports launch_gui() from gui.py.

Runs the GUI loop.

2. gui.py
Handles all UI components using Tkinter:

File Inputs:

Select Input Folder (MXF files)

Select Output Folder

Output Basename

Profile Management:

Dropdown to select VLC profile

Text area to display the selected profile string

Edit Profile button → opens profile editor (from profile_editor.py)

Progress & Logs:

Progress bar updates during batch conversion

Scrollable log window for VLC output

Start Conversion Button:

Validates inputs

Calls start_conversion_thread() (from converter.py)

Functions in gui.py:

launch_gui(): Initializes the entire GUI.

on_edit_profile(): Opens profile editor popup.

on_profile_select(): Loads selected VLC profile into the text box.

3. vlc_utils.py
Responsible for loading VLC profiles and finding VLC executable:

find_vlc(): Detect VLC binary path.

get_vlc_profile_path(): Return VLC config file path based on OS.

load_vlc_profiles(): Parse vlc-qt-interface.ini to load available profiles.

Sanitization: Removes unnecessary quotes from profile strings.

4. converter.py
Handles batch conversion logic and threading:

convert_with_logs(input_file, output_file, profile_str, muxer, log_callback): Runs VLC in CLI mode for one file.

batch_convert(files, output_folder, profile_str, muxer, basename, progress_callback, log_callback): Loops through all files.

start_conversion_thread(...): Runs conversion in a background thread to keep UI responsive.

5. profile_editor.py
Creates a popup editor window to modify profile strings:

parse_profile_string(profile_str): Convert vcodec=mp4v,ab=512,... into a dictionary.

build_profile_string(profile_dict): Convert dictionary back to string.

open_profile_editor(current_profile_str, profile_entry): Opens editor, populates fields, updates main GUI on save.

6. helpers.py
Shared helper functions:

normalize_profile_string(profile_str): Converts VLC profile into normalized form and extracts muxer.

Utility functions for string cleaning, parsing, etc.

⚙️ Installation & Setup
Requirements
Python 3.7+

VLC installed and accessible in PATH

Required Python libraries:

bash
Copy
Edit
pip install tk
Run the App
bash
Copy
Edit
python main.py
▶️ How It Works
Select Input Folder containing MXF files.

Select Output Folder for converted files.

Choose or edit a VLC Profile.

Set an Output Basename (e.g., output → output_001.mp4).

Click Start Batch Conversion → Progress bar and logs update in real-time.

🛠 Customization
Add more profile presets by editing VLC's config (vlc-qt-interface.ini).

Extend UI to support custom codecs, filters, etc.

Modify vlc_utils.py to change VLC path detection.

📌 Example Profile String
ini
Copy
Edit
vcodec=h264,vb=800,scale=1,acodec=mp4a,ab=128,channels=2,samplerate=44100,muxer=mp4
✅ Roadmap
 Add drag-and-drop for files

 Support custom file extensions

 Add cancel button for conversions

 Implement queue system for multiple folders

