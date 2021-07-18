#!/usr/bin/env python
# coding: utf-8

import torch
import numpy as np
from transformers import BertTokenizer, BertForTokenClassification, BertConfig
from transformers import AutoTokenizer, AutoModelForTokenClassification
import nltk    
from nltk import tokenize  
from transformers import pipeline

def predictBERTNER(sentencas,MODEL_DIR):
        
    model = BertForTokenClassification.from_pretrained(MODEL_DIR)
    #tokenizer = BertTokenizer.from_pretrained(MODEL_DIR, do_lower_case=True) # lower or not, this is important
    tokenizer = BertTokenizer.from_pretrained("pucpr/biobertpt-all", do_lower_case=True) # lower or not, this is important
    #config = BertConfig.from_pretrained(MODEL_DIR, num_labels=3)
    config = BertConfig.from_pretrained(MODEL_DIR)
    #print(config.id2label)
    #print(type(config.id2label))
    dic_label=config.id2label
    
    predictedModel=[]
    
    for test_sentence in sentencas:
        if not test_sentence.split():
            continue
        tokenized_sentence_subword = tokenizer.tokenize(test_sentence) #subtoken
        tokenized_sentence_subword_idx = tokenizer.convert_tokens_to_ids(tokenized_sentence_subword)
        input_ids = torch.tensor([tokenized_sentence_subword_idx])#.cuda()
        
        with torch.no_grad():
            output = model(input_ids)
        label_indices = np.argmax(output[0].to('cpu').numpy(), axis=2)

        
        # join bpe split tokens
        tokens = tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])
        new_tokens, new_labels = [], []
        for token, label_idx in zip(tokens, label_indices[0]):
            if token.startswith("##"):
                new_tokens[-1] = new_tokens[-1] + token[2:]
            else:
                new_labels.append(label_idx)
                new_tokens.append(token)
            
        FinalLabelSentence = []
        for token, label in zip(new_tokens, new_labels):
            #print(label)
            label = dic_label.get(label)
            if label == "O" or label == "X":
                FinalLabelSentence.append("O")
            else:
                FinalLabelSentence.append(label)
                
        predictedModel.append(FinalLabelSentence)
            
            
    return predictedModel

def predictALLSentenceBERT(sentencas,MODELS_DIR):
    print('entrou')
    print(sentencas)
    
    predictedModels=[]

    sentencas_tokenized = []
    for sentenca in sentencas:
        if not sentenca.split():
            continue
        #print(sentenca)
        sentencas_tokenized.append(tokenize.word_tokenize(sentenca, language='portuguese')) 

    for i in range(len(MODELS_DIR)):

        try:   

            MODEL_DIR = MODELS_DIR[i]
            print(MODEL_DIR)

            #tag_values = tags_values[i]

            #print(tag_values)
            ner_results = predictBERTNER(sentencas,MODEL_DIR)
            predictedModels.append(ner_results)

        except:
            print('Erro BERT (frase muito grande provavelmente)')
            raise
    
    print(predictedModels)


    result=''
    temLabel=0

    for i, sentenca in enumerate(sentencas_tokenized):
        if len(sentenca)<1:
            continue

        for j, token in enumerate(sentenca):
	        temLabel=0
	        result = result+'\''+token.strip()+'\':'+'{'
	        #print('"',token.strip(),'":','{')
	        for k, MODEL_DIR in enumerate(MODELS_DIR):
	                #print('"',all_tags[k][i][j].strip(),'",')
	                if predictedModels[k][i][j].strip().lower() != 'o':
	                        result = result+'\''+predictedModels[k][i][j].strip()+'\','
	                        temLabel=1    
	        #print('},')
	        if temLabel==0:
                        result = result + "'O',"
	        result = result[0:len(result)-1]
	        result = result+'},'
    result = result[0:len(result)-1]
    print(result)

    return result

