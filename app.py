# Serve model as a lambda function

import pickle
import numpy as np
import sys
import base64
import json
print('Loading function')

model = None
# model variable refers to the global variable
with open('iris_trained_model.pkl', 'rb') as f:
    model = pickle.load(f)

#Load Model
def handler(event, context):
    global model

    print("Received event: " + json.dumps(event, indent=2))
    data = json.loads(base64.b64decode(event['body']).decode('ascii')) # Get data posted as a json
    print("base64 decoded: " + json.dumps(data, indent=2))
    data = np.array(data)[np.newaxis, :]  # converts shape from (4,) to (1, 4)
    prediction = model.predict(data)  # runs globally loaded model on the data
    return str(prediction[0])

