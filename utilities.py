import numpy as np



def one_hot(class_data, classes=16):

    ret = np.zeros((len(class_data),classes))
    ret[np.arange(len(class_data)),class_data] = 1
    return ret