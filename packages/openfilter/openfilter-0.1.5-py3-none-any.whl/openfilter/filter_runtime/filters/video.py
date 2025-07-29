from openfilter.filter_runtime.filter import FilterConfig, Filter

__all__ = ['VideoConfig', 'Video']

DEPRECATION_MESSAGE = "Video, VideoConfig and the 'video' docker image have been deprecated! Use " \
    "VideoIn / VideoInConfig / 'video_in' or VideoOut / VideoOutConfig / 'video_out' as required in its place."


class VideoConfig(FilterConfig):
    def __init__(self, *args, **kwargs):
        raise RuntimeError(DEPRECATION_MESSAGE)


class Video(Filter):
    """DEPRECATED!"""

    FILTER_TYPE = 'DEPRECATED'

    def __init__(self, *args, **kwargs):
        raise RuntimeError(DEPRECATION_MESSAGE)


if __name__ == '__main__':
    Video.run()
