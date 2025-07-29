"""
Some tests I made with Manim (3D, as it is the most difficult):
- ImageMobject + Cairo works, but positioning gets crazy.
- ImageMobject + Opengl fails
- OpenGLImageMobject + Opengl works perfectly.
- VideoMobject (ImageMobject) + Cairo works, but positioning gets crazy.
- VideoMobject (ImageMobject) + Opengl fails
- VideoMobject (OpenGLImageMobject) + Opengl only shows the first frame, but positioning is perfect.
- Didn't test anything else
"""
from yta_video_manim.animations.base_manim_animation import BaseManimAnimation
from yta_video_manim.animations.base_manim_animation_wrapper import BaseManimAnimationWrapper
from yta_video_manim.animations.base_three_d_manim_animation import BaseThreeDManimAnimation
from yta_video_manim.animations.classes.video.mobjects.video_mobject import VideoMobject
from yta_video_manim.animations.classes.video.mobjects.video_opengl_mobject import VideoOpenGLMobject
from yta_video_manim.animations.classes.image.opengl_image_mobject import OpenGLImageMobject
from yta_constants.manim import ManimRenderer
from yta_validation.parameter import ParameterValidator
from yta_programming.output import Output
from yta_programming.decorators.requires_dependency import requires_dependency
from yta_constants.file import FileExtension
from manim import *
from typing import Union


class TestVideoMobjectIn2DManimAnimationWrapper(BaseManimAnimationWrapper):

    __test__ = False

    def __init__(self):
        # TODO: This parameter validation could be done
        # by our specific parameter validator (under
        # construction yet)
        exception_messages = []

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        super().__init__(TestVideoMobjectIn2DManimAnimationGenerator)

class TestVideoMobjectIn2DManimAnimationGenerator(BaseManimAnimation):

    __test__ = False

    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(
        self,
        parameters: dict,
        output_filename: Union[str, None] = None
    ):
        """
        Build the manim animation video and stores it
        locally as the provided 'output_filename', 
        returning the final output filename.

        This method will call the '.animate()' method
        to build the scene with the instructions that
        are written in that method.
        """
        output_filename = Output.get_filename(output_filename, FileExtension.MOV)

        return super().generate(
            parameters,
            renderer = ManimRenderer.CAIRO,
            output_filename = output_filename
        )
    
    def animate(self):
        video1 = VideoMobject(
            filename = 'prueba.mp4',
        ).scale_to_fit_width(5)
        self.add(video1)
        self.wait(0.25)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.play(video1.animate.shift(2 * DOWN), run_time = 0.5)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.wait(0.25)

class TestVideoOpenGLMobjectIn2DManimAnimationWrapper(BaseManimAnimationWrapper):

    __test__ = False

    def __init__(self):
        # TODO: This parameter validation could be done
        # by our specific parameter validator (under
        # construction yet)
        exception_messages = []

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        super().__init__(TestVideoOpenGLMobjectIn2DManimAnimationGenerator)

class TestVideoOpenGLMobjectIn2DManimAnimationGenerator(BaseManimAnimation):

    __test__ = False

    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, parameters: dict, output_filename: Union[str, None] = None):
        """
        Build the manim animation video and stores it
        locally as the provided 'output_filename', 
        returning the final output filename.

        This method will call the '.animate()' method
        to build the scene with the instructions that
        are written in that method.
        """
        output_filename = Output.get_filename(output_filename, FileExtension.MOV)

        return super().generate(
            parameters,
            renderer = ManimRenderer.OPENGL,
            output_filename = output_filename
        )
    
    def animate(self):
        video1 = VideoOpenGLMobject(
            filename = 'prueba.mp4',
        ).scale_to_fit_width(5)
        self.add(video1)
        self.wait(0.25)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.play(video1.animate.shift(2 * DOWN), run_time = 0.5)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.wait(0.25)

class TestVideoMobjectIn3DManimAnimationWrapper(BaseManimAnimationWrapper):

    __test__ = False

    def __init__(self):
        # TODO: This parameter validation could be done
        # by our specific parameter validator (under
        # construction yet)
        exception_messages = []

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        super().__init__(TestVideoMobjectIn3DManimAnimationGenerator)

