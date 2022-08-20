import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import joblib

app = FastAPI(debug=True)

@app.get('/')
def hello():
    return {'welcome': 'yeah'}

@app.get('/{name}')
def user(name:str):
    return {'Welcome, {}! Enter values to test the water quality'.format(name)}

#create a route to predict the water potability model
@app.post('/predict')
def waterQuality(ph:float, Hardness:float, Solids:float, Chloramines:float, Sulfate:float,Conductivity:float, Organic_carbon:float, Trihalomethanes:float, Turbidity:float):
    model = joblib.load('water_model.pkl')
    make_prediction = model.predict([[ph, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity]])
    result = make_prediction[0]
    if (result == 0):
        return {"The water is not potable"}
    else:
        return {"The water is potable"}
    # if (result == 0):
    #     print('Water is not potable')
    # else:
    #     print("Water is potable")

    # return {'Prediction' : result}

if __name__ == "__main__":
    uvicorn.run("deployment.fastapi_app:app", port='127.0.0.1', host='8000')

