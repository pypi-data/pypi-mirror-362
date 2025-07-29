"""
This is how detected scenes on a video look like when
doing 'print(scene_manager.get_scene_list())':

(00:00:00.000 [frame=0, fps=25.000], 00:00:01.240 [frame=31, fps=25.000])
(00:00:01.240 [frame=31, fps=25.000], 00:00:14.720 [frame=368, fps=25.000])
(00:00:14.720 [frame=368, fps=25.000], 00:00:15.880 [frame=397, fps=25.000])
(00:00:15.880 [frame=397, fps=25.000], 00:00:17.320 [frame=433, fps=25.000])
(00:00:17.320 [frame=433, fps=25.000], 00:00:28.960 [frame=724, fps=25.000])
(00:00:28.960 [frame=724, fps=25.000], 00:00:30.400 [frame=760, fps=25.000])
(00:00:30.400 [frame=760, fps=25.000], 00:01:00.040 [frame=1501, fps=25.000])

As you can see, one scene is a pair of time moments 
and frames, but I think they are actually wrong 
because the end of a scene should be one frame before
the start of the next one.
"""
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
from yta_image.description.descriptor import BlipImageDescriptor
from yta_programming.output import Output
from yta_constants.file import FileExtension
from moviepy.Clip import Clip
from scenedetect import open_video, SceneManager, ContentDetector
from scenedetect.scene_manager import save_images
from typing import Union
from imageio import imsave


# TODO: Turn this into a class and make it possible
# to store in attributes the information and to 
# save images to be able to identify it easy
# TODO: This is an advanced feature, so
# move to an advanced video library

class VideoScene:
    """
    A class that represent a video scene detected
    by the scene detector.
    """

    video_filename: str = None
    start_time: float = None
    end_time: float = None
    first_frame_number: int = None 
    last_frame_number: int = None
    _first_frame: 'Image' = None
    _last_frame: 'Image' = None

    def __init__(
        self,
        video_filename: str,
        start_time: float,
        end_time: float,
        first_frame_number: int,
        last_frame_number: int
    ):
        # TODO: Make some checkings
        self.video_filename = video_filename
        self.start_time = start_time
        # TODO: I think that the end_time is not okay, it
        # must be 1 frame before because it is actually
        # the next scene first moment, so it is out of this
        # scene. And this is actually failing because it is
        # giving as the end of the last scene of a video 
        # that lasts 1 second exactly (with fps = 25) a 
        # time of 60.04 and a frame of 1501 which is
        # not possible.
        self.end_time = end_time
        self.first_frame_number = first_frame_number
        self.last_frame_number = last_frame_number

    def __str__(
        self
    ):
        return f'[{str(self.start_time)} (frame = {str(self.first_frame_number)}), {str(self.end_time)} (frame = {str(self.last_frame_number)})]'
    
    @property
    def first_frame(
        self
    ):
        if self._first_frame is None:
            self._first_frame = VideoFrameExtractor.get_frame_by_t(self.video_filename, self.start_time)

        return self._first_frame
    
    @property
    def last_frame(
        self
    ):
        if self._last_frame is None:
            self._last_frame = VideoFrameExtractor.get_frame_by_t(self.video_filename, self.end_time)

        return self._last_frame
    
    # TODO: Maybe a property (?)
    def describe(
        self
    ):
        """
        Describe a frame of the scene.
        """
        frame_in_the_middle = int((self.first_frame_number + self.last_frame_number) / 2)
        image = VideoFrameExtractor.get_frame_by_index(self.video_filename, frame_in_the_middle)

        # TODO: The limits are not good images to describe
        return BlipImageDescriptor().describe(image)
    
    def save_first_image(
        self,
        output_filename: Union[str, None] = None
    ):
        """
        Save the first image of the scene to the provided
        'output_filename' (or to a temporary file if not
        provided). This method returns the final filename
        that has been used to store the image.
        """
        output_filename = Output.get_filename(output_filename, FileExtension.PNG)

        # TODO: Create a better way to write an output
        # that detects the type of object it is receiving
        # and acts consequently
        imsave(output_filename, self.first_frame)

        return output_filename
    
    def save_last_image(
        self,
        output_filename: Union[str, None] = None
    ):
        """
        Save the last image of the scene to the provided
        'output_filename' (or to a temporary file if not
        provided). This method returns the final filename
        that has been used to store the image.
        """
        output_filename = Output.get_filename(output_filename, FileExtension.PNG)

        # TODO: Create a better way to write an output
        # that detects the type of object it is receiving
        # and acts consequently
        imsave(output_filename, self.last_frame)

        return output_filename

