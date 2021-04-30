import spacy
nlp = spacy.load("en_core_web_sm")
from conll import read_corpus_conll
from conll import evaluate
import pandas as pd

'''Reconstruct sentences from the file of Conll'''
def reconstructSentences(corpus_file):
    test_sents = read_corpus_conll(corpus_file)
    sentences_list = []
    for line in test_sents:
        string = ""
        for word in line:
            w = word[0].partition(' ')[0]
            string += " "
            string = string + w
        if (string != ' -DOCSTART-'):
            sentences_list.append(string)
    return sentences_list

''' Retokenization of the sentences using retokenize.merge of spacy and creation of list of lists
    for token.text and IOB of spacy
    mylist is the list containing tuple of token.text and token_iob_
'''
def retokenizationOfSentences(sentences_list):
    iob_type_list = []
    ent_list = []
    for sentence in sentences_list:
        doc = nlp(sentence)
        with doc.retokenize() as retokenizer:
            i = 0
            init = -1
            for token in doc:
                if (token.whitespace_ == '' and init == -1):
                    init = i
                if (token.whitespace_ == ' ' or i == len(doc) - 1) \
                        and init != -1:
                    retokenizer.merge(doc[init:i + 1])
                    init = -1
                i += 1

        list1 = []
        for token in doc:
            if (token.ent_iob_ == 'O'):
                mytuple = (token.text, token.ent_iob_)
                list1.append(mytuple)
            elif (token.ent_iob_ + "-" + token.ent_type_ == 'B-GPE' or
                token.ent_iob_ + "-" + token.ent_type_ == 'I-GPE'):
                mytuple = (token.text, token.ent_iob_ + "-LOC")
                list1.append(mytuple)
            elif (token.ent_iob_ + "-" + token.ent_type_ == 'B-LOC' or
                    token.ent_iob_ + "-" + token.ent_type_ == 'I-LOC' or
                    token.ent_iob_ + "-" + token.ent_type_ == 'B-ORG' or
                    token.ent_iob_ + "-" + token.ent_type_ == 'I-ORG' or
                    token.ent_iob_ + "-" + token.ent_type_ == 'B-MISC' or
                    token.ent_iob_ + "-" + token.ent_type_ == 'I-MISC'):
                mytuple = (token.text, token.ent_iob_ + "-" + token.ent_type_)
                list1.append(mytuple)
            elif (token.ent_iob_ + "-" + token.ent_type_ == 'B-PERSON' or
                      token.ent_iob_ + "-" + token.ent_type_ == 'I-PERSON'):
                mytuple = (token.text, token.ent_iob_ + "-PER")
                list1.append(mytuple)
            else:
                mytuple = (token.text, token.ent_iob_ + "-MISC")
                list1.append(mytuple)
        ent_list.append(list1)

        list2 = []
        for token in doc:
            if (token.ent_iob_ == 'O'):
                iob_type_list.append(token.ent_iob_)
            elif (token.ent_iob_ + "-" + token.ent_type_ == 'B-GPE' or
                  token.ent_iob_ + "-" + token.ent_type_ == 'I-GPE'):
                iob_type_list.append(token.ent_iob_ + "-LOC")
            elif (token.ent_iob_ + "-" + token.ent_type_ == 'B-LOC' or
                  token.ent_iob_ + "-" + token.ent_type_ == 'I-LOC' or
                  token.ent_iob_ + "-" + token.ent_type_ == 'B-ORG' or
                  token.ent_iob_ + "-" + token.ent_type_ == 'I-ORG' or
                  token.ent_iob_ + "-" + token.ent_type_ == 'B-MISC' or
                  token.ent_iob_ + "-" + token.ent_type_ == 'I-MISC'):
                iob_type_list.append(token.ent_iob_ + "-" + token.ent_type_)
            elif (token.ent_iob_ + "-" + token.ent_type_ == 'B-PERSON' or
                  token.ent_iob_ + "-" + token.ent_type_ == 'I-PERSON'):
                iob_type_list.append(token.ent_iob_ + "-PER")
            else:
                iob_type_list.append(token.ent_iob_ + "-MISC")
    return iob_type_list, ent_list

''' Creation of list of lists of the test file that will be used as ground truth'''
def groundTruthList(corpus_file):
    file = read_corpus_conll(corpus_file)
    gt_list1 = []
    gt_list2 = []
    list = []
    for tuple in file:
        list1 = []
        for sentence in tuple:
            frase = sentence[0]
            tupl1 = (frase.split()[0], frase.split()[3])
            list1.append(tupl1)
        if (('-DOCSTART-', 'O') not in list1):
            gt_list2.append(list1)

    for tuple_list in file:
        list1 = []
        for sentence in tuple_list:
            frase = sentence[0]
            if(frase.split()[0] != '-DOCSTART-'):
                gt_list1.append(frase.split()[3])
    return gt_list1, gt_list2

'''Evaluation using the evaluate function from conll'''
def evaluation(retokenized_list, gt_list):

    results = evaluate(retokenized_list, gt_list)

    pd_tbl = pd.DataFrame().from_dict(results, orient='index')
    pd_tbl.round(decimals=3)
    return pd_tbl

def isInChunk(entity_text, chunk_list):
    for chunk in chunk_list:
        if (entity_text in chunk):
            return chunk
    return ''

def entityGroup(sentence):
    doc = nlp(sentence)

    tuple_list = []
    for ent in doc.ents:
        tupl = ()
        tupl = (ent.text, ent.label_)
        tuple_list.append(tupl)

    chunk_list = []
    chunk_dict = {}
    for chunk in doc.noun_chunks:
        chunk_list.append(chunk.text)
        chunk_dict[chunk.text] = []

    dict = {}
    for entita in tuple_list:
        chunk_text = isInChunk(entita[0], chunk_list)
        if(chunk_text == ''):
            chunk_text = entita[0]
            chunk_dict[chunk_text] = []
        chunk_dict[chunk_text].append(entita[1])
    list = []

    for item in chunk_dict.items():
        if (item[1]):
            list.append(item[1])
    return list

def mostFrequent(final_list, n):
    tag_dict = {}
    final_list2 = final_list
    for list in final_list:
        for group in list:
            t = tuple(group)
            if (len(t) > 1):
                tag_dict[t] = 0
    for list2 in final_list2:
        for group2 in list2:
            t2 = tuple(group2)
            if(len(t2) > 1):
                tag_dict[t2] += 1
    return(dict(sorted(tag_dict.items(), key=lambda item: item[1], reverse=True)[:n]))

def fixSegmentation(sentence):

    doc = nlp(sentence)

    ent_iob_list = [t.ent_iob_ for t in doc] #list of iob tags
    ent_type_list = [t.ent_type_ for t in doc] #list of entity type
    ent_list = [t.text for t in doc.ents] #list of entities text
    tok_list =[token for token in doc] #list of tokens

    for token in doc:
        if (token.dep_ == 'compound' and token.head.ent_type_ != ''):
            ent_type_list[token.i] = token.head.ent_type_
            for entity in ent_list:
                if token.head.text in entity:
                    if (token.i < token.head.i):
                        ent_iob_list[token.i] = "B"
                    else:
                        ent_iob_list[token.i] = "I"
    list = []
    for a, b, c in zip(tok_list, ent_iob_list, ent_type_list ):
        if(c != ''):
            tupl = (a.text, b+"-"+c)
        else:
            tupl = (a.text, b)
        list.append(tupl)
    return list