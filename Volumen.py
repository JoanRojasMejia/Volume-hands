#-----------------------Importacion de librerias ------------------------------------
import cv2
import SeguimientoManos as sm
import numpy as np
#--------------------- Importacion de librerias para controlar el volumen ---------------------------
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#------------------- Parametros de la camara ------------------
anchocam, altocam = 640, 480
#------------------- Lectura de la camara ------------------
cap = cv2.VideoCapture(0)
cap.set(3,anchocam)
cap.set(4,altocam)
#------------------- Creamos el objeto que almacena nustra clase ------------------
detector = sm.DetectorManos(maxManos = 1,confDeteccion = 0.6)

#----------------------------Control de audio del pc ----------------------
dispositivos = AudioUtilities.GetSpeakers()
interfaz = dispositivos.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volumen = cast(interfaz, POINTER(IAudioEndpointVolume))
RangoVol = volumen.GetVolumeRange()
#print(RangoVol)
volMin = RangoVol[0]
volMax = RangoVol[1]

while True:
    ret, frame = cap.read()
    frame = detector.encontrarManos(frame)
    lista, bbox = detector.encontrarPosicion(frame, dibujar=False)

    if len(lista) != 0:
        x1, y1 = lista[4][1], lista[4][2]
        x2, y2 = lista[8][1], lista[8][2]
        #---------- Vamos a comprobar que el dedo indice y el dedo pulgar esten arriba ---------
        dedos = detector.dedosarriba()

        #---------- Nos aseguramos que los dedos esten arriba ---------
        if dedos[0] == 1 and dedos[0] == 1:
            longitud, frame, linea = detector.distancia(4,8,frame, r=8, t=2)
            print(int(longitud))

            vol = np.interp(longitud, [25,200], [volMin, volMax])
            volumen.SetMasterVolumeLevel(vol,None)

            if longitud > 25:
                cv2.circle(frame, (linea[4], linea[5]), 10, (0,255,0), cv2.FILLED)
    
    cv2.imshow("Variador de Volumen", frame)
    t = cv2.waitKey(1)

    if t == 27:
        break

cap.release()
cv2.destroyAllWindows()

















