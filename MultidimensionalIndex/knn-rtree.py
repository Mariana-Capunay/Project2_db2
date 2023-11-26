import generate_image_info
import numpy as np
from rtree import index

class KNN_R_Tree:
	def __init__(self, n_data: int, load_data: bool = True, load_feature: bool = True):
		self.n_data = n_data
		if load_data:
			generate_image_info.load_images(n=n_data)
		if load_feature:
			generate_image_info.load_features(n=n_data)
		self.index = index.Index()
		for i in range(n_data):
			generate_image_info.get_vector(i)
	
	def get_distance(x: int, y: int):
		vector_x = np.array(generate_image_info.get_vector(x))
		vector_y = np.array(generate_image_info.get_vector(y))
		return np.array(np.sum(abs(vector_x-vector_y) ** 2)) ** 1/2
	