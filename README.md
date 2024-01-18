# Machine Translation for Pandemic Response

This repository contains the code to use the Microsoft Azure and Google Cloud translation services to translate the full TICO-19 dataset from each language into English, and calculate the BLEU scores for each. My collaborator ran the same translations from English to the target languages, her results (without code) are also included here. As the TICO-19 dataset is large, running this script on the full dataset takes significant time. Therefore, toy files containing the first 10 sentences of data for each language have been provided here, in order to conveniently demonstrate the code functionality. The full dataset with all sentences can be downloaded [here](https://tico-19.github.io/).

## Project Overview

Are currently available machine translation (MT) systems ready for pandemic response? This paper aims to answer this question by evaluating the performance of two existing systems against the TICO-19 dataset, a corpus of content related to the COVID-19 pandemic translated into 38 languages. Two MT systems (Google and Microsoft) were used for translation, both from English to the target languages and from the target languages to English. Three different automatic evaluation metrics were used and analyzed (BLEU, BERTscore, and Comet), and a limited subset of translations were scored using human evaluation. In addition, we provide an analysis based on language status and region.

## Running the scripts

### Azure and Google Cloud API Access
Running each script requires an account with access to each respective API. To run azure_translate.py, you will need to add your account key and endpoint to the code in lines 31 and 32, and your location to line 37. To run google_translate.py, save the JSON file containing your Google key in the same directory as the script, and update the code on line 19. If using alternative methods of access, simply comment out line 19 altogether.

### Directory Structure
Each script iterates through a directory containing the TICO-19 files to access and translate the data. The output translations are the saved in the folders microsoft_output and google_output respectively. The script will produce one tsv file per translated languages, and one file containing the BLEU scores for each language (bleu_scores.txt). Given python's directory iteration requirements, empty folders for the output files must be created beforehand, and the folder containing the original dataset needs to be named correctly. All folders must be in the same directory as the script. Therefore, empty, correctly named output folders have been included in this repository. Overall, ensure your directory structure directly mimics the one here to successfully run the code.

**Note:** The files contained in the folder tico_files are toy files, not the full dataset.

**Note 2:** If you run the code more than once, delete the bleu_scores.txt file beforehand. Otherwise, results from subsequent runs will be appended to the bottom of the existing file rather than overwriting them. This is not an issue for the output tsv files, which will just be overwritten.

## Directory Contents
+ **azure_translate.py** --> Script to translate TICO-19 sentences using Microsoft Azure
+ **google_translate.py** --> Script to translate TICO-19 sentences using Microsoft Azure
+ **tico_files** --> toy Tico-19 files that can be used to demo the code
+ **microsoft_output** --> empty folder where output files from azure_translate.py will be saved upon running the code
+ **google_output** --> empty folder where output files from azure_translate.py will be saved upon running the code
+ **Results** --> results obtained from translating the full TICO-19 dataset which are presented in the final report. This also includes results from translating from English into each target language (and corresponding BLEU scores), provided my collaborator. Finally, BERT and COMET scores for translations in both directions are included here - the code for these was run exclusively by my collaborator due to compatibility issues.
+ **final_report** --> The final paper outlining results and findings for this project.
