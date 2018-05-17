import os.path
import numpy as np
import matplotlib.image as mpimg
import pickle
import rospkg

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.
    """
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

def round_to_minus(x):
	'''
	If the probability>0.5, returns 1, else return 0
	'''
	if x>0.3:
		return 1
	else:
		return -1

def user_recognized(Base_path,classifier):
	#Leer las imagenes y convertirlas en vector
	X_list=[]
	Path=[]
	#Crear Path para cada una de las imagenes
	for dirname, dirnames, filenames in os.walk(Base_path):
		for x in filenames:
			Path.append(Base_path+'/'+x)

	#Leer cada imagen
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
	    lda,clf, X_test_lda, y_test,target_names,n_classes = pickle.load(f)

	#Extraccion de caracteristicas
	X_lda = lda.transform(X)
	# Convertir de numpy a int
	y_pred = map(int,clf.predict(X_lda))
	# Obtener probabilidad de cada clase
	y_proba=clf. predict_proba(X_lda)
	# Probabilidad mas alta
	y_max=[max(i) for i in y_proba]
	# Redondear la probabilidad a -1 y 1
	y_rounded=map(round_to_minus,y_max)
	# Multiplicar la probabilidad mas alta y la clase predicha
	y_final=map(lambda x,y:x*y, y_pred, y_rounded)
	# Obtener la clase mas repetida
	freq_dic=getFrequencyDict(y_final)
	user_detected=keywithmaxval(freq_dic)
	if user_detected<0:
		return 'NO USER IN THE DATA BASE'
	return target_names[user_detected-1]

if __name__ == '__main__':
	#Path de las imagenes
	rospack = rospkg.RosPack()
	# get the file path for rospy_tutorials
	CSV_Images=rospack.get_path('tt2_pack')+'/include/user'
	classifier=rospack.get_path('tt2_pack')+'/include/Clasificador.pkl'
	print user_recognized(CSV_Images,classifier)
