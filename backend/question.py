import nltk
from sklearn.svm import LinearSVC
import collections
from nltk.metrics import precision, recall
from nltk.corpus import nps_chat
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

class isQuestion():
    def __init__(self):
        posts = nps_chat.xml_posts()
        features = self.__get_feature_set(posts)
        new_features=[]
        for j in features: 
            label=j[1]
            if(label!='whQuestion' and label!='ynQuestion'):
                label='NotQuestion'
            new_features.append((j[0],label))
        features=new_features
        #self.classifier = self.naiveBayes(features)
        #self.classifier = self.DecisionTree(features)
        #self.classifier = self.MaxentClassifier(features)
        self.classifier = self.SVM(features)
        #self.classifier = self.KNN(features)
        
    def __get_feature_set(self, posts):
        feature = []
        for post in posts:
            post_text = post.text            
            features = {}
            words = nltk.word_tokenize(post_text)
            for word in words:
                features['contains({})'.format(word.lower())] = True
            feature.append((features, post.get('class')))
        return feature
    
    def naiveBayes(self, feature_set):
        training_size = int(len(feature_set) * 0.1)
        train_set, test_set = feature_set[training_size:], feature_set[:training_size]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        print("accuracy = ","{0:.5f}".format(nltk.classify.accuracy(classifier, test_set)))
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)
        for i, (feats, label) in enumerate(test_set):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)
        print("\t\tWH-Question\t\tYN-Question\t\tNotQuestion\n")
        print( 'Precision:\t', "{0:.5f}".format(precision(refsets['whQuestion'], testsets['whQuestion'])), "\t\t", "{0:.5f}".format(precision(refsets['ynQuestion'], testsets['ynQuestion'])), "\t\t", "{0:.5f}".format(precision(refsets['NotQuestion'], testsets['NotQuestion'])))
        print( 'Recall:   \t', "{0:.5f}".format(recall(refsets['whQuestion'], testsets['whQuestion'])), "\t\t", "{0:.5f}".format(recall(refsets['ynQuestion'], testsets['ynQuestion'])), "\t\t", "{0:.5f}".format(recall(refsets['NotQuestion'], testsets['NotQuestion'])))
        return classifier
    
    def MaxentClassifier(self, feature_set):
        training_size = int(len(feature_set) * 0.1)
        train_set, test_set = feature_set[training_size:], feature_set[:training_size]
        classifier = nltk.MaxentClassifier.train(train_set,max_iter=15)
        print("accuracy = ","{0:.5f}".format(nltk.classify.accuracy(classifier, test_set)))
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)

        for i, (feats, label) in enumerate(test_set):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)
        print("\t\tWH-Question\t\tYN-Question\t\tNotQuestion\n")
        print( 'Precision:\t', "{0:.5f}".format(precision(refsets['whQuestion'], testsets['whQuestion'])), "\t\t", "{0:.5f}".format(precision(refsets['ynQuestion'], testsets['ynQuestion'])), "\t\t", "{0:.5f}".format(precision(refsets['NotQuestion'], testsets['NotQuestion'])))
        print( 'Recall:   \t', "{0:.5f}".format(recall(refsets['whQuestion'], testsets['whQuestion'])), "\t\t", "{0:.5f}".format(recall(refsets['ynQuestion'], testsets['ynQuestion'])), "\t\t", "{0:.5f}".format(recall(refsets['NotQuestion'], testsets['NotQuestion'])))
        return classifier
    
    def DecisionTree(self, feature_set):
        training_size = int(len(feature_set) * 0.1)
        train_set, test_set = feature_set[training_size:], feature_set[:training_size]
        classifier = nltk.classify.SklearnClassifier(DecisionTreeClassifier(max_depth=200)).train(train_set)
        print("accuracy = ","{0:.5f}".format(nltk.classify.accuracy(classifier, test_set)))
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)
        for i, (feats, label) in enumerate(test_set):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)
        print("\t\tWH-Question\t\tYN-Question\t\tNotQuestion\n")
        print( 'Precision:\t', "{0:.5f}".format(precision(refsets['whQuestion'], testsets['whQuestion'])), "\t\t", "{0:.5f}".format(precision(refsets['ynQuestion'], testsets['ynQuestion'])), "\t\t", "{0:.5f}".format(precision(refsets['NotQuestion'], testsets['NotQuestion'])))
        print( 'Recall:   \t', "{0:.5f}".format(recall(refsets['whQuestion'], testsets['whQuestion'])), "\t\t", "{0:.5f}".format(recall(refsets['ynQuestion'], testsets['ynQuestion'])), "\t\t", "{0:.5f}".format(recall(refsets['NotQuestion'], testsets['NotQuestion'])))
        return classifier
    
    def KNN(self, feature_set):
        training_size = int(len(feature_set) * 0.1)
        train_set, test_set = feature_set[training_size:], feature_set[:training_size]
        classifier = nltk.classify.SklearnClassifier(KNeighborsClassifier()).train(train_set)
        print("accuracy = ","{0:.5f}".format(nltk.classify.accuracy(classifier, test_set)))
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)
        for i, (feats, label) in enumerate(test_set):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)
        print("\t\tWH-Question\t\tYN-Question\t\tNotQuestion\n")
        print( 'Precision:\t', "{0:.5f}".format(precision(refsets['whQuestion'], testsets['whQuestion'])), "\t\t", "{0:.5f}".format(precision(refsets['ynQuestion'], testsets['ynQuestion'])), "\t\t", "{0:.5f}".format(precision(refsets['NotQuestion'], testsets['NotQuestion'])))
        print( 'Recall:   \t', "{0:.5f}".format(recall(refsets['whQuestion'], testsets['whQuestion'])), "\t\t", "{0:.5f}".format(recall(refsets['ynQuestion'], testsets['ynQuestion'])), "\t\t", "{0:.5f}".format(recall(refsets['NotQuestion'], testsets['NotQuestion'])))
        return classifier
    
    def SVM(self, feature_set):
        training_size = int(len(feature_set) * 0.1)
        train_set, test_set = feature_set[training_size:], feature_set[:training_size]
        classifier = nltk.classify.SklearnClassifier(LinearSVC()).train(train_set)
        print("accuracy = ","{0:.5f}".format(nltk.classify.accuracy(classifier, test_set)))
        refsets = collections.defaultdict(set)
        testsets = collections.defaultdict(set)
        for i, (feats, label) in enumerate(test_set):
            refsets[label].add(i)
            observed = classifier.classify(feats)
            testsets[observed].add(i)
        print("\t\tWH-Question\t\tYN-Question\t\tNotQuestion\n")
        print( 'Precision:\t', "{0:.5f}".format(precision(refsets['whQuestion'], testsets['whQuestion'])), "\t\t", "{0:.5f}".format(precision(refsets['ynQuestion'], testsets['ynQuestion'])), "\t\t", "{0:.5f}".format(precision(refsets['NotQuestion'], testsets['NotQuestion'])))
        print( 'Recall:   \t', "{0:.5f}".format(recall(refsets['whQuestion'], testsets['whQuestion'])), "\t\t", "{0:.5f}".format(recall(refsets['ynQuestion'], testsets['ynQuestion'])), "\t\t", "{0:.5f}".format(recall(refsets['NotQuestion'], testsets['NotQuestion'])))
        return classifier
    
    def predict_question(self, text):
        words = nltk.word_tokenize(text.lower())        
        if '?' in text:
            return 1
        features = {}
        for word in words:
            features['contains({})'.format(word.lower())] = True            
        prediction_result = self.classifier.classify(features)
        if prediction_result == 'whQuestion' or prediction_result == 'ynQuestion':
            return 1
        return 0  # return the list of questions

def Question_detection(transcript):
    result = []
    obj = isQuestion()
    for i in transcript:
        if(obj.predict_question(i) == 1):
            result.append(i)
    return result

# Example usage:
transcript = ["Hello everyone", "How are you" ,"What is the weather like today?", "This is not a question."]
questions = Question_detection(transcript)
print("Detected Questions:")
for q in questions:
    print(q)
