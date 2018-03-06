import os.path
import numpy as np
import matplotlib.image as mpimg
import pickle

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]


def user_recognized(Base_path,classifier):
	#Leer las imagenes y convertirlas en vector
	X_list=[]
	Path=[]
	for dirname, dirnames, filenames in os.walk(Base_path):
		for x in filenames:
			Path.append(Base_path+'/'+x)

	for img in Path:
		imagen=mpimg.imread(img)
		shape = imagen.shape
		im_flat = imagen.ravel() #Convertimos en vector
		X_list.append(im_flat)
	h,w=shape

	#Matriz de imagenes vectorizadas. Data
	X = np.array(X_list)

	#La funcion with crea una variable temporal
	with open(classifier) as f:  # Python 3: open(..., 'rb')
	    pca,clf, X_test_pca, y_test,target_names,n_classes = pickle.load(f)

	#Extraccion de caracteristicas
	X_pca = pca.transform(X)
	y_pred = clf.predict(X_pca)
	freq_dic=getFrequencyDict(y_pred)
	return target_names[keywithmaxval(freq_dic)]
'''
#Path de las imagenes
Base_path=os.getcwd().replace('src/scripts','include/s12')
classifier='Clasificador.pkl'
print user_recognized(Base_path,classifier)
'''