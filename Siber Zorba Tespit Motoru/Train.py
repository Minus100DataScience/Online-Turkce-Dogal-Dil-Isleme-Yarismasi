import warnings
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import joblib
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.model_selection import KFold
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer


def read_text(csv):
    datas = csv  # dataset that holds the texts

    field = ["Paylaşım"]  # the columns that we are going to read

    textlist = []  # list that we are going to hold texts

    # reading csv file encoding for turkish characters
    df = pd.read_csv(datas, skipinitialspace=True, usecols=field, encoding="windows-1254")
    for text in df.Paylaşım:
        textlist.append(text)  # reading texts to list

    textlist = pre_process(textlist)  # sending list to preprocess function to clean text

    return textlist


def repeats(text):
    size_of_word = len(text)
    repeat_count = 1
    firsts_index = 0
    i = 0
    while i < (size_of_word-1):
        if text[i] == text[i+1]:
            firsts_index = i - repeat_count + 1
            repeat_count = repeat_count + 1
            i = i+1
        elif repeat_count > 2:
            j = 0
            while j < repeat_count-1:
                text = text[:firsts_index] + text[firsts_index+1:]
                j = j + 1
            size_of_word = size_of_word - (repeat_count - 1)
            repeat_count = 1
            i = firsts_index
            i = i + 1
        else:
            i = i + 1
    if repeat_count > 2:
        j = 0
        while j < repeat_count - 1:
            text = text[:firsts_index] + text[firsts_index + 1:]
            j = j + 1
    return text


def cities(cits):
    city = []
    for citi in cits:
        city.append(str(citi).lower())
    # print(city)
    return city


def names(nam):
    namez = []
    for name in nam:
        namez.append(str(name))
    # print(city)
    return namez


def pre_process(text_list):

    month_list = ["ocak", "şubat", "mart", "nisan", "mayıs", "haziran", "temmuz", "ağustos", "eylül", "ekim", "kasım", "aralık"]
    day_list = ["pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar"]
    smaller = []  # holding processed texts
    for text in text_list:
        text = text.lower()  # turning text to lowercase
        text = nltk.re.sub('[^a-zİıŞşÇçÜüĞğÖö]+', ' ', text)  # removing punctuations and numbers from text
        stop_words = set(stopwords.words('turkish'))
        # print(stop_words)
        text = repeats(text)
        word_tokens = word_tokenize(text)
        filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                if len(w) > 1:
                    if w not in month_list and w not in day_list:
                        filtered_sentence.append(w)
        textimiz = lis_to_string(filtered_sentence)
        # print(textimiz)
        smaller.append(textimiz)

    # returning processed text list to readText function go up
    return smaller


def lis_to_string(s):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in s:
        str1 += ele
        str1 += " "

        # return string
    return str1


def newset(corp, oldcsv, newcsv):

    field = ["Tip"]
    # reading csv file encoding for turkish characters
    df = pd.read_csv(oldcsv, skipinitialspace=True, usecols=field, encoding="windows-1254")
    print(df.Tip.value_counts())
    with open(newcsv, 'a', encoding="windows-1254") as content_file:
        for i in range(len(corp)):
            string = (df.Tip[i] + "," + corp[i])
            content_file.write(string + "\n")
            i += 1


def vector(newcsv):
    df = pd.read_csv(newcsv, encoding='windows-1254')
    stop_words = set(stopwords.words('turkish'))
    vectorizer = TfidfVectorizer(min_df=10, max_df=0.95, sublinear_tf=True, norm='l2',
                                 ngram_range=(1, 3), encoding='windows-1254', stop_words=stop_words, analyzer='word')
    models = [('LR', LogisticRegression(solver='newton-cg', multi_class='multinomial')),
              ('LSVC', LinearSVC()),
              ('SGD', SGDClassifier(tol=1e-3, penalty='l2'))]
    for name, model in models:
        print(name)
        k_fold(vectorizer, model, df, name)


def k_fold(vectorizer, model, data, name):
    pipeline = Pipeline([('vect', vectorizer),
                         ('chi', SelectKBest(chi2, k="all")),
                         ('clf', model)])
    kf = KFold(n_splits=15, shuffle=True)
    scores = []
    for train_index, test_index in kf.split(data):
        train_text = data.iloc[train_index]['Paylaşım'].values.astype('U')
        train_y = data.iloc[train_index]['Tip'].values.astype('U')

        test_text = data.iloc[test_index]['Paylaşım'].values.astype('U')
        test_y = data.iloc[test_index]['Tip'].values.astype('U')

        model = pipeline.fit(train_text, train_y)
        predictions = model.predict(test_text)
        with warnings.catch_warnings():
            warnings.filterwarnings(action='once')
            score = accuracy_score(test_y, predictions)
            print(score)
            scores.append(score)
    filename = 'Models/'+name + '_finalized_model.sav'
    joblib.dump(model, filename)
    print("Score: " + str(sum(scores) / len(scores)))


def main():
    csv = "Datasets/tweetset.csv"
    corpus = read_text(csv)
    newcsv = "Datasets/newcsv.csv"
    file = open(newcsv, 'w')
    file.write("Tip" + "," + "Paylaşım" + "\n")
    file.close()
    newset(corpus, csv, newcsv)
    vector(newcsv)


main()
