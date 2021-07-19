import flask
from flask import Flask, render_template
from flask import request
from flask.json import jsonify
import json
import predict_ner as predict

app = flask.Flask(__name__)
app.config["DEBUG"] = True

'''
MODELS_DIR = [
              r"/home/terumi/Documents/NER_BioBERTpt/scripts/model10_drugsepocas"
              ,r"/home/terumi/Documents/NER_BioBERTpt/scripts/model10epocas_DiagnosticProcedureDados"
              ,r"/home/terumi/Documents/NER_BioBERTpt/scripts/model10epocas_DiseaseSyndromeDados"             
              ,r"/home/terumi/Documents/NER_BioBERTpt/scripts/model10epocas_HealthCareActivityDados"             
]
'''
MODELS_DIR = [
              r"pucpr/clinicalnerpt-chemical"
              ,r"pucpr/clinicalnerpt-diagnostic"
              ,r"pucpr/clinicalnerpt-disease"             
              ,r"pucpr/clinicalnerpt-disorder"             
              ,r"pucpr/clinicalnerpt-finding"             
              ,r"pucpr/clinicalnerpt-healthcare"             
              ,r"pucpr/clinicalnerpt-laboratory"             
              ,r"pucpr/clinicalnerpt-medical"             
              ,r"pucpr/clinicalnerpt-pharmacologic"             
              ,r"pucpr/clinicalnerpt-procedure"             
              ,r"pucpr/clinicalnerpt-quantitative"             
              ,r"pucpr/clinicalnerpt-sign"             
              ,r"pucpr/clinicalnerpt-therapeutic"             
]



@app.route('/', methods=['GET'])
def index():
    print ("iniciando")
    print(MODELS_DIR)
    return render_template('index.html')

@app.route("/entidades")
def ner():
    SentencasSomente = request.args.get('word')
    SentencasSomente = SentencasSomente.replace('.','.#')
    sentencas = SentencasSomente.split('#')
    print(sentencas)
    result = predict.predictALLSentenceBERT(sentencas,MODELS_DIR)
    return jsonify(result)

#app.run()
#app.run(host="0.0.0.0", port=int("5000"), debug=False)#map port to 5000
#process.env.PORT

import os
port = int(os.environ.get("PORT", 5000))

app.run(host="0.0.0.0", port=port, debug=False)#map port to 5000
