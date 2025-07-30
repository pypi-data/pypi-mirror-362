import enum
from dataclasses import dataclass, field

from .binary import BinaryWritable
from .common import Light
from .object import Bbox, Decor, Object
from .pbdf import PbdfReader, PbdfRelease, PbdfWriter
from .texture import TextureProject
from .typing import mat33, mat33_new, vec2i32, vec3, vec3_new


@dataclass
class EventType:
    name: str = ""
    param_size: int = 0
    param_buffer: bytes = field(default_factory=lambda: bytes(0))

    def read(self, read: PbdfReader, index: int) -> None:
        if read.format.release == PbdfRelease.OEM:
            self.param_size = self.calc_param_size_oem(index)
        else:
            self.name = read.str()
            self.param_size = read.i32()
        param_count = read.i32()
        self.param_buffer = read.bytes(self.param_size * param_count)

    def write(self, write: PbdfWriter) -> None:
        if write.format.release != PbdfRelease.OEM:
            write.str(self.name)
            write.i32(self.param_size)
        write.i32(len(self.param_buffer) // self.param_size if self.param_size else 0)
        write.bytes(self.param_buffer)

    def calc_param_size_oem(self, index: int) -> int:
        match index:
            case 1 | 13 | 19 | 30 | 31 | 32 | 33 | 34 | 37: return 4
            case 6 | 15 | 20: return 44
            case 12: return 12
            case 14 | 21 | 29: return 8
            case _: return 0


@dataclass
class EventTypeFile:
    types: list[EventType] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        if read.format.release == PbdfRelease.OEM:
            type_count = 43
        else:
            type_count = read.i32()
            read.i32()  # param size total
        self.types = [read.any(EventType, i) for i in range(type_count)]

    def write(self, write: PbdfWriter) -> None:
        if write.format.release != PbdfRelease.OEM:
            write.i32(len(self.types))
            write.i32(self.calc_param_size_total())
        [write.any(x) for x in self.types]

    def calc_param_size_total(self) -> int:
        return sum(len(t.param_buffer) for t in self.types)


@dataclass
class Event:
    type: int = 0
    param: int = 0
    link: int = 0

    def read(self, read: PbdfReader) -> None:
        self.type = read.i32()
        self.param = read.i32()
        self.link = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.type)
        write.i32(self.param)
        write.i32(self.link)


@dataclass
class EventList:
    events: list[Event] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.events = [read.any(Event) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.events))
        [write.any(x) for x in self.events]


@dataclass
class EventMacroFile:
    event_list: EventList = field(default_factory=EventList)
    macro_params: list[int] = field(default_factory=list)
    init_macro_params: list[int] = field(default_factory=list)
    active_params: list[int] = field(default_factory=list)
    inactive_params: list[int] = field(default_factory=list)
    replace_params: list[int] = field(default_factory=list)
    exchange_params: list[int] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.event_list = read.any(EventList)
        self.macro_params = [read.i32() for _ in range(read.i32())]
        self.init_macro_params = [read.i32() for _ in range(read.i32())]
        self.active_params = [read.i32() for _ in range(read.i32())]
        self.inactive_params = [read.i32() for _ in range(read.i32())]
        self.replace_params = [read.i32() for _ in range(read.i32())]
        self.exchange_params = [read.i32() for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.any(self.event_list)
        write.i32(len(self.macro_params))
        [write.i32(x) for x in self.macro_params]
        write.i32(len(self.init_macro_params))
        [write.i32(x) for x in self.init_macro_params]
        write.i32(len(self.active_params))
        [write.i32(x) for x in self.active_params]
        write.i32(len(self.inactive_params))
        [write.i32(x) for x in self.inactive_params]
        write.i32(len(self.replace_params))
        [write.i32(x) for x in self.replace_params]
        write.i32(len(self.exchange_params))
        [write.i32(x) for x in self.exchange_params]


@dataclass
class VoodooFile:
    face_lod: list[int] = field(default_factory=lambda: [0] * 16)

    def read(self, read: PbdfReader) -> None:
        self.face_lod = [read.i32() for _ in range(16)]

    def write(self, write: PbdfWriter) -> None:
        [write.i32(x) for x in self.face_lod]


@dataclass
class Sector:
    object: Object = field(default_factory=Object)
    vertex_brightness: list[int] = field(default_factory=list)
    bbox: Bbox = field(default_factory=Bbox)

    def read(self, read: PbdfReader, has_face_material: bool) -> None:
        self.object = read.any(Object, has_face_material, read.format.voodoo and read.format.version != 9, read.format.version != 7)
        self.vertex_brightness = [read.u8() for _ in range(len(self.object.positions))]
        self.bbox = read.any(Bbox)

    def write(self, write: PbdfWriter, has_face_material: bool) -> None:
        write.any(self.object, has_face_material, write.format.voodoo and write.format.version != 9, write.format.version != 7)
        [write.u8(x) for x in self.vertex_brightness]
        write.any(self.bbox)


@dataclass
class RouteFile:
    texture_project_name: str = ""
    texture_project: TextureProject = field(default_factory=TextureProject)
    has_sector_face_material: bool = False
    sectors: list[Sector] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.texture_project_name = read.str()
        self.texture_project = read.any(TextureProject, 256)
        self.has_sector_face_material = read.b32()
        self.sectors = [read.any(Sector, self.has_sector_face_material) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.str(self.texture_project_name)
        write.any(self.texture_project)
        write.b32(self.has_sector_face_material)
        write.i32(len(self.sectors))
        [write.any(x, self.has_sector_face_material) for x in self.sectors]


@dataclass
class ZoneSector:
    visible_sectors: list[int] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        visible_sector_count = read.i32()
        if visible_sector_count > 0:
            self.visible_sectors = [read.i32() for _ in range(visible_sector_count)]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.visible_sectors) if self.visible_sectors else -1)
        [write.i32(x) for x in self.visible_sectors]


@dataclass
class ZoneFile:
    sectors: list[ZoneSector] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.sectors = [read.any(ZoneSector) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.sectors))
        [write.any(x) for x in self.sectors]


@dataclass
class DecorationEvent:
    event_index: int = 0
    unknown: int = 0

    def read(self, read: PbdfReader) -> None:
        self.event_index = read.i32()
        self.unknown = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.event_index)
        write.i32(self.unknown)


@dataclass
class Decoration:
    descriptor_index: int = 0
    events: list[DecorationEvent] = field(default_factory=list)
    position: vec3 = field(default_factory=vec3_new)
    rotation: mat33 = field(default_factory=mat33_new)

    def read(self, read: PbdfReader) -> None:
        self.descriptor_index = read.i32()
        self.events = [read.any(DecorationEvent) for _ in range(read.i32())]
        self.position = read.vec3()
        self.rotation = read.mat33()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.descriptor_index)
        write.i32(len(self.events))
        [write.any(x) for x in self.events]
        write.vec3(self.position)
        write.mat33(self.rotation)