class TestVideoMobjectIn3DManimAnimationGenerator(BaseThreeDManimAnimation):

    __test__ = False

    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, parameters: dict, output_filename: Union[str, None] = None):
        """
        Build the manim animation video and stores it
        locally as the provided 'output_filename', 
        returning the final output filename.

        This method will call the '.animate()' method
        to build the scene with the instructions that
        are written in that method.
        """
        output_filename = Output.get_filename(output_filename, FileExtension.MOV)

        return super().generate(
            parameters,
            renderer = ManimRenderer.CAIRO,
            output_filename = output_filename
        )
    
    def animate(self):
        video1 = VideoMobject(
            filename = 'prueba.mp4',
        ).scale_to_fit_width(5)
        self.add(video1)
        self.wait(0.25)
        self.begin_ambient_camera_rotation(rate = 0.15)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.play(video1.animate.shift(2 * DOWN), run_time = 0.5)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
        self.wait(0.25)

class TestVideoOpenGLMobjectIn3DManimAnimationWrapper(BaseManimAnimationWrapper):

    __test__ = False

    def __init__(self):
        # TODO: This parameter validation could be done
        # by our specific parameter validator (under
        # construction yet)
        exception_messages = []

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        super().__init__(TestVideoOpenGLMobjectIn3DManimAnimationGenerator)

class TestVideoOpenGLMobjectIn3DManimAnimationGenerator(BaseThreeDManimAnimation):

    __test__ = False

    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, parameters: dict, output_filename: Union[str, None] = None):
        """
        Build the manim animation video and stores it
        locally as the provided 'output_filename', 
        returning the final output filename.

        This method will call the '.animate()' method
        to build the scene with the instructions that
        are written in that method.
        """
        output_filename = Output.get_filename(output_filename, FileExtension.MOV)

        return super().generate(
            parameters,
            renderer = ManimRenderer.OPENGL,
            output_filename = output_filename
        )
    
    def animate(self):
        video1 = VideoMobject(
            filename = 'prueba.mp4',
        ).scale_to_fit_width(5)
        self.add(video1)
        self.wait(0.25)
        self.begin_ambient_camera_rotation(rate = 0.15)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.play(video1.animate.shift(2 * DOWN), run_time = 0.5)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
        self.wait(0.25)

class TestImageOpenGLMobjectIn3DManimAnimationWrapper(BaseManimAnimationWrapper):

    __test__ = False

    filename: str = None

    def __init__(self, filename: str):
        # TODO: I should test if it is a valid file
        ParameterValidator.validate_mandatory_string('filename', filename, do_accept_empty = False)

        exception_messages = []

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        self.filename = filename
        super().__init__(TestVideoOpenGLMobjectIn3DManimAnimationGenerator)

class TestImageOpenGLMobjectIn3DManimAnimationGenerator(BaseThreeDManimAnimation):

    __test__ = False

    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, parameters: dict, output_filename: Union[str, None] = None):
        """
        Build the manim animation video and stores it
        locally as the provided 'output_filename', 
        returning the final output filename.

        This method will call the '.animate()' method
        to build the scene with the instructions that
        are written in that method.
        """
        output_filename = Output.get_filename(output_filename, FileExtension.MOV)

        return super().generate(
            parameters,
            renderer = ManimRenderer.OPENGL,
            output_filename = output_filename
        )
    
    def animate(self):
        image = OpenGLImageMobject.init(self.parameters['filename']).scale_to_fit_width(5)
        self.add(image)
        image.shift(10 * UP)
        self.play(image.animate.shift(10 * DOWN), run_time = 0.25)
        self.move_camera(phi = 30 * DEGREES, frame_center = image, run_time = 0.25)
        self.move_camera(phi = -60 * DEGREES, frame_center = image, run_time = 0.50)
        self.move_camera(phi = 30 * DEGREES, frame_center = image, run_time = 0.25)
        self.wait(0.25)

class TestOpenGLImageMobjectIn3DManimAnimationWrapper(BaseManimAnimationWrapper):

    __test__ = False

    def __init__(self):
        # TODO: This parameter validation could be done
        # by our specific parameter validator (under
        # construction yet)
        exception_messages = []

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        super().__init__(TestVideoOpenGLMobjectIn3DManimAnimationGenerator)

