import numpy as np
import time
import statistics as stats
import os.path
from time import sleep
from sense_hat import SenseHat
#import keyboard
import threading

teclaPulsada = ''

#Para que se pueda detectar input de teclado
def callback(event):
    global teclaPulsada
    while (teclaPulsada != 'q'): 
        teclaPulsada = input("Pulse 'q' para parar:")
    print("Tecla 'q' pulsada!")
    

#Funcion que crea 2 csv, uno que engloba todo y otro por cada solo y persona
def createAndAppend(datosIMU):
    print("Almacenando datos...")
    userID = int(datosIMU[0][8])
    solo = int(datosIMU[0][6])
    tipo_archivo = ".csv"

    #Creando archivo independiente
    archivo = f"datos_{solo}_{userID}"
    intentos=0
    while(os.path.isfile(archivo+tipo_archivo)):
        #En caso de que exista un fichero con dicho nombre, le pone un numero al final (consecutivo)
        print("El archivo",archivo,"ya existe")
        intentos+=1
        if(intentos>1):
            archivo=archivo[:-1]
        archivo=archivo+"("+str(intentos)+")"
    np.savetxt(f"{archivo}{tipo_archivo}",datosIMU, header="acel_x,acel_y,acel_z,gyro_x,gyro_y,gyro_z,solo,nivel,user_id",delimiter=',',fmt='%.6f', comments='')

    #Hacemos un append al final
    archivo = "datos_globales"
    if(not os.path.isfile(archivo+tipo_archivo)):
        np.savetxt(f"{archivo}{tipo_archivo}",datosIMU, header="acel_x,acel_y,acel_z,gyro_x,gyro_y,gyro_z,solo,nivel,user_id",delimiter=',',fmt='%.6f', comments='')
    else:
        with open(archivo+tipo_archivo, "ab") as f:
            #f.write(b"\n")
            np.savetxt(f,datosIMU,delimiter=',',fmt='%.6f')

    print("Datos almacenados correctamente")



#Interfaz de usuario en pantalla
O = [50,98,168]
X = [255,255,255]

PLAY = [
  O, O, X, O, O, O, O, O,
  O, O, X, X, O, O, O, O,
  O, O, X, X, X, O, O, O,
  O, O, X, X, X, X, O, O,
  O, O, X, X, X, X, O, O,
  O, O, X, X, X, O, O, O,
  O, O, X, X, O, O, O, O,
  O, O, X, O, O, O, O, O,
  ]


T_CUENTA_ATRAS = 1#s
F_MUESTREO = 20#Hz
#Se crea el objeto sense y se inician todas las variables
sense=SenseHat()

t = 0
t_sample=[]

t_ini=time.time()
t_ant=t_ini
accel_x, accel_y, accel_z = [], [], []
gyros_x, gyros_y, gyros_z = [], [], []
T_m = 1.0/ F_MUESTREO
cuentra_atras = T_CUENTA_ATRAS
#Formato de los datos de salida:
#Medidas sensores, ts, solo, nivel, id_user
userID = 0 #Uno distinto por musico
solo = 0 
lista_solos = ["Shostakovich", "Requiem", "Gazza Ladra","Berlioz", "Saint-saens", "Pulcinella"]# 0 Shostakovich, 1 Requiem, 2 Gazza Ladra, 3 Berlioz, 4 Saint-saens, 5 Pulcinella
nivel = 0 # Del 1 al 5

archivo="datos" # nombre del archivo
tipo_archivo=".csv" # extensión 

#keyboard.add_hotkey('q', lambda: callback('q'))

