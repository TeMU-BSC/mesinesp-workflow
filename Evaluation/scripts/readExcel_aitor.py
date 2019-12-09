'''author: Aitor'''

import os
import xlrd
import glob
import pprint
from math import floor



def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# pp = pprint.PrettyPrinter(indent=4)


#### LOADING ####
path = 'submissions'
files = [f for f in glob.glob(path + "**/*.xlsx", recursive=True)]


list_of_annotators = []

for f in files:

    wb = xlrd.open_workbook(f)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    list_of_documents = []

    for col in range(1, sheet.ncols):

        doc_id = ""
        decs = set()

        for row in range(sheet.nrows):
            if row == 0:
                doc_id = str(floor(sheet.cell_value(row, col)))
                # print(sheet.cell_value(row, col))
            elif 1 < row < 17:
                # if str(sheet.cell_value(row, col)) == "X":  # Aitor: Only compares to UPPERCASED "X" (some annotators typed lowercased "x")
                if str(sheet.cell_value(row, col)) in "Xx":  # Alejandro: Takes into account X and x
                    precod = sheet.cell_value(row, 0).split(" ")[0]
                    decs.add(int(precod))
            elif row >= 17:
                string = sheet.cell_value(row, col)
                if string:
                    if isfloat(string):
                        decs.add(int(floor(float(string))))
                    else:
                        decs.add(int(floor(float(string))))

        document = {'id': doc_id, 'decs': set(decs)}
        list_of_documents.append(document)

    annotator = {'id': os.path.splitext(os.path.basename(f))[0], 'docs': list_of_documents}
    # pp.pprint(annotator)
    list_of_annotators.append(annotator)

#### ALL LOADED ####
for annotator_1 in list_of_annotators:
    print(annotator_1['id'])
    ann_iaa = []
    for doc_1 in annotator_1['docs']:
        doc_iaa = []
        for annotator_2 in list_of_annotators:
            if annotator_1['id'] != annotator_2['id']:
                for doc_2 in annotator_2['docs']:
                    if doc_1['id'] == doc_2['id']:
                        intersection = doc_1['decs'].intersection(doc_2['decs'])
                        union = doc_1['decs'].union(doc_2['decs'])
                        result = len(intersection)/len(union)
                        doc_iaa.append(result)
                        break
        if doc_iaa:
            result = sum(doc_iaa)/len(doc_iaa)
            print ('\t' + str(doc_1['id']) + ": {0:.3f}".format(result)
                   + " (average IAA with " + str(len(doc_iaa)) + " other annotators).")
            ann_iaa.append(result)
        else:
            print('\t' + str(doc_1['id']) + ": NA")

    if ann_iaa:
        result = sum(ann_iaa) / len(ann_iaa)
        print("\n\tTotal: {0:.3f}".format(result) + " (based on " + str(len(ann_iaa)) + " documents).")
    else:
        print("\n\tTotal: NA")
    print("\n------\n")
