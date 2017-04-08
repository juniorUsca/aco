import random
import operator
import datetime
import simplejson
import math

def get_etiquetas(dic, num_etiquetas):
	etiquetas = {}
	# ordenamos las etiquetas
	dic = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
	# coje las n primeras etiquetas
	
	flag = False
	inicio = ""

	n = 0
	for etiq, val in dic:
		if val != 0:
			etiquetas[etiq] = val
			# cogemos el primer elemento para el grafo
			if not flag:
				inicio = etiq
				flag = True
			n+=1
		if n>=num_etiquetas:
			break

	return (etiquetas, inicio)

def gg(hormigas, inicio, destino, Q):
	sum_i = .0
	sum_j = .0
	for hormiga in hormigas:
		# sum_i
		if inicio in hormiga["visitados_dic"] and \
		   hormiga["visitados_dic"][inicio] == destino:
			sum_i += 1.
		# sum_j
		if destino in hormiga["visitados_dic"] and \
		   hormiga["visitados_dic"][destino] == inicio:
			sum_j += 1.
	# apetencia: Con(i,j) = gi+gj/m
	con = (sum_i + sum_j) / len(hormigas)
	if con == .0:
		#con = 1000
		con = 1

	# calculamos el gg
	return Q * sum_i/con

def colonia_hormigas( doc_id, grafo, inicio, n, alfa, beta, rastro_ini, num_hormigas, num_iteraciones, evap, Q ):
	
	out = open('out.'+str(doc_id)+'.'+inicio+'.'+str(datetime.datetime.now().strftime("%I:%M%pon%B%d,%Y")), 'w+')
	

	rastros = {}
	probabilidades = {}
	# iniciamos los rastros como rastro_ini=10
	for key_i, val_i in grafo.items():
		for key_j, val_j in grafo.items():
			if key_i != key_j:
				if not key_i in rastros:
					rastros[ key_i ] = {}
				rastros[ key_i ][ key_j ] = rastro_ini


	for it in xrange(0,num_iteraciones):
		
		if math.fmod (it+1, 500) == 0.0 or it == 0:
			print "Iteracion "+inicio+" #"+str(it)
		out.write( ">>>>>>>>>>> Iteracion #"+str(it)+"\n" )

		hormigas = []
		primer_probs = True
		probabilidades = {}

		for num_hormiga in xrange(0,num_hormigas):
			
			#peso_total = 0.
			visitados = []
			visitados_dic = {}
			no_visitados = grafo.keys()
			actual = ""
			#rastros = {}
			probs = {}

			# ponemos como nodo visitado el inicio
			visitados.append(inicio)
			no_visitados.remove(inicio)
			actual = inicio

			######## obtenemos el camino de la hormiga #########

			#print ">> Hormiga #"+str(num_hormiga)
			out.write( ">> Hormiga #"+str(num_hormiga)+"\t: " )

			# mientras haya un elemento en no_visitados
			while no_visitados:
				# calculamos el vecindario factible
				N = 0.
				for key in no_visitados:
					rn = math.pow(rastros[actual][key],alfa)*math.pow(n[key],beta)
					probs[key] = rn
					N += rn
				
				# obtenemos rand para escoger el camino
				rand = random.random() # [0,1)
				#rand = random.uniform(0, 1)

				suma = 0.
				flag = False
				# se calcula la probabilidad para cada palabra no visitada
				for key in no_visitados:
					probs[key] = probs[key] / N
					# vemos que camino escoger con rand
					suma += probs[key]

					if suma >= rand and not flag:
						flag = True
						visitados_dic[ visitados[-1] ] = key
						visitados.append(key)
						# no_visitados.remove(key)
						# break
				if flag:
					no_visitados.remove( visitados[-1] )

				if primer_probs:
					probabilidades = probs.copy()
					primer_probs   = False

			hormiga = {
				"visitados"     : visitados,
				"visitados_dic" : visitados_dic,
			}
			hormigas.append( hormiga )
			
			#print hormiga["visitados"]
			simplejson.dump(hormiga["visitados"], out)
			out.write( "\n" )

		#print probabilidades
		out.write( "PROBABILIDADES: " )
		simplejson.dump(probabilidades, out)
		out.write( "\n" )
		
		
		#print "\n>> Evaporamiento #"+str(it)
		out.write( ">> Evaporamiento #"+str(it)+"\n" )
		##################### evaporamiento ####################

		# evaporacion
		for key_i, val_i in rastros.items():
			for key_j, val_j in val_i.items():
				# cantidad de feromonas depositadas
				c_fer = gg(hormigas, key_i, key_j, Q)
				rastros[ key_i ][ key_j ] = (1.-evap) * rastros[key_i][key_j] + (evap*c_fer)

		#print rastros
		simplejson.dump(rastros, out)
		out.write("\n")

		# amontonamiento de feromonas
		'''
		T = 0
		for key, val in rastros.items():
			rastros[ key ] = (evap * rastros[key]) + 

		# evaporacion
		for key, val in rastros.items():
			rastros[ key ] = (evap * rastros[key]) + 
		'''
	######## obtenemos el vector final #########
	
	salida = {}
	etiquetas = []

	no_visitados = grafo.keys()

	etiquetas.append(inicio)
	no_visitados.remove(inicio)
	actual = inicio

	while no_visitados:

		val_primer = 0.
		val_mayor  = 0.
		flag_primero = True
		word = ""

		# buscamos el mayor de los rastros
		for key in no_visitados:
			val = rastros[actual][key]
			if flag_primero:
				flag_primero = False
				val_primer = val

			if val_mayor < val:
				val_mayor = val
				word = key

		# si todos tienen el mismo rastro
		if val_primer == val_mayor:
			val_mayor = 0.
			# buscar en las probabilidades
			for key in no_visitados:
				val = probabilidades[ key ]
				if val_mayor < val:
					val_mayor = val
					word = key

		s = {
			"destino"      : word,
			"rastro"       : rastros[actual][word],
			"probabilidad" : probabilidades[ word ]
		}
		salida[actual] = s
		etiquetas.append(word)
		no_visitados.remove(word)
		actual = word

	return (etiquetas, salida)

