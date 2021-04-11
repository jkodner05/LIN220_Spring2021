import re, math, sys
from threading import Thread

# User installed
import nltk.corpus
import numpy as np
import scipy.spatial.distance as dist
import scipy.cluster.hierarchy as hierarchy
from matplotlib import pyplot as plt
from sklearn.metrics.cluster import homogeneity_score, completeness_score, v_measure_score

START = "<START>"
STOP = "<STOP>"
LEFT = "<LEFT>"
RIGHT = "<RIGHT>"
UNKNOWN = "<UNK>"



class Word(object):
    """Object representing a word"""

    def __init__(self, wordform, contextlen):
        self.wordform = wordform # string representing the word
        self.posfreqs = {} # dictionary of POS tag : frquency
        self.maxpos = None # most frequent POS tag
        self.contextvec = [0] * (contextlen+3)*2 # vector for context word counts

    def updatepos(self, tokenpos):
        """updates token frequency of each POS tag for this Word and updates the most frequent tag"""
        self.posfreqs[tokenpos] = self.posfreqs.get(tokenpos,0) + 1
        if not self.maxpos or self.posfreqs[tokenpos] > self.posfreqs[self.maxpos]:
            self.maxpos = tokenpos
    
    def __repr__(self):
        return self.wordform
        


class Cluster(object):
    """Object representing a cluster"""
    
    def __init__(self, clusterid, members, maxdistance):
        self.clusterid = clusterid # id associated with this cluster
        self.members = members # words belonging to this cluster
        self.maxdistance = maxdistance # distance calculated at the cluster's highest join

    def __repr__(self):
        return "#%s @ %s: %s" % (self.clusterid, self.maxdistance, self.members)




def update_contexts(sentences, typedict, indices):
    """Populates the context vectors for each Word"""
    contextdict = {}
    for sent in sentences:
        update_contexts_sent(typedict, indices,  sent)


def get_topkwordlist(notags, k, padding):
    """include START and STOP"""
    freqdict = {}
    for sent in notags:
        for word in sent:
            if padding:
                freqdict[word] = freqdict.get(word,0) + 1
            elif re.match(r"\w+$", word):
                freqdict[word] = freqdict.get(word,0) + 1

    sortedwordfreqs = sorted(freqdict.items(), key = lambda kv: kv[1], reverse=True)
    topk = [w for w, freq in sortedwordfreqs][0:k]
    if padding:
        topk.extend([START,STOP,UNKNOWN])
    return topk


def get_indexdict(words):
    """Associates each word type with an index in the context vector"""
    indexdict = {}
    index = 0
    for word in words:
        if left(word) not in indexdict:
            indexdict[left(word)] = index
            index += 1
        if right(word) not in indexdict:
            indexdict[right(word)] = index
            index += 1
    return indexdict


def left(word):
    """This function annotates words as left context"""
    return LEFT+word


def right(word):
    """This function annotates words as right context"""
    return RIGHT+word


def make_tree(distances, method):
    """Performs agglomerative clustering using the scikit-learn library"""
    return hierarchy.linkage(distances, method=method)


def get_clusters(tree, wordlist, cutofffrac):
    """Extracts a list of Cluster objects from the agglomerative tree"""
    clusters = []

    #initialize singleton clusters
    for i, word in enumerate(wordlist):
        singleton = Cluster(i, {word}, 0)
        clusters.append(singleton)

    #iterate through joins
    newnodebase = len(wordlist)
    for i,row in enumerate(tree):
        lefttreei = int(row[0])
        righttreei = int(row[1])
        distance = row[2]
        lefttreemembers = clusters[lefttreei].members
        righttreemembers = clusters[righttreei].members
        joinedmembers = lefttreemembers.union(righttreemembers)
        clusters.append(Cluster(newnodebase+i, joinedmembers, distance))

    filtered_clusters = filter_clusters(clusters, cutofffrac)

    return filtered_clusters


def calc_distances_multi(typedict, distfunc, words_topk):
    """calculates the distance between two subtrees"""
    distances = np.zeros((len(words_topk),len(words_topk)))
    numsplits = 8 # Set numsplits to a number that works for you. Something between 4-16 for speed. 1 for debugging.

    def worker(lmin, lmax, rmin, rmax):
        for i, word1 in enumerate(words_topk):
            if i < lmin:
                continue
            if i >= lmax:
                break
            for j, word2 in enumerate(words_topk):
                if j < rmin:
                    continue
                if j >= rmax:
                    break
                if j > i:
                    break
                distances[i,j] = distfunc(typedict[word1].contextvec, typedict[word2].contextvec)
                distances[j,i] = distances[i,j]

    q, r = divmod(len(words_topk), numsplits)
    indices = [q*i + min(i, r) for i in range(numsplits+1)]

    splitsize = len(words_topk) / numsplits
    lindex = 0
    threads = []
    for i in range(numsplits):
        for j in range(numsplits):
            if j > i:
                continue
            threads.append(Thread(target=worker, args=(indices[i], indices[i+1], indices[j], indices[j+1])))

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return distances


def plot_dendrogram(tree, title, outname, namelist, k, frac):
    """Plots the agglomerative clusterings and saves to file"""
    def label_func(leafnum):
        word = namelist[leafnum]
        return word

    plt.figure(figsize=(int(0.45*k), int(0.4*k)))
    plt.title(title)
    plt.xlabel('sample index')
    plt.ylabel('distance')
    hierarchy.dendrogram(
        tree,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
        leaf_label_func = label_func,
        color_threshold = frac*max(tree[:,2]),
        distance_sort='descending',
    )
    plt.savefig(outname)
    plt.show()



###
### Your Functions Begin Here
###

