# Subtitle Downloader Script

This script allows you to download subtitles for video files in a specified directory using the OpenSubtitles API. It searches for subtitles in the specified language and saves them as `.srt` files.

## Requirements

- Python 3.x
- `opensubtitlescom` library (install via pip)
- OpenSubtitles account and API key

## Installation

1. Clone the repository or download the script.
2. Install the required library:

   ```bash
   pip install opensubtitlescom
   ```

3. Set up your OpenSubtitles credentials as environment variables or pass them as command line arguments.

## Usage

To run the script, use the following command:

```bash
python scripts/subtitle.py <directory> <dest_lang> [username] [password] [api_key]
```

### Parameters:

- `<directory>`: Path to the directory containing video files.
- `<dest_lang>`: Target subtitle language (default: 'en').
- `[username]`: OpenSubtitles username (optional, can use environment variable `OPENSUBTITLES_USERNAME`).
- `[password]`: OpenSubtitles password (optional, can use environment variable `OPENSUBTITLES_PASSWORD`).
- `[api_key]`: OpenSubtitles API key (optional, can use environment variable `OPENSUBTITLES_API_KEY`).

### Examples:

```bash
python scripts/subtitle.py '/media/Movies' 'fr'
python scripts/subtitle.py '/media/Movies' 'en' 'myuser' 'mypassword' 'myapikey'
```

## How It Works

1. The script checks the specified directory for video files with common extensions (e.g., `.mp4`, `.mkv`, `.avi`, etc.).
2. It retrieves OpenSubtitles credentials from environment variables or command line arguments.
3. For each video file, it searches for subtitles in the specified language.
4. If found, the subtitles are downloaded and saved as `.srt` files in the same directory as the video.

## Error Handling

- If the OpenSubtitles credentials are not provided, the script will display an error message and usage instructions.
- If there are no subtitles found for a video file, it will notify you and continue processing other files.
- The script will check your OpenSubtitles download quota and pause if it has been exhausted.
