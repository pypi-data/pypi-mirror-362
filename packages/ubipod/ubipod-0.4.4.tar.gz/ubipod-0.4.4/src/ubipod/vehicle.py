import enum
from dataclasses import dataclass, field

from .common import Light
from .object import Decor, Object, Prism
from .pbdf import PbdfReader, PbdfRelease, PbdfWriter
from .texture import TextureProject
from .typing import vec2, vec2_new, vec3, vec3_new


@dataclass
class AutoPart:
    shock_damper: float = 0.0
    mass: float = 0.0
    position: vec3 = field(default_factory=vec3_new)
    radius: float = 0.0
    friction: float = 0.0
    grip: vec3 = field(default_factory=vec3_new)
    stiffness: float = 0.0
    viscosity: float = 0.0
    z_empty: float = 0.0
    z_max: float = 0.0
    z_min: float = 0.0

    def read(self, read: PbdfReader) -> None:
        read.bytes(60)
        self.shock_damper = read.f()
        self.mass = read.f()
        read.bytes(4)
        self.position = read.vec3()
        self.radius = read.f()
        read.bytes(56)
        self.friction = read.f()
        self.grip = read.vec3()
        read.bytes(12)
        self.stiffness = read.f()
        self.viscosity = read.f()
        self.z_empty = read.f()
        self.z_max = read.f()
        self.z_min = read.f()
        read.bytes(24)

    def write(self, write: PbdfWriter) -> None:
        write.bytes(bytearray(60))
        write.f(self.shock_damper)
        write.f(self.mass)
        write.bytes(bytearray(4))
        write.vec3(self.position)
        write.f(self.radius)
        write.bytes(bytearray(56))
        write.f(self.friction)
        write.vec3(self.grip)
        write.bytes(bytearray(12))
        write.f(self.stiffness)
        write.f(self.viscosity)
        write.f(self.z_empty)
        write.f(self.z_max)
        write.f(self.z_min)
        write.bytes(bytearray(24))


class TransmissionType(enum.IntEnum):
    FOUR_WHEEL = 1
    TRACTION = 2
    PROPULSION = 3


@dataclass
class Motor:
    speed_factors_used: int = 0
    speed_factors: list[float] = field(default_factory=lambda: [0.0] * 9)
    steer_max: float = 0.0
    steer_speed: float = 0.0
    steer_recall: float = 0.0
    unknown494: float = 0.0
    inertia_moments: vec3 = field(default_factory=vec3_new)
    gear_up_speed: float = 0.0
    gear_down_speed: float = 0.0
    chassis_mass: float = 0.0
    gravity_factor: float = 0.0
    fin_factor: vec2 = field(default_factory=vec2_new)
    brake_distribution: float = 0.0
    zoom_factor: float = 0.0
    viscous_friction: float = 0.0
    brake_slope_curve: float = 0.0
    brake_max: float = 0.0
    transmission_type: TransmissionType = TransmissionType.FOUR_WHEEL

    def read(self, read: PbdfReader) -> None:
        read.bytes(19)
        self.speed_factors_used = read.i8()
        self.speed_factors = [read.f() for _ in range(9)]
        read.bytes(20)
        self.steer_max = read.f()
        self.steer_speed = read.f()
        self.steer_recall = read.f()
        read.bytes(8 if read.format.release == PbdfRelease.OEM else 4)
        self.unknown494 = read.f()
        read.bytes(112)
        self.inertia_moments = read.vec3()
        read.bytes(4)
        self.gear_up_speed = read.f()
        self.gear_down_speed = read.f()
        self.chassis_mass = read.f()
        read.bytes(4)
        self.gravity_factor = read.f()
        read.bytes(4)
        self.fin_factor = read.vec2()
        self.brake_distribution = read.f()
        self.zoom_factor = read.f()
        self.viscous_friction = read.f()
        self.brake_slope_curve = read.f()
        self.brake_max = read.f()
        self.transmission_type = TransmissionType(read.i32())
        read.bytes(8)

    def write(self, write: PbdfWriter) -> None:
        write.bytes(bytearray(19))
        write.i8(self.speed_factors_used)
        [write.f(x) for x in self.speed_factors]
        write.bytes(bytearray(20))
        write.f(self.steer_max)
        write.f(self.steer_speed)
        write.f(self.steer_recall)
        write.bytes(bytearray(8 if write.format.release == PbdfRelease.OEM else 4))
        write.f(self.unknown494)
        write.bytes(bytearray(112))
        write.vec3(self.inertia_moments)
        write.bytes(bytearray(4))
        write.f(self.gear_up_speed)
        write.f(self.gear_down_speed)
        write.f(self.chassis_mass)
        write.bytes(bytearray(4))
        write.f(self.gravity_factor)
        write.bytes(bytearray(4))
        write.vec2(self.fin_factor)
        write.f(self.brake_distribution)
        write.f(self.zoom_factor)
        write.f(self.viscous_friction)
        write.f(self.brake_slope_curve)
        write.f(self.brake_max)
        write.i32(self.transmission_type.value)
        write.bytes(bytearray(8))


