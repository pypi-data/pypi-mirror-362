# English 21st-century function word sets

ARTICLES_DETERMINERS = frozenset([
    "the", "a", "an",
    "this", "that", "these", "those",
    "each", "every", "all", "some", "any",
    "no", "none", "both",
    "either", "neither",
    "enough",
    "much", "many", "several", "various", "certain", "other", "another", "such",
    "little", "few", "fewer", "less", "more", "most", "plenty",
])

POSSESSIVE_DETERMINERS = frozenset([
    "my", "your", "his", "her", "its", "our", "their",
])

PERSONAL_PRONOUNS = frozenset([
    "i", "you", "he", "she", "it", "we", "they",
    "me", "him", "her", "us", "them",
])

POSSESSIVE_PRONOUNS = frozenset([
    "mine", "yours", "his", "hers", "its", "ours", "theirs",
])

DEMONSTRATIVE_PRONOUNS = frozenset([
    "this", "that", "these", "those", "such",
])

INDEFINITE_PRONOUNS = frozenset([
    "all", "another", "any", "anybody", "anyone", "anything",
    "both", "each", "either", "everybody", "everyone", "everything",
    "few", "many", "most", "much", "neither", "nobody", "none", "no one", "nothing",
    "one", "other", "others", "several", "some", "somebody", "someone", "something",
    "plenty", "lot", "lots", "anywhere", "somewhere", "everywhere", "nowhere",
])

INTERROGATIVE_PRONOUNS = frozenset([
    "who", "whom", "whose", "what", "which",
])

PREPOSITIONS = frozenset([
    "about", "above", "across", "after", "against", "along", "amid", "among",
    "around", "as", "at", "before", "behind", "below", "beneath", "beside",
    "besides", "between", "beyond", "but", "by", "concerning", "despite",
    "down", "during", "except", "for", "from", "in", "inside", "into",
    "like", "near", "of", "off", "on", "onto", "out", "outside", "over",
    "past", "regarding", "since", "through", "throughout", "till", "to",
    "toward", "under", "underneath", "until", "up", "upon", "with", "within",
    "without",
    # compound
    "according to", "because of", "due to", "instead of", "in spite of", "out of",
    "ahead of", "apart from", "as for", "as to", "close to", "far from", "next to",
])

COORD_CONJUNCTIONS = frozenset([
    "and", "or", "nor", "but", "so", "yet", "for",
])

SUBORD_CONJUNCTIONS = frozenset([
    "that", "if", "because", "although", "though", "while", "whereas",
    "when", "whenever", "where", "wherever",
    "since", "as", "until", "unless", "before", "after", "once",
    "even though", "even if", "rather than",
])

ADVERBS = frozenset([
    # place
    "here", "there", "where", "everywhere", "somewhere", "anywhere", "nowhere",
    "above", "below", "inside", "outside", "away", "back",
    # time
    "now", "then", "today", "tomorrow", "yesterday", "already", "still",
    "yet", "soon", "later", "again", "before", "after", "recently", "lately",
    "always", "often", "frequently", "usually", "sometimes",
    "rarely", "seldom", "never", "ever",
    # manner/degree
    "well", "badly", "better", "worse", "fast", "hard",
    "very", "too", "quite", "rather", "pretty", "fairly",
    "extremely", "highly", "deeply", "enough", "almost", "nearly",
    "hardly", "barely", "just", "exactly", "only", "even", "instead",
    # linking / stance
    "however", "therefore", "thus", "hence", "otherwise", "meanwhile",
    "afterwards", "besides", "anyway", "indeed", "perhaps", "maybe",
    "actually", "certainly", "clearly", "obviously",
])

ADV_LOCUTIONS = frozenset([
    "right away", "straight away", "at once", "in fact", "of course",
    "for example", "for instance", "by the way", "in other words",
    "as well", "at least", "at most", "in general", "in particular",
    "to be honest", "in my opinion", "on the one hand", "on the other hand",
    "at the same time", "in the meantime", "after all", "all of a sudden",
    "out of the blue", "from time to time", "once in a while",
    "every now and then", "every so often", "kind of", "sort of",
    "a lot", "a lot of", "lots of", "a bit", "a little bit",
    "as soon as possible", "as far as", "as long as", "as much as",
    "up to now", "so far", "just now", "these days", "nowadays",
    "no longer", "any more", "ahead of time", "on time", "in time",
    "at first", "at last", "in front of", "on top of", "side by side",
    "for good", "for now", "for sure", "so to speak", "by all means",
])

NEGATIONS = frozenset([
    "not", "n't", "no", "none",
    "neither", "nor", "never", "hardly", "scarcely", "barely",
    "nobody", "no one", "nothing", "nowhere",
    "without",
])

AUX_BE = frozenset([
    "be", "am", "is", "are", "was", "were", "been", "being",
])

AUX_HAVE = frozenset([
    "have", "has", "had", "having",
])

MODAL_VERBS = frozenset([
    "can", "can't", "cannot", "could", "couldn't",
    "may", "might", "mightn't",
    "shall", "shan't", "should", "shouldn't",
    "will", "won't", "would", "wouldn't",
    "must", "mustn't",
    "ought", "oughtn't",
    "need", "needn't",
    "dare", "daren't",
    "used to",
])

categories = {
    "articles": sorted(ARTICLES_DETERMINERS),
    "poss_det": sorted(POSSESSIVE_DETERMINERS),
    "pers_pron": sorted(PERSONAL_PRONOUNS),
    "poss_pron": sorted(POSSESSIVE_PRONOUNS),
    "dem_pron": sorted(DEMONSTRATIVE_PRONOUNS),
    "indef_pron": sorted(INDEFINITE_PRONOUNS),
    "inter_pron": sorted(INTERROGATIVE_PRONOUNS),
    "prepositions": sorted(PREPOSITIONS),
    "coord_conj": sorted(COORD_CONJUNCTIONS),
    "subord_conj": sorted(SUBORD_CONJUNCTIONS),
    "adverbs": sorted(ADVERBS),
    "adv_locutions": sorted(ADV_LOCUTIONS),
    "negations": sorted(NEGATIONS),
    "aux_be": sorted(AUX_BE),
    "aux_have": sorted(AUX_HAVE),
    "modals_full": sorted(MODAL_VERBS),
}

data = {
    "name": "English – 21st century",
    "language": "en",
    "period": "21c",
    "categories": categories,
}
