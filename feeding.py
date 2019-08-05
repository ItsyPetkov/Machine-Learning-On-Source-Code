# Importing and organizing required packages and libraries
import pandas as pd;
from sklearn.model_selection import train_test_split;
from sklearn.metrics import confusion_matrix, classification_report;
from sklearn.preprocessing import StandardScaler;
from sklearn.ensemble import RandomForestClassifier;
from sklearn.neural_network import MLPClassifier;
from sklearn.neighbors import KNeighborsClassifier;
from sklearn.linear_model import LogisticRegression;

#Reading in all of the excel files created from preprocessing.py
dataframe2 = pd.read_csv('dataframe2.csv');
dataframe3 = pd.read_csv('dataframe3.csv');
dataframe4 = pd.read_csv('dataframe4.csv');
dataframe5 = pd.read_csv('dataframe5.csv');

dataframe2 = dataframe2.dropna(subset = ['Unnamed: 0', 'Edit_Distance', 'LoC', 'LoC_Chars',
       'LoC_Close_Bracket_Char', 'LoC_Open_Bracket_Char', 'LoC_SemiColon',
       'Replacement_Line_Chars', 'Replacement_Line_Close_Bracket_Char',
       'Replacement_Line_Open_Bracket_Char', 'Replacement_Line_SemiColon',
       'Replacing_line', 'Replacing_line_number', 'Similar_Chars',
       'Similar_Tokens']);

dataframe3 = dataframe3.dropna(subset = ['Unnamed: 0', 'Edit_Distance', 'LoC', 'LoC_Chars',
       'LoC_Close_Bracket_Char', 'LoC_Open_Bracket_Char', 'LoC_SemiColon',
       'NaN2', 'Replacement_Line_Chars', 'Replacement_Line_Close_Bracket_Char',
       'Replacement_Line_Open_Bracket_Char', 'Replacement_Line_SemiColon',
       'Replacing_line', 'Replacing_line_number', 'Similar_Chars',
       'Similar_Tokens']);

dataframe4 = dataframe4.dropna(subset=['Unnamed: 0', 'Edit_Distance', 'LoC', 'LoC_Chars',
       'LoC_Close_Bracket_Char', 'LoC_Open_Bracket_Char', 'LoC_SemiColon',
       'Replacement_Line_Chars', 'Replacement_Line_Close_Bracket_Char',
       'Replacement_Line_Open_Bracket_Char', 'Replacement_Line_SemiColon',
       'Replacing_line', 'Replacing_line_number', 'Similar_Chars',
       'Similar_Tokens']);

dataframe5 = dataframe5.dropna(subset=['Unnamed: 0', 'Edit_Distance', 'LoC', 'LoC_Chars',
       'LoC_Close_Bracket_Char', 'LoC_Open_Bracket_Char', 'LoC_SemiColon',
       'Replacement_Line_Chars', 'Replacement_Line_Close_Bracket_Char',
       'Replacement_Line_Open_Bracket_Char', 'Replacement_Line_SemiColon',
       'Replacing_line', 'Replacing_line_number', 'Similar_Chars',
       'Similar_Tokens']);

#Function used for creating class labels
def labelCreation(dataframe):
    labels = [];
    index = dataframe['LoC'].index.values;
    for i in range(len(index)):
        if str(dataframe.iloc[i]['Unnamed: 0']) == str(dataframe.iloc[i]['Replacing_line_number']):
            labels.append('1');
        else:
            labels.append('0');
    return labels;

#Picking features for training
def features(dataframe):
    X = dataframe[['Similar_Chars','Similar_Tokens','Edit_Distance','LoC_SemiColon','Replacement_Line_SemiColon','LoC_Open_Bracket_Char',
       'Replacement_Line_Open_Bracket_Char','LoC_Close_Bracket_Char','Replacement_Line_Close_Bracket_Char']];
    return X;

#Training and splitting the data
#X_train, X_test, Y_train, Y_test = train_test_split(features(dataframe = dataframe2), labelCreation(dataframe = dataframe2), test_size=0.2);
#X_train, X_test, Y_train, Y_test = train_test_split(features(dataframe = dataframe3), labelCreation(dataframe = dataframe3), test_size=0.2);
X_train, X_test, Y_train, Y_test = train_test_split(features(dataframe = dataframe4), labelCreation(dataframe = dataframe4), test_size=0.2);
#X_train, X_test, Y_train, Y_test = train_test_split(features(dataframe = dataframe5), labelCreation(dataframe = dataframe5), test_size=0.2);

#Scalling is added in order to get the optimized result
sc = StandardScaler();
X_train = sc.fit_transform(X_train);
X_test = sc.transform(X_test);

#Feeding the data into a k -  neighbors classifier
knn = KNeighborsClassifier(n_neighbors = 1);
knn.fit(X_train, Y_train);
pred_knn = knn.predict(X_test);

#Let's see how well the model performed
print(classification_report(Y_test, pred_knn));
print(confusion_matrix(Y_test, pred_knn));

#Feeding the data into a logistic regression model
logreg = LogisticRegression();
logreg.fit(X_train, Y_train);
pred_logreg = logreg.predict(X_test);

#Let's see how well the model performed
print(classification_report(Y_test, pred_logreg));
print(confusion_matrix(Y_test, pred_logreg));

#Feeding the data into a random forest classifier model
rfc = RandomForestClassifier(n_estimators = 200);
rfc.fit(X_train, Y_train);
pred_rfc = rfc.predict(X_test);

#Let's see how well the model performed
print(classification_report(Y_test, pred_rfc));
print(confusion_matrix(Y_test, pred_rfc));

#Feeding the data into a neural network model
mlpc=MLPClassifier(hidden_layer_sizes=(11,11,11), max_iter=500);
mlpc.fit(X_train, Y_train);
pred_mlpc = mlpc.predict(X_test);

#Let's see how well the model performed
print(classification_report(Y_test, pred_mlpc));
print(confusion_matrix(Y_test, pred_mlpc));