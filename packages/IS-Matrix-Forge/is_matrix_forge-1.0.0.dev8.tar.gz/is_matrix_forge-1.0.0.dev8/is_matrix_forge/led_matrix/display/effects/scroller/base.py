from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar
from is_matrix_forge.common.decorators import freeze_setter

if TYPE_CHECKING:
    from is_matrix_forge.led_matrix import LEDMatrixController

# Make our base class generic so you can subclass it for other scrollers, too
C = TypeVar('C', bound='LEDMatrixController')

class Scroller(ABC, Generic[C]):
    """
    Base functionality for scrolling-like animations on an LEDMatrixController.

    Subclasses only need to implement start_scrolling (and stop_scrolling, if desired).
    """

    def __init__(
        self,
        controller: C,
        *,
        keep_lit: bool = True
    ):
        self._controller: C | None = None
        self._keep_lit: bool | None = None

        # these setters enforce type checks/freeze behavior
        self.controller = controller
        self.keep_lit = keep_lit

    @property
    def controller(self) -> C:
        """The LEDMatrixController instance used for scrolling."""
        return self._controller  # type: ignore

    @controller.setter
    @freeze_setter(allow_reassignment_to_same_value=True)
    def controller(self, new: C) -> None:
        from is_matrix_forge.led_matrix.controller import LEDMatrixController
        assert isinstance(new, LEDMatrixController), (
            f"Expected LEDMatrixController, got {type(new).__name__}"
        )
        self._controller = new

    @property
    def is_scrolling(self) -> bool:
        """
        Whether a scroll animation is currently in progress.
        """
        return bool(self.controller.animating)

    @property
    def keep_lit(self) -> bool:
        """
        If True, keep the LED matrix powered while scrolling.
        """
        return self._keep_lit  # type: ignore

    @keep_lit.setter
    def keep_lit(self, new: bool) -> None:
        if not isinstance(new, bool):
            raise TypeError('"keep_lit" must be a bool')
        self._keep_lit = new

    @abstractmethod
    def start_scrolling(self) -> None:
        """
        Begin the scroll animation. Must be implemented by subclasses.
        """

    def stop_scrolling(self) -> None:
        """
        Stop the scroll animation. Optional override by subclasses.
        """
        self.controller.animating = False