class TestOpenGLImageMobjectIn3DManimAnimationGenerator(BaseThreeDManimAnimation):

    __test__ = False
    
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, parameters: dict, output_filename: Union[str, None] = None):
        """
        Build the manim animation video and stores it
        locally as the provided 'output_filename', 
        returning the final output filename.

        This method will call the '.animate()' method
        to build the scene with the instructions that
        are written in that method.
        """
        return super().generate(
            parameters,
            renderer = ManimRenderer.OPENGL,
            output_filename = output_filename
        )
    
    def animate(self):
        # TODO: Why this? Maybe better downloading an image...
        from yta_image.generation.reviews.tripadvisor.generator import TripadvisorImageGenerator
        from yta_constants.multimedia import DEFAULT_MANIM_SCENE_HEIGHT

        # This makes an image navigating in 3D scenario and being rendered
        # with alpha transparency (if it nos working, go to 'opengl_renderer.py'
        # and change the line 596 replacing 1.0 by 0.0)
        self.camera.background_color = [0, 0, 0, 0]
        image = OpenGLImageMobject.init(
            filename_or_array = np.asarray(TripadvisorImageGenerator.generate_review()),
        ).scale_to_fit_width(5)
        image.move_to((0, DEFAULT_MANIM_SCENE_HEIGHT + image.height / 2, 0))
        self.add(image)
        #self.move_camera(phi = 75 * DEGREES, theta = 30 * DEGREES, run_time = 0.0000001)
        self.set_camera_orientation(phi = 75 * DEGREES, theta = 30 * DEGREES)
        self.play(image.animate.move_to((0, -DEFAULT_MANIM_SCENE_HEIGHT - image.height / 2, 0)), run_time = 5, rate_func = linear)
        print('Animation finished')
        print(self.camera.background_opacity)

    @requires_dependency('moviepy', 'yta_multimedia_manim', 'moviepy')
    def animate_two(self):
        # TODO: Fix these dependencies
        from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
        from yta_constants.multimedia import DEFAULT_MANIM_SCENE_WIDTH, DEFAULT_MANIM_SCENE_HEIGHT
        from moviepy import VideoFileClip

        # This below is for trying to render a video but the internal
        # counter is not working properly
        image = OpenGLImageMobject.init(
            filename_or_array = VideoFrameExtractor.get_frame_by_index('prueba.mp4', 0)
        ).scale_to_fit_width(DEFAULT_MANIM_SCENE_WIDTH)
        self.add(image)
        #self.begin_ambient_camera_rotation()
        self.wait(0.25)
        self.wait(0.25)
        self.move_camera(phi = 45 * DEGREES, added_anims = [image.animate.move_to((0, DEFAULT_MANIM_SCENE_HEIGHT / 2, -DEFAULT_MANIM_SCENE_HEIGHT / 2))], run_time = 1, rate_func = linear)
        videoclip = VideoFileClip('prueba.mp4')
        #previous_image = image
        print(videoclip.fps * videoclip.duration)
        print((int) (videoclip.fps * videoclip.duration))
        videoclip = videoclip.with_subclip(0, 1)
        for i in range((int) (videoclip.fps * videoclip.duration)):
            if i == 0:
                i += 1
                print(self.mobjects)
                other_image = OpenGLImageMobject.init(
                    filename_or_array = VideoFrameExtractor.get_frame_by_index('prueba.mp4', i),
                ).scale_to_fit_width(DEFAULT_MANIM_SCENE_WIDTH).move_to(self.mobjects[0])
                print(self.mobjects[0].__class__)
                print(self.mobjects[1].__class__)
                print(self.mobjects)
                self.add(other_image)
                print(self.mobjects)
                self.play(Transform(self.mobjects[0], self.mobjects[len(self.mobjects) - 1]), run_time = 1 / 60)
                print(self.mobjects)
                self.remove(self.mobjects[0])
                image = other_image
                #self.add(other_image)
                #previous_image = other_image
                #self.wait(1 / 60)
                print(self.mobjects)
            else:
                print(self.mobjects)
                other_image = OpenGLImageMobject.init(
                    filename_or_array = VideoFrameExtractor.get_frame_by_index('prueba.mp4', i),
                ).scale_to_fit_width(DEFAULT_MANIM_SCENE_WIDTH).move_to(self.mobjects[len(self.mobjects) - 1])
                print(self.mobjects[0].__class__)
                print(self.mobjects[1].__class__)
                print(self.mobjects)
                self.add(other_image)
                print(self.mobjects)
                self.play(Transform(self.mobjects[len(self.mobjects) - 2], self.mobjects[len(self.mobjects) - 1]), run_time = 1 / 60)
                print(self.mobjects)
                self.remove(self.mobjects[len(self.mobjects) - 2])
                image = other_image
                #self.add(other_image)
                #previous_image = other_image
                #self.wait(1 / 60)
                print(self.mobjects)
        #self.play(Uncreate(image), run_time = 0.5, rate_func = linear)
        #image.animate.move_to((0, 0, HALF_SCENE_HEIGHT))
        self.wait(0.25)
        #self.stop_ambient_camera_rotation()




