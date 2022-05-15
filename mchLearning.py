import json
import os
from subprocess import call

import graphviz
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import tree, linear_model
from sklearn.ensemble import RandomForestClassifier
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
    path_predecir = os.getcwd() + '/machinelearning/predict.csv'

    col = ['emails_phishing_recibidos', 'emails_phishing_clicados', 'vulnerable']
    col2 = ['emails_phishing_recibidos', 'emails_phishing_clicados']
    # Read json file and load it into variable of pd
    # Training json loaded
    with open(path_etiquetado, 'r') as f:
        datos = pd.read_csv(f, names=col)
    # This json is not tagged, used to predict
    with open(path_predecir, 'r') as f:
        predecir = pd.read_csv(f, names=col2)

    x_train = datos.drop('vulnerable', axis=1)
    y_train = datos['vulnerable']

    """
    DECISION TREE
    """
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x_train, y_train)

    y_predict = clf.predict(predecir)
    c = 0
    for i in y_predict:
        if i == 1:
            c += 1
    print("Decision Tree classified as vulnerable", str(c), "users")

    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = graphviz.Source(dot_data)
    dot_data = tree.export_graphviz(clf,
                                    out_file='machinelearning/gráficos/decision_tree.dot',
                                    feature_names=['Emails Recibidos', 'Emails Clickados'],
                                    class_names=['No vulnerable', 'Vulnerable'],
                                    rounded=True, proportion=False,
                                    precision=2, filled=True)
    call(['dot', '-Tpng', 'machinelearning/gráficos/decision_tree.dot',
          '-o', 'machinelearning/gráficos/decision_tree.png', '-Gdpi=600'])

    """
    RANDOM FOREST 
    """
    rf_clf = RandomForestClassifier(max_depth=2, random_state=0, n_estimators=10)
    rf_clf.fit(x_train, y_train)

    # Predict data on test part
    y_predict = rf_clf.predict(predecir)

    c = 0
    for i in y_predict:
        if i == 1:
            c += 1

    print("Random forest classified as vulnerable", str(c), "users")

    """
    LINEAL REGRESSION
    """

    with open('machinelearning/users_IA_clases.json') as file:
        data_users_entrenamiento = json.load(file)

    data_x = []
    data_y = []

    for user in data_users_entrenamiento["usuarios"]:
        data_y.append([user["vulnerable"]])
        if user["emails_phishing_recibidos"] != 0:
            data_x.append([user["emails_phishing_clicados"], user["emails_phishing_recibidos"]])
        else:
            data_x.append([0, 0])

    data_x_train = data_x[:-20]
    data_x_test = data_x[-20:]
    data_y_train = data_y[:-20]
    data_y_test = data_y[-20:]
    regr = linear_model.LinearRegression()
    regr.fit(data_x_train, data_y_train)

    m = regr.coef_
    b = regr.intercept_
    x = data_x_test

    data_y_pred = regr.predict(np.array(data_x_test))
    for i in range(0, len(data_y_pred)):
        if data_y_pred[i] < 0.5:
            data_y_pred[i] = 0
        else:
            data_y_pred[i] = 1

    print("Mean squared error: %.2f" % mean_squared_error(data_y_test, data_y_pred))
    print("Accuracy Regresión Lineal: ", accuracy_score(data_y_test, data_y_pred))


    x_real = []
    for i in x:
        if i[1] == 0:
            i[1] = 0.01
        x_real.append(i[0] / i[1])
    x = x_real

    # Plot outputs
    plt.scatter(np.array(x), np.array(data_y_test), color="black")
    plt.plot((m[0][0] * np.array(x)) + b, np.array(x))
    plt.show()



    """
    EXPORT GRAPHVIZ DOT AND PNG FILES OF DECISION TREES
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
              '-o', 'machinelearning/gráficos/png/tree' + str(i) + '.png', '-Gdpi=600'])
