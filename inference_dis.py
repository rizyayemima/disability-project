#!/usr/bin/env python
# coding: utf-8

# In[19]:


import tensorflow as tf
import numpy as np
import json
import warnings 
warnings.filterwarnings('ignore')

import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk


# In[20]:


# load YAML model
json_file = open('model.json', 'r')
model_json = json_file.read()
json_file.close()
model = tf.keras.models.model_from_json(model_json)
# load weights into model
model.load_weights("model.h5")


# In[45]:


root = tk.Tk()
root.geometry("420x300")  # Size of window 
root.title('Pengenalan Alphabet BISINDO - DIS_6')
my_font1=('times', 18, 'bold')
l1 = tk.Label(root,text='Alphabet BISINDO',width=30,font=my_font1)  
l1.grid(row=1,column=1,columnspan=3)
b1 = tk.Button(root, text='Upload Images', width=20,command = lambda:upload_file())
b1.grid(row=2,column=1,columnspan=3)


# In[46]:


def upload_file():
    f_types = [('Jpg Files', '*.jpg'),('PNG Files','*.png')]   # type of files to select 
    filename = tk.filedialog.askopenfilename(multiple=True,filetypes=f_types)
    col=1 # start from column 1
    row=4 # start from row 4
    
    result = {}
    for f in filename:
        img=Image.open(f) 
        pred=predict(f)
        if len(filename)==1: col=2 # if single image put it center
        img=img.resize((100,100), Image.ANTIALIAS) # new width & height
        img=ImageTk.PhotoImage(img)
        e1 =tk.Label(root) 
        e1.grid(row=row,column=col)
        e1.image = img
        e1['image']=img         
        e1 = tk.Label(root,text=pred)
        e1.grid(row=row+1,column=col)
        if(col==3): # start new line
            row=row+2# next row, skip 1 row for label
            col=1    # first column
        else:       # within the same row 
            col=col+1 # next column         
    
    print(pred)

def predict(img):
    img = tf.keras.preprocessing.image.load_img(img, target_size=(150,150))
    x = tf.keras.preprocessing.image.img_to_array(img)/255.
    x = np.expand_dims(x, axis=0)
    
    image = np.vstack([x])
    pred = np.max(model.predict_classes(image), axis=-1)

    from string import ascii_uppercase
    alphabets = [az for az in ascii_uppercase]

    return ' '+alphabets[pred]+' '


# In[47]:


root.mainloop()


# In[ ]:




