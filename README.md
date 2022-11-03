The goal of this project is to create a machine learning model that will determine from a user's photo who he looks like from celebrities.  
Project stages:  
1) Data search (image parsing)  
2) Writing an image processing program (in order to form a training and test sample)  
3) Choosing the optimal ML model  
4) ML model training (takes place in Google Colab environment, GPU is used)  
5) ML model pipeline formation  
6) Conclusion of the ML model in a Docker container  
  
The stack of technologies used: Python, Docker, Jupyter Notebook(Google Colab), Keras, OpenCV, NumPy, face_recognition  
  
By translating the task into machine learning language, the task is a multi-class classification.  
The metric in the project is accuracy.  
  
A multilayer neural network was chosen as a machine learning model.  Based on the logic of the problem, the accuracy of the prediction of the neural network model is more important than the speed.  
Dropout layers are used to reduce overfitting. To speed up learning - Batch Normalization.  
Activation function in all layers of the network, (except the last layer) - ELU.  
The training of the multilayer neural network model was carried out in the Google Colab environment, using GPU. Next, the entire model (weights, state of the optimizer, and other parameters) was saved on the local computer, in order to create a pipeline, as well as deploy the model to a Docker container. 
  
ML Pipeline:
 - Image analysis by the face_recognition library for face recognition  
 - If the face in the image is recognized, we cut out everything superfluous from the image, leaving only the face  
 - We change the face image to 170x170 pixels  
 - We pass the resize-images to the face_encodings function of the face_recognition library, as a result, all images are encoded as a vector of size 128x1  
 - We transmit the image encoded as a vector to the input of the neural network  
 - There are 233 neurons on the output layer of the neural network, the output values of which represent the probabilities of belonging to a particular class (a certain celebrity is a class), the activation function of the output layer is Softmax. From the output values of the last layer of the neural network, we take the maximum, the index of the maximum value is the class number - this is the prediction of the neural network for the object. In order to make a prediction in the form of a string, we take a string from the dictionary by the current (maximum) index  
 
 As a result of the project, a model with a multilayer neural network architecture was obtained (the number of layers is optimal), which was trained on high-quality data and, as a result, has a high metric (accuracy) on test data. As well as a fully formed pipeline from image processing to the final prediction of the model.   
 The model within the project was packaged in a Docker container for further use.  
