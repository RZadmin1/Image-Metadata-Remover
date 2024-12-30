# utils.py

from PIL import Image
import piexif

import os
from pathlib import Path



def remove_metadata(image_path, output_path, ignore_list):
    """
    Remove metadata from a single image while respecting the given ignore list.
    Saves the metadata-free image to the specified output path.
    """
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Get EXIF data
            exif_data = img.info.get("exif", b"")
            
            if exif_data and isinstance(exif_data, bytes):
                # Load EXIF data using piexif
                exif_dict = piexif.load(exif_data)

                # Iterate over each IFD (Image File Directory)
                for ifd_name in list(exif_dict.keys()):
                    # Check if the current item has the '.items' attribute
                    if hasattr(exif_dict[ifd_name], "items"):
                        for tag, val in list(exif_dict[ifd_name].items()):
                            tag_name = piexif.TAGS[ifd_name].get(tag, {}).get("name", "Unknown")
                            
                            # If the tag is in the ignore list, skip it
                            if tag_name in ignore_list:
                                print(f"Skipping {tag_name} ({hex(tag)}) to avoid modifying image quality.")
                                continue
                            
                            # Otherwise, remove the tag
                            print(f"Removing {tag_name} ({hex(tag)})")
                            del exif_dict[ifd_name][tag]
                    else:
                        print(f"Skipped non-standard IFD: {ifd_name} (does not have .items attribute)")
                
                # Dump the modified EXIF data
                exif_bytes = piexif.dump(exif_dict)
                
                # Save the image without the removed metadata
                img.save(output_path, exif=exif_bytes)
                print(f"Image saved to {output_path} without unwanted metadata.")
            else:
                print("No EXIF data found or unsupported EXIF format.")
                # Save a copy of the original image to the output path
                img.save(output_path)
                print(f"Image saved to {output_path} without modification.")

    except Exception as e:
        print(f"Failed to remove metadata: {e}")



def sweep_metadata(input_path, output_path, ignore_list=None):
    """
    Removes metadata from all images in the input_path directory and saves them to the output_path directory.
    
    Args:
        input_path (str): Path to the directory containing input images.
        output_path (str): Path to the directory where metadata-free images will be saved.
        ignore_list (list, optional): List of metadata tag names to ignore during removal. Defaults to None.
    """
    if ignore_list is None:
        ignore_list = []
    
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)
    
    try:
        # Iterate through all files in the input directory
        for filename in os.listdir(input_path):
            input_file = os.path.join(input_path, filename)
            
            # Check if the file is an image (by extension)
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif')):
                output_file = os.path.join(output_path, filename)
                print(f"Processing {filename}...")
                
                # Attempt to remove metadata and save the new file
                try:
                    remove_metadata(input_file, output_file, ignore_list=ignore_list)
                    print(f"  Successfully saved metadata-free version to {output_file}.")
                except Exception as e:
                    print(f"  Failed to process {filename}: {e}")
            else:
                print(f"Skipping non-image file: {filename}")
    except Exception as e:
        print(f"Error while processing directory: {e}")



def display_metadata(image_path, ignore_list=[]):
    """
    Displays metadata for the selected image, ignoring specified tags.
    
    Args:
        image_path (str): Path to the image.
        ignore_list (list, optional): List of metadata tag names to ignore. Defaults to empty list [].
    """
    
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Print basic metadata from PIL
            print("Basic Metadata (PIL):")
            for key, value in img.info.items():
                print(f"  {key}: {value}")

            # Check if EXIF data exists and is in the correct format
            exif_data = img.info.get("exif")
            print(f"EXIF Data Type: {type(exif_data)}")  # Debugging line
            
            if exif_data and isinstance(exif_data, bytes):
                print("\nEXIF Metadata (piexif):")
                # Load EXIF data using piexif
                exif_dict = piexif.load(exif_data)

                for ifd_name in exif_dict:
                    print(f"IFD: {ifd_name}")
                    
                    # Check if the current item has the '.items' attribute (i.e., is a dictionary)
                    if hasattr(exif_dict[ifd_name], 'items'):
                        for tag, val in exif_dict[ifd_name].items():
                            tag_name = piexif.TAGS[ifd_name][tag]['name']
                            
                            # Skip tags in the ignore list
                            if tag_name in ignore_list:
                                # print(f"  [Ignored] {tag_name}")
                                continue
                            
                            print(f"  {tag_name}: {val}")
                    else:
                        print(f"  [Skipped] No items to display for IFD: {ifd_name}")
            else:
                print("\nNo EXIF data found or EXIF data is not in expected format.")

    except Exception as e:
        print(f"Failed to display metadata: {e}")



# def display_metadata(image_path):
#     """
#     Displays metadata for the selected image.
#     """
#     try:
#         # Open the image
#         with Image.open(image_path) as img:
#             # Print basic metadata from PIL
#             print("Basic Metadata (PIL):")
#             for key, value in img.info.items():
#                 print(f"  {key}: {value}")

#             # Check if EXIF data exists and is in the correct format
#             exif_data = img.info.get("exif")
#             print(f"EXIF Data Type: {type(exif_data)}")  # Debugging line
            
#             if exif_data and isinstance(exif_data, bytes):
#                 print("\nEXIF Metadata (piexif):")
#                 # Load EXIF data using piexif
                
#                 exif_dict = piexif.load(exif_data)
#                 """ if exif_dict:
#                     print(exif_dict)
#                     exif_dict.popitem() """
                
#                 for ifd_name in exif_dict:
#                     print(f"IFD: {ifd_name}")
                    
#                     # Check if the current item has the '.items' attribute (i.e., is a dictionary)
#                     if hasattr(exif_dict[ifd_name], 'items'):
#                         for tag, val in exif_dict[ifd_name].items():
#                             print(f"  {piexif.TAGS[ifd_name][tag]['name']}: {val}")
#                     else:
#                         print(f"  [Skipped] No items to display for IFD: {ifd_name}")
#             else:
#                 print("\nNo EXIF data found or EXIF data is not in expected format.")

#     except Exception as e:
#         print(f"Failed to display metadata: {e}")