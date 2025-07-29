from yta_video_manim.config import ManimConfig
from yta_constants.manim import ManimRenderer
from yta_constants.file import FileExtension
from yta_file.filename.handler import FilenameHandler
from yta_file.handler import FileHandler
from yta_programming.path import DevPathHandler
from yta_programming.output import Output
from manim.cli.render.commands import render as manim_render
from manim import ThreeDScene, config
from threading import Thread
from abc import abstractmethod
from typing import Union


class BaseThreeDManimAnimation(ThreeDScene):
    """
    General class so that our own classes can inherit it 
    and work correctly.
    """
    def setup(self):
        """
        This method is called when manim is trying to use it to
        render the scene animation. It is called the first, to
        instantiate it and before the 'construct' method that
        is the one that will render.
        """
        # Preset configuration we need for any scene
        # Disables caching to avoid error when cache is overload
        config.disable_caching = True
        config.max_files_cached = 9999
        # This makes the video background transparent to fit well over the main video
        self.camera.background_opacity = 0.0

        self.parameters = ManimConfig.config

        return self.parameters

    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.setup()

    @abstractmethod
    def animate(self):
        """
        The code that creates the manim animation, specific for
        each animation subclass.
        """
        # This must be implemented by the subclass. This is the
        # code that actually generates the video scene by using
        # the manim engine.s
        pass

    def generate(
        self,
        parameters,
        renderer: ManimRenderer = ManimRenderer.CAIRO,
        output_filename: Union[str, None] = None
    ):
        """
        Generates the animation video file using the provided
        'parameters' and stores it locally as 'output_filename'
        """
        output_filename = Output.get_filename(output_filename, FileExtension.MOV)

        renderer = (
            ManimRenderer.CAIRO
            if renderer is None else
            ManimRenderer.to_enum(renderer)
        )
        
        # We write parameters in file to be able to read them
        ManimConfig.write(parameters)

        # Variables we need to make it work
        FPS = str(60)
        CLASS_MANIM_CONTAINER_ABSPATH = DevPathHandler.get_code_abspath(self.__class__)
        CLASS_FILENAME_WITHOUT_EXTENSION = FilenameHandler.get_file_name(DevPathHandler.get_code_filename(self.__class__))
        CLASS_NAME = self.__class__.__name__
        
        output_filename_extension = FilenameHandler.get_extension(output_filename)

        # These args are in 'manim.cli.render.commands.py' injected
        # as '@output_options', '@render_options', etc.
        args = {
            # I never used this 'format' before
            '--format': True,
            output_filename_extension: True, # Valid values are: [png|gif|mp4|webm|mov]
            # Qualities are here: manim\constants.py > QUALITIES
            '--quality': True,
            'h': True,
            '--fps': True,
            FPS: True,
            '--transparent': True,
            '--renderer': True,
            # The 'cairo' default option has been working good always
            renderer.value: True, # 'opengl' or 'cairo', 'cairo' is default
            # The '--output_file' changes the created file name, not the path
            CLASS_MANIM_CONTAINER_ABSPATH: True,
            CLASS_NAME: True
        }

        # TODO: Do more Exception checkings (such as '.smtg')
        if output_filename_extension != 'mov':
            del args['--transparent']

        # We need to execute this as a thread because the program ends when
        # finished if not a thread
        render_thread = Thread(target = manim_render, args = [args])
        render_thread.start()
        render_thread.join()
            
        CREATED_FILE_ABSPATH = f"{DevPathHandler.get_project_abspath()}media/videos/{CLASS_FILENAME_WITHOUT_EXTENSION}/1080p{FPS}/{CLASS_NAME}.{output_filename_extension}"

        FileHandler.rename_file(CREATED_FILE_ABSPATH, output_filename)

        return output_filename