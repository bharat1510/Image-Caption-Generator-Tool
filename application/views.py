from re import search
from django.shortcuts import render, redirect
from .models import *
from image_caption_generator.settings import *

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages


# Web Scapping Packages
from urllib.request import urlopen as uReq

# For Model
import cv2
import numpy as np
from tensorflow import keras


# Create your views here.
def index(request):
    if request.method == 'GET':
        var = {
            'result': True,
        }
        return render(request, 'index.html', var)

    elif request.method == 'POST':
        searchImg = request.POST.get('image', '')

        resultImg = getImage(searchImg)

        caption = generateLabel(resultImg)

        var = {
            'result': True,
        }

        return render(request, 'productlist_search.html', var)

 
def getImage(searchImg):
    
    test_img = cv2.imread(searchImg)
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)

    test_img = cv2.resize(test_img, (224,224))
    # test_img = cv2.resize(test_img, (299,299))

    test_img = np.reshape(test_img, (1,224,224,3))
    # test_img = np.reshape(test_img, (1,299,299,3))
    
    return test_img

# from keras.preprocessing.sequence import pad_sequences

def generateLabel(resultImg):
    
    model = keras.models.load_model('path/to/location')

    test_feature = modele.predict(resultImg).reshape(1,2048)
    
    test_img = cv2.imread(searchImg)
    test_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)


    text_inp = ['startofseq']

    count = 0
    caption = ''

    while count < 25:
        count += 1

        encoded = []
        for i in text_inp:
            encoded.append(new_dict[i])

        encoded = [encoded]

        encoded = pad_sequences(encoded, padding='post', truncating='post', maxlen=40)


        prediction = np.argmax(model.predict([test_feature, encoded]))

        sampled_word = inv_dict[prediction]

        caption = caption + ' ' + sampled_word
            
        if sampled_word == 'endofseq':
            break

        text_inp.append(sampled_word)
        
    plt.figure()
    plt.imshow(test_img)
    plt.xlabel(caption)




