from yta_constants.enum import YTAEnum as Enum


class FfmpegAudioCodec(Enum):
    """
    TODO: Fill this

    Should be used in the "**-c:a {codec}**" flag.
    """

    AAC = 'aac'
    """
    Default encoder.
    """
    AC3 = 'ac3'
    """
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-ac3-and-ac3_005ffixed
    """
    AC3_FIXED = 'ac3_fixed'
    """
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-ac3-and-ac3_005ffixed
    """
    FLAC = 'flac'
    """
    FLAC (Free Lossless Audio Codec) Encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-flac-2
    """
    OPUS = 'opus'
    """
    This is a native FFmpeg encoder for the Opus format. Currently, it's
    in development and only implements the CELT part of the codec. Its
    quality is usually worse and at best is equal to the libopus encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-opus
    """
    LIBFDK_AAC = 'libfdk_aac'
    """
    libfdk-aac AAC (Advanced Audio Coding) encoder wrapper. The libfdk-aac
    library is based on the Fraunhofer FDK AAC code from the Android project.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libfdk_005faac
    """
    LIBLC3 = 'liblc3'
    """
    liblc3 LC3 (Low Complexity Communication Codec) encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-liblc3
    """
    LIBMP3LAME = 'libmp3lame'
    """
    LAME (Lame Ain't an MP3 Encoder) MP3 encoder wrapper.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libmp3lame-1
    """
    LIBOPENCORE_AMRNB = 'libopencore_amrnb'
    """
    OpenCORE Adaptive Multi-Rate Narrowband encoder.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libopencore_002damrnb-1ss
    """
    LIBOPUS = 'libopus'
    """
    libopus Opus Interactive Audio Codec encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libopus-1
    """
    LIBSHINE = 'libshine'
    """
    Shine Fixed-Point MP3 encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libshine-1
    """
    LIBTWOLAME = 'libtwolame'
    """
    TwoLAME MP2 encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libtwolame
    """
    LIBVO_AMRWBENC = 'libvo-amrwbenc'
    """
    VisualOn Adaptive Multi-Rate Wideband encoder.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libvo_002damrwbenc
    """
    LIBVORBIS = 'libvorbis'
    """
    libvorbis encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libvorbis
    """
    MJPEG = 'mjpeg'
    """
    Motion JPEG encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-mjpeg
    """
    WAVPACK = 'wavpack'
    """
    WavPack lossless audio encoder.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-wavpack
    """
    COPY = 'copy'
    """
    Indicates that the codec must be copied from 
    the input.
    """

class FfmpegVideoCodec(Enum):
    """
    These are the video codecs available as Enums. The amount of codecs
    available depends on the ffmpeg built version.
    
    Should be used in the "**-c:v {codec}**" flag.
    """

    A64_MULTI = 'a64_multi'
    """
    A64 / Commodore 64 multicolor charset encoder. a64_multi5 is extended with 5th color (colram).

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-a64_005fmulti_002c-a64_005fmulti5
    """
    A64_MULTI5 = 'a64_multi5'
    """
    A64 / Commodore 64 multicolor charset encoder. a64_multi5 is extended with 5th color (colram).

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-a64_005fmulti_002c-a64_005fmulti5
    """
    CINEPAK = 'Cinepak'
    """
    Cinepak aka CVID encoder. Compatible with Windows 3.1 and vintage MacOS.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-Cinepak
    """
    GIF = 'GIF'
    """
    GIF image/animation encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-Cinepak
    """
    HAP = 'Hap'
    """
    Vidvox Hap video encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-Hap
    """
    JPEG2000 = 'jpeg2000'
    """
    The native jpeg 2000 encoder is lossy by default

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-jpeg2000
    """
    LIBRAV1E = 'librav1e'
    """
    rav1e AV1 encoder wrapper.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-librav1e
    """
    LIBAOM_AV1 = 'libaom-av1'
    """
    libaom AV1 encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libaom_002dav1
    """
    # TODO: Continue with this (https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libsvtav1)
    QTRLE = 'qtrle'
    """
    TODO: Find information about this video codec.

    More info: ???
    """
    PRORES = 'prores'
    """
    Apple ProRes encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-ProRes
    """
    COPY = 'copy'
    """
    Indicates that the codec must be copied from 
    the input.
    """

class FfmpegVideoFormat(Enum):
    """
    Enum list to simplify the way we choose a video format for
    the ffmpeg command. This should be used with the FfmpegFlag
    '-f' flag that forces that video format.

    Should be used in the "**-f {format}**" flag.
    """

    CONCAT = 'concat'
    """
    The format will be the concatenation.
    """
    AVI = 'avi'
    """
    Avi format.

    # TODO: Explain more
    """
    PNG = 'png'
    """
    # TODO: Look for mor information about this vcodec
    # TODO: I don't know if this one is actually an FfmpegVideoFormat
    # or if I need to create another Enum class. This option us used
    # in the '-vcodec' option, and the other ones are used in the
    # 'c:v' option.
    """
    # TODO: Keep going

class FfmpegFilter(Enum):
    """
    Enum list to simplify the way we use a filter for the
    ffmpeg command.

    Should be used in the "**-filter {filter}**" flag.
    """

    THUMBNAIL = 'thumbnail'
    """
    Chooses the most representative frame of the video to be used
    as a thumbnail.
    """

class FfmpegPixelFormat(Enum):
    """
    Enum list to simplify the way we use a pixel format for
    the ffmpeg command.

    Should be used in the "**-pix_fmt {format}**" flag.
    """
    
    YUV420p = 'yuv420p'
    """
    This is de default value. TODO: Look for more information about it
    """
    RGB24 = 'rgb24'
    """
    TODO: Look for more information about this pixel format.
    """
    ARGB = 'argb'
    """
    TODO: Look for more information about this pixel format
    """
    YUVA444P10LE = 'yuva444p10le'
    """
    TODO: Look for more information about this pixel format
    """
