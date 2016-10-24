"""
Test functions for video_reader methods
"""
import unittest
import video_reader as vr
from PIL import Image, ImageChops


class VideoReaderTest(unittest.TestCase):
    def test_frame_size(self):
        """
        Testing frame_size method from video_reader
        """
        output = vr.frame_size('smoking videos/8 Year Old Boy Smokes  8 Jahre Alter Junge Raucht_0.mp4')
        req = {"width": 1280, "height": 720}
        self.assertEqual(output, req)

    def test_frame_reader(self):
        """
        Testing frame_reader method from video_reader
        """
        filename = '/home/aswin/Videos/BACKUP/smoking videos/8 Year Old Boy Smokes  8 Jahre Alter Junge Raucht_0.mp4'
        time = '0.19446'
        im = vr.frame_reader(filename, time)
        real = Image.open('test.png')
        self.assertEqual(ImageChops.difference(im, real).getbbox(), None)

    def test_get_tag_area(self):
        """
        """
        filename = '/home/aswin/Videos/BACKUP/smoking videos/8 Year Old Boy Smokes  8 Jahre Alter Junge Raucht_0.mp4'
        time = '0.19446'
        [new_tag_window, new_tags] = vr.get_tag_area(filename, time, [292, 82, 249])
        real = [525.6, 147.6, 448.2]
        print new_tags, real
        im = vr.frame_reader(filename, time)
        im = im.crop((real[0], real[1], real[0] + real[2], real[1] + real[2]))
        im.save('test2.png')
        self.assertEqual(ImageChops.difference(im, new_tag_window).getbbox(), None)

if __name__ == '__main__':
    unittest.main()
