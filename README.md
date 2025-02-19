# Jellyfin Toolbox

A collection of Python scripts to enhance the Jellyfin experience. This toolbox includes:

## Future Features

- [x] [NFO/XML Translator Script](docs/translate.md)
- [x] [Subtitle Downloader Script](docs/subtitle.md)
- [ ] Bulk editing of age restrictions
- [ ] Video compression
- [ ] Metadata Cleanup & Normalization (correct and clean metadata in `.nfo` and `.xml` files)
- [ ] Auto-Renaming & Sorting (automatically rename and organize media files based on metadata)
- [ ] Multi-Source Subtitle Downloader (support for additional subtitle sources like Subscene, Addic7ed)
- [ ] Duplicate Media Finder (detect and report duplicate media files)
- [ ] Poster & Fanart Downloader (automatically download posters and background images for media)
- [ ] Smart Watchlist Generator (automatically create dynamic playlists based on watch history, genres, and user preferences)

## Prerequisites

You can install the required libraries using pip:

```bash
pip install -r requirements.txt
```

Note: If you clone the repository and run the above command, you do not need to run `pip install` for each script individually, as the `requirements.txt` file includes all necessary libraries.

## Contributing

Contributions are welcome! Feel free to submit a pull request to add new features or improve existing scripts.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
