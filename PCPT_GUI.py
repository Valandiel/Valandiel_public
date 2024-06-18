import customtkinter
from tkinter import *
from PCPT_BackEnd import PlaylistConverter

def run_backend():
    # Fetch the values from the GUI elements
    file_name = file_entry.get()
    process = clicked.get()
    xspf_music_directory_output = directory_entry.get()
    
    # Create an instance of PC with these values
    playlist_converter = PlaylistConverter(file_name, process, xspf_music_directory_output)
    
    # Call the main method of PC instance
    playlist_converter.main()

#interface

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("800x500")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60,fill="both", expand=True)

title_label = customtkinter.CTkLabel(master=frame, text="Playlist Directory Manager")
title_label.pack(pady=12, padx=10)

file_label = customtkinter.CTkLabel(master=frame, text="Input file name :")
file_label.pack(pady=12, padx=10)

file_entry = customtkinter.CTkEntry(master=frame, placeholder_text="File name")
file_entry.pack(pady=12, padx=20)

directory_label = customtkinter.CTkLabel(master=frame, text="Input the directory expected for your musics in your playlist:")
directory_label.pack(pady=12, padx=10)

directory_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Directory", width=400)
directory_entry.pack(pady=12, padx=10)

convert_button = customtkinter.CTkButton(master=frame, text="Convert", command=run_backend)
convert_button.pack(pady=12, padx=10)

def process_option_selected(choice):
    myLabel = customtkinter.CTkLabel(root, text=choice)
    myLabel.pack()

process_options = ["Directory","Convert"]

clicked = StringVar()
clicked.set(process_options[0])

drop = customtkinter.CTkOptionMenu(root, variable=clicked, values=process_options, command=process_option_selected)
drop.pack(pady=20)

root.mainloop()