import enum
import io
import os
import struct
from dataclasses import dataclass, field

from .binary import BinaryReader, BinaryWritable, BinaryWriter


@dataclass
class ReservoirTime:
    day: int = 0
    month: int = 0
    year: int = 0
    hour: int = 0
    minute: int = 0
    second: int = 0

    def read(self, read: BinaryReader) -> None:
        self.day = read.u8()
        self.month = read.u8()
        self.year = read.u8()
        self.hour = read.u8()
        self.minute = read.u8()
        self.second = read.u8()

    def write(self, write: BinaryWriter) -> None:
        write.u8(self.day)
        write.u8(self.month)
        write.u8(self.year)
        write.u8(self.hour)
        write.u8(self.minute)
        write.u8(self.second)


@dataclass
class ReservoirHeader:
    created: ReservoirTime = field(default_factory=ReservoirTime)
    modified: ReservoirTime = field(default_factory=ReservoirTime)
    description: str = ""
    project: str = ""
    version_minor: int = 0
    version_major: int = 0

    def read(self, read: BinaryReader) -> None:
        if read.strbytes(4) != "USSB":
            raise OSError("Invalid reservoir header.")
        self.created = read.any(ReservoirTime)
        self.modified = read.any(ReservoirTime)
        self.description = read.strbytes(0xFF)
        self.project = read.strbytes(81)
        self.version_minor = read.u16()
        self.version_major = read.u16()

    def write(self, write: BinaryWriter) -> None:
        write.strbytes("USSB", 4)
        write.any(self.created)
        write.any(self.modified)
        write.strbytes(self.description, 0xFF)
        write.strbytes(self.project, 81)
        write.u16(self.version_minor)
        write.u16(self.version_major)


@dataclass
class BflFile:
    samples: bytes = field(default_factory=lambda: bytes(0))

    def read(self, read: BinaryReader, length: int) -> None:
        self.sampels = read.bytes(length)

    def write(self, write: BinaryWriter) -> None:
        write.bytes(self.samples)

    def get_samples(self, rsv: 'RsvFile', resource_id: int, format_id: int) -> tuple[int, ...]:
        param = rsv.resources[resource_id].params[format_id]
        format = rsv.formats[format_id]
        samples = memoryview(self.samples)
        if format.bits == 8:
            return tuple(samples[param.ptr:param.ptr + param.size])
        elif format.bits == 16:
            return struct.unpack(f"<{param.size / 2}h", samples[param.ptr:param.ptr + param.size])
        else:
            raise ValueError("Invalid format bit depth.")


@dataclass
class BnkFile:
    ids: list[int] = field(default_factory=list)

    def read(self, read: BinaryReader) -> None:
        self.ids = [read.i16() for _ in range(read.u16())]

    def write(self, write: BinaryWriter) -> None:
        write.u16(len(self.ids))
        [write.i16(x) for x in self.ids]


@dataclass
class EsvEvent:
    id: int = 0
    name: str = ""
    author: str = ""
    type: int = 0
    param1: int = 0
    param2: int = 0
    param3: int = 0
    looping: bool = False
    spatial: bool = False
    doppler: bool = False
    dynamic: bool = False
    reverbable: bool = False
    stoppable: bool = False

    def read(self, read: BinaryReader) -> None:
        self.id = read.u16()
        self.name = read.strbytes(80)
        self.author = read.strbytes(14)
        self.type = read.u32()
        self.param1 = read.u32()
        self.param2 = read.u32()
        self.param3 = read.u32()
        self.looping = read.b32()
        self.spatial = read.b32()
        self.doppler = read.b32()
        self.dynamic = read.b32()
        self.reverbable = read.b32()
        self.stoppable = read.b32()

    def write(self, write: BinaryWriter) -> None:
        write.u16(self.id)
        write.strbytes(self.name, 80)
        write.strbytes(self.author, 14)
        write.u32(self.type)
        write.u32(self.param1)
        write.u32(self.param2)
        write.u32(self.param3)
        write.b32(self.looping)
        write.b32(self.spatial)
        write.b32(self.doppler)
        write.b32(self.dynamic)
        write.b32(self.reverbable)
        write.b32(self.stoppable)


class EsvParamType(enum.IntEnum):
    RESOURCE = 0
    EVENT = 1
    FULL = 2
    CALCULATION = 3


@dataclass
class EsvParam:
    name: str = ""
    type: EsvParamType = EsvParamType.RESOURCE

    def read(self, read: BinaryReader) -> None:
        self.name = read.strbytes(19)
        self.type = EsvParamType(read.u8())

    def write(self, write: BinaryWriter) -> None:
        write.strbytes(self.name, 19)
        write.u8(self.type)


