import os
import subprocess
import threading
from vlc_utils import find_vlc

def convert_with_logs(input_file, output_file, profile_str, muxer, log_callback):
    input_file = os.path.normpath(input_file)
    output_file = os.path.normpath(output_file)

    vlc_exe = find_vlc()
    if not vlc_exe:
        log_callback("ERROR: VLC executable not found.")
        return -1

    command = [
        vlc_exe,
        "-I", "dummy",
        input_file,
        "--sout",
        f"#transcode{{{profile_str}}}:standard{{access=file,mux={muxer},dst={output_file}}}",
        "vlc://quit"
    ]

    log_callback(f"Running VLC command: {' '.join(command)}")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    if stdout:
        for line in stdout.splitlines():
            if "dummy interface" in line or "idummy demux" in line:
                continue
            log_callback(line)

    if stderr:
        log_callback(f"ERROR: {stderr}")

    return process.returncode

def batch_convert(files, output_folder, profile_str, muxer, basename, progress_callback, log_callback):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    total = len(files)
    for idx, file in enumerate(files, start=1):
        base_name = basename.strip() or "output"
        counter = str(idx).zfill(3)
        output_file_name = f"{base_name}_{counter}.{muxer}"
        output_path = os.path.abspath(os.path.join(output_folder, output_file_name))

        log_callback(f"--- Converting: {file} ---")

        code = convert_with_logs(file, output_path, profile_str, muxer, log_callback)

        if code == 0 and os.path.exists(output_path):
            log_callback(f"✅ Completed: {output_path}")
        else:
            log_callback(f"❌ Failed: {file} (No output created)")

        progress = int((idx / total) * 100)
        progress_callback(progress)

def start_conversion_thread(files, output_folder, profile_str, muxer, basename, progressbar, logbox, start_btn):
    def update_progress(value):
        progressbar['value'] = value

    def log_callback(text):
        logbox.insert("end", text + "\n")
        logbox.see("end")

    def run():
        start_btn.config(state="disabled")
        batch_convert(files, output_folder, profile_str, muxer, basename, update_progress, log_callback)
        start_btn.config(state="normal")
        log_callback("Batch conversion finished.")

    threading.Thread(target=run, daemon=True).start()
