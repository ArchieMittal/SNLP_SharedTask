from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk

tokens = []
num=0
with open('corpus.txt', 'rb') as lines:
	for line in lines:
		num+=1
		for token in line.split():
			tokens.append(token)

words = list(set(tokens))
#print (num)
#print ('\n')
def features(word, index):
    """ word: [c1, c2, ...], index: the index of the word """
    return {
        'character': word[index],
        'is_first': index == 0,
        'is_last': index == len(word) - 1,
        'prev_char-1': '' if index < 2 or len(word) < 2 else word[index-2],
        'prev_char': '' if index == 0 else word[index - 1],
        'next_char': '' if index == len(word) - 1 else word[index + 1],
        'next_char+1': '' if len(word) < 2 or index > len(word) - 3 else word[index + 2]
    }

def untag(tagged_word):
    return [c for c, t in tagged_word]

def createTags(token):
	tags = []
	for character in token:
		tag = (character.lower(), character)
		tags.append(tag)
	return tags

tagged_words = map(createTags, words)

# Split the dataset for training and testing
cutoff = int(.8 * len(tagged_words))
training_words = tagged_words[:cutoff]
test_words = tagged_words[cutoff:]

#print len(training_words)
#print len(test_words)

def transform_to_dataset(tagged_words):
    X, y = [], []

    for tagged in tagged_words:
        for index in range(len(tagged)):
            X.append(features(untag(tagged), index))
            y.append(tagged[index][1])

    return X, y
 
X, y = transform_to_dataset(training_words)

clf = Pipeline([
    ('vectorizer', DictVectorizer(sparse=False)),
    ('classifier', DecisionTreeClassifier(criterion='entropy'))
])

clf.fit(X, y)

X_test, y_test = transform_to_dataset(test_words)
print "Accuracy:", clf.score(X_test, y_test)
def decoder(word):
    decoded_word = []
    tags = clf.predict([features(word, index) for index in range(len(word))])
    return ''.join(tags)
    

with open('testinput.txt', 'r') as fin, open("testoutput.txt", "w") as fout: #Removing stopwords
	for line in fin:
		tokens=word_tokenize(line)
		for w in tokens:
			o_word=decoder(w)
			fout.writelines(o_word + ' ')
		fout.writelines('\n')
			
			
			
			