@dataclass
class DecorationList:
    decorations: list[Decoration] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.decorations = [read.any(Decoration) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.decorations))
        [write.any(x) for x in self.decorations]


@dataclass
class DecorDescriptor:
    file_name: str = ""
    texture_project_name: str = ""
    texture_project: TextureProject = field(default_factory=TextureProject)
    file: Decor = field(default_factory=Decor)

    def read(self, read: PbdfReader) -> None:
        self.file_name = read.str()
        self.texture_project_name = read.str()
        self.texture_project = read.any(TextureProject, read.format.tex_size_small)
        self.file = read.any(Decor)

    def write(self, write: PbdfWriter) -> None:
        write.str(self.file_name)
        write.str(self.texture_project_name)
        write.any(self.texture_project)
        write.any(self.file)


@dataclass
class EnvironmentFile:
    event_list: EventList = field(default_factory=EventList)
    descriptors: list[DecorDescriptor] = field(default_factory=list)
    global_list: DecorationList = field(default_factory=DecorationList)
    sector_lists: list[DecorationList] = field(default_factory=list)

    def read(self, read: PbdfReader, sector_count: int) -> None:
        self.event_list = read.any(EventList)
        self.descriptors = [read.any(DecorDescriptor) for _ in range(read.i32())]
        self.global_list = read.any(DecorationList)
        self.sector_lists = [read.any(DecorationList) for _ in range(sector_count)]

    def write(self, write: PbdfWriter, sector_count: int) -> None:
        write.any(self.event_list)
        write.i32(len(self.descriptors))
        [write.any(x) for x in self.descriptors]
        write.any(self.global_list)
        [write.any(x) for x in self.sector_lists]


@dataclass
class LightList:
    lights: list[Light] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.lights = [read.any(Light) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.lights))
        [write.any(x) for x in self.lights]


@dataclass
class LightFile:
    object_ambient: int = 0
    direction: vec3 = field(default_factory=vec3_new)
    circuit_light: int = 0
    circuit_dark: int = 0
    object_tunnel: int = 0
    object_shadow: int = 0
    limit_r: list[int] = field(default_factory=lambda: [0] * 4)
    limit_g: list[int] = field(default_factory=lambda: [0] * 4)
    limit_b: list[int] = field(default_factory=lambda: [0] * 4)
    global_list: LightList = field(default_factory=LightList)
    sector_lists: list[LightList] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        sector_count = read.i32()
        self.object_ambient = read.i32()
        self.direction = read.vec3()
        self.circuit_light = read.i32()
        self.circuit_dark = read.i32()
        self.object_tunnel = read.i32()
        self.object_shadow = read.i32()
        if read.format.release != PbdfRelease.OEM:
            self.limit_r = [read.u8() for _ in range(4)]
            self.limit_g = [read.u8() for _ in range(4)]
            self.limit_b = [read.u8() for _ in range(4)]
        self.global_list = read.any(LightList)
        self.sector_lists = [read.any(LightList) for _ in range(sector_count)]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.sector_lists))
        write.i32(self.object_ambient)
        write.vec3(self.direction)
        write.i32(self.circuit_light)
        write.i32(self.circuit_dark)
        write.i32(self.object_tunnel)
        write.i32(self.object_shadow)
        if write.format.release != PbdfRelease.OEM:
            [write.u8(x) for x in self.limit_r]
            [write.u8(x) for x in self.limit_g]
            [write.u8(x) for x in self.limit_b]
        write.any(self.global_list)
        [write.any(x) for x in self.sector_lists]


@dataclass
class Anim3DKey:
    has_transform: bool = False
    rotation: mat33 = field(default_factory=mat33_new)
    position: vec3 = field(default_factory=vec3_new)

    def read(self, read: PbdfReader) -> None:
        self.has_transform = read.b32()
        if self.has_transform:
            self.rotation = read.mat33()
            self.position = read.vec3()

    def write(self, write: PbdfWriter) -> None:
        write.b32(self.has_transform)
        if self.has_transform:
            write.mat33(self.rotation)
            write.vec3(self.position)


@dataclass
class Anim3D:
    start_frame: int = 0
    has_face_material: bool = False
    texture_page: str = ""
    objects: list[Object] = field(default_factory=list)
    frame_object_keys: list[list[Anim3DKey]] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.start_frame = read.i32()
        frame_count = read.i32()
        self.has_face_material = read.b32()
        object_count = read.i32()
        self.texture_page = read.str()
        self.objects = [read.any(Object, self.has_face_material, False, True) for _ in range(object_count)]
        self.frame_object_keys = [[read.any(Anim3DKey) for _ in range(object_count)] for _ in range(frame_count)]

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.start_frame)
        write.i32(len(self.frame_object_keys))
        write.b32(self.has_face_material)
        write.i32(len(self.objects))
        write.str(self.texture_page)
        [write.any(x, self.has_face_material, False, True) for x in self.objects]
        [[write.any(ok) for ok in f] for f in self.frame_object_keys]


@dataclass
class Anim2DSprite:
    page_index: int = 0
    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0

    def read(self, read: PbdfReader) -> None:
        self.page_index = read.i32()
        self.left = read.i32()
        self.top = read.i32()
        self.right = read.i32()
        self.bottom = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.page_index)
        write.i32(self.left)
        write.i32(self.top)
        write.i32(self.right)
        write.i32(self.bottom)


@dataclass
class Anim2DSpriteFrame:
    sprite_index: int = 0
    width: int = 0
    height: int = 0
    translation_x: int = 0
    translation_y: int = 0

    def read(self, read: PbdfReader) -> None:
        self.sprite_index = read.i32()
        self.width = read.i32()
        self.height = read.i32()
        self.translation_x = read.i32()
        self.translation_y = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.sprite_index)
        write.i32(self.width)
        write.i32(self.height)
        write.i32(self.translation_x)
        write.i32(self.translation_y)


