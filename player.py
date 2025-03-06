
from tkinter import filedialog
from tkinter import *
import yt_dlp
import pygame
import os
import random
from tkinter import Tk, filedialog, Button, Entry, Label, StringVar, messagebox

root = Tk()
root.title('Music Player')
root.geometry("600x300")

pygame.mixer.init()

menubar = Menu(root)
root.config(menu = menubar)

songs = []
current_song = ""
paused = False

def addPlaylist():
    def choose_folder():
        folder = filedialog.askdirectory(title="Select Download Folder")
        if folder:
            folder_path.set(folder)

    # Function to download the playlist
    def download_playlist():
        playlist_url = playlist_url_entry.get()
        download_folder = folder_path.get()

        if not playlist_url:
            messagebox.showerror("Error", "Please enter a playlist URL.")
            return
        if not download_folder:
            messagebox.showerror("Error", "Please select a download folder.")
            return

        # Ensure the output folder exists
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # Set the output template to include the selected folder
        output_path = os.path.join(download_folder, '%(playlist_index)s - %(title)s.%(ext)s')

        ydl_opts = {
            'format': 'bestaudio/best',  # Download the best audio quality
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',  # Convert to MP3
                'preferredquality': '192',  # Audio quality
            }],
            'outtmpl': output_path,  # Output file template
            'ignoreerrors': True,  # Skip errors in case of unavailable videos
            'extract_flat': False,  # Ensure full video details are fetched
            'progress_hooks': [lambda d: update_progress(d)],  # Update progress
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([playlist_url])
            messagebox.showinfo("Success", "Playlist downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to update download progress
    def update_progress(data):
        if data['status'] == 'downloading':
            progress_label.config(text=f"Downloading: {data['filename']} - {data['_percent_str']}")

    # Create the main GUI window
    root = Tk()
    root.title("YouTube Playlist MP3 Downloader")
    root.geometry("500x200")

    # Playlist URL input
    Label(root, text="Enter Playlist URL:").grid(row=0, column=0, padx=10, pady=10)
    playlist_url_entry = Entry(root, width=40)
    playlist_url_entry.grid(row=0, column=1, padx=10, pady=10)

    # Folder selection
    Label(root, text="Download Folder:").grid(row=1, column=0, padx=10, pady=10)
    folder_path = StringVar()
    folder_entry = Entry(root, textvariable=folder_path, width=40, state='readonly')
    folder_entry.grid(row=1, column=1, padx=10, pady=10)
    Button(root, text="Browse", command=choose_folder).grid(row=1, column=2, padx=10, pady=10)

    # Progress label
    progress_label = Label(root, text="", fg="blue")
    progress_label.grid(row=2, column=0, columnspan=3, pady=10)

    # Download button
    Button(root, text="Download Playlist", command=download_playlist).grid(row=3, column=0, columnspan=3, pady=20)

    # Run the GUI
    root.mainloop()


def load_music():
    global current_song, songs
    # Open the file dialog to select the directory
    root.directory = filedialog.askdirectory()
    
    if not root.directory:
        return  # If no directory is selected, exit the function
    
    songs = []  # Clear the previous song list
    # Loop through files in the selected directory
    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext.lower() == ".mp3":  # Only consider .mp3 files
            songs.append(song)  # Add the song name to the list
    
    # Clear the Listbox and populate it with the songs
    songlist.delete(0, END)
    for song in songs:
        songlist.insert("end", song)  # Insert each song in the Listbox
    
    if songs:
        songlist.selection_set(0)  # Select the first song
        current_song = songs[songlist.curselection()[0]]

def play_music():
    global current_song, paused
    if not paused:
        pygame.mixer.music.load(os.path.join(root.directory, current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False
    
def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True
    
def next_music():
    global current_song, paused
    try:
        songlist.selection_clear(0,END)
        songlist.selection_set(songs.index(current_song)+1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

def prev_music():
    global current_song, paused
    try:
        songlist.selection_clear(0,END)
        songlist.selection_set(songs.index(current_song)-1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass
    
def shuffleMusic():
    random.shuffle(songs)
    
    # Clear the current Listbox
    songlist.delete(0, END)
    
    # Re-insert the shuffled songs into the Listbox
    for song in songs:
        songlist.insert("end", song)

organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label = 'Select Folder', command = load_music)
menubar.add_cascade(label='organise', menu = organise_menu)

yt_menu = Menu(menubar, tearoff = False)
yt_menu.add_command(label= 'add playlist', command = addPlaylist)
menubar.add_cascade(label = 'add playlist', menu= yt_menu)


# Listbox for displaying songs
songlist = Listbox(root, bg="black", fg="Blue", width=100, height=15, bd=2, relief="solid")
songlist.pack(pady=10)

# Load button images and keep references to them
play_btn_image = PhotoImage(file='play.png')
pause_btn_image = PhotoImage(file='pause.png')
next_btn_image = PhotoImage(file='next.png')
previous_btn_image = PhotoImage(file='previous.png')
shuffle_btn_image = PhotoImage(file='shuffle.png')

# Create a frame to hold the buttons
control_frame = Frame(root)
control_frame.pack(pady=10)  # Padding around the frame for spacing

# Create the buttons using the images
play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command = play_music)
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command = pause_music)
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command = next_music)
previous_btn = Button(control_frame, image=previous_btn_image, borderwidth=0, command = prev_music)
shuffle_btn = Button(control_frame, image=shuffle_btn_image, borderwidth=0, command = shuffleMusic)

# Grid layout for the buttons in the frame
play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
previous_btn.grid(row=0, column=0, padx=7, pady=10)
shuffle_btn.grid(row=0, column=4, padx=7, pady=10)

# Keep references to the images to avoid garbage collection
play_btn.image = play_btn_image
pause_btn.image = pause_btn_image
next_btn.image = next_btn_image
previous_btn.image = previous_btn_image



root.mainloop()