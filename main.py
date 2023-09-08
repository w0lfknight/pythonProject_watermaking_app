import tkinter as tk
from tkinter import filedialog, colorchooser
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk

image = None
image_path = None
watermark_text = ""
selected_text_color = (255, 255, 255)  # Default text color (white)
watermark_position = (10, 10)  # Initial watermark position

def upload_image():
    global image, image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])

    if image_path:
        image = Image.open(image_path)
        image.thumbnail((400, 400))  # Resize image to fit in GUI
        update_watermark_canvas()

def choose_text_color():
    global selected_text_color
    color = colorchooser.askcolor(initialcolor=selected_text_color, title="Select Text Color")
    if color[1]:
        selected_text_color = tuple(int(x) for x in color[0])
        update_color_button_color()

def update_color_button_color():
    color_button.config(bg='#%02x%02x%02x' % selected_text_color)

def add_watermark():
    global watermark_text
    watermark_text = watermark_entry.get()

    # Update watermark on the canvas
    update_watermark_canvas()

def update_watermark_canvas():
    global image, watermark_text, watermark_position
    if image:
        watermark_canvas.delete("all")
        image_tk = ImageTk.PhotoImage(image)
        watermark_canvas.create_image(0, 0, anchor="nw", image=image_tk, tags="image")
        watermark_canvas.image = image_tk
        watermark_canvas.create_text(watermark_position, text=watermark_text, fill=f'#{selected_text_color[0]:02x}{selected_text_color[1]:02x}{selected_text_color[2]:02x}', anchor="nw", font=("Helvetica", 12), tags="watermark")

def move_watermark(event):
    global watermark_position
    watermark_position = (event.x, event.y)
    update_watermark_canvas()

def save_watermarked_image():
    global image
    if image:
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if save_path:
            try:
                final_image = image.copy()
                draw = ImageDraw.Draw(final_image)
                draw.text(watermark_position, watermark_text, fill=(selected_text_color[0], selected_text_color[1], selected_text_color[2], 255), font=ImageFont.load_default())
                final_image.save(save_path)
                messagebox.showinfo("Saved", "Watermarked image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

root = tk.Tk()
root.title("Image Watermarking App")

upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack()

watermark_entry = tk.Entry(root)
watermark_entry.pack()

watermark_button = tk.Button(root, text="Add Watermark", command=add_watermark)
watermark_button.pack()

color_button = tk.Button(root, text="Choose Text Color", command=choose_text_color)
color_button.pack()

watermark_canvas = tk.Canvas(root, width=400, height=400, bg="white")
watermark_canvas.pack()
watermark_canvas.bind("<Button-1>", move_watermark)

save_button = tk.Button(root, text="Save Watermarked Image", command=save_watermarked_image)
save_button.pack()

root.mainloop()
