import os
import json
import pickle
import random
from datetime import datetime, timedelta

import nltk
import numpy
import tensorflow
import tflearn
from nltk.stem.lancaster import LancasterStemmer

try:
    nltk.data.find('tokenizers/punkt/english.pickle')
except LookupError:
    nltk.download('punkt_tab')


class ChatBot:
    def __init__(self, train=False, accuracy=0.8, files="files", message_default = "Sorry, I don't understand"):
        self.accuracy = accuracy
        self.message_default = message_default

        self.DIR_INTENTS = f"{files}/intents.json"
        self.DIR_PICKLE = f"{files}/training_models/data.pickle"
        self.DIR_MODEL = f"{files}/training_models/model.tflearn"


        self.words = []
        self.labels = []
        self.docs_x = []
        self.docs_y = []
        self.training = []
        self.output = []
        self.model = None

        self.stemmer = LancasterStemmer()

        self._dir_check()

        # if os.path.isfile(self.DIR_INTENTS):
        with open(self.DIR_INTENTS) as file:
            self.data = json.load(file)

        if train:
            self.train()
        else:
            try:
                self.load()
            except:
                self.train()
        
    def _dir_check(self):
        folder = os.path.dirname(self.DIR_PICKLE)
        if folder:
            os.makedirs(folder, exist_ok=True)

        if not os.path.exists(self.DIR_INTENTS):
            current_dir = os.path.dirname(os.path.realpath(__file__))
            file_intents = os.path.join(current_dir, 'intents.json')
            with open(file_intents, 'r') as ref_file:
                intents = json.load(ref_file)
            os.makedirs(os.path.dirname(self.DIR_INTENTS), exist_ok=True)
            with open(self.DIR_INTENTS, 'w') as json_file:
                json.dump(intents, json_file, indent=4)

    def load(self):
        with open(self.DIR_PICKLE, "rb") as f:
            self.words, self.labels, self.training, self.output = pickle.load(f)

        self._load_model()
        self.model.load(self.DIR_MODEL)

    def _load_model(self):
        tensorflow.compat.v1.reset_default_graph()

        net = tflearn.input_data(shape=[None, len(self.training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(self.output[0]), activation="softmax")
        net = tflearn.regression(net)

        self.model = tflearn.DNN(net)

    def train(self):
        for intent in self.data["intents"]["main"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                self.words.extend(wrds)
                self.docs_x.append(wrds)
                self.docs_y.append(intent["tag"])

            if intent["tag"] not in self.labels:
                self.labels.append(intent["tag"])

        self.words = [self.stemmer.stem(w.lower()) for w in self.words if w not in "?"]
        self.words = sorted(list(set(self.words)))

        self.labels = sorted(self.labels)

        out_empty = [0 for _ in range(len(self.labels))]

        for x, doc in enumerate(self.docs_x):
            bag = []

            wrds = [self.stemmer.stem(w) for w in doc]

            for w in self.words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[self.labels.index(self.docs_y[x])] = 1

            self.training.append(bag)
            self.output.append(output_row)

        self.training = numpy.array(self.training)
        self.output = numpy.array(self.output)

        with open(self.DIR_PICKLE, "wb") as f:
            pickle.dump((self.words, self.labels, self.training, self.output), f)

        self._load_model()

        self.model.fit(self.training, self.output, n_epoch=1000, batch_size=8, show_metric=True)
        self.model.save(self.DIR_MODEL)

    def _bag_of_words(self, s, words):
        bag = [0 for _ in range(len(words))]

        s_words = nltk.word_tokenize(s)
        s_words = [self.stemmer.stem(word.lower()) for word in s_words]

        for se in s_words:
            for i, w in enumerate(words):
                if w == se:
                    bag[i] = 1

        return numpy.array(bag)

    def __time_day_part(self):
        nowTime = datetime.now()
        hours = nowTime.hour
        if 4 <= hours < 12:
                return "morning"
        elif 12 <= hours < 18:
            return "afternoon"
        else:
            return "evening"

    def _answer_fill(self, message):
        message = message.replace("[time_day_part]", self.__time_day_part())
        return message

    def ask(self, message, need_accuracy=False):
        results = self.model.predict([self._bag_of_words(message, self.words)])[0]
        results_index = numpy.argmax(results)
        results_max = results[results_index]
        tag = self.labels[results_index]

        # Default respon
        out_message = self.message_default
        out_accuracy = float(0)

        if results_max > self.accuracy:
            for tg in self.data["intents"]["main"]:
                if tg['tag'] == tag:
                    responses = tg['responses']

            try:
                out_message = self._answer_fill(random.choice(responses))
                out_accuracy = float(results_max)
            except:
                print("Error: can't get responses")

        if need_accuracy:
            return out_message, out_accuracy
        else:
            return out_message

    def _clean_text(self, text):
        text = text.replace("!", "")
        text = text.replace("?", "")
        return text.lower()

    def run_loop(self, need_accuracy=False):
        print("----------------------------------------------")
        print("Start talking with the bot!")
        print("----------------------------------------------")
        while True:
            inp = input("You: ")
            if inp.lower() == "quit":
                break

            answer = self.ask(inp, True)
            if need_accuracy:
                print(f"Bot: {answer[0]} => {answer[1]}")
            else:
                print(f"Bot: {answer[0]}")

if __name__ == "__main__":
    bot = ChatBot(False, 0.1)
    bot.run_loop()