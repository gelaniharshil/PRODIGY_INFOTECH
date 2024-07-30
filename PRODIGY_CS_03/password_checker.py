import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import hashlib
import random
import json

permutation_indices = []

def open_image():
    global img, img_display, permutation_indices
    file_path = filedialog.askopenfilename(filetypes=[("Image files", ".png;.jpg;.jpeg;.bmp")])
    if file_path:
        img = Image.open(file_path)
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        root.title(f"Image Encryption Tool - {file_path}")
        path_entry.delete(0, tk.END)
        path_entry.insert(0, file_path)
        permutation_indices = []

def save_image():
    if img:
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", ".png"), ("JPEG files", ".jpg"), ("All files", ".")])
        if file_path:
            img.save(file_path)
            messagebox.showinfo("Save Image", "Image saved successfully!")

def save_permutation_indices(file_path):
    global permutation_indices
    if permutation_indices:
        with open(file_path, 'w') as f:
            json.dump(permutation_indices, f)
        messagebox.showinfo("Save Indices", "Permutation indices saved successfully!")

def load_permutation_indices(file_path):
    global permutation_indices
    try:
        with open(file_path, 'r') as f:
            permutation_indices = json.load(f)
        messagebox.showinfo("Load Indices", "Permutation indices loaded successfully!")
        return True
    except Exception as e:
        messagebox.showerror("Load Indices", f"Error loading permutation indices: {e}")
        return False

def encrypt_image():
    global img, img_display, permutation_indices
    if img:
        method = method_var.get()
        encrypted_img = img.copy()
        pixels = encrypted_img.load()

        if method == "Substitution":
            for i in range(encrypted_img.size[0]):
                for j in range(encrypted_img.size[1]):
                    if len(pixels[i, j]) == 4:  # RGBA
                        r, g, b, a = pixels[i, j]
                        pixels[i, j] = (255-r, 255-g, 255-b, a)
                    else:  # RGB
                        r, g, b = pixels[i, j]
                        pixels[i, j] = (255-r, 255-g, 255-b)
            print("Substitution encryption complete")

        elif method == "Permutation":
            width, height = encrypted_img.size
            permutation_indices = generate_permutation_indices(width, height)
            shuffled_pixels = [pixels[i % width, i // width] for i in permutation_indices]

            # Apply the permutation
            for i in range(width * height):
                x = i % width
                y = i // width
                pixels[x, y] = shuffled_pixels[i]

            print("Permutation encryption complete")

 # Save permutation indices to a file
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", ".json")])
            if file_path:
                save_permutation_indices(file_path)

        elif method == "Transformation":
            for i in range(encrypted_img.size[0]):
                for j in range(encrypted_img.size[1]):
                    if len(pixels[i, j]) == 4:  # RGBA
                        r, g, b, a = pixels[i, j]
                        pixels[i, j] = (g, b, r, a)
                    else:  # RGB
                        r, g, b = pixels[i, j]
                        pixels[i, j] = (g, b, r)
            print("Transformation encryption complete")

        img = encrypted_img
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        messagebox.showinfo("Encrypt Image", "Image encrypted successfully!")
        print("Encryption method:", method)

def decrypt_image():
    global img, img_display, permutation_indices
    if img:
        method = method_var.get()
        decrypted_img = img.copy()
        pixels = decrypted_img.load()

        if method == "Substitution":
            for i in range(decrypted_img.size[0]):
                for j in range(decrypted_img.size[1]):
                    if len(pixels[i, j]) == 4:  # RGBA
                        r, g, b, a = pixels[i, j]
                        pixels[i, j] = (255-r, 255-g, 255-b, a)
                    else:  # RGB
                        r, g, b = pixels[i, j]
                        pixels[i, j] = (255-r, 255-g, 255-b)
            print("Substitution decryption complete")

        elif method == "Permutation":
            file_path = filedialog.askopenfilename(filetypes=[("JSON files", ".json")])
            if file_path and load_permutation_indices(file_path):
                width, height = decrypted_img.size
                inverse_permutation_indices = [0] * (width * height)
                for i, idx in enumerate(permutation_indices):
                    inverse_permutation_indices[idx] = i

                unshuffled_pixels = [None] * (width * height)
                for i in range(width * height):
                    x = i % width
                    y = i // width
                    unshuffled_pixels[i] = pixels[x, y]

                for i in range(width * height):
                    x = i % width
                    y = i // width
                    pixels[x, y] = unshuffled_pixels[inverse_permutation_indices[i]]

                print("Permutation decryption complete")
            else:
                messagebox.showerror("Decrypt Image", "No permutation information available!")

        elif method == "Transformation":
            for i in range(decrypted_img.size[0]):
                for j in range(decrypted_img.size[1]):
                    if len(pixels[i, j]) == 4:  # RGBA
                        r, g, b, a = pixels[i, j]
                        pixels[i, j] = (b, r, g, a)
                    else:  # RGB
                        r, g, b = pixels[i, j]
                        pixels[i, j] = (b, r, g)
            print("Transformation decryption complete")

        img = decrypted_img
        img_display = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor=tk.NW, image=img_display)
        messagebox.showinfo("Decrypt Image", "Image decrypted successfully!")
        print("Decryption method:", method)

def generate_permutation_indices(width, height):
    indices = list(range(width * height))
    random.shuffle(indices)
    return indices
root = tk.Tk()
root.title("Image Encryption Tool")

# Modern style layout
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()

frame = tk.Frame(root, bg='white')
frame.pack(pady=20)

open_button = tk.Button(frame, text="Open Image", bg='lightblue', command=open_image)
open_button.grid(row=0, column=0, padx=10, pady=10)

method_var = tk.StringVar(value="Substitution")
method_label = tk.Label(frame, text="Method:", bg='white')
method_label.grid(row=0, column=1, padx=10, pady=10)
method_menu = ttk.Combobox(frame, textvariable=method_var, values=["Substitution", "Permutation", "Transformation"], width=15)
method_menu.grid(row=0, column=2, padx=10, pady=10)
method_menu.current(0)

encrypt_button = tk.Button(frame, text="Encrypt Image", bg='lightgreen', command=encrypt_image)
encrypt_button.grid(row=0, column=3, padx=10, pady=10)

decrypt_button = tk.Button(frame, text="Decrypt Image", bg='lightcoral', command=decrypt_image)
decrypt_button.grid(row=0, column=4, padx=10, pady=10)

save_button = tk.Button(frame, text="Save Image", bg='lightyellow', command=save_image)
save_button.grid(row=0, column=5, padx=10, pady=10)

path_entry = tk.Entry(root, width=100)
path_entry.pack(pady=10)

img = None
img_display = None

root.mainloop()