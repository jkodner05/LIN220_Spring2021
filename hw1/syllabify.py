
EN_VOWELS = None
SN_VOWELS = None

def get_words_from_file(fname):
    """Reads a wordlist file that contains one word per line
    input:
        fname (str): Filename
    returns:
        (list): list of trimmed and cleaned words
    """
    return


def get_transcription_dict_from_file(fname):
    """Reads CMUdict ARPABET transcription file into a dictionary
    input:
        fname (str): Filename. File contains space-separated word arpabet pairs
    returns:
        (dict: str:tuple): dict mapping word form sttrings to tuples of characters
    """
    return


def lookup_transcriptions(wordlist, transcriptiondict):
    """Attempts to match transcriptions to items in wordlist
    input:
        wordlist (list): list of words to transcribe
        transcriptions (dict): dictionary of word:transcription pairs
    returns:
        (dict: str:tuple): word:transcription pairs 
        (list): OOV words without transcritpions
    """
    return 
        

def estimate_onsets(transcriptions, vowels):
    """Find all the attested word-initial onsets
    input:
        transcriptions (dict): word:transcription tuple pairs
        vowels (set): vowels to use for finding nuclei
    returns:
        (set): set of onsets. Each onset is a tuple of ARPABET phones
    """
    return 


def mark_vowels(transcription, vowels):
    """Find the locations of each vowel in the transcription
    input:
        transcription (tuple): tuple of phones
        vowels (set): vowels to use for finding nuclei
    returns:
        (sequence): sequence of indices corresponding to the vowels
    """
    return


def mark_syllstarts(transcription, nuc_indices, licit_onsets):
    """Find the locations of the first phone of each syllable
    input:
        transcription (tuple): tuple of phones
        nuc_indices (sequence): indices of the nulcei in the transcription
        licit_onsets (set): collection of valid onsets. Each onset is a tuple of ARPABET phones
    returns:
        (sequence): sequence of indices corresponding to the first phone of each syllable
    """
    return


def split_transcription(transcription, syllstart_indices):
    """Split a transcription into a sequence of syllables
    input:
        transcription (tuple): tuple of phones
        syllstart_indices (sequence): sequence of indices corresponding to the first phone of each syllable
    returns:
        (sequence): a sequence of sequences. Each inner sequence is a syllable represented as a sequence of phones
    """
    return


def get_syllabifications(transcriptions, licit_onsets, vowels):
    """Syllabify a series of transcriptions
    input:
        transcriptions (dict): dictionary of word:transcription pairs, where each transcription is a tuple of strings (phones)
        licit_onsets (set): a collection of licit onsets represented as tuples of phones
        vowels (set): a collections of vowels
    returns:
        (dict): a dictinary mapping word to syllabified transcription
    """
    syllabifications = {}
    for word, trans in transcriptions.items():
        nucleus_indices = mark_vowels(trans, vowels)
        syllstart_indices = mark_syllstarts(trans, nucleus_indices, licit_onsets)
        syllabifications[word] = split_transcription(trans, syllstart_indices)
    return syllabifications


def write_syllables(fname, syllabified_dict):
    """Write syllabifications to a file.
    Each line in the output file should contain a tab-separated word-syllabification pair and end in a newline.
    The syllabification should be in ARPABET notation, but with a . inserted between syllbles
    For example, a valid line is "applesauce	AE1 P AH0 L . S AO2 S"
    input:
        fname (str): output filename
        (dict): a dictinary mapping word to syllabified transcription
        transcriptions (dict): dictionary of word:transcription pairs, where each transcription is a tuple of strings (phones)
        licit_onsets (set): a collection of licit onsets represented as tuples of phones
        vowels (set): a collections of vowels
    returns:
        None
    """
    return


def gen_transcriptions(wordlist):
    """Create a Shona ARPABET-Style transcription for each word in the wordlist
    Most characters should map to their own capitalized form in the transcription. The exceptions are as follows:
        a --> AA0
        e --> EY0
        i --> IY0
        o --> OW0
        u --> UW0
        bh -> BH not B H
        ch -> CH not C H...
        dh -> DH
        mh -> MH
        nh -> NH
        n' -> N'
        sh -> SH
        sv -> SH
        zh -> ZH
        zv -> ZH
    input:
        wordlist (list): list of words to transcribe
    returns:
        (dict): dictionary of word:transcription pairs
    """
    return 
            

def syllabify_en_with_sn(trainingfname, testingfname, outfname):
    """Learns licit onsets from Shona and uses those to syllabify English
    input:
        trainingfname (str): Shona wordlist file to read in
        testingfname (str): English wordlist file to read in
t        outfname (str): output file to write to
    returns:
        None
    """
    return


def syllabify_english_OOV(wordlistfname, outfname):
    """Syllabifies English words without transcription"""
    return


def syllabify_english(wordlistfname, outfname):
    """This function looks up transcriptions for a word list and syllabifies"""
    vowels = EN_VOWELS # collection of vowels for English ARPABET

    # Read in the files
    wordlist = get_words_from_file(wordlistfname)
    cmudict = get_transcription_dict_from_file("cmudict.dict")

    # Match the words in the wordlist to the words in the transcription dictionary
    transcribed_wordlist, OOV_wordlist = lookup_transcriptions(wordlist, cmudict)

    # Learn an approximation of the licit onsets from the data
    licit_onsets = estimate_onsets(transcribed_wordlist, vowels)

    # perform the syllabification
    syllabified_dict = get_syllabifications(transcribed_wordlist, licit_onsets, vowels)

    # Write the result to a file
    write_syllables(outfname, syllabified_dict)

    
def syllabify_shona(wordlistfname, outfname):
    """This function converts a word list to transcriptions and syllabifies"""
    vowels = SN_VOWELS # collection of vowels for English ARPABET

    # Read in the file
    wordlist = get_words_from_file(wordlistfname)

    # Convert the wordlist to transcriptions
    transcribed_wordlist = gen_transcriptions(wordlist)

    # Learn an approximation of the licit onsets from the data
    licit_onsets = estimate_onsets(transcribed_wordlist, vowels)

    # perform the syllabification
    syllabified_dict = get_syllabifications(transcribed_wordlist, licit_onsets, vowels)

    # Write the result to a file
    write_syllables(outfname, syllabified_dict)


def main():

    # Part 2: Syllabify English with CMUDict
    #syllabify_english("wordlist_en.txt", "en_syllabified.tsv")

    # Part 3: Syllabify Shona
    #syllabify_shona("wordlist_sn.txt", "sn_syllabified.tsv")
    
    # EC 1: Syllabify English with Shona Onsets
    #syllabify_en_with_sn("wordlist_sn.txt", "wordlist_en.txt", "ensn_syllabified.tsv")

    # EC 2: Syllabify OOV words
    #syllabify_OOV("wordlist_en.txt", "en_syllabified.tsv")


if __name__ == "__main__":
    main()
