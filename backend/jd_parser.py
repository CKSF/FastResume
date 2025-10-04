import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)

    # Part-of-speech tagging
    pos_tags = nltk.pos_tag(words)

    # Filter for nouns and adjectives, and exclude stop words
    keywords = [word for word, tag in pos_tags if (tag.startswith('NN') or tag.startswith('JJ')) and word.isalpha() and word.lower() not in stop_words]

    # Get the frequency distribution of the words
    fdist = nltk.FreqDist(keywords)

    # Return the most common keywords
    return [word for word, freq in fdist.most_common(15)]