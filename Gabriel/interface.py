from tkinter import *
from tkinter import ttk, filedialog
import pygame
import os
from envia_serial import *
import json

# Keep track of current music playing
isPlaying = False

# Initialize Pygame mixer for audio playback
pygame.mixer.init()

# List to store the playlist (paths to songs)
folder_path = 'musicas'
all_files = os.listdir(folder_path)
playlist = [file[:-4] for file in all_files]
print(playlist)
current_song_index = 0  # Index of the currently playing song

with open("data.json", "r", encoding='utf-8') as file: # will help to track songs timestamps
    songs_json = json.load(file)
print(songs_json.keys())

current_song_info = {}
current_time_s = 0
states_count = 0 
current_state_time = 0
hue_brightness_index = 0
beats_index = 0

# Function to toggle fullscreen mode
def toggle_full_screen():
    is_fullscreen = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not is_fullscreen)

# Function to choose a song and update the interface
def choose_song():
    global current_song_index
    global current_song_info
    global isPlaying
    global songs_json
    global current_state_time
    global states_count
    global hue_brightness_index
    global beats_index
    
    # Open a file dialog to select an mp3 file from the 'musicas' folder
    song_path = filedialog.askopenfilename(
        initialdir="musicas",  # Default folder 'musicas'
        title="Escolha uma música",
        filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*"))
    )

    if song_path:  # If a file is selected
        # Get the song's name and update the label
        song_name = os.path.basename(song_path)[:-4]

        current_song_info = songs_json[song_name]
        current_state_time = current_song_info["state_time"]
        states_count = 0 
        hue_brightness_index = 0
        beats_index = 0

        song_status.config(text="Ouvindo agora")
        isPlaying = True
        song_label.config(text=f"{song_name}")

        # Update playlist's current song playing
        for index, song in enumerate(playlist):
            if (song == song_name):
                current_song_index = index

        # Switch to the music player frame
        main_frame.grid_forget()  # Hide the main frame
        music_player_frame.grid(row=0, column=0)  # Show the music player frame

        # Load and play the selected song
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=0, start=0.0)

def update_time():
    global current_time_s
    global states_count
    global hue_brightness_index
    global beats_index
    global isPlaying

    if isPlaying:
        try:
            # Get the current time in milliseconds and convert to seconds
            current_time_s = pygame.mixer.music.get_pos() / 1000

            if current_time_s >= states_count * current_state_time and current_time_s <= current_song_info["total_time_length"]:
                enviar_hue(current_song_info["hue"][hue_brightness_index])
                enviar_brightness(current_song_info["brightness"][hue_brightness_index])
                states_count += 1 
                hue_brightness_index += 1

            elif current_time_s >= current_song_info["beats"][beats_index]:
                enviar_batida()
                beats_index += 1
        # Song has reached its end
        except:
            isPlaying = False

        # minutes = int(current_time_s // 60)
        # seconds = int(current_time_s % 60)
    
    # Call this function again after 1 millisecond
    root.after(1, update_time)

# Function to play/pause the song
def play_pause_song():
    global isPlaying
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        play_button.config(text="Tocar")
        song_status.config(text="Música pausada")
        isPlaying = False
    else:
        pygame.mixer.music.unpause()
        play_button.config(text="Pausar")
        song_status.config(text="Ouvindo agora")
        isPlaying = True

def next_song():
    global current_song_index
    global isPlaying
    global current_song_info
    global current_state_time
    global hue_brightness_index
    global beats_index
    global states_count

    current_song_index += 1  # Move to the next song
    if current_song_index >= len(playlist):
        current_song_index = 0  # If we are at the end, loop back to the first song

    # Stop the current song
    pygame.mixer.music.stop()

    # Get the next song from the playlist
    next_song = playlist[current_song_index] 
    current_song_info = songs_json[next_song]   
    current_state_time = current_song_info["state_time"]
    hue_brightness_index = 0
    beats_index = 0
    states_count = 0

    # Update the UI
    play_button.config(text="Pausar")
    song_status.config(text="Ouvindo agora")
    song_label.config(text=f"{next_song}")

    next_song_path = f"./{folder_path}/{next_song}.mp3"

    # Load and play the next song
    pygame.mixer.music.load(next_song_path)
    pygame.mixer.music.play(loops=0, start=0.0)
    isPlaying = True

