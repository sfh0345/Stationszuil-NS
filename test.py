import tkinter as tk
from PIL import Image, ImageTk


#define
def add_image_to_canvas(canvas, image_path, x, y, width, height):
    # Load the image and resize it
    original_image = Image.open(image_path)
    resized_image = original_image.resize((width, height))

    # Create a PhotoImage object from the resized image
    tk_image = ImageTk.PhotoImage(resized_image)

    # Create an image item at the specified coordinates
    canvas.create_image(x, y, anchor=tk.NW, image=tk_image)
    return tk_image


# Aanroepen functie
image_path = "assets/Nederlandse_Spoorwegen_logo.svg.png"
image = add_image_to_canvas(canvas, image_path, x=850, y=17, width=50, height=20)

