import tensorflow as tf
import numpy as np
import cv2

model = tf.keras.applications.MobileNetV2(weights="imagenet")

def classify_coin(image):
    img_resized = cv2.resize(image, (224, 224))
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(
        np.expand_dims(img_resized, axis=0)
    )
    preds = model.predict(img_array)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]
    return decoded
