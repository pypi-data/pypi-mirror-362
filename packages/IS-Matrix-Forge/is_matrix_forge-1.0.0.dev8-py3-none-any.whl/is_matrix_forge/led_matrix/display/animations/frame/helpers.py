from typing import Any, List, Union
from pathlib import Path

from inspyre_toolbox.path_man import provision_path

from is_matrix_forge.led_matrix.display.grid.helpers import is_valid_grid


def check_path(path: Union[str, Path], skip_exists_check: bool = False) -> Path:
    path = provision_path(path)

    if not skip_exists_check and not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return path


def load_frames_from_file(path: Union[str, Path]) -> List['Frame']:
    from is_matrix_forge.led_matrix.display.animations.frame.base import Frame
    from is_matrix_forge.led_matrix.helpers import get_json_from_file

    path = provision_path(path)



def is_valid_frames(raw: Any, width: int, height: int) -> bool:
    """
    Check if a list of frames is valid.

    A list of frames is valid if it is a list of lists of 0s and 1s, and the length of each list is equal to the width
    and height.


    Parameters:
        raw (Any):
            The list of frames to check.

        width (int):
            The expected width (in pixels) of the frames.

        height (int):
            The expected height (in pixels) of the frames.

    Returns:
        bool:
            - True if the list of frames is valid.
            - False otherwise.
    """
    return (
            isinstance(raw, list)
            and len(raw) > 0
            and all(is_valid_grid(frame, width, height) for frame in raw)
    )


def migrate_frame(matrix_spec: List[List[int]], duration: Union[int, str]) -> dict:
    """
    Creates a frame entry from a matrix spec.

    Note:
         A 'matrix spec' is a list of lists each containing 0s and 1s representing the pixels of a frame. 1 indicates a
         pixel is on; 0 indicates it is off.
    """
    return {
        'grid':     matrix_spec,
        'duration': duration
    }
