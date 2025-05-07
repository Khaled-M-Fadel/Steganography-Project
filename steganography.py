import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import os
import cv2
import shutil

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Application")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Window size
        window_width = 800
        window_height = 600

        # Center the window on the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.root.resizable(False, False)  # Disable resizing

        # Main Frame
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="#1A1A1A")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        ctk.CTkLabel(
            self.main_frame, 
            text="Select File Type", 
            font=("Roboto", 28, "bold"), 
            text_color="#FFFFFF"
        ).pack(pady=30)

        # Buttons style
        button_style = {
            "font": ("Roboto", 16), 
            "corner_radius": 15, 
            "fg_color": "#00D4FF", 
            "hover_color": "#33E4FF", 
            "text_color": "#1A1A1A"
        }

        # File type buttons
        ctk.CTkButton(
            self.main_frame, 
            text="Image", 
            command=self.open_image_window, 
            height=50, 
            **button_style
        ).pack(pady=15, padx=50, fill="x")
        ctk.CTkButton(
            self.main_frame, 
            text="Video", 
            command=self.open_video_window, 
            height=50, 
            **button_style
        ).pack(pady=15, padx=50, fill="x")
        ctk.CTkButton(
            self.main_frame, 
            text="Text", 
            command=self.open_text_window, 
            height=50, 
            **button_style
        ).pack(pady=15, padx=50, fill="x")

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def open_image_window(self):
        self.clear_frame(self.main_frame)
        ctk.CTkLabel(
            self.main_frame, 
            text="Image Steganography", 
            font=("Roboto", 24, "bold"), 
            text_color="#FFFFFF"
        ).pack(pady=20)

        # File selection
        ctk.CTkButton(
            self.main_frame, 
            text="Select Image", 
            command=self.select_image, 
            font=("Roboto", 14), 
            corner_radius=10, 
            fg_color="#00D4FF", 
            hover_color="#33E4FF", 
            text_color="#1A1A1A"
        ).pack(pady=10)
        self.image_path_label = ctk.CTkLabel(self.main_frame, text="No image selected", font=("Roboto", 12), text_color="#D3D3D3")
        self.image_path_label.pack()

        # Message input
        ctk.CTkLabel(self.main_frame, text="Message to Hide:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.message_entry = ctk.CTkEntry(self.main_frame, width=400, font=("Roboto", 14), fg_color="#252525", text_color="#FFFFFF")
        self.message_entry.pack()

        # Technique selection
        ctk.CTkLabel(self.main_frame, text="Technique:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.technique = ctk.CTkOptionMenu(
            self.main_frame, 
            values=["LSB", "Parity"], 
            font=("Roboto", 14), 
            fg_color="#00D4FF", 
            button_color="#00D4FF", 
            button_hover_color="#33E4FF", 
            text_color="#1A1A1A"
        )
        self.technique.pack()

        # Action buttons
        ctk.CTkButton(
            self.main_frame, 
            text="Hide Message", 
            command=self.hide_image_message, 
            font=("Roboto", 14), 
            corner_radius=10, 
            fg_color="#28A745", 
            hover_color="#3CC45F", 
            text_color="#FFFFFF"
        ).pack(pady=10)
        ctk.CTkButton(
            self.main_frame, 
            text="Extract Message", 
            command=self.extract_image_message, 
            font=("Roboto", 14), 
            corner_radius=10, 
            fg_color="#FFC107", 
            hover_color="#FFDB58", 
            text_color="#1A1A1A"
        ).pack(pady=10)
        ctk.CTkButton(
            self.main_frame, 
            text="Back", 
            command=self.back_to_main, 
            font=("Roboto", 14), 
            corner_radius=10, 
            fg_color="#6C757D", 
            hover_color="#ADB5BD", 
            text_color="#FFFFFF"
        ).pack(pady=10)

    def open_video_window(self):
        self.clear_frame(self.main_frame)
        ctk.CTkLabel(
            self.main_frame, 
            text="Video Steganography", 
            font=("Roboto", 24, "bold"), 
            text_color="#FFFFFF"
        ).pack(pady=20)

        # File selection
        ctk.CTkButton(
            self.main_frame, 
            text="Select Video", 
            command=self.select_video, 
            font=("Roboto", 14), 
            corner_radius=10, 
            fg_color="#00D4FF", 
            hover_color="#33E4FF", 
            text_color="#1A1A1A"
        ).pack(pady=10)
        self.video_path_label = ctk.CTkLabel(self.main_frame, text="No video selected", font=("Roboto", 12), text_color="#D3D3D3")
        self.video_path_label.pack()

        # Message input
        ctk.CTkLabel(self.main_frame, text="Message to Hide:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.video_message_entry = ctk.CTkEntry(self.main_frame, width=400, font=("Roboto", 14), fg_color="#252525", text_color="#FFFFFF")
        self.video_message_entry.pack()

        # Technique selection
        ctk.CTkLabel(self.main_frame, text="Technique:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.video_technique = ctk.CTkOptionMenu(
            self.main_frame, 
            values=["LSB"], 
            font=("Roboto", 14), 
            fg_color="#00D4FF", 
            button_color="#00D4FF", 
            button_hover_color="#33E4FF", 
            text_color="#1A1A1A"
        )
        self.video_technique.pack()

        # Action buttons
        ctk.CTkButton(
            self.main_frame, 
            text="Hide Message", 
            command=self.hide_video_message, 
            font=("Roboto", 14), 
            corner_radius=10, 
            fg_color="#28A745", 
            hover_color="#3CC45F", 
            text_color="#FFFFFF"
        ).pack(pady=10)
        ctk.CTkButton(
            self.main_frame, 
            text="Extract Message", 
            command=self.extract_video_message, 
            font=("Roboto", 14), 
            corner_radius=10, 
            fg_color="#FFC107", 
            hover_color="#FFDB58", 
            text_color="#1A1A1A"
        ).pack(pady=10)
        ctk.CTkButton(
            self.main_frame, 
            text="Back", 
            command=self.back_to_main, 
            font=("Roboto", 14), 
            corner_radius=10, 
            fg_color="#6C757D", 
            hover_color="#ADB5BD", 
            text_color="#FFFFFF"
        ).pack(pady=10)

    def open_text_window(self):
        self.clear_frame(self.main_frame)
        ctk.CTkLabel(
            self.main_frame, 
            text="Text Steganography", 
            font=("Roboto", 24, "bold"), 
            text_color="#FFFFFF"
        ).pack(pady=20)

        # File selection
        ctk.CTkButton(
            self.main_frame, 
            text="Select Text File", 
            command=self.select_text_file, 
            font=("Roboto", 14), 
            corner_radius=10, 
            fg_color="#00D4FF", 
            hover_color="#33E4FF", 
            text_color="#1A1A1A"
        ).pack(pady=10)
        self.text_path_label = ctk.CTkLabel(self.main_frame, text="No text file selected", font=("Roboto", 12), text_color="#D3D3D3")
        self.text_path_label.pack()

        # Message input
        ctk.CTkLabel(self.main_frame, text="Message to Hide:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.text_message_entry = ctk.CTkEntry(self.main_frame, width=400, font=("Roboto", 14), fg_color="#252525", text_color="#FFFFFF")
        self.text_message_entry.pack()

        # Technique selection
        ctk.CTkLabel(self.main_frame, text="Technique:", font=("Roboto", 14), text_color="#FFFFFF").pack(pady=10)
        self.text_technique = ctk.CTkOptionMenu(
            self.main_frame, 
            values=["LSB", "Parity"], 
            font=("Roboto", 14), 
            fg_color="#00D4FF", 
            button_color="#00D4FF", 
            button_hover_color="#33E4FF", 
            text_color="#1A1A1A"
        )
        self.text_technique.pack()

        # Action buttons
        ctk.CTkButton(
            self.main_frame, 
            text="Hide Message", 
            command=self.hide_text_message, 
            font=("Roboto", 14), 
            corner_radius=10, 
            fg_color="#28A745", 
            hover_color="#3CC45F", 
            text_color="#FFFFFF"
        ).pack(pady=10)
        ctk.CTkButton(
            self.main_frame, 
            text="Extract Message", 
            command=self.extract_text_message, 
            font=("Roboto", 14), 
            corner_radius=10, 
            fg_color="#FFC107", 
            hover_color="#FFDB58", 
            text_color="#1A1A1A"
        ).pack(pady=10)
        ctk.CTkButton(
            self.main_frame, 
            text="Back", 
            command=self.back_to_main, 
            font=("Roboto", 14), 
            corner_radius=10, 
            fg_color="#6C757D", 
            hover_color="#ADB5BD", 
            text_color="#FFFFFF"
        ).pack(pady=10)

    def back_to_main(self):
        self.clear_frame(self.main_frame)
        ctk.CTkLabel(
            self.main_frame, 
            text="Select File Type", 
            font=("Roboto", 28, "bold"), 
            text_color="#FFFFFF"
        ).pack(pady=30)
        button_style = {
            "font": ("Roboto", 16), 
            "corner_radius": 15, 
            "fg_color": "#00D4FF", 
            "hover_color": "#33E4FF", 
            "text_color": "#1A1A1A"
        }
        ctk.CTkButton(self.main_frame, text="Image", command=self.open_image_window, height=50, **button_style).pack(pady=15, padx=50, fill="x")
        ctk.CTkButton(self.main_frame, text="Video", command=self.open_video_window, height=50, **button_style).pack(pady=15, padx=50, fill="x")
        ctk.CTkButton(self.main_frame, text="Text", command=self.open_text_window, height=50, **button_style).pack(pady=15, padx=50, fill="x")

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            self.image_path = file_path
            self.image_path_label.configure(text=os.path.basename(file_path))

    def select_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.video_path = file_path
            self.video_path_label.configure(text=os.path.basename(file_path))

    def select_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.text_path = file_path
            self.text_path_label.configure(text=os.path.basename(file_path))

    def hide_image_message(self):
        if not hasattr(self, "image_path"):
            messagebox.showerror("Error", "Please select an image!")
            return
        message = self.message_entry.get()
        if not message:
            messagebox.showerror("Error", "Please enter a message!")
            return
        technique = self.technique.get()
        output_dir = "Output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, "output_image.png")

        try:
            img = Image.open(self.image_path).convert("RGB")
            if technique == "LSB":
                self.hide_lsb_image(img, message, output_path)
            else:
                self.hide_parity_image(img, message, output_path)
            messagebox.showinfo("Success", f"Message hidden in {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_image_message(self):
        if not hasattr(self, "image_path"):
            messagebox.showerror("Error", "Please select an image!")
            return
        technique = self.technique.get()

        try:
            img = Image.open(self.image_path).convert("RGB")
            if technique == "LSB":
                message = self.extract_lsb_image(img)
            else:
                message = self.extract_parity_image(img)
            messagebox.showinfo("Extracted Message", message or "No message found")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def hide_lsb_image(self, img, message, output_path):
        message += "\0"
        binary_message = ''.join(format(ord(c), '08b') for c in message)
        pixels = np.array(img, dtype=np.uint8)
        flat_pixels = pixels.ravel()
        if len(binary_message) > len(flat_pixels) * 3:
            raise ValueError("Message too large for image")

        index = 0
        for i in range(0, len(flat_pixels), 3):
            if index >= len(binary_message):
                break
            for j in range(3):
                if i + j < len(flat_pixels) and index < len(binary_message):
                    current_value = flat_pixels[i + j]
                    new_value = (current_value & 0xFE) | int(binary_message[index])
                    flat_pixels[i + j] = np.uint8(new_value)
                    index += 1
        pixels = flat_pixels.reshape(pixels.shape)
        Image.fromarray(pixels).save(output_path)

    def extract_lsb_image(self, img):
        pixels = np.array(img, dtype=np.uint8).ravel()
        binary_message = ""
        for i in range(0, len(pixels), 3):
            for j in range(3):
                if i + j < len(pixels):
                    binary_message += str(pixels[i + j] & 1)
                    if len(binary_message) % 8 == 0:
                        char = chr(int(binary_message[-8:], 2))
                        if char == "\0":
                            return "".join(chr(int(binary_message[k:k+8], 2)) for k in range(0, len(binary_message)-8, 8))
        return ""

    def hide_parity_image(self, img, message, output_path):
        message += "\0"
        binary_message = ''.join(format(ord(c), '08b') for c in message)
        pixels = np.array(img, dtype=np.uint8)
        flat_pixels = pixels.ravel()
        if len(binary_message) > len(flat_pixels):
            raise ValueError("Message too large for image")

        for i in range(len(binary_message)):
            pixel_sum = sum((flat_pixels[i] >> j) & 1 for j in range(8))
            if (pixel_sum % 2) != int(binary_message[i]):
                flat_pixels[i] ^= 1
        pixels = flat_pixels.reshape(pixels.shape)
        Image.fromarray(pixels).save(output_path)

    def extract_parity_image(self, img):
        pixels = np.array(img, dtype=np.uint8).ravel()
        binary_message = ""
        for i in range(len(pixels)):
            pixel_sum = sum((pixels[i] >> j) & 1 for j in range(8))
            binary_message += str(pixel_sum % 2)
            if len(binary_message) % 8 == 0:
                char = chr(int(binary_message[-8:], 2))
                if char == "\0":
                    return "".join(chr(int(binary_message[j:j+8], 2)) for j in range(0, len(binary_message)-8, 8))
        return ""

    def hide_video_message(self):
        if not hasattr(self, "video_path"):
            messagebox.showerror("Error", "Please select a video!")
            return
        message = self.video_message_entry.get()
        if not message:
            messagebox.showerror("Error", "Please enter a message!")
            return
        technique = self.video_technique.get()
        output_dir = "Output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, "output_video.mp4")

        try:
            # Create temporary directory for frames
            if os.path.exists("frames"):
                shutil.rmtree("frames")
            os.makedirs("frames")
            if os.path.exists("modified_frames"):
                shutil.rmtree("modified_frames")
            os.makedirs("modified_frames")

            # Step 1: Extract frames from video
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                raise ValueError("Could not open video file")

            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))

            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame_path = os.path.join("frames", f"frame_{frame_count:04d}.png")
                cv2.imwrite(frame_path, frame)
                frame_count += 1
            cap.release()

            if frame_count == 0:
                raise ValueError("No frames extracted from video")

            # Step 2: Hide message in frames using LSB
            message += "\0"
            binary_message = ''.join(format(ord(c), '08b') for c in message)
            bits_per_frame = (frame_width * frame_height * 3) // 3  # 1 bit per RGB pixel
            frames_needed = (len(binary_message) + bits_per_frame - 1) // bits_per_frame

            if frames_needed > frame_count:
                raise ValueError("Video too short to hide the message")

            bit_index = 0
            for i in range(frame_count):
                input_path = os.path.join("frames", f"frame_{i:04d}.png")
                output_path = os.path.join("modified_frames", f"frame_{i:04d}.png")

                if i < frames_needed and bit_index < len(binary_message):
                    img = Image.open(input_path).convert("RGB")
                    pixels = np.array(img, dtype=np.uint8)
                    flat_pixels = pixels.ravel()

                    for j in range(0, len(flat_pixels), 3):
                        if bit_index >= len(binary_message):
                            break
                        for k in range(3):
                            if j + k < len(flat_pixels) and bit_index < len(binary_message):
                                current_value = flat_pixels[j + k]
                                new_value = (current_value & 0xFE) | int(binary_message[bit_index])
                                flat_pixels[j + k] = np.uint8(new_value)
                                bit_index += 1

                    pixels = flat_pixels.reshape(pixels.shape)
                    Image.fromarray(pixels).save(output_path)
                else:
                    shutil.copy(input_path, output_path)

            # Step 3: Reconstruct video from modified frames
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

            for i in range(frame_count):
                frame_path = os.path.join("modified_frames", f"frame_{i:04d}.png")
                frame = cv2.imread(frame_path)
                out.write(frame)

            out.release()
            messagebox.showinfo("Success", f"Message hidden in {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            # Clean up temporary directories
            if os.path.exists("frames"):
                shutil.rmtree("frames")
            if os.path.exists("modified_frames"):
                shutil.rmtree("modified_frames")

    def extract_video_message(self):
        if not hasattr(self, "video_path"):
            messagebox.showerror("Error", "Please select a video!")
            return
        technique = self.video_technique.get()

        try:
            # Create temporary directory for frames
            if os.path.exists("frames"):
                shutil.rmtree("frames")
            os.makedirs("frames")

            # Step 1: Extract frames from video
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                raise ValueError("Could not open video file")

            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame_path = os.path.join("frames", f"frame_{frame_count:04d}.png")
                cv2.imwrite(frame_path, frame)
                frame_count += 1
            cap.release()

            if frame_count == 0:
                raise ValueError("No frames extracted from video")

            # Step 2: Extract message from frames using LSB
            binary_message = ""
            for i in range(frame_count):
                frame_path = os.path.join("frames", f"frame_{i:04d}.png")
                img = Image.open(frame_path).convert("RGB")
                pixels = np.array(img, dtype=np.uint8).ravel()
                for j in range(0, len(pixels), 3):
                    for k in range(3):
                        if j + k < len(pixels):
                            binary_message += str(pixels[j + k] & 1)
                            if len(binary_message) % 8 == 0:
                                char = chr(int(binary_message[-8:], 2))
                                if char == "\0":
                                    message = "".join(chr(int(binary_message[m:m+8], 2)) for m in range(0, len(binary_message)-8, 8))
                                    messagebox.showinfo("Extracted Message", message[:-1] or "No message found")
                                    return
            messagebox.showinfo("Extracted Message", "No message found or video too short")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            if os.path.exists("frames"):
                shutil.rmtree("frames")

    def hide_text_message(self):
        if not hasattr(self, "text_path"):
            messagebox.showerror("Error", "Please select a text file!")
            return
        message = self.text_message_entry.get()
        if not message:
            messagebox.showerror("Error", "Please enter a message!")
            return
        technique = self.text_technique.get()
        output_dir = "Output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, "output_text.txt")

        try:
            with open(self.text_path, "r", encoding="utf-8") as f:
                cover_text = f.read()
            if technique == "LSB":
                hidden_text = self.hide_lsb_text(cover_text, message)
            else:
                hidden_text = self.hide_parity_text(cover_text, message)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(hidden_text)
            messagebox.showinfo("Success", f"Message hidden in {output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_text_message(self):
        if not hasattr(self, "text_path"):
            messagebox.showerror("Error", "Please select a text file!")
            return
        technique = self.text_technique.get()

        try:
            with open(self.text_path, "r", encoding="utf-8") as f:
                text = f.read()
            if technique == "LSB":
                message = self.extract_lsb_text(text)
            else:
                message = self.extract_parity_text(text)
            messagebox.showinfo("Extracted Message", message or "No message found")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def hide_lsb_text(self, cover_text, message):
        message += "\0"
        binary_message = ''.join(format(ord(c), '08b') for c in message)
        result = ""
        cover_index = 0
        for bit in binary_message:
            while cover_index < len(cover_text) and cover_text[cover_index] not in " \n":
                result += cover_text[cover_index]
                cover_index += 1
            if cover_index >= len(cover_text):
                raise ValueError("Cover text too short")
            result += cover_text[cover_index]
            result += "\u200B" if bit == "1" else "\u200C"
            cover_index += 1
        result += cover_text[cover_index:]
        return result

    def extract_lsb_text(self, text):
        binary_message = ""
        i = 0
        while i < len(text):
            if text[i] in "\u200B\u200C":
                binary_message += "1" if text[i] == "\u200B" else "0"
                if len(binary_message) % 8 == 0:
                    char = chr(int(binary_message[-8:], 2))
                    if char == "\0":
                        return "".join(chr(int(binary_message[j:j+8], 2)) for j in range(0, len(binary_message)-8, 8))
            i += 1
        return ""

    def hide_parity_text(self, cover_text, message):
        message += "\0"
        binary_message = ''.join(format(ord(c), '08b') for c in message)
        result = ""
        bit_index = 0
        word_count = 0
        for char in cover_text:
            result += char
            if char in " \n" and bit_index < len(binary_message):
                word_count += 1
                if (word_count % 2) != int(binary_message[bit_index]):
                    result += "\u200B"
                bit_index += 1
        if bit_index < len(binary_message):
            raise ValueError("Cover text too short")
        return result

    def extract_parity_text(self, text):
        binary_message = ""
        word_count = 0
        i = 0
        while i < len(text):
            if text[i] in " \n":
                word_count += 1
                parity = word_count % 2
                if i + 1 < len(text) and text[i + 1] == "\u200B":
                    parity = 1 - parity
                    i += 1
                binary_message += str(parity)
                if len(binary_message) % 8 == 0:
                    char = chr(int(binary_message[-8:], 2))
                    if char == "\0":
                        return "".join(chr(int(binary_message[j:j+8], 2)) for j in range(0, len(binary_message)-8, 8))
            i += 1
        return ""

if __name__ == "__main__":
    root = ctk.CTk()
    app = SteganographyApp(root)
    root.mainloop()