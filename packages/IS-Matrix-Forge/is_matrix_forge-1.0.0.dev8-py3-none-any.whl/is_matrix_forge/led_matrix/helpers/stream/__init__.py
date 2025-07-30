import cv2
from serial import Serial, SerialException

from is_matrix_forge.led_matrix.constants import *
from is_matrix_forge.led_matrix.helpers.status_handler import get_status
from is_matrix_forge.led_matrix import send_col

from .errors import *
from ...errors.matrix import MatrixConnectionError, MatrixInUseError


def play_stream(dev, capture, mode: str) -> None:
    """
    Core routine for piping frames to the LED matrix via serial.

    Parameters:
        dev (`serial.tools.list_ports_common.ListPortInfo`):
            The serial port descriptor returned by `serial.tools.list_ports`.

        capture (`cv2.VideoCapture`):
            An already-opened OpenCV capture object.

        mode ({'camera', 'video'}):
            Identifies the status flag and grayscale conversion table entry.

    Returns:
        None

    Raises:
        RuntimeError:
            If the serial port is not open.
    """
    try:
        with Serial(dev.device, DEFAULT_BAUDRATE) as s:

            ok, first_frame = capture.read()

            if not ok:
                raise StreamSourceUnreadableError()
    except SerialException as e:
        raise MatrixInUseError from e

    # ── Calculate scaling and crop once based on the first frame ───────
    scale_y = HEIGHT / first_frame.shape[0]
    scaled_w = int(round(first_frame.shape[1] * scale_y))
    start_x = max(0, int(round(scaled_w / 2 - WIDTH / 2)))
    end_x = min(scaled_w, start_x + WIDTH)
    dim = (HEIGHT, scaled_w)

    # ── Main pump loop ────────────────────────────────────────────────
    while get_status() == mode:
        ok, frame = capture.read()
        if not ok:
            break

        gray     = cv2.cvtColor(frame, __GRAYSCALE_CVT[mode])
        resized  = cv2.resize(gray, dim)
        cropped  = resized[0:HEIGHT, start_x:end_x]

        # Stream one column at a time
        for x in range(cropped.shape[1]):
            send_col(
                dev,
                s,
                x,
                [cropped[y, x] for y in range(HEIGHT)]
            )
        commit_cols(dev, s)

    capture.release()
