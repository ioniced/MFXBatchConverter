import os
import shutil
import configparser
import platform

def find_vlc():
    vlc_path = shutil.which("vlc")
    if vlc_path:
        return vlc_path

    possible_paths = [
        r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None

def get_vlc_profile_path():
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.getenv('APPDATA'), 'vlc', 'vlc-qt-interface.ini')
    elif system == "Darwin":
        return os.path.expanduser('~/Library/Preferences/org.videolan.vlc/vlc-qt-interface.ini')
    else:
        return os.path.expanduser('~/.config/vlc/vlc-qt-interface.ini')

def load_vlc_profiles():
    path = get_vlc_profile_path()
    if not os.path.exists(path):
        return {}

    config = configparser.ConfigParser(interpolation=None)
    config.read(path, encoding="utf-8")

    if 'codecs-profiles' not in config:
        return {}

    profiles = {}
    for key in config['codecs-profiles']:
        if key.lower().endswith("profile-name"):
            idx = key.split("\\")[0]
            name = config['codecs-profiles'][key]
            value_key = f"{idx}\\Profile-Value".lower()
            value = config['codecs-profiles'].get(value_key, "")

            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]

            profiles[name] = value

    return profiles