import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import mnist
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
import cv2

# Define the model architecture
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48, 48, 1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', optimizer=Adam(learning_rate=0.001), metrics=['accuracy'])

# Load and preprocess data
# Example data loading code (replace with actual emotion dataset)
# Here I'm using a dummy dataset (like MNIST) to simulate the data structure and shape
# Replace this section with your actual dataset loading and preprocessing code

# Loading and processing a dataset for emotion recognition (like FER2013)
# x_train, y_train, x_test, y_test = load_emotion_dataset()

# Split dataset into training and validation sets
# x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.2, random_state=42)

# Train the model
callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, verbose=1),
    ModelCheckpoint('emotion_model.h5', save_best_only=True, verbose=1)
]

# Uncomment this section for actual training
# model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=30, batch_size=64, callbacks=callbacks)

# Load weights for the model if not training
model.load_weights('base/model.h5')

# Using the model for inference
# Load an example image, preprocess it, and predict emotion
def preprocess_image(image_path):
    # Load the image
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # Resize to match model input
    img = cv2.resize(img, (48, 48))
    # Normalize the image
    img = img / 255.0
    # Reshape to match input dimensions
    img = np.expand_dims(img, axis=-1)
    return img

# Load and preprocess a sample image for inference
sample_image = preprocess_image("sample_face.jpg")  # Replace with your sample image path

# Make a prediction
prediction = model.predict(np.array([sample_image]))
emotion_classes = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Find the class with the highest probability
predicted_emotion = emotion_classes[np.argmax(prediction)]

print("Predicted Emotion:", predicted_emotion)
