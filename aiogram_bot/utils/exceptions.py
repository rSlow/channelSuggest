class MediaTypeError(TypeError):
    def __init__(self, media_type: str):
        super().__init__(f"<{media_type}> not expected as media type")


class AudioMixedError(TypeError):
    pass


class DocumentMixedError(TypeError):
    pass


class TooMuchMediaError(RuntimeError):
    pass
