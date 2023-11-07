import os
import pydicom
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

# Function to convert a DICOM file to a PNG image
def dicom_to_png(input_path, output_path):
    dicom_data = pydicom.dcmread(input_path)
    image = dicom_data.pixel_array
    image = image - np.min(image)
    image = image / np.max(image)
    image = (image * 255).astype(np.uint8)
    img = Image.fromarray(image)
    img.save(output_path)

# Function to handle the conversion process
def convert_dicom_to_png():
    input_folder = input_path_entry.get()
    output_folder = output_path_entry.get()

    if not os.path.exists(input_folder):
        messagebox.showerror("Error", "Input folder does not exist.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.dcm'):
                input_path = os.path.join(root, file)
                output_file = os.path.splitext(file)[0] + '.png'
                output_path = os.path.join(output_folder, output_file)
                dicom_to_png(input_path, output_path)
    
    messagebox.showinfo("Conversion Complete", "DICOM to PNG conversion is complete.")

# Create the GUI window
window = tk.Tk()
window.title("DICOM to PNG Converter")

# Create input path selection
input_label = tk.Label(window, text="Select DICOM Input Folder:")
input_label.pack()
input_path_entry = tk.Entry(window)
input_path_entry.pack()
input_browse_button = tk.Button(window, text="Browse", command=lambda: input_path_entry.insert(0, filedialog.askdirectory()))
input_browse_button.pack()

# Create output path selection
output_label = tk.Label(window, text="Select PNG Output Folder:")
output_label.pack()
output_path_entry = tk.Entry(window)
output_path_entry.pack()
output_browse_button = tk.Button(window, text="Browse", command=lambda: output_path_entry.insert(0, filedialog.askdirectory()))
output_browse_button.pack()

# Create conversion button
convert_button = tk.Button(window, text="Convert to PNG", command=convert_dicom_to_png)
convert_button.pack()

# Start the GUI
window.mainloop()
window.destroy()

if __name__ == '__main__':
    convert_dicom_to_png()
    quit()