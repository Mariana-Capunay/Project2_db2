import generate_image_info
import numpy as np
import heapq


class KNN_Secuencial:
	def __init__(self, n_data: int, load_data: bool = True, load_feature: bool = True):
		self.n_data = n_data
		if load_data:
			generate_image_info.load_images(n=n_data)
		if load_feature:
			generate_image_info.load_features(n=n_data)
	
	def get_distance(x: int, y: int):
		vector_x = np.array(generate_image_info.get_vector(x))
		vector_y = np.array(generate_image_info.get_vector(y))
		return np.array(np.sum(abs(vector_x-vector_y) ** 2)) ** 1/2
	
	def range_search(self, point: int, feature: int, max_dist):
		value_point = generate_image_info.get_feature(point, feature)
		total, n_good = 0, 0
		result = []
		for i in range(self.n_data):
			if i == point and self.get_distance(i, point) < max_dist:
				near_point_value = generate_image_info.get_feature(i, feature)
				result.append(i)
				total += 1
				if near_point_value == value_point:
					n_good += 1
		return result, n_good / total
	
	def knn_search(self, point: int, feature: int, k: int = 8):
		value_point = generate_image_info.get_feature(point, feature)
		heap = []
		for i in range(self.n_data):
			if i == point:
				continue
			d = self.get_distance(i, point)
			
			if len(heap) < k:
				heap.append((-d, i))
				if len(heap) == k:
					heapq.heapify(heap)
			else:
				heapq.heappushpop(heap, (-d, i))
		result = []
		accepted = 0
		for d, near_point in heap:
			result.append(near_point)
			if value_point == generate_image_info.get_feature(near_point, feature):
				accepted += 1
		return heap, accepted / len(result)