# NFO/XML Translator Script

This script translates the content of NFO or XML files in a specified directory using the `deep-translator` and `fasttext` libraries. It detects the original language of the text and translates it into the desired target language.

## Requirements

- Python 3.x
- `fasttext`, `requests`, and `deep-translator` libraries (install via pip)

## Installation

1. Clone the repository or download the script.
2. Install the required libraries:

   ```bash
   pip install deep-translator fasttext requests
   ```

3. The script will automatically download the FastText model if it's not present.

## Usage

To run the script, use the following command:

```bash
python scripts/translate.py <directory> <dest_lang>
```

### Parameters:

- `<directory>`: Path to the directory containing NFO or XML files.
- `<dest_lang>`: Target language code (default: 'en').

### Examples:

```bash
python scripts/translate.py /media/Movies fr
python scripts/translate.py /media/Movies en
```

## How It Works

1. The script checks the specified directory for NFO or XML files.
2. It downloads the FastText language detection model if it's not already present.
3. For each file, it cleans the content to keep only valid XML elements.
4. It detects the original language of the text and translates specified elements (e.g., genre, description) into the desired language.
5. The translated XML is saved back to the original file with UTF-8 encoding.

## Error Handling

- If the provided directory is invalid, the script will display an error message.
- If an NFO or XML file is empty, an error will be raised.
- The script handles XML parsing errors and notifies you if there are issues with specific files.
