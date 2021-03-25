#!/usr/bin/env python
# coding: utf-8


from transformers import BertTokenizer, BertForTokenClassification
from transformers import AutoTokenizer, AutoModelForTokenClassification

from transformers import pipeline

def predictALLSentenceBERT(sentencas,MODELS_DIR):
    print('entrou')
    print(sentencas)
    
    tags_values = [
    ["O","Finding","Finding","Finding","Finding","Finding"]
    #,["Chemical&Drugs","O","Chemical&Drugs","Chemical&Drugs","Chemical&Drugs","Chemical&Drugs"]
    #,["DiagnosticProcedure","DiagnosticProcedure","O","DiagnosticProcedure","DiagnosticProcedure","DiagnosticProcedure"] 
    #,["O","Procedures","Procedures","Procedures","Procedures","Procedures"]
    #,["DiseaseorSyndrome","DiseaseorSyndrome","DiseaseorSyndrome","O","DiseaseorSyndrome","DiseaseorSyndrome"]
    #,["Disorders","Disorders","Disorders","Disorders","O","Disorders"]
    #,["HealthCare","HealthCare","HealthCare","HealthCare","O","HealthCare"]
    #,["Laboratory","O","Laboratory","Laboratory","Laboratory","Laboratory"]
    #,["Medical","Medical","O","Medical","Medical","Medical"]
    #,["O","Pharmacologic","Pharmacologic","Pharmacologic","Pharmacologic","Pharmacologic"]
    #,["Quantitative","Quantitative","O","Quantitative","Quantitative","Quantitative"]
    #,["Sign","Sign","O","Sign","Sign","Sign"]
    #,["Therapeutic","Therapeutic","O","Therapeutic","Therapeutic","Therapeutic"]
    ]
    
    predictedModels = []
    all_tokens=[]
    all_labels=[]
    for i in range(len(MODELS_DIR)):
        try:   
            MODEL_DIR = MODELS_DIR[i]
            print(MODEL_DIR)
            tag_values = tags_values[i]
            #print(tag_values)
            
            model = AutoModelForTokenClassification.from_pretrained(MODEL_DIR)
            tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
            
            #tokenizer = BertTokenizer.from_pretrained("pucpr/clininalnerpt-diagnostic")
            #model = BertForTokenClassification.from_pretrained("pucpr/clininalnerpt-diagnostic")

            nlp = pipeline("ner", model=model, tokenizer=tokenizer)

            ner_results = nlp(sentencas)
            print(ner_results)
           
            predictedModels.append(ner_results)
        
        except:
            print('Erro BERT (frase muito grande provavelmente)')
            raise
    
        #print(predictedModels)
    
    for k in range(0,len(predictedModels)):
        tokens=[]
        labels=[]
        print(predictedModels[k])
        
        for x in range(len(predictedModels[k])):
            dic1=predictedModels[k][x]
            #print(dic1)
            palavra = dic1.get('word')
            if palavra.startswith("##"):
                tokens[-1]=tokens[-1] + palavra[2:]
            else:
                labels.append(dic1.get('entity'))
                tokens.append(palavra)
        all_tokens.append(tokens)
        all_labels.append(labels)
    
    texto="{"

    #for x in range(len(all_tokens)):
    for i, token in enumerate(all_tokens[0]):

        palavra = token

        texto = texto + "'"+palavra+"':{"
        temLabel=0
        #print(palavra)
        #listaLabelsPalavra=[]
        for x in range(len(all_labels)):
            tag_values =tags_values[x] 
            #print(x)
            #print(tag_values)
            #listaLabelsPalavra.append(all_labels[i][x])
            label= all_labels[x][i]
            #print(label)
            num_label= label[6:len(label)]
            label_string = tag_values[int(num_label)]
            #print(label_string)
            if label_string != 'O':
                texto = texto + "'"+label_string+"',"
                temLabel=1            
        if temLabel==0:
            texto = texto + "'O',"
        texto = texto[:len(texto)-1]
        texto = texto + "},"
    texto = texto[:len(texto)-1]

    texto=texto+"}"
    
    print(texto)
    return texto

