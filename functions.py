import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud


#  Functions for reading files :
def read_vocabulary(file = 'vocabulary.txt'):
    with open(file, 'r', encoding = 'utf-8') as f:
        rows = f.read().split('\n') # split the file into rows
        # dictionary structure: {word : word_id}
        vocabulary = {int(row.split('\t')[1]) : row.split('\t')[0] for row in rows[:-1]}
    return vocabulary

def read_tfid(file = 'tfid.csv'):
    tfid = {}
    #structure tfid --> {annoucement_id : [word_id1, word_id2, ....]}
    with open(file, 'r', encoding = 'utf-8') as f:
        rows = f.read().split('\n') # split the file into rows
        for row in rows:
            row_elements = row.split('\t')
            tfid[row_elements[0]] = row_elements[1:]
    return tfid

# Functions for clustering part:

def plot_inertia(dataset_scores, info):
    x = list(dataset_scores.keys())
    y = list(dataset_scores.values())
    fig = plt.figure()
    plt.plot(x,y, color = "red")
    plt.plot(x[2], y[2], 'o', ms=30, mec='b', mfc='none', mew=2)
    plt.annotate('Optimal number of clusters',
                 xy=(x[2]+2, 2*y[2]), xytext=(x[2]+5, 4*y[2]),
                 arrowprops = dict(facecolor='black', shrink=0.05))
    plt.title("Elbow-Method for" + info, color="blue")
    plt.xlabel("k - Number of clusters")
    plt.ylabel("Inertia")
    plt.show()
    fig.savefig("optimal-clusters-" + info + ".png")

# Functions for WORDCLOUDs :

def get_words_for_annoucements(tfid, announcements_list):
    word_container = []
    for id_ann in announcements_list:
        word_id_list = tfid[str(id_ann)]
        word_container.extend([vocabulary[int(word_id)] for word_id in word_id_list[1:]])
    return word_container

def generate_wordcloud(text, name):
    wordcloud = WordCloud(max_font_size=50, background_color="white").generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    wordcloud.to_file(name +".png")
