import cv2
import os
import os
from PIL import Image
import imagehash

def split_video_to_frames(video_path, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Open the video file
    print("Splitting Video Into PNGs")
    video = cv2.VideoCapture(video_path)
    success, frame = video.read()
    count = 0

    while success:
        # Save the frame as a PNG image
        frame_path = os.path.join(output_directory, f"frame_{count}.png")
        cv2.imwrite(frame_path, frame)

        # Read the next frame
        success, frame = video.read()
        count += 1

    # Release the video file
    video.release()

    print(f"Split {count} frames from the video.")

def remove_duplicate_pngs(directory):
    # Get a list of all PNG files in the directory
    png_files = [file for file in os.listdir(directory) if file.endswith(".png")]

    # Dictionary to store the hash values and corresponding file paths
    hash_dict = {}

    # Iterate over each PNG file
    for png_file in png_files:
        file_path = os.path.join(directory, png_file)

        # Open the image file
        image = Image.open(file_path)

        # Calculate the hash value
        image_hash = imagehash.average_hash(image)

        # Check if the hash value already exists in the dictionary
        if image_hash in hash_dict:
            # Remove the duplicate file
            os.remove(file_path)
            print(f"Removed duplicate file: {file_path}")
        else:
            # Add the hash value and file path to the dictionary
            hash_dict[image_hash] = file_path

    print("Duplicate files removed.")

# Directory containing PNG files
inputDir = input("Input File Path: ")
directory = input("Output Directory: ")

split_video_to_frames(inputDir, directory)
remove_duplicate_pngs(directory)