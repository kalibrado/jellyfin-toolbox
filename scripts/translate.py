import os
import sys
import xml.etree.ElementTree as ET
import fasttext
import requests
from deep_translator import GoogleTranslator

MODEL_PATH = "/tmp/lid.176.bin"
MODEL_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"

def download_model():
    """Télécharge le modèle fastText si absent."""
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    print(f"Downloading model from {MODEL_URL}...")
    
    response = requests.get(MODEL_URL, stream=True)
    if response.status_code == 200:
        with open(MODEL_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Download complete!")
    else:
        print(f"Failed to download model. HTTP Status: {response.status_code}")
        sys.exit(1)

if not os.path.exists(MODEL_PATH):
    download_model()

model = fasttext.load_model(MODEL_PATH)

def print_usage():
    """Displays the script usage."""
    print("Usage: python translate.py <directory> <dest_lang>")
    print("Options:")
    print("  <directory>   : Path to the directory containing NFO or XML files")
    print("  <dest_lang>   : Target language code (default: 'en')")
    print("Examples:")
    print("  python translate.py /media/Movies fr")
    print("  python translate.py /media/Movies en")

def translate_text(text, dest="en"):
    """Translates the text using deep-translator."""
    try:
        translated_text = GoogleTranslator(source="auto", target=dest).translate(text)
        return translated_text
    except Exception as e:
        print(f"Error translating text: '{text}'\nError: {e}")
        return text  # Return original text in case of error

def detect_language(text):
    """Detects the language using fastText."""
    text = text.replace("\n", " ")  # Nettoyer le texte pour éviter les erreurs
    prediction = model.predict(text, k=1)
    detected_lang = prediction[0][0].replace("__label__", "")
    print(f"Detected language for '{text[:50]}...': {detected_lang}")  # Affichage partiel pour lisibilité
    return detected_lang

def clean_nfo_file(filepath):
    """Cleans the file to keep only valid XML content."""
    with open(filepath, "r", encoding="utf-8", errors="ignore") as file:
        lines = file.readlines()

    if len(lines) == 0:
        raise ValueError(f"Empty File: {filepath}")

    # Filter lines that are part of the XML content
    cleaned_lines = [line for line in lines if line.strip().startswith("<")]

    # Write the cleaned content back to the file
    with open(filepath, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)

def translate_file(filepath, dest_lang="fr"):
    """Translates the content of an NFO file after cleaning it."""
    clean_nfo_file(filepath)

    # Parse the cleaned XML
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Tags to translate for series or movie XML files
        tags_to_translate = {"genre", "Genre", "description", "plot", "overview", "Overview"}

        # Translate specified elements
        for elem in root.iter():
            if elem.tag in tags_to_translate and elem.text:
                original_text = elem.text.strip()
                detected_lang = detect_language(original_text)  # Detect text language
                
                if detected_lang == dest_lang:
                    print(f"Skipping translation for '{original_text}' (already in target language)")
                    continue
                
                translated_text = translate_text(original_text, dest=dest_lang)
                elem.text = translated_text
                print(f"Translated: '{original_text}'\nTo: '{translated_text}'")

        # Save the translated XML back to the original file with UTF-8 encoding
        tree.write(filepath, encoding="utf-8", xml_declaration=True)
    except ET.ParseError as e:
        print(f"Error parsing file {filepath}: {e}")

def translate_files_in_directory(directory, dest_lang="en"):
    """Translates all NFO or XML files in the specified directory."""
    for root, _, files in os.walk(directory):
        print(f"Checking directory: {root}")
        for file in files:
            if file.endswith((".nfo", ".xml")):
                filepath = os.path.join(root, file)
                print(f"Processing file: {file}")
                try:
                    translate_file(filepath, dest_lang=dest_lang)
                except ValueError as e:
                    print(e)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    directory = sys.argv[1]
    dest_lang = sys.argv[2] if len(sys.argv) > 2 else "en"

    if not os.path.isdir(directory):
        print("The provided path is not a valid directory.")
        sys.exit(1)

    # Normalize the path to handle Unicode characters correctly
    directory = os.path.normpath(directory)
    translate_files_in_directory(directory, dest_lang=dest_lang)
