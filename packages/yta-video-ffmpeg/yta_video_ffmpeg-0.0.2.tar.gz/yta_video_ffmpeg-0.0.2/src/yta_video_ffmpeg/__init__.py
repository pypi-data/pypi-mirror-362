"""
Module to simplify the use of Ffmpeg and to make
awesome things with simple methods.

Nice help: https://www.bannerbear.com/blog/how-to-use-ffmpeg-in-python-with-examples/
Official doc: https://www.ffmpeg.org/ffmpeg-resampler.html
More help: https://kkroening.github.io/ffmpeg-python/
Nice guide: https://img.ly/blog/ultimate-guide-to-ffmpeg/
Available flags: https://gist.github.com/tayvano/6e2d456a9897f55025e25035478a3a50

Interesting usage: https://stackoverflow.com/a/20325676
Maybe avoid writting on disk?: https://github.com/kkroening/ffmpeg-python/issues/500#issuecomment-792281072
"""
from yta_multimedia_utils.dimensions import get_video_size
from yta_multimedia_utils.resize import get_cropping_points_to_keep_aspect_ratio
from yta_general_utils.coordinate import NORMALIZATION_MAX_VALUE, NORMALIZATION_MIN_VALUE
from yta_date import Date
from yta_validation import PythonValidator
from yta_validation.parameter import ParameterValidator
from yta_file.handler import FileHandler
from yta_constants.file import FileType
from yta_constants.video import FfmpegAudioCodec, FfmpegFilter, FfmpegPixelFormat, FfmpegVideoCodec, FfmpegVideoFormat
from yta_programming.output import Output
from yta_temp import Temp
from typing import Union
from subprocess import run


