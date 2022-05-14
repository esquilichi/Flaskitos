import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.exceptions import DataConversionWarning
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
import json
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=DataConversionWarning)

with open('machinelearning/users_IA_clases.json', 'r') as f:
    data_train = json.load(f)

matriz_train = [None] * len(data_train['usuarios'])
for i in range(len(data_train['usuarios'])):
    matriz_train[i] = [None] * 2


list_train = [None] * len(data_train['usuarios'])

i = 0
for usuario in range(len(data_train['usuarios'])):

    matriz_train[i][0] = data_train['usuarios'][usuario]['emails_phishing_recibidos']
    matriz_train[i][1] = data_train['usuarios'][usuario]['emails_phishing_clicados']

    list_train[i] =[data_train['usuarios'][usuario]['vulnerable']]

    i += 1

# Use only one feature
data_train_Y = list_train
data_train_X = matriz_train

# Split the data into training/testing sets
data_X_train = data_train_X[:20]

data_X_test = data_train_X[20:]

# Split the targets into training/testing sets
data_y_train = data_train_Y[:20]
data_y_test = data_train_Y[20:]

def RegresionLinear():
    res = []
    for i in data_X_test:
        res.append([i[1] / i[0]])
    print(res)
    print(data_y_test)

    # Create linear regression object
    regr = linear_model.LinearRegression()

    print(data_X_test)
    # Train the model using the training sets
    regr.fit(data_X_train, data_y_train)

    # Make predictions using the testing set
    data_y_pred = regr.predict(data_X_test)

    # The coefficients
    print("Coefficients: \n", regr.coef_)
    # Este es el valor donde corta el eje Y (en X=0)
    print('Independent term: \n', regr.intercept_)
    # The mean squared error
    print("Mean squared error: %.2f" % mean_squared_error(data_y_test, data_y_pred))
    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(data_y_test, data_y_pred))

    user_pred = []

    for valor in data_y_pred:
        if valor < 0.5:
            user_pred.append(0)
        else:
            user_pred.append(1)

    print("Accuracy in Regresion Linear: %.2f" % accuracy_score(data_y_test, user_pred))

    # Plot outputs
    plt.scatter(res, data_y_test, color="black")
    plt.plot(0.02 * np.array(res) + regr.intercept_, res, color="blue", linewidth=3)


    plt.xlabel("Probabilidad de click")
    plt.ylabel("Vulnerable no (0) si (1)")
    plt.xticks()
    plt.yticks()
    plt.show()


def decisionTree():
    from sklearn import tree

    regr = tree.DecisionTreeClassifier()
    # Train the model using the training sets
    regr.fit(data_X_train, data_y_train)

    # Make predictions using the testing set
    data_y_pred = regr.predict(data_X_test)

    user_pred = []
    for valor in data_y_pred:
        if valor < 0.5:
            user_pred.append(0)
        else:
            user_pred.append(1)

    print("Accuracy in DecisionTree: %.2f" % accuracy_score(data_y_test, user_pred))

    tree.plot_tree(regr, filled=True, fontsize=10, rounded = True, precision=2, proportion=False)
    plt.show()

def forest():
    from sklearn.ensemble import RandomForestClassifier
    from sklearn import tree

    regr = RandomForestClassifier(max_depth=2, random_state=0, n_estimators=9)
    # Train the model using the training sets
    regr.fit(data_X_train, data_y_train)

    # Make predictions using the testing set
    data_y_pred = regr.predict(data_X_test)

    user_pred = []
    for valor in data_y_pred:
        if valor < 0.5:
            user_pred.append(0)
        else:
            user_pred.append(1)

    print("Accuracy in Random Forest: %.2f" % accuracy_score(data_y_test, user_pred))

    for i in range(len(regr.estimators_)):
        estimator = regr.estimators_[i]
        tree.plot_tree(estimator, filled=True, fontsize=10, rounded = True, precision=2, proportion=False)
        plt.show()


RegresionLinear()
decisionTree()
forest()
