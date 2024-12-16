import serial

__all__ = ['envia_pose', 'envia_string', 'serial_monitora', 'enviar_hue', 'enviar_brightness', 'enviar_batida']


def envia_pose(arduino, pose_perna, pose_braco):
    ''' 
    Função que envia a pose (string) para o Arduino.

    É necessário indicar a pose de qual membro do corpo estamos enviando,
    pois a função no Arduino foi definida de forma que precisa receber 
    um identificador para saber se deve executar os movimentos das pernas ou braços.
    '''
    arduino.write(('Movimento ' + str(pose_perna) + " " + str(pose_braco) +"\n").encode("UTF-8") )  
    # print('Enviado pro arduino!')
    return 


def envia_string(arduino, string):
    '''
    Função que envia uma string qualquer ao Arduino.
    '''
    arduino.write((str(string) +"\n").encode("UTF-8") )  
    return


def serial_monitora(arduino):
  '''
  Função que monitora serial do Arduino, printando qualquer texto enviado do Arduino ao Python.
  '''
  while True:
    if arduino != None:
      texto_recebido = arduino.readline().decode().strip()
      if texto_recebido != "":
        print(texto_recebido)


def enviar_hue(arduino,hue):
    envia_string(arduino, "Hue %d\n"%hue)


def enviar_brightness(arduino, brightness):
    envia_string(arduino, "Brightness %d\n"%brightness)

def enviar_batida(arduino):
    envia_string(arduino, "Batida\n")
