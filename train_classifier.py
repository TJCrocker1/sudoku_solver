from classifier import digit_net
from keras.optimizers import Adam
from keras.datasets import mnist
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
import argparse

# ----------------------------------------------------------------------------------------------------------------------
# argument parser
# ----------------------------------------------------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help = "path to model output after trainning")
args = vars(ap.parse_args())

# ----------------------------------------------------------------------------------------------------------------------
# initialize the initial learning rate, number of epochs to train for, and batch size
# ----------------------------------------------------------------------------------------------------------------------
INIT_LR = 1e-3
EPOCHS = 10
BS = 128

# ----------------------------------------------------------------------------------------------------------------------
# import and modify the MNIST data set
# ----------------------------------------------------------------------------------------------------------------------

# load the MNIST dataset
print("[INFO] accessing MNIST...")
((trainData, trainLabels), (testData, testLabels)) = mnist.load_data()

# add a channel (i.e., grayscale) dimension to the digits
trainData = trainData.reshape((trainData.shape[0], 28, 28, 1))
testData = testData.reshape((testData.shape[0], 28, 28, 1))

# scale data to the range of [0, 1]
trainData = trainData.astype("float32") / 255.0
testData = testData.astype("float32") / 255.0

# convert the labels from integers to vectors
le = LabelBinarizer()
trainLabels = le.fit_transform(trainLabels)
testLabels = le.transform(testLabels)

# ----------------------------------------------------------------------------------------------------------------------
# initialise and train the model
# ----------------------------------------------------------------------------------------------------------------------

# initialize the optimizer and model
print("[INFO] compiling model...")
opt = Adam(lr=INIT_LR)
model = digit_net.build(width=28, height=28, depth=1, classes=10)
model.compile(loss="categorical_crossentropy", optimizer=opt,
	metrics=["accuracy"])

# train the network
print("[INFO] training network...")
H = model.fit(
	trainData, trainLabels,
	validation_data=(testData, testLabels),
	batch_size=BS,
	epochs=EPOCHS,
	verbose=1)

# ----------------------------------------------------------------------------------------------------------------------
# evaluate the model and save
# ----------------------------------------------------------------------------------------------------------------------

# evaluate the network
print("[INFO] evaluating network...")
predictions = model.predict(testData)
print(classification_report(
	testLabels.argmax(axis=1),
	predictions.argmax(axis=1),
	target_names=[str(x) for x in le.classes_]))

# serialize the model to disk
print("[INFO] serializing digit model...")
model.save(args["model"], save_format="h5")