# TODO: Remove all these commented classes below when
# the ones above are working properly
# class TestVideoMobjectIn2DManimAnimation(BaseManimAnimation):
#     def construct(self):
#         """
#         This method is called by manim when executed by shell and
#         will call the scene animation render method to be processed
#         and generated.
#         """
#         self.animate()

#     def generate(self, output_filename: str = 'output.mov'):
#         """
#         Checks and validates the provided parameters and generates
#         the manim animation if those parameters are valid. The 
#         'text' parameter is limited to 30 characters.
#         """
#         # Check and validate all parameters
#         parameters = {}

#         # Generate the animation when parameters are valid
#         super().generate(parameters, renderer = 'cairo', output_filename = output_filename)

#         return output_filename
    
#     def animate(self):
#         video1 = VideoMobject(
#             filename = 'prueba.mp4',
#         ).scale_to_fit_width(5)
#         self.add(video1)
#         self.wait(0.25)
#         self.play(video1.animate.shift(1 * UP), run_time = 0.25)
#         self.play(video1.animate.shift(2 * DOWN), run_time = 0.5)
#         self.play(video1.animate.shift(1 * UP), run_time = 0.25)
#         self.wait(0.25)

# class TestVideoOpenGLMobjectIn2DManimAnimation(BaseManimAnimation):
#     def construct(self):
#         """
#         This method is called by manim when executed by shell and
#         will call the scene animation render method to be processed
#         and generated.
#         """
#         self.animate()

#     def generate(self, output_filename: str = 'output.mov'):
#         """
#         Checks and validates the provided parameters and generates
#         the manim animation if those parameters are valid. The 
#         'text' parameter is limited to 30 characters.
#         """
#         # Check and validate all parameters
#         parameters = {}

#         # Generate the animation when parameters are valid
#         super().generate(parameters, renderer = 'opengl', output_filename = output_filename)

#         return output_filename
    
#     def animate(self):
#         video1 = VideoOpenGLMobject(
#             filename = 'prueba.mp4',
#         ).scale_to_fit_width(5)
#         self.add(video1)
#         self.wait(0.25)
#         self.play(video1.animate.shift(1 * UP), run_time = 0.25)
#         self.play(video1.animate.shift(2 * DOWN), run_time = 0.5)
#         self.play(video1.animate.shift(1 * UP), run_time = 0.25)
#         self.wait(0.25)

# class TestVideoMobjectIn3DManimAnimation(BaseThreeDManimAnimation):
#     def construct(self):
#         """
#         This method is called by manim when executed by shell and
#         will call the scene animation render method to be processed
#         and generated.
#         """
#         self.animate()

#     def generate(self, output_filename: str = 'output.mov'):
#         """
#         Checks and validates the provided parameters and generates
#         the manim animation if those parameters are valid. The 
#         'text' parameter is limited to 30 characters.
#         """
#         # Check and validate all parameters
#         parameters = {}

#         # Generate the animation when parameters are valid
#         super().generate(parameters, renderer = 'cairo', output_filename = output_filename)

#         return output_filename
    
