import enum
import math
from dataclasses import dataclass, field

from .pbdf import PbdfReader, PbdfWriter
from .typing import vec2i32, vec3, vec3_new


@dataclass
class Bbox:
    min: vec3 = field(default_factory=vec3_new)
    max: vec3 = field(default_factory=vec3_new)

    def read(self, read: PbdfReader) -> None:
        self.min = read.vec3()
        self.max = read.vec3()

    def write(self, write: PbdfWriter) -> None:
        write.vec3(self.min)
        write.vec3(self.max)


@dataclass
class Contact:
    radius: float = 0.0
    center: vec3 = field(default_factory=vec3_new)
    mass: int = 0

    def read(self, read: PbdfReader) -> None:
        self.radius = read.f()
        self.center = read.vec3()
        read.bytes(12)
        self.mass = read.i32()
        read.bytes(32)

    def write(self, write: PbdfWriter) -> None:
        write.f(self.radius)
        write.vec3(self.center)
        write.bytes(bytearray(12))
        write.i32(self.mass)
        write.bytes(bytearray(32))


@dataclass
class Prism:
    extent: vec3 = field(default_factory=vec3_new)
    length: float = 0.0  # hypotenuse of 2d extent, e.g. sqrt(extent[0] * extent[0] + extent[1] * extent[1])
    center: vec3 = field(default_factory=vec3_new)

    def read(self, read: PbdfReader) -> None:
        self.extent = read.vec3()
        self.length = read.f()
        self.center = read.vec3()

    def write(self, write: PbdfWriter) -> None:
        write.vec3(self.extent)
        write.f(self.length)
        write.vec3(self.center)

    def calc_radius(self) -> float:
        v = self.extent
        return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])


class Effect(enum.IntEnum):
    FLAT = 1
    GOURAUD = 2
    TEXTURE = 3
    TEXGOU = 4

    def is_color(self) -> bool:
        return self in [Effect.FLAT, Effect.GOURAUD]

    def is_gouraud(self) -> bool:
        return self in [Effect.GOURAUD, Effect.TEXGOU]


@dataclass
class EffectData:
    color: int = 0
    texture_index: int = 0
    texture_uvs: list[vec2i32] = field(default_factory=lambda: [(0, 0)] * 4)

    def read(self, read: PbdfReader, effect: Effect, index_count: int) -> None:
        if effect in (Effect.FLAT, Effect.GOURAUD):
            self.color = read.i32()
        else:
            self.texture_index = read.i32()
        self.texture_uvs = [read.vec2i32() for _ in range(4)]
        read.i32()
        if index_count == 4:
            read.vec3()

    def write(self, write: PbdfWriter, effect: Effect, index_count: int) -> None:
        if effect in (Effect.FLAT, Effect.GOURAUD):
            write.i32(self.color)
        else:
            write.i32(self.texture_index)
        [write.vec2i32(x) for x in self.texture_uvs]
        write.i32(0)
        if index_count == 4:
            write.vec3((0.0,) * 3)


@dataclass
class FaceProperty:
    visible: bool = False
    road: bool = False
    wall: bool = False
    slip: int = 0
    backface: bool = False
    trans: bool = False
    dural: bool = False
    lod: int = 0


@dataclass
class Face:
    material_name: str = ""
    index_count: int = 0
    indices: list[int] = field(default_factory=lambda: [0] * 4)
    normal: vec3 = field(default_factory=vec3_new)
    effect: Effect = Effect.FLAT
    effect_data: EffectData = field(default_factory=EffectData)
    mirror: int = 0
    property: int = 0

    def read(self, read: PbdfReader, has_material: bool, has_mirror: bool, has_property: bool) -> None:
        if has_material:
            self.material_name = read.str()
        if read.key == 0x5CA8 or read.key == 0xD13F:
            self.indices[3] = read.i32()
            self.indices[0] = read.i32()
            self.index_count = read.i32()
            self.indices[2] = read.i32()
            self.indices[1] = read.i32()
        else:
            self.index_count = read.i32()
            self.indices = [read.i32() for _ in range(4)]
        self.normal = read.vec3()
        self.effect = Effect[read.str()]
        self.effect_data = read.any(EffectData, self.effect, self.index_count)
        if has_mirror and any(self.normal):
            self.mirror = read.i32()
        if has_property:
            self.property = read.i32()

    def write(self, write: PbdfWriter, has_material: bool, has_mirror: bool, has_property: bool) -> None:
        if has_material:
            write.str(self.material_name)
        if write.key == 0x5CA8 or write.key == 0xD13F:
            write.i32(self.indices[3])
            write.i32(self.indices[0])
            write.i32(self.index_count)
            write.i32(self.indices[2])
            write.i32(self.indices[1])
        else:
            write.i32(self.index_count)
            [write.i32(x) for x in self.indices]
        write.vec3(self.normal)
        write.str(self.effect.name)
        write.any(self.effect_data, self.effect, self.index_count)
        if has_mirror and any(self.normal):
            write.i32(self.mirror)
        if has_property:
            write.i32(self.property)

    def decode_property(self) -> FaceProperty:
        p = self.property
        visible = bool(p & 0b1)
        road = bool(p & 0b1000)
        wall = bool(p & 0b100000)
        lod = p >> 6 & 0b11
        trans = bool(p & 0b100000000)
        backface = bool(p & 0b10000000000)
        dural = bool(p & 0b10000000000000)
        slip = p >> 16 & 0xFF
        return FaceProperty(visible, road, wall, slip, backface, trans, dural, lod)

    def encode_property(self, property: FaceProperty) -> None:
        p = 0
        if property.visible:
            p |= 0b1
        if property.road:
            p |= 0b1000
        if property.wall:
            p |= 0b100000
        if property.lod:
            p |= (property.lod & 0b11) << 6
        if property.trans:
            p |= 0b100000000
        if property.backface:
            p |= 0b10000000000
        if property.dural:
            p |= 0b10000000000000
        if property.slip:
            p |= (property.slip & 0xFF) << 16
        self.property = p


