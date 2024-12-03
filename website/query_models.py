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

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'utf-8')

bnb = None
rfc = None
svc = None
dnn = None
tfidf = None

def load_models():
    base_path = '../models/'
    global bnb
    global rfc 
    global svc 
    global dnn
    global tfidf 
    #print(tensorflow.__version__)
    bnb = joblib.load(base_path + 'bnb_best.joblib')
    rfc = joblib.load(base_path + 'rfc_best.joblib')
    svc = joblib.load(base_path + 'svc_best.joblib')
    dnn = load_model(base_path + 'dnn_tf.keras')
    #print(dnn)
    #print(dnn.summary())
    tfidf = joblib.load('../data/tfidf.pkl')
    #print(tfidf)

def use_models(input):
    text = input
    #print("New Text: " + text)
    text = clean_text(text)
    X_new = tfidf.transform([text])
    #print(X_new)
    #print(X_new.shape)
    #print(type(X_new))
    X_new_tf = tensorflow.convert_to_tensor(X_new.toarray(), dtype = tensorflow.float32)
    #print("New type: " + str(type(X_new_tf)))
    dnn_conf = dnn.predict(X_new_tf)
    svc_conf = svc.predict_proba(X_new.toarray())
    predictions = {}
    predictions['label'] = ['Real' if x == 0 else 'Fake' for x in [bnb.predict(X_new)[0], rfc.predict(X_new)[0], svc.predict(X_new.toarray())[0], make_dnn_label(dnn_conf[0][0])]]
    predictions['confidence'] = [bnb.predict_proba(X_new).max(axis = 1)[0], rfc.predict_proba(X_new).max(axis = 1)[0], max(svc_conf[0]), dnn_conf[0][0]]
    models = ['Bernoulli Naive-Bayes', 'Random Forest', 'Support Vector Classifier', 'Deep Neural Network']
    pred_df = pd.DataFrame(predictions, index = models)
    ax = sns.barplot(data = pred_df, x = pred_df.index, y = 'confidence', hue = 'label', palette='BuGn')
    for p in ax.patches:
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
    random_filename = generate_random_filename()
    filepath = f'./images/{random_filename}'
    plt.savefig(filepath, format='png', dpi=300)
    json_data = pred_df.to_json(orient='index')
    #print(type(json_data))
    json_dict = json.loads(json_data)
    comp_dict = {}
    comp_dict['models'] = json_dict
    comp_dict['filepath'] = random_filename
    updated_json_data = json.dumps(comp_dict, indent=4)
    return updated_json_data

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


def make_dnn_label(conf):
    if conf > 0.5:
        return 1
    else:
        return 0

def generate_random_filename(extension='png', length=8):
    random_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"{random_name}.{extension}"

if __name__ == "__main__":
    load_models()
    if len(sys.argv) > 1:
        text = sys.argv[1]
        #print(type(text))
        if isinstance(text, bytes):
            text = text.decode('utf-8', 'ignore')
        #print(text)
        result = use_models(text)
        print(json.dumps(result))
        sys.stdout.flush()
'''
    for line in sys.stdin:
        data = json.loads(line)
        text = data.get('text', '')
        result = use_models(text)
        print(json.dumps(result))
        sys.stdout.flush()
'''