#     def animate(self):
#         video1 = VideoMobject(
#             filename = 'prueba.mp4',
#         ).scale_to_fit_width(5)
#         self.add(video1)
#         self.wait(0.25)
#         self.begin_ambient_camera_rotation(rate = 0.15)
#         self.play(video1.animate.shift(1 * UP), run_time = 0.25)
#         self.play(video1.animate.shift(2 * DOWN), run_time = 0.5)
#         self.play(video1.animate.shift(1 * UP), run_time = 0.25)
#         self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
#         self.wait(0.25)

# class TestVideoOpenGLMobjectIn3DManimAnimation(BaseThreeDManimAnimation):
#     def construct(self):
#         """
#         This method is called by manim when executed by shell and
#         will call the scene animation render method to be processed
#         and generated.
#         """
#         self.animate()

#     def generate(self, output_filename: str = 'output.mov'):
#         """
#         Checks and validates the provided parameters and generates
#         the manim animation if those parameters are valid. The 
#         'text' parameter is limited to 30 characters.
#         """
#         # Check and validate all parameters
#         parameters = {}

#         # Generate the animation when parameters are valid
#         super().generate(parameters, renderer = 'opengl', output_filename = output_filename)

#         return output_filename
    
#     def animate(self):
#         video1 = VideoOpenGLMobject(
#             filename = 'prueba.mp4',
#         ).scale_to_fit_width(5)
#         self.add(video1)
#         self.wait(0.25)
#         self.begin_ambient_camera_rotation(rate = 0.15)
#         self.play(video1.animate.shift(1 * UP), run_time = 0.25)
#         self.play(video1.animate.shift(2 * DOWN), run_time = 0.5)
#         self.play(video1.animate.shift(1 * UP), run_time = 0.25)
#         self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
#         self.wait(0.25)

# class TestImageOpenGLMobjectIn3DManimAnimation(BaseThreeDManimAnimation):
#     def construct(self):
#         """
#         This method is called by manim when executed by shell and
#         will call the scene animation render method to be processed
#         and generated.
#         """
#         self.animate()

#     def generate(self, filename: str, output_filename: str = 'output.mov'):
#         """
#         Checks and validates the provided parameters and generates
#         the manim animation if those parameters are valid. The 
#         'text' parameter is limited to 30 characters.
#         """
#         # Check and validate all parameters
#         parameters = {
#             'filename': filename
#         }

#         # Generate the animation when parameters are valid
#         super().generate(parameters, renderer = 'opengl', output_filename = output_filename)

#         return output_filename
    
#     def animate(self):
#         image = OpenGLImageMobject.init(self.parameters['filename']).scale_to_fit_width(5)
#         self.add(image)
#         image.shift(10 * UP)
#         self.play(image.animate.shift(10 * DOWN), run_time = 0.25)
#         self.move_camera(phi = 30 * DEGREES, frame_center = image, run_time = 0.25)
#         self.move_camera(phi = -60 * DEGREES, frame_center = image, run_time = 0.50)
#         self.move_camera(phi = 30 * DEGREES, frame_center = image, run_time = 0.25)
#         self.wait(0.25)

# class TestOpenGLImageMobjectIn3DManimAnimation(BaseThreeDManimAnimation):
#     def construct(self):
#         """
#         This method is called by manim when executed by shell and
#         will call the scene animation render method to be processed
#         and generated.
#         """
#         self.animate()

#     def generate(self, output_filename: str = 'output.mov'):
#         """
#         Checks and validates the provided parameters and generates
#         the manim animation if those parameters are valid. The 
#         'text' parameter is limited to 30 characters.
#         """
#         # Check and validate all parameters
#         parameters = {}

#         # Generate the animation when parameters are valid
#         super().generate(parameters, renderer = 'opengl', output_filename = output_filename)

#         return output_filename
    
#     def animate(self):
#         from yta_multimedia.image.generation.reviews.tripadvisor.tripadvisor_image_generator import TripadvisorImageGenerator
#         from yta_multimedia.video.consts import MANIM_SCENE_DEFAULT_SIZE

