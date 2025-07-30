"""
Module to simplify the way we work with
the moviepy video time moment 't'.
"""
from yta_validation.parameter import ParameterValidator


SMALL_AMOUNT_TO_FIX = 0.0000000001
"""
Small amount we need to add to fix some floating
point number issues we've found. Something like
0.3333333333333326 will turn into 9 frames for a 
fps = 30 video, but this is wrong, as it should
be 10 frames and it is happening due to a minimal
floating point difference.
"""


class T:
    """
    Class to wrap the functionality related
    to handling the moviepy video time 
    moment 't'.
    """

    def get_frame_indexes(
        duration: float,
        fps: float
    ):
        """
        Get the list of the frame indexes of
        the video with the given 'duration'
        and 'fps'.

        If a video lasts 1 second and has 5
        fps, this method will return: 0, 1,
        2, 3, 4.
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)

        return [
            i
            for i in range(int(duration * fps + SMALL_AMOUNT_TO_FIX))
        ]
    
    def get_first_n_frames_indexes(
        duration: float,
        fps: float,
        n: int
    ):
        """
        Obtain the first 'n' frames indexes of the current
        video to be able to use them within a condition
        with the '.get_frame(t)' method.

        This list can be used to check if the current frame
        number (index) is on it or not, to apply the frame
        image effect or to leave it as it is.

        Each frame time moment has been increased by 
        a small amount to ensure it is greater than 
        the base frame time value (due to decimals
        issue).
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_int('n', n, do_include_zero = False)

        return T.get_odd_frames_indexes(duration, fps)[:n]

    def get_last_n_frames_indexes(
        duration: float,
        fps: float,
        n: int
    ):
        """
        Obtain the last 'n' frames indexes of the current
        video to be able to use them within a condition
        with the '.get_frame(t)' method.

        This list can be used to check if the current frame
        number (index) is on it or not, to apply the frame
        image effect or to leave it as it is.

        Each frame time moment has been increased by 
        a small amount to ensure it is greater than 
        the base frame time value (due to decimals
        issue).
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_int('n', n, do_include_zero = False)

        return T.get_odd_frames_indexes(duration, fps)[-n:]

    def get_even_frames_indexes(
        duration: float,
        fps: float
    ):
        """
        Array containing all the even indexes of video
        frames that can be used to obtain its corresponding
        frame time moment, or to simplify calculations.
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)

        frame_indexes = T.get_frame_indexes(duration, fps)

        return frame_indexes[frame_indexes % 2 == 0]

    def get_first_n_even_frames_indexes(
        duration: float,
        fps: float,
        n: int
    ):
        """
        Obtain the first 'n' even frames indexes of the 
        current video to be able to use them within a
        condition with the '.get_frame(t)' method.

        This list can be used to check if the current frame
        number (index) is on it or not, to apply the frame
        image effect or to leave it as it is.

        If 'n' is greater than the real number of even
        frames, 'n' will get that value so the result will
        be all the even frames indexes.

        Each frame time moment has been increased by 
        a small amount to ensure it is greater than 
        the base frame time value (due to decimals
        issue).
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_int('n', n, do_include_zero = False)

        return T.get_even_frames_indexes(duration, fps)[:n]

    def get_last_n_even_frames_indexes(
        duration: float,
        fps: float,
        n: int
    ):
        """
        Obtain the last 'n' even frames indexes of the
        current video to be able to use them within a
        condition with the '.get_frame(t)' method.

        This list can be used to check if the current frame
        number (index) is on it or not, to apply the frame
        image effect or to leave it as it is.

        If 'n' is greater than the real number of even
        frames, 'n' will get that value so the result will
        be all the even frames indexes.

        Each frame time moment has been increased by 
        a small amount to ensure it is greater than 
        the base frame time value (due to decimals
        issue).
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_int('n', n, do_include_zero = False)

        return T.get_even_frames_indexes(duration, fps)[-n:]

    def get_odd_frames_indexes(
        duration: float,
        fps: float,
    ):
        """
        Array containing all the odd indexes of video
        frames that can be used to obtain its corresponding
        frame time moment, or to simplify calculations.
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)

        frame_indexes = T.get_frame_indexes(duration, fps)

        return frame_indexes[frame_indexes % 2 != 0]

    def get_last_n_odd_frames_indexes(
        duration: float,
        fps: float,
        n: int
    ):
        """
        Obtain the last 'n' odd frames indexes of the
        current video to be able to use them within a
        condition with the '.get_frame(t)' method.

        This list can be used to check if the current frame
        number (index) is on it or not, to apply the frame
        image effect or to leave it as it is.

        If 'n' is greater than the real number of odd
        frames, 'n' will get that value so the result will
        be all the odd frames indexes.

        Each frame time moment has been increased by 
        a small amount to ensure it is greater than 
        the base frame time value (due to decimals
        issue).
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_int('n', n, do_include_zero = False)

        return T.get_odd_frames_indexes(duration, fps)[-n:]

    def get_first_n_odd_frames_indexes(
        duration: float,
        fps: float,
        n: int
    ):
        """
        Obtain the first 'n' odd frames indexes of the 
        current video to be able to use them within a
        condition with the '.get_frame(t)' method.

        This list can be used to check if the current frame
        number (index) is on it or not, to apply the frame
        image effect or to leave it as it is.

        If 'n' is greater than the real number of odd
        frames, 'n' will get that value so the result will
        be all the odd frames indexes.

        Each frame time moment has been increased by 
        a small amount to ensure it is greater than 
        the base frame time value (due to decimals
        issue).
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_int('n', n, do_include_zero = False)

        return T.get_odd_frames_indexes(duration, fps)[:n]

    def get_frame_time_moments(
        duration: float,
        fps: float
    ):
        """
        Get the time moment of each video
        frame according to the provided video
        'duration' and 'fps'. This will always
        include the second 0 and the
        inmediately before the duration.

        If a video lasts 1 second and has 5
        fps, this method will return: 0, 0.2,
        0.4, 0.6, 0.8.

        This method can return non-exact
        decimal values so we recommend you to
        add a small amount to ensure it is
        above the expected base frame time.
        """
        ParameterValidator.validate_mandatory_positive_number('duration', duration, do_include_zero = False)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)

        return [
            (1 / fps * i) + SMALL_AMOUNT_TO_FIX
            for i in range(int(duration * fps + SMALL_AMOUNT_TO_FIX) + 1)
        ][:-1]

    def frame_time_to_frame_index(
        t: float,
        fps: float
    ):
        """
        Transform the provided 't' frame time to 
        its corresponding frame index according
        to the 'fps' provided.

        This method applies the next formula:

        int(t * fps + SMALL_AMOUNT_TO_FIX)
        """
        ParameterValidator.validate_mandatory_positive_number('t', t, do_include_zero = True)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)

        return int((t + SMALL_AMOUNT_TO_FIX) * fps)

    def frame_index_to_frame_time(
        i: int,
        fps: float
    ):
        """
        Transform the provided 'i' frame index to
        its corresponding frame time according to
        the 'fps' provided.

        This method applies the next formula:

        i * 1 / fps + SMALL_AMOUNT_TO_FIX
        """
        ParameterValidator.validate_mandatory_positive_int('i', i, do_include_zero = True)
        ParameterValidator.validate_mandatory_positive_number('fps', fps, do_include_zero = False)

        return i * 1 / fps + SMALL_AMOUNT_TO_FIX
