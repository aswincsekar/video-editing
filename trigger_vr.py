import video_reader as vr
import sys
import os
import json
import glob
import termcolor
import timeit


filepath = sys.argv[1]
tag_filepath = sys.argv[2]
source_dest = sys.argv[3]
mode = sys.argv[4]

print(sys.argv)

# count of failed file reads
tag_count = 0
file_fail_count = 0
total_count = 0
file_count = 0
if mode == '1':
    search_path = os.path.join(tag_filepath, '*.json')
    # print(glob.glob(search_path))
    # tags = os.listdir(tag_filepath)
    tags = glob.glob(search_path)
    base_path = os.path.dirname(os.path.abspath(__file__))

    for tag in tags:
        # print tag
        tag_file = os.path.join(base_path, tag)
        with open(tag_file) as tf:
            data = json.load(tf)
            total_tags = len(data['tags'])
        total_count += total_tags
        file_count += 1
        print( termcolor.colored("file count :"+str(file_count),'yellow'))
        with open(tag_file) as tg:
            data = json.load(tg)
            title = data['title']
        filename = os.path.join(base_path, filepath, title)
        print ("file : " + title)
        if os.path.isfile(filename):
            try:
                start_time = timeit.default_timer()
                count = vr.change_tag_file(filename, tag_file, source_dest)
                elapsed = timeit.default_timer() - start_time
                print(termcolor.colored('elapsed time :','green') + str(elapsed))
                tag_count += count
            except:
                print (termcolor.colored(" Tagging Failed ", 'red'))
                raise
        else :
            print (termcolor.colored(" Video File Not Found ", 'red'))
            file_fail_count += 1

        print(termcolor.colored('File FAIL COUNT', 'green')+" : "+str(file_fail_count))
        print(termcolor.colored('Tag COUNT', 'green') + " : " + str(tag_count))
        print(termcolor.colored('Total Tag COUNT', 'green') + " : " + str(total_count))

elif mode == '0':
    try:
        vr.change_tag_file(filepath, tag_filepath, source_dest)
    except:
        print "momo"
        pass

print('oyo done')
