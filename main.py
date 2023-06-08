import os
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import TkinterDnD

# Global background color
BG_COLOR = "#FFC0CB"


def add_watermark(image_paths):
    wm_image = Image.open("./watermark.png")  # watermark

    for img_path in image_paths:
        og_image = Image.open(img_path)  # original

        wm_width = int(og_image.width * 0.15)
        wm_height = int((wm_width / wm_image.width) * wm_image.height)
        wm_image = wm_image.resize((wm_width, wm_height))

        result_image = Image.new("RGBA", og_image.size)
        result_image.paste(og_image, (0, 0))

        position = (og_image.width - wm_image.width,
                    og_image.height - wm_image.height)

        result_image.paste(wm_image, position, mask=wm_image)
        os.makedirs("outputs", exist_ok=True)
        filename = os.path.basename(img_path)
        output_path = os.path.join("outputs", "result_" + filename)
        result_image.save(output_path)

        show_image(og_image, "Original Image")

        show_image(result_image, "Watermarked Image")

    status_label.config(text="Images saved in 'outputs' folder", bg=BG_COLOR)


def select_images():
    image_paths = filedialog.askopenfilenames(filetypes=[("All Files", "*.*")])
    if image_paths:
        add_watermark(image_paths)


def show_image(image, label_text):
    image = image.resize((400, 300))  # Adjust the size as desired

    photo = ImageTk.PhotoImage(image)

    image_frame = ttk.LabelFrame(window, text=label_text)
    image_frame.pack(padx=10, pady=10)
    image_label = tk.Label(image_frame, image=photo)
    image_label.pack()

    image_label.image = photo


window = TkinterDnD.Tk()
window.geometry("900x900")
window.configure(background=BG_COLOR)

style = ttk.Style()
style.theme_use("default")

text = "Add Watermark"
font_size = 60
padding = 10
style.configure(
    "ModernLabel.TLabel",
    font=("Arial Rounded MT Bold", font_size, "bold"),
    background=BG_COLOR,
    padding=padding
)

label = ttk.Label(window, style="ModernLabel.TLabel", text=text)
label.pack()

header_label = ttk.Label(window, text="Add files from top left",
                         font=("Arial", 16, "bold"),
                         background=BG_COLOR
                         )
header_label.pack()

menubar = tk.Menu(window)
window.config(menu=menubar)

file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="Open Images", command=select_images)

status_label = tk.Label(window, bg=BG_COLOR)
status_label.pack()

window.mainloop()
