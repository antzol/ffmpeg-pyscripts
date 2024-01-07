import json
import os
import subprocess

from modules import globals


def get_streams(input_path):
    if not os.path.isfile(input_path):
        return []
    cmd = [globals.__FFPROBE__, '-print_format', 'json', '-show_streams', input_path]
    result = subprocess.run(cmd, capture_output=True, check=True)
    streams = json.loads(result.stdout)
    return streams


def contains_audio(streams_info: dict):
    for stream in streams_info['streams']:
        if 'codec_type' in stream and stream['codec_type'] == 'audio':
            return True
    return False


def contains_subtitles(streams_info: dict):
    for stream in streams_info['streams']:
        if 'codec_type' in stream and stream['codec_type'] == 'subtitle':
            return True
    return False
