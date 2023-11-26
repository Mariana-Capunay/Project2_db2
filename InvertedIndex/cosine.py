import json
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from InvertedIndex import path_local_index
from InvertedIndex import preProcessListandIndex
from InvertedIndex import processQuery




def retrieval(self, doc_index,doc_idfs,query,k): # calcula el coseno entre el vector de la query y el vector de cada documento. Tiene como entrada a self, el indice invertido, los idf de los documentos, la query y el numero de documentos a retornar
    #diccionario para almacenar los resultados
    results = {}
    #prepocesamos la query
    query = processQuery(query)

    r=[]

    #contabilizamos la cantidad de palabras de la query en un dicc
    query_freq = {}
    for term in query:
        if term in query_freq:
            query_freq[term] += 1
        else:
            query_freq[term] = 1
    
    #calculamos el tf-idf de la query
    for term in doc_index:
        if term in query_freq:
            tf = np.log10(query_freq[term] + 1)
            idf = self.calculo_idf(term, doc_idfs, doc_index, len(doc_index))
            r.append(round(tf * idf, 3))
        else:
            r.append(0)

    #calculamos la norma de la query
    array = np.array(list(r))
    query_norm = np.linalg.norm(array)

    #calculamos el coseno entre la query y cada documento
    for doc in doc_index:
        #calculamos el coseno
        dot_product = np.dot(r, doc_index[doc])
        doc_norm = doc_idfs[doc]
        cos = dot_product / (query_norm * doc_norm)
        results[doc] = cos

    #ordenamos los resultados
    results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    #retornamos los k primeros
    return results[:k]

doc_index = preProcessListandIndex.index 

