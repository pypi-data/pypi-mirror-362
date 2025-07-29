ARTICLES_DETERMINERS = sorted({
    # definite singular/plural with historical spellings
    "lo", "lu", "li", "la", "las", "los", "ls",
    # indefinite
    "un", "una", "uns", "unas",
    # demonstratives / determiners
    "aquest", "aquesta", "aqueste", "aquestas", "aquestes",
    "aquel", "aqueu", "aquella", "aqueles", "aqueles", "aquels", "aquelas",
    "cel", "cela", "cels", "celas", "celes",
    # quantifiers
    "tot", "tota", "tots", "totz", "totas",
    "cada", "cadun", "caduna",
    "alguns", "algun", "algunas", "alguna",
    "negun", "neguna", "negunas",
    "divers", "diverses", "altres", "autre", "autra", "altres",
})

POSSESSIVE_DETERMINERS = sorted({
    "mon", "ma", "mos", "mes",
    "ton", "ta", "tos", "tes",
    "son", "sa", "sos", "ses",
    "nostre", "nostra", "nostres", "nostras",
    "vostre", "vostra", "vostres", "vostras",
    "lor", "lors",
})

PERSONAL_PRONOUNS = sorted({
    # tonic / subject historical variants
    "ieu", "eu", "tu", "vos", "vosautres",
    "el", "il", "ela", "nos", "nosautres", "els", "eles",
    # clitic object pronouns (variants incl. enclitic -z/-s)
    "me", "m'", "te", "t'", "se", "s'",
    "lo", "l'", "lui", "la", "los", "ls", "las",
    "li", "lor", "en", "n'",
})

POSSESSIVE_PRONOUNS = sorted({
    "lo mieu", "la mia", "los mieus", "las mias",
    "lo to", "la tua", "los tos", "las tas",
    "lo sieu", "la sieua", "los sieus", "las sieus",
    "lo nòstre", "la nòstra", "los nòstres", "las nòstras",
    "lo vòstre", "la vòstra", "los vòstres", "las vòstras",
    "lo lor", "la lor", "los lors", "las lors",
})

DEMONSTRATIVE_PRONOUNS = sorted({
    "aquest", "aquesta", "aqueles", "aqueste", "aquestas",
    "aquel", "aquels", "aqueles", "aquelas",
    "cel", "cela", "cels", "celas",
    "ço", "so",  # neuter demonstrative
})

INDEFINITE_PRONOUNS = sorted({
    "qualc", "qualqu", "qualcun", "qualcuna",
    "quine", "quines", "quicòm", "quicom",
    "qualsevol", "res", "ren", "rien",
    "negun", "neguna", "neguns", "negunas",
    "cadun", "caduna",
    "tots", "totas", "tuit", "tuitz",
    "d'autras", "d'autres",
})

INTERROGATIVE_PRONOUNS = sorted({
    "qui", "cui", "que", "qu'", "quic", "qual",
    "cals", "cau", "cossí", "ont", "on", "quand", "quant", "perqué", "per que",
})

PREPOSITIONS = sorted({
    "a", "ab", "amb", "am", "d'", "de", "del", "dels",
    "dins", "en", "entre", "per", "pels", "pel", "per", "sens", "sensa",
    "sus", "sobre", "jos", "sota",
    "vers", "contra", "fins", "fins a", "fins que",
    "aprés", "avant", "abans", "davant", "darrere", "tras", "entre",
})

COORD_CONJUNCTIONS = sorted({
    "e", "et", "o", "u", "ni", "mas", "mais", "pues", "pus", "car",
})

SUBORD_CONJUNCTIONS = sorted({
    "que", "cuy", "si", "s'", "perque", "puoisque", "puesque", "puois",
    "quan", "quand", "cant", "mentre", "mentre que",
    "abans que", "aprés que", "fin que", "tant que", "tro que",
    "com", "coma", "soi que",
})

ADVERBS = sorted({
    # place
    "aicí", "aissi", "aci", "lai", "ailà", "alhors",
    # time
    "ara", "adés", "ia", "ja", "iam", "enci", "encara", "totjorn",
    "sempre", "jamai", "onc", "nunca",
    # manner / degree
    "ben", "plan", "mal", "mala", "pauc", "pro", "massa", "molt", "força",
    "tot", "quasi",
    # discourse / emphasis
    "certes", "segur", "vertat", "soi", "doncs", "donc", "pus", "anc",
})

ADV_LOCUTIONS = sorted({
    "d'un còp", "d'un' ora", "a la fina", "de tant en tant",
    "en aquest temps", "d'ara enlà", "mòrtz e vius", "tot aplech",
    "tanostant", "aissi doncs", "a lop de jorn", "a lurs jorns",
})

NEGATIONS = sorted({
    "non", "no", "ne", "pas", "pauc", "res", "ren", "negun", "jamai",
})

AUX_ESSER = sorted({
    "esser", "èsser", "sui", "si", "es", "es", "som", "sèm", "sètz", "son", "sont",
    "fui", "fo", "fos", "fostz", "foron",
    "er", "era", "eran",
})

AUX_AVER = sorted({
    "aver", "aure", "ai", "as", "a", "avem", "avetz", "an",
    "ague", "agues", "aguet", "aguem", "aguetz", "agueren",
    "avia", "aviatz", "avian",
})

MODAL_VERBS = sorted({
    # poder
    "poder", "puc", "potes", "pot", "podem", "podetz", "pòdon",
    # voler
    "voler", "vuelh", "vòl", "vol", "volèm", "voletz", "vòlon",
    "volia", "volian",
    # dever/debre
    "dever", "debre", "deu", "deus", "devetz", "devon", "devei",
    # saber
    "saber", "sai", "saps", "sap", "sabem", "sabetz", "sàbon",
})

categories = {
    "articles": ARTICLES_DETERMINERS,
    "poss_det": POSSESSIVE_DETERMINERS,
    "pers_pron": PERSONAL_PRONOUNS,
    "poss_pron": POSSESSIVE_PRONOUNS,
    "dem_pron": DEMONSTRATIVE_PRONOUNS,
    "indef_pron": INDEFINITE_PRONOUNS,
    "inter_pron": INTERROGATIVE_PRONOUNS,
    "prepositions": PREPOSITIONS,
    "coord_conj": COORD_CONJUNCTIONS,
    "subord_conj": SUBORD_CONJUNCTIONS,
    "adverbs": ADVERBS,
    "adv_locutions": ADV_LOCUTIONS,
    "negations": NEGATIONS,
    "aux_esser": AUX_ESSER,
    "aux_aver": AUX_AVER,
    "modals_full": MODAL_VERBS,
}

data = {
    "name": "Old Occitan (langue d'oc) — 12th-13th c.",
    "language": "oc",
    "period": "12-13c",
    "categories": categories,
}
