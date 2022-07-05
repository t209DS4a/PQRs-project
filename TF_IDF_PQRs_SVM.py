'''This is the model used in the  '''

pip install textblob

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import sklearn
from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import metrics

import seaborn as sns
import matplotlib.pyplot as plt

from textblob import TextBlob 
import re
import numpy as np
import pandas as pd
import joblib
import mysql.connector
from mysql.connector.constants import ClientFlag




config = {
    'user': 'root',
    'password': 'Team209',
    'host': '34.135.47.175'
    'database': 'testdb'
}

# now we establish our connection
cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor(buffered=True)

#Pull the data from SQL
query = ("Select * from PQR")
cursor.execute(query)
result = cursor.fetchall()

#Convert the raw data into dataframe rows
data = pd.DataFrame(result, columns=['pqr', 'tipo'])
df = data


#Data Cleaning

df["pqr_clean"] = None
for i in range(len(df["pqr"])):
    #Leave just chars in utf-8
  df["pqr_clean"][i] = re.sub(r"[^a-zA-Z0-9 ]","",df["pqr"][i])

#Create a column where it's going to be stored the translation
df["pqr_translate"] = None
for i in range(len(df["pqr_clean"])):
  try:
    df["pqr_translate"][i] = str(TextBlob(df["pqr_clean"][i]).translate(from_lang='es', to='en'))
  except:
    ""

df["pqr_translate"] = df["pqr_translate"].str.lower()

#Address the  spanish words
conditionlist = [
    (df['tipo'] == "queja") ,
    (df['tipo'] == "peticion"),
    (df['tipo'] == "reclamo")]
choicelist = [0, 1, 2]
df["tipo_token"] = np.select(conditionlist, choicelist, default='Not Specified')


#Auxiliar tables
category_id_df = df[['tipo', 'tipo_token']].drop_duplicates()
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['tipo_token', 'tipo']].values)
id_to_category
complaints = df[["tipo","pqr_translate","tipo_token"]]



#Creates tokenizer
tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
#Fit the tokenizer data
features = tfidf.fit_transform(complaints.pqr_translate).toarray()
features

#Organize labels
labels = complaints.tipo_token
category_id_df

#Split the data between train and test
X_train, X_test, y_train, y_test = train_test_split(complaints['pqr_translate'], complaints['tipo'], random_state = 0)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

#Evaluate random forest, SVC, MultinomialNB
models = [
RandomForestClassifier(n_estimators=200, max_depth=3, random_state=0),
LinearSVC(),
MultinomialNB(),
LogisticRegression(random_state=0)]

#Batch length to run cross validation
CV = 5

#Length of the dataframe
cv_df = pd.DataFrame(index=range(CV * len(models)))

#Store the model results
entries = []

#Iterate over the models and cross validations size 
#Store the accuracy in the entries matrix
for model in models:
    model_name = model.__class__.__name__
    accuracies = cross_val_score(model, features, labels, scoring='accuracy', cv=CV)
    for fold_idx, accuracy in enumerate(accuracies):
        entries.append((model_name, fold_idx, accuracy))
        
#Store the entire results according to the size and model.
cv_df = pd.DataFrame(entries, columns=['model_name', 'fold_idx', 'accuracy'])


#Obtain just the mean of the accuracy per model
cv_df.groupby('model_name').accuracy.mean()

#The best result was SVC, then it's the model to use
model = LinearSVC()
X_train, X_test, y_train, y_test, indices_train, indices_test = train_test_split(features, labels, complaints.index, test_size=0.33, random_state=0)

#Fit the model
model.fit(X_train, y_train)

#Predict
y_pred = model.predict(X_test)

#Shows the classification metrics
print(metrics.classification_report(y_test, y_pred, 
                                    target_names=complaints['tipo'].unique()))

#Test the model
texts = ["i am student, and I need loan","I can't get the money out of the country.","i want to check my last buy, that was furnitures using credit","i'm sure that had been paid my house completely"]
text_features = tfidf.transform(texts)
predictions = model.predict(text_features)
for text, predicted in zip(texts, predictions):
  print('"{}"'.format(text))
  print("  - Predicted as: '{}'".format(id_to_category[predicted]))
  print("")


# save the model to disk
filename = 'finalized_model.sav'
joblib.dump(model, filename)

#Test the saved model
loaded_model = joblib.load(filename)
result = loaded_model.score(X_test, y_test)
print(result)

#Generate a prediction charging a  model
texts = ["i am student, and I need loan","I can't get the money out of the country.","i want to check my last buy, that was furnitures using credit","i'm sure that had been paid my house completely"]
text_features = tfidf.transform(texts)
predictions = loaded_model.predict(text_features)
for text, predicted in zip(texts, predictions):
  print('"{}"'.format(text))
  print("  - Predicted as: '{}'".format(id_to_category[predicted]))
  print("")

