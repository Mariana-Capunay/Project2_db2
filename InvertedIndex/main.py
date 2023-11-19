from InvertedIndex import InvertedIndex
from InvertedIndex import processQuery
from Global_Index.merge_posting import final_merge

a = InvertedIndex()
nro_buckets = 128
final_merge(nro_buckets=nro_buckets)


    



