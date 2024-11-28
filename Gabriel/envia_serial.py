from serial import Serial

__all__ = ['enviar_serial', 'enviar_batida', 'enviar_hue', 'enviar_brightness']

arduino_serial = Serial("COM7", baudrate=9600)

def enviar_serial(texto):
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