from time import time

from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

import numpy as np
import pickle

#La funcion with crea una variable temporal
with open('Clasificador.pkl') as f:  # Python 3: open(..., 'rb')
    clf, X_test_pca, y_test,target_names,n_classes = pickle.load(f)

print "Predicting the people names on the testing set"
t0 = time()
y_pred = clf.predict(X_test_pca)
print "done in %0.3fs" % (time() - t0)
print classification_report(y_test, y_pred, target_names=target_names)
print confusion_matrix(y_test, y_pred, labels=range(n_classes))