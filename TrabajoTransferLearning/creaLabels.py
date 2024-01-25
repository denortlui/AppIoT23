import os

lista_nombres = []

#Leemos todos los nombres
for dirpath, dirnames, filenames in os.walk("./dataset"):
    for filename in filenames:
        if filename.endswith('.png'):
            #name = filename.split(' ', 1)[0]
            name = filename.rsplit(' ', 1)[0]
            #name = name.split(' ', 1)[1]
            if name not in lista_nombres:
                print(name)
                lista_nombres.append(name)

#Escribimos en un fichero todo
with open('labels_lego.txt', 'w') as file:
    for item in lista_nombres:
        file.write(item.split(' ', 1)[1]+"\n")
    file.close()
