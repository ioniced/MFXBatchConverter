import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os

from vlc_utils import load_vlc_profiles
from profile_editor import open_profile_editor
from converter import start_conversion_thread
from helpers import normalize_profile_string

def launch_gui():
    root = tk.Tk()
    root.title("MXF Batch Converter (VLC)")
    root.geometry("850x650")

    profiles = load_vlc_profiles()

    # === Input Folder ===
    tk.Label(root, text="Input Folder:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    input_folder_var = tk.StringVar()
    input_entry = tk.Entry(root, textvariable=input_folder_var, width=50)
    input_entry.grid(row=0, column=1, sticky="we", padx=5)
    file_listbox = tk.Listbox(root, width=70, height=8)
    file_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    def select_input_folder():
        folder = filedialog.askdirectory()
        if folder:
            input_folder_var.set(folder)
            files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(".mxf")]
            file_listbox.delete(0, tk.END)
            for f in files:
                file_listbox.insert(tk.END, f)

    input_btn = tk.Button(root, text="Browse", command=select_input_folder)
    input_btn.grid(row=0, column=2, padx=5)

    # === Output Folder ===
    tk.Label(root, text="Output Folder:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    output_folder_var = tk.StringVar()
    output_entry = tk.Entry(root, textvariable=output_folder_var, width=50)
    output_entry.grid(row=2, column=1, sticky="we", padx=5)
    output_btn = tk.Button(root, text="Browse", command=lambda: output_folder_var.set(filedialog.askdirectory()))
    output_btn.grid(row=2, column=2, padx=5)

    # === Output Basename ===
    tk.Label(root, text="Output Basename:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    basename_var = tk.StringVar(value="output")
    basename_entry = tk.Entry(root, textvariable=basename_var, width=20)
    basename_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

    # === VLC Profile Dropdown ===
    selected_profile = tk.StringVar()
    tk.Label(root, text="VLC Profile:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    profile_dropdown = ttk.Combobox(root, textvariable=selected_profile, values=list(profiles.keys()), width=40, state="readonly")
    profile_dropdown.grid(row=4, column=1, sticky="we", padx=5)

    # === Profile String Editor ===
    tk.Label(root, text="Profile String:").grid(row=5, column=0, sticky="nw", padx=5, pady=5)
    profile_entry = tk.Text(root, height=3, width=70)
    profile_entry.grid(row=5, column=1, columnspan=2, sticky="we", padx=5, pady=5)

    # === Edit Profile Button ===
    def on_edit_profile():
        current_profile_str = profile_entry.get("1.0", "end").strip()
        open_profile_editor(current_profile_str, profile_entry)

    edit_profile_btn = tk.Button(root, text="Edit", command=on_edit_profile)
    edit_profile_btn.grid(row=5, column=3, sticky="ns", padx=5, pady=5)

    # Default Profile
    default_profile_name = "Video for MPEG4 1080p TV/device"
    if default_profile_name in profiles:
        selected_profile.set(default_profile_name)
        profile_entry.delete("1.0", tk.END)
        profile_entry.insert("1.0", profiles[default_profile_name])
    else:
        profile_entry.insert("1.0", "vcodec=mp4v,acodec=mpga,ab=512,channels=2,samplerate=44100,width=1920,height=1080,fps=0,muxer=mp4")

    def on_profile_select(event):
        profile_name = selected_profile.get()
        if profile_name in profiles:
            profile_entry.delete("1.0", tk.END)
            profile_entry.insert("1.0", profiles[profile_name])

    profile_dropdown.bind("<<ComboboxSelected>>", on_profile_select)

    # === Progress Bar ===
    progress = tk.DoubleVar()
    progressbar = ttk.Progressbar(root, variable=progress, maximum=100)
    progressbar.grid(row=6, column=0, columnspan=4, sticky="we", padx=5, pady=5)

    # === Log Box ===
    logbox = scrolledtext.ScrolledText(root, height=15, width=80, state='normal')
    logbox.grid(row=7, column=0, columnspan=4, padx=5, pady=5)

    # === Start Button ===
    def start():
        input_folder = input_folder_var.get()
        output_folder = output_folder_var.get()
        raw_profile = profile_entry.get("1.0", "end").strip()
        profile_str, muxer = normalize_profile_string(raw_profile)
        basename = basename_var.get()

        if not os.path.isdir(input_folder):
            messagebox.showerror("Error", "Input folder is invalid or does not exist.")
            return
        if not output_folder:
            messagebox.showerror("Error", "Please select an output folder.")
            return
        if not profile_str:
            messagebox.showerror("Error", "Please enter a VLC profile string.")
            return
        if not basename.strip():
            messagebox.showerror("Error", "Please enter a valid output basename.")
            return

        files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(".mxf")]
        if not files:
            messagebox.showinfo("Info", "No MXF files found in the input folder.")
            return

        logbox.delete('1.0', tk.END)

        start_conversion_thread(files, output_folder, profile_str, muxer, basename, progressbar, logbox, start_btn)

    start_btn = tk.Button(root, text="Start Conversion", command=start)
    start_btn.grid(row=8, column=0, columnspan=4, pady=10)

    root.columnconfigure(1, weight=1)
    root.mainloop()
