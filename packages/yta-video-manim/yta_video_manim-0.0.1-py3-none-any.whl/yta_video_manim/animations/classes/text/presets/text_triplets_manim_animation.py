from yta_video_manim.animations.base_manim_animation import BaseManimAnimation
from yta_video_manim.animations.base_manim_animation_wrapper import BaseManimAnimationWrapper
from yta_constants.manim import ManimRenderer, ManimAnimationType
from yta_video_manim.constants import DEFAULT_SCENE_SIZE
from yta_video_manim.dimensions import fitting_text
from yta_validation.parameter import ParameterValidator
from yta_programming.output import Output
from yta_constants.file import FileExtension
from manim import *
from typing import Union


class TextTripletsManimAnimationWrapper(BaseManimAnimationWrapper):
    """
    The provided 'text' is splitted in triplets and appear on the screen. This animation
    lasts 'duration' seconds. Each triplet appear each 'duration' / len(words).
    """

    __test__ = False
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
        super().__init__(TextTripletsManimAnimationGenerator, ManimAnimationType.TEXT_ALPHA)

class TextTripletsManimAnimationGenerator(BaseManimAnimation):
    """
    The provided 'text' is splitted in triplets and appear on the screen. This animation
    lasts 'duration' seconds. Each triplet appear each 'duration' / len(words).
    """

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
        words = self.parameters['text'].split(' ')
        # We need to adjust the array to contain a multiple of 3 number of elements
        leftover_numbers = words[len(words) - len(words) % 3:]
        if len(leftover_numbers) > 0:
            words = words[:len(words) - len(leftover_numbers)]

        words_triplets = []
        subarray = []
        for word in words:
            subarray.append(word)
            if len(subarray) == 3:
                words_triplets.append(subarray)
                subarray = []
        if leftover_numbers:
            words_triplets += [leftover_numbers]
        each_triplet_time = self.parameters['duration'] / len(words_triplets)

        for triplet in words_triplets:
            str = ' '.join(triplet)
            # I don't know how to show one word before the other
            # Helping information:
            # For example say you would like to not render and skip the begin of a video , you put self.next_section(skip_animations=True) in the line after def construct(self): and put self.next_section() before the first line of the animation you want to render.
            # Thank you: https://www.reddit.com/r/manim/comments/tq1ii8/comment/ihzogki/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
            text = fitting_text(str, DEFAULT_SCENE_SIZE[0] / 2)
            # Create 3 similar texts with each word
            self.add(text)
            self.wait(each_triplet_time)
            self.remove(text)


    