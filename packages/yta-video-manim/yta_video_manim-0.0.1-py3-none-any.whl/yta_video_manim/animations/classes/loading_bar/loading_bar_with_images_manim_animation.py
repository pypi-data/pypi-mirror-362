from yta_video_manim.dimensions import ManimDimensions
from yta_constants.manim import ManimRenderer
from yta_video_manim.animations.base_manim_animation import BaseManimAnimation
from yta_video_manim.animations.classes.loading_bar.parameter_classes.loading_bar_image import LoadingBarImage
from yta_video_manim.animations.classes.loading_bar.mobjects.loading_bar_mobject import LoadingBarMobject
from yta_video_manim.animations.base_manim_animation_wrapper import BaseManimAnimationWrapper
from yta_validation.parameter import ParameterValidator
from yta_programming.output import Output
from yta_constants.file import FileExtension
from typing import Union
from manim import *


class LoadingBarWithImagesManimAnimationWrapper(BaseManimAnimationWrapper):
    """
    Loading bar with images. It will go from 'start_percentage'
    to 'end_percentage' in the provided 'duration' time. It will
    show the bar progressing and also the 'images' if provided.

    Images will be displayed and will be static or in movement.
    If image 'start_percentage' and 'end_percentage' is the same,
    it will be static at that percentage position. If they are
    different, it will move from 'start_percentage' to
    'end_percentage' in the animation 'duration' time.

    You can put the same 'start_percentage' and 'end_percentage'
    in one image than in the loading bar to make it advance
    at the same time the progress bar does.

    Here is an example of 'images' object you can pass:
    loading_bar_images = [
        LoadingBarImage('minecraft_sword_128x128.png', 60, 0, 100),
        LoadingBarImage('arrow_up_128x128.png', -60, 0, 100),
        LoadingBarImage('minecraft_sword_128x128.png', 60, 40, 40),
        LoadingBarImage('minecraft_sword_128x128.png', 60, 78, 78)
    ]
    """
    start_percentage: float = None
    end_percentage: float = None
    duration: float = None
    images: list[LoadingBarImage] = None

    def __init__(
        self,
        start_percentage: int = 0,
        end_percentage: int = 100,
        duration: float = 5,
        images: list[LoadingBarImage] = None
    ):
        ParameterValidator.validate_mandatory_number_between('start_percentage', start_percentage, 0, 100)
        ParameterValidator.validate_mandatory_number_between('end_percentage', end_percentage, 0, 100)
        ParameterValidator.validate_mandatory_number_between('duration', duration, 0, 120)
        # TODO: This parameter validation could be done
        # by our specific parameter validator (under
        # construction yet)
        exception_messages = []

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        images = [image.toJSON() for image in images] if images and len(images) > 0 else []
        
        self.start_percentage = start_percentage
        self.end_percentage = end_percentage
        self.duration = duration
        self.images = images
        super().__init__(LoadingBarWithImagesManimAnimationGenerator)

class LoadingBarWithImagesManimAnimationGenerator(BaseManimAnimation):
    """
    Loading bar with images. It will go from 'start_percentage'
    to 'end_percentage' in the provided 'duration' time. It will
    show the bar progressing and also the 'images' if provided.

    Images will be displayed and will be static or in movement.
    If image 'start_percentage' and 'end_percentage' is the same,
    it will be static at that percentage position. If they are
    different, it will move from 'start_percentage' to
    'end_percentage' in the animation 'duration' time.

    You can put the same 'start_percentage' and 'end_percentage'
    in one image than in the loading bar to make it advance
    at the same time the progress bar does.

    Here is an example of 'images' object you can pass:
    loading_bar_images = [
        LoadingBarImage('minecraft_sword_128x128.png', 60, 0, 100),
        LoadingBarImage('arrow_up_128x128.png', -60, 0, 100),
        LoadingBarImage('minecraft_sword_128x128.png', 60, 40, 40),
        LoadingBarImage('minecraft_sword_128x128.png', 60, 78, 78)
    ]
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
        loading_bar = LoadingBarMobject()
        
        # We make LoadingBarImages objects again
        images = []
        for image in self.parameters['images']:
            images.append(LoadingBarImage(image['image_filename'], ManimDimensions.manim_height_to_height(image['y']), image['start_percentage'], image['end_percentage']))

        loading_bar_animation = loading_bar.get_animation(images, self.parameters['start_percentage'], self.parameters['end_percentage'], self.parameters['duration'])

        # We add the mobjects to forze them to appear
        self.add(*loading_bar.get_mobjects())

        self.play(*loading_bar_animation, rate_func = linear, run_time = self.parameters['duration'])