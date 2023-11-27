import generate_image_info
from rtree import index
from sklearn.decomposition import PCA
import struct
pca_vector_images = "pca_vector_images.bin"


class KNN_High_D_Tree:

    def __init__(self, n_data: int, load_data: bool, size:int = 100, rd:bool = True):
        self.n_data = n_data
        self.size = min(size, n_data)
        p = index.Property()
        p.dimension = self.size
        
        if load_data:
            generate_image_info.load_images(n=n_data)
            generate_image_info.load_features(n=n_data)
        self.idx = index.Index(properties=p)
        pca = PCA(n_components=self.size)  
        
        if rd:
            data = [[]] * n_data

            for i in range(n_data):
                data[i] = generate_image_info.get_vector(i)
                   
            data = pca.fit_transform(data)
            file = open(pca_vector_images, "wb")
            for i in range(n_data):
                self.idx.insert(i, tuple(data[i] + data[i]))
                data_to_write = struct.pack('f'*len(data[i]), *data[i])
                file.write(data_to_write)
                i += 1
            file.close()

    def get_vector(self, n: int):
        data_file = open(pca_vector_images, "rb")
        data_file.seek(4*self.size*n)
        data_bin = data_file.read(self.size * 4)
        data_file.close()
        return list(struct.unpack('f'*self.size, data_bin))

    def knn_search(self, id: int, k: int = 8):
        point = generate_image_info.get_pos_to_id(id, self.n_data)
        assert point >= 0, "No existe el ID"
        result_ids = list(self.idx.nearest(self.get_vector(point), num_results=k))
        result_ids = result_ids
        return generate_image_info.get_data_images(result_ids)

a =  KNN_High_D_Tree(40000, True, 100, False)
print(a.knn_search(15970, 5))