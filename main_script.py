# Import the required libraries
import cv2
import torch
from PIL import Image
import os
import gradio as gr

# Your original code for the auto-zoom function
# ...

# Define a function to clear the input and output folders
def clear_folders():
    input_dir = "input"
    output_base_dir = "output"
    for folder in [input_dir, output_base_dir]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

# Define a function to run the auto-zoom function on the input folder and save the results in the output folder
def run_application():
    input_dir = "input"
    output_base_dir = "output"
    auto_zoom(input_dir, output_base_dir)

# Define a function to display the images in the output folder as a grid
def show_results():
    output_base_dir = "output"
    images = []
    for folder in os.listdir(output_base_dir):
        folder_path = os.path.join(output_base_dir, folder)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            img = Image.open(file_path)
            images.append(img)
    return gr.outputs.ImageGrid(images)

# Define a function to upload an image to the input folder and resize it according to the height and width sliders
def upload_image(image, height, width):
    input_dir = "input"
    image.save(os.path.join(input_dir, "image.jpg"))
    img = cv2.imread(os.path.join(input_dir, "image.jpg"))
    img = cv2.resize(img, (width, height))
    cv2.imwrite(os.path.join(input_dir, "image.jpg"), img)

# Create a Gradio interface with four components:
# - A file upload component to upload an image to the input folder
# - Two sliders to select the height and width of the image
# - Two buttons, one to clear folders and the other to run the auto-zoom function
# - An image grid component to display the results

iface = gr.Interface(
    fn=[upload_image, clear_folders, run_application, show_results],
    inputs=[gr.inputs.Image(type="file", label="Upload an image"), gr.inputs.Slider(100, 1000, 1, 512, label="Height"), gr.inputs.Slider(100, 1000, 1, 512, label="Width")],
    outputs=[None, None, None, gr.outputs.ImageGrid(label="Results")],
    layout="vertical",
    live=False,
    title="Auto-Zoom Demo",
    description="This is a demo of an auto-zoom function that crops an image containing a human to different aspect ratios."
)

iface.launch()
