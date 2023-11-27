import generate_image_info
import heapq


class KNN_Secuencial:
	def __init__(self, n_data: int, load_data: bool):
		self.n_data = n_data
		if load_data:
			generate_image_info.load_images(n=n_data)
			generate_image_info.load_features(n=n_data)
	
	def range_search(self, id: int, feature: int, max_dist):
		point = generate_image_info.id_to_pos[id]
		value_point = generate_image_info.get_feature(point, feature) if feature != -1 else 0
		total, n_good = 0, 0
		result = [point]
		for i in range(self.n_data):
			
			if i == point and generate_image_info.get_distance(i, point) < max_dist * 4000:
				near_point_value = generate_image_info.get_feature(i, feature) if feature != -1 else 0
				result.append(i)
				total += 1
				if near_point_value == value_point:
					n_good += 1
		return generate_image_info.get_data_images(result), n_good / total 
	
	def knn_search(self, id: int, feature: int, k: int = 8):
		point = generate_image_info.get_pos_to_id(id, self.n_data)
		assert point >= 0, "No existe el ID"
		value_point = generate_image_info.get_feature(point, feature) if feature != -1 else 0
		heap = []
		for i in range(self.n_data):
			if i == point:
				continue
			d = generate_image_info.get_distance(i, point)
			
			if len(heap) < k:
				heap.append((-d, i))
				if len(heap) == k:
					heapq.heapify(heap)
			else:
				heapq.heappushpop(heap, (-d, i))
				
		result = [point]
		accepted = 0
		for d, near_point in heap:
			result.append(near_point)
			if value_point == 0 or value_point == generate_image_info.get_feature(near_point, feature):
				accepted += 1
		return generate_image_info.get_data_images(result), accepted / len(result)
	
# a = KNN_Secuencial(20, True)
# rows ,acuarry = a.knn_search(15970, -1,k=5)
# print(rows)
# print(acuarry)
