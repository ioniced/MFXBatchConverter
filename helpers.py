def normalize_profile_string(profile_str):
    profile_str = profile_str.replace(";", ",")
    parts = profile_str.split(",")
    kv = {}
    for part in parts:
        if "=" in part:
            k, v = part.split("=", 1)
            kv[k.strip().lower()] = v.strip()

    mapping = {
        "audio_codec": "acodec",
        "acodec_bitrate": "ab",
        "acodec_channels": "channels",
        "acodec_samplerate": "samplerate",
        "video_codec": "vcodec",
        "vcodec_width": "width",
        "vcodec_height": "height",
        "vcodec_framerate": "fps",
        "vcodec_bitrate": "vb"
    }

    normalized = {}
    muxer = kv.get("muxer", "mp4")

    for k, v in kv.items():
        if k == "muxer":
            continue
        if k in mapping:
            normalized[mapping[k]] = v
        elif k in ["vcodec", "acodec", "width", "height", "fps", "vb", "ab", "channels", "samplerate"]:
            normalized[k] = v

    transcode_str = ",".join(f"{k}={v}" for k, v in normalized.items())
    return transcode_str, muxer
