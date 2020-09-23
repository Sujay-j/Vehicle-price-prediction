from flask import Flask,render_template,request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import  StandardScaler

app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

standard_to = StandardScaler()
@app.route("/predict",methods=['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        kms_Driven2 = np.log(Kms_Driven)
        Owner = int(request.form['Owner'])
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol == 'Petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
        elif(Fuel_Type_Petrol=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel =1
        else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
        year=2020-year
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual =1
        else:
            Seller_Type_Individual = 0

        Transmission_Mannual = request.form['Transmission_Mannual']
        if Transmission_Mannual == 'Mannual':
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0
        Prediction = model.predict([[Present_Price,kms_Driven2,Owner,year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
        output = round(Prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_text="Sorry you cannot sell this cars=")
        else:
            return render_template('index.html',prediction_text="You can sell this car at {}".format(output))
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)