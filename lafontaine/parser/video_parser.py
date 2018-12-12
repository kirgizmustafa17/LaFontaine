from lafontaine.parser.scene import Scene
from lafontaine.parser.frame import Frame
from lafontaine.feature_detector.feature_director import FeatureDirector
from lafontaine.parser.video_stats import VideoStats
from moviepy.editor import VideoFileClip


class VideoParser:
    def __init__(self, video_path):
        self.video = VideoFileClip(video_path)
        self.audio = self.video.audio
        self.duration = self.video.duration
        self.video_stats = VideoStats(self.video.fps, self.video.w, self.video.h)

    def get_scenes(self, feature_director: FeatureDirector):
        scenes = []
        current_scene = None
        countdown = None
        recording = False

        for t, raw_img in self.video.iter_frames(with_times=True):
            audio_frame = self.audio.get_frame(t)

            percent = (100 / self.duration) * t
            print(f"Processing frame at {t:.2f}. {percent:.2f}%")

            frame = Frame(raw_img, audio_frame, t)

            result = feature_director.check_for_all_features(frame)

            if countdown and countdown < 0:
                recording = False
                scenes.append(current_scene)
                current_scene = None
                countdown = None

            if recording:
                current_scene.add_frame(frame)
                countdown -= 1
            else:
                if result and result.result is True:
                    if current_scene is None:
                        current_scene = Scene()
                    recording = True
                    countdown = result.frames
                    current_scene.add_frame(frame)

        if current_scene is not None:
            scenes.append(current_scene)

        return scenes