@dataclass
class Anim2DFrame:
    value: vec3 = field(default_factory=vec3_new)
    sprite_frames: list[Anim2DSpriteFrame] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.value = read.vec3()
        self.sprite_frames = [read.any(Anim2DSpriteFrame) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.vec3(self.value)
        write.i32(len(self.sprite_frames))
        [write.any(x) for x in self.sprite_frames]


@dataclass
class Anim2D:
    start_frame: int = 0
    sprite_count_total: int = 0
    texture_project_name: str = ""
    texture_project: TextureProject = field(default_factory=TextureProject)
    sprites: list[Anim2DSprite] = field(default_factory=list)
    frames: list[Anim2DFrame] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.start_frame = read.i32()
        frame_count = read.i32()
        sprite_count = read.i32()
        self.sprite_count_total = read.i32()
        self.texture_project_name = read.str()
        self.texture_project = read.any(TextureProject, 256)
        self.sprites = [read.any(Anim2DSprite) for _ in range(sprite_count)]
        self.frames = [read.any(Anim2DFrame) for _ in range(frame_count)]

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.start_frame)
        write.i32(len(self.frames))
        write.i32(len(self.sprites))
        write.i32(self.sprite_count_total)
        write.str(self.texture_project_name)
        write.any(self.texture_project)
        [write.any(x) for x in self.sprites]
        [write.any(x) for x in self.frames]


@dataclass
class Anim:
    frame_count: int = 0
    anim3ds: list[Anim3D] = field(default_factory=list)
    anim2ds: list[Anim2D] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        ani2d_count = read.i32()
        ani3d_count = read.i32()
        self.frame_count = read.i32()
        self.anim3ds = [read.any(Anim3D) for _ in range(ani3d_count)]
        self.anim2ds = [read.any(Anim2D) for _ in range(ani2d_count)]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.anim2ds))
        write.i32(len(self.anim3ds))
        write.i32(self.frame_count)
        [write.any(x) for x in self.anim3ds]
        [write.any(x) for x in self.anim2ds]


@dataclass
class AnimDescriptor:
    file_name: str = ""
    wrongway0: int = 0
    wrongway1: int = 0
    file: Anim = field(default_factory=Anim)

    def read(self, read: PbdfReader) -> None:
        self.file_name = read.str()
        if self.file_name == "wrongway.ani":
            self.wrongway0 = read.i16()
            read.i16()  # gap
            self.wrongway1 = read.i16()
            read.i16()  # gap
        self.file = read.any(Anim)

    def write(self, write: PbdfWriter) -> None:
        write.str(self.file_name)
        if self.file_name == "wrongway.ani":
            write.i16(self.wrongway0)
            write.i16(0)  # gap
            write.i16(self.wrongway1)
            write.i16(0)  # gap
        write.any(self.file)


@dataclass
class AnimationEvent:
    event_index: int = 0
    frame_count: int = 0

    def read(self, read: PbdfReader) -> None:
        self.event_index = read.i32()
        self.frame_count = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.event_index)
        write.i32(self.frame_count)


@dataclass
class Animation:
    descriptor_index: int = 0
    trigger: int = 0
    frozen: int = 0
    fixed: int = 0
    speed: int = 0
    events: list[AnimationEvent] = field(default_factory=list)
    position: vec3 = field(default_factory=vec3_new)
    rotation: mat33 = field(default_factory=mat33_new)

    def read(self, read: PbdfReader) -> None:
        self.descriptor_index = read.i32()
        self.trigger = read.i32()
        self.frozen = read.i32()
        self.fixed = read.i32()
        self.speed = read.i32()
        self.events = [read.any(AnimationEvent) for _ in range(read.i32())]
        self.position = read.vec3()
        self.rotation = read.mat33()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.descriptor_index)
        write.i32(self.trigger)
        write.i32(self.frozen)
        write.i32(self.fixed)
        write.i32(self.speed)
        write.i32(len(self.events))
        [write.any(x) for x in self.events]
        write.vec3(self.position)
        write.mat33(self.rotation)


@dataclass
class AnimationList:
    event_count: int = 0
    animations: list[Animation] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        count = read.i32()
        self.event_count = read.i32()
        self.animations = [read.any(Animation) for _ in range(count)]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.animations))
        write.i32(self.event_count)
        [write.any(x) for x in self.animations]


@dataclass
class AnimationFile:
    event_list: EventList = field(default_factory=EventList)
    descriptors: list[AnimDescriptor] = field(default_factory=list)
    global_list: AnimationList = field(default_factory=AnimationList)
    sector_lists: list[AnimationList] = field(default_factory=list)

    def read(self, read: PbdfReader, sector_count: int) -> None:
        self.event_list = read.any(EventList)
        self.descriptors = [read.any(AnimDescriptor) for _ in range(read.i32())]
        read.i32()  # total animation count
        self.global_list = read.any(AnimationList)
        self.sector_lists = [read.any(AnimationList) for _ in range(sector_count)]

    def write(self, write: PbdfWriter, sector_count: int) -> None:
        write.any(self.event_list)
        write.i32(len(self.descriptors))
        [write.any(x) for x in self.descriptors]
        write.i32(self.calc_total_animation_count())
        write.any(self.global_list)
        [write.any(x) for x in self.sector_lists]

    def calc_total_animation_count(self) -> int:
        return len(self.global_list.animations) + sum(len(x.animations) for x in self.sector_lists)


@dataclass
class Speaker:
    exist: bool = False
    position: vec3 = field(default_factory=vec3_new)
    rotation: mat33 = field(default_factory=mat33_new)
    sound_id: int = 0

    def read(self, read: PbdfReader) -> None:
        self.exist = read.b32()
        self.position = read.vec3()
        self.rotation = read.mat33()
        self.sound_id = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.b32(self.exist)
        write.vec3(self.position)
        write.mat33(self.rotation)
        write.i32(self.sound_id)


@dataclass
class SpeakerFile:
    speakers: list[Speaker] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.speakers = [read.any(Speaker) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.speakers))
        [write.any(x) for x in self.speakers]


@dataclass
class World:
    fog_distance: int = 0
    fog_intensity: int = 0
    fog_mist_z: int = 0
    fog_mist_intensity: int = 0
    bg_on: bool = False
    bg_color: int = 0

    def read(self, read: PbdfReader) -> None:
        self.fog_distance = read.i32()
        self.fog_intensity = read.i32()
        self.fog_mist_z = read.i32()
        self.fog_mist_intensity = read.i32()
        self.bg_on = read.b32()
        self.bg_color = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.fog_distance)
        write.i32(self.fog_intensity)
        write.i32(self.fog_mist_z)
        write.i32(self.fog_mist_intensity)
        write.b32(self.bg_on)
        write.i32(self.bg_color)


