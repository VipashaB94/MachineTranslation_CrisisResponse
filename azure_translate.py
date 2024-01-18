#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 12:59:22 2023

@author: vipashabansal
"""

import csv, os, requests, uuid, json
import pandas as pd
from sacrebleu.metrics import BLEU, CHRF, TER

#Calculate the BLEU Scores using completed translations for the language compared
#with the translations provided by the TICO-19 dataset.
def metrics(tico_en, mt_en):
    refs = [tico_en]
    hyps = mt_en
    
    bleu = BLEU()
    bleu_score = str(bleu.corpus_score(hyps, refs))
    
    bleu2 = bleu_score.split()
    
    return bleu2[2]

#Access Azure and Translate File
def translate(df, lang, orig_code):
    #UPDATE HERE WITH YOUR AZURE ACCESS INFORMATION
    
    # Add your key and endpoint here
    key = "ADD YOUR KEY HERE" #Update with your key
    endpoint = "ADD ENDPOINT HERE" #Update with endpoint

    # location, also known as region.
    # required if you're using a multi-service or regional (not global) resource.
    # It can be found in the Azure portal on the Keys and Endpoint page.
    location = "westus" #Update with your location

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': lang,
        'to': ['en']
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    
    #Translate file
    fin_trans = []
    
    sents = []
    
    for item in df["targetString"]:
        sents.append(item)
    
    for line in sents:
        body = [{'text': line}]


        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        
        result = json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
        res_dict = json.loads(result)
        
        #get translation from the dictionary (res_dict)
        fin_res = res_dict[0]["translations"][0]["text"]
        #printing translations helps ensure code is actively running and not frozen
        print(fin_res)
        fin_trans.append(fin_res)
        
    #add translations to df as a new column
    df["en-mt"] = pd.Series(fin_trans)
        
    #write dataframe to a file
    filepath = ""
    if lang == "ti":
        filepath = "microsoft_output/{}_en.tsv".format(orig_code)
    else:
        filepath = "microsoft_output/{}_en.tsv".format(lang)
    df.to_csv(filepath, sep="\t")
    
    return df["sourceString"], df["en-mt"]





supported_languages = ["am", "ar", "bn", "es-419", "fa", "fr", "hi", "id", "km", "ku", "mr", "ms", "my", "ne", "prs", "ps", "pt-br", "ru", "so", "sw", "ta", "ti", "ti-er", "ur", "zh", "zu"]

#Iterate through the TICO-19 files
directory = 'tico_files'
files = []

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        if f.endswith("tsv"):
            files.append(f)

for file in files:
    data = pd.read_table(file, usecols=["sourceLang", "targetLang", "sourceString", "targetString"])
    lang = data.loc[3, 'targetLang']
    
    from_lang = ""
    
    tico_en = []
    mt_en = []
    
    #Ensure from_lang matches microsoft language codes, which don't always perfectly match TICO-19 codes
    if lang.lower() in supported_languages:
        if lang.lower() == "ti-er":
            from_lang = "ti"
        elif lang.lower() == "es-419":
            from_lang = "es"
        elif lang.lower() == "zh":
            from_lang = "zh-Hans"
        else:
            from_lang = lang.lower()
        
        #Run translation
        en_hum, en_mt = translate(data, from_lang, lang)
        
        for item in en_hum:
            tico_en.append(str(item))
        for item in en_mt:
            mt_en.append(str(item))
            
        #Run metrics to calculate and save BLEU scores
        bleu = metrics(tico_en, mt_en)
        print("{} {} \n".format(from_lang, bleu))
        with open("microsoft_output/bleu_scores.txt", "a") as bleu_file:
            bleu_file.write("{} {} \n".format(lang, bleu))
            
            
            
            
            