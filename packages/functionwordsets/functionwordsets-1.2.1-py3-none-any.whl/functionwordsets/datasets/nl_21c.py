# Dutch 21st-century function words by grammatical nature.

ARTICLES_DETERMINERS = frozenset([
    "de", "het", "een",
    "dit", "deze", "dat", "die",
    "elke", "ieder", "iedere", "alle", "sommige", "enkele",
    "veel", "vele", "meest", "meeste",
    "geen", "ander", "andere", "verschillende", "dergelijke",
])

POSSESSIVE_DETERMINERS = frozenset([
    "mijn", "jouw", "uw", "zijn", "haar", "ons", "onze", "jullie", "hun",
])

PERSONAL_PRONOUNS = frozenset([
    "ik", "je", "jij", "u", "hij", "zij", "ze", "het",
    "we", "wij", "jullie", "zij", "ze",
    "me", "mij", "jou", "u", "hem", "haar", "het", "ons", "hen", "hun",
    "zich",
])

POSSESSIVE_PRONOUNS = frozenset([
    "de mijne", "het mijne",
    "de jouwe", "het jouwe",
    "de uwe", "het uwe",
    "de zijne", "het zijne", "de hare", "het hare",
    "de onze", "het onze",
    "de jullie", "het jullie",
    "de hunne", "het hunne",
])

DEMONSTRATIVE_PRONOUNS = frozenset([
    "dit", "deze", "dat", "die", "ditgene", "datgene", "diegene",
])

INDEFINITE_PRONOUNS = frozenset([
    "men", "iets", "niets", "niemand", "iedereen", "alles",
    "sommigen", "velen", "anderen", "enigen",
    "wat", "wat dan ook",
])

INTERROGATIVE_PRONOUNS = frozenset([
    "wie", "wat", "welk", "welke", "waar", "waarom", "wanneer", "hoe", "hoeveel",
    "wiens", "wier",
])

PREPOSITIONS = frozenset([
    "aan", "achter", "bij", "binnen", "buiten", "boven", "onder",
    "in", "op", "tegen", "tegenover", "voor", "zonder", "tussen", "langs",
    "sinds", "met", "na", "naast", "om", "over", "per", "rond", "tijdens",
    "van", "voorbij", "volgens", "tot", "totdat", "onder", "gedurende", "dankzij",
    "in plaats van", "ondanks", "wegens", "met betrekking tot",
])

COORD_CONJUNCTIONS = frozenset([
    "en", "of", "maar", "doch", "want", "dus", "noch",
])

SUBORD_CONJUNCTIONS = frozenset([
    "dat", "als", "wanneer", "toen", "terwijl", "omdat", "doordat", "zodat",
    "hoewel", "ofschoon", "aangezien", "opdat", "voor", "nadat", "voordat",
    "totdat", "zodra", "indien", "mits", "tenzij", "zoals", "om",
])

ADVERBS = frozenset([
    # plaats
    "hier", "daar", "overal", "ergens", "nergens",
    "boven", "beneden", "binnen", "buiten",
    # tijd
    "nu", "toen", "straks", "dadelijk", "altijd", "vaak", "soms",
    "zelden", "nooit", "al", "nog", "reeds", "weer", "vroeg", "laat",
    # wijze / graad
    "goed", "slecht", "beter", "slechter",
    "zeer", "heel", "erg", "te", "tamelijk", "behoorlijk",
    "bijna", "nauwelijks", "net", "precies", "slechts", "alleen",
    "even", "zelfs", "echt", "misschien",
    # discourse / linking
    "echter", "daarom", "desondanks", "vervolgens", "bovendien",
])

ADV_LOCUTIONS = frozenset([
    "meteen", "opnieuw", "in feite", "bijvoorbeeld", "natuurlijk",
    "zonder twijfel", "hoe dan ook", "onder andere", "ten slotte",
    "in het algemeen", "in het bijzonder", "op dit moment", "voorlopig",
    "langzamerhand", "langzaamaan", "steeds meer", "een beetje",
    "zo snel mogelijk", "tot nu toe", "af en toe", "van tijd tot tijd",
    "meestal", "niettemin",
])

NEGATIONS = frozenset([
    "niet", "geen", "niets", "niemand", "nooit", "nergens", "noch", "zonder",
])

AUX_ZIJN = frozenset([
    "zijn", "ben", "bent", "is", "zijn", "was", "waren", "geweest",
])

AUX_HEBBEN = frozenset([
    "hebben", "heb", "hebt", "heeft", "hebben", "had", "hadden", "gehad",
])

MODAL_VERBS = frozenset([
    # kunnen
    "kunnen", "kan", "kunt", "kan", "kunnen", "kon", "konden", "gekund",
    # moeten
    "moeten", "moet", "moeten", "moest", "moesten", "gemoeten",
    # willen
    "willen", "wil", "wilt", "wil", "willen", "wilde", "wilden", "gewild",
    # zullen
    "zullen", "zal", "zult", "zal", "zullen", "zou", "zouden",
    # mogen
    "mogen", "mag", "mogen", "mocht", "mochten", "gemogen",
    # laten (causatief)
    "laten", "laat", "laten", "liet", "lieten", "gelaten",
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
    "aux_zijn": sorted(AUX_ZIJN),
    "aux_hebben": sorted(AUX_HEBBEN),
    "modals_full": sorted(MODAL_VERBS),
}

data = {
    "name": "Dutch – 21st century",
    "language": "nl",
    "period": "21c",
    "categories": categories,
}
