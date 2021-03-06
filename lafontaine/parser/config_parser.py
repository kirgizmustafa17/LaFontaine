import json
from datetime import timedelta

from lafontaine.feature_director.features.sound.sound_delta_detector import SoundDeltaDetector
from lafontaine.feature_director.feature_director import FeatureDirector
from lafontaine.feature_director.features.image.color_counter import ColorCounter
from lafontaine.feature_director.features.image.face_recognizer import FaceRecognizer
from lafontaine.feature_director.features.image.frame_delta_detector import FrameDeltaDetector
from lafontaine.feature_director.features.sound.high_volume_detector import HighVolumeDetector
from lafontaine.feature_director.features.sound.sound_peak_detector import SoundPeakDetector
from lafontaine.feature_director.features.subtitle.subtitle_conversation_count import SubtitleConversationCount
from lafontaine.feature_director.features.subtitle.subtitle_density_detector import SubtitleDensityDetector
from lafontaine.feature_director.features.subtitle.subtitle_intensity_detector import SubtitleIntensityDetector


class ConfigParser:
    @staticmethod
    def get_director_from_config(config: str, cuda: bool) -> FeatureDirector:
        all_features = []

        loaded = json.loads(config)
        features = loaded['features']
        genre = loaded['genre']
        max_length = int(loaded['max_length'])

        for feature in features:
            feature_id = feature['id']
            frames = feature['frames']

            # Image Features
            if feature_id == 'FaceRecognizer':
                face_count = feature['face_count']
                all_features.append(FaceRecognizer(face_count, frames, cuda))

            elif feature_id == 'ColorCounter':
                color_count = feature['color_count']
                all_features.append(ColorCounter(color_count, frames))

            elif feature_id == 'FrameDeltaDetector':
                delta = feature['delta']
                frame_limit = feature['frame_limit']
                change_limit = feature['scene_change_limit']
                all_features.append(FrameDeltaDetector(delta, change_limit, frame_limit, frames))

            # Sound Features
            elif feature_id == 'SoundPeakDetector':
                audio_threshold = feature['audio_threshold']
                all_features.append(SoundPeakDetector(audio_threshold, frames))

            elif feature_id == 'HighVolumeDetector':
                volume = feature['volume']
                frame_limit = feature['frame_limit']
                all_features.append(HighVolumeDetector(volume, frame_limit, frames))

            elif feature_id == 'SoundDeltaDetector':
                delta = feature['delta']
                frame_limit = feature['frame_limit']
                change_limit = feature['scene_change_limit']
                all_features.append(SoundDeltaDetector(delta, change_limit, frame_limit, frames))

            # Subtitle Features
            elif feature_id == 'SubtitleDensityDetector':
                char_count = feature['char_count']
                all_features.append(SubtitleDensityDetector(char_count, frames))

            elif feature_id == 'SubtitleIntensityDetector':
                char_count = feature['char_count']
                intensity_char = feature['intensity_char']
                all_features.append(SubtitleIntensityDetector(intensity_char, char_count, frames))

            elif feature_id == 'SubtitleConversationCount':
                conversation_count = feature['conversation_count']
                all_features.append(SubtitleConversationCount(conversation_count, frames))

        director = FeatureDirector(genre, timedelta(seconds=max_length), all_features)
        return director
