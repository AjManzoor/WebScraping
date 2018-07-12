import pandas as pd
import math

doc_a = ["the cat sat on my face", "the dog sat on my bed", "the rat sat on my head", "the elephant sat on my bike"]

def calc_tfidf(doc_a, stop_word_list):
    bow_a = []
    for x in range(len(doc_a)):
        bow_a.append(doc_a[x].split())

    word_set = set()

    for i in range(len(bow_a)):
        word_set = word_set.union(set(bow_a[i]))

    word_dict_a = []

    for x in range(len(doc_a)):
        word_dict_a.append(dict.fromkeys(word_set,0)) 


    for x in range(len(bow_a)):
        for word in bow_a[x]:
            word_dict_a[x][word] +=1



    def compute_TF(word_dict, bow):
        tf_dict = {}
        bow_count = len(bow)
        for word, count in word_dict.items():
            tf_dict[word] = count / float(bow_count)
        return tf_dict

    tf_bow_a = []

    for m in range(len(word_dict_a)):
        tf_bow_a.append(compute_TF(word_dict_a[m], bow_a[m]))
        

    def compute_IDF(doc_list):
        idf_dict = {}
        N = len(doc_list)

        idf_dict = dict.fromkeys(doc_list[0].keys(),0)
        for doc in doc_list:
            for word, val in doc.items():
                if val > 0:
                    idf_dict[word] +=1

        for word, val in idf_dict.items():
            idf_dict[word] = math.log(N/float(val))

        return idf_dict
        

    idfs = compute_IDF(word_dict_a)

    def compute_TFIDF(tf_bow, idfs):
        tfidf = {}
        for word, val in tf_bow.items():
            tfidf[word] = val * idfs[word]
        return tfidf

    tfidf_bow_a = []
    for u in range(len(tf_bow_a)):
        tfidf_bow_a.append(compute_TFIDF(tf_bow_a[u], idfs))
        

    tfidf_set_a = set()
    final_tfidf = {}

    for r in range(len(tfidf_bow_a)):
        for word , val in tfidf_bow_a[r].items():
            if not word.isdigit() and word not in stop_word_list:
                if word not in final_tfidf :
                        final_tfidf[word] = val
                else:
                    try:
                        if final_tfidf[word] < val:
                            final_tfidf[word] = val
                    except:
                        print(word)
                        print('error key')        

    return final_tfidf

