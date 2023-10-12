import nltk
from nltk.stem.snowball import SnowballStemmer
nltk.download('punkt')

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
    colection = []
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
        
        tamaño_maximo_buffer = 4096  # Tamaño máximo del buffer en bytes
        cont = 0

        # Abrir el archivo en modo lectura
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            while True:
                buffer = []  # Lista para almacenar las líneas del buffer
                tamaño_buffer = 0  # Tamaño actual del buffer
                
                # Leer líneas del archivo y agregarlas al buffer hasta que el tamaño máximo se alcance
                for linea in archivo:
                    tamaño_linea = len(linea.encode("utf-8"))  # Tamaño de la línea en bytes
                    # Si la línea cabe en el buffer sin exceder el tamaño máximo
                    if tamaño_buffer + tamaño_linea <= tamaño_maximo_buffer:
                        buffer.append(linea.strip())  # Agrega la línea al buffer
                        tamaño_buffer += tamaño_linea  # Actualiza el tamaño del buffer
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
                print("Tamaño buffer: ",tamaño_buffer)
            print("Listo")
            print(cont)

    def preProcesar(self,texto): #recibe una fila y genera diccionario (pos_row, suma(tf_por_campo*peso_campo))

        # 1. tokenizar
        tokens = nltk.word_tokenize(texto.lower())

        print("Tokens:",tokens)

        # 3. sacar el lexema
        stemmer = SnowballStemmer('spanish')
        token_lexem = {}

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

                # agregamos correctamente el contador en el diccionario
                if lexema in token_lexem:
                    token_lexem[lexema] += 1 #ya apareció antes
                else:
                    token_lexem[lexema] = 1 #aparece por primera vez

        print("Lexemas+tf: ",token_lexem)
        
        return token_lexem #retorna diccionario de lexemas con su tf
    

        
    def spimiInvert(self,token_stream):
        output_file = "txt"
        
        while True:
            token = token_stream



    