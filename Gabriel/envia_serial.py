from serial import Serial

__all__ = ['enviar_serial', 'enviar_batida', 'enviar_hue', 'enviar_brightness', 'envia_pose']

# arduino_serial = Serial("COM7", baudrate=9600)

def enviar_serial(texto):
    return # só pra testar sem o arduino
    arduino_serial.write(texto.encode("UTF-8"))
    # texto_recebido = arduino_serial.readline().decode().strip()

def enviar_batida():
    enviar_serial("batida\n")
    print("batida")

def enviar_hue(hue):
    enviar_serial("hue %d\n"%hue)
    print("hue %d"%hue)

def enviar_brightness(brightness):
    enviar_serial("brightness %d\n"%brightness)
    print("brightness ", brightness)

def envia_pose(string):
    ''' 
    Função que envia a pose (string) para o Arduino.

    É necessário colocar 'Movimento ' antes de enviar o nome da pose,
    pois a função no Arduino foi definida de forma que precisa receber 
    um identificador de movimento para saber que se trata de um movimento.
    '''
    enviar_serial(f"{'Movimento ' + string}\n")
    print(f"{'Movimento ' + string}\n")
    return 

#OBS: Vamos ter que decidir como diferenciar movimentos de braços e pernas no Arduino, e alterar esta função depois