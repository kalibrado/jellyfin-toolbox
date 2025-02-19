# Jellyfin Toolbox

A collection of Python scripts to enhance the Jellyfin experience. This toolbox includes:

- **Translation of summaries**: A script to translate media summaries into your desired language.
- **Bulk editing of age restrictions**: A tool to easily modify age restrictions for multiple videos.
- **Subtitle downloader**: Subtitle download script.
- **Video compression**: A script to compress videos to optimize storage space.
- **Automatic language detection**: A feature to detect the language of summaries before translating.

## Future Features

- [x] Translation of summaries
- [x] Automatic language detection
- [ ] Bulk editing of age restrictions
- [ ] Subtitle downloader
- [ ] Video compression

## Prerequisites

You can install them using pip:

```bash
pip install -r requirements.txt
```

## Usage

To recursively translate all `.nfo` and `.xml` files in a directory and detect the language before translating:

```bash
python translate.py /path/to/media_folder fr
```

- Replace `/path/to/media_folder` with the actual path to your media files.
- Replace `fr` with the target language code (e.g., `en` for English, `es` for Spanish, etc.).

## Contributing

Contributions are welcome! Feel free to submit a pull request to add new features or improve existing scripts.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
