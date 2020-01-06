import os
import numpy as np
from PIL import Image
from matplotlib import pylab as plt



main_folder = "AML-Cytomorphology_LMU"

def load_data(roof=100):

    image_data = []
    class_data = []
    class_index = 0
    for filename in os.listdir(main_folder):
        nr = 0
        for image in os.listdir(main_folder + "/" + filename):
            nr += 1
            im = Image.open(main_folder + "/" + filename + "/" + image)
            np_image = np.array(im)
            image_data += [np_image]
            class_data += [class_index]
            if roof:
                if nr >= roof:
                    break

        print(filename, " got ", nr, " sets.")
        class_index += 1

    return np.array(image_data), np.array(class_data)


# image_data, class_data = load_data()
# print("image data shape: ", image_data.shape)
# print("class data shape: ", class_data.shape)
