
# functionwordsets

_Comprehensive multilingual function-word datasets with a simple Python API_

[![DOI](https://zenodo.org/badge/1013331042.svg)](https://doi.org/10.5281/zenodo.15811953)

---

## Overview
`functionwordsets` ships ready-to-use **function-word lists** for many languages and time-periods.  
Each dataset is a tiny **Python module** located in `functionwordsets/datasets/` and is loaded on demand through a minimal API.

Supported out of the box :

| ID        | Language / period                    | Entries* |
|-----------|--------------------------------------|----------|
| `fr_21c`  | French – 21st century                | **688** |
| `en_21c`  | English – 21st century               | **390** |
| `sp_21c`  | Spanish – 21st century               | **481** |
| `it_21c`  | Italian – 21st century               | **495** |
| `nl_21c`  | Dutch – 21st century                 | **287** |
| `gr_5cbc` | Ancient Greek – 5th-4th c. BCE       | **264** |
| `oc_13c`  | Old Occitan – 12th-13th c.           | **360** |
| `la_1cbc` | Classical Latin – 1st c. BCE         | **353** |

\*Number of distinct word-forms in the union of all categories.

You can also add or fork your own datasets: just drop a `<id>.py` file following the template shown below.

---

## 💡 Supported grammatical categories
*(summary unchanged – see below for details)*

---

## Installation
```bash
pip install functionwordsets         # from PyPI
# or, from a cloned repo
pip install -e .
```
Python ≥ 3.8 – zero runtime dependencies – wheel < 20 kB zipped.

---

## Quick start
```python
import functionwordsets as fw

# List available datasets
print(fw.available_ids())            # ['fr_21c', 'en_21c', …]

# Load one set (defaults to fr_21c)
fr = fw.load()                       # same as fw.load('fr_21c')
print(fr.name, len(fr.all))          # French – 21st century 688

# Membership test
if 'ne' in fr.all:
    ...

# Build a custom stop-set: only articles + prepositions
stops = fr.subset(['articles', 'prepositions'])
```

### Command-line helpers
```bash
# List dataset IDs
fw-list

# Export every French function word to a text file
fw-export fr_21c -o fr.txt

# Export only conjunctions & negations from Spanish as JSON
fw-export sp_21c --include coord_conj subord_conj negations -o sp_stop.json
```

---

## Dataset layout

Internally each dataset is defined as a small Python dictionary:

```python
data = {
    "name": "English – 21st century",
    "language": "en",
    "period": "21c",
    "categories": {
        "articles": [...],
        "prepositions": [...],
        # …
    }
}
```
`functionwordsets` treats the object as read-only, so feel free to edit or extend it in your fork.

---

### Notes on auxiliary categories
Keys for auxiliary verbs follow the pattern `aux_<lemma>` (e.g. `aux_être`, `aux_be`, `aux_ser`). They vary by language; see each dataset file for the exact key.

---

Enjoy !
