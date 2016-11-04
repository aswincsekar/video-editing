"""
Count number of tags by video name and also push them to a spreadsheet
command example:
calculate_tags <tags_source_folder_path>
"""
import sys
import os
import glob
import json


print("arguments : ", sys.argv)

base_path = os.path.dirname(os.path.abspath(__file__))
print(base_path)

tags_source_path = sys.argv[1]
# tags_source_path = os.path.join(base_path, tags_source_path)
print(tags_source_path)

file_list = glob.glob(tags_source_path+"*.json")
print(file_list)
total_tags = 0
for file in file_list:
    print(file)
    with open(file) as filestream:
        data = json.load(filestream)
        # print(data['tags'])
        print("length : "+str(len(data['tags'])))
        total_tags = total_tags + len(data['tags'])

print('oyo total tags :' + str(total_tags))