def read_corpus(use_universal):
    """This function reads in the news section of Brown, lowercases everything, and returns tagged gold sentences and tokenized sentences with the sentences removed
    input:
        use_universal (bool): if True, uses the universal tagset, else uses the default
    returns:
        (list of lists of (word, tag) pairs: gold data as a list of tokenized sentences, each sentence is a list of (lowercased word, tag) pairs
        (list of lists of words): list of tokenized sentences, each sentence is a list of lowercased words. All tags are removed."""
    # The instructor solved this in 7 lines including the return
    gold = []
    notags = []
    # Your code here
    return list(gold), notags


def get_poscounts(golds, k):
    """Creates a dictionary of Word objects from the gold data set
    input:
        golds (list of lists of (word,tag) pairs: input data
        k (int): length of context vector to be associated with each Word
    returns:
        (dict of str:Word): a dictionary mapping word forms from the gold data to Word objects. Each Word keeps track of all the POS it was attested with in the gold data."""
    # The instructor solved this in 8 lines including the return
    types = {}
    # Your code here
    return types


def update_contexts_sent(typedict, indices, sentence):
    """This function updates all the Word objects' context vectors with counts from the provided sentence. The sentence must be padded with a single START and STOP symbol. Context words that do not appear in the index dictionary should be replaced with UNKNOWN.
    input:
        typedict (dict of str:Word): dictionary of Word objects
        indices: (dict of str:int): built in get_indexdict(.). Maps context words to indices in the context vectors
        sentence (list): List of word tokens
    returns:
        None. It updates the Words in typedict
    """
    # The instructor solved this in 13 lines.
    return


def norm(vec):
    """Divides each value in the context vector by the sum of the vector
    input:
        vec (list): list of integers
    return:
        (list): normalized vector"""
    # The instructor completed this function in 1 line including the return
    return [] 


def dist_euclidean(w, v):
    """Calculates euclidean distance between vectors w and v after normalizing them
    input:
        w (list): unnormalized vector
        v (list): unnormalized vector
    returns:
        (float): euclidean distance"""
    # The instructor completed this function in 1 line including the return
    return 0


def dist_manhattan(w, v):
    """Calculates manhattan distance between vectors w and v after normalizing them
    input:
        w (list): unnormalized vector
        v (list): unnormalized vector
    returns:
        (float): manhattan distance"""
    # The instructor completed this funciton in 1 line including the return
    return 0


def dist_cossim(w, v):
    """calculates -(cosine similarity - 1) as a distance metric. Rounded to 5 decimal places
    input:
        w (list): unnormalized vector
        v (list): unnormalized vector
    returns:
        (float): distance metric based on cosine similarity"""
    # The instructor completed this function in 5 line including the return
    return 0


def dist_kl(w, v):
    """EC: calculates KL-divergence between vectors w and v after normalizing them
    input:
        w (list): unnormalized vector
        v (list): unnormalized vector
    returns:
        (float): symmetrical KL-divergence (KL(w||v) + KL(v||w))"""
    # The instructor completed this function in 5 line including the return
    return 0


def filter_clusters(clusters, cutofffrac):
    """Finds the largest possible clusters with join distances smaller than the max distance * cutofffrac
    input:
        clusters (ordered list of Clusters): list of Clusters from agglomerative clustering
        cutofffrac (float): expected to be in range [0,1]
    return:
        (dict of int:Custer): dictionary of cluster ids to clusters. Every leaf should be included in exactly one cluster"""
    # The instructor completed this function in 12 line including the return
    filteredbyid = {}
    # Your code here
    return filteredbyid


def evaluate(clusters, typedict):
    """Given the predicted clusters and type dictionary, this function calculates homogeneity, completeness, and V-measure assuming the gold tags are the most frequent tags for each type in the type dict
    input:
        clusters (dict of int:Cluster): Clusters by id
        typedict (dict of str:Word): Word by wordform
    return:
        (float): homogeneity score
        (float): completeness score
        (float): V measure"""
    # The instructor completed this function in 7 line including the return
    golds = []
    preds = []
    # Your code here
    return homogeneity_score(golds, preds), completeness_score(golds, preds), v_measure_score(golds, preds, beta=2.0)


def main(use_universal, k_tree, k_context, cutoff_frac, distfuncname, treefname):
    # finds the distance function specified by the command line argument
    distfunc = globals()[distfuncname]

    # reads the corpus
    golds, notags = read_corpus(use_universal)
    # populations the type dictionary
    typedict = get_poscounts(golds, k_context)
    # gets the top k most frequent words as context words
    contextwords = get_topkwordlist(notags, k_context, padding=True)
    # makes an index dictionary to for looking up with the context vectors
    indexdict = get_indexdict(contextwords)
    # gets the top k words taht will actually be clustered
    topkwords = get_topkwordlist(notags, k_tree, padding=False)

    print("Populating context vectors", k_context)
    update_contexts(notags, typedict, indexdict)

    print("Calculating distances. Be Patient...")
    distances = calc_distances_multi(typedict, distfunc, topkwords)

    print("Getting clusters")
    tree = make_tree(dist.squareform(distances), 'average')
    clusters = get_clusters(tree, topkwords, cutoff_frac)
    h, c, v = evaluate(clusters, typedict)
    print("H: %s\tC: %s\tV: %s" % (h, c, v))

    print("Drawing the tree")
    plot_dendrogram(tree, "Dendrogram with %s percent cutoff" % (cutoff_frac*100), treefname, topkwords, len(topkwords), cutoff_frac)
    print("Done!")

if __name__=="__main__":
    main(True if sys.argv[1].lower() == "true" else False, int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5], sys.argv[6])



