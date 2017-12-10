from polyglot.text import Text, Word
import string
from scipy.stats import chi
import numpy as np
import pandas as pd
import sys

class Classifier():

    def __init__(self, inputs, N):
        self.labels = [inputs.index(i)%N for i in inputs]
        self.inputs = inputs
        self.num_intents = N
        self.all_words = sum(inputs, [])

    def compare_intent_freqs_to_general_freqs(self, pval = 0.05):

        predictors = {}

        for i in range(self.num_intents):
            pseudo = 1

            # DAFUQ IS THIS THROWING AN ERROR ON 2ND ITERATION?!! REEEEEEEEE
            # intent_indices = [y for y, x in enumerate(self.labels) if i == x]
            labs = np.array(self.labels)
            intent_indices = list(np.where(labs == i)[0])

            tr = self.inputs
            intent_inputs = [x for x in self.inputs if self.inputs.index(x) in intent_indices]
            intent_all_words = sum(intent_inputs, [])
            intent_L = float(len(intent_all_words))
            if intent_L == 0:
                continue
            intent_counts = {x: pseudo + intent_all_words.count(x) for x in set(self.all_words)}

            non_intent_indices = [y for y, x in enumerate(self.labels) if x != i]
            non_intent_inputs = [x for x in self.inputs if self.inputs.index(x) in non_intent_indices]
            non_intent_all_words = sum(non_intent_inputs, [])
            non_intent_L = float(len(non_intent_all_words))
            non_intent_counts = {x: pseudo + non_intent_all_words.count(x) for x in set(self.all_words)}
            expected = {x: intent_L * (non_intent_counts[x] + intent_counts[x]) / (intent_L + non_intent_L) for x in set(self.all_words)}

            chisq = {x: ((expected[x] - intent_counts[x])**2)/expected[x] for x in set(self.all_words)}

            scores = {x: min(chi.cdf(chisq[x],1),chi.sf(chisq[x],1)) for x in set(self.all_words)}

            passed = [x for x in scores if scores[x] < pval]
            predictors[i] = passed

        return(predictors)

    def likelihood_reassign(self, preds):

        pseudo = 1

        likes = {i:[] for i in range(len(self.inputs))}
        freqs = {j:None for j in range(len(preds))}

        for j in freqs:
            # intent_indices = [self.labels.index(x) for x in self.labels if self.labels.index(x) == j]
            intent_indices = [i for i, x in enumerate(self.labels) if x == j]
            intent_inputs = [x for x in self.inputs if self.inputs.index(x) in intent_indices]
            intent_all_words = sum(intent_inputs, [])
            intent_L = float(len(intent_all_words))
            if intent_L == 0:
                continue
            # intent_freqs = {x: intent_all_words.count(x)/intent_L for x in preds[j]}
            intent_freqs = {x: (intent_all_words.count(x) + pseudo) / intent_L for x in preds[j]}

            # non_intent_indices = [self.labels.index(x) for x in self.labels if self.labels.index(x) != j]
            non_intent_indices = [i for i, x in enumerate(self.labels) if x != j]
            non_intent_inputs = [x for x in self.inputs if self.inputs.index(x) in non_intent_indices]
            non_intent_all_words = sum(non_intent_inputs, [])
            non_intent_L = float(len(non_intent_all_words))
            if non_intent_L == 0:
                continue
            non_intent_freqs = {x: (non_intent_all_words.count(x) + pseudo)/non_intent_L for x in preds[j]}

            freqs[j] = (intent_freqs, non_intent_freqs)

        # For every msg in inputs
        freqs = {k:freqs[k] for k in freqs if not freqs[k] is None}
        self.num_intents = len(freqs)

        for i in likes:
            msg = self.inputs[i]
            L = len(msg)

            # likes[self.inputs.index(msg)] = []

            # For every possible intent
            for intent in range(self.num_intents):

                # For every predictor word in intent
                for p in range(self.num_intents):
                    pred_counts = {word:msg.count(word) for word in preds[intent]}
                    # expected_counts = {word:[L*freqs[intent][k] for k in freqs[intent]] for word in preds[intent]}
                    expected_counts_intent = {word: L * freqs[intent][0][word] for word in preds[intent]}
                    expected_counts_non_intent = {word: L * freqs[intent][1][word] for word in preds[intent]}
                    chis_intent = sum([((pred_counts[word] - expected_counts_intent[word])**2)/expected_counts_intent[word] for word in preds[intent]])
                    chis_non_intent = sum([((pred_counts[word] - expected_counts_non_intent[word]) ** 2) / expected_counts_non_intent[word] for word in preds[intent]])
                    df = len(preds[intent])-1
                    score_intent = 1 - 2*min(chi.cdf(chis_intent,df),chi.sf(chis_intent,df))
                    score_non_intent = 1 - 2*min(chi.cdf(chis_non_intent,df),chi.sf(chis_intent,df))
                    likes[intent].append(score_intent/score_non_intent)
        return(likes)

    def relabel(self,likeli):
        self.labels = [np.argmax(x) for x in likeli]
        return()

    def training(self, iters = 100):
        Pv = 0.1
        for i in range(iters):
            predictors = self.compare_intent_freqs_to_general_freqs(pval = Pv)
            likelihoods = self.likelihood_reassign(predictors)
            self.relabel(likelihoods)
            Pv = Pv - 0.15*Pv
        pass

data = '/home/theo/Desktop/hakaton.csv'
with open(data) as f:
    lines = f.read().splitlines()

repl = [u'\xc8\xcc\xdf', u'\xd4\xc0\xcc\xc8\xcb\xc8\xdf', u'\xce\xd2\xd7\xc5\xd1\xd2\xc2\xce']
client = [' '.join(x.split(',')[3:]) for x in lines if x.split(',')[2] == '1']
client = client[:10000]
client = [x.translate(string.maketrans("", ""), string.punctuation + '0') for x in client]
client = [x for x in client if len(x.split(' ')) > 3]
client = [[Word(i.decode('windows-1251'), language='ru') for i in x.split() if (len(i) > 2)] for x in client]
client = [[i for i in x if i not in repl] for x in client]
client = [sum([list(i.morphemes) for i in x],[]) for x in client]

test = Classifier(client, 50)
test.training()

# polyglot download morph2.ru
