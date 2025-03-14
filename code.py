import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

roi_entry_values = []

def perform_watermarking():
    try:
        global image, logo, alpha_value, roi

        if roi[3] - roi[2] > 0 and roi[1] - roi[0] > 0:

            logo_resized = cv2.resize(logo, (roi[3] - roi[2], roi[1] - roi[0]))
    
    # Apply alpha blending to blend the logo with the ROI of the image
        watermarked_image = image.copy()
        watermarked_image[roi[0]:roi[1], roi[2]:roi[3]] = cv2.addWeighted(image[roi[0]:roi[1], roi[2]:roi[3]], 1 - alpha_value, logo, alpha_value, 0)
    
    # Display the watermarked image
        cv2.imshow("Watermarked Image", watermarked_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print("error in perform_watermarking:", e)

def extract_watermark():
    try:
        global watermarked_image, alpha_value, roi
    
    # Extract the watermark by subtracting the original ROI from the watermarked ROI
        extracted_watermark = (watermarked_image[roi[0]:roi[1], roi[2]:roi[3]] - (1 - alpha_value) * image[roi[0]:roi[1], roi[2]:roi[3]]) / alpha_value
    
    # Display the extracted watermark
        cv2.imshow("Extracted Watermark", extracted_watermark.astype(np.uint8))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print("Error in extract_watermark:", e)    

def select_image():
    global image_path, image
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=(("Image files", "*.png;*.jpg;*.jpeg"),))
    if image_path:
        image = cv2.imread(image_path)

def select_logo():
    global logo_path, logo
    logo_path = filedialog.askopenfilename(title="Select Logo", filetypes=(("Image files", "*.png;*.jpg;*.jpeg"),))
    if logo_path:
        logo = cv2.imread(logo_path)

def update_alpha_value(value):
    global alpha_value
    alpha_value = float(value) / 100

def select_roi():
    global roi_window
    roi_window = tk.Toplevel(root)
    roi_window.title("Select ROI")

    
    tk.Label(roi_window, text="Y Start:").pack()
    roi_entry_values.append(tk.Entry(roi_window))
    roi_entry_values[0].pack()

    tk.Label(roi_window, text="Y End:").pack()
    roi_entry_values.append(tk.Entry(roi_window))
    roi_entry_values[1].pack()

    tk.Label(roi_window, text="X Start:").pack()
    roi_entry_values.append(tk.Entry(roi_window))
    roi_entry_values[2].pack()

    tk.Label(roi_window, text="X End:").pack()
    roi_entry_values.append(tk.Entry(roi_window))
    roi_entry_values[3].pack()

    tk.Button(roi_window, text="Confirm ROI", command=confirm_roi).pack()

def confirm_roi():
    global roi
    try:
        y_start = int(roi_entry_values[0].get())
        y_end = int(roi_entry_values[1].get())
        x_start = int(roi_entry_values[2].get())
        x_end = int(roi_entry_values[3].get())

        roi = (y_start, y_end, x_start, x_end)
        print("ROI set to:", roi)
        roi_window.destroy() 
    except Exception as e:
        print("Error confirming ROI:", e)




# Create a tkinter window
root = tk.Tk()
root.title("Watermarking GUI")

# Initialize variables
image_path = ""
logo_path = ""
image = None
logo = None
alpha_value = 0.5
roi = None

# Create GUI elements
tk.Label(root, text="Select Image:").pack()
tk.Button(root, text="Browse", command=select_image).pack()

tk.Label(root, text="Select Logo:").pack()
tk.Button(root, text="Browse", command=select_logo).pack()

tk.Label(root, text="Alpha Value:").pack()
alpha_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=update_alpha_value)
alpha_slider.set(50)  # Initial alpha value
alpha_slider.pack()

tk.Button(root, text="Select ROI", command=select_roi).pack()

tk.Button(root, text="Perform Watermarking", command=perform_watermarking).pack()
tk.Button(root, text="Extract Watermark", command=extract_watermark).pack()

root.mainloop()
