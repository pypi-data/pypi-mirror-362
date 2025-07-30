# led_matrix_lib/status_handler.py


_status = None


def set_status(new_status):

    global _status
    _status = new_status


def get_status():
    return _status