@dataclass
class Object:
    positions: list[vec3] = field(default_factory=list)
    faces: list[Face] = field(default_factory=list)
    normals: list[vec3] = field(default_factory=list)
    radius: float = 0.0  # length of bounding box (prism) extent

    def read(self, read: PbdfReader, has_face_material: bool, has_face_mirror: bool, has_face_property: bool) -> None:
        vertex_count = read.i32()
        self.positions = [read.vec3() for _ in range(vertex_count)]
        face_count = read.i32()
        read.i32()  # tri_count
        read.i32()  # quad_count
        self.faces = [read.any(Face, has_face_material, has_face_mirror, has_face_property) for _ in range(face_count)]
        self.normals = [read.vec3() for _ in range(vertex_count)]
        self.radius = read.f()

    def write(self, write: PbdfWriter, has_face_material: bool, has_face_mirror: bool, has_face_property: bool) -> None:
        write.i32(len(self.positions))
        [write.vec3(x) for x in self.positions]
        write.i32(len(self.faces))
        write.i32(sum(1 for x in self.faces if x.index_count == 3))  # tri_count
        write.i32(sum(1 for x in self.faces if x.index_count == 4))  # quad_count
        [write.any(x, has_face_material, has_face_mirror, has_face_property) for x in self.faces]
        [write.vec3(x) for x in self.normals]
        write.f(self.radius)

    def calc_bbox(self) -> Bbox:
        if len(self.positions):
            min_pos = [math.inf] * 3
            max_pos = [-math.inf] * 3
            for pos in self.positions:
                for i in range(3):
                    min_pos[i] = min(min_pos[i], pos[i])
                    max_pos[i] = max(max_pos[i], pos[i])
        else:
            min_pos = [0.0] * 3
            max_pos = [0.0] * 3
        return Bbox(tuple(min_pos), tuple(max_pos))

    def calc_prism(self) -> Prism:
        bbox = self.calc_bbox()
        prism = Prism()
        prism.center = tuple((bbox.max[i] + bbox.min[i]) / 2 for i in range(3))
        prism.extent = tuple((bbox.max[i] - bbox.min[i]) / 2 for i in range(3))
        width = abs(prism.extent[0])
        height = abs(prism.extent[1])
        prism.length = math.sqrt(width * width + height * height)
        return prism


@dataclass
class Decor:
    has_face_material: bool = False
    object: Object = field(default_factory=Object)
    prism: Prism = field(default_factory=Prism)
    total_mass: int = 0
    inertia_mat_diag: vec3 = field(default_factory=vec3_new)
    resistance: int = 0
    friction: int = 0
    contacts: list[Contact] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.has_face_material = read.b32()
        self.object = read.any(Object, self.has_face_material, False, True)
        self.prism = read.any(Prism)
        self.total_mass = read.i32()
        self.inertia_mat_diag = read.vec3()
        self.resistance = read.i32()
        self.friction = read.i32()
        self.contacts = [read.any(Contact) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.has_face_material)
        write.any(self.object, self.has_face_material, False, True)
        write.any(self.prism)
        write.i32(self.total_mass)
        write.vec3(self.inertia_mat_diag)
        write.i32(self.resistance)
        write.i32(self.friction)
        write.i32(len(self.contacts))
        [write.any(x) for x in self.contacts]
