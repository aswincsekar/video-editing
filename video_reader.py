"""
Funtions to read, crop video frames
"""
from __future__ import division
import subprocess as sp
import json
import numpy
import uuid
from PIL import Image
import os

# example subprocess
# ret = subprocess.call(["ls", "-la"])
# print ret

FFMPEG_BIN = "ffmpeg"
FFPROBE_BIN = "ffprobe"


def frame_size(input_file):
    """
    Get video frame_size
    eg : ffprobe -v error -show_entries stream=width,height \
          -of default=noprint_wrappers=1
    """
    command = [FFPROBE_BIN,
               '-v', 'error',
               '-show_entries', 'stream=width,height',
               '-of', 'default=noprint_wrappers=1',
               '-print_format', 'json',
               input_file]
    output = sp.check_output(command)
    output = json.loads(output)
    output = output['streams'][0]
    return output


def frame_reader(input_file, time):
    """
    Given framenumber return the frame
    eg :
    i = vr.frame_reader('/home/aswin/Videos/BACKUP/smoking videos/8 Year Old \
    Boy Smokes  8 Jahre Alter Junge Raucht_0.mp4', '0.19446', 1)
    """
    command = [FFMPEG_BIN,
               '-i', input_file,
               '-ss', time,
               '-vframes', '1',
               '-f', 'image2pipe',
               '-pix_fmt', 'rgb24',
               '-vcodec', 'rawvideo', '-']
    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)
    # take the size from the frame_size
    size = frame_size(input_file)
    raw_image = pipe.stdout.read(size['width']*size['height']*3)
    # transform the byte read into a numpy array
    image = numpy.fromstring(raw_image, dtype='uint8')
    image = image.reshape((size['height'], size['width'], 3))
    # throw away the data in the pipe's buffer.
    pipe.stdout.flush()
    pipe.terminate()
    im = Image.fromarray(image)
    return im


def get_tag_area(input_file, time, tag_area, bugs, offset=111.319):
    """
    Given the Video and a Tag area get the clip
    """
    frame = frame_reader(input_file, time)
    size = frame_size(input_file)
    ratio = size['height']/400
    if bugs:
        tag_area[0] -= offset
    new_tags = list(map(lambda x: x*ratio, tag_area))
    cropped = frame.crop((new_tags[0], new_tags[1], new_tags[0] + new_tags[2], new_tags[1] + new_tags[2]))
    return [cropped, new_tags]


def get_all(input_file, tags, dest_path, bugs, offset):
    """
    Get all the clips and store them somewhere
    """
    count = 0
    for tag in tags:
        tag_area = [tag['box']['left'], tag['box']['top'], tag['box']['edge']]
        [im, t] = get_tag_area(input_file, str(tag['time']), tag_area, bugs, offset)
        filename = str(uuid.uuid4())+'.png'
        paths = os.path.join(dest_path, filename)
        print(paths)
        im.save(paths)


def change_tag_file(input_file, tag_file, dest_path):
    """
    Get the tags and the offset from the tag file
    """
    ratio = 0
    offset = 0
    bugs = True
    with open(tag_file) as tf:
        data = json.load(tf)
        size = frame_size(input_file)
        ratio = size['height']/400
        altered_width = size['width']/ratio
        offset = (data['width'] - altered_width)/2
        get_all(input_file, data['tags'], dest_path, bugs, offset)
