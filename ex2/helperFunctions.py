import numpy as np
import matplotlib.pyplot as plt
from pandas import Series, DataFrame


def plotData(X, y, theta=None):
    """
    Plots the data points X and y into a new figure.
    With + for the positive examples and o for the negative examples.
    X is assumed to be a m x 2 DataFrame and y a m length Series.
    """

    f = plt.figure()
    p = plt.scatter(X[y == 0][0], X[y == 0][1], marker='o', c='y', label='Y = 0')
    plt.scatter(X[y == 1][0], X[y == 1][1], marker='+', s=30, label='Y = 1')
    p.axes.yaxis.label.set_text('Variable 2')
    p.axes.xaxis.label.set_text('Variable 1')

    if theta is not None:
        if np.size(theta) == 3:
            # Linear case is easy
            l = plt.Line2D([20, -1/theta[2]*(theta[1]*20+theta[0])],
                           [-1/theta[1]*(theta[2]*20+theta[0]), 20],
                           color='black', label='Decision boundary')
            p.axes.add_line(l)
        else:
            # Use a grid.
            evalGrid = np.zeros([50, 50])
            uu = np.linspace(-1.0, 1.5, 50)
            vv = np.linspace(-1.0, 1.5, 50)
            for i, u in enumerate(uu):
                for j, v in enumerate(vv):
                    evalGrid[i, j] = np.dot(mapFeatureArray(np.array([[u, v]]), degree=6),
                                            theta)[0]
            plt.contour(uu, vv, evalGrid.T, [0])

    plt.legend(loc='upper right')

    f.show()

    return f


def mapFeature(X, degree=1):
    """
    Take X, an m x 2 DataFrame, and return a numpy array with more features,
    including all degrees up to degree.
    1, X1, X2, X1^2, X2^2, X1*X2, X1*X2^2, etc.
    """

    m, n = np.shape(X)

    if not n == 2:
        raise ValueError('mapFeature supports input feature vectors of length 2, not %i' % n)

    out = np.ones([1, m])

    for totalPower in xrange(1, degree+1):
        for x1Power in xrange(0, totalPower+1):
            out = np.append(out, [X[0]**(totalPower-x1Power) * X[1]**x1Power], axis=0)

    return out.T


def mapFeatureArray(X, degree=1):
    """
    Take X, an m x 2 np.array, and return a numpy array with more features,
    including all degrees up to degree.
    1, X1, X2, X1^2, X2^2, X1*X2, X1*X2^2, etc.
    A factor of ~10 faster than the DateFrame version.
    """

    m, n = np.shape(X)

    if not n == 2:
        raise ValueError('mapFeature supports input feature vectors of length 2, not %i' % n)

    out = np.ones([1, m])

    for totalPower in xrange(1, degree+1):
        for x1Power in xrange(0, totalPower+1):
            out = np.append(out, [[X[0][0]**(totalPower-x1Power) * X[0][1]**x1Power]], axis=0)

    return out.T


def sigmoid(z):
    """
    Compute sigmoid functoon
    Compute the sigmoid of each value of z (z can be a matrix, vector, or scalar).
    Accepts a scalar object, numpy array, Series, or DataFrame.
    """

    g = 1 / (1 + np.exp(-1*z))

    return g


def costFunction(theta, X, y):
    """
    Compute cost and gradient for logistic regression
    COSTFUNCTION(theta, X, y) computes the cost of using theta as the
    parameter for logistic regression and the gradient of the cost
    w.r.t. to the parameters.
    """

    m = len(y) * 1.0

    cost = 1/m * (
        np.dot(-1*y, np.log(sigmoid(np.dot(X, theta))))
        - np.dot(1 - y, np.log(1 - sigmoid(np.dot(X, theta))))
        )

    grad = 1/m * np.dot(sigmoid(np.dot(X, theta)) - y, X)

    return cost, grad


def costFunctionReg(theta, X, y, lamb):
    """
    Compute cost and gradient for logistic regression with regularization
    JCOSTFUNCTIONREG(theta, X, y, lamb) computes the cost of using
    theta as the parameter for regularized logistic regression and the
    gradient of the cost w.r.t. to the parameters.
    """

    m = len(y) * 1.0

    shorttheta = theta[1:]

    cost = 1/m * (
        np.dot(-1*y, np.log(sigmoid(np.dot(X, theta))))
        - np.dot(1 - y, np.log(1 - sigmoid(np.dot(X, theta))))
        + lamb / 2 * np.inner(shorttheta, shorttheta)
        )

    grad = 1/m * (
        np.dot(sigmoid(np.dot(X, theta)) - y, X)
        + lamb * np.append(0, shorttheta)
        )

    return cost, grad


def predict(theta, X):
    """
    PREDICT Predict whether the label is 0 or 1 using learned logistic
    regression parameters theta
    p = PREDICT(theta, X) computes the predictions for X using a
    threshold at 0.5 (i.e., if sigmoid(theta'*x) >= 0.5, predict 1)
    """

    return sigmoid(np.dot(X, theta)) > 0.5
