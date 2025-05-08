# Steganography Project

A simple application project that allows you to hide information (text) within different file types: **Images, Text, and Videos** using various techniques such as LSB and Parity, with a user-friendly graphical interface.

---

## Key Features
- **Hide and extract messages in images** (PNG, JPG, JPEG) using LSB and Parity techniques.
- **Hide and extract messages in video files** (MP4, AVI, MOV) using the LSB technique (with some known issues in extraction).
- **Hide and extract messages in text files** (TXT) using LSB and Parity techniques.
- Modern and user-friendly graphical interface built with the [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) library.
- Automatically saves output files in the `Output` folder.

---

## Application Screenshots
![image](https://github.com/user-attachments/assets/2581751c-c83c-4776-81c5-d78dae8e9eb8)
![image](https://github.com/user-attachments/assets/1acfeee6-f100-411d-9487-6c34da38f289)

---

## Requirements
Before running the project, install the following packages:

```bash
pip install customtkinter pillow numpy opencv-python
```

---

## How to Run
To run the application:

```bash
python steganography.py
```

---

## Known Issues
- Extracting messages from videos may not work correctly in some cases.
- The message size must be appropriate for the file size (image/video/text), otherwise an error message will be displayed.

---