@dataclass
class EsvType:
    description: str = ""
    params: list[EsvParam] = field(default_factory=lambda: [EsvParam()] * 3)

    def read(self, read: BinaryReader) -> None:
        self.description = read.strbytes(20)
        self.params = [read.any(EsvParam) for _ in range(3)]

    def write(self, write: BinaryWriter) -> None:
        write.strbytes(self.description, 20)
        [write.any(self.params[i]) for i in range(3)]


@dataclass
class EsvFile:
    header: ReservoirHeader = field(default_factory=ReservoirHeader)
    types: list[EsvType] = field(default_factory=list)
    events: list[EsvEvent] = field(default_factory=list)

    def read(self, read: BinaryReader) -> None:
        self.header = read.any(ReservoirHeader)
        event_count = read.u16()
        _ = read.u16()  # last_event_index
        type_count = read.u8()
        _ = read.u8()  # align
        self.types = [read.any(EsvType) for _ in range(type_count)]
        self.events = [read.any(EsvEvent) for _ in range(event_count)]

    def write(self, write: BinaryWriter) -> None:
        write.any(self.header)
        write.u16(len(self.events))
        write.u16(max(0, len(self.events) - 1))
        write.u8(len(self.types))
        write.u8(0)
        [write.any(x) for x in self.types]
        [write.any(x) for x in self.events]


@dataclass
class SmmRange:
    resource: int = 0
    vol_max: int = 0
    in_a: float = 0
    in_b: float = 0
    in_c: float = 0
    in_d: float = 0
    out_b: float = 0.0
    out_c: float = 0.0
    pitch: bool = False

    def read(self, read: BinaryReader) -> None:
        self.resource = read.u16()
        self.vol_max = read.u16()
        self.in_a = read.f()
        self.in_b = read.f()
        self.in_c = read.f()
        self.in_d = read.f()
        self.out_b = read.f()
        self.out_c = read.f()
        self.pitch = read.b32()

    def write(self, write: BinaryWriter) -> None:
        write.u16(self.resource)
        write.u16(self.vol_max)
        write.f(self.in_a)
        write.f(self.in_b)
        write.f(self.in_c)
        write.f(self.in_d)
        write.f(self.out_b)
        write.f(self.out_c)
        write.b32(self.pitch)


@dataclass
class SmmSplit:
    id: int = 0
    description: str = ""
    ranges: list[SmmRange] = field(default_factory=list)

    def read(self, read: BinaryReader) -> None:
        self.id = read.u32()
        range_count = read.i32()
        self.description = read.strbytes(20)
        if range_count > 0:
            self.ranges = [read.any(SmmRange) for _ in range(range_count)]

    def write(self, write: BinaryWriter) -> None:
        write.u32(self.id)
        write.u32(len(self.ranges))
        write.strbytes(self.description, 20)
        [write.any(x) for x in self.ranges]


@dataclass
class SmmFile:
    splits: list[SmmSplit] = field(default_factory=list)

    def read(self, read: BinaryReader) -> None:
        if read.strbytes(4) != "SMMH":
            raise OSError("Invalid SMM header.")
        split_count = read.u16()
        _ = read.u16()  # last_split_index
        self.splits = [read.any(SmmSplit) for _ in range(split_count)]

    def write(self, write: BinaryWriter) -> None:
        write.strbytes("SMMH", 4)
        write.u16(len(self.splits))
        write.u16(max(0, len(self.splits) - 1))
        [write.any(x) for x in self.splits]


@dataclass
class RsvParam:
    file: str = ""
    volume: int = 0
    is_looping: bool = False
    ptr: int = 0
    size: int = 0
    frequency: int = 0
    start_loop: int = 0
    loop_length: int = 0

    def read(self, read: BinaryReader) -> None:
        self.file = read.strbytes(21)
        self.volume = read.u8()
        read.file.seek(2, os.SEEK_CUR)  # align
        self.is_looping = read.b32()
        self.ptr = read.u32()
        self.size = read.u32()
        self.frequency = read.u32()
        self.start_loop = read.u32()
        self.loop_length = read.u32()

    def write(self, write: BinaryWriter) -> None:
        write.strbytes(self.file, 21)
        write.u8(self.volume)
        write.file.seek(2, os.SEEK_CUR)  # align
        write.b32(self.is_looping)
        write.u32(self.ptr)
        write.u32(self.size)
        write.u32(self.frequency)
        write.u32(self.start_loop)
        write.u32(self.loop_length)


class RsvResourceType(enum.IntEnum):
    SAMPLE = 1
    MIDI = 2
    CD = 3
    SEQUENCE = 4
    SPLIT = 5


