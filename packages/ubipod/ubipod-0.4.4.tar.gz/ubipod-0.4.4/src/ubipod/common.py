import enum
from dataclasses import dataclass, field

from .pbdf import PbdfReader, PbdfWriter
from .typing import mat33, mat33_new, vec3, vec3_new


class LightDiffusion(enum.IntEnum):
    NONE = 0
    LINEAR = 1
    SQUARE = 2


class LightType(enum.IntEnum):
    CYLINDER = 0
    SPHERE = 1
    CONE = 2


@dataclass
class Light:
    type: LightType = LightType.CYLINDER
    position: vec3 = field(default_factory=vec3_new)
    rotation: mat33 = field(default_factory=mat33_new)
    radius: float = 0.0
    intensity: float = 0.0
    diffusion_type: LightDiffusion = LightDiffusion.NONE
    angle: float = 0.0

    def read(self, read: PbdfReader) -> None:
        self.type = LightType(read.i32())
        self.position = read.vec3()
        self.rotation = read.mat33()
        self.radius = read.f()
        self.intensity = read.f()
        self.diffusion_type = LightDiffusion(read.i32())
        self.angle = read.f()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.type)
        write.vec3(self.position)
        write.mat33(self.rotation)
        write.f(self.radius)
        write.f(self.intensity)
        write.i32(self.diffusion_type)
        write.f(self.angle)
