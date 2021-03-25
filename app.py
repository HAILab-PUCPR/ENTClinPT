import flask
from flask import Flask, render_template
from flask import request
from flask.json import jsonify
import json
import predict_ner as predict

app = flask.Flask(__name__)
app.config["DEBUG"] = True

MODELS_DIR = [
              "pucpr/clininalnerpt-finding"
              #,"pucpr/clininalnerpt-chemical"
              #,"pucpr/clininalnerpt-diagnostic"
              #,"pucpr/clininalnerpt-procedures"
              #,"pucpr/clininalnerpt-disease"
              #,"pucpr/clininalnerpt-disorders"
              #,"pucpr/clininalnerpt-healthcare"
              #,"pucpr/clininalnerpt-laboratory"
              #,"pucpr/clininalnerpt-medical"
              #,"pucpr/clininalnerpt-pharmacologic"
              #,"pucpr/clininalnerpt-quantitative"
              #,"pucpr/clininalnerpt-sign"
              #,"pucpr/clininalnerpt-therapeutic"
]




@app.route('/', methods=['GET'])
def index():
    print ("iniciando")
    print(MODELS_DIR)
    return render_template('index.html')

@app.route("/entidades")
def ner():
    SentencasSomente = [request.args.get('word')]
    result = predict.predictALLSentenceBERT(SentencasSomente,MODELS_DIR)
    return jsonify(result)

#app.run()
#app.run(host="0.0.0.0", port=int("5000"), debug=False)#map port to 5000
#process.env.PORT

import os
port = int(os.environ.get("PORT", 5000))

app.run(host="0.0.0.0", port=port, debug=False)#map port to 5000
