from email.encoders import encode_base64
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
import smtplib
import sys

'''     LIBRERIAS CAMARA '''
import time
import imutils
import cv2
import tkinter
import numpy as np
from threading import Thread

'''     LIBRERIAS CORREO ALERTA    '''

#######################################################################
# INICIO LA CAPTURA DE VIDEO INDICANDO MI WEBCAM (0) - TAMAÑO
#######################################################################
captura = cv2.VideoCapture(0)
captura.set(3, 640)  # Ancho de pantalla
captura.set(4, 480)  # Alto de pantalla

#######################################################################
# CREO UN BOTÓN TEMPORAL PARA PARA ACTIVA LA APLICACION
#######################################################################

mode = 0

def init():
    Thread(target=mt).start()
    top = tkinter.Tk()
    B = tkinter.Button(top, text="Iniciar Detector", command=IniciaAplicacion)
    B.pack()
    C = tkinter.Button(top, text="Terminar Aplicación", command=TerminarAplicacion)
    C.pack()
    top.mainloop()

def IniciaAplicacion():
    global mode
    mode = 1


def TerminarAplicacion():
    global mode
    mode = 2



def mt():
    con = 0
    global mode

    e, f_start = captura.read()
    f_start = imutils.resize(f_start, width=500)
    gray = cv2.cvtColor(f_start, cv2.COLOR_BGR2GRAY)
    f_start = cv2.GaussianBlur(gray, (21, 21), 0)

    while True:
        ret, frame = captura.read()
        frame = imutils.resize(frame, width=500)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        frameDelta = cv2.absdiff(gray, f_start)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        f_start = gray

        if(thresh.sum()>100):
            con+=1
        else:
            if(con>0):
                con-=1
            
        cv2.imshow('vi',thresh)
       
        if(con>20):
            print("Alerando al Usuario")
            mode =0
            con = 0
            AlertaEmail()
            cv2.destroyWindow('vi')

        else:
            pass

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # press 'ESC' to quit
            break

    captura.release()
    cv2.destroyAllWindows()


#######################################################################
# ENVIAR UN EMAIL AL DETECTAR UN MOVIMIENTO
#######################################################################
def AlertaEmail():
    msg = MIMEMultipart()
    message = "ESTAN MATANDO UN HUEON!!! " + time.strftime("%c")
    password = "Dp505sns$"
    msg['From'] = "cat.rguzmanr@gmail.com"
    msg['To'] = "rguzman@outlook.com"
    msg['Subject'] = "Alarma Alarma"
    msg.attach(MIMEText(message, 'plain'))

    # Adjuntamos la imagen
    file = open("alerta.jpg", "rb")
    foto = MIMEImage(file.read())
    foto.add_header('Content-Disposition',
                    'attachment; filename = "alerta.jpg"')
    msg.attach(foto)

    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print("Mensaje enviado correctamente %s:" % (msg['To']))


init()