@dataclass
class World2:
    bg_texture_project_name: str = ""
    bg_texture_project: TextureProject = field(default_factory=TextureProject)
    bg_texture_start: int = 0
    bg_texture_end: int = 0
    sky_type: int = 0
    sky_z: int = 0
    sky_zoom: int = 0
    sky_gouraud_intensity: int = 0
    sky_gouraud_start: int = 0
    sky_speed: int = 0
    sky_texture_project_name: str = ""
    sky_texture_project: TextureProject = field(default_factory=TextureProject)
    sky_lensflare_texture: bytes = field(default_factory=lambda: bytes(0))
    sky_sun_color: int = 0
    sky_arcade: int = 0

    def read(self, read: PbdfReader) -> None:
        self.bg_texture_project_name = read.str()
        self.bg_texture_project = read.any(TextureProject, 256)
        self.bg_texture_start = read.i32()
        self.bg_texture_end = read.i32()
        self.sky_type = read.i32()
        self.sky_z = read.i32()
        self.sky_zoom = read.i32()
        self.sky_gouraud_intensity = read.i32()
        self.sky_gouraud_start = read.i32()
        self.sky_speed = read.i32()
        self.sky_texture_project_name = read.str()
        self.sky_texture_project = read.any(TextureProject, read.format.tex_size_small)
        if read.format.voodoo:
            self.sky_lensflare_texture = read.bytes(read.format.tex_size_small * read.format.tex_size_small * read.format.tex_bpp)
        self.sky_sun_color = read.i32()
        if read.format.release == PbdfRelease.ARCADE:
            self.sky_arcade = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.str(self.bg_texture_project_name)
        write.any(self.bg_texture_project)
        write.i32(self.bg_texture_start)
        write.i32(self.bg_texture_end)
        write.i32(self.sky_type)
        write.i32(self.sky_z)
        write.i32(self.sky_zoom)
        write.i32(self.sky_gouraud_intensity)
        write.i32(self.sky_gouraud_start)
        write.i32(self.sky_speed)
        write.str(self.sky_texture_project_name)
        write.any(self.sky_texture_project)
        if write.format.voodoo:
            write.bytes(self.sky_lensflare_texture)
        write.i32(self.sky_sun_color)
        if write.format.release == PbdfRelease.ARCADE:
            write.i32(self.sky_arcade)


@dataclass
class SectorAniFile:
    has_face_material: bool = False
    objects: list[Object] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.has_face_material = read.b32()
        self.objects = [read.any(Object, self.has_face_material, False, True) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.b32(self.has_face_material)
        write.i32(len(self.objects))
        [write.any(x, self.has_face_material, False, True) for x in self.objects]


@dataclass
class SectorAniInfo:
    sector_index: int = 0
    file: SectorAniFile = field(default_factory=SectorAniFile)
    unknown10: int = 0
    subs: list[vec2i32] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.sector_index = read.i32()
        self.file = read.any(SectorAniFile)
        sub_count = read.i32()
        self.unknown10 = read.i32()
        self.subs = [read.vec2i32() for _ in range(sub_count)]

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.sector_index)
        write.any(self.file)
        write.i32(len(self.subs))
        write.i32(self.unknown10)
        [write.vec2i32(x) for x in self.subs]


@dataclass
class SectorAniInfoFile:
    infos: list[SectorAniInfo] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.anis = [read.any(SectorAniInfo) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.anis))
        [write.any(x) for x in self.anis]


@dataclass
class TexAniKey:
    texture_index: int = 0
    uvs: list[vec2i32] = field(default_factory=lambda: [(0, 0)] * 4)

    def read(self, read: PbdfReader) -> None:
        self.texture_index = read.i32()
        self.uvs = [read.vec2i32() for _ in range(4)]

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.texture_index)
        [write.vec2i32(x) for x in self.uvs]


@dataclass
class TexAniStep:
    time: float = 0.0
    key_index: int = 0

    def read(self, read: PbdfReader) -> None:
        self.time = read.f()
        self.key_index = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.f(self.time)
        write.i32(self.key_index)


@dataclass
class TexAniFile:
    keys: list[TexAniKey] = field(default_factory=list)
    duration: float = 0.0
    sync_curve: list[TexAniStep] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.keys = [read.any(TexAniKey) for _ in range(read.i32())]
        self.duration = read.f()
        self.sync_curve = [read.any(TexAniStep) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.keys))
        [write.any(x) for x in self.keys]
        write.f(self.duration)
        write.i32(len(self.sync_curve))
        [write.any(x) for x in self.sync_curve]


@dataclass
class TexAniPoly:
    loop: int = 0
    index_count: int = 0
    face_index: int = 0

    def read(self, read: PbdfReader) -> None:
        self.loop = read.i32()
        self.index_count = read.i32()
        self.face_index = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.loop)
        write.i32(self.index_count)
        write.i32(self.face_index)


@dataclass
class TexAniSector:
    sector_index: int = 0
    polys: list[TexAniPoly] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.sector_index = read.i32()
        self.polys = [read.any(TexAniPoly) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.sector_index)
        write.i32(len(self.polys))
        [write.any(x) for x in self.polys]


@dataclass
class TexAni:
    ani_index: int = 0
    sectors: list[TexAniSector] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.ani_index = read.i32()
        self.sectors = [read.any(TexAniSector) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.ani_index)
        write.i32(len(self.sectors))
        [write.any(x) for x in self.sectors]


@dataclass
class TexAniInfoFile:
    ani_filenames: list[str] = field(default_factory=list)
    ani_files: list[TexAniFile] = field(default_factory=list)
    anis: list[TexAni] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        for _ in range(read.i32()):
            self.ani_filenames.append(read.str())
            self.ani_files.append(read.any(TexAniFile))
        read.i32()  # poly count total
        self.anis = [read.any(TexAni) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.ani_files))
        for i in range(len(self.ani_files)):
            write.str(self.ani_filenames[i])
            write.any(self.ani_files[i])
        write.i32(self.calc_poly_count_total())
        write.i32(len(self.anis))
        [write.any(x) for x in self.anis]

    def calc_poly_count_total(self) -> int:
        return sum(sum(len(s.polys) for s in a.sectors) for a in self.anis)


@dataclass
class RepairZone:
    positions: list[vec3] = field(default_factory=lambda: [vec3_new()] * 4)
    center: vec3 = field(default_factory=vec3_new)
    height: float = 0.0
    size: float = 0.0

    def read(self, read: PbdfReader) -> None:
        self.positions = [read.vec3() for _ in range(4)]
        self.center = read.vec3()
        self.height = read.f()
        self.size = read.f()

    def write(self, write: PbdfWriter) -> None:
        [write.vec3(x) for x in self.positions]
        write.vec3(self.center)
        write.f(self.height)
        write.f(self.size)


@dataclass
class RepairZoneFile:
    repair_zones: list[RepairZone] = field(default_factory=list)
    repair_seconds: float = 0.0

    def read(self, read: PbdfReader) -> None:
        self.repair_zones = [read.any(RepairZone) for _ in range(read.i32())]
        self.repair_seconds = read.f()

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.repair_zones))
        [write.any(x) for x in self.repair_zones]
        write.f(self.repair_seconds)


