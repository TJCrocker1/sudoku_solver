# ------------------------------------------------ sudoku net ----------------------------------------------------------
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Activation
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Dropout

# ----------------------------------------------------------------------------------------------------------------------
# SudokuNet is a network with two convolutional and two fully connected layers
# ----------------------------------------------------------------------------------------------------------------------
class digit_net:
    @staticmethod
    def build (width, height, depth, classes):

        # initialise model
        model = Sequential()
        inputShape = (height, width, depth)

        # first set of CONV => RELU => POOL layers
        model.add(Conv2D(32, (5, 5), padding = "same", input_shape = inputShape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2,2)))

        # second set of CONV => RELU => POOL layers
        model.add(Conv2D(32, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        # first set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(64))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))

        # second set of FC => RELU layers
        model.add(Dense(64))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))

        # softmax classifier
        model.add(Dense(classes))
        model.add(Activation("softmax"))

        # return the constructed network architecture
        return model