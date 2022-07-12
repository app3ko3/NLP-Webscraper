from tensorflow import keras
from functions import *
from PIL import Image
import numpy as np
import cv2
import os

class LogoDetector():
    def __init__(self):
        self.model = keras.models.load_model(os.path.join(os.getcwd(), 'Lib', 'saved_model'))
        self.dims = (100, 100, 3) # i/p dimensions
        
    def prepare_img(self, src):
        ext = find_ext(src)
        path = gen_path(ext)

        if not download_url(src, path):
            return [], ''            

        try:
            img = Image.open(path)
        except:
            print('[Error]', src)
            return [], path
           
        if self.dims[2] == 3:
            img = img.convert('RGB')
                
        img = img.resize((self.dims[0], self.dims[1]))
        img.save(path)
        img_data = cv2.imread(path)
        
        return img_data, path

    def predict(self, srcs, verbose=False):
        preds = []
        for src in srcs:
            img_data, path = self.prepare_img(src)
            if path and path in os.listdir():
                os.remove(path)
            if len(img_data) > 0:
                pred = self.model.predict(np.array([img_data]))[0][0]
                preds.append(pred)
                print('[{:.2f}] {}'.format(pred, src))
            else:
                print('[X]', src)
        return preds
