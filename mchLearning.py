import json
import os
from subprocess import call

import graphviz
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import tree, linear_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
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

    print(len(x_train))
    regression_train = x_train[15:]
    regression_test = x_train[:15]

    regression_train_y = y_train[15:]
    regression_test_y = y_train[:15]
    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Train the model using the training sets
    regr.fit(regression_train, regression_train_y)
    # Make predictions using the testing set
    predicted_y = regr.predict(regression_test)
    # The mean squared error
    print("Mean squared error: %.2f" % mean_squared_error(regression_test_y, predicted_y))

    plt.scatter(np.arange(0,len(regression_test),1), regression_test_y, color="black")
    plt.plot(0.02 * np.array(regression_test) + regr.intercept_, predicted_y, color="blue", linewidth=3)
    plt.xticks(())
    plt.yticks(())
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
