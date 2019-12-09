'''
Script to extract the data from the Excel files with DeCS indexings for MESINESP task.

Author: alejandro.asensio@bsc.es

Usage:
$ python extract_indexings.py
'''

import json

import excel_utils


# EXCELS_DIR = 'test'
EXCELS_DIR = 'submissions'

# Test
# indexings = {
#     'file1': {'1': [10, 11], '2': [20, 21], '4': [40, 41]},
#     'file2': {'1': [12, 13], '3': [30, 31], '4': [40, 42]},
#     'file3': {'1': [10, 13], '2': [20, 22], '3': [30, 32]}
# }

# Real data
indexings = excel_utils.extract_indexings_from_excels_dir(EXCELS_DIR)
print(json.dumps(indexings))


# UNDERSTANDING RESULTS WITH ANTONIO
# -----------------------------------------------------------------------------

# list_of_annotators = extract_data_from_excels_dir(EXCELS_DIR)
# #### ALL LOADED ####
# print('MACRO: ')
# for annotator_1 in list_of_annotators:
#     print(annotator_1['id'])
#     ann_iaa = []
#     for doc_1 in annotator_1['docs']:
#         doc_iaa = []
#         for annotator_2 in list_of_annotators:
#             if annotator_1['id'] != annotator_2['id']:
#                 for doc_2 in annotator_2['docs']:
#                     if doc_1['id'] == doc_2['id']:
#                         intersection = set(doc_1['decs']).intersection(set(doc_2['decs']))
#                         union = set(doc_1['decs']).union(set(doc_2['decs']))
#                         result = len(intersection)/len(union)
#                         doc_iaa.append(result)
#                         break
#         if doc_iaa:
#             result = sum(doc_iaa)/len(doc_iaa)
#             print ('\t' + str(doc_1['id']) + ": {0:.3f}".format(result)
#                    + " (average IAA with " + str(len(doc_iaa)) + " other annotators).")
#             ann_iaa.append(result)
#         else:
#             print('\t' + str(doc_1['id']) + ": NA")

#     if ann_iaa:
#         result = sum(ann_iaa) / len(ann_iaa)
#         print("\n\tTotal: {0:.3f}".format(result) + " (based on " + str(len(ann_iaa)) + " documents).")
#     else:
#         print("\n\tTotal: NA")
#     print("\n------\n")


# print('----------------------------------------')
# print('MICRO: ')
# for annotator_1 in list_of_annotators:
#     print(annotator_1['id'])
#     ann_iaa = []
#     for doc_1 in annotator_1['docs']:
#         for annotator_2 in list_of_annotators:
#             if annotator_1['id'] != annotator_2['id']:
#                 for doc_2 in annotator_2['docs']:
#                     if doc_1['id'] == doc_2['id']:
#                         intersection = set(doc_1['decs']).intersection(set(doc_2['decs']))
#                         union = set(doc_1['decs']).union(set(doc_2['decs']))
#                         result = len(intersection)/len(union)
#                         ann_iaa.append(result)
#                         break

#     if ann_iaa:
#         result = sum(ann_iaa) / len(ann_iaa)
#         print("\n\tTotal: {0:.3f}".format(result) + " (based on " + str(len(ann_iaa)) + " documents).")
#     else:
#         print("\n\tTotal: NA")
#     print("\n------\n")
