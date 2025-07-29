"""
TODO: This is a frame filter, which is
actually an image filter to apply to 
one video frame, that is an image. So,
I think this filter should be in the
'yta_image_...' library but being 
applied as a filter to the video in the
'yta_video_advanced_filters' library.
"""
from skimage.filters import gaussian as skimage_gaussian
from typing import Union


class FrameFilter:
    """
    Filters to be applied on moviepy video frames so we
    can modify them by using 'clip.transform' method.

    Example below:
    ``` 
    clip.transform(
        lambda get_frame, t:
        FrameFilter.blur(get_frame, t, blur_radius = blur_radius)
    )
    ```
    
    """
    @staticmethod
    def blur(
        get_frame,
        t,
        blur_radius: Union[int, None] = None
    ):
        return skimage_gaussian(get_frame(t).astype(float), sigma = blur_radius)