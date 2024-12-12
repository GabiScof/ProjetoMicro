import cv2
import mediapipe as mp
from datetime import datetime 
from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
import pygame
import os
import json
import threading
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
import serial
import time
import sys
from serial import Serial 


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.dispositivos.comunica_arduino import envia_pose, envia_string, serial_monitora
from src.config.poses import dicionario_poses, dicionario_poses_pernas
from src.deteccao_poses.exibicao import calcula_angulo,funcao_texto
from src.utils.distancia import distancia


'''
=========================================================
                Inicialização do Arduino
=========================================================
'''

try:
    arduino = serial.Serial("COM8", baudrate=9600, timeout=0.4) #Alterar porta de acordo com dispositivo
    time.sleep(2)
    print("Conexão estabelecida com o Arduino.")
except Exception as e:
    print(f"Erro ao conectar com o Arduino: {e}")
    exit()


'''
=========================================================
Definições de variáveis globais e setup inicial de música
=========================================================
'''

isPlaying = False
pygame.mixer.init()
folder_path = 'data\musica\lista_musicas'
all_files = os.listdir(folder_path)
playlist = [file[:-4] for file in all_files]
current_song_index = 0

with open("data\musica\data.json", "r", encoding='utf-8') as file: 
    songs_json = json.load(file)

current_song_info = {}
current_time_s = 0
states_count = 0
current_state_time = 0
hue_brightness_index = 0
beats_index = 0
beat_anterior = 0

'''
=========================================================
            Definições de funções de músicas
=========================================================
'''

def toggle_full_screen():
    '''
    Função que faz alterar para tela cheia.
    '''
    is_fullscreen = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not is_fullscreen)


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
    
    song_path = filedialog.askopenfilename(
        initialdir="data\musica\lista_musicas",  
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

        main_frame.grid_forget()  
        music_player_frame.grid(row=0, column=0)  

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=0, start=0.0)


def update_time():
    '''
    Função que acompanha o tempo da música e atualiza suas variáveis.

    Essencial para o envio da batida.
    '''
    global current_time_s
    global states_count
    global hue_brightness_index
    global beats_index
    global isPlaying

    if isPlaying:
        try:
            current_time_s = pygame.mixer.music.get_pos() / 1000

            if current_time_s >= states_count * current_state_time and current_time_s <= current_song_info["total_time_length"]:
                states_count += 1 
                hue_brightness_index += 1

            elif current_time_s >= current_song_info["beats"][beats_index]:
                # envia_string(arduino, "Batida") #BACALHAU
                beats_index += 1

        except:
            isPlaying = False

    root.after(1, update_time)


def play_pause_song():
    '''
    Função para iniciar música e pausar.
    '''
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
    '''
    Função para passar para a próxima música.
    '''
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
    '''
    Função para voltar para a música anterior.
    '''
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
    '''
    Função para parar música.
    '''
    global isPlaying

    pygame.mixer.music.stop()
    play_button.config(text="Pausar")
    isPlaying = False
    music_player_frame.grid_forget()
    main_frame.grid(row=0, column=0)  


'''
=========================================================
            Chamada de funções de música
=========================================================
'''

# Cria a janela principal
root = tk.Tk()
root.attributes('-fullscreen', False)

# Cria o frame principal
main_frame = ttk.Frame(root, padding=10)
main_frame.grid()

# Rótulo de título
ttk.Label(main_frame, text="ROBÔ DANÇANTE").grid(column=3, row=3)

# Botão para escolher a música
choose_song_button = ttk.Button(main_frame, text="Escolher música", command=choose_song)
choose_song_button.grid(column=3, row=4)

# Botão para alternar para tela cheia
full_screen_button = ttk.Button(main_frame, text="Tela cheia", command=toggle_full_screen)
full_screen_button.grid(column=3, row=5)

# Botão para sair do programa
exit_button = ttk.Button(main_frame, text="Sair", command=root.destroy)
exit_button.grid(column=3, row=6)

# Cria o frame do player de música (inicialmente oculto)
music_player_frame = ttk.Frame(root, padding=10)

song_status = ttk.Label(music_player_frame)
song_status.grid(column=1, row=0)

song_label = ttk.Label(music_player_frame)  
song_label.grid(column=1, row=1)