@dataclass
class TimeFile:
    has_lap_times: bool = False
    lap_min: float = 0.0
    lap_avg: float = 0.0
    has_part_times: bool = False
    parts_min: list[float] = field(default_factory=lambda: [0.0] * 5)
    parts_avg: list[float] = field(default_factory=lambda: [0.0] * 5)

    def read(self, read: PbdfReader) -> None:
        self.has_lap_times = read.b32()
        self.lap_min = read.f()
        self.lap_avg = read.f()
        self.has_part_times = read.b32()
        self.parts_min = [read.f() for _ in range(5)]
        self.parts_avg = [read.f() for _ in range(5)]

    def write(self, write: PbdfWriter) -> None:
        write.b32(self.has_lap_times)
        write.f(self.lap_min)
        write.f(self.lap_avg)
        write.b32(self.has_part_times)
        [write.f(x) for x in self.parts_min]
        [write.f(x) for x in self.parts_avg]


@dataclass
class Beacon:
    points: list[vec3] = field(default_factory=lambda: [vec3_new()] * 4)
    normal: vec3 = field(default_factory=vec3_new)
    positive_event: int = 0
    negative_event: int = 0

    def read(self, read: PbdfReader) -> None:
        self.points = [read.vec3() for _ in range(4)]
        self.normal = read.vec3()
        self.positive_event = read.i32()
        self.negative_event = read.i32()

    def write(self, write: PbdfWriter) -> None:
        [write.vec3(x) for x in self.points]
        write.vec3(self.normal)
        write.i32(self.positive_event)
        write.i32(self.negative_event)


@dataclass
class Checkpoint:
    beacon_index: int = 0
    positive: int = 0
    distance_to_next: int = 0
    map_line_from: vec3 = field(default_factory=vec3_new)
    map_line_to: vec3 = field(default_factory=vec3_new)

    def read(self, read: PbdfReader) -> None:
        self.beacon_index = read.i32()
        self.positive = read.i16()
        self.distance_to_next = read.i16()
        self.map_line_from = read.vec3()
        self.map_line_to = read.vec3()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.beacon_index)
        write.i16(self.positive)
        write.i16(self.distance_to_next)
        write.vec3(self.map_line_from)
        write.vec3(self.map_line_to)


@dataclass
class BeaconFile:
    event_list: EventList = field(default_factory=EventList)
    beacons: list[Beacon] = field(default_factory=list)
    checkpoints: list[Checkpoint] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.event_list = read.any(EventList)
        self.beacons = [read.any(Beacon) for _ in range(read.i32())]
        if read.format.release != PbdfRelease.OEM:
            self.checkpoints = [read.any(Checkpoint) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.any(self.event_list)
        write.i32(len(self.beacons))
        [write.any(x) for x in self.beacons]
        if write.format.release != PbdfRelease.OEM:
            write.i32(len(self.checkpoints))
            [write.any(x) for x in self.checkpoints]


@dataclass
class Phase:
    name: str = ""
    event_index: int = 0

    def read(self, read: PbdfReader) -> None:
        self.name = read.str()
        self.event_index = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.str(self.name)
        write.i32(self.event_index)


@dataclass
class PhaseFile:
    event_list: EventList = field(default_factory=EventList)
    phases: list[Phase] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.event_list = read.any(EventList)
        self.phases = [read.any(Phase) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.any(self.event_list)
        write.i32(len(self.phases))
        [write.any(x) for x in self.phases]


@dataclass
class Gate:
    position: vec3 = field(default_factory=vec3_new)
    axis_x: vec3 = field(default_factory=vec3_new)
    axis_y: vec3 = field(default_factory=vec3_new)

    def read(self, read: PbdfReader) -> None:
        self.position = read.vec3()
        self.axis_x = read.vec3()
        self.axis_y = read.vec3()

    def write(self, write: PbdfWriter) -> None:
        write.vec3(self.position)
        write.vec3(self.axis_x)
        write.vec3(self.axis_y)


@dataclass
class GateFile:
    gates: list[Gate] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.gates = [read.any(Gate) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.gates))
        [write.any(x) for x in self.gates]


@dataclass
class PitFile:
    pits: list[vec3] = field(default_factory=list)
    repair_seconds: int = 0

    def read(self, read: PbdfReader) -> None:
        self.pits = [read.vec3() for _ in range(read.i32())]
        self.repair_seconds = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.pits))
        [write.vec3(x) for x in self.pits]
        write.i32(self.repair_seconds)


class MapGraph(enum.IntEnum):
    NONE = 0
    PREFER = 1
    IGNORE = 2
    ADDITIONAL = 3


class MapConstraintType(enum.IntEnum):
    NONE = 0
    MIN_SPEED = 1
    MAX_SPEED = 2
    STOP_ATTACK = 3
    DISENGAGE = 4
    PIT = 5
    START = 6


@dataclass
class MapConstraintData:
    type: MapConstraintType = MapConstraintType.NONE
    graph: MapGraph = MapGraph.NONE
    hidden: bool = False
    disabled: bool = False
    number: int = 0
    param: int = 0


@dataclass
class MapTrail:
    level: int = 0
    position_count: int = 0
    position_start: int = 0
    constraint: int = 0

    def read(self, read: PbdfReader) -> None:
        self.level = read.i32()
        self.position_count = read.i32()
        self.position_start = read.i32()
        self.constraint = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.level)
        write.i32(self.position_count)
        write.i32(self.position_start)
        write.i32(self.constraint)

    def get_constraint_data(self) -> MapConstraintData:
        type = MapConstraintType(self.constraint & 0xF)
        graph = MapGraph(self.constraint >> 4 & 0b11)
        hidden = bool(self.constraint >> 6 & 0b1)
        disabled = bool(self.constraint >> 7 & 0b1)
        number = self.constraint >> 8 & 0xFF
        param = self.constraint >> 16 & 0xFFFF
        return MapConstraintData(type, graph, hidden, disabled, number, param)

    def set_constraint_data(self, data: MapConstraintData) -> None:
        self.constraint = data.type.value
        self.constraint |= data.graph.value << 4
        self.constraint |= data.hidden << 6
        self.constraint |= data.disabled << 7
        self.constraint |= (data.number & 0xFF) << 8
        self.constraint |= (data.param & 0xFFFF) << 16


@dataclass
class MapSection:
    trails: list[MapTrail] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.trails = [read.any(MapTrail) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.trails))
        [write.any(x) for x in self.trails]


