from utils import isInChunk, entityGroup, reconstructSentences, mostFrequent, evaluation, groundTruthList


'''    Main    '''
corpus_file = 'test.txt'
sentences_list = reconstructSentences(corpus_file)
final_list = []
for sentence in sentences_list:
    list1 = entityGroup(sentence)
    final_list.append(list1)

frequent_tag_dict = mostFrequent(final_list, 10)
print(frequent_tag_dict)






