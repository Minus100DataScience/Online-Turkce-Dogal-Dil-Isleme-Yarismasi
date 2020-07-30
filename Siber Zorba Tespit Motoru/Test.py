import joblib
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def most_frequent(liste):
    counter = 0
    num = liste[0]
    for i in liste:
        curr_frequency = liste.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            num = i
    return num


def user(textin):
    if textin == "EXIT":
        exit()
    else:
        textin = pre_process(textin)
        classi = classify(textin)
        return classi


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


def pre_process(text):
    text = text.lower()  # turning text to lowercase
    text = nltk.re.sub('[^a-zİıŞşÇçÜüĞğÖö]+', ' ', text)  # removing punctuations and numbers from text
    stop_words = set(stopwords.words('turkish'))
    word_tokens = word_tokenize(text)
    text = repeats(text)
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    # returning processed text list to readText function go up
    return text


def classify(text):
    text = [text]
    loaded_model_lsvc = joblib.load('Models/LSVC_finalized_model.sav')
    loaded_model_lr = joblib.load('Models/LR_finalized_model.sav')
    loaded_model_sgd = joblib.load('Models/SGD_finalized_model.sav')

    result_lsvc = loaded_model_lsvc.predict(text)
    result_lr = loaded_model_lr.predict(text)
    result_sgd = loaded_model_sgd.predict(text)

    resultlist = [result_lr, result_lsvc, result_sgd]
    res = most_frequent(resultlist)
    return res[0]


def add_tested(yon, text, res):
    if yon == "Y":
        with open("Datasets/tweetset.csv", 'a', encoding="windows-1254") as content_file:
            string = (res + "," + text)
            content_file.write(string + "\n")
    else:
        with open("Datasets/tweetset.csv", 'a', encoding="windows-1254") as content_file:
            if res == "Pozitif":
                string = ("Negatif" + "," + text)
                content_file.write(string + "\n")
            else:
                string = ("Pozitif" + "," + text)
                content_file.write(string + "\n")