@dataclass
class MapConstraint:
    beacon_index: int = 0
    guide_index: int = 0
    constraint: int = 0

    def read(self, read: PbdfReader) -> None:
        self.beacon_index = read.i32()
        self.guide_index = read.i32()
        self.constraint = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.beacon_index)
        write.i32(self.guide_index)
        write.i32(self.constraint)


@dataclass
class MapFile:
    positions: list[vec3] = field(default_factory=list)
    sections: list[MapSection] = field(default_factory=list)
    constraint_name: str = "NEANT"
    constraints: list[MapConstraint] = field(default_factory=list)
    passes_oem: list[int] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        if read.format.release == PbdfRelease.OEM:
            self.passes_oem = [read.i32() for _ in range(read.i32())]
        self.positions = [read.vec3() for _ in range(read.i32())]
        self.sections = [read.any(MapSection) for _ in range(read.i32())]
        self.constraint_name = read.str()
        if self.constraint_name == "PLANS CONTRAINTES":
            self.constraints = [read.any(MapConstraint) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        if write.format.release == PbdfRelease.OEM:
            write.i32(len(self.passes_oem))
            [write.i32(x) for x in self.passes_oem]
        write.i32(len(self.positions))
        [write.vec3(x) for x in self.positions]
        write.i32(len(self.sections))
        [write.any(x) for x in self.sections]
        write.str(self.constraint_name)
        if self.constraint_name == "PLANS CONTRAINTES":
            write.i32(len(self.constraints))
            [write.any(x) for x in self.constraints]


@dataclass
class PathNode:
    position: vec3 = field(default_factory=vec3_new)
    distance: float = 0.0
    neighbor: int = -1
    out_arcs: list[int] = field(default_factory=list)
    in_arcs: list[int] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.position = read.vec3()
        self.distance = read.f()
        if read.format.release != PbdfRelease.OEM:
            self.neighbor = read.i32()
        self.out_arcs = [read.i32() for _ in range(read.i32())]
        self.in_arcs = [read.i32() for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.vec3(self.position)
        write.f(self.distance)
        if write.format.release != PbdfRelease.OEM:
            write.i32(self.neighbor)
        write.i32(len(self.out_arcs))
        [write.i32(x) for x in self.out_arcs]
        write.i32(len(self.in_arcs))
        [write.i32(x) for x in self.in_arcs]


@dataclass
class PathArc:
    parent_node: int = 0
    child_node: int = 0
    trails: list[int] = field(default_factory=list)
    distance_trail: int = 0
    distances: list[float] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.parent_node = read.i32()
        self.child_node = read.i32()
        self.trails = [read.i32() for _ in range(read.i32())]
        self.distance_trail = read.i32()
        self.distances = [read.f() for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.parent_node)
        write.i32(self.child_node)
        write.i32(len(self.trails))
        [write.i32(x) for x in self.trails]
        write.i32(self.distance_trail)
        write.i32(len(self.distances))
        [write.f(x) for x in self.distances]


@dataclass
class PathNeighbor:
    initial_node: int = 0
    final_node: int = 0
    parent_neighbor: int = 0

    def read(self, read: PbdfReader) -> None:
        self.initial_node = read.i32()
        self.final_node = read.i32()
        self.parent_neighbor = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.initial_node)
        write.i32(self.final_node)
        write.i32(self.parent_neighbor)


@dataclass
class PathFile:
    circuit_length: float = 0.0
    nodes: list[PathNode] = field(default_factory=list)
    arcs: list[PathArc] = field(default_factory=list)
    neighbors: list[PathNeighbor] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.circuit_length = read.f()
        node_count = read.i32()
        arc_count = read.i32()
        if read.format.release != PbdfRelease.OEM:
            neighbor_count = read.i32()
            read.i32()  # alloc size
        else:
            neighbor_count = 0
        self.nodes = [read.any(PathNode) for _ in range(node_count)]
        self.arcs = [read.any(PathArc) for _ in range(arc_count)]
        self.neighbors = [read.any(PathNeighbor) for _ in range(neighbor_count)]

    def write(self, write: PbdfWriter) -> None:
        write.f(self.circuit_length)
        write.i32(len(self.nodes))
        write.i32(len(self.arcs))
        if write.format.release != PbdfRelease.OEM:
            write.i32(len(self.neighbors))
            write.i32(self.calc_alloc_size())
        [write.any(x) for x in self.nodes]
        [write.any(x) for x in self.arcs]
        if write.format.release != PbdfRelease.OEM:
            [write.any(x) for x in self.neighbors]

    def calc_alloc_size(self) -> int:
        size = 0
        size += sum(len(node.out_arcs) + len(node.in_arcs) for node in self.nodes)
        size += sum(len(arc.trails) + len(arc.distances) for arc in self.arcs)
        return size


class CompetitorAttackType(enum.IntEnum):
    DETACH = 1
    PASS_RIGHT = 2
    PASS_LEFT = 3
    TAIL_RIGHT = 5
    TAIL_LEFT = 6
    ZIGZAG = 7
    HIT_FRONT = 8
    ACCEL = 10
    BRAKE = 11
    HIT_RIGHT = 12
    HIT_LEFT = 13
    ERROR = 15
    EVENT = 16


class CompetitorAttackContext(enum.IntFlag):
    NONE = 0
    FRONT = 1 << 0
    LEFT = 1 << 1
    RIGHT = 1 << 2
    REAR = 1 << 3


@dataclass
class CompetitorAttack:
    type: CompetitorAttackType = CompetitorAttackType.ERROR
    context: CompetitorAttackContext = CompetitorAttackContext.NONE
    percentage: int = 0

    def read(self, read: PbdfReader) -> None:
        self.type = CompetitorAttackType(read.i32())
        self.context = CompetitorAttackContext(read.i32())
        self.percentage = read.i32()

    def write(self, write: PbdfWriter) -> None:
        write.i32(self.type.value)
        write.i32(self.context.value)
        write.i32(self.percentage)


class CompetitorBehavior(enum.IntEnum):
    PASSIVE = 1
    DEFENSIVE = 2
    AGGRESSIVE = 3


@dataclass
class Competitor:
    name: str = ""
    level: int = 0
    behavior: int = CompetitorBehavior.PASSIVE
    car_index: str = ""
    attacks: list[CompetitorAttack] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.name = read.str()
        self.level = read.i32()
        self.behavior = read.i32()
        self.car_index = read.str()
        self.attacks = [read.any(CompetitorAttack) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.str(self.name)
        write.i32(self.level)
        write.i32(self.behavior)
        write.str(self.car_index)
        write.i32(len(self.attacks))
        [write.any(x) for x in self.attacks]


@dataclass
class CompetitorFile:
    competitors: list[Competitor] = field(default_factory=list)

    def read(self, read: PbdfReader) -> None:
        self.competitors = [read.any(Competitor) for _ in range(read.i32())]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.competitors))
        [write.any(x) for x in self.competitors]