class VideoScenes:
    """
    Class that represent the scenes of a video by using
    a scene detector that detects all the different
    scenes based on a threshold and on consecutive frames
    variation.
    """

    video_filename: str = None
    _scenes: list[VideoScene] = None

    @property
    def scenes(
        self
    ):
        """
        All the different scenes found in the video.
        """
        self._scenes = (
            self._detect_scenes()
            if self._scenes is None else
            self._scenes
        )

        return self._scenes

    def __init__(
        self,
        video_filename: str
    ):
        # TODO: Check if video is not filename
        self.video_filename = video_filename

    def _detect_scenes(
        self
    ):
        video = open_video(self.video_filename, backend = 'moviepy')

        scene_manager = SceneManager()
        scene_manager.add_detector(ContentDetector(threshold = 20))  # 27 is recommended
        scene_manager.detect_scenes(video)

        return [
            VideoScene(
                video_filename = self.video_filename,
                start_time = scene[0].get_seconds(),
                end_time = scene[1].get_seconds(),
                first_frame_number = scene[0].get_frames(),
                last_frame_number = scene[1].get_frames()
            ) for scene in scene_manager.get_scene_list()
            # This is how a scene looks like when printing it:
            # (00:00:00.000 [frame=0, fps=25.000], 00:00:01.240 [frame=31, fps=25.000])
        ]

    # TODO: This should be done by each VideoScene and
    # in another way, manually better, from the original
    # video extracting the grames, I think.
    def save_scenes_images(
        self,
        output_dirname: str
    ):
        # TODO: Check that dirname exist
        save_images(
            self.scenes,
            # TODO: Where does this 'video_manager' come from?
            video_manager,
            num_images = 1,
            image_name_template = '$SCENE_NUMBER',
            output_dir = output_dirname
        )

    def __str__(
        self
    ):
        return '\n'.join([
            scene.__str__()
            for scene in self.scenes
        ])


def detect_scenes_from_video(
    video: Clip
):
    """
    Detect the different scenes in the provided 'video'
    (that must be or have a valid filename) based on 
    ambient change (I mean it detects the scene change
    according to color change, etc.).

    This method returns a narray containing the different
    scenes with both 'start' and 'end' fields. Each of
    those fields include a 'second' and 'frame' sub field.

    TODO: This link https://www.scenedetect.com/docs/latest/api.html#example says that
    there is a backend 'VideoStreamMoviePy' class to process it with moviepy. This is
    interesting to use in a clip, and not in a filename.
    """
    # TODO: This import is not working when on top, why (?)
    from scenedetect import SceneManager, ContentDetector

    # This comes from here: https://www.scenedetect.com/
    # Other project: https://github.com/slhck/scenecut-extractor (only ffmpeg)
    video = VideoParser.to_moviepy(video)
    # TODO: I think this has to be a path so it is not able to
    # detect scenes from a video in memory (?)

    # Explained here: https://web.archive.org/web/20160316124732/http://www.bcastell.com/tech-articles/pyscenedetect-tutorial-part-2/

    # TODO: Check if thiss 'filename' includes the abspath
    video = open_video(video.filename, backend = 'moviepy')
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold = 27))  # 27 is recommended
    scene_manager.detect_scenes(video)

    return [
        {
            'start': {
                'second': scene[0].get_seconds(),
                'frame': scene[0].get_frames()
            },
            'end': {
                'second': scene[1].get_seconds(),
                'frame': scene[1].get_frames()
            }
        }
        for scene in scene_manager.get_scene_list()
    ]

    # This code below is working but it is quite old
    
    from scenedetect import VideoManager, SceneManager, StatsManager
    from scenedetect.detectors import ContentDetector
    from scenedetect.scene_manager import save_images, write_scene_list_html

    video_manager = VideoManager([video_filename])
    stats_manager = StatsManager()
    scene_manager = SceneManager(stats_manager)

    scene_manager.add_detector(ContentDetector(threshold = 30))
    video_manager.set_downscale_factor()

    video_manager.start()
    scene_manager.detect_scenes(frame_source = video_manager)

    scenes = scene_manager.get_scene_list()
    print(f'{len(scenes)} scenes detected!')

    save_images(
        scenes,
        video_manager,
        num_images = 1,
        image_name_template = '$SCENE_NUMBER',
        output_dir = 'scenes')

    for scene in scenes:
        start, end = scene

        # your code
        print(f'{start.get_seconds()} - {end.get_seconds()}')

    return scenes


# This is to work with abruptness and sooness (https://moviepy.readthedocs.io/en/latest/ref/videofx/moviepy.video.fx.all.accel_decel.html)
    
# I previously had 4.4.2 decorator for moviepy. I forced 4.0.2 and it is apparently working

"""
Interesting:
- https://www.youtube.com/watch?v=Ex1kuxe6jRg (el canal entero tiene buena pinta)
- https://www.youtube.com/watch?v=m6chqKlhpPo Echarle un vistazo a ese tutorial
- https://zulko.github.io/moviepy/ref/videofx.html
- https://stackoverflow.com/questions/48491070/how-to-flip-an-mp4-video-horizontally-in-python
"""
