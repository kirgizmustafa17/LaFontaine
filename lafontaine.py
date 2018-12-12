
import argparse
import time
import pathlib
import os
from lafontaine.feature_detector.image.face_recognizer import FaceRecognizer
from lafontaine.feature_detector.sound.sound_peak_detector import SoundPeakDetector
from lafontaine.feature_detector.feature_director import FeatureDirector
from lafontaine.generator.video_generator import VideoGenerator
from lafontaine.parser.video_parser import VideoParser

parser = argparse.ArgumentParser(description='Generate trailers from movies')
parser.add_argument('-f', '--file', help='Path for the video', required=True)
args = vars(parser.parse_args())

path_to_video = args['file']


# Parsers
video_parser = VideoParser(path_to_video)

video_stats = video_parser.video_stats
print(f'Loaded {video_stats.width}x{video_stats.height} video with {video_stats.fps} FPS.')

start = time.time()
print('Started processing..')

feature_director = FeatureDirector(sound_features=[SoundPeakDetector(path_to_video)])
#feature_director = FeatureDirector(image_features=[FaceRecognizer(1)])

# Parse scenes
scenes = video_parser.get_scenes(feature_director)

end = time.time()
print(f'Finished processing. Took {end - start} seconds.')

print(f'Found {len(scenes)} scenes.')

# Generator
video_generator = VideoGenerator(path_to_video)

video_name = os.path.basename(path_to_video)
pathlib.Path(f'out/{video_name}').mkdir(exist_ok=True)

count = 0
for s in scenes:
    video_generator.generate_from_scene(s, f'out/{video_name}/scene{count}.mp4', video_stats.fps)
    count += 1

"""
Benchmarks
2018-12-03, No optimizations: Processing 30 second, 1024*768 video takes 292 seconds.
2018-12-10, Iterating with 1/10th of a second, processing a 30 second, 1024*768 video takes 140 seconds.
"""