@dataclass
class Auto:
    wheel_fr: AutoPart = field(default_factory=AutoPart)
    wheel_rr: AutoPart = field(default_factory=AutoPart)
    wheel_fl: AutoPart = field(default_factory=AutoPart)
    wheel_rl: AutoPart = field(default_factory=AutoPart)
    chassis: AutoPart = field(default_factory=AutoPart)
    motor: Motor = field(default_factory=Motor)
    motor_curves: list[int] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.wheel_fr = read.any(AutoPart)
        self.wheel_rr = read.any(AutoPart)
        self.wheel_fl = read.any(AutoPart)
        self.wheel_rl = read.any(AutoPart)
        self.chassis = read.any(AutoPart)
        self.motor = read.any(Motor)
        self.motor_curves = [read.i32() for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.any(self.wheel_fr)
        write.any(self.wheel_rr)
        write.any(self.wheel_fl)
        write.any(self.wheel_rl)
        write.any(self.chassis)
        write.any(self.motor)
        write.i32(len(self.motor_curves))
        [write.i32(x) for x in self.motor_curves]


@dataclass
class GraphicsObject:
    object: Object = field(default_factory=Object)
    prism: Prism = field(default_factory=Prism)

    def read(self, read: PbdfReader, has_face_material: bool) -> None:
        self.object = read.any(Object, has_face_material, False, True)
        self.prism = read.any(Prism)

    def write(self, write: PbdfWriter, has_face_material: bool) -> None:
        write.any(self.object, has_face_material, False, True)
        write.any(self.prism)


@dataclass
class Graphics:
    texture_project_name: str = ""
    texture_project: TextureProject = field(default_factory=TextureProject)
    has_face_material: bool = False
    chassis_rr0: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_rl0: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_sr0: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_sl0: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_fr0: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_fl0: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_rr1: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_rl1: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_sr1: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_sl1: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_fr1: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_fl1: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_rr2: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_rl2: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_sr2: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_sl2: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_fr2: GraphicsObject = field(default_factory=GraphicsObject)
    chassis_fl2: GraphicsObject = field(default_factory=GraphicsObject)
    wheel_fr: GraphicsObject = field(default_factory=GraphicsObject)
    wheel_rr: GraphicsObject = field(default_factory=GraphicsObject)
    wheel_fl: GraphicsObject = field(default_factory=GraphicsObject)
    wheel_rl: GraphicsObject = field(default_factory=GraphicsObject)
    shadow_r0: Object = field(default_factory=Object)
    shadow_f0: Object = field(default_factory=Object)
    shadow_r2: Object = field(default_factory=Object)
    shadow_f2: Object = field(default_factory=Object)
    shadow_oem: Object = field(default_factory=Object)

    def read(self, read: PbdfReader) -> None:
        self.texture_project_name = read.str()
        self.texture_project = read.any(TextureProject, read.format.tex_size_small)
        self.has_face_material = read.b32()
        self.chassis_rr0 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_rl0 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_sr0 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_sl0 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_fr0 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_fl0 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_rr1 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_rl1 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_sr1 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_sl1 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_fr1 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_fl1 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_rr2 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_rl2 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_sr2 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_sl2 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_fr2 = read.any(GraphicsObject, self.has_face_material)
        self.chassis_fl2 = read.any(GraphicsObject, self.has_face_material)
        self.wheel_fr = read.any(GraphicsObject, self.has_face_material)
        self.wheel_rr = read.any(GraphicsObject, self.has_face_material)
        self.wheel_fl = read.any(GraphicsObject, self.has_face_material)
        self.wheel_rl = read.any(GraphicsObject, self.has_face_material)
        if read.format.release == PbdfRelease.OEM:
            self.shadow_oem = read.any(Object, self.has_face_material, False, True)
        else:
            self.shadow_r0 = read.any(Object, self.has_face_material, False, True)
            self.shadow_f0 = read.any(Object, self.has_face_material, False, True)
            self.shadow_r2 = read.any(Object, self.has_face_material, False, True)
            self.shadow_f2 = read.any(Object, self.has_face_material, False, True)

    def write(self, write: PbdfWriter) -> None:
        write.str(self.texture_project_name)
        write.any(self.texture_project)
        write.i32(self.has_face_material)
        write.any(self.chassis_rr0, self.has_face_material)
        write.any(self.chassis_rl0, self.has_face_material)
        write.any(self.chassis_sr0, self.has_face_material)
        write.any(self.chassis_sl0, self.has_face_material)
        write.any(self.chassis_fr0, self.has_face_material)
        write.any(self.chassis_fl0, self.has_face_material)
        write.any(self.chassis_rr1, self.has_face_material)
        write.any(self.chassis_rl1, self.has_face_material)
        write.any(self.chassis_sr1, self.has_face_material)
        write.any(self.chassis_sl1, self.has_face_material)
        write.any(self.chassis_fr1, self.has_face_material)
        write.any(self.chassis_fl1, self.has_face_material)
        write.any(self.chassis_rr2, self.has_face_material)
        write.any(self.chassis_rl2, self.has_face_material)
        write.any(self.chassis_sr2, self.has_face_material)
        write.any(self.chassis_sl2, self.has_face_material)
        write.any(self.chassis_fr2, self.has_face_material)
        write.any(self.chassis_fl2, self.has_face_material)
        write.any(self.wheel_fr, self.has_face_material)
        write.any(self.wheel_rr, self.has_face_material)
        write.any(self.wheel_fl, self.has_face_material)
        write.any(self.wheel_rl, self.has_face_material)
        if write.format.release == PbdfRelease.OEM:
            write.any(self.shadow_oem, self.has_face_material, False, True)
        else:
            write.any(self.shadow_r0, self.has_face_material, False, True)
            write.any(self.shadow_f0, self.has_face_material, False, True)
            write.any(self.shadow_r2, self.has_face_material, False, True)
            write.any(self.shadow_f2, self.has_face_material, False, True)


@dataclass
class Sounds:
    engine: int = 0
    gear_next: int = 0
    gear_prev: int = 0
    brake: int = 0
    brake_stop: int = 0
    crash_soft: int = 0
    unknown: int = 0
    shock: int = 0
    accel: int = 0
    accel_stop: int = 0
    decel: int = 0
    decel_stop: int = 0
    crash: int = 0
    skid_roof: int = 0
    skid_roof_stop: int = 0

    def read(self, read: PbdfReader) -> None:
        read.bytes(4)
        self.engine = read.i16()
        self.gear_next = read.i16()
        self.gear_prev = read.i16()
        self.brake = read.i16()
        self.brake_stop = read.i16()
        self.crash_soft = read.i16()
        self.unknown = read.i16()
        self.shock = read.i16()
        self.accel = read.i16()
        self.accel_stop = read.i16()
        self.decel = read.i16()
        self.decel_stop = read.i16()
        self.crash = read.i16()
        self.skid_roof = read.i16()
        self.skid_roof_stop = read.i16()
        read.bytes(2)

    def write(self, write: PbdfWriter) -> None:
        write.bytes(bytearray(4))
        write.i16(self.engine)
        write.i16(self.gear_next)
        write.i16(self.gear_prev)
        write.i16(self.brake)
        write.i16(self.brake_stop)
        write.i16(self.crash_soft)
        write.i16(self.unknown)
        write.i16(self.shock)
        write.i16(self.accel)
        write.i16(self.accel_stop)
        write.i16(self.decel)
        write.i16(self.decel_stop)
        write.i16(self.crash)
        write.i16(self.skid_roof)
        write.i16(self.skid_roof_stop)
        write.bytes(bytearray(2))


@dataclass
class Vehicle:
    name: str = ""
    auto: Auto = field(default_factory=Auto)
    graphics: Graphics = field(default_factory=Graphics)
    lod1_file_name: str = ""
    lod1_file: Decor = field(default_factory=Decor)
    lod2_file_name: str = ""
    lod2_file: Decor = field(default_factory=Decor)
    sounds: Sounds = field(default_factory=Sounds)
    default_accel: int = 0
    default_brakes: int = 0
    default_grip: int = 0
    default_handling: int = 0
    default_speed: int = 0
    light: Light = field(default_factory=Light)

    def read(self, read: PbdfReader) -> None:
        read.offset(0)
        if read.format.version < 6:
            self.name = read.str()
        if read.format.version < 8:
            self.auto = read.any(Auto)
        self.graphics = read.any(Graphics)
        self.lod1_file_name = read.str()
        self.lod1_file = read.any(Decor)
        self.lod2_file_name = read.str()
        self.lod2_file = read.any(Decor)
        if read.format.version >= 8:
            self.auto = read.any(Auto)
        self.sounds = read.any(Sounds)
        if read.format.version < 8:
            self.default_accel = read.i32()
            self.default_brakes = read.i32()
            self.default_grip = read.i32()
            self.default_handling = read.i32()
            self.default_speed = read.i32()
        else:
            self.default_speed = read.i32()
            self.default_handling = read.i32()
            self.default_grip = read.i32()
            self.default_brakes = read.i32()
            self.default_accel = read.i32()
            self.default_brakes = read.i32()
            self.default_handling = read.i32()
            self.default_speed = read.i32()
            self.default_grip = read.i32()
            self.default_accel = read.i32()
        self.light = read.any(Light)
        if read.format.version > 5:
            self.name = read.str()

    def write(self, write: PbdfWriter) -> None:
        write.offset()
        if write.format.version < 6:
            write.str(self.name)
        if write.format.version < 8:
            write.any(self.auto)
        write.any(self.graphics)
        write.str(self.lod1_file_name)
        write.any(self.lod1_file)
        write.str(self.lod2_file_name)
        write.any(self.lod2_file)
        if write.format.version >= 8:
            write.any(self.auto)
        write.any(self.sounds)
        if write.format.version < 8:
            write.i32(self.default_accel)
            write.i32(self.default_brakes)
            write.i32(self.default_grip)
            write.i32(self.default_handling)
            write.i32(self.default_speed)
        else:
            write.i32(self.default_speed)
            write.i32(self.default_handling)
            write.i32(self.default_grip)
            write.i32(self.default_brakes)
            write.i32(self.default_accel)
            write.i32(self.default_brakes)
            write.i32(self.default_handling)
            write.i32(self.default_speed)
            write.i32(self.default_grip)
            write.i32(self.default_accel)
        write.any(self.light)
        if write.format.version > 5:
            write.str(self.name)
