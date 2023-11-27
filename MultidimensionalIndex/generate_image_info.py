from skimage.io import imread
from skimage import transform
import pywt
import pywt.data
import pandas as pd
import struct
import numpy as np

output_file = "vector_images.bin"
position_data_file = "position_data.bin"
position_feature_file = "position_feature.bin"
images_csv = "images.csv"
features_csv = "styles.csv"
id_to_pos_file = "id_to_pos.bin"

INTEGER_BYTES = 4
FLOAT_BYTES = 4
N_FEATURES = 9
EXPECTED_LENGTH_DATA = 4000

id_to_pos = {}


def get_feature_vector(picture, cortes=3):
    LL = picture
    for i in range(cortes):
        LL, (LH, HL, HH) = pywt.dwt2(LL, 'haar')
    return LL.flatten()


def load_images(n: int):
    # Abre el archivo TXT en modo de escritura binario
    ids = []
    with open(output_file, 'wb') as file:
        position_data = open(position_data_file, "wb")
        links_image = pd.read_csv(images_csv)
        # Itera a través de las imágenes y obtiene las características

        i = 0
        for image_name, image_link in zip(links_image["filename"], links_image["link"]):
            if i == n:
                break

            position_seek = file.tell()          
            position_data.write(struct.pack('i', position_seek))
            img = imread(image_link)
            img_res = transform.resize(img, (250, 250, 3))
            img_encoding = get_feature_vector(img_res, 4)
            assert EXPECTED_LENGTH_DATA == len(img_encoding), "INVALID DATA"
            id = int(str(image_name[:len(image_name)-4]))
            ids.append([id, i])
            id_to_pos[id] = i
            data = struct.pack('i' + 'f'*len(img_encoding), id, *img_encoding)
            file.write(data)
            i += 1
        position_data.close()
    ids.sort()

    id_file = open(id_to_pos_file, "wb")
    for i in range(n):
        print(ids[i][0],ids[i][1])
        id_file.write(struct.pack('ii', ids[i][0], ids[i][1]))
    id_file.close()
    return EXPECTED_LENGTH_DATA


def get_vector(n: int):
    pos_file = open(position_data_file, "rb")
    pos_file.seek(n*INTEGER_BYTES)
    position_in_file = int.from_bytes(pos_file.read(INTEGER_BYTES), byteorder='little')
    pos_file.close()
    data_file = open(output_file, "rb")
    data_file.seek(position_in_file)
    data_bin = data_file.read(INTEGER_BYTES + EXPECTED_LENGTH_DATA * FLOAT_BYTES)
    data_file.close()
    return list(struct.unpack('i' + 'f'*EXPECTED_LENGTH_DATA, data_bin))[1:]


def get_pos_to_id(id: int, n: int):
    ini = 0
    fin = n-1
    file = open(id_to_pos_file, "rb")
    while ini < fin:
        mid = (ini + fin + 1) // 2
        file.seek(2*INTEGER_BYTES*mid)
        data = file.read(INTEGER_BYTES)
        [returned_id] = struct.unpack('i', data) 
        if id < returned_id:
            fin = mid-1
        else:
            ini = mid
    file.seek(2*INTEGER_BYTES*ini)
    data = file.read(2*INTEGER_BYTES)
    file.close()
    (returned_id, pos) = list(struct.unpack('ii', data))
    if returned_id != id:
        return -1
    return pos


def load_features(n: int):
    file = open(features_csv, "r")
    head = file.readline().split(',')
    head.pop()
    n_features = len(head)
    pos_file = open(position_feature_file, "wb")
    assert n_features == N_FEATURES, "INVALID DATA"
    for _ in range(n):
        position = file.tell()
        pos_file.write(struct.pack('i', position))
        data = file.readline()
        assert data is not None        
    pos_file.close()
    file.close()


def get_feature(n: int, feature: int = -1):
    position_file = open(position_feature_file, 'rb')
    position_file.seek(n*INTEGER_BYTES)
    pos_in_file = int.from_bytes(position_file.read(INTEGER_BYTES), byteorder='little')
    position_file.close()
    feature_file = open(features_csv, "r")
    feature_file.seek(pos_in_file)
    data_feature = feature_file.readline().split(',')
    feature_file.close()
    if feature == -1:
        return data_feature[:N_FEATURES]
    else:
        assert feature >= 0 and feature <= N_FEATURES, "INVALID FEATURE"
        if feature == 0:
            print("FEATURE IS ID")
        return data_feature[feature] 


def get_data_images(elements: list[int]):
    file = open(images_csv, "r")
    d = {}
    for i in range(len(elements)):
        d[elements[i]] = i
    data = [[]]*len(elements)
    for i in range(max(elements)+2):
        cur = file.readline()
        if i-1 in elements:
            cur = cur[:-1]
            cur = cur.split(',')
            cur.append(get_feature(i, N_FEATURES)[:-1])
            data[d[i-1]] = cur 
    return data


def get_distance(x: int, y: int):
    vector_x = np.array(get_vector(x))
    vector_y = np.array(get_vector(y))
    return np.array(np.sum(abs(vector_x-vector_y) ** 2)) ** 1/2