while(1):
    #Se pregunta por los datos de entrada
    res = input("Pulsa enter para comenzar una prueba nueva o 'q' para salir...")
    if res == 'q':
        break

    datos_incorrectos = True
    while(datos_incorrectos):
        print("Introduzca los datos de la prueba")
        print("Lista de solos: ")
        for i in range(len(lista_solos)):
            print(f"   {i+1} - {lista_solos[i]}")

        try:
            solo = int(input("Solo: "))
            userID = int(input("Usuario: "))
            print(solo)
            print(userID)
        except:
            solo = 0
            userID = 0
        #Se comprueba la entrada
        if solo not in range(1, len(lista_solos)+1) or userID>99:
            print("Datos introducidos erroneos.")
        else:
            print("Datos de la prueba:")
            print(f"   userID: {userID}")
            print(f"   Solo: {lista_solos[solo-1]}")
            print("")
            while(1):
                res = input("¿Continuar con la ejecución? (s/n): ")
                if(res == 'S' or res == 'N' or res == 's' or res == 'n'):
                    if res == 'S' or res == 's':
                        datos_incorrectos = False
                    break


    #Espero untiempo antes de empezar
    t_ini = time.time()
    cuentra_atras = T_CUENTA_ATRAS
    while (cuentra_atras>0):
        print(f"Comenzando recogida de datos en {cuentra_atras}")
        sleep(1)
        cuentra_atras -= 1

    #Comenzamos hilo para detectar pausa
    teclaPulsada = ''
    hilo = threading.Thread(target=callback, args=("a",))

    #bucle for para tomar los datos
    print("Pulse q o el joystick para terminar la recogida de datos")
    print("Grabando...")
    sense.set_pixels(PLAY)
    escuchando = True
    t_ini = time.time()
    t = 0
    teclaPulsada = ''
    hilo.start()
    while(escuchando):
        accel_x, accel_y, accel_z = [], [], []
        gyros_x, gyros_y, gyros_z = [], [], []

        t_actual = time.time()
        t_ant = t_actual
        acceleration = sense.get_accelerometer_raw()
        #acceleration = {'x': 1.0, 'y': 2.0, 'z': 3.0}
        #datos de aceleración en Gs
        accel_x.append(acceleration['x'])
        accel_y.append(acceleration['y'])
        accel_z.append(acceleration['z'])
        gyroscope = sense.get_gyroscope_raw()
        #gyroscope = {'x': 1.0, 'y': 2.0, 'z': 3.0}
        #datos de velocidad rad/s
        gyros_x.append(gyroscope['x'])
        gyros_y.append(gyroscope['y'])
        gyros_z.append(gyroscope['z'])
        
        t = t_actual - t_ini

        #Si se ha pulsado el botón de parar, salgo del bucle
        #Tanto si se pulsa el boton del bucle
        events = sense.stick.get_events()
        for event in events:
            if event.direction == "middle":
                escuchando = False
                break

        #Como si se pulsa la barra espaciadora
        if teclaPulsada == 'q':
            escuchando = False

        #Espero a que me toce muestrear
        deltaTime = 0.0
        while (deltaTime<T_m):
            t_actual = time.time()
            deltaTime = t_actual-t_ant

    # fin de la toma de muestras
    sense.clear()

    print("")
    print(f"Tiempo de grabacion: {str(round(t, 2))}s")
    print("Frecuencai muestreo: ",int(1/float(format(deltaTime,"f")))," Hz")
    input("Pulsa intro para continuar...")
    nivel = 0
    while(nivel == 0):
        try:
            nivel = int(input("Nivel (1-5): "))
        except:
            nivel = 0

        if nivel not in range(1, 6):
            nivel = 0
        

    #Creo los datos que se introduciran en el csv
    nivel_data = [ round(nivel, 1) for i in range(len(accel_x))]
    solo_data = [ round(solo, 1) for i in range(len(accel_x))]
    userID_data = [ round(userID, 1) for i in range(len(accel_x))]
    
    #Paso los datos al csv
    #Medidas sensores, ts, solo, nivel, id_user
    datosIMU=np.rot90(np.array([accel_x,accel_y,accel_z,gyros_x,gyros_y,gyros_z, solo_data, nivel_data, userID_data]))

    #Se almacenan los datos de los sensores
    createAndAppend(datosIMU)