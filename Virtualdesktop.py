import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import boto3

# Your public S3 image URL
IMAGE_URL = 'https://donot-dare.s3.us-east-1.amazonaws.com/Desktop-Virtualization.jpg'

# Your AWS WorkSpace ID
WORKSPACE_ID = 'ws-5wfhj50nm'

# Your AWS region where the WorkSpace is located
REGION = 'us-east-1'

# Initialize boto3 WorkSpaces client
client = boto3.client('workspaces', region_name=REGION)

# Function to get WorkSpace status
def get_workspace_status():
    try:
        response = client.describe_workspaces(WorkspaceIds=[WORKSPACE_ID])
        status = response['Workspaces'][0]['State']
        return status
    except Exception as e:
        return f"Error: {str(e)}"

# Function triggered by the button
def open_virtual_desktop():
    status = get_workspace_status()
    if status == "AVAILABLE":
        messagebox.showinfo("Opening", "Virtual Desktop is available. Launch it from your AWS WorkSpaces client.")
    else:
        messagebox.showwarning("Status", f"Virtual Desktop is not ready. Current Status: {status}")

# GUI Setup
root = tk.Tk()
root.title("Cloud Virtual Desktop Access")
root.geometry("700x500")
root.configure(bg='white')

# Load Image from S3
try:
    img_data = requests.get(IMAGE_URL).content
    with open('temp_image.jpg', 'wb') as handler:
        handler.write(img_data)

    img = Image.open("temp_image.jpg")
    img = img.resize((650, 300))
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=photo, bg='white')
    label.image = photo
    label.pack(pady=10)
except Exception as e:
    label = tk.Label(root, text=f"Failed to load image: {e}", fg="red", bg='white')
    label.pack()

# Status label
status_label = tk.Label(root, text="Status: Checking...", font=("Arial", 14), bg='white')
status_label.pack(pady=5)

def update_status():
    status = get_workspace_status()
    status_label.config(text=f"Status: {status}")

update_status()

# Connect button
btn = tk.Button(root, text="Connect to Virtual Desktop", command=open_virtual_desktop,
                bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=15, pady=10)
btn.pack(pady=20)

root.mainloop()