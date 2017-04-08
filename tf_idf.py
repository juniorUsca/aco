import math

def tf_idf(str_file):
	a_buffer=[]
	doc_tam={}
	archivo = open(str_file, "r") 

	while 1:
		linea1 = archivo.readline()
		if not linea1 : break
		#append agrega al final
		a_buffer.append(linea1)

	archivo.close()
	
	print "DF"

	words = {}
	a_flag = {}
	i = 0
	for linea in a_buffer:
		words_l = linea.split()
		#doc_tam.append(len(words_l))
		doc_tam[i] = len(words_l)
		i += 1

		for w in words_l:
			if w in words:
				if not w in a_flag:
					words[w] += 1
				if w in a_flag and a_flag[w]==False:
					words[w] += 1
				a_flag[w] = True
			else:
				words[w] = 1
				a_flag[w] = True

		for kf in a_flag.keys():
			a_flag[kf] = False

	del a_flag

	tam_col = len(words)
	tam_fil =len(a_buffer)
	
	#matrix = [[0 for x in range(tam_col)] for y in range(tam_fil)]
	pesos = {}

	for d in range(tam_fil):
		if not d in pesos:
			pesos[d] = {}
		#for w in words.keys():
			#pesos[d][w] = 0
	
	print "Contando palabras"

	num_linea = 0
	for linea in a_buffer:
		words_l = linea.split()
		for w in words_l:
			if w in pesos[num_linea]:
			#if w in pesos.get(num_linea)
				pesos[num_linea][w] += 1
			else:
				pesos[num_linea][w] = 1
		num_linea+=1

	del a_buffer

	print "TF"

	#TF
	for k,v in pesos.items():
		for k1,p in v.items():
			pesos[k][k1] = p/(doc_tam[k]*1.0)

	del doc_tam
	
	print "IDF"

	#idf
	idf = {}

	for kw,vw in words.items():
		idf[kw] = math.log(tam_fil/(vw*1.0))

	print "TF*IDF"

	for k,v in pesos.items():
		for k1,p in v.items():
			pesos[k][k1] = pesos[k][k1]*idf[k1]

	'''print words
	print idf
	print "pesos"
	for (v) in pesos.values():
		print v'''

	return {"tf_idf": pesos, "df": words}
	