class FfmpegFlag:
    """
    Class to simplify the way we push flags into the ffmpeg command.
    """

    overwrite: str = '-y'
    """
    Overwrite the output file if existing.

    Notation: **-y**
    """

    @staticmethod
    def force_format(
        format: FfmpegVideoFormat
    ) -> str:
        """
        Force the output format to be the provided 'format'.

        Notation: **-f {format}**
        """
        format = FfmpegVideoFormat.to_enum(format).value

        return f'-f {format}'
    
    @staticmethod
    def safe_routes(
        value: int
    ) -> str:
        """
        To enable or disable unsafe paths.

        Notation: **-safe {value}**
        """
        ParameterValidator.validate_mandatory_int('value', value)
        # TODO: Check that 'value' is a number between -1 and 1

        return f'-safe {str(value)}'
    
    @staticmethod
    def input(
        input: str
    ) -> str:
        """
        To set the input (or inputs) we want.

        Notation: **-i {input}**
        """
        ParameterValidator.validate_mandatory_string('input', input, do_accept_empty = False)

        return f'-i {input}'
    
    @staticmethod
    def audio_codec(
        codec: Union[FfmpegAudioCodec, str]
    ) -> str:
        """
        Sets the general audio codec.

        Notation: **-c:a {codec}**
        """
        # We cannot control the big amount of audio codecs that
        # are available so we allow any string as parameter
        try:
            codec = FfmpegAudioCodec.to_enum(codec).value
        except:
            pass

        return f'-c:a {codec}'
    
    @staticmethod
    def video_codec(
        codec: Union[FfmpegVideoCodec, str]
    ) -> str:
        """
        Sets the general video codec.

        Notation: **-c:v {codec}**
        """
        # We cannot control the big amount of video codecs that
        # are available so we allow any string as parameter
        try:
            codec = FfmpegVideoCodec.to_enum(codec).value
        except:
            pass

        return f'-c:v {codec}'

    @staticmethod
    def v_codec(
        codec: Union[FfmpegVideoCodec, str]
    ) -> str:
        """
        Sets the video codec.

        TODO: I don't know exactly the difference between '-c:v {codec}'
        and the '-vcodec' generated in this method. I keep this method
        until I actually find the difference. I don't even know if the
        video codecs I can provide as values are the same as in the other
        method.

        Notation: **-vcodec {codec}**
        """
        # We cannot control the big amount of video codecs that
        # are available so we allow any string as parameter
        try:
            codec = FfmpegVideoCodec.to_enum(codec).value
        except:
            pass

        return f'-vcodec {codec}'

    @staticmethod
    def codec(
        codec: Union[FfmpegVideoCodec, FfmpegAudioCodec, str]
    ) -> str:
        """
        Sets the general codec with '-c {codec}'.

        -c copy indica que se deben copiar los flujos de audio y video sin recodificación, lo que hace que la operación sea rápida y sin pérdida de calidad. TODO: Turn this 'copy' to AudioCodec and VideoCodec (?)

        Notation: **-c {codec}**
        """
        # We cannot control the big amount of video codecs that
        # are available so we allow any string as parameter

        # TODO: Validate provided 'codec'
        # TODO: This method has a variation, it can be '-c:a' or '-c:v'
        if not PythonValidator.is_instance(codec, [FfmpegVideoCodec, FfmpegAudioCodec]):
            try:
                codec = FfmpegVideoCodec.to_enum(codec)
            except:
                pass

        if not PythonValidator.is_instance(codec, [FfmpegVideoCodec, FfmpegAudioCodec]):
            try:
                codec = FfmpegAudioCodec.to_enum(codec)
            except:
                pass

        if PythonValidator.is_instance(codec, [FfmpegVideoCodec, FfmpegAudioCodec]):
            codec = codec.value

        return f'-c {codec}'
    
    @staticmethod
    def map(
        map: str
    ) -> str:
        """
        Set input stream mapping.
        -map [-]input_file_id[:stream_specifier][,sync_file_id[:stream_s set input stream mapping

        # TODO: Improve this

        Notation: **-map {map}**
        """
        ParameterValidator.validate_mandatory_string('map', map, do_accept_empty = False)

        return f'-map {map}'
    
    @staticmethod
    def filter(
        filter: FfmpegFilter
    ) -> str:
        """
        Sets the expected filter to be used.

        Notation: **-filter {filter}**
        """
        filter = FfmpegFilter.to_enum(filter).value

        return f'-filter {filter}'
    
    @staticmethod
    def frame_rate(
        frame_rate: int
    ) -> str:
        """
        Sets the frame rate (Hz value, fraction or abbreviation)

        Notation: **-r {frame_rate}**
        """
        ParameterValidator.validate_mandatory_int('frame_rate', frame_rate)
        # TODO: Maybe accept some range (?)

        return f'-r {str(frame_rate)}'
    
    @staticmethod
    def pixel_format(
        format: FfmpegPixelFormat
    ) -> str:
        """
        Set the pixel format.

        Notation: **-pix_fmt {format}**
        """
        format = FfmpegPixelFormat.to_enum(format).value

        return f'-pix_fmt {format}'
    
    @staticmethod
    def scale_with_size(
        size: tuple
    ) -> str:
        """
        Set a new size.

        Notation: **-vf scale=size[0]:size[1]**
        """
        ParameterValidator.validate_mandatory_tuple('size', size, 2)

        return f'-vf scale={str(int(size[0]))}:{str(int(size[1]))}'

    @staticmethod
    def scale_with_factor(
        w_factor: float,
        h_factor: float
    ) -> str:
        """
        Set a new size multiplying by a factor.

        Notation: **-vf "scale=iw*w_factor:ih*h_factor"**
        """
        ParameterValidator.validate_mandatory_float('w_factor', w_factor)
        ParameterValidator.validate_mandatory_float('h_factor', h_factor)

        return f'-vf "scale=iw*{str(w_factor)}:ih*{str(h_factor)}"'

    @staticmethod
    def crop(
        size: tuple,
        origin: tuple
    ) -> str:
        """
        Crop the video to a new with the provided 'size'
        starting with the top left corner at the given
        'origin' position of the original video.
        
        Notation: **-vf "crop=size[0]:size[1]:origin[0]:origin[1]"**
        """
        ParameterValidator.validate_mandatory_tuple('size', size, 2)
        ParameterValidator.validate_mandatory_tuple('origin', origin, 2)

        return f"-vf \"crop={str(int(size[0]))}:{str(int(size[1]))}:{str(int(origin[0]))}:{str(int(origin[1]))}\""
    
    @staticmethod
    def seeking(
        seconds: int
    ) -> str:
        """
        Skip the necessary amount of time to go directly
        to the provided 'seconds' time of the input (that
        must be provided after this).

        Notation: **-ss 00:00:03**
        """
        ParameterValidator.validate_mandatory_int('seconds', seconds)

        return f'-ss {Date.seconds_to_hh_mm_ss(seconds)}'
    
    @staticmethod
    def to(
        seconds: int
    ) -> str:
        """
        Used with 'seeking' to match the duration we want
        to apply to the new trimmed input. In general, 
        this will be the amount of 'seconds' to be played.

        Notation: **-to 00:00:05**
        """
        ParameterValidator.validate_mandatory_int('seconds', seconds)

        return f'-to {Date.seconds_to_hh_mm_ss(seconds)}'
    
