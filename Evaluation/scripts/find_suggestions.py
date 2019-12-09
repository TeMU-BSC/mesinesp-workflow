'''
Script to find the suggestions with missing DeCS in every document of each annotator for MESINESP task.

Author: alejandro.asensio@bsc.es

Usage:
$ python extract_indexings.py
'''

import json
from collections import defaultdict

import excel_utils


# EXCELS_DIR = 'test'
EXCELS_DIR = 'submissions'

# Minimum presence of each DeCS among other annotators that have annotated the
# same document, in order to make suggestions to other annotators.
THRESHOLD = 0.2

def get_decs_per_doc(indexings: dict) -> dict:
    '''Return all DeCS added for each doc, possibly containing duplicates.'''
    decs_per_doc = dict()
    for filename, docs in indexings.items():
        for doc, decs in docs.items():
            decs_per_doc.setdefault(doc, []).extend(decs)
    return decs_per_doc


def get_times_per_doc(indexings: dict) -> dict:
    '''Return the times a doc is annotated.'''
    times_per_doc = defaultdict(int)
    for filename, docs in indexings.items():
        for doc, decs in docs.items():
            times_per_doc[doc] += 1
    return times_per_doc


def get_suggestions(indexings: dict, decs_per_doc: dict, times_per_doc: dict, threshold: float) -> dict:
    '''Return the relevant missing DeCS in every doc for each annotator,
    regarding a minimum presence of the given threshold (percentage).'''
    suggestions = dict()
    for filename, docs in indexings.items():
        suggested_docs = dict()
        for doc, decs in docs.items():
            diff = set(decs_per_doc[doc]) - set(docs[doc])
            suggested_docs[doc] = []
            for item in diff:
                # print(item, decs_per_doc[doc].count(item) / times_per_doc[doc])
                if decs_per_doc[doc].count(item) / times_per_doc[doc] >= threshold:
                    suggested_docs[doc].append(item)
        suggestions[filename] = suggested_docs
    return suggestions


# Test
# indexings = {
#     'file1': {'1': [10, 11], '2': [20, 21], '4': [40, 41]},
#     'file2': {'1': [12, 13], '3': [30, 31], '4': [40, 42]},
#     'file3': {'1': [10, 13], '2': [20, 22], '3': [30, 32]}
# }

# Real data
indexings = excel_utils.extract_indexings_from_excels_dir(EXCELS_DIR)

# Find DeCS suggestions
decs_per_doc = get_decs_per_doc(indexings)
times_per_doc = get_times_per_doc(indexings)
suggestions = get_suggestions(indexings, decs_per_doc, times_per_doc, THRESHOLD)
print(json.dumps(suggestions))
