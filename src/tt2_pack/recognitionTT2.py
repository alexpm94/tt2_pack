#! /usr/bin/env python

from numpy import genfromtxt
from time import time
import os.path

from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import RandomizedPCA
from sklearn.svm import SVC

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import logging
import pylab as pl
import pickle
import rospkg 

def recognition():
    rospack = rospkg.RosPack()
    # get the file path for rospy_tutorials
    CSV_Images=rospack.get_path('tt2_pack')+'/include/user_images.csv'

    classifier_path=rospack.get_path('tt2_pack')+'/include/Clasificador.pkl'
    #Leer el archivo csv
    my_data = np.genfromtxt(CSV_Images, delimiter=',',dtype=str)

    #Obtener los datos a partir del csv
    #Numero de clases
    target_names=np.array(my_data[::31,2])
    #Path de las imagenes
    Path=my_data[:,0]

    #Leer las imagenes y convertirlas en vector
    X_list=[]

    for img in Path:
    	imagen=mpimg.imread(img)
    	shape = imagen.shape
    	im_flat = imagen.ravel() #Convertimos en vector
    	X_list.append(im_flat)

    #Matriz de imagenes vectorizadas. Data
    X = np.array(X_list)
    #Label relacionado a cada clase
    y =np.array([int(i) for i in my_data[:,1]])
    h,w=shape

    n_samples, n_features = X.shape
    n_classes = target_names.shape[0]


    print "Tamano de la base de datos:"
    print "n_imagenes: %d" % n_samples
    print "n_caracteristicas: %d" % n_features
    print "n_clases: %d" % n_classes


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)
    print X_test.shape, X_train.shape

    ###############################################################################
    # Compute a PCA (eigenfaces) on the face dataset (treated as unlabeled
    # dataset): unsupervised feature extraction / dimensionality reduction

    n_components = 80

    print "Extracting the top %d eigenfaces from %d faces" % (n_components, X_train.shape[0])
    t0 = time()
    pca = RandomizedPCA(n_components=n_components, whiten=True).fit(X_train)
    print "done in %0.3fs" % (time() - t0)
    eigenfaces = pca.components_.reshape((n_components, h, w))
    ei_mean = pca.mean_.reshape(h,w)


    print "Projecting the input data on the eigenfaces orthonormal basis"
    t0 = time()
    X_train_pca = pca.transform(X_train)
    X_test_pca = pca.transform(X_test)
    print "done in %0.3fs" % (time() - t0)

    var=pca.explained_variance_ratio_
    first_pc=pca.components_[0]
    second_pc=pca.components_[1]

    #print var, sum(var), eigenfaces.shape, ei_mean.shape, X_train_pca.shape

    ###############################################################################
    # Train a SVM classification model
    print "Fitting the classifier to the training set"
    t0 = time()
    param_grid = {
             'C': [1e3, 5e3, 1e4, 5e4, 1e5],
              'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1],
              }
    # for sklearn version 0.16 or prior, the class_weight parameter value is 'auto'
    #Grid encuantra el mejor parametro de C y gamma pa ser utilizado con el kernel rbf
    clf = GridSearchCV(SVC(kernel='rbf', class_weight='balanced',probability=True), param_grid)
    clf = clf.fit(X_train_pca, y_train)
    print "done in %0.3fs" % (time() - t0)
    print "Best estimator found by grid search:"
    print clf.best_estimator_


    ###############################################################################
    # Quantitative evaluation of the model quality on the test set
    print "Predicting the people names on the testing set"
    t0 = time()
    y_pred = clf.predict(X_test_pca)
    y_proba=clf. predict_proba(X_test_pca)
    print "done in %0.3fs" % (time() - t0)

    #Guardar Variables del modelo ya entrenado
    with open(classifier_path, 'w') as f:  # Python 3: open(..., 'wb')
        pickle.dump([pca,clf, X_test_pca, y_test,target_names,n_classes], f)


    print classification_report(y_test, y_pred, target_names=target_names)
    print confusion_matrix(y_test, y_pred, labels=range(n_classes))

    ###############################################################################
    # Qualitative evaluation of the predictions using matplotlib

    def plot_gallery(images, titles, h, w, n_row=4, n_col=4):
        """Helper function to plot a gallery of portraits"""
        pl.figure(figsize=(1.8 * n_col, 2.4 * n_row))
        pl.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
        for i in range(n_row * n_col):
            pl.subplot(n_row, n_col, i + 1)
            pl.imshow(images[i].reshape((h, w)), cmap=pl.cm.gray)
            pl.title(titles[i], size=12)
            pl.xticks(())
            pl.yticks(())


    # plot the result of the prediction on a portion of the test set

    def title(y_pred, y_test, target_names, i):
        pred_name = target_names[y_pred[i]-1].rsplit(' ', 1)[-1]
        true_name = target_names[y_test[i]-1].rsplit(' ', 1)[-1]
        return 'predicted: %s\ntrue:      %s' % (pred_name, true_name)

    prediction_titles = [title(y_pred, y_test, target_names, i)
                             for i in range(y_pred.shape[0]-1)]

    plot_gallery(X_test, prediction_titles, h, w)

    # plot the gallery of the most significative eigenfaces

    eigenface_titles = ["eigenface %d" % i for i in range(eigenfaces.shape[0])]
    plot_gallery(eigenfaces, eigenface_titles, h, w)

    pl.show()
