import os
import numpy as np
from PIL import Image
from matplotlib import pylab as plt
from scipy import misc
from utilities import split_train_test_set


class_keys = {'BAS': 0, 'EBO': 1, 'EOS': 2, 'KSC': 3, 'LYA': 4, 'LYT': 5, 'MMZ': 6, 'MOB': 7, 'MON': 8, 'MYB': 9 , 'MYO': 10,
        'NGB': 11, 'NGS': 12, 'PMB': 13, 'PMO': 14}

main_folder = "AML-Cytomorphology_LMU"

def load_data(roof=100,downsample=False):

    first = True
    image_data = []
    class_data = []
    #class_index = 0
    for filename in os.listdir(main_folder):
        class_index = class_keys[filename]
        print("class index: ", class_index)
        nr = 0
        for image in os.listdir(main_folder + "/" + filename):
            nr += 1
            im = Image.open(main_folder + "/" + filename + "/" + image)
            np_image = np.array(im)
            np_image = misc.imresize(np_image, 0.25)
            image_data += [np_image]
            class_data += [class_index]
            if roof:
                if nr >= roof:
                    break
            if first:
                plt.imshow(np_image)
                plt.show()
                print("np_image shape: ", np_image.shape)

                first = False

        print(filename, " got ", nr, " sets.")
        #class_index += 1

    return np.array(image_data), np.array(class_data)


# image_data, class_data = load_data(roof=None)
# print("image data shape: ", image_data.shape)
# print("class data shape: ", class_data.shape)
#
# train_x, train_y, test_x, test_y = split_train_test_set(image_data, class_data, split=0.1)
#
# def check_class_nr(class_data):
#
#     classes, return_counts = np.unique(class_data, return_counts = True)
#     for i in range(len(classes)):
#         print("class ", class_keys[classes[i]], ": ", return_counts[i])
#
#
# print("train check: ")
# check_class_nr(train_y)
# print("test check: ")
# check_class_nr(test_y)