@dataclass
class RsvResource:
    description: str = ""
    id: int = 0
    type: RsvResourceType = RsvResourceType.SAMPLE
    pitchable: bool = False
    volable: bool = False
    panable: bool = False
    spacable: bool = False
    reverbable: bool = False
    loadable: bool = False
    params: list[RsvParam] = field(default_factory=list)

    def read(self, read: BinaryReader, param_count: int) -> None:
        self.description = read.strbytes(0x100)
        self.id = read.u16()
        self.type = RsvResourceType(read.u16())
        self.pitchable = read.b32()
        self.volable = read.b32()
        self.panable = read.b32()
        self.spacable = read.b32()
        self.reverbable = read.b32()
        self.loadable = read.b32()
        self.params = [read.any(RsvParam) for _ in range(param_count)]

    def write(self, write: BinaryWriter, param_count: int) -> None:
        write.strbytes(self.description, 0x100)
        write.u16(self.id)
        write.u16(self.type)
        write.b32(self.pitchable)
        write.b32(self.volable)
        write.b32(self.panable)
        write.b32(self.spacable)
        write.b32(self.reverbable)
        write.b32(self.loadable)
        [write.any(self.params[i]) for i in range(param_count)]


@dataclass
class RsvFormat:
    bits: int = 0
    hz: int = 0

    def read(self, read: BinaryReader) -> None:
        self.bits = read.u16()
        self.hz = read.u16()

    def write(self, write: BinaryWriter) -> None:
        write.u16(self.bits)
        write.u16(self.hz)


@dataclass
class RsvFile:
    header: ReservoirHeader = field(default_factory=ReservoirHeader)
    formats: list[RsvFormat] = field(default_factory=list)
    resources: list[RsvResource] = field(default_factory=list)

    def read(self, read: BinaryReader) -> None:
        self.header = read.any(ReservoirHeader)
        resource_count = read.u16()
        _ = read.u16()  # last_resource_index
        format_count = read.u16()
        self.formats = [read.any(RsvFormat) for _ in range(format_count)]
        self.resources = [read.any(RsvResource, format_count) for _ in range(resource_count)]

    def write(self, write: BinaryWriter) -> None:
        write.any(self.header)
        write.u16(len(self.resources))
        write.u16(max(0, len(self.resources) - 1))
        write.u16(len(self.formats))
        [write.any(x) for x in self.formats]
        [write.any(x, len(self.formats)) for x in self.resources]


@dataclass
class MegaFile:
    rsv: RsvFile = field(default_factory=RsvFile)
    smm: SmmFile = field(default_factory=SmmFile)
    esv: EsvFile = field(default_factory=EsvFile)
    bnk: BnkFile = field(default_factory=BnkFile)
    bfl: BflFile = field(default_factory=BflFile)

    def read(self, read: BinaryReader) -> None:
        rsv_start = read.u32()
        rsv_length = read.u32()
        smm_start = read.u32()
        smm_length = read.u32()
        esv_start = read.u32()
        esv_length = read.u32()
        bnk_start = read.u32()
        bnk_length = read.u32()
        bfl_start = read.u32()
        bfl_length = read.u32()
        if rsv_length:
            read.file.seek(rsv_start)
            self.rsv = read.any(RsvFile)
        if smm_length:
            read.file.seek(smm_start)
            self.smm = read.any(SmmFile)
        if esv_length:
            read.file.seek(esv_start)
            self.esv = read.any(EsvFile)
        if bnk_length:
            read.file.seek(bnk_start)
            self.bnk = read.any(BnkFile)
        if bfl_length:
            read.file.seek(bfl_start)
            self.bfl = read.any(BflFile, bfl_length)

    def write(self, write: BinaryWriter) -> None:
        def write_sub(sub: BinaryWritable) -> tuple[int, int]:
            start = write.file.tell()
            write.any(sub)
            return (start, write.file.tell() - start)

        write.file.seek(40)
        rsv_start, rsv_length = write_sub(self.rsv)
        smm_start, smm_length = write_sub(self.smm)
        esv_start, esv_length = write_sub(self.esv)
        bnk_start, bnk_length = write_sub(self.bnk)
        bfl_start, bfl_length = write_sub(self.bfl)
        write.file.seek(0)
        write.u32(rsv_start)
        write.u32(rsv_length)
        write.u32(smm_start)
        write.u32(smm_length)
        write.u32(esv_start)
        write.u32(esv_length)
        write.u32(bnk_start)
        write.u32(bnk_length)
        write.u32(bfl_start)
        write.u32(bfl_length)
