from dataclasses import dataclass
from typing import Dict, List

from is_matrix_forge.led_matrix.display.grid.grid import MATRIX_WIDTH, MATRIX_HEIGHT
from is_matrix_forge.led_matrix.display.grid import Grid
from is_matrix_forge.led_matrix.display.animations.animation import Animation, Frame


@dataclass(frozen=True)
class TextScrollerConfig:
    """Immutable configuration for the text scroller."""
    text: str
    font_map: Dict[str, List[List[int]]]
    spacing: int = 1
    frame_duration: float = 0.05
    wrap: bool = False  # unused for vertical mode
    direction: str = "horizontal"  # one of: "horizontal", "vertical_up", "vertical_down"


class TextScroller:
    """Generates scrolling‐text Animations in horizontal or vertical directions."""

    VALID_DIRS = {"horizontal", "vertical_up", "vertical_down"}

    def __init__(self, config: TextScrollerConfig):
        self.config = config
        if config.direction not in self.VALID_DIRS:
            raise ValueError(f"Unsupported scroll direction: {config.direction}")
        # ensure font fits display height
        sample = next(iter(config.font_map.values()))
        if len(sample) > MATRIX_HEIGHT:
            raise ValueError(f"Font height {len(sample)} > display height {MATRIX_HEIGHT}")

    def generate_animation(self) -> Animation:
        """Build and return your scrolling‐text Animation.

        Raises:
            ValueError: if `text` contains a character not in `font_map`.
        """
        # build list of glyphs from text
        glyphs: List[List[List[int]]] = []  # each glyph: rows of cols
        for ch in self.config.text:
            glyph = self.config.font_map.get(ch)
            if glyph is None:
                raise ValueError(f"Character '{ch}' not found in font_map")
            glyphs.append(glyph)

        glyph_h = len(glyphs[0])
        glyph_ws = [len(g[0]) for g in glyphs]

        frames: List[Frame] = []

        if self.config.direction == "horizontal":
            # existing horizontal behavior unchanged
            total_w = sum(glyph_ws) + self.config.spacing * (len(glyph_ws) - 1)
            canvas = [[0] * total_w for _ in range(MATRIX_HEIGHT)]
            x = 0
            # render glyphs horizontally
            for g, w in zip(glyphs, glyph_ws):
                vpad = (MATRIX_HEIGHT - glyph_h) // 2
                for r in range(glyph_h):
                    canvas[vpad + r][x : x + w] = g[r]
                x += w + self.config.spacing

            offsets = range(0, total_w) if self.config.wrap else range(-MATRIX_WIDTH, total_w)
            for off in offsets:
                window = [
                    [canvas[r][off + c] if 0 <= off + c < total_w else 0 for c in range(MATRIX_WIDTH)]
                    for r in range(MATRIX_HEIGHT)
                ]
                cols = [[window[r][c] for r in range(MATRIX_HEIGHT)] for c in range(MATRIX_WIDTH)]
                frames.append(Frame(grid=Grid(init_grid=cols)))

        else:
            # vertical mode: scroll each glyph in turn, center-justified
            direction = self.config.direction
            for glyph, w in zip(glyphs, glyph_ws):
                # horizontal center offset
                x0 = (MATRIX_WIDTH - w) // 2
                # choose offset range
                if direction == "vertical_up":
                    offsets = range(MATRIX_HEIGHT, -glyph_h - 1, -1)
                else:  # vertical_down
                    offsets = range(-glyph_h, MATRIX_HEIGHT + 1)
                # scroll this glyph
                for off in offsets:
                    window = [[0] * MATRIX_WIDTH for _ in range(MATRIX_HEIGHT)]
                    for r in range(glyph_h):
                        for c in range(w):
                            if glyph[r][c]:
                                y = off + r
                                if 0 <= y < MATRIX_HEIGHT:
                                    window[y][x0 + c] = 1
                    cols = [[window[r][c] for r in range(MATRIX_HEIGHT)] for c in range(MATRIX_WIDTH)]
                    frames.append(Frame(grid=Grid(init_grid=cols)))
                # blank-gap frames between letters
                for _ in range(self.config.spacing):
                    blank = [[0] * MATRIX_WIDTH for _ in range(MATRIX_HEIGHT)]
                    cols = [[blank[r][c] for r in range(MATRIX_HEIGHT)] for c in range(MATRIX_WIDTH)]
                    frames.append(Frame(grid=Grid(init_grid=cols)))

        anim = Animation(frame_data=frames)
        anim.set_all_frame_durations(self.config.frame_duration)
        return anim