@dataclass
class CircuitDifficulty:
    difficulty_name: str = ""
    map_filename: str = "NEANT"
    map_file: MapFile = field(default_factory=MapFile)
    path_filename: str = "NEANT"
    path_file: PathFile = field(default_factory=PathFile)
    competitor_filename_oem: str = "NEANT"
    competitor_file_oem: CompetitorFile = field(default_factory=CompetitorFile)

    def read(self, read: PbdfReader, offset: int) -> None:
        if offset and read.format.release != PbdfRelease.ARCADE:
            read.offset(offset)
        self.difficulty_name = read.str()

        self.map_filename = read.str()
        if self.map_filename.upper() != "NEANT":
            self.map_file = read.any(MapFile)

        self.path_filename = read.str()
        if self.path_filename.upper() != "NEANT":
            self.path_file = read.any(PathFile)

        if read.format.release == PbdfRelease.OEM:
            self.competitor_filename_oem = read.str()
            if self.competitor_filename_oem.upper() != "NEANT":
                self.competitor_file_oem = read.any(CompetitorFile)

    def write(self, write: PbdfWriter, offset: int) -> None:
        if offset and write.format.release != PbdfRelease.ARCADE:
            write.offset()
        write.str(self.difficulty_name)

        write.str(self.map_filename)
        if self.map_filename.upper() != "NEANT":
            write.any(self.map_file)

        write.str(self.path_filename)
        if self.path_filename.upper() != "NEANT":
            write.any(self.path_file)

        if write.format.release == PbdfRelease.OEM:
            write.str(self.competitor_filename_oem)
            if self.competitor_filename_oem.upper() != "NEANT":
                write.any(self.competitor_file_oem)


@dataclass
class CircuitDirection:
    time_file: TimeFile = field(default_factory=TimeFile)
    beacon_filename: str = "NEANT"
    beacon_file: BeaconFile = field(default_factory=BeaconFile)
    phase_file: PhaseFile = field(default_factory=PhaseFile)
    gate_file: GateFile = field(default_factory=GateFile)
    difficulty_easy: CircuitDifficulty = field(default_factory=CircuitDifficulty)
    difficulty_medium: CircuitDifficulty = field(default_factory=CircuitDifficulty)
    difficulty_hard: CircuitDifficulty = field(default_factory=CircuitDifficulty)

    def read(self, read: PbdfReader, offset: int) -> None:
        if offset and read.format.release != PbdfRelease.ARCADE:
            read.offset(offset)

        self.time_file = read.any(TimeFile)

        self.beacon_filename = read.str()
        if self.beacon_filename.upper() != "NEANT":
            self.beacon_file = read.any(BeaconFile)
            self.phase_file = read.any(PhaseFile)

        self.gate_file = read.any(GateFile)

        self.difficulty_easy = read.any(CircuitDifficulty, 0)
        self.difficulty_medium = read.any(CircuitDifficulty, offset + 1)
        self.difficulty_hard = read.any(CircuitDifficulty, offset + 2)

    def write(self, write: PbdfWriter, offset: int) -> None:
        if offset and write.format.release != PbdfRelease.ARCADE:
            write.offset()

        write.any(self.time_file)

        write.str(self.beacon_filename)
        if self.beacon_filename.upper() != "NEANT":
            write.any(self.beacon_file)
            write.any(self.phase_file)

        write.any(self.gate_file)

        write.any(self.difficulty_easy, 0)
        write.any(self.difficulty_medium, offset + 1)
        write.any(self.difficulty_hard, offset + 2)


@dataclass
class CircuitConcurrent:
    difficulty_name: str = ""
    competitor_filename: str = "NEANT"
    competitor_file: CompetitorFile = field(default_factory=CompetitorFile)

    def read(self, read: PbdfReader, offset: int) -> None:
        if read.format.release != PbdfRelease.ARCADE:
            read.offset(offset)
        self.difficulty_name = read.str()

        self.competitor_filename = read.str()
        if self.competitor_filename.upper() != "NEANT":
            self.competitor_file = read.any(CompetitorFile)

    def write(self, write: PbdfWriter, offset: int) -> None:
        if write.format.release != PbdfRelease.ARCADE:
            write.offset()
        write.str(self.difficulty_name)

        write.str(self.competitor_filename)
        if self.competitor_filename.upper() != "NEANT":
            write.any(self.competitor_file)


