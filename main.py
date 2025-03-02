import tkinter
from tkinter import filedialog
import customtkinter
from pytubefix import YouTube
from PIL import ImageTk, Image
import requests
from io import BytesIO
import os


path = ''

def browse_dir():
    global path
    directory_path = filedialog.askdirectory()
    if directory_path:
        dir_button.configure(text=directory_path)
        path = directory_path
        print(path)

def download_video():
    try:
        choice = combo.get()
        url= link.get()
        pPercentage.configure(text= "0%")
        pPercentage.update()
        progressbar.set(0)
        ytb = YouTube(url, on_progress_callback= progress)
        if(choice == "mp3"):
            stream = ytb.streams.filter(only_audio=True).first()
            stream.download(filename=ytb.title+".mp3", output_path=path)
        else:
            stream = ytb.streams.get_highest_resolution()
            stream.download(output_path=path)
      
        VideoName.configure(text= "Video Name: " + ytb.title, font=("Arial", 25, "bold"))
        ViewsName.configure(text= "Video views: " + str(ytb.views), font=("Arial", 25, "bold"))
        thumb_url = ytb.thumbnail_url

        response = requests.get(thumb_url)
        img_data = BytesIO(response.content)

        pil_img = Image.open(img_data)
        img = customtkinter.CTkImage(light_image=pil_img, dark_image=pil_img, size=(720, 480))
        img_label.configure(image=img)
        img_label.update()
        print("Downloaded") 
    except Exception as e:

        print("Failed to download, error:", e)
        title.configure(text="Failed to download, error: " + str(e), text_color="red")
        title.update()
def progress(stream, chunk, bytes_remaining):
    total = stream.filesize
    bytes_downloaded = total - bytes_remaining
    percentage = (bytes_downloaded / total) * 100
    
    per = str(int(percentage))
    pPercentage.configure(text= per + "%")
    pPercentage.update()
    progressbar.set(float(percentage)/100)
    
#system settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")
#app frame
app = customtkinter.CTk()
app.geometry("1280x1080")

app.title("Youtube Downloader")

title = customtkinter.CTkLabel(app, text="Insert a link:")
title.pack(padx=10, pady=5)

url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=20, textvariable=url_var)
link.pack(padx=10, pady=5)
dir_button = customtkinter.CTkButton(app, width=140, height = 20, text="Browse:", corner_radius=15, command=browse_dir)
dir_button.pack(padx=10, pady=0)


text2 = customtkinter.CTkLabel(app, text="Download as: (Default is app directory)")
text2.pack()

options = ["mp4", "mp3"]

combo = customtkinter.CTkComboBox(app, values=options, width=80)
combo.pack()



img_label = customtkinter.CTkLabel(app, text="")
img_label.pack(padx=10, pady=5)
VideoName = customtkinter.CTkLabel(app, text="Video Name: ")
VideoName.pack(padx=10, pady=5)
ViewsName = customtkinter.CTkLabel(app, text="Video views: ")
ViewsName.pack(padx=10, pady=5)



pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()

progressbar = customtkinter.CTkProgressBar(app, width=400)
progressbar.set(0)
progressbar.pack(padx = 10, pady = 5)



download = customtkinter.CTkButton(app, text="Download", width=20, height=2, command=download_video)
download.pack()



app.mainloop()