from tkinter import *
import tkinter as tk
import pygame
import os
import json
import threading

import cv2
import mediapipe as mp
from tkinter import ttk, filedialog
import tkinter as tk
from PIL import Image, ImageTk
from Gabriela.poses import dicionario_poses, dicionario_poses_pernas

from Gabriel.envia_serial import *
from Gabriela.camera import calcula_angulo, funcao_texto

__all__ = ["toggle_full_screen", "choose_song", "update_time", "play_pause_song", "next_song", "previous_song", "stop_song", "interface"]

'''
=========================================================
    Definições de variáveis globais e setup inicial
=========================================================
'''

# Poses captadas pela Câmera
pose_atual_braco = None
pose_atual_perna = None

# Keep track of current music playing
isPlaying = False
pygame.mixer.init()
folder_path = 'Gabriel/musicas'
all_files = os.listdir(folder_path)
playlist = [file[:-4] for file in all_files]
current_song_index = 0

with open("Gabriel/data.json", "r", encoding='utf-8') as file:  # will help to track songs timestamps
    songs_json = json.load(file)

current_song_info = {}
current_time_s = 0
states_count = 0
current_state_time = 0
hue_brightness_index = 0
beats_index = 0

# Create the main window
root = tk.Tk()
root.attributes('-fullscreen', False)

'''
=========================================================
    Definições de funções de interface com usuário
=========================================================
'''

