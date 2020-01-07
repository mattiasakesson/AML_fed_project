import numpy as np



def one_hot(class_data, classes=16):

    ret = np.zeros((len(class_data),classes))
    ret[np.arange(len(class_data)),class_data] = 1
    return ret


def split_train_test_set(image_data, class_data, split=0.1):

    classes = np.unique(class_data)
    class_ind = [[]]
    i=0
    for c in classes:
        print("c: ", c)
        class_ind[i] = np.where(class_data == c)
        i += 1

    train_x = []
    train_y = []
    test_x = []
    test_y = []

    for i in range(len(classes)):

        split_i = int(len(class_ind[i][0])*(1-split))
        if i == 0:
            train_x = image_data[:split_i]
            train_y = class_data[:split_i]
            test_x = image_data[split_i:]
            test_y = class_data[split_i:]
        else:
            train_x += image_data[:split_i]
            train_y += class_data[:split_i]
            test_x += image_data[split_i:]
            test_y += class_data[split_i:]
        
    return np.array(train_x), np.array(train_y), np.array(test_x), np.array(test_y)
            
            
        


