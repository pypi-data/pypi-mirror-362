from yta_video_manim.animations.base_manim_animation import BaseManimAnimation
from yta_video_manim.animations.base_manim_animation_wrapper import BaseManimAnimationWrapper
from yta_constants.manim import ManimRenderer, ManimAnimationType
from yta_video_manim.dimensions import fitting_text, ManimDimensions
from yta_video_manim.constants import DEFAULT_MANIM_SCENE_SIZE
from yta_validation.parameter import ParameterValidator
from yta_programming.output import Output
from yta_constants.file import FileExtension
from manim import *
from typing import Union


class TextWordByWordManimAnimationWrapper(BaseManimAnimationWrapper):
    """
    The provided 'text' is shown word by word in the center of the scene
    with a fixed width.
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
        super().__init__(TextWordByWordManimAnimationGenerator, ManimAnimationType.TEXT_ALPHA)

class TextWordByWordManimAnimationGenerator(BaseManimAnimation):
    """
    The provided 'text' is shown word by word in the center of the scene
    with a fixed width.
    """
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
        words = self.parameters['text'].split(' ')
        word_duration = float(self.parameters['duration']) / len(words)
        for word in words:
            text = fitting_text(word, ManimDimensions.manim_width_to_width(DEFAULT_MANIM_SCENE_SIZE[0] / 6))
            text = Text(word, font_size = text.font_size, stroke_width = 2.0, font = 'Arial').shift(DOWN * 0)
            self.add(text)
            self.wait(word_duration)
            self.remove(text)