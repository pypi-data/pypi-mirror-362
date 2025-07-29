from yta_video_manim.animations.base_three_d_manim_animation import BaseThreeDManimAnimation
from yta_video_manim.animations.base_manim_animation_wrapper import BaseManimAnimationWrapper
from yta_constants.manim import ManimRenderer
from yta_constants.file import FileExtension
from yta_programming.output import Output
from manim import *
from typing import Union


class Axes3DExampleWrapper(BaseManimAnimationWrapper):
    def __init__(self, text: str, duration: float):
        # TODO: This parameter validation could be done
        # by our specific parameter validator (under
        # construction yet)
        exception_messages = []

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        super().__init__(Axes3DExampleGenerator)

class Axes3DExampleGenerator(BaseThreeDManimAnimation):
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
        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 1.8)

        # 3D variant of the Dot() object
        dot = Dot3D()

        # zoom out so we see the axes
        self.set_camera_orientation(zoom=0.5)

        self.play(FadeIn(axes), FadeIn(dot), FadeIn(x_label), FadeIn(y_label))

        self.wait(0.5)

        # animate the move of the camera to properly see the axes
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)

        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=0.15)

        # one dot for each direction
        upDot = dot.copy().set_color(RED)
        rightDot = dot.copy().set_color(BLUE)
        outDot = dot.copy().set_color(GREEN)

        self.wait(1)

        self.play(
            upDot.animate.shift(UP),
            rightDot.animate.shift(RIGHT),
            outDot.animate.shift(OUT),
        )

        self.wait(2)


class Image3DWrapper(BaseManimAnimationWrapper):
    def __init__(self, text: str, duration: float):
        # TODO: This parameter validation could be done
        # by our specific parameter validator (under
        # construction yet)
        exception_messages = []

        if len(exception_messages) > 0:
            raise Exception('\n'.join([exception_message for exception_message in exception_messages]))
        
        super().__init__(Image3DGenerator)

class Image3DGenerator(BaseThreeDManimAnimation):
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
            renderer = ManimRenderer.CAIRO,
            output_filename = output_filename
        )
    
    def animate(self):
        self.video1 = ImageMobject(
                filename_or_array = 'C:/Users/dania/Desktop/wallpaper1080.png',
            ).scale_to_fit_height(3)
        ax = Axes(
            x_range=[0, 10, 1],
            x_length=9,
            y_range=[0, 20, 5],
            y_length=6,
            axis_config={"include_numbers": True, "include_tip": False},

        ).to_edge(DL + RIGHT + UP, buff=1).scale(0.7)
        labels = ax.get_axis_labels()

        self.play(Create(VGroup(ax, labels)))
        self.play(FadeIn(self.video1))
        self.wait(3)
        self.move_camera(phi=0*DEGREES, theta= -90 * DEGREES, zoom= 0.7, run_time=0.4, gamma=0*DEGREES)

        self.begin_ambient_camera_rotation(90 * DEGREES / 3, about='phi')
        self.begin_ambient_camera_rotation(90 * DEGREES / 3, about='theta')
        self.wait(3)






# TODO: I don't know why these classes below only
# have a 'construct' method. I think it was to 
# simplify the way I rendered them for testing, but
# I think they should be like a 2D scene
# TODO: Remove these classes below soon, please
# class Axes3DExample(BaseThreeDManimAnimation):
#     def construct(self):
#         axes = ThreeDAxes()

#         x_label = axes.get_x_axis_label(Tex("x"))
#         y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 1.8)

#         # 3D variant of the Dot() object
#         dot = Dot3D()

#         # zoom out so we see the axes
#         self.set_camera_orientation(zoom=0.5)

#         self.play(FadeIn(axes), FadeIn(dot), FadeIn(x_label), FadeIn(y_label))

#         self.wait(0.5)

#         # animate the move of the camera to properly see the axes
#         self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)

#         # built-in updater which begins camera rotation
#         self.begin_ambient_camera_rotation(rate=0.15)

#         # one dot for each direction
#         upDot = dot.copy().set_color(RED)
#         rightDot = dot.copy().set_color(BLUE)
#         outDot = dot.copy().set_color(GREEN)

#         self.wait(1)

#         self.play(
#             upDot.animate.shift(UP),
#             rightDot.animate.shift(RIGHT),
#             outDot.animate.shift(OUT),
#         )

#         self.wait(2)

# class Image3D(BaseThreeDManimAnimation):
#     def construct(self):
#         self.video1 = ImageMobject(
#                 filename_or_array = 'C:/Users/dania/Desktop/wallpaper1080.png',
#             ).scale_to_fit_height(3)
#         ax = Axes(
#             x_range=[0, 10, 1],
#             x_length=9,
#             y_range=[0, 20, 5],
#             y_length=6,
#             axis_config={"include_numbers": True, "include_tip": False},

#         ).to_edge(DL + RIGHT + UP, buff=1).scale(0.7)
#         labels = ax.get_axis_labels()

#         self.play(Create(VGroup(ax, labels)))
#         self.play(FadeIn(self.video1))
#         self.wait(3)
#         self.move_camera(phi=0*DEGREES, theta= -90 * DEGREES, zoom= 0.7, run_time=0.4, gamma=0*DEGREES)

#         self.begin_ambient_camera_rotation(90 * DEGREES / 3, about='phi')
#         self.begin_ambient_camera_rotation(90 * DEGREES / 3, about='theta')
#         self.wait(3)