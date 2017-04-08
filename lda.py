from __future__ import print_function
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups

import numpy as np
from scipy.sparse import csr_matrix
import operator

def print_top_words(model, feature_names, n_top_words):
	for topic_idx, topic in enumerate(model.components_):
		print("Topic #%d:" % topic_idx)
		print(" ".join([feature_names[i]
						for i in topic.argsort()[:-n_top_words - 1:-1]]))
	print()

def lda(matriz, n_topics=10, n_top_words=20):


	indptr = [0]
	indices = []
	keywords = []
	data = []
	vocabulary = {}

	for key_d, val_d in matriz.items():
		for key_w, val_w in val_d.items():
			index = vocabulary.setdefault(key_w, len(vocabulary))
			indices.append(index)
			data.append(val_w)
		indptr.append(len(indices))


	tf_idf = csr_matrix((data, indices, indptr), dtype=float)

	vocabulary_sorted = [t for t, i in sorted( vocabulary.items(), key=operator.itemgetter(1) )]
	#dic = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)

	'''
	n_samples = 20
	n_features = 10
	n_topics = 10
	n_top_words = 20

	print("Loading dataset...")
	t0 = time()
	dataset = fetch_20newsgroups(shuffle=True, random_state=1,
								 remove=('headers', 'footers', 'quotes'))
	data_samples = dataset.data[:n_samples]
	print("done in %0.3fs." % (time() - t0))'''

	'''# Use tf-idf features for NMF.
	print("Extracting tf-idf features for NMF...")
	tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
									   max_features=n_features,
									   stop_words='english')
	t0 = time()
	tfidf = tfidf_vectorizer.fit_transform(data_samples)
	print("done in %0.3fs." % (time() - t0))

	# Fit the NMF model
	print("Fitting the NMF model with tf-idf features, "
		  "n_samples=%d and n_features=%d..."
		  % (n_samples, n_features))
	t0 = time()
	nmf = NMF(n_components=n_topics, random_state=1,
			  alpha=.1, l1_ratio=.5).fit(tfidf)
	print("done in %0.3fs." % (time() - t0))

	print("\nTopics in NMF model:")
	tfidf_feature_names = tfidf_vectorizer.get_feature_names()
	print_top_words(nmf, tfidf_feature_names, n_top_words)'''
	'''
	# Use tf (raw term count) features for LDA.
	print("Extracting tf features for LDA...")
	tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
									max_features=n_features,
									stop_words='english')
	t0 = time()
	tf = tf_vectorizer.fit_transform(data_samples)
	print("done in %0.3fs." % (time() - t0))

	print(tf.toarray())'''

	print("Fitting LDA models with tf_idf features ")

	lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
									learning_method='online',
									learning_offset=50.,
									random_state=0)
	t0 = time()
	lda.fit(tf_idf)
	print("done in %0.3fs." % (time() - t0))

	print("\nTopics in LDA model:")
	print_top_words(lda, vocabulary_sorted, n_top_words)