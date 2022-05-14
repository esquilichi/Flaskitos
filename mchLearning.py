import json
import os
from subprocess import call

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import tree, linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score, mean_squared_error
from sklearn.tree import export_graphviz


def calcular_cliclados(a, b):
    if b != 0:
        return a / b
    else:
        return 0


if __name__ == '__main__':
    # Path to json file we are loading
    path_etiquetado = os.getcwd() + '/machinelearning/train.csv'
    path_predecir = os.getcwd() + '/machinelearning/users_IA_predecir.json'

    col = ['emails_phishing_recibidos', 'emails_phishing_clicados', 'vulnerable']
    col2 = ['emails_phishing_recibidos', 'emails_phishing_clicados']
    # Read json file and load it into variable of pd
    # Training json loaded
    with open(path_etiquetado, 'r') as f:
        datos = pd.read_csv(f, names=col)
    # This json is not tagged, used to predict
    with open(path_predecir, 'r') as f:
        predecir = pd.read_csv(f, names=col2)

    """
    RANDOM FOREST 
    """

    x_train = datos.drop('vulnerable', axis=1)
    y_train = datos['vulnerable']

    # Split data for testing and for predicting
    X_train, X_test, Y_train, y_test = train_test_split(x_train, y_train, test_size=0.5)

    rf_clf = RandomForestClassifier(criterion='entropy')
    rf_clf.fit(X_train, Y_train)

    # Predict data on test part
    y_predict = rf_clf.predict(X_test)

    # Accuracy
    print("Accuracy %.3f" % accuracy_score(y_test, y_predict))

    """
    LINEAL REGRESSION
    """
    regr = linear_model.LinearRegression()
    regr.fit(X_train, Y_train)
    y_predict = regr.predict(X_test)
    print("Mean squared error: %.2f" % mean_squared_error(y_test,
                                                          y_predict))

    """
    EXPORT GRAPHVIZ DOT AND PNG FILES OF DECISION TREES
    """
    """
    for i in range(len(rf_clf.estimators_)):
        # print(i)
        estimator = rf_clf.estimators_[i]
        export_graphviz(estimator,
                        out_file='machinelearning/gráficos/random_forest.dot',
                        feature_names=['Emails Recibidos', 'Emails Clickados'],
                        class_names=['No vulnerable', 'Vulnerable'],
                        rounded=True, proportion=False,
                        precision=2, filled=True)
        call(['dot', '-Tpng', 'machinelearning/gráficos/random_forest.dot',
              '-o', 'machinelearning/gráficos/png/tree'+str(i)+'.png', '-Gdpi=600'])
    """