def start_video_processing():
    video = cv2.VideoCapture(0) # Inicia captura de vídeo
   
    if not video.isOpened(): # Verifica que a captura foi inicada
        print("Erro: Não foi possível acessar a câmera.")
        exit()

    mp_pose = mp.solutions.pose # Importa a solução Pose do MediaPipe
    pose = mp_pose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5) # Parametros da função
    mp_draw = mp.solutions.drawing_utils # Importa as ferramentas de desenho do MediaPipe

    # Define o label (interface) do Tkinter 
    video_label = ttk.Label(root) # Colocar o video no label principal (root)
    video_label.grid(row=0, column=1) # Posiciona o video no label

    def update_video():
        ret, frame = video.read() # Inicializa leitura do vídeo

        if not ret: # Verifica se leitura foi feita
            print("Falha ao capturar o vídeo.")
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Converção de cores BGR para RGB (RGB: Padrão do MediaPipe)
        result = pose.process(frame_rgb) # Processa o quadro de imagem e rastrea os pontos

        # Verifica se os landmarks foram encontrados
        if result.pose_landmarks:

            # Chama as variáveis globais das posições atuais 
            global pose_atual_braco
            global pose_atual_perna

            # Desenha os landmarks na imagem
            mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            h, w, _ = frame.shape # Captura as dimensões do frame
            landmarks = result.pose_landmarks.landmark # Traça desenho entre pontos rastreados

            #-----------------------------------------------------------------------------------------------------------------------------------
            # Calcula as coordenadas dos pontos específicos
            # Pé Direito
            peDY = int(landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y * h)
            peDX = int(landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x * w)
            peDZ = int(landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].z)

            # Pé Esquerdo
            peEY = int(landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y * h)
            peEX = int(landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x * w)
            peEZ = int(landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].z)

            # Mão direita
            maoDY = int(landmarks[mp_pose.PoseLandmark.RIGHT_INDEX].y * h)
            maoDX = int(landmarks[mp_pose.PoseLandmark.RIGHT_INDEX].x * w)
            maoDZ = int(landmarks[mp_pose.PoseLandmark.RIGHT_INDEX].z)
            # Mão esquerda
            maoEY = int(landmarks[mp_pose.PoseLandmark.LEFT_INDEX].y * h)
            maoEX = int(landmarks[mp_pose.PoseLandmark.LEFT_INDEX].x * w)
            maoEZ = int(landmarks[mp_pose.PoseLandmark.LEFT_INDEX].z)

            # Torso direito
            torsoDX = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x * w)
            torsoDY = int(landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y * h)

            # Torso Esquerdo
            torsoEX = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].x * w)
            torsoEY = int(landmarks[mp_pose.PoseLandmark.LEFT_HIP].y * h)

            # Ombro Direito
            ombroDX = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w)
            ombroDY = int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h)

            # Ombro Esquerdo
            ombroEX = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x * w)
            ombroEY = int(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y * h)

            # Cotovelo Direito
            cotoveloDX = int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x * w)
            cotoveloDY = int(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y * h)

            # Cotovelo Esquerdo
            cotoveloEX = int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x * w)
            cotoveloEY = int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y * h)

            # Joelho Direito
            joelhoDX = int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].x * w)
            joelhoDY = int(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE].y * h)

            # Joelho Esquerdo
            joelhoEX = int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x * w)
            joelhoEY = int(landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y * h)

            #-----------------------------------------------------------------------------------------------------------------------------------
            # Calcula os ângulos e exibe (CALCULO DE ANGULO APENAS PARA EXIBIÇÃO: Entre vetor e vetor vertical)

            # Perna direita (baixo)
            anguloPDB = calcula_angulo(peDX, peDY, joelhoDX, joelhoDY)
            cv2.putText(frame, str(anguloPDB), (int((peDX+joelhoDX)/2)-40, int((peDY+joelhoDY)/2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Perna direita (cima)
            anguloPDC = calcula_angulo(joelhoDX, joelhoDY, torsoDX, torsoDY)
            cv2.putText(frame, str(anguloPDC), (int((joelhoDX+torsoDX)/2)-40, int((joelhoDY+torsoDY)/2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Perna esquerda (baixo)
            anguloPEB = calcula_angulo(peEX, peEY, joelhoEX, joelhoEY)
            cv2.putText(frame, str(anguloPEB), (int((peEX+joelhoEX)/2)+40, int((peEY+joelhoEY)/2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Perna esquerda (cima)
            anguloPEC = calcula_angulo(joelhoEX, joelhoEY, torsoEX, torsoEY)
            cv2.putText(frame, str(anguloPEC), (int((joelhoEX+torsoEX)/2)+40, int((joelhoEY+torsoEY)/2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Braço (cima) direito
            anguloBDC = calcula_angulo(cotoveloDX, cotoveloDY, ombroDX, ombroDY)
            cv2.putText(frame, str(anguloBDC), (int((cotoveloDX+ombroDX)/2)-40, int((cotoveloDY+ombroDY)/2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Braço (baixo) direito
            anguloBDB = calcula_angulo(maoDX, maoDY, cotoveloDX, cotoveloDY)
            cv2.putText(frame, str(anguloBDB), (int((cotoveloDX + maoDX) / 2)-40, int((cotoveloDY + maoDY) / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Braço (cima) esquerdo
            anguloBEC = calcula_angulo(cotoveloEX, cotoveloEY, ombroEX, ombroEY)
            cv2.putText(frame, str(anguloBEC), (int((cotoveloEX+ombroEX)/2)+40, int((cotoveloEY+ombroEY)/2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Braço (baixo) esquerdo
            anguloBEB = calcula_angulo(maoEX, maoEY, cotoveloEX, cotoveloEY)
            cv2.putText(frame, str(anguloBEB), (int((cotoveloEX + maoEX) / 2)+40, int((cotoveloEY + maoEY) / 2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            #-----------------------------------------------------------------------------------------------------------------------------------
            # Exibição visual

            texto = str(peDX) + "," + str(peDY) + "," + str(peDZ)
            cv2.putText(frame, texto, (peDX, peDY),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            texto = str(maoDX) + "," + str(maoDY) + "," + str(maoDZ)
            cv2.putText(frame, texto, (maoDX, maoDY),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            #-----------------------------------------------------------------------------------------------------------------------------------
            # Percorrer o dicionário e ver se a pessoa está fazendo uma das poses dos BRAÇOS
            for movimento, angulos in dicionario_poses.items():
                if angulos["condicao"](anguloBEC, anguloBEB, anguloBDC, anguloBDB):
                    cor = (255, 105, 180)
                    texto = movimento
                    coord1 = 10
                    coord2 = 300
                    pose_atual_braco = movimento
                    funcao_texto(texto, cor, frame, coord1, coord2)

            #-----------------------------------------------------------------------------------------------------------------------------------
            # Percorrer o dicionário e ver se a pessoa está fazendo uma das poses das PERNAS
            for movimento, angulos in dicionario_poses_pernas.items():
                if angulos["condicao"](anguloPEC, anguloPEB, anguloPDC, anguloPDB):
                    cor = (255, 105, 180)
                    texto = movimento
                    coord1 = 10
                    coord2 = 250
                    pose_atual_perna = movimento
                    funcao_texto(texto, cor, frame, coord1, coord2)



        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Converte o frame para Image (padrão do Tkinter)
        frame_img = Image.fromarray(frame_bgr)
        frame_tk = ImageTk.PhotoImage(frame_img)

        # Atualiza a imagem no Tkinter label
        video_label.img = frame_tk 
        video_label.configure(image=frame_tk)

        # Chama a função de novo a cada 1ms
        root.after(1, update_video)

    update_video()

def toggle_full_screen():
    '''
    Função que faz alterar para tela cheia.
    '''
    is_fullscreen = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not is_fullscreen)

# Function to choose a song and update the interface
def choose_song():
    '''
    Função que serve para permitir a escolha da música e atualiza a interface.
    '''
    global current_song_index
    global current_song_info
    global isPlaying
    global songs_json
    global current_state_time
    global states_count
    global hue_brightness_index
    global beats_index
    
    song_path = tk.filedialog.askopenfilename(
        initialdir="musicas",  # Default folder 'musicas'
        title="Escolha uma música",
        filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*"))
    )

    if song_path:
        song_name = os.path.basename(song_path)[:-4]

        current_song_info = songs_json[song_name]
        current_state_time = current_song_info["state_time"]
        states_count = 0 
        hue_brightness_index = 0
        beats_index = 0

        song_status.config(text="Ouvindo agora")
        isPlaying = True
        song_label.config(text=f"{song_name}")

        for index, song in enumerate(playlist):
            if song == song_name:
                current_song_index = index

        main_frame.grid_forget()  # Hide the main frame
        music_player_frame.grid(row=0, column=0)  # Show the music player frame

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
                envia_pose(pose_atual_braco)
                envia_pose(pose_atual_perna)
                #BACALHAU
                beats_index += 1
        # Song has reached its end
        except:
            isPlaying = False

        # minutes = int(current_time_s // 60)
        # seconds = int(current_time_s % 60)
    
    # Call this function again after 1 millisecond
    root.after(1, update_time)


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

    current_song_index += 1
    if current_song_index >= len(playlist):
        current_song_index = 0

    pygame.mixer.music.stop()

    next_song = playlist[current_song_index] 
    current_song_info = songs_json[next_song]   
    current_state_time = current_song_info["state_time"]
    hue_brightness_index = 0
    beats_index = 0
    states_count = 0

    play_button.config(text="Pausar")
    song_status.config(text="Ouvindo agora")
    song_label.config(text=f"{next_song}")

    next_song_path = f"./{folder_path}/{next_song}.mp3"

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

    current_song_index -= 1
    if current_song_index < 0:
        current_song_index = len(playlist) - 1

    pygame.mixer.music.stop()

    previous_song = playlist[current_song_index]    
    current_song_info = songs_json[previous_song]   
    current_state_time = 0
    hue_brightness_index = 0
    beats_index = 0
    states_count = 0

    play_button.config(text="Pausar")
    song_status.config(text="Ouvindo agora")
    song_label.config(text=f"{previous_song}")

    previous_song_path = f"./{folder_path}/{previous_song}.mp3"

    pygame.mixer.music.load(previous_song_path)
    pygame.mixer.music.play(loops=0, start=0.0)
    isPlaying = True

def stop_song():
    global isPlaying

    pygame.mixer.music.stop()
    play_button.config(text="Pausar")
    isPlaying = False
    music_player_frame.grid_forget()
    main_frame.grid(row=0, column=0)  

'''
=========================================================
    Interface do TkInter
=========================================================
'''

# Create a main frame
main_frame = tk.ttk.Frame(root, padding=10)
main_frame.grid()

# Title Label
tk.ttk.Label(main_frame, text="ROBÔ DANÇANTE").grid(column=3, row=3)

# Button to choose the song
choose_song_button = tk.ttk.Button(main_frame, text="Escolher música", command=choose_song)
choose_song_button.grid(column=3, row=4)

# Button to toggle fullscreen
full_screen_button = tk.ttk.Button(main_frame, text="Tela cheia", command=toggle_full_screen)
full_screen_button.grid(column=3, row=5)

# Button to exit the program
exit_button = tk.ttk.Button(main_frame, text="Sair", command=root.destroy)
exit_button.grid(column=3, row=6)

# Create the music player frame (initially hidden)
music_player_frame = tk.ttk.Frame(root, padding=10)

song_status = tk.ttk.Label(music_player_frame)
song_status.grid(column=1, row=0)

song_label = tk.ttk.Label(music_player_frame)  
song_label.grid(column=1, row=1)

next_button = tk.ttk.Button(music_player_frame, text="Anterior", command=previous_song)
next_button.grid(column=1, row=2)

play_button = tk.ttk.Button(music_player_frame, text="Pausar", command=play_pause_song)
play_button.grid(column=1, row=3)

next_button = tk.ttk.Button(music_player_frame, text="Próxima", command=next_song)
next_button.grid(column=1, row=4)

stop_button = tk.ttk.Button(music_player_frame, text="Encerrar player", command=stop_song)
stop_button.grid(column=1, row=5)

full_screen_button_music = tk.ttk.Button(music_player_frame, text="Tela cheia", command=toggle_full_screen)
full_screen_button_music.grid(column=1, row=6)

exit_button_music = tk.ttk.Button(music_player_frame, text="Sair", command=root.destroy)
exit_button_music.grid(column=1, row=7)

# Inicia o processamento de vídeo em uma thread separada para não bloquear o loop principal do Tkinter
thread = threading.Thread(target=start_video_processing, daemon=True)
thread.start()

# Chama as funções
update_time() # Atualiza a posição na música (para detectar batida)
root.mainloop() # Inicializa o root do Tkinter

# from tkinter import *
# from tkinter import ttk, filedialog
# import pygame
# import os
# from envia_serial import *
# import json

# # Keep track of current music playing
# isPlaying = False

# # Initialize Pygame mixer for audio playback
# pygame.mixer.init()

# # List to store the playlist (paths to songs)
# folder_path = 'musicas'
# all_files = os.listdir(folder_path)
# playlist = [file[:-4] for file in all_files]
# print(playlist)
# current_song_index = 0  # Index of the currently playing song

# with open("data.json", "r", encoding='utf-8') as file: # will help to track songs timestamps
#     songs_json = json.load(file)
# print(songs_json.keys())

# current_song_info = {}
# current_time_s = 0
# states_count = 0 
# current_state_time = 0
# hue_brightness_index = 0
# beats_index = 0

# # Function to toggle fullscreen mode
# def toggle_full_screen():
#     is_fullscreen = root.attributes('-fullscreen')
#     root.attributes('-fullscreen', not is_fullscreen)

# # Function to choose a song and update the interface
# def choose_song():
#     global current_song_index
#     global current_song_info
#     global isPlaying
#     global songs_json
#     global current_state_time
#     global states_count
#     global hue_brightness_index
#     global beats_index
    
#     # Open a file dialog to select an mp3 file from the 'musicas' folder
#     song_path = filedialog.askopenfilename(
#         initialdir="musicas",  # Default folder 'musicas'
#         title="Escolha uma música",
#         filetypes=(("MP3 files", "*.mp3"), ("All files", "*.*"))
#     )

#     if song_path:  # If a file is selected
#         # Get the song's name and update the label
#         song_name = os.path.basename(song_path)[:-4]

#         current_song_info = songs_json[song_name]
#         current_state_time = current_song_info["state_time"]
#         states_count = 0 
#         hue_brightness_index = 0
#         beats_index = 0

#         song_status.config(text="Ouvindo agora")
#         isPlaying = True
#         song_label.config(text=f"{song_name}")

#         # Update playlist's current song playing
#         for index, song in enumerate(playlist):
#             if (song == song_name):
#                 current_song_index = index

#         # Switch to the music player frame
#         main_frame.grid_forget()  # Hide the main frame
#         music_player_frame.grid(row=0, column=0)  # Show the music player frame

#         # Load and play the selected song
#         pygame.mixer.music.load(song_path)
#         pygame.mixer.music.play(loops=0, start=0.0)

# def update_time():
#     global current_time_s
#     global states_count
#     global hue_brightness_index
#     global beats_index
#     global isPlaying

#     if isPlaying:
#         try:
#             # Get the current time in milliseconds and convert to seconds
#             current_time_s = pygame.mixer.music.get_pos() / 1000

#             if current_time_s >= states_count * current_state_time and current_time_s <= current_song_info["total_time_length"]:
#                 enviar_hue(current_song_info["hue"][hue_brightness_index])
#                 enviar_brightness(current_song_info["brightness"][hue_brightness_index])
#                 states_count += 1 
#                 hue_brightness_index += 1

#             elif current_time_s >= current_song_info["beats"][beats_index]:
#                 enviar_batida()
#                 beats_index += 1
#         # Song has reached its end
#         except:
#             isPlaying = False

#         # minutes = int(current_time_s // 60)
#         # seconds = int(current_time_s % 60)
    
#     # Call this function again after 1 millisecond
#     root.after(1, update_time)

# # Function to play/pause the song
# def play_pause_song():
#     global isPlaying
#     if pygame.mixer.music.get_busy():
#         pygame.mixer.music.pause()
#         play_button.config(text="Tocar")
#         song_status.config(text="Música pausada")
#         isPlaying = False
#     else:
#         pygame.mixer.music.unpause()
#         play_button.config(text="Pausar")
#         song_status.config(text="Ouvindo agora")
#         isPlaying = True

# def next_song():
#     global current_song_index
#     global isPlaying
#     global current_song_info
#     global current_state_time
#     global hue_brightness_index
#     global beats_index
#     global states_count

#     current_song_index += 1  # Move to the next song
#     if current_song_index >= len(playlist):
#         current_song_index = 0  # If we are at the end, loop back to the first song

#     # Stop the current song
#     pygame.mixer.music.stop()

#     # Get the next song from the playlist
#     next_song = playlist[current_song_index] 
#     current_song_info = songs_json[next_song]   
#     current_state_time = current_song_info["state_time"]
#     hue_brightness_index = 0
#     beats_index = 0
#     states_count = 0

#     # Update the UI
#     play_button.config(text="Pausar")
#     song_status.config(text="Ouvindo agora")
#     song_label.config(text=f"{next_song}")

#     next_song_path = f"./{folder_path}/{next_song}.mp3"

#     # Load and play the next song
#     pygame.mixer.music.load(next_song_path)
#     pygame.mixer.music.play(loops=0, start=0.0)
#     isPlaying = True

# def previous_song():
#     global current_song_index
#     global isPlaying
#     global current_song_info
#     global current_state_time
#     global hue_brightness_index
#     global beats_index
#     global states_count

#     current_song_index -= 1  # Move to the previous song
#     if current_song_index < 0:
#         current_song_index = len(playlist) - 1  # If we are at the begin, loop back to the last song

#     # Stop the current song
#     pygame.mixer.music.stop()

#     # Get the previous song from the playlist
#     previous_song = playlist[current_song_index]    
#     current_song_info = songs_json[previous_song]   
#     current_state_time = 0
#     hue_brightness_index = 0
#     beats_index = 0
#     states_count = 0

#     # Update the UI
#     play_button.config(text="Pausar")
#     song_status.config(text="Ouvindo agora")
#     song_label.config(text=f"{previous_song}")

#     previous_song_path = f"./{folder_path}/{previous_song}.mp3"

#     # Load and play the previous song
#     pygame.mixer.music.load(previous_song_path)
#     pygame.mixer.music.play(loops=0, start=0.0)
#     isPlaying = True

# # Function to stop the song
# def stop_song():
#     global isPlaying

#     pygame.mixer.music.stop()
#     play_button.config(text="Pausar")
#     isPlaying = False
#     music_player_frame.grid_forget()
#     main_frame.grid(row=0, column=0)  # Show the music player frame 

# # Create the main window
# root = Tk()
# root.attributes('-fullscreen', False)  # Don't start in full-screen mode

# # Create a main frame
# main_frame = ttk.Frame(root, padding=10)
# main_frame.grid()

# # Title Label
# ttk.Label(main_frame, text="ROBÔ DANÇANTE").grid(column=3, row=3)

# # Button to choose the song
# choose_song_button = ttk.Button(main_frame, text="Escolher música", command=choose_song)
# choose_song_button.grid(column=3, row=4)

# # Button to toggle fullscreen
# full_screen_button = ttk.Button(main_frame, text="Tela cheia", command=toggle_full_screen)
# full_screen_button.grid(column=3, row=5)

# # Button to exit the program
# exit_button = ttk.Button(main_frame, text="Sair", command=root.destroy)
# exit_button.grid(column=3, row=6)

# # Create the music player frame (initially hidden)
# music_player_frame = ttk.Frame(root, padding=10)

# # Add a label for displaying the song name
# song_status = ttk.Label(music_player_frame)
# song_status.grid(column=1, row=0)

# song_label = ttk.Label(music_player_frame) # , font=("Arial", 18)
# song_label.grid(column=1, row=1)

# # Previous Music button
# next_button = ttk.Button(music_player_frame, text="Anterior", command=previous_song)
# next_button.grid(column=1, row=2)

# # Play/Pause button
# play_button = ttk.Button(music_player_frame, text="Pausar", command=play_pause_song)
# play_button.grid(column=1, row=3)

# # Next Music button
# next_button = ttk.Button(music_player_frame, text="Próxima", command=next_song)
# next_button.grid(column=1, row=4)

# # Stop button
# stop_button = ttk.Button(music_player_frame, text="Encerrar player", command=stop_song)
# stop_button.grid(column=1, row=5)

# # Button to toggle fullscreen (for the new frame)
# full_screen_button_music = ttk.Button(music_player_frame, text="Tela cheia", command=toggle_full_screen)
# full_screen_button_music.grid(column=1, row=6)

# # Button to exit the program from music player frame
# exit_button_music = ttk.Button(music_player_frame, text="Sair", command=root.destroy)
# exit_button_music.grid(column=1, row=7)
# update_time()
# # Run the Tkinter main loop
# root.mainloop()