import pandas as pd
import numpy as np
import nltk 

# Ejemplo de texto de entrada
data = pd.DataFrame({'Documentos': ['Doc1', 'Doc2', 'Doc3', 'Doc4'],
                    'Texto': ['Este es un ejemplo de documento.', 
                                'Un segundo ejemplo de documento.', 
                                'Un tercer ejemplo de documento.', 
                                'Un último ejemplo de documento.']})

collection = data['Texto'].str.split()  # Divide el texto en palabras

# Definir la clase InvertedIndex
class InvertedIndex:
    def __init__(self):
        self.index = dict()
        self.length = dict()

    def add(self, document):
        # Agregar un documento a la colección
        doc_id = len(self.length)
        self.length[doc_id] = 0

        # Incrementar el contador de palabras en el documento y agregar el documento a la lista de documentos
        for token in document:
            if token not in self.index:
                self.index[token] = list()
            self.index[token].append(doc_id)
            self.length[doc_id] += 1

    def lookup(self, word):
        # Buscar un término en el índice
        if word in self.index:
            return self.index[word]
        else:
            return []

    def compute_tfidf(self, data, collection):
        # Calcular TF-IDF para cada término en el índice
        for document in collection:
            self.add(document)

        # Calcular TF-IDF para cada término en el índice
        idf_freq = dict()
        for term in self.index:
            idf_freq[term] = np.log(len(self.length) / len(self.index[term]))

        # Calcular TF-IDF para cada término en el índice
        tf_idf = dict()
        for term in self.index:
            tf_idf[term] = dict()
            for doc_id in self.index[term]:
                tf_idf[term][doc_id] = self.index[term].count(doc_id) * idf_freq[term]

        # Normalizar los vectores de documentos
        length = dict()
        for doc_id in self.length:
            length[doc_id] = 0
            for term in self.index:
                length[data['Documentos'][doc_id]] += tf_idf[term][doc_id] ** 2
            length[doc_id] = np.sqrt(length[doc_id])

        return length, idf_freq, self.index
    

# Crear una instancia de la clase InvertedIndex
index_instance = InvertedIndex()

# Calcular TF-IDF y otros resultados
length, idf_freq, index = index_instance.compute_tfidf(data, collection)

# Imprimir resultados
print("Longitud de vectores normalizados:")
for doc, value in length.items():
    print(f"{doc}: {value}")

print("\nIDF (Frecuencia inversa de documentos) para términos:")
for term, value in idf_freq.items():
    print(f"{term}: {value}")

print("\nÍndice de términos:")
for term, postings in index.items():
    print(f"{term}: {postings}")
