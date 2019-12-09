'''
Util functions to analyze Excel files for the initial phase of indexers'
selection for MESINESP task.

Author: alejandro.asensio@bsc.es
Based on the original script made by: aitor.gonzalez@bsc.es
'''

import re
import os
import xlrd
from typing import List


# EXCELS_DIR = 'test'
EXCELS_DIR = 'submissions'

# Minimum presence of each DeCS among other annotators that have annotated the
# same document, in order to make suggestions to other annotators.
THRESHOLD = 0.2


def read_excel_file(filename: str) -> List[list]:
    '''Return a list with the rows in the Excel file.
    Each row is a list with its cells as its elements.
    Source: https://stackoverflow.com/a/20105297
    '''
    wb = xlrd.open_workbook(filename)
    # sh = wb.sheet_by_name('Sheet1')
    sh = wb.sheet_by_index(0)
    all_rows = [sh.row_values(rownum) for rownum in range(sh.nrows)]
    return all_rows


def parse_excel_file(filename: str) -> dict:
    '''Return an indexed doc object.'''

    # Get all rows from the Excel file
    all_rows = read_excel_file(filename)

    # Purge empty lines and the final row (num. 200) starting with 'BSC-2019' string
    data_rows = [row for row in all_rows if not ('' in set(row) and len(set(row)) == 1 or row[0] == 'BSC-2019')]

    # Define the different row categories inside the Excel files
    docIds = data_rows[0]
    difficulties = data_rows[1]
    middle_rows = data_rows[2:17]
    final_rows = data_rows[17:]

    # Construct the result list
    docs = dict()
    for i, docId in enumerate(docIds):
        try:
            # Try to convert the docId into an integer
            docId = int(docId)

            # Get the decsCodes only for those rows with an "X" or "x"
            precoded_decs = [int(re.match('^\d+', middle_row[0]).group(0)) for middle_row in middle_rows if middle_row[i].upper() == 'X']
            
            # Get the decsCodes typed in manually
            manual_decs = [int(decsCodes[i]) for decsCodes in final_rows if decsCodes[i] != '']
            indexed_doc = {str(docId): precoded_decs + manual_decs}
            docs.update(indexed_doc)
        except Exception:
            pass

    return docs


def extract_indexings_from_excels_dir(excels_dir: str) -> dict:
    '''Extract the DeCS codes from Excel files inside excel_dir input directory name.'''
    indexings = dict()
    for root, dirs, files in os.walk(excels_dir):
        for filename in files:
            if filename.endswith('.xlsx'):
                filename_relative_path = os.path.join(root, filename)
                indexings[filename] = parse_excel_file(filename_relative_path)
    return indexings
