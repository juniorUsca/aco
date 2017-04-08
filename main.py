from tf_idf import *
from grafoHormiga import *
from lda import *

_file = "20ng-train-stemmed.txt"
#_file = "texto.txt"

############################## TF_IDF ############################
print "#########################################"
print "Inicia tf_idf"
res_tf_idf = tf_idf(_file)
print "Fin tf_idf"
_tf_idf = res_tf_idf["tf_idf"]


############################## LDA ############################
print "#########################################"

#_num_topicos = 10
_num_topicos = 20
_num_top_words = 20
lda(_tf_idf, _num_topicos, _num_top_words)

############################## ACO ############################
print "#########################################"

_n = res_tf_idf["df"]

# heuristica
_alfa = 1.
# feromona
_beta = 1.
_rastro = 10.
_num_horm = 30
#_num_horm = 2
_num_iterac = 250
#_num_iterac = 500
#_num_iterac = 2500
_evap = 0.2
_Q = 1.
_num_etiquetas = 10

# para cada documento generamos una colonia de hormigas
for doc,vc in _tf_idf.items():
	# el grafo tiene el formato {"hola":0.123, "tiene": 0.345, "mama": 0.456} osea es el vector caracteristico
	(_grafo, inicio) = get_etiquetas(vc, _num_etiquetas)
	(etiquetas_ordenadas, detalles_etiquetas) = colonia_hormigas( doc, _grafo, inicio, _n, _alfa, _beta, _rastro, _num_horm, _num_iterac, _evap, _Q )
	print "doc #"+str(doc), etiquetas_ordenadas