class FfmpegCommand:
    """
    Class to represent a command to be built and
    executed by the FfmpegHandler.

    A valid example of a command is built like this:
    
    FfmpegCommand([
        FfmpegFlag.force_format(FfmpegVideoFormat.CONCAT),
        FfmpegFlag.safe_routes(0),
        FfmpegFlag.overwrite,
        FfmpegFlag.frame_rate(frame_rate),
        FfmpegFlag.input(concat_filename),
        FfmpegFlag.video_codec(FfmpegVideoCodec.QTRLE),
        FfmpegFlag.pixel_format(pixel_format), # I used 'argb' in the past
        output_filename
    ])
    """
    args: list[Union[FfmpegFlag, any]] = None
    
    def __init__(
        self,
        args: list[Union[FfmpegFlag, any]]
    ):
        # TODO: Validate args
        self.args = args

    def run(
        self
    ):
        """
        Run the command.
        """
        run(self.__str__())

    def __str__(
        self
    ) -> str:
        """
        Turn the command to a string that can be directly
        executed as a ffmpeg command.
        """
        # TODO: Clean args (?)
        # Remove 'None' args, our logic allows them to make it easier
        args = [
            arg
            for arg in self.args
            if arg is not None
        ]

        return f"ffmpeg {' '.join(args)}"

