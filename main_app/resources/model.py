import csv
import pickle
from .data_cleaning import DataCleaning
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report


class Model:
    """This class is the implementation of our model. We are using the SVM model to make classification."""
    def __init__(self):
        self.x = list()
        self.y = list()

        self.x_train = list()
        self.x_test = list()
        self.y_train = list()
        self.y_test = list()

        self.data_cleaning = DataCleaning()
        self.all_comments = list()
        self.model = None

    def data_generate(self):
        """Read and process the data to train and test our model."""

        print('Making X and Y data...')
        self.data_cleaning.steps_control_to_cleaning_dataset(self.read_csv())
        self.all_comments = self.data_cleaning.all_comments

        tfconverter = TfidfVectorizer(max_features=1000, min_df=1, max_df=0.7)
        self.x = tfconverter.fit_transform(self.all_comments).toarray()

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y,
                                                                                test_size=0.2, random_state=0)

    def train_model(self):
        """The method train a model based in SVM classifier.
        This model are saved like a picklefile and can be loaded after."""

        print('Training the Model...\n')
        classifier = svm.SVC(kernel='linear')
        classifier.fit(self.x_train, self.y_train)

        with open('sentiment_classifier', 'wb') as picklefile:
            pickle.dump(classifier, picklefile)

    def load_model(self):
        with open('main_app/resources/sentiment_classifier', 'rb') as training_model:
            self.model = pickle.load(training_model)
        print('Model Loaded...')

    def make_prediction(self, comments):
        """This method receive a list of comments. This comments have been cleaned.
        In this step, this methods will be vectorized and used to make a prediction.

        The vectorization transform a list of comments in a sparse matrix. This matrix are used to
        nourish our model.
        """
        print('Make prediction...')

        tfconverter = TfidfVectorizer(max_features=1000, min_df=1, max_df=0.7)
        data = tfconverter.fit_transform(comments).toarray()
        predict = self.model.predict(data)

        return predict

    def define_metrics(self):
        y_pred = self.model.predict(self.x_test)
        matrix = confusion_matrix(self.y_test, y_pred)
        classification = classification_report(self.y_test, y_pred)
        accuracy_ = accuracy_score(self.y_test, y_pred)

        print('Confusion Matrix: ', matrix)
        print('Classification Score: ', classification)
        print('Accuracy: ', accuracy_)

    def read_csv(self):
        """Read a csv file that contains the data to make a train of model
        These data are composed of target and a text.

        The target is limited in 0 or 1. The 0 represents a bad feeling and 1
        represents a good feeling.

        The text is a lot of tweets obtained in kaggle datasets."""

        mylist = list()
        with open('main_app/resources/data/train.csv', 'r') as file:
            reader = csv.reader(file)
            try:
                for row in reader:
                    mylist.append(row[2])
                    self.y.append(row[1])
                file.close()
            except UnicodeDecodeError:
                print('Error in decode')
        return mylist
