import nltk
from nltk.stem.snowball import SnowballStemmer
nltk.download('punkt')

tamaño_maximo_buffer = 4096  # Tamaño máximo del buffer en bytes

"""
    Pasos:
        1. Preprocesar los documentos
        2. Contabilizar term_frecuency y doc_id (posting list)
        3. Pasar datos a memoria secundaria
"""

"""
    Cuando llega una query:
        1. Se preprocesa 
        2. Se genera una lista de terminos = indice_invertido + terminos de query
        3. Se genera un espacio vectorial con longitud fija (longitud=lista de terminos)
        4. Se genera un vector para cada fila y la query
        5. Se calcula coseno entre (vector_por_fila, vector_query)
        6. Se ordenan los resultados (orden descendente)
        7. Se retornan los k más relacionados
"""

class InvertedIndex:
    colection_header = []
    pesos = [0,1,1,1,1,1,1,1,1,1] # para guardar pesos de cada campo
    stopList = []

    def __init__(self):
        self.setStoplist("stoplist.txt") #definimos StopList
        
        ruta_archivo = r"C:\Users\ASUS\Downloads\prueba\styles.csv" # Ruta del archivo CSV
        self.preProcessCSV(ruta_archivo) #preprocesamos cada buffer del CSV

    def setStoplist(self,nombre):
        stop_words = open(nombre, "r", encoding="latin1") 

        for i in stop_words:
            self.stopList.append(i.strip('\n')) #se agrega cada elemento quitando saltos de linea

        stop_words.close() #cierra archivo leido

        stoplist_extended = "'«[]¿?$.,»:;!,º«»()@¡😆“/#|*%'`"
        for caracter in stoplist_extended:
            self.stopList.append(caracter)
        #print(self.stopList)
    
    def preProcessCSV(self,ruta_archivo):
        cont = 0
        pos_row = 0

        # Abrir el archivo en modo lectura
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:

            """ENCABEZADO"""
            encabezado_text = archivo.readline()
            pos_row += len(encabezado_text.encode("utf-8"))  # Tamaño de la línea en bytes
            pos_row += 1 #para contar donde inicia fila que sigue

            self.colection_header = encabezado_text.strip().split(',')
            #print('Encabezados del CSV:', self.colection_header)
            
            #print(pos_row)

            # modificar para leer todo el csv (ahora solo lee una pagina o buffer)
            #while
            pos_row = self.getBufferIndex(pos_row,archivo)
            """
                for c in campos:
                    print(c,end='-')
                print("\n")
            """
                    

    """
                # Leer líneas del archivo y agregarlas al buffer hasta que el tamaño máximo se alcance
                for linea in archivo:
                    tamaño_linea = len(linea.encode("utf-8"))  # Tamaño de la línea en bytes
                    
                    if tamaño_buffer + tamaño_linea <= tamaño_maximo_buffer: # Si la línea cabe en el buffer sin exceder el tamaño máximo
                        #buffer.append(linea.strip())  # Agrega la línea al buffer
                        self.preProcessandIndex(linea) #preProcesa la linea y retorna un indice invertido
                        tamaño_buffer += tamaño_linea  # Actualiza el tamaño del buffer
                        if cont==0:
                            print(linea.strip(), end='-;-')
                            print(tamaño_linea,end='\n')
                    else:
                        break  # Si excede el tamaño máximo, detén la lectura del buffer
                

                # Pausa el programa por 3 segundos antes de leer el siguiente buffer
                # preprocesar el buffer(linea por linea y enviar tokens a la funcion preProcesar)
                
                cont+=1
                # Si el archivo ha llegado al final, sal del bucle
                if not buffer or tamaño_buffer==0:
                    break

                # Procesar el buffer (hacer lo que necesites con las líneas leídas)
                #print("Nuevo buffer:\n\n", "\n".join(buffer))  # En este ejemplo, simplemente imprime el buffer
                #print("Tamaño buffer: ",tamaño_buffer)
            print("Listo")
            print(cont)
    """

    def getBufferIndex(self,pos_inicio,archivo):
        archivo.seek(pos_inicio)
        buffer = archivo.read(tamaño_maximo_buffer) #leemos un buffer desde el csv
        ind_actual = 0
        indice_local = {} #para indice invertido local

        #print(len(buffer))

        #encontramos primer salto de linea y lo definimos como el límite
        i = len(buffer)-1
        while buffer[i]!='\n':
            i -= 1
        #print(i)
        #print(buffer)
        
        #se lee una cantidad entera de lineas
        while ind_actual<i-1: #obtendremos cada linea 
            cont_comas = 0
            campos = [] 
            
            while cont_comas<8:
                campo = ""

                #recorremos cada campo
                while buffer[ind_actual]!=',':  
                    if buffer[ind_actual]!='\n':
                        campo += buffer[ind_actual]
                    ind_actual += 1

                cont_comas += 1 #aumentamos la cantidad de comas
                ind_actual += 1
                campos.append(campo)    #añadimos el campo

            campo = ""

            while buffer[ind_actual]!='\n':    
                campo += buffer[ind_actual]
                ind_actual += 1

            campos.append(campo)

            for campo in campos:
                print(campo,end= ' - ')
            print('\n')

            ind_actual += 1
            
            
            #preProcesa cada linea
            self.preProcessListandIndex(list_campos=campos,dicc_lexemas=indice_local)

        indice_local = dict(sorted(indice_local.items())) #ordena indice local 

        #enviar indice a un archivo .json
    
        #print("indice local: ",indice_local)
        return pos_inicio
        

    def preProcessListandIndex(self,list_campos,dicc_lexemas):
        #los campos se encuentran separados en una lista
        print(list_campos)
        #dicc_lexemas = {} #se imprime solo para verificar correctitud del indice invertido por linea
        for i,campo in enumerate(list_campos):
            self.preProcessandIndex(texto=campo,dicc_lexemas=dicc_lexemas,peso=self.pesos[i])
            #print("Lexemas+tf: ",dicc_lexemas) #verificacion del indice invertido por linea
        

        
    def preProcessandIndex(self,texto,dicc_lexemas,peso=1): #recibe una fila y genera diccionario (pos_row, suma(tf_por_campo*peso_campo))
        # 1. tokenizar
        tokens = nltk.word_tokenize(texto.lower())

        #print("Tokens:",tokens)

        # 3. sacar el lexema
        stemmer = SnowballStemmer('spanish')
        #dicc_lexemas = {}

        # 2. obtener stoplist y eliminarlo
        """  # Primera idea de implementacion
        for i in range (len(tokens)-1,-1,-1):
            
            if tokens[i] in self.stopList:
            tokens.pop(i)
            else:
                token_lexem.append()
        """

        # 2da idea de implementacion
        for i in range (len(tokens)):
            if tokens[i] not in self.stopList:
                lexema = stemmer.stem(tokens[i]) #obtenemos el lexema
                if peso!=0: #solo se debe añadir si su peso realmente influye
                    # agregamos correctamente el contador en el diccionario
                    if lexema in dicc_lexemas:
                        dicc_lexemas[lexema] += peso #ya apareció antes
                    else:
                        dicc_lexemas[lexema] = peso #aparece por primera vez

        
        #return dicc_lexemas #retorna diccionario de lexemas con su tf
    

        
    def spimiInvert(self,token_stream):
        output_file = "txt"
        
        while True:
            token = token_stream



    