next_button = ttk.Button(music_player_frame, text="Anterior", command=previous_song)
next_button.grid(column=1, row=2)

play_button = ttk.Button(music_player_frame, text="Pausar", command=play_pause_song)
play_button.grid(column=1, row=3)

next_button = ttk.Button(music_player_frame, text="Próxima", command=next_song)
next_button.grid(column=1, row=4)

stop_button = ttk.Button(music_player_frame, text="Encerrar player", command=stop_song)
stop_button.grid(column=1, row=5)

full_screen_button_music = ttk.Button(music_player_frame, text="Tela cheia", command=toggle_full_screen)
full_screen_button_music.grid(column=1, row=6)

exit_button_music = ttk.Button(music_player_frame, text="Sair", command=root.destroy)
exit_button_music.grid(column=1, row=7)


'''
=========================================================
       Definições de variáveis globais da interface
=========================================================
'''

pose_atual_braco = None
pose_atual_perna = None
pose_anterior_braco = "Nada"
pose_anterior_perna = "Nada"


ultimo_tempo_deteccao = time.time()
ultimo_tempo_deteccao_perna = time.time()

contador = 0 
contador_perna = 0

impressa = False
impressa_perna = False




'''
=========================================================
        Chamada de funções de detecção de poses
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

            global pose_anterior_braco
            global pose_anterior_perna

            global ultimo_tempo_deteccao
            global ultimo_tempo_deteccao_perna

            global contador
            global contador_perna

            global impressa
            global impressa_perna

            global beats_index
            global beat_anterior

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

            #detecado = False

            if distancia(ombroDX,maoDX,ombroDY,maoDY) <60 and distancia(ombroEX,maoEX,ombroEY,maoEY) <60 and distancia(ombroDX,cotoveloDX,ombroDY,cotoveloDY) <60 and distancia(ombroEX,cotoveloEX,ombroEY,cotoveloEY) <60:
                cor = (255, 105, 180)
                texto = 'ambos_frente'
                coord1 = 10
                coord2 = 300
                pose_atual_braco = texto
                funcao_texto(texto, cor, frame, coord1, coord2)

            elif distancia(ombroDX,maoDX,ombroDY,maoDY) <60 and distancia(ombroDX,cotoveloDX,ombroDY,cotoveloDY) <60:
                            cor = (255, 105, 180)
                            texto = 'direita_frente'
                            coord1 = 10
                            coord2 = 300
                            pose_atual_braco = texto
                            funcao_texto(texto, cor, frame, coord1, coord2)

            elif distancia(ombroEX,maoEX,ombroEY,maoEY) <60 and distancia(ombroEX,cotoveloEX,ombroEY,cotoveloEY) <60:
                            cor = (255, 105, 180)
                            texto = 'esquerda_frente'
                            coord1 = 10
                            coord2 = 300
                            pose_atual_braco = texto
                            funcao_texto(texto, cor, frame, coord1, coord2)

            else:                
                for movimento, angulos in dicionario_poses.items():
                    if angulos["condicao"](anguloBEC, anguloBEB, anguloBDC, anguloBDB):
                        #detecado = True
                        cor = (255, 105, 180)
                        texto = movimento
                        coord1 = 10
                        coord2 = 300
                        pose_atual_braco = texto
                        funcao_texto(texto, cor, frame, coord1, coord2)
                        

            #         # Utilização de um contador para ver se a pose está sendo efeituada há um tempo
            #         if pose_atual_braco == pose_anterior_braco:
            #             contador +=1

            #         # Verifica que a pose está há um tempo (contador) e que ainda não foi impressa
            #         if contador > 6 and not impressa:
            #             impressa = True # Indica que já foi impressa
            #             print('MEXEU BRACO: '+ 'Movimento ' + str(pose_atual_perna) + " " + str(pose_atual_braco)) # Descomentar caso queira ver no terminal, invés de ver no Arduino.
            #             # envia_pose(arduino, pose_atual_perna, pose_atual_braco) # BACALHAU

            #         # Verifica que a pose atual é diferente da pose anterior
            #         if pose_atual_braco != pose_anterior_braco:
            #             contador = 0 # Reseta contador
            #             impressa = False # Indica que ainda não foi impressa (já que é pose nova)
            #             pose_anterior_braco = pose_atual_braco # Atualiza a pose anterior
            #             ultimo_tempo_deteccao = time.time() # Salva tempo de troca de pose
            #         break

            # if not detecado: # Verifica que nenhuma pose foi detectada
            #     if (time.time() - ultimo_tempo_deteccao > 3) and pose_atual_braco != 'Nada': # Verifica que a pose atual já não era 'Nada' (pois queremos imprimir só 1 vez)
            #         pose_atual_braco = 'Nada'
            #         print('MEXEU BRACO: '+ 'Movimento ' + str(pose_atual_perna) + " " + str(pose_atual_braco))  # Apenas imprime "Nada" após 3 segundos de inatividade
            #         # envia_pose(arduino, pose_atual_perna, pose_atual_braco) # BACALHAU

       
            #-----------------------------------------------------------------------------------------------------------------------------------
            
            # Percorrer o dicionário e ver se a pessoa está fazendo uma das poses das PERNAS
            # print(distancia(ombroDX,maoDX,ombroDY,maoDY))

            #detecado_perna = False
            



            for movimento, angulos in dicionario_poses_pernas.items():
                if angulos["condicao"](anguloPEC, anguloPDC):
                    #detecado_perna = True
                    cor = (255, 105, 180)
                    texto = movimento
                    coord1 = 10
                    coord2 = 250
                    pose_atual_perna = movimento
                    funcao_texto(texto, cor, frame, coord1, coord2)
                

            # if anguloPDC >=10  or anguloPEC>=10:
            #     cor = (255, 105, 180)
            #     texto = "dobrado"
            #     coord1 = 10
            #     coord2 = 250
            #     pose_atual_perna = movimento
            #     funcao_texto(texto, cor, frame, coord1, coord2)

            # if anguloPDC <=10  and anguloPEC<=10:
            #     cor = (255, 105, 180)
            #     texto = "retas"
            #     coord1 = 10
            #     coord2 = 250
            #     pose_atual_perna = movimento
            #     funcao_texto(texto, cor, frame, coord1, coord2)

            

            if beats_index > beat_anterior:
                print('Movimento ' + str(pose_atual_perna) + " " + str(pose_atual_braco))
                envia_pose(arduino, pose_atual_perna, pose_atual_braco) # BACALHAU

            #         # Utilização de um contador para ver se a pose está sendo efeituada há um tempo
            #         if pose_atual_perna == pose_anterior_perna:
            #             contador_perna +=1

            #         # Verifica que a pose está há um tempo (contador_perna) e que ainda não foi impressa
            #         if contador_perna > 10 and not impressa_perna:
            #             impressa_perna = True # Indica que já foi impressa
            #             print('MEXEU PERNA: '+ 'Movimento ' + str(pose_atual_perna) + " " + str(pose_atual_braco)) # Descomentar caso queira ver no terminal, invés de ver no Arduino.
            #             # envia_pose(arduino, pose_atual_perna, pose_atual_braco) # BACALHAU


            #         # Verifica que a pose atual é diferente da pose anterior
            #         if pose_atual_perna != pose_anterior_perna:
            #             contador_perna = 0 # Reseta contador_perna
            #             impressa_perna = False # Indica que ainda não foi impressa (já que é pose nova)
            #             pose_anterior_perna = pose_atual_perna # Atualiza a pose anterior
            #             ultimo_tempo_deteccao_perna = time.time() # Salva tempo de troca de pose
            #         break

            # if not detecado_perna: # Verifica que nenhuma pose foi detectada
            #     if (time.time() - ultimo_tempo_deteccao_perna > 3) and pose_atual_perna != 'Nada': # Verifica que a pose atual já não era 'Nada' (pois queremos imprimir só 1 vez)
            #         pose_atual_perna = 'Nada'
            #         print('MEXEU PERNA: '+ 'Movimento ' + str(pose_atual_perna) + " " + str(pose_atual_braco))  # Apenas imprime "Nada" após 3 segundos de inatividade
            #         # envia_pose(arduino, pose_atual_perna, pose_atual_braco) # BACALHAU

            beat_anterior = beats_index

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


'''
=========================================================
          Inicialização e Execução do Sistema
=========================================================
'''

thread = threading.Thread(target=start_video_processing, daemon=True)
thread.start()
thread2 = threading.Thread(target=serial_monitora, args=[arduino], daemon=True)
thread2.start()

update_time() 
root.mainloop() 