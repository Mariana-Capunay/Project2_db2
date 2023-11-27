from InvertedIndex import InvertedIndex
from Global_Index.merge_posting import final_merge
from read_byte import get_row
# 1. Creamos instancia de Inverted Index
indice = InvertedIndex()

# 2. Aplicamos SPIMI a CSV
#indice.do_Spimi()

# 3. Definimos el total de buckets y hacemos el merge hasta tener una sola carpeta ordenada
#nro_buckets = 128
#final_merge(nro_buckets=nro_buckets)


################################################################ Query 

#1. Procesamos la query y calculamos similitudes
InvertedIndexQuery = indice.processQuery("adidas shoes red") # obtenemos similitudes
print("processQuery:",InvertedIndexQuery)

#2. Calculamos el coseno entre query y los docs
result = indice.cosine(InvertedIndexQuery,5)

print("Filas que coinciden: ")
for pos_row in result:
    print(get_row(pos_row))
#print(result)