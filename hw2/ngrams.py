import re
from math import log, exp

START = "<START>"
STOP = "<STOP>"
OOV = "<OOV>"

tokenize_rx = re.compile(r"(\W)")

def read_lines_from_file(fname):
    """read in a file and return a list of stripped lines
    input: 
        fname (str): file name to read
    returns:
        (list): list of lines from the file. Strip but do not lowercase or split. Do not return empty lines
    """
    return []


def tokenize_words(line):
    """tokenize words in a line. Split off punctuation as their own tokens, do not lowercase
    input:
        line (str): text string
    return:
        (list): list of word or punctuation tokens, original casing
    """
    return


def tokenize_chars(line):
    """tokenize characters in a line.
    input:
        line (str): text string
    return:
        (list): list of characters, orginal casing
    """
    return


def tokenize_wordchars(lines):
    """Turn a sequence of text lines into a series of character-tokenized words
    input:
        lines (seq): sequence of text strings
    return:
        (list): list of lists of characters
    """
    return


def pad(seq, n):
    """Pad a sequence of tokens
    input:
        seq (seq): sequence of tokens
        n (int): indicates ngram width that the returned line will be used for
    return:
        (tuple): tuple with START and STOP padding
    """
    return


def get_ngrams(seq, n):
    """Returns a list of ngrams with padding from a sequence
    input:
        seq (seq): sequence of tokens
        n (int): ngram width
    return:
        (list): list of n-grams from padded sequence
    """
    return


def update_freqdict(seq, freqdict):
    """updates a dictionary of frequencies
    input: 
        seq (sequence): token sequence
        freqdict (dict str:dict str:int): frequency dictionary mapping contexts to tokens, tokens to frequencies
    return:
        (none): the frequency dictionary is updated by-reference, not returned
    """
    return


def get_ngramlogprobs(freqdict):
    """converts a dicitonary of ngram frequencies into a dictionary of ngram log probabilities
    input:
        freqdict (dict str:dict str:num): frequency dict mapping contexts to tokens, tokens to frequencies
    return:
        (dict str:dict str:num): dict mapping contexts to tokens, tokens to log probabilities 
    """
    return


def get_ngramlogprobs_fromcorpus(tokenizedseqs, n):
    """converts a list of tokenized lines into a dictionary of ngram log probabilities
    input:
        tokenizedlines (list): a list of tokenized lines. Each tokenized line is a list of tokens
        n (int): ngram width. 1 for unigram, 2 for bigram, 3 for trigram, etc.
    return:
        (dict str:dict str:num): dict mapping contexts to tokens, tokens to log probabilities 
    """
    return

    
def addalpha_bigram(freqdict, alpha):
    """performs add alpha smoothing on bigram frequencies, include OOV
    input:
        freqdict (dict str:dict str:num): frequency dict mapping contexts to tokens, tokens to frequencies
        alpha: value to be added
    return:
        (dict str:dict str:num): a new dictionary with smoothed frequencies. Be careful not to modify freqdict
    """
    return
            

def get_bigramlogprobs_fromcorpus_addalpha(tokenizedseqs, alpha):
    """converts a list of tokenized lines into a dictionary of ngram log probabilities with alpha smoothing
    input:
        tokenizedlines (list): a list of tokenized lines. Each tokenized line is a list of tokens
        alpha (num): smoothing parameter
    return:
        (dict str:dict str:num): dict mapping contexts to tokens, tokens to smoothed log probabilities 
    """
    return


def replace_OOV(seq, typeset):
    """Replaces OOV tokens in a sequence with the special OOV type
    input: 
       seq (seq): Token sequence
       typeset (collection): collection of types in the vocabulary
    return:
       (seq): Sequence with every token not in typeset replaced with OOV
    """
    return


def score_sequence(seq, ngramlogprobs):
    """Scores a sequence of ngrams
    input:
        seq (seq): a sequence of ngrams
        ngramlogprobs (dict str:dict str:num): dict mapping contexts to tokens, tokens to log probabilities
    return:
        float('-inf') if any ngram is missing from ngramlogprobs. log probability of the sequence otherwise
    """
    return


def main():

    # Some useful commands
    lines = read_lines_from_file("flatland_clean.txt")

    tokenizedlines = [tokenize_words(line) for line in lines]
    uniprobs = get_ngramlogprobs_fromcorpus(tokenizedlines, 1)
    biprobs = get_ngramlogprobs_fromcorpus(tokenizedlines, 2)
    triprobs = get_ngramlogprobs_fromcorpus(tokenizedlines, 3)
    biprobs_smooth = get_bigramlogprobs_fromcorpus_addalpha(tokenizedlines, 1)

    tokenizedwords = tokenize_wordchars(lines)
    uniprobs_w = get_ngramlogprobs_fromcorpus(tokenizedwords, 1)
    biprobs_w = get_ngramlogprobs_fromcorpus(tokenizedwords, 2)
    biprobs_w_smooth = get_bigramlogprobs_fromcorpus_addalpha(tokenizedwords, 1)



if __name__ == "__main__":
    main()
