import json 

path_local_index = r"C:\Users\ASUS\OneDrive - UNIVERSIDAD DE INGENIERIA Y TECNOLOGIA\Escritorio\bd2_proyecto_2023.2\proyecto_2\Project2_db2\InvertedIndex\Local_Index\Merge128"


def find_word(word:str,limit = 10000):
    # Retorna el diccionario de la palabra si es que existe, si no, retorna un diccionario vacio
    ini = 0
    fin = limit
    while 1:
        mid = int((ini + fin)/2)
        ruta_indice_local = path_local_index+"\index"+str(mid+1).zfill(2)+".json"
        try:
            file = open(ruta_indice_local,"r")
            data = json.load(file)
            list_data = list(data)
            first_word = list_data[0]
            last_word = list_data[-1]
            if first_word <= word and word <= last_word:
                if word in data.keys():
                    return data[word]
                else:
                    return {}
            elif word < first_word: 
                fin = mid-1
            else:
                ini = mid+1
        except:
            ini = mid-1
    return {}