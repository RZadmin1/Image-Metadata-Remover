# Image Metadata Remover - v1.0.0
# Rajin Zaman

import os
from utils import *
from PyQt6.QtWidgets import QApplication
from ui import MetadataRemoverUI

INPUT_DIR = "input/"
OUTPUT_DIR = "output/"


IGNORE_LIST = [
    "Image Width", "Image Height", "Bits Per Sample", "Compression", "Photometric Interpretation",
    "Padding", "MakerNote", "Orientation", "XResolution", "YResolution", "ResolutionUnit", "YCbCrPositioning",
    "ExposureProgram", "PhotographicSensitivity", "ExifVersion", "ExposureCompensation", "MeteringMode",
    "Flash", "FlashpixVersion", "ExifImageWidth", "ExifImageLength", "SensingMethod", "SceneType",
    "JpgFromRawStart", "JpgFromRawLength"
]

# Example dictionary mapping common EXIF tags
EXIF_TAGS = {
    0x0100: "Image Width",
    0x0101: "Image Height",
    0x0103: "Compression",
    0x0112: "Orientation",
    0x011A: "XResolution",
    0x011B: "YResolution",
    # Add other important tags...
}


# Controller for the file paths and program execution
class MetadataController:
    def __init__(self):
        self.input_folder = ""
        self.output_folder = ""

    def set_input_folder(self, folder):
        self.input_folder = folder

    def set_output_folder(self, folder):
        self.output_folder = folder

    def run_metadata_removal(self):
        if not self.input_folder or not self.output_folder:
            return "Input or output folder not set."
        try:
            sweep_metadata(self.input_folder, self.output_folder, ignore_list=IGNORE_LIST)
            return "Metadata removal complete!"
        except Exception as e:
            return f"Error: {e}"


def main():
    """ # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Iterate over all image files in the input directory
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            input_path = os.path.join(INPUT_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename)

            print(f"Processing: {filename}")
            try:
                # Remove metadata and save the result
                remove_metadata(input_path, output_path)
                print(f"Processed and saved to: {output_path}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}") """
    
    """ # Replace 'input/example.jpg' with the actual path to an image in your input folder
    image_path = "input/Car.jpg"
    display_metadata(image_path, IGNORE_LIST)
    
    # # Remove metadata and save to output
    # output_path = "output/Car.jpg"
    # remove_metadata(image_path, output_path, ignore_list=IGNORE_LIST)

    input_folder = "input"
    output_folder = "output"

    sweep_metadata(input_folder, output_folder, ignore_list=IGNORE_LIST)
    
    # Display metadata after modification
    print("\nModified Metadata:")
    display_metadata("output/Car.jpg", IGNORE_LIST) """

    app = QApplication([])
    controller = MetadataController()
    ui = MetadataRemoverUI(controller)
    ui.show()
    app.exec()



if __name__ == "__main__":
    main()