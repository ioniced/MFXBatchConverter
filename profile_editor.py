import tkinter as tk

def parse_profile_string(profile_str):
    profile_str = profile_str.strip().rstrip(",")
    pairs = profile_str.split(",")
    d = {}
    for pair in pairs:
        if "=" in pair:
            k, v = pair.split("=", 1)
            d[k.strip()] = v.strip()
    return d

def build_profile_string(profile_dict):
    parts = [f"{k}={v}" for k, v in profile_dict.items()]
    return ",".join(parts)

def open_profile_editor(current_profile_str, profile_entry):
    normalized_str = current_profile_str.replace(";", ",")
    profile_dict = parse_profile_string(normalized_str)

    editor = tk.Toplevel()
    editor.title("Edit VLC Profile")

    entries = {}

    row = 0
    for key, value in profile_dict.items():
        tk.Label(editor, text=key).grid(row=row, column=0, sticky="w", padx=5, pady=3)
        ent = tk.Entry(editor, width=30)
        ent.grid(row=row, column=1, padx=5, pady=3)
        ent.insert(0, value)
        entries[key] = ent
        row += 1

    def save_and_close():
        new_profile_dict = {k: e.get().strip() for k, e in entries.items()}
        new_profile_str = build_profile_string(new_profile_dict)
        profile_entry.delete("1.0", tk.END)
        profile_entry.insert("1.0", new_profile_str)
        editor.destroy()

    save_btn = tk.Button(editor, text="Save", command=save_and_close)
    save_btn.grid(row=row, column=0, columnspan=2, pady=10)
