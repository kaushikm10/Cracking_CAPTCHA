from flask import Flask, render_template, url_for, request
from keras.models import load_model
import numpy as np 
from captcha.image import ImageCaptcha
import random
import string
import cv2
import os
import time

app = Flask(__name__)
model = load_model('captcha.h5')
lower = list(string.ascii_lowercase)


def predict(filename):
    img = cv2.imread(filename)/255.0
    img = np.expand_dims(img, axis=0)
    res = np.array(model.predict(img))
    ans = np.reshape(res, (5, 26))
    l_ind = []
    probs = []
    for a in ans:
        l_ind.append(np.argmax(a))
    capt = ''
    for l in l_ind:
        capt = capt + lower[l]
    return capt

def generate_captcha():
    length = 5
    captcha = ""
    for i in range(length):
        captcha = captcha + lower[random.randint(0, 25)]
    image = ImageCaptcha()
    data = image.generate(captcha)

    for filename in os.listdir('static/img'):
        if filename.startswith('gene'):
            os.remove('static/img/'+filename)
    temp = str(time.time())[:10]
    filename = f'static/img/generated_captcha_{temp}.png'
    image.write(captcha, f'static/img/generated_captcha_{temp}.png')
    return captcha, filename

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        captcha, filename = generate_captcha()
        pred = predict(filename)
        return render_template('home.html', flag=1, captcha=captcha, prediction=pred, filename=filename)
    return render_template('home.html', flag=0)

if __name__ == '__main__':
    app.run(debug=False)
