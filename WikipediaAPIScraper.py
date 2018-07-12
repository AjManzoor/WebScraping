import os
import sys

script_paths = ["/TFIDF2.py", "Neo4j.py"]

for path in range(len(script_paths)):
    sys.path.append(os.path.abspath(script_paths[path]))

import wikipediaapi
import wikipedia
import string
import operator
import math
import numpy
import TFIDF2 as tf_idf
import Neo4j

#print(wikipedia.summary('Coventry Transport Museum'))


def stop_word_list():
    stop_word_array2 = []
    F = open('stopwords.txt','r') 
    stop_word_array = F.readlines()
    for word in stop_word_array:
        word = word.replace('\n', '')
        stop_word_array2.append(word)

    return stop_word_array2

def activities_list():
    activites_array2 = []
    F = open('activities.txt','r') 
    activities_array = F.readlines()
    for word in activities_array:
        word = word.replace('\n', '')
        activites_array2.append(word)

    return activites_array2

def print_sections(sections,title_array, level=0):
    for s in sections:
        #print(s.title)
        title_array.append(s.title)
        #print(title_array)
        print_sections(s.sections, title_array, level + 1)
    return title_array

def clean_text(dirty_text):
        try:
            translator = str.maketrans(' ',' ', string.punctuation)
            dirty_text= dirty_text.translate(translator)
            dirty_text = dirty_text.replace('\n', ' ')
            dirty_text = dirty_text.lower()
            return dirty_text
        except:
            print(' error')

def extract_key_word(sentence):
    words = ['club','soceity','volunteering','for', 'the ', 'coventry']
    sentence = sentence.lower()   
    for word in words:
        if word in sentence:
            sentence = sentence.replace(word, '')
            
    sentence = sentence.strip()
    return sentence
    
    


def generate_tags(activity, stop_word_list):

    stop_word_list = stop_word_list 
    data = {}
    all_documents = []
    all_documents
    
    page_search = activity

    wiki_wiki = wikipediaapi.Wikipedia('en')

    page_py = wiki_wiki.page(page_search)
    try:
        search_item  = wikipedia.page(page_search)
    except wikipedia.exceptions.DisambiguationError as e:
        print(e.options[0])
        search_item  = wikipedia.page(e.options[0])
        activity = e.options[0]
        
    sections_array = print_sections(page_py.sections, [])
    #print(sections_array)
    


    #print(wikipedia.summary('Coventry Transport Museum'))
    cleaned_text= clean_text(wikipedia.summary(activity))
    all_documents.append(cleaned_text)

    for section in range(len(sections_array)):        
        cleaned_text = clean_text(search_item.section(sections_array[section]))
        if cleaned_text:
            all_documents.append(cleaned_text)
       
    #print(all_documents)
    calculated_tfidf = tf_idf.calc_tfidf(all_documents, stop_word_list)

    sorted_data = reversed(sorted(calculated_tfidf.items(), key=operator.itemgetter(1)))

    Neo4j.add_activity_to_graph(activity)

    x = 0
    for items in sorted_data:
        if x < 50:
            #print(items)
            Neo4j.add_tag_to_graph(items[0])
            Neo4j.add_relationship_to_graph(activity, items[0] ,items[1])
            x+=1
        else:
            break
    
    
activity_list = activities_list()
for activity in activity_list:
    key_word = extract_key_word(activity)
    print(key_word)
    generate_tags(key_word, stop_word_list())
print('done')


