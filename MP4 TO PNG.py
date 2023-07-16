import cv2
import os
from PIL import Image
import imagehash
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

def split_video_to_frames(video_path, output_directory):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Open the video file
    print("Splitting Video Into PNGs")
    video = cv2.VideoCapture(video_path)
    success, frame = video.read()
    count = 0
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Update the status text
    status_label.config(text=f"Splitting Video into PNGs: {video_path}")

    # Create the progress bar
    progress_bar = Progressbar(window, length=300, mode='determinate')
    progress_bar.pack()

    for count in range(total_frames):
        # Check if the cancel button was pressed
        if cancel_pressed:
            break

        # Save the frame as a PNG image
        frame_path = os.path.join(output_directory, f"frame_{count}.png")
        cv2.imwrite(frame_path, frame)

        # Update the progress bar
        progress = (count / total_frames) * 100
        progress_bar['value'] = progress
        window.update_idletasks()

        # Read the next frame
        success, frame = video.read()

    # Release the video file
    video.release()

    print(f"Split {count} frames from the video.")

def remove_duplicate_pngs(directory):
    # Get a list of all PNG files in the directory
    png_files = [file for file in os.listdir(directory) if file.endswith(".png")]

    # Dictionary to store the hash values and corresponding file paths
    hash_dict = {}

    # Update the status text
    status_label.config(text=f"Removing Duplicate PNGs: {directory}")

    # Iterate over each PNG file
    for png_file in png_files:
        # Check if the cancel button was pressed
        if cancel_pressed:
            break

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
    status_label.config(text="Processing Complete")

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
    input_entry.delete(0, tk.END)
    input_entry.insert(tk.END, file_path)

def browse_directory():
    directory_path = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(tk.END, directory_path)

def cancel_process():
    global cancel_pressed
    cancel_pressed = True

def process_video():
    global cancel_pressed
    cancel_pressed = False

    video_path = input_entry.get()
    output_directory = output_entry.get()
    disable_duplicates = duplicates_checkbox_var.get()

    if not video_path or not output_directory:
        messagebox.showerror("Error", "Please provide both input file and output directory.")
        return

    status_label.config(text="Processing Video...")
    window.update_idletasks()

    split_video_to_frames(video_path, output_directory)

    if not disable_duplicates:
        status_label.config(text="Removing Duplicates...")
        remove_duplicate_pngs(output_directory)

    messagebox.showinfo("Processing Complete", "Video processing complete!")
    status_label.config(text="Ready")

    # Show progress bar and cancel button
    progress_bar.pack()

# Create the Tkinter window
window = tk.Tk()
window.title("Video to Frames")
window.geometry("400x350")

# Create the input file path label and entry field
input_label = tk.Label(window, text="Input File Path:")
input_label.pack()
input_entry = tk.Entry(window, width=50)
input_entry.pack()
browse_file_button = tk.Button(window, text="Browse", command=browse_file)
browse_file_button.pack()

# Create the output directory label and entry field
output_label = tk.Label(window, text="Output Directory:")
output_label.pack()
output_entry = tk.Entry(window, width=50)
output_entry.pack()
browse_directory_button = tk.Button(window, text="Browse", command=browse_directory)
browse_directory_button.pack()

# Create the checkbox to disable duplicate removal
duplicates_checkbox_var = tk.BooleanVar()
duplicates_checkbox = tk.Checkbutton(
    window, text="Disable Duplicate Removal", variable=duplicates_checkbox_var
)
duplicates_checkbox.pack()

# Create the process button
process_button = tk.Button(window, text="Process Video", command=process_video)
process_button.pack()

# Create the status label
status_label = tk.Label(window, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(fill=tk.X)

# Create the progress bar and cancel button (initially hidden)
progress_bar = Progressbar(window, length=300, mode='determinate')
cancel_button = tk.Button(window, text="Cancel", command=cancel_process)

# Start the Tkinter event loop
window.mainloop()