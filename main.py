import customtkinter as ctk
import tkinter as tk
from engine.model import load_model
from engine.utils import predict_digit
from tkinter import *
from PIL import Image, ImageDraw
import numpy as np

# Load trained model
load_model("models/emnist_ds.keras")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Handwritten Digit Recognizer(emnist)")
        self.geometry("600x400")
        self.resizable(False, False)

        ctk.set_appearance_mode("Dark")  
        ctk.set_default_color_theme("blue")  

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Handwritten\nDigit\nRecognizer\n(emnist)", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.classify_btn = ctk.CTkButton(self.sidebar_frame, text="Recognize Digit", width= 150, height= 30, command=self.classify_handwriting)
        self.classify_btn.grid(row=1, column=0, padx=20, pady=10)

        self.clear_btn = ctk.CTkButton(self.sidebar_frame, text="Clear Canvas", width= 150, height= 30, command=self.clear_all, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.clear_btn.grid(row=2, column=0, padx=20, pady=10)
        
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.label = ctk.CTkLabel(self.main_area, text="Draw a digit...", font=ctk.CTkFont(size=24))
        self.label.pack(pady=(0, 10))
        
        self.canvas_width = 300
        self.canvas_height = 300
        self.canvas = tk.Canvas(self.main_area, width=self.canvas_width, height=self.canvas_height, bg="white", cursor="cross", highlightthickness=0)
        self.canvas.pack(pady=10)

        self.image = Image.new("L", (self.canvas_width, self.canvas_height), 255)
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def draw_lines(self, event):
        r = 10
        x, y = event.x, event.y

        self.canvas.create_oval(
            x - r, y - r, x + r, y + r,
            fill="black",
            outline="black"
        )

        self.draw.ellipse(
            (x - r, y - r, x + r, y + r),
            fill=0
        )

    def clear_all(self):
        self.canvas.delete("all")
        self.image = Image.new("L", (self.canvas_width, self.canvas_height), 255)
        self.draw = ImageDraw.Draw(self.image)
        self.label.config(text="Draw a digit")

    def classify_handwriting(self):
        digit, acc = predict_digit(self.image)
        self.label.configure(text=f"{digit} ({int(acc * 100)}%)")


if __name__ == "__main__":
    app = App()
    app.mainloop()