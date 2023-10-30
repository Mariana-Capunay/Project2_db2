from skimage.io import imread
from skimage import transform
import pywt
import pywt.data
import pandas as pd
import struct

output_file = "vector_images.bin"
position_data_file = "position_data.bin"
images_csv = "images.csv"
INTEGER_BYTES = 4
FLOAT_BYTES = 4


def get_feature(picture, cortes=3):
    LL = picture
    for i in range(cortes):
        LL, (LH, HL, HH) = pywt.dwt2(LL, 'haar')
    return LL.flatten()


def load_images(n: int):
    # Abre el archivo TXT en modo de escritura binario
    with open(output_file, 'wb') as file:
        position_data = open(position_data_file, "wb")
        links_image = pd.read_csv(images_csv)
        # Itera a través de las imágenes y obtiene las características
        data_len = 0
        i = 0
        for image_name, image_link in zip(links_image["filename"], links_image["link"]):
            if i == n:
                break
            position_seek = file.tell()
            position_data.write(struct.pack('i', position_seek))
            img = imread(image_link)
            img_res = transform.resize(img, (250, 250, 3))
            img_encoding = get_feature(img_res, 4)
            assert data_len == 0 or data_len == len(img_encoding), "INVALID DATA"
            data_len = len(img_encoding)
            vector = struct.pack('f'*len(img_encoding), *img_encoding)
            id = int(str(image_name[:len(image_name)-4]))
            file.write(struct.pack('i', id))
            file.write(vector)
            i += 1
    return data_len


def get_vector(n: int):
    file = open(position_data_file, "rb")
    file.seek(n*INTEGER_BYTES)
    return struct.pack('f'*len(img_encoding), *img_encoding)

#print(load_images(10))

