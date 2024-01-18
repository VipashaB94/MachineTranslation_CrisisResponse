#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 12:54:13 2023

@author: vipashabansal
"""

import csv, os
import pandas as pd
from sacrebleu.metrics import BLEU, CHRF, TER
from google.cloud import translate_v2 as translate
import six

#To run this code, put your google key JSON file in the same directory as this
#script, and then change 'google_key.json' to match that filename. If you are
#using environment variables or other acess methods, simply comment out the line
#of code below instead.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_key.json'


#Calculate the BLEU Scores using completed translations for the language compared
#with the translations provided by the TICO-19 dataset.
def metrics(tico_en, mt_en):
    refs = [tico_en]
    hyps = mt_en
    
    bleu = BLEU()
    bleu_score = str(bleu.corpus_score(hyps, refs))
    
    bleu2 = bleu_score.split()
    
    return bleu2[2]

#Translate file
def translation(df, lang, orig_code):
    
    translate_client1 = translate.Client()
    
    fin_trans = []
    
    sents = []
    for item in df["targetString"]:
        sents.append(item)
    
    for line in sents:
        if isinstance(line, six.binary_type):
            line = line.decode("utf-8")
        
        result = translate_client1.translate(line, source_language=lang, target_language="en")
        fin_res = result['translatedText']
        #printing translations helps ensure code is actively running and not frozen
        print(fin_res)
        
        fin_trans.append(fin_res)
    
    #add translations to df as a new column
    df["en-mt"] = pd.Series(fin_trans)
    
    #write dataframe to a file
    filepath = ""
    if lang == "ti":
        filepath = "google_output/{}_en.tsv".format(orig_code)
    else:
        filepath = "google_output/{}_en.tsv".format(lang)
    df.to_csv(filepath, sep="\t")
    
    return df["sourceString"], df["en-mt"]

    

#Returns list of languages supported by Google Cloud Translation
def list_languages():
    """Lists all available languages."""

    translate_client = translate.Client()

    results = translate_client.get_languages()

    for language in results:
        print(u"{name} ({language})".format(**language))

#list_languages()

supported_languages = ["am", "ar", "bn", "ckb", "es-419", "fa", "fr", "ha", "hi", "id", "km", "ln", "mr", "ms", "my", "ne", "om", "ps", "pt-br", "ru", "so", "sw", "ta", "ti", "ti-er", "ur", "zh", "zu", "rw", "ku"]

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
    
    #Ensure from_lang matches Google language codes, which don't always perfectly match TICO-19 codes
    if lang.lower() in supported_languages:
        if lang.lower() == "ti-er":
            from_lang = "ti"
        elif lang.lower() == "es-419":
            from_lang = "es"
        elif lang.lower() == "pt-br":
            from_lang = "pt"
        else:
            from_lang = lang.lower()
        
        #Run translation
        en_hum, en_mt = translation(data, from_lang, lang)
        
        for item in en_hum:
            tico_en.append(str(item))
        for item in en_mt:
            mt_en.append(str(item))
        
        #Run metrics to calculate and save BLEU scores
        bleu = metrics(tico_en, mt_en)
        print("{} {} \n".format(lang, bleu))
        with open("google_output/bleu_scores.txt", "a") as bleu_file:
            bleu_file.write("{} {} \n".format(lang, bleu))

    
    
    