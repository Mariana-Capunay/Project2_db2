from InvertedIndex import InvertedIndex
from InvertedIndex import processQuery
from Global_Index.merge_posting import final_merge

a = InvertedIndex()
nro_buckets = 128
final_merge(nro_buckets=nro_buckets)



#imprimir preProcessCSV
print("PreProcessCSV:")
a.preProcessCSV("data/1000.csv")

#llamar a la funcion para procesar la consulta y calcular similitudes
print("processQuery:")
similarities = a.process_query_and_calculate_similarities("coronavirus covid-19")


