import sys
sys.path.append('../../..')
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class DataCleaning:
    """This class have with purpose clean the comments. Remove words, emoji, links, etc"""
    def __init__(self):
        self.all_comments = list()
        self.tokens_list = list()
        self.vocabulary = set()
        self.all_words = list()
        self.emoticons_str = r"""
                    (?:
                        [:=;] # Eyes
                        [oO\-]? # Nose (optional)
                        [D\)\]\(\]/\\OpP] # Mouth
                    )"""
        self.regex_str = [
            self.emoticons_str,
            r'<[^>]+>',  # HTML tags
            r'(?:@[\w_]+)',  # @-mentions
            r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
            r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
            r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
            r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
            r'(?:[\w_]+)',  # other words
            r'(?:\S)'  # anything else
        ]
        self.tokens_re = re.compile(r'(' + '|'.join(self.regex_str) + ')', re.VERBOSE | re.IGNORECASE)
        self.emoticon_re = re.compile("["u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)

    def steps_control_to_cleaning_dataset(self, comments):
        for i in comments:
            self.de_emojify(i)

        for i in range(0, len(self.tokens_list)):
            self.tokens_list[i] = self.lemma(self.tokens_list[i])
            self.all_comments.append(' '.join(self.tokens_list[i]))

        self.vocabulary = self.lemma(self.vocabulary)

    def de_emojify(self, comment):
        """This method remove the emoji from comments. The emojis ins't important to make the
        predictions in our model. This process is executed with encode process,
        because emojis are not compatible with ascii encode"""

        tokens = self.pre_process(comment)
        tokens = self.remove_stop_words(tokens)

        tokens_aux = list()
        for i in tokens:
            try:
                i.encode('ascii')
                self.vocabulary.add(i)
                tokens_aux.append(i)
            except UnicodeEncodeError:
                break

        self.tokens_list.append(tokens_aux)

    def pre_process(self, my_string):
        """Receive a string(comment) and return the token that corresponding a string received."""

        tokens = self.tokenize(my_string)
        tokens = [token if self.emoticon_re.search(token) else token.lower() for token in tokens]
        return tokens

    def tokenize(self, s):
        return self.tokens_re.findall(s)

    def lemma(self, tokens):
        """Lemma is the process to reduce the word to your root word.
        This method receive a token and make a lemmatization about each word in token list."""

        new_tokens = set()
        lem = WordNetLemmatizer()
        for i in tokens:
            lemma = lem.lemmatize(i)
            new_tokens.add(lemma)
            self.all_words.append(lemma)
        return new_tokens

    def remove_stop_words(self, tokens):
        """This method remove the stop words of each token. Stop Words are the words that aren't important
        to make our predictions. This occur because this words don't expressive good or bad feelings."""

        stop = stopwords.words('english') + list(string.punctuation) + ['...', '<', ':']
        return [term.lower() for term in tokens
                if term not in stop
                and not term.startswith(('#', '@'))
                and not term.isnumeric()]

