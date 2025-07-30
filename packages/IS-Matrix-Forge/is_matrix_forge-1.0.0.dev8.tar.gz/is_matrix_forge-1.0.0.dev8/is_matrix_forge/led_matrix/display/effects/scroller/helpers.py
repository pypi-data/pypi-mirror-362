from easy_exit_calls import ExitCallHandler
from is_matrix_forge.common.decorators import freeze_setter, validate_type


ECH = ExitCallHandler()
DEFAULT_TIME_BETWEEN_JIGGLES = 50
MAX_TIME_BETWEEN_JIGGLES     = 59  # Matrix goes to sleep after 60 seconds of command inactivity, so we need to jiggle
                                   # at least once every minute


class MatrixJiggler:
    def __init__(
            self,
            controller    = None,
            power_monitor = None,
            interval: int = None,
            do_not_clear_on_stop: bool = False,

    ):
        if controller and power_monitor:
            raise ValueError("Cannot specify both `controller` and `power_monitor`")

        self.controller         = controller
        self.power_monitor      = power_monitor
        self.clear_on_stop      = not do_not_clear_on_stop
        self._controller        = None
        self.__interval         = None
        self.__last_jiggle_time = None
        self._power_monitor     = None

    @property
    def controller(self):
        return self._controller

    @property
    def interval(self) -> float:
        return self.__interval

    @interval.setter
    @validate_type([float, int], float)
    def interval(self, new):
        self.__interval = new

    @property
    def power_monitor(self):
        return self._power_monitor

    @power_monitor.setter
    @freeze_setter()
    def power_monitor(self, new):
        from is_matrix_forge.monitor.monitor import PowerMonitor

        if not isinstance(new, PowerMonitor):
            raise TypeError(f"Expected {PowerMonitor}, got {type(new)}")

        self._controller = new.controller

        self._power_monitor = new

    def cleanup(self):
        if self.clear_on_stop:
            self.controller.clear()