#         # This makes an image navigating in 3D scenario and being rendered
#         # with alpha transparency (if it nos working, go to 'opengl_renderer.py'
#         # and change the line 596 replacing 1.0 by 0.0)
#         self.camera.background_color = [0, 0, 0, 0]
#         image = OpenGLImageMobject.init(
#             filename_or_array = np.asarray(TripadvisorImageGenerator.generate_review()),
#         ).scale_to_fit_width(5)
#         image.move_to((0, MANIM_SCENE_DEFAULT_SIZE[1] + image.height / 2, 0))
#         self.add(image)
#         #self.move_camera(phi = 75 * DEGREES, theta = 30 * DEGREES, run_time = 0.0000001)
#         self.set_camera_orientation(phi = 75 * DEGREES, theta = 30 * DEGREES)
#         self.play(image.animate.move_to((0, -MANIM_SCENE_DEFAULT_SIZE[1] - image.height / 2, 0)), run_time = 5, rate_func = linear)
#         print('Animation finished')
#         print(self.camera.background_opacity)

#     def animate_two(self):
#         from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
#         from yta_multimedia.video.consts import MANIM_SCENE_DEFAULT_SIZE
#         from moviepy import VideoFileClip

#         # This below is for trying to render a video but the internal
#         # counter is not working properly
#         image = OpenGLImageMobject.init(
#             filename_or_array = VideoFrameExtractor.get_frame_by_index('prueba.mp4', 0)
#         ).scale_to_fit_width(MANIM_SCENE_DEFAULT_SIZE[0])
#         self.add(image)
#         #self.begin_ambient_camera_rotation()
#         self.wait(0.25)
#         self.wait(0.25)
#         self.move_camera(phi = 45 * DEGREES, added_anims = [image.animate.move_to((0, MANIM_SCENE_DEFAULT_SIZE[1] / 2, -MANIM_SCENE_DEFAULT_SIZE[1] / 2))], run_time = 1, rate_func = linear)
#         videoclip = VideoFileClip('prueba.mp4')
#         #previous_image = image
#         print(videoclip.fps * videoclip.duration)
#         print((int) (videoclip.fps * videoclip.duration))
#         videoclip = videoclip.with_subclip(0, 1)
#         for i in range((int) (videoclip.fps * videoclip.duration)):
#             if i == 0:
#                 i += 1
#                 print(self.mobjects)
#                 other_image = OpenGLImageMobject.init(
#                     filename_or_array = VideoFrameExtractor.get_frame_by_index('prueba.mp4', i),
#                 ).scale_to_fit_width(MANIM_SCENE_DEFAULT_SIZE[0]).move_to(self.mobjects[0])
#                 print(self.mobjects[0].__class__)
#                 print(self.mobjects[1].__class__)
#                 print(self.mobjects)
#                 self.add(other_image)
#                 print(self.mobjects)
#                 self.play(Transform(self.mobjects[0], self.mobjects[len(self.mobjects) - 1]), run_time = 1 / 60)
#                 print(self.mobjects)
#                 self.remove(self.mobjects[0])
#                 image = other_image
#                 #self.add(other_image)
#                 #previous_image = other_image
#                 #self.wait(1 / 60)
#                 print(self.mobjects)
#             else:
#                 print(self.mobjects)
#                 other_image = OpenGLImageMobject.init(
#                     filename_or_array = VideoFrameExtractor.get_frame_by_index('prueba.mp4', i),
#                 ).scale_to_fit_width(MANIM_SCENE_DEFAULT_SIZE[0]).move_to(self.mobjects[len(self.mobjects) - 1])
#                 print(self.mobjects[0].__class__)
#                 print(self.mobjects[1].__class__)
#                 print(self.mobjects)
#                 self.add(other_image)
#                 print(self.mobjects)
#                 self.play(Transform(self.mobjects[len(self.mobjects) - 2], self.mobjects[len(self.mobjects) - 1]), run_time = 1 / 60)
#                 print(self.mobjects)
#                 self.remove(self.mobjects[len(self.mobjects) - 2])
#                 image = other_image
#                 #self.add(other_image)
#                 #previous_image = other_image
#                 #self.wait(1 / 60)
#                 print(self.mobjects)
#         #self.play(Uncreate(image), run_time = 0.5, rate_func = linear)
#         #image.animate.move_to((0, 0, HALF_SCENE_HEIGHT))
#         self.wait(0.25)
#         #self.stop_ambient_camera_rotation()