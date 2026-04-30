#!/usr/bin/env python3
"""
YouTube Mashup Generator - Roll Number: 102303124

This script:
1. Searches and downloads N videos of a given singer
2. Extracts audio from each video
3. Cuts the first Y seconds from each audio
4. Combines everything into one final mashup

Usage:
python 102303124.py "Singer Name" N Y output.mp3

Example:
python 102303124.py "Sharry Maan" 20 20 mashup.mp3
"""

import sys
import os
import re
import shutil

try:
    import yt_dlp
    from pydub import AudioSegment
except ImportError:
    print("Required libraries are missing.")
    print("Install using: pip install yt-dlp pydub")
    sys.exit(1)


# -------------------- INPUT VALIDATION --------------------

def validate_inputs(args):
    if len(args) != 5:
        print("Invalid number of arguments.")
        print("Usage: python 102303124.py <SingerName> <NumVideos> <Duration> <OutputFile>")
        return False

    singer = args[1]

    try:
        num_videos = int(args[2])
        duration = int(args[3])
    except:
        print("NumVideos and Duration must be integers.")
        return False

    if num_videos <= 10:
        print("Number of videos should be more than 10.")
        return False

    if duration <= 20:
        print("Duration must be more than 20 seconds.")
        return False

    output = args[4]
    if not output.endswith((".mp3", ".wav", ".m4a")):
        print("Output file must be an audio format.")
        return False

    if not singer.strip():
        print("Singer name cannot be empty.")
        return False

    return True


# -------------------- DOWNLOAD VIDEOS --------------------

def download_videos(singer, count):
    folder = "temp_videos"

    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    print(f"\nStep 1: Downloading {count} videos of {singer}...")

    options = {
        'format': 'best',
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'max_downloads': count
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            query = f"{singer} audio"
            result = ydl.extract_info(f"ytsearch{count}:{query}", download=True)

            if "entries" in result:
                print(f"Downloaded {len(result['entries'])} videos successfully.")
                return folder
            else:
                print("No videos found.")
                return None

    except Exception as e:
        print("Download error:", e)
        return None


# -------------------- CONVERT TO AUDIO --------------------

def convert_videos_to_audio(video_folder):
    print("\nStep 2: Converting videos to audio...")

    audio_folder = "temp_audio"
    os.makedirs(audio_folder, exist_ok=True)

    files = [f for f in os.listdir(video_folder)
             if f.endswith(('.mp4', '.mkv', '.webm', '.avi', '.mov'))]

    if not files:
        print("No video files found.")
        return None

    for i, file in enumerate(files, 1):
        try:
            input_path = os.path.join(video_folder, file)
            output_path = os.path.join(audio_folder, f"audio_{i}.mp3")

            audio = AudioSegment.from_file(input_path)
            audio.export(output_path, format="mp3")

            print(f"Converted: {file}")
        except Exception as e:
            print(f"Error converting {file}: {e}")

    return audio_folder


# -------------------- CUT AUDIO --------------------

def trim_audio(audio_folder, duration):
    print(f"\nStep 3: Cutting first {duration} seconds...")

    cut_folder = "temp_cut"
    os.makedirs(cut_folder, exist_ok=True)

    files = sorted([f for f in os.listdir(audio_folder) if f.endswith(".mp3")])

    for i, file in enumerate(files, 1):
        try:
            input_path = os.path.join(audio_folder, file)
            output_path = os.path.join(cut_folder, f"clip_{i}.mp3")

            audio = AudioSegment.from_mp3(input_path)
            trimmed = audio[:duration * 1000]

            trimmed.export(output_path, format="mp3")

            print(f"Clip {i} created")
        except Exception as e:
            print(f"Error trimming {file}: {e}")

    return cut_folder


# -------------------- MERGE AUDIO --------------------

def merge_all_audio(cut_folder, output_file):
    print("\nStep 4: Merging all clips...")

    files = sorted([f for f in os.listdir(cut_folder) if f.endswith(".mp3")])

    if not files:
        print("No clips to merge.")
        return False

    final_audio = AudioSegment.empty()

    for i, file in enumerate(files, 1):
        path = os.path.join(cut_folder, file)
        audio = AudioSegment.from_mp3(path)

        final_audio += audio
        print(f"Added clip {i}")

    final_audio.export(output_file, format="mp3")

    print(f"\nMashup created: {output_file}")
    return True


# -------------------- CLEANUP --------------------

def cleanup(*folders):
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    print("Temporary files removed.")


# -------------------- MAIN --------------------

def main():
    print("=" * 50)
    print("YouTube Mashup Generator - Roll: 102303124")
    print("=" * 50)

    if not validate_inputs(sys.argv):
        sys.exit(1)

    singer = sys.argv[1]
    num = int(sys.argv[2])
    duration = int(sys.argv[3])
    output = sys.argv[4]

    if shutil.which("ffmpeg") is None:
        print("ffmpeg is required. Please install it first.")
        sys.exit(1)

    try:
        video_folder = download_videos(singer, num)
        if not video_folder:
            sys.exit(1)

        audio_folder = convert_videos_to_audio(video_folder)
        if not audio_folder:
            sys.exit(1)

        cut_folder = trim_audio(audio_folder, duration)
        if not cut_folder:
            sys.exit(1)

        if not merge_all_audio(cut_folder, output):
            sys.exit(1)

        cleanup(video_folder, audio_folder, cut_folder)

        print("\nMashup created successfully!")

    except KeyboardInterrupt:
        print("\nProcess stopped by user.")
        cleanup("temp_videos", "temp_audio", "temp_cut")

    except Exception as e:
        print("Unexpected error:", e)
        cleanup("temp_videos", "temp_audio", "temp_cut")


if __name__ == "__main__":
    main()