import re
from nltk.stem import PorterStemmer
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
ps = PorterStemmer()
source_file_name = "200_title.txt"
output_file_dictionary_name = "dictionary.txt"
output_file_postings_name = "postings.txt"

def tokenizer(array):
    term_pair = [] #general pair for 2 step (with term,  docid)
    word_pair = [] #sort pair without docid
    sort_pair = [] #sort pair for 3 step( with term,  docid)
    merge_item = {} # merge pair for 4 step(with term, df, posting-list)
    for index, row in enumerate(array):
        content_array = row.split(' ')
        for word_index, word in enumerate(content_array):
            pair = []
            result_word = re.sub('[^A-Za-z0-9]+', '', word)
            result_word = result_word.lower()
            result_word = ps.stem(result_word)
            pair.append(result_word)
            pair.append(index)
            word_pair.append(result_word)
            term_pair.append(pair)

    for index, row in enumerate(term_pair):
        if term_pair[index][0] == "":
            del term_pair[index]
    for index, row in enumerate(word_pair):
        if word_pair[index] == "":
            del word_pair[index]
    # step 2 generate term pairs and step 3 sort pairs
    word_pair.sort()
    for index, row in enumerate(word_pair):
        _pair = []
        for delta, item in enumerate(term_pair):
            if row is item[0]:
                _pair.append(row)
                _pair.append(item[1])
        sort_pair.append(_pair)
    # merge for step 3
    for index, row in enumerate(term_pair):
        df = 1
        posting_list = {}
        posting_list[row[1]] = 1
        merge_pair = (row[0], df, posting_list)
        if merge_item.get(row[0]):
            newvalue = merge_item.get(row[0])[1] + 1
            new_posting_list = merge_item[row[0]][2]
            if new_posting_list.get(row[1]):
                value = merge_item[row[0]][2]
                new_posting_list[row[1]] = value[row[1]] + 1
            else:
                new_posting_list[row[1]] = 1
            _merge_pair = (row[0], newvalue, new_posting_list)
            merge_item[row[0]] = _merge_pair
        else:
            merge_item[row[0]] = merge_pair

    for index, row in enumerate(sort_pair):
        if sort_pair[index][0] == "":
            del sort_pair[index]
    output_file_dictionary = open(output_file_dictionary_name, 'w')
    output_file_postings = open(output_file_postings_name, 'w')

    array_posting = []
    for row in merge_item:
        posting = merge_item[row][2]
        for item in posting:
            _array = []
            _array.append(item)
            _array.append(posting[item])
            # for x in range(posting[item]):
            array_posting.append(_array)
    array_dictionary = []
    offset = 0
    for row in merge_item:
        _array = []
        _array.append(row)
        _array.append(merge_item[row][1])
        _array.append(offset)
        offset = offset + merge_item[row][2].__len__()
        array_dictionary.append(_array)
    # array_posting = sorted(array_posting, key=lambda x: x[0], reverse=False)
    np.savetxt(output_file_postings_name, np.array(array_posting), fmt="%s")
    np.savetxt(output_file_dictionary_name, np.array(array_dictionary), fmt="%s")
    # array_posting.append(merge_item[])
try:
    source_file = open(source_file_name, 'r')
    source_array = []
    for index, row in enumerate(source_file):
        source_array.append(row)
    source_file.close()
    try:
        tokenizer(source_array)
    except:
        print("Tokenizer error!")
except:
    print(source_file_name + " file doesn't exit. Please check it out!")

