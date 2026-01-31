import numpy as np
from engine.model import load_model

def predict_digit(img):
    img = img.resize((28, 28))
    img = img.convert("L")

    img = np.array(img)

    img = 255 - img

    img = img.reshape(1, 28, 28, 1)
    img = img / 255.0
    model = load_model("models/emnist_ds.keras")
    res = model.predict(img, verbose=0)[0]
    return np.argmax(res), np.max(res)