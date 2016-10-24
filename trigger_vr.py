import video_reader as vr
import sys
import os
import json
import glob
import termcolor

filepath = sys.argv[1]
tag_filepath = sys.argv[2]
source_dest = sys.argv[3]
mode = sys.argv[4]

print(sys.argv)

# count of failed file reads
fail_count = 0

if mode == '1':
    search_path = os.path.join(tag_filepath, '*.json')
    print(glob.glob(search_path))
    # tags = os.listdir(tag_filepath)
    tags = glob.glob(search_path)
    base_path = os.path.dirname(os.path.abspath(__file__))

    for tag in tags:
        # print tag
        tag_file = os.path.join(base_path, tag)

        with open(tag_file) as tg:
            data = json.load(tg)
            title = data['title']
        filename = os.path.join(base_path, filepath, title)
        if os.path.isfile(filename):
            try:
                vr.change_tag_file(filename, tag_file, source_dest)
            except:
                print " Does N0T Exist"
                fail_count += 1
                pass
    print(termcolor.colored('FAIL COUNT', 'green')+" : "+str(fail_count))

elif mode == '0':
    try:
        vr.change_tag_file(filepath, tag_filepath, source_dest)
    except:
        print "momo"
        pass

print('oyo done')