def previous_song():
    global current_song_index
    global isPlaying
    global current_song_info
    global current_state_time
    global hue_brightness_index
    global beats_index
    global states_count

    current_song_index -= 1  # Move to the previous song
    if current_song_index < 0:
        current_song_index = len(playlist) - 1  # If we are at the begin, loop back to the last song

    # Stop the current song
    pygame.mixer.music.stop()

    # Get the previous song from the playlist
    previous_song = playlist[current_song_index]    
    current_song_info = songs_json[previous_song]   
    current_state_time = 0
    hue_brightness_index = 0
    beats_index = 0
    states_count = 0

    # Update the UI
    play_button.config(text="Pausar")
    song_status.config(text="Ouvindo agora")
    song_label.config(text=f"{previous_song}")

    previous_song_path = f"./{folder_path}/{previous_song}.mp3"

    # Load and play the previous song
    pygame.mixer.music.load(previous_song_path)
    pygame.mixer.music.play(loops=0, start=0.0)
    isPlaying = True

# Function to stop the song
def stop_song():
    global isPlaying

    pygame.mixer.music.stop()
    play_button.config(text="Pausar")
    isPlaying = False
    music_player_frame.grid_forget()
    main_frame.grid(row=0, column=0)  # Show the music player frame 

# Create the main window
root = Tk()
root.attributes('-fullscreen', False)  # Don't start in full-screen mode

# Create a main frame
main_frame = ttk.Frame(root, padding=10)
main_frame.grid()

# Title Label
ttk.Label(main_frame, text="ROBÔ DANÇANTE").grid(column=3, row=3)

# Button to choose the song
choose_song_button = ttk.Button(main_frame, text="Escolher música", command=choose_song)
choose_song_button.grid(column=3, row=4)

# Button to toggle fullscreen
full_screen_button = ttk.Button(main_frame, text="Tela cheia", command=toggle_full_screen)
full_screen_button.grid(column=3, row=5)

# Button to exit the program
exit_button = ttk.Button(main_frame, text="Sair", command=root.destroy)
exit_button.grid(column=3, row=6)

# Create the music player frame (initially hidden)
music_player_frame = ttk.Frame(root, padding=10)

# Add a label for displaying the song name
song_status = ttk.Label(music_player_frame)
song_status.grid(column=1, row=0)

song_label = ttk.Label(music_player_frame) # , font=("Arial", 18)
song_label.grid(column=1, row=1)

# Previous Music button
next_button = ttk.Button(music_player_frame, text="Anterior", command=previous_song)
next_button.grid(column=1, row=2)

# Play/Pause button
play_button = ttk.Button(music_player_frame, text="Pausar", command=play_pause_song)
play_button.grid(column=1, row=3)

# Next Music button
next_button = ttk.Button(music_player_frame, text="Próxima", command=next_song)
next_button.grid(column=1, row=4)

# Stop button
stop_button = ttk.Button(music_player_frame, text="Encerrar player", command=stop_song)
stop_button.grid(column=1, row=5)

# Button to toggle fullscreen (for the new frame)
full_screen_button_music = ttk.Button(music_player_frame, text="Tela cheia", command=toggle_full_screen)
full_screen_button_music.grid(column=1, row=6)

# Button to exit the program from music player frame
exit_button_music = ttk.Button(music_player_frame, text="Sair", command=root.destroy)
exit_button_music.grid(column=1, row=7)
update_time()
# Run the Tkinter main loop
root.mainloop()