# -*- coding: utf-8 -*-
"""Untitled2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/RiaGusmita/Indonesian-POS-Tagger-using-Flair/blob/main/EvaluateFlairForPOSTagging.ipynb
"""

from google.colab import drive
drive.mount('/content/gdrive', force_remount=True)

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/gdrive/'My Drive'/Colab/Indonesian-POS-Tagger-using-Flair/

!pip install flair

from flair.data_fetcher import NLPTaskDataFetcher, NLPTask
from flair.embeddings import TokenEmbeddings, WordEmbeddings, StackedEmbeddings, BertEmbeddings
from typing import List

from flair.data import Corpus
from flair.datasets import ColumnCorpus

# define columns
columns = {0: 'text', 1: 'pos'}

# this is the folder in which train, test and dev files reside
data_folder = '/content/gdrive/My Drive/Colab/Indonesian-POS-Tagger-using-Flair/Datasets/IDN Tagged Corpus/'

# init a corpus using column format, data folder and the names of the train, dev and test files
corpus: Corpus = ColumnCorpus(data_folder, columns,
                              train_file='train.01.txt',
                              test_file='test.01.txt',
                              dev_file='dev.01.txt')

tag_type = 'upos'

# 3. make the tag dictionary from the corpus
tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
#print(tag_dictionary.idx2item)

# 4. initialize embeddings
embedding_types: List[TokenEmbeddings] = [
    WordEmbeddings('id-crawl'),
    WordEmbeddings('id'),
    #WordEmbeddings('glove'),
    #BertEmbeddings('bert-base-multilingual-cased')
]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

# 5. initialize sequence tagger
from flair.models import SequenceTagger
tagger: SequenceTagger = SequenceTagger(hidden_size=256,
                                        embeddings=embeddings,
                                        tag_dictionary=tag_dictionary,
                                        tag_type=tag_type,
                                        use_crf=True)

from flair.trainers import ModelTrainer

trainer: ModelTrainer = ModelTrainer(tagger, corpus)

# 7. start training
trainer.train('resources/taggers/fromIDNTaggedCorpus',
              learning_rate=0.1,
              mini_batch_size=32,
              max_epochs=15)

from flair.data import Sentence

sentence = Sentence('saya dan dia kemarin pergi ke pasar bersama untuk membeli jeruk')
tag_pos = SequenceTagger.load('resources/taggers/example-universal-pos/best-model.pt')
tag_pos.predict(sentence)
print(sentence.to_tagged_string())

from tqdm import tqdm 
fileName = "/content/gdrive/MyDrive/Colab/Indonesian-POS-Tagger-using-Flair/Datasets/newFormatTrain.txt"
data = open(fileName,'r')
txt = data.read()

### converting text in form of list of (words with their tags) ###
txt = txt.split('\n')

### removing DOCSTART (document header)
txt = [x for x in txt if x != '-DOCSTART- -X- -X- O']
### check ###
for i in range(10):
  print(txt[i])
  print('-'*10)

### Extracting Sentences ###
# Initialize empty list for storing words
words = []
# initialize empty list for storing sentences #
corpus = []

for i in tqdm(txt):
  ## if blank sentence encountered ##
  if i =='':
    ## previous words form a sentence ##
    corpus.append(' '.join(words))
    ## Refresh Word list ##
    words = []
  else:
   ## word at index 0 ##
    words.append(i.split()[0])

for i in range(10):
  print(corpus[i])
  print('-'*10)

### Extracting POS ###
# Initialize empty list for storing word pos
w_pos = []
#initialize empty list for storing sentence pos #
POS = []
for i in tqdm(txt):
  ## blank sentence = new line ##
  if i =='':
    ## previous words form a sentence POS ##
    POS.append(' '.join(w_pos))
    ## Refresh words list ##
    w_pos = []
  else:
    ## pos tag from index 1 ##
    w_pos.append(i.split()[1])

for i in range(10):
  print(corpus[i])
  print(POS[i])

### Removing blanks form sentence and pos ###
corpus = [x for x in corpus if x!= '']
POS = [x for x in POS if x!= '']

### Check ###
for i in range(10):
  print(corpus[i])
  print(POS[i])

pos = SequenceTagger.load('resources/taggers/example-universal-pos/best-model.pt')
#for storing pos tagged string#
f_pos = []
## for every sentence ##
for i in tqdm(corpus):
  sentence = Sentence(i)
  pos.predict(sentence)
  ## append tagged sentence ##
  f_pos.append(sentence.to_tagged_string())

for i in range(10):
  print(f_pos[i])
  print(corpus[i])

import re

### Extracting POS tags ###
## in every sentence by index ##
for i in tqdm(range(len(f_pos))):
  ## for every words ith sentence ##
  for j in corpus[i].split():
    ## replace that word from ith sentence in f_pos ##
    f_pos[i] = str(f_pos[i]).replace(j,"",1)

  ## Removing < > symbols ##
  for j in  ['<','>']:
    f_pos[i] = str(f_pos[i]).replace(j,"")

    ## removing redundant spaces ##
    f_pos[i] = re.sub(' +', ' ', str(f_pos[i]))
    f_pos[i] = str(f_pos[i]).lstrip()

for i in range(10):
  print(f_pos[i])
  print(corpus[i])

### Removing Symbols and redundant space ###

## in every sentence by index ##
for i in tqdm(range(len(corpus))):
  # Removing Symbols #
  corpus[i] = re.sub('[^a-zA-Z]', ' ', str(corpus[i]))
  POS[i] = re.sub('[^a-zA-Z]', ' ', str(POS[i]))
  f_pos[i] = re.sub('[^a-zA-Z]', ' ', str(f_pos[i]))  

  ## Removing HYPH SYM (they are for symbols) ##
  f_pos[i] = str(f_pos[i]).replace('HYPH',"")
  f_pos[i] = str(f_pos[i]).replace('SYM',"")
  POS[i] = str(POS[i]).replace('SYM',"")
  POS[i] = str(POS[i]).replace('HYPH',"")                       

  ## Removing redundant space ##
  POS[i] = re.sub(' +', ' ', str(POS[i]))
  f_pos[i] = re.sub(' +', ' ', str(f_pos[i]))
  corpus[i] = re.sub(' +', ' ', str(corpus[i]))

for i in range(1000):
  print('corpus   '+corpus[i])
  print('actual   '+POS[i])  
  print('flair    '+f_pos[i])
  print('-'*50)

### EVALUATION FUNCTION ###
def eval(x,y):
  # correct match #
  count = 0
  #Total comparisons made# 
  comp = 0
  ## for every sentence index in dataset ##
  for i in range(len(x)):
    ## if the sentence length match ##
    if len(x[i].split()) == len(y[i].split()):
      ## compare each word ##
      for j in range(len(x[i].split())):
        if x[i][j] == y[i][j] :
          ## Match! ##
          count = count+1
          comp = comp + 1
        else:
          comp = comp + 1
  return (count/comp)*100

print("Flair Score ", eval(POS,f_pos))

