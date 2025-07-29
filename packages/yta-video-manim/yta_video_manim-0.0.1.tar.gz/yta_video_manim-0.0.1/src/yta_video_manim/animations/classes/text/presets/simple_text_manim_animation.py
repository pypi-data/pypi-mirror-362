"""
This class can be considered as a base class so you
copy the 2 classes on this file, adapt the params
(attributes) and customize the 'animate' method with
your specific animation.

The wrapper class must be always next to the generator
class because they work toghether
"""
from yta_video_manim.animations.base_manim_animation import BaseManimAnimation
from yta_video_manim.animations.base_manim_animation_wrapper import BaseManimAnimationWrapper
from yta_constants.manim import ManimRenderer, ManimAnimationType
from yta_validation.parameter import ParameterValidator
from yta_programming.output import Output
from yta_constants.file import FileExtension
from manim import *
from typing import Union


# This class and the generator must be always in
# the same file because they are extremely
# connected and they are dependant
class SimpleTextManimAnimationWrapper(BaseManimAnimationWrapper):
    """
    Simple Text animation wrapper, used only for testing.
    """
    text: str = None
    duration: float = None

    def __init__(self, text: str, duration: float):
        ParameterValidator.validate_mandatory_string('text', text, do_accept_empty = False)
        ParameterValidator.validate_mandatory_number_between('duration', duration, 1, 100)

        # TODO: This parameter validation could be done
        # by our specific parameter validator (under
        # construction yet)
        exception_messages = []

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        self.text = text
        self.duration = duration
        super().__init__(SimpleTextManimAnimationGenerator, ManimAnimationType.TEXT_ALPHA)

class SimpleTextManimAnimationGenerator(BaseManimAnimation):
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
        text = Text(self.parameters['text'], font_size = 26, font = 'Minecraftia').shift(DOWN * 0).scale(1)
        self.add(text)
        # The sound duration will be set as video duration if
        # larger than the 'duration' parameter so I need to
        # look for a way to enshort the video
        #self.add_sound(GoogleDriveResource('https://drive.google.com/file/d/1Dzeb6Qae4UdpmuA6U9d6t3MXnvhzukzg/view?usp=sharing').download(Temp.create_filename('tmp.mp3')))
        self.wait(self.parameters['duration'])

    #     def animate_one(self):
    #         """
    #         This code will generate the manim animation and belongs to the
    #         Scene manim object.
    #         """
    #         text = Text(self.parameters['text'], font_size = 140, stroke_width = 2.0, font = 'Haettenschweiler').shift(DOWN * 0).scale(0.001)
    #         self.wait(1 / 60)
    #         self.add(text)
    #         self.add_sound(GoogleDriveResource('https://drive.google.com/file/d/1WPS8uWB1LTuzPzxQ2Zcp1FpwvLM3fhM5/view?usp=sharing').download(Temp.create_filename('tmp.mp3')))
    #         self.play(text.animate.scale(1000), run_time = 49 / 60)
    #         self.play(Rotate(text, 0.03), run_time = 3 / 60)
    #         self.play(Rotate(text, -0.04), run_time = 3 / 60)
    #         self.play(Rotate(text, -0.02), run_time = 3 / 60)
    #         self.play(Rotate(text, 0.04), run_time = 3 / 60)
    #         self.play(Rotate(text, -0.01), run_time = 3 / 60)
    #         self.play(Rotate(text, 0.03), run_time = 3 / 60)
    #         self.play(Rotate(text, -0.04), run_time = 3 / 60)
    #         self.play(Rotate(text, -0.02), run_time = 3 / 60)
    #         self.play(Rotate(text, 0.04), run_time = 3 / 60)
    #         self.play(Rotate(text, -0.01), run_time = 3 / 60)
    #         #self.add_sound(TOUSE_ABSOLUTE_PATH + 'sounds/xp_error.mp3')
    #         #self.play(AddTextLetterByLetter(text), run_time = self.parameters['duration'])
            
    #         #simple_play_animation(self, Write, text, self.parameters['duration'])

    #     def animate_two(self):
    #         """
    #         This code will generate the manim animation and belongs to the
    #         Scene manim object.
    #         """
    #         text = Text(self.parameters['text'], font_size = 140, stroke_width = 2.0, font = 'Haettenschweiler').shift(DOWN * 0).scale(7 / 10)
    #         self.wait(1 / 60)
    #         self.add(text)
    #         self.play(text.animate.scale(10 / 7), run_time = 6 / 60)
    #         self.play(ApplyWave(text), run_time = 30 / 60)

    #     def animate(self):
    #         text = Text(self.parameters['text'], font_size = 26, font = 'Minecraftia').shift(DOWN * 0).scale(1)
    #         self.add(text)
    #         # The sound duration will be set as video duration if
    #         # larger than the 'duration' parameter so I need to
    #         # look for a way to enshort the video
    #         #self.add_sound(GoogleDriveResource('https://drive.google.com/file/d/1Dzeb6Qae4UdpmuA6U9d6t3MXnvhzukzg/view?usp=sharing').download(Temp.create_filename('tmp.mp3')))
    #         self.wait(self.parameters['duration'])

    # __all__ = [
    #     'SimpleTextManimAnimationX'
    # ]












