from dataclasses import dataclass

import colour as colour_science


@dataclass
class Colour:
    rgb: tuple[int, int, int]
    name: str | None = None

    _lab: tuple[float, float, float] | None = None

    @property
    def hex(self) -> str:
        r, g, b = self.rgb
        return f"#{r:02x}{g:02x}{b:02x}"

    @property
    def lab(self) -> tuple[float, float, float]:
        if self._lab is None:
            rgb_normalised = [x / 255 for x in self.rgb]

            xyz = colour_science.sRGB_to_XYZ(rgb_normalised)
            self._lab = tuple(
                colour_science.XYZ_to_Lab(xyz)
            )

        return self._lab

    @classmethod
    def from_hex(cls, hex_code: str, name: str | None = None):
        rgb = (
            int(hex_code[1:3], 16),
            int(hex_code[3:5], 16),
            int(hex_code[5:7], 16),
        )

        return cls(
            rgb=rgb,
            name=name
        )
