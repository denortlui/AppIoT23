#%% RED NEURONAL

#%%  Etiquetas de las actividades

column_names = ["acel_x", "acel_y", "acel_z", "gyro_x","gyro_y","gyro_z","solo","nivel","user_id"]

LABELS = ["Shostakovich", "Requiem", "Gazza Ladra","Berlioz", "Saint-saens", "Pulcinella"]
DIR_DATOS = "."
N_FEATURES = 3

# El número de pasos dentro de un segmento de tiempo (20Hz).
TIME_PERIODS = 100

# Los pasos a dar de un segmento al siguiente; si este valor es igual a
# TIME_PERIODS, entonces no hay solapamiento entre los segmentos
STEP_DISTANCE = 1


import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Conv1D, MaxPooling1D, GlobalAveragePooling1D, Flatten, AveragePooling1D
from keras.layers import SimpleRNN

model_m = Sequential()
model_m.add(Conv1D(100, 5, activation='relu', input_shape=(TIME_PERIODS,
                                                            3)))
model_m.add(Conv1D(100, 5, activation='relu'))
model_m.add(MaxPooling1D(3))
model_m.add(Conv1D(10, 3, activation='relu'))
model_m.add(Conv1D(10, 3, activation='relu'))
model_m.add(MaxPooling1D(3))
model_m.add(GlobalAveragePooling1D())
model_m.add(Dropout(0.2))
model_m.add(Dense(6, activation='softmax'))

print(model_m.summary())

##Cargamos los pesos

model_m.load_weights("bm_6124_1526.h5")

#%% Cargamos los datos y probamos
import pandas as pd
import numpy as np
solo = 1
#Cargamos los datos de entrada
df = pd.read_csv(f"{DIR_DATOS}/datosTestSolo{solo}.csv", header=1, names=column_names).head(900)
if solo == 1 or solo == 3 or solo == 4:
            print("Detected low sampled input: resampling....")
            index = pd.date_range('1/1/2000', periods=df.shape[0], freq='T')
            res = df.set_index(index)
            output = res.resample('30S').ffill()
            df = output.reset_index()[column_names]

#Normalizamos los datos
df["gyro_x"] = (df["gyro_x"] - min(df["gyro_x"].values)) / (max(df["gyro_x"].values) - min(df["gyro_x"].values))
df["gyro_y"] = (df["gyro_y"] - min(df["gyro_y"].values)) / (max(df["gyro_y"].values) - min(df["gyro_y"].values))
df["gyro_z"] = (df["gyro_z"] - min(df["gyro_z"].values)) / (max(df["gyro_z"].values) - min(df["gyro_z"].values))

segment = []

for i in range(0, len(df) - 100, 1):
    gxs = df['gyro_x'].values[i: i+100]
    gys = df['gyro_y'].values[i: i+100]
    gzs = df['gyro_z'].values[i: i+100]

    segment.append([gxs, gys, gzs])



#Representamos los datos que introducimos a la red
import matplotlib.pyplot as plt

plt.figure()
plt.plot(df['gyro_x'].values[:])
plt.plot(df['gyro_y'].values[:])
plt.plot(df['gyro_z'].values[:])
plt.show()

#segment = [gxs, gys, gzs]
#
datos_input = np.asarray(segment, dtype=np.float32).reshape(-1, TIME_PERIODS, N_FEATURES)
prediccion = model_m.predict(datos_input)
#prediccion= model_m(datos_input, training=False)
#
solo_estimado = np.argmax(prediccion, axis=1)
histograma = []

for i in range(len(LABELS)):
    histograma.append(np.count_nonzero(solo_estimado==i))


plt.figure()
plt.bar(LABELS, histograma)
#print("Solo estimado: ")
#for i in range(len(prediccion[0])):
#    if prediccion[0][i] == max(prediccion[0]):
#        aux = " <-------------------------------"
#    else:
#        aux = ""
#    print(f"  -{LABELS[i]}: {str(prediccion[0][i])}" + aux)
# %%
