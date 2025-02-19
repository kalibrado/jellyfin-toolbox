
import os
import sys
import time
from datetime import datetime, timezone
from opensubtitlescom import OpenSubtitles

def print_usage():
    """Displays the script usage."""
    print("Usage: python scripts/subtitle.py <directory> <dest_lang> [username] [password] [api_key]")
    print("Options:")
    print("  <directory>   : Path to the directory containing video files")
    print("  <dest_lang>   : Target subtitle language (default: 'en')")
    print("  [username]    : OpenSubtitles username (optional, can use env var)")
    print("  [password]    : OpenSubtitles password (optional, can use env var)")
    print("  [api_key]     : OpenSubtitles API key (optional, can use env var)")
    print("Examples:")
    print("  python scripts/subtitle.py '/media/Movies' 'fr'")
    print("  python scripts/subtitle.py '/media/Movies' 'en' 'myuser' 'mypassword' 'myapikey'")

# Get credentials from environment variables or arguments
USERNAME = os.getenv("OPENSUBTITLES_USERNAME") or (sys.argv[3] if len(sys.argv) > 3 else None)
PASSWORD = os.getenv("OPENSUBTITLES_PASSWORD") or (sys.argv[4] if len(sys.argv) > 4 else None)
API_KEY = os.getenv("OPENSUBTITLES_API_KEY") or (sys.argv[5] if len(sys.argv) > 5 else None)

if not USERNAME or not PASSWORD or not API_KEY:
    print("Error: OpenSubtitles credentials are required.")
    print("Set them via environment variables or pass them as arguments.")
    print_usage()
    sys.exit(1)

# Initialize OpenSubtitles API
subtitles = OpenSubtitles("jellyfin-toolbox", API_KEY)
subtitles.login(USERNAME, PASSWORD)

video_extensions = [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".mpeg", ".mpg", ".m4v"]

def get_remaining_quota():
    """Retrieves the remaining quota and pauses the script if necessary."""
    try:
        user_info = subtitles.user_info()
        remaining = user_info["data"].get("remaining_downloads", 100)
        total = user_info["data"].get("allowed_downloads", 100)
        reset_time_utc = user_info["data"].get("reset_time_utc")

        print(f"Remaining quota: {remaining}/{total}")

        if remaining == 0 and reset_time_utc:
            reset_time = datetime.strptime(reset_time_utc, "%Y-%m-%dT%H:%M:%S.%fZ")
            reset_timestamp = reset_time.replace(tzinfo=timezone.utc).timestamp()
            current_timestamp = time.time()
            wait_time = max(int(reset_timestamp - current_timestamp), 0)

            wait_hours = wait_time // 3600
            wait_minutes = (wait_time % 3600) // 60

            print(f"Quota exhausted! Waiting {wait_hours}h {wait_minutes}m...")
            sys.exit(0)
    except Exception as e:
        print(f"Failed to retrieve quota info: {e}")
        sys.exit(1)

def download_sub(filepath, filename, dest_lang="en"):
    """Downloads a subtitle for a video file."""
    path, name = os.path.split(filepath)
    srt_path = os.path.join(path, f"{os.path.splitext(name)[0]}.srt")

    get_remaining_quota()
    print(f"Searching subtitles for: {filename}")
    
    try:
        response = subtitles.search(query=filename, languages=dest_lang)
    
        if not response or len(response.data) == 0:
            print(f"No subtitles found for {filename}\n")
            return

        subtitle_data = subtitles.download_and_parse(response.data[0], force_download=True)
        
        if not subtitle_data:
            print(f"Error parsing subtitles for {filename}\n")
            return

        with open(srt_path, "w", encoding="utf-8") as file:
            for index, subtitle in enumerate(subtitle_data, start=1):
                file.write(f"{index}\n")
                file.write(f"{subtitle.start} --> {subtitle.end}\n")
                file.write(f"{subtitle.content}\n\n")
            print(f"Subtitle saved: {srt_path}\n")
    except Exception as e:
        print(f"Error downloading subtitle: {e}\n")

def dl_subtitle_files_in_directory(directory, dest_lang="en"):
    """Downloads subtitles for all video files in a directory."""
    for root, _, files in os.walk(directory):
        print(f"Checking directory: {root}")
        for file in files:
            if file.endswith(tuple(video_extensions)):
                filepath = os.path.join(root, file)
                filename = os.path.splitext(file)[0]
                srt_path = os.path.join(root, f"{filename}.srt")
                if os.path.exists(srt_path):
                    print(f"Subtitle already exists: {filename}, skipping...\n")
                    continue
                print(f"Processing file: {filename}")
                download_sub(filepath, filename, dest_lang=dest_lang)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    directory = sys.argv[1]
    dest_lang = sys.argv[2] if len(sys.argv) > 2 else "en"

    if not os.path.isdir(directory):
        print("The provided path is not a valid directory.")
        sys.exit(1)

    directory = os.path.normpath(directory)
    dl_subtitle_files_in_directory(directory, dest_lang=dest_lang)
