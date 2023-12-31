import json
import pickle
from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd


app=Flask(__name__)
## Load the model
regmodel=pickle.load(open('regmodel.pkl','rb'))
scalar=pickle.load(open('scaling.pkl','rb'))
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    request_data=request.json['data']
    print(request_data)
    print(np.array(list(request_data.values())).reshape(1,-1))
    new_data=scalar.transform(np.array(list(request_data.values())).reshape(1,-1))
    output=regmodel.predict(new_data)
    x=output[0].tolist()
    return jsonify(x)
    

@app.route('/predict',methods=['POST'])
def predict():
   data=[float(x) for x in request.form.values()]## for every value in request.form we are converting into float and passing into data
   final_input=scalar.transform(np.array(data).reshape(1,-1))
   print(final_input)
   output=regmodel.predict(final_input)[0]
   return render_template("home.html",prediction_text="The house price prediction is {}".format (output))

if __name__=="__main__":
    app.run(debug=True)