@dataclass
class Circuit:
    event_type_file: EventTypeFile = field(default_factory=EventTypeFile)
    event_macro_file: EventMacroFile = field(default_factory=EventMacroFile)
    route_filename: str = ""
    voodoo_file: VoodooFile = field(default_factory=VoodooFile)
    route_file: RouteFile = field(default_factory=RouteFile)
    zone_file: ZoneFile = field(default_factory=ZoneFile)
    environment_filename: str = "NEANT"
    environment_file: EnvironmentFile = field(default_factory=EnvironmentFile)
    light_filename: str = "NEANT"
    light_file: LightFile = field(default_factory=LightFile)
    animation_filename: str = "NEANT"
    animation_file: AnimationFile = field(default_factory=AnimationFile)
    speaker_filename: str = "NEANT"
    speaker_file: SpeakerFile = field(default_factory=SpeakerFile)
    world: World = field(default_factory=World)
    world2: World2 = field(default_factory=World2)
    ani_info_filenames: list[str] = field(default_factory=list)
    ani_info_files: list[BinaryWritable] = field(default_factory=list)
    repair_zone_filename: str = "NEANT"
    repair_zone_file: RepairZoneFile = field(default_factory=RepairZoneFile)
    direction_forward: CircuitDirection = field(default_factory=CircuitDirection)
    direction_reverse: CircuitDirection = field(default_factory=CircuitDirection)
    concurrent_easy: CircuitConcurrent = field(default_factory=CircuitConcurrent)
    concurrent_medium: CircuitConcurrent = field(default_factory=CircuitConcurrent)
    concurrent_hard: CircuitConcurrent = field(default_factory=CircuitConcurrent)
    time_file_oem: TimeFile = field(default_factory=TimeFile)
    beacon_filename_oem: str = "NEANT"
    beacon_file_oem: BeaconFile = field(default_factory=BeaconFile)
    phase_file_oem: PhaseFile = field(default_factory=PhaseFile)
    gate_filename_oem: str = "NEANT"
    gate_file_oem: GateFile = field(default_factory=GateFile)
    pit_filename_oem: str = "NEANT"
    pit_file_oem: PitFile = field(default_factory=PitFile)
    difficulty_easy_oem: CircuitDifficulty = field(default_factory=CircuitDifficulty)
    difficulty_medium_oem: CircuitDifficulty = field(default_factory=CircuitDifficulty)
    difficulty_hard_oem: CircuitDifficulty = field(default_factory=CircuitDifficulty)

    def read(self, read: PbdfReader) -> None:
        read.offset(0)
        if read.format.release != PbdfRelease.OEM:
            read.i32()  # 3
            read.i32()  # unused

        self.event_type_file = read.any(EventTypeFile)
        self.event_macro_file = read.any(EventMacroFile)

        if read.format.release == PbdfRelease.OEM:
            self.time_file_oem = read.any(TimeFile)
        if read.format.version < 8:
            self.route_filename = read.str()
        if read.format.voodoo:
            self.voodoo_file = read.any(VoodooFile)
        self.route_file = read.any(RouteFile)
        self.zone_file = read.any(ZoneFile)

        self.environment_filename = read.str()
        if self.environment_filename.upper() != "NEANT":
            self.environment_file = read.any(EnvironmentFile, len(self.route_file.sectors))

        if read.format.version < 8:
            self.light_filename = read.str()
            if self.light_filename.upper() != "NEANT":
                self.light_file = read.any(LightFile)

            self.animation_filename = read.str()
            if self.animation_filename.upper() != "NEANT":
                self.animation_file = read.any(AnimationFile, len(self.route_file.sectors))
        else:
            self.animation_file = read.any(AnimationFile, len(self.route_file.sectors))
            self.light_file = read.any(LightFile)

        if read.format.release == PbdfRelease.OEM:
            self.beacon_filename_oem = read.str()
            if self.beacon_filename_oem.upper() != "NEANT":
                self.beacon_file_oem = read.any(BeaconFile)
                self.phase_file_oem = read.any(PhaseFile)

        if read.format.version < 6:
            self.speaker_filename = read.str()
            if self.speaker_filename.upper() != "NEANT":
                self.speaker_file = read.any(SpeakerFile)

            self.world = read.any(World)
        else:
            self.world = read.any(World)

            self.speaker_filename = read.str()
            if self.speaker_filename.upper() != "NEANT":
                self.speaker_file = read.any(SpeakerFile)

        self.world2 = read.any(World2)

        for _ in range(read.i32() // 2):
            ani_info_filename = read.str()
            self.ani_info_filenames.append(ani_info_filename)
            if ani_info_filename == "ANIME SECTEUR":
                self.ani_info_files.append(read.any(SectorAniInfoFile))
            else:
                self.ani_info_files.append(read.any(TexAniInfoFile))

        if read.format.release == PbdfRelease.OEM:
            self.gate_filename_oem = read.str()
            if self.gate_filename_oem.upper() != "NEANT":
                self.gate_file_oem = read.any(GateFile)

            self.pit_filename_oem = read.str()
            if self.pit_filename_oem.upper() != "NEANT":
                self.pit_file_oem = read.any(PitFile)

            self.difficulty_easy_oem = read.any(CircuitDifficulty, 1)
            self.difficulty_medium_oem = read.any(CircuitDifficulty, 2)
            self.difficulty_hard_oem = read.any(CircuitDifficulty, 3)
        else:
            self.repair_zone_filename = read.str()
            if self.repair_zone_filename.upper() != "NEANT":
                self.repair_zone_file = read.any(RepairZoneFile)

            self.direction_forward = read.any(CircuitDirection, 0)
            self.direction_reverse = read.any(CircuitDirection, 3)
            self.concurrent_easy = read.any(CircuitConcurrent, 6)
            self.concurrent_medium = read.any(CircuitConcurrent, 7)
            self.concurrent_hard = read.any(CircuitConcurrent, 8)
            read.offset(9)  # unused

    def write(self, write: PbdfWriter) -> None:
        write.offset()
        if write.format.release != PbdfRelease.OEM:
            write.i32(3)  # 3
            write.i32(0)  # unused

        write.any(self.event_type_file)
        write.any(self.event_macro_file)

        if write.format.release == PbdfRelease.OEM:
            write.any(self.time_file_oem)
        if write.format.version < 8:
            write.str(self.route_filename)
        if write.format.voodoo:
            write.any(self.voodoo_file)
        write.any(self.route_file)
        write.any(self.zone_file)

        write.str(self.environment_filename)
        if self.environment_filename.upper() != "NEANT":
            write.any(self.environment_file, len(self.route_file.sectors))

        if write.format.version < 8:
            write.str(self.light_filename)
            if self.light_filename.upper() != "NEANT":
                write.any(self.light_file)

            write.str(self.animation_filename)
            if self.animation_filename.upper() != "NEANT":
                write.any(self.animation_file, len(self.route_file.sectors))
        else:
            write.any(self.animation_file, len(self.route_file.sectors))
            write.any(self.light_file)

        if write.format.release == PbdfRelease.OEM:
            write.str(self.beacon_filename_oem)
            if self.beacon_filename_oem.upper() != "NEANT":
                write.any(self.beacon_file_oem)
                write.any(self.phase_file_oem)

        if write.format.version < 6:
            write.str(self.speaker_filename)
            if self.speaker_filename.upper() != "NEANT":
                write.any(self.speaker_file)

            write.any(self.world)
        else:
            write.any(self.world)

            write.str(self.speaker_filename)
            if self.speaker_filename.upper() != "NEANT":
                write.any(self.speaker_file)

        write.any(self.world2)

        write.i32(len(self.ani_info_filenames) * 2)
        for i in range(len(self.ani_info_filenames)):
            write.str(self.ani_info_filenames[i])
            write.any(self.ani_info_files[i])

        if write.format.release == PbdfRelease.OEM:
            write.str(self.gate_filename_oem)
            if self.gate_filename_oem.upper() != "NEANT":
                write.any(self.gate_file_oem)

            write.str(self.pit_filename_oem)
            if self.pit_filename_oem.upper() != "NEANT":
                write.any(self.pit_file_oem)

            write.any(self.difficulty_easy_oem, 1)
            write.any(self.difficulty_medium_oem, 2)
            write.any(self.difficulty_hard_oem, 3)
        else:
            write.str(self.repair_zone_filename)
            if self.repair_zone_filename.upper() != "NEANT":
                write.any(self.repair_zone_file)

            write.any(self.direction_forward, 0)
            write.any(self.direction_reverse, 3)
            write.any(self.concurrent_easy, 6)
            write.any(self.concurrent_medium, 7)
            write.any(self.concurrent_hard, 8)
            write.offset()  # unused