# TODO: Maybe move all these classes to specific files and
# export only this one in the '__init__.py' file...
class FfmpegHandler:
    """
    Class to simplify and encapsulate ffmpeg functionality.
    """

    @staticmethod
    def validate_video_filename(
        filename: str
    ):
        """
        Validate if the provided 'filename' parameter is
        a string and a valid video file (based on its
        extension).
        """
        ParameterValidator.validate_mandatory_string('video_filename', filename, do_accept_empty = False)

        # TODO: If possible (and no dependency issue) check 
        # the content to validate it is parseable as video
        if not FileHandler.is_video_file(filename):
            raise Exception('The provided "filename" is not a valid video file name.')
        
    @staticmethod
    def validate_audio_filename(
        filename: str
    ) -> None:
        """
        Validate if the provided 'filename' parameter is
        a string and a valid audio file (based on its
        extension).
        """
        ParameterValidator.validate_mandatory_string('audio_filename', filename, do_accept_empty = False)

        # TODO: If possible (and no dependency issue) check 
        # the content to validate it is parseable as audio
        if not FileHandler.is_audio_file(filename):
            raise Exception('The provided "filename" is not a valid audio file name.')

    @staticmethod
    def write_concat_file(
        filenames: str
    ) -> str:
        """
        Writes the files to concat in a temporary text file with
        the required format and returns that file filename. This
        is required to use different files as input.

        This method returns the created file filename that 
        includes the list with the 'filenames' provided ready
        to be concatenated.
        """
        text = '\n'.join(
            f"file '{filename}'"
            for filename in filenames
        )

        # TODO: Maybe this below is interesting for the 'yta_general_utils.file.writer'
        # open('concat.txt', 'w').writelines([('file %s\n' % input_path) for input_path in input_paths])
        filename = Temp.get_wip_filename('concat_ffmpeg.txt')
        FileHandler.write_str(filename, text)

        return filename

    @staticmethod
    def run_command(
        command: Union[list[FfmpegFlag, any], FfmpegCommand]
    ) -> None:
        """
        Runs the provided ffmpeg 'command'.
        """
        command = (
            FfmpegCommand(command)
            if not PythonValidator.is_instance(command, FfmpegCommand) else
            command
        )

        command.run()

    # TODO: Check this one below
    @staticmethod
    def get_audio_from_video_deprecated(
        video_filename: str,
        codec: FfmpegAudioCodec = None,
        output_filename: Union[str, None] = None
    ) -> str:
        """
        Exports the audio of the provided video to a local file named
        'output_filename' if provided or as a temporary file.

        # TODO: This has not been tested yet.

        Pro tip: You can read the return with AudioParser.as_audioclip
        method.

        This method returns the filename of the file that has been
        generated as a the audio of the provided video.
        """
        FfmpegHandler.validate_video_filename(video_filename)
        
        output_filename = Output.get_filename(output_filename, FileType.AUDIO)

        if codec:
            codec = FfmpegAudioCodec.to_enum(codec)

        FfmpegCommand([
            FfmpegFlag.input(video_filename),
            FfmpegFlag.audio_codec(codec) if codec else None,
            output_filename
        ]).run()

        return output_filename
    
    @staticmethod
    def get_audio_from_video(
        video_filename: str,
        output_filename: Union[str, None] = None
    ) -> str:
        """
        Exports the audio of the provided video to a local file named
        'output_filename' if provided or as a temporary file.

        Pro tip: You can read the return with AudioParser.as_audioclip
        method.

        This method returns the filename of the file that has been
        generated as a the audio of the provided video.
        """
        FfmpegHandler.validate_video_filename(video_filename)
        
        output_filename = Output.get_filename(output_filename, FileType.AUDIO)

        # TODO: Verify valid output_filename extension

        FfmpegCommand([
            FfmpegFlag.input(video_filename),
            FfmpegFlag.map('0:1'),
            output_filename
        ]).run()

        return output_filename

    @staticmethod
    def get_best_thumbnail(
        video_filename: str,
        output_filename: Union[str, None] = None
    ) -> str:
        """
        Gets the best thumbnail of the provided 'video_filename'.

        Pro tip: You can read the return with ImageParser.to_pillow
        method.

        This method returns the filename of the file that has been
        generated as a the thumbnail of the provided video.
        """
        FfmpegHandler.validate_video_filename(video_filename)

        output_filename = Output.get_filename(output_filename, FileType.IMAGE)

        FfmpegCommand([
            FfmpegFlag.input(video_filename),
            FfmpegFlag.filter(FfmpegFilter.THUMBNAIL),
            output_filename
        ]).run()

        return output_filename
    
    @staticmethod
    def concatenate_videos(
        video_filenames: str,
        output_filename: str = None
    ) -> str:
        """
        Concatenates the provided 'video_filenames' in the order in
        which they are provided.

        Using Ffmpeg is very useful when trying to concatenate similar
        videos (the ones that we create always with the same 
        specifications) because the codecs are the same so the speed
        is completely awesome.

        Pro tip: You can read the return with VideoParser.to_moviepy
        method.

        This method returns the filename of the file that has been
        generated as a concatenation of the provided ones.
        """
        for video_filename in video_filenames:
            FfmpegHandler.validate_video_filename(video_filename)

        output_filename = Output.get_filename(output_filename, FileType.VIDEO)

        concat_filename = FfmpegHandler.write_concat_file(video_filenames)

        FfmpegCommand([
            FfmpegFlag.overwrite,
            FfmpegFlag.force_format(FfmpegVideoFormat.CONCAT),
            FfmpegFlag.safe_routes(0),
            FfmpegFlag.input(concat_filename),
            FfmpegFlag.codec('copy'),
            output_filename
        ]).run()

        return output_filename
    
    @staticmethod
    def concatenate_images(
        image_filenames: str,
        frame_rate = 60,
        pixel_format: FfmpegPixelFormat = FfmpegPixelFormat.YUV420p,
        output_filename: Union[str, None] = None
    ) -> str:
        """
        Concatenates the provided 'image_filenames' in the order in
        which they are provided.

        Using Ffmpeg is very useful when trying to concatenate similar
        images because the speed is completely awesome.

        Pro tip: You can read the return with VideoParser.to_moviepy().

        This method returns the filename of the file that has been
        generated as a concatenation of the provided ones.
        """
        for image_filename in image_filenames:
            FfmpegHandler.validate_video_filename(image_filename)

        output_filename = Output.get_filename(output_filename, FileType.VIDEO)

        concat_filename = FfmpegHandler.write_concat_file(image_filenames)

        # TODO: Should we check the pixel format or give freedom (?)
        # pixel_format = FfmpegPixelFormat.to_enum(pixel_format)

        FfmpegCommand([
            FfmpegFlag.force_format(FfmpegVideoFormat.CONCAT),
            FfmpegFlag.safe_routes(0),
            FfmpegFlag.overwrite,
            FfmpegFlag.frame_rate(frame_rate),
            FfmpegFlag.input(concat_filename),
            FfmpegFlag.video_codec(FfmpegVideoCodec.QTRLE),
            FfmpegFlag.pixel_format(pixel_format), # I used 'argb' in the past
            output_filename
        ]).run()

        return output_filename

    @staticmethod
    def resize_video(
        video_filename: str,
        size: tuple,
        output_filename: Union[str, None] = None
    ) -> str:
        """
        Resize the provided 'video_filename', by keeping
        the aspect ratio (cropping if necessary), to the
        given 'size' and stores it locally as
        'output_filename'.

        This method returns the generated file filename.

        See more: 
        https://www.gumlet.com/learn/ffmpeg-resize-video/
        """
        FfmpegHandler.validate_video_filename(video_filename)
        ParameterValidator.validate_mandatory_tuple('size', size, None)
        # TODO: I think we don't need this with the 'Output.get_filename'
        ParameterValidator.validate_mandatory_string('output_filename', output_filename, do_accept_empty = False)
        
        output_filename = Output.get_filename(output_filename, FileType.VIDEO)

        # Validate that 'size' is a valid size
        # TODO: This code is a bit strange, but was refactored from the
        # original one that was in 'yta_multimedia' to remove the
        # dependency. Maybe update it?
        if not PythonValidator.is_numeric_tuple_or_list_or_array_of_2_elements_between_values(size, NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE, NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE):
            # TODO: Raise error
            raise Exception(f'The provided size parameter is not a tuple or array, or does not have 2 elements that are numbers between {str(NORMALIZATION_MIN_VALUE)} and {str(NORMALIZATION_MAX_VALUE)}.')

        w, h = get_video_size(video_filename)

        if (w, h) == size:
            # No need to resize, we just copy it to output
            FileHandler.copy_file(video_filename, output_filename)
        else:
            # First, we need to know if we need to scale it
            original_ratio = w / h
            new_ratio = size[0] / size[1]

            new_size = (
                (w * (size[1] / h), size[1])
                # Original video is wider than the expected one
                if original_ratio > new_ratio else
                # Original video is higher than the expected one
                (size[0], h * (size[0] / w))
                if original_ratio < new_ratio else
                (size[0], size[1])
            )

            tmp_filename = Temp.get_wip_filename('tmp_ffmpeg_scaling.mp4')

            # Scale to new dimensions
            FfmpegCommand([
                FfmpegFlag.input(video_filename),
                FfmpegFlag.scale_with_size(new_size),
                tmp_filename
            ]).run()

            # Now, with the new video resized, we look for the
            # cropping points we need to apply and we crop it
            top_left, _ = get_cropping_points_to_keep_aspect_ratio(new_size, size)

            # Second, we need to know if we need to crop it
            FfmpegCommand([
                FfmpegFlag.input(tmp_filename),
                FfmpegFlag.crop(size, top_left),
                FfmpegFlag.overwrite,
                output_filename
            ]).run()

        return output_filename
    
    @staticmethod
    def trim(
        video_filename: str,
        start_seconds: int,
        duration_seconds: int,
        output_filename: Union[str, None] = None
    ) -> str:
        """
        Trims the provided 'video_filename' and generates a
        shorter resource that is stored as 'output_filename'.
        This new resource will start from 'start_seconds' and
        last the provided 'duration_seconds'.

        This method returns the generated file filename.

        Thank you:
        https://www.plainlyvideos.com/blog/ffmpeg-trim-videos
        https://trac.ffmpeg.org/wiki/Seeking
        """
        FfmpegHandler.validate_video_filename(video_filename)
        ParameterValidator.validate_mandatory_positive_number('start_seconds', start_seconds, do_include_zero = True)
        ParameterValidator.validate_mandatory_positive_number('duration_seconds', duration_seconds, do_include_zero = True)
        
        output_filename = Output.get_filename(output_filename, FileType.VIDEO)

        command = FfmpegCommand([
            FfmpegFlag.seeking(start_seconds),
            FfmpegFlag.input(video_filename),
            FfmpegFlag.to(duration_seconds),
            FfmpegFlag.codec(FfmpegVideoCodec.COPY),
            FfmpegFlag.overwrite,
            output_filename
        ])
        # TODO: Remove this command when confirmed
        print(command)
        command.run()

        #ffmpeg_command = f'-ss 00:02:05 -i {video} -to 00:03:10 -c copy video-cutted-ffmpeg.mp4'
        return output_filename

    # TODO: This method must replace the one in 
    # yta_multimedia\video\audio.py > set_audio_in_video_ffmpeg
    @staticmethod
    def set_audio(
        video_filename: str,
        audio_filename: str,
        output_filename: Union[str, None] = None
    ):
        """
        TODO: This method has not been properly tested yet.

        Set the audio given in the 'audio_filename' in the also
        provided video (in 'video_filename') and creates a new
        file containing the video with the audio.

        This method returns the generated file filename.
        """
        FfmpegHandler.validate_video_filename(video_filename)
        FfmpegHandler.validate_audio_filename(audio_filename)
        # TODO: I think we don't need this with the 'Output.get_filename'
        ParameterValidator.validate_mandatory_string('output_filename', output_filename)
        
        output_filename = Output.get_filename(output_filename, FileType.VIDEO)
        
        # cls.run_command([
        #     FfmpegFlag.input(video_filename),
        #     FfmpegFlag.input(audio_filename),
        #     output_filename
        # # TODO: Unfinished
        # ])

        # TODO: Is this actually working (?)
        run(f"ffmpeg -i {video_filename} -i {audio_filename} -c:v copy -c:a aac -strict experimental -y {output_filename}")

        return output_filename
        
        # Apparently this is the equivalent command according
        # to ChatGPT, but maybe it doesn't work
        # ffmpeg -i input_video -i input_audio -c:v copy -c:a aac -strict experimental -y output_filename

        # There is also a post that says this:
        # ffmpeg -i input.mp4 -i input.mp3 -c copy -map 0:v:0 -map 1:a:0 output.mp4
        # in (https://superuser.com/a/590210)


        # # TODO: What about longer audio than video (?)
        # # TODO: This is what was being used before FFmpegHandler
        # input_video = ffmpeg.input(video_filename)
        # input_audio = ffmpeg.input(audio_filename)

        # ffmpeg.concat(input_video, input_audio, v = 1, a = 1).output(output_filename).run(overwrite_output = True)

    
    # TODO: Create a 'set_audio_in_video' method to replace the
    # yta_multimedia\video\audio.py > set_audio_in_video_ffmpeg

    # TODO: Keep going

    # https://www.reddit.com/r/ffmpeg/comments/ks8zfs/comment/gieu7x6/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # https://stackoverflow.com/questions/38368105/ffmpeg-custom-sequence-input-images/51618079#51618079
    # https://stackoverflow.com/a/66014158