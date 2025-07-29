
from yta_video_manim.animations.base_manim_animation import BaseManimAnimation
from yta_video_manim.animations.base_manim_animation_wrapper import BaseManimAnimationWrapper
from yta_constants.manim import ManimRenderer, ManimAnimationType
from yta_video_manim.constants import DEFAULT_SCENE_SIZE
from yta_video_manim.dimensions import fitting_text
# TODO: This dependency on 'yta_multimedia' must dissapear
from yta_multimedia.video.position import Position
from yta_validation.parameter import ParameterValidator
from yta_programming.output import Output
from yta_constants.file import FileExtension
from manim import *
from typing import Union


class RainOfWordsManimAnimationWrapper(BaseManimAnimationWrapper):
    """
    This is a rain of the provided 'words' over the screen, that
    appear in random positions.
    """
    words: list[str] = None
    duration: float = None

    def __init__(
        self,
        words: list[str],
        duration: float
    ):
        ParameterValidator.validate_mandatory_list_of_string('words', words)
        ParameterValidator.validate_mandatory_number_between('duration', duration, 1, 100)

        # TODO: This parameter validation could be done
        # by our specific parameter validator (under
        # construction yet)
        exception_messages = []

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        self.words = words
        self.duration = duration
        super().__init__(RainOfWordsManimAnimationGenerator, ManimAnimationType.TEXT_ALPHA)

class RainOfWordsManimAnimationGenerator(BaseManimAnimation):
    """
    This is a rain of the provided 'words' over the screen, that
    appear in random positions.
    """
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
        each_word_time = self.parameters['duration'] / len(self.parameters['words'])
        # Adjust the divisor number to modify word size
        for word in self.parameters['words']:
            text = fitting_text(word, DEFAULT_SCENE_SIZE[0] / 6)
            # TODO: This was previously considering the limits to
            # make the text be always inside the scene, but now...
            #random_coords = Position.RANDOM_INSIDE.get_manim_position_center((text.width, text.height))
            random_coords = Position.RANDOM_INSIDE.get_manim_position_center()
            text.move_to(random_coords)
            self.add(text)
            self.wait(each_word_time)