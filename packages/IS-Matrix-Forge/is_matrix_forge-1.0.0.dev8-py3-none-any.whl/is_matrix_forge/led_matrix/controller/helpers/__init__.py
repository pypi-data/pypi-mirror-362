from __future__ import annotations

def get_controllers(threaded: bool = False) -> list['LEDMatrixController']:
    from is_matrix_forge.led_matrix.constants import DEVICES
    from is_matrix_forge.led_matrix.controller.controller import LEDMatrixController

    return [LEDMatrixController(device, 100, thread_safe=True) for device in DEVICES]
