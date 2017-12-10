# LOK_chat
An attempt at improving chatbots

- frequency_analysis.py
This part of code used to analyse frequency of words in given phrases, but we switched it off.
Now it just cleans up the phrases.

- morpheme_classifier.py
Using EM approach to discern between different intents of a client based on message morpheme content.
Needs tweaking

- clasterisation.py
performs morphemic analysis of the text, replaces all words by infinitive. Then it calculates word-counts of all wo- rds in each string therefore producing list of vectors which is used to compute distance matrix. The distance matrix is used to perform clasterization analysis and should result in a set of clusteres of closely-related words.
Unfortunately for unknown reasons it failes to build any sensible distance matrix (may be due to large amount of zeros in the array).

- chatbot.py is a sample bot performing a simple operation with text in dialoge and sending result to one of the speakers (operator). The operation is to be replaced by text analysis which woul help the operator to promote relevant products according to previous knowledge of clients intents.