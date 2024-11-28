from pydub import AudioSegment
import os

def convert_mp3_to_wav(mp3_file, wav_file):
    # Load the MP3 file
    audio = AudioSegment.from_mp3(mp3_file)
    
    # Export as WAV file
    audio.export(wav_file, format="wav")

# List to store the playlist (paths to songs)
folder_path = 'musicas'
all_files = os.listdir(folder_path)
playlist = [file[:-4] for file in all_files]

for song in playlist:
    mp3_file = f"musicas/{song}.mp3"  
    wav_file = f"wav/{song}.wav"  
    convert_mp3_to_wav(mp3_file, wav_file)
