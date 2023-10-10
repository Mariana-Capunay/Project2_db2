import nltk
from nltk.stem.snowball import SnowballStemmer
nltk.download('punkt')
class InvertedIndex:
    colection = []
    stopList = []

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

    def __init__(self):
        self.setStoplist("stoplist.txt")

    def setStoplist(self,nombre):
        stop_words = open(nombre, "r", encoding="latin1") 

        for i in stop_words:
            self.stopList.append(i.strip('\n')) #se agrega cada elemento quitando saltos de linea

        stop_words.close() #cierra archivo leido

        stoplist_extended = "'«[]¿?$.,»:;!,º«»()@¡😆“/#|*%'`"
        for caracter in stoplist_extended:
            self.stopList.append(caracter)
        #print(self.stopList)
    

    def preProcesar(self,texto):
        token = []

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



    