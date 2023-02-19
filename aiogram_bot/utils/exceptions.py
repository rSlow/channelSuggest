class MediaTypeError(TypeError):
    def __init__(self, media_type: str):
        super().__init__(f"<{media_type}> not expected as media type")


class TooMuchMediaError(RuntimeError):
    pass
