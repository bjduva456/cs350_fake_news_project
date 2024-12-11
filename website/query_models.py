# -*- coding: utf-8 -*-
import joblib
import tensorflow
#from keras.models import load_model
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import string
import json
import sys
import re
import io

'''
This script is used to manage model-based operations on the web server. 
It is invoked through server.js initially on start up, and again whenever a client sends a POST request.

On startup, this script prepares the models for use.

When invoked via POST request, this script takes the text input, converts it into a Document Term Matrix, and runs the DTM through our various models to make predictions.
It then generates a graph to show the differences in model predictions and confidence, which is saved on the server, and then returns the predictions and confidence back to
server.js as a JSON object. 
'''

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')

#the models and vectorizer are initialized as global objects to be used in multiple functions
bnb = None
rfc = None
svc = None
dnn = None
tfidf = None

#load_models() is called on server startup, it uses joblib and keras' load_model() to define the global objects. 
def load_models():
    base_path = '../models/'
    global bnb
    global rfc 
    global svc 
    global dnn
    global tfidf 
    bnb = joblib.load(base_path + 'bnb_best.joblib')
    rfc = joblib.load(base_path + 'rfc_best.joblib')
    svc = joblib.load(base_path + 'svc_best.joblib')
    dnn = load_model(base_path + 'dnn_tf.keras')
    tfidf = joblib.load('../data/tfidf.pkl')

#use_models() is ran in response to POST requests, it takes text input and converts it to a DTM, which is ran through our models. A graph and a JSON of prediction information are returned. 
def use_models(input):
    #==Text Formatting==
    text = input
    text = clean_text(text) #clean_text() is used to format the text the same way we did while training the models.
    X_new = tfidf.transform([text]) #the cleaned text is now turned into a DTM
    X_new_tf = tensorflow.convert_to_tensor(X_new.toarray(), dtype = tensorflow.float32) #The DNN was having issues predicting on X_new so I type cast it (as a dense matrix) into a tensor object.
    #==Prediction Generation==
    dnn_conf = dnn.predict(X_new_tf) #dnn_conf is defined as keras models predict differently than other models, their predictions are a floating value between 0 and 1 (and act as model confidence).
    svc_conf = svc.predict_proba(X_new.toarray()) #SVC's predict_proba() returns a vector of confidences. SVC also needed X_new to be converted to a dense matrix to run.
    predictions = {} 
    #The following line sets the label for ever model as Real or Fake depending on it's predict score (0 or 1 respectively). make_dnn_label() is used to convert the float to an int.
    predictions['label'] = ['Real' if x == 0 else 'Fake' for x in [bnb.predict(X_new)[0], rfc.predict(X_new)[0], svc.predict(X_new.toarray())[0], make_dnn_label(dnn_conf[0][0])]]
    #The following line sets the confidence for the models, max() needs to be found as predict_proba for sklearn models tends to return a vector.
    predictions['confidence'] = [bnb.predict_proba(X_new).max(axis = 1)[0], rfc.predict_proba(X_new).max(axis = 1)[0], max(svc_conf[0]), dnn_conf[0][0]]
    models = ['Bernoulli Naive-Bayes', 'Random Forest', 'Support Vector Classifier', 'Deep Neural Network']
    pred_df = pd.DataFrame(predictions, index = models) #A DataFrame is generated from the predictions, using the models as the index.
    #==Graph Generation==
    ax = sns.barplot(data = pred_df, x = pred_df.index, y = 'confidence', hue = 'label', palette='BuGn')
    for p in ax.patches: #this loop is used to annotate the bars with their height for better readability.
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{height:.2f}',
                    (p.get_x() + p.get_width() / 2., p.get_height()),  
                    ha='center', va='center', 
                    fontsize=12, color='black',  
                    xytext=(0, 5), textcoords='offset points') 
    ax.set_xlabel('Model', fontsize=14)
    ax.set_ylabel('Confidence Level', fontsize=14)
    ax.legend(title='Classification', fontsize=12)
    ax.set_title('Your Predictions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    random_filename = generate_random_filename() #A random filename is generated.
    filepath = f'./images/{random_filename}'
    plt.savefig(filepath, format='png', dpi=300)
    #==Compiling the results==
    json_data = pred_df.to_json(orient='index') #The df is converted to a JSON object, rotated so the confidence and prediction are attached to their own models as containers.
    json_dict = json.loads(json_data) #the JSON object is converted back to a dictionary to add the graph's filepath to.
    comp_dict = {}
    comp_dict['models'] = json_dict #predictions are added to the new dict under 'models'.
    comp_dict['filepath'] = random_filename #filepath is added to the dict.
    updated_json_data = json.dumps(comp_dict, indent=4) #the dict is converted to a JSON object, ready to be returned.
    return updated_json_data

#Helper function for use_models(), which cleans the text using regex and returns the clean text.
def clean_text(text):
    
    #type checking
    if not isinstance(text, str):
        return []

    #lowercasing
    text = text.lower()
    
    #removing punctuation
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)

    text = re.sub('[’‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    text = ' '.join(re.findall(r'\b[a-zA-Z0-9]+\b', text))


    return text

#Helper function for use_models() which converts the dnn's prediction to an int for use in the labels section of the predictions dict.
def make_dnn_label(conf):
    if conf > 0.5:
        return 1
    else:
        return 0

#Helper function for user_models() which generates a random filename for the graph
def generate_random_filename(extension='png', length=8):
    random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) #Create a string of 8 characters /[a-z0-9]/
    return f"{random_name}.{extension}" #return the randomly generated file name as a .png

#Main function that is invoked when the server starts, and again when a POST request is made.
if __name__ == "__main__":
    load_models()
    if len(sys.argv) > 1: #sys.argv refers to arguments passed to the function through Node.js child_process.spawn by default it has a length of 1.
        text = sys.argv[1] #the way the child_process.spawn is set up, the second argument will always be the text to parse.
        if isinstance(text, bytes):
            text = text.decode('utf-8', 'ignore') #this  is yet another way to ensure the text is using utf-8 encoding for the DNN
        result = use_models(text) 
        print(json.dumps(result)) #Prnting the result will activate child_process.spawn's stdout, allowing the data to be used.
        sys.stdout.flush() #Afterwards, clear the stdout to prevent cluttter.
