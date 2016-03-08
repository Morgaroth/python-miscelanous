import argparse

__author__ = 'mateusz'

parser = argparse.ArgumentParser(description='Converts images to smaller size & creates gifs.')
parser.add_argument('fps', metavar='fpss', type=float, nargs='+',
                    help='list of frames per second for creating gifs')
parser.add_argument('-r', '--resize', type=int, metavar='percents',
                    help='resize ratio in percents to resize images before create gif.')
parser.add_argument('-s', '--max-size', type=float, metavar='max_size',
                    help='if passed, images will be resized to rich passed size.')
args = parser.parse_args()
print(args)
