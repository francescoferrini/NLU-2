from utils import groundTruthList, reconstructSentences, fixSegmentation, evaluation

'''     Main      '''

sentence = "Apple's Steve Jobs died in 2011 in Palo Alto, California."
print(fixSegmentation(sentence))

''' #For running the code on a corpus file
sentences_list = reconstructSentences('test.txt')
fixed_list = []
for sentence in sentences_list:
    fix = fixSegmentation(sentence)
    fixed_list.append(fix)
print(fixed_list)'''