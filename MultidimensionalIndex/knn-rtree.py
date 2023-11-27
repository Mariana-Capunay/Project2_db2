import generate_image_info
from rtree import index


class KNN_R_Tree:
	def __init__(self, n_data: int, load_data: bool = True):
		self.n_data = n_data
		p = index.Property()
		p.dimension = generate_image_info.EXPECTED_LENGTH_DATA 		
		if load_data:
			generate_image_info.load_images(n=n_data)
			generate_image_info.load_features(n=n_data)
		self.idx = index.Index(properties=p)
	   	
		for i in range(n_data):
			vector = generate_image_info.get_vector(i)
			self.idx.insert(i, tuple(vector + vector))

	def knn_search(self, id: int, k: int = 8):
		try:
			point = generate_image_info.get_pos_to_id(id)
		except:
			return []
		result_ids = list(self.idx.nearest(generate_image_info.get_vector(point), num_results=k))
		result_ids = result_ids
		return generate_image_info.get_data_images(result_ids)


