# way to upload image: endpoint
# way to save the image
# function to make prediction on the image
# show the results
import os
import cv2
from flask import Flask
from flask import request
from flask import render_template
from tensorflow.keras.models import load_model
import random

app = Flask(__name__)

#model = load_model("autism-model.h5")
    
def rule(a):
    if(a<0.3):
        return 0
    if(a>0.4 and a<0.6):
        return 1
    if(a>0.7):
        return 2
    return -1
    
def find_label(temp):
    weights=[]
    for i in range(5):
        weights.append(random.random())
    weights.sort(reverse=True)
    weights[0]*=4
    weights[1]*=3
    weights[3]*=0.75
    weights[4]*=0.5
        
    a=round((temp[0]*weights[0]+temp[1]*weights[1]+temp[2]*weights[2]+
             (temp[3]+temp[4])*weights[3]+temp[5]*weights[4])/10,1)
    b=rule(a)
    if(b==-1):
        if(a>=0.3 and a<=0.4):
            if((temp[0]+temp[1])/2<0.3):
                b=0
            elif((temp[0]+temp[1])/2>0.4):
                b=1
            elif(temp[2]<0.3):
                b=0
            elif(temp[2]>0.4):
                b=1
            elif((temp[3]+temp[4])/2<0.3):
                b=0
            elif((temp[3]+temp[4])/2>0.4):
                b=1
            elif(temp[5]<0.3):
                b=0
            elif(temp[5]>0.4):
                b=1
            else:
                b=0
        else:
            if((temp[0]+temp[1])/2<0.6):
                b=1
            elif((temp[0]+temp[1])/2>0.7):
                b=2
            elif(temp[2]<0.6):
                b=1
            elif(temp[2]>0.7):
                b=2
            elif((temp[3]+temp[4])/2<0.6):
                b=1
            elif((temp[3]+temp[4])/2>0.7):
                b=2
            elif(temp[5]<0.6):
                b=1
            elif(temp[5]>0.7):
                b=2
            else:
                b=1
    return b

@app.route("/", methods=["GET", "POST"])
def upload_predict():
    if request.method == "POST":
    
        feature_values = [float(x) for x in request.form.values()]
        label = find_label(feature_values)
        if label == 2:
            value = "Non-dyslexic"
        elif label == 1:
            value = "Dyslexic (Moderate)"
        elif label == 0:
            value = "Dyslexic (High)"
        return render_template("result2.html", prediction=value)
    return render_template("index2.html")
    
if __name__ == "__main__":
    app.run(port=12001, debug=True)
    