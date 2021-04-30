from utils import reconstructSentences, retokenizationOfSentences, groundTruthList, evaluation
from sklearn.metrics import classification_report

'''         Main        '''

corpus_file = 'test.txt'
sentences_list = reconstructSentences(corpus_file)

retokenized_list1, retokenized_list2 = retokenizationOfSentences(sentences_list)
print("----------------------------------------------------------------------------------------------------------")
gt_list1, gt_list2 = groundTruthList(corpus_file)
print(classification_report(gt_list1, retokenized_list1))

pandas_table = evaluation(gt_list2, retokenized_list2)
print(pandas_table)

