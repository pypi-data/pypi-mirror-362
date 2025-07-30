import io
import os
from dataclasses import dataclass, field

from .binary import BinaryReader, BinaryWriter
from .typing import vec3, vec3_new


@dataclass
class SequenceHeader:
    type: int = 0
    data: bytes = field(default_factory=lambda: bytes(0))

    def read(self, read: BinaryReader) -> None:
        self.type = read.i32()
        self.data = read.bytes(read.i32())

    def write(self, write: BinaryWriter) -> None:
        write.i32(self.type)
        write.i32(len(self.data))
        write.bytes(self.data)


@dataclass
class SequenceInfo:
    unknown0: int = 0
    circuit_index: int = 0
    time: float = 0.0
    unknown1: list[int] = field(default_factory=lambda: [0] * 7)
    race_time: float = 0.0
    start_time: float = 0.0
    lap_times: list[float] = field(default_factory=lambda: [0.0] * 3)
    part_times: list[list[float]] = field(default_factory=lambda: [[0.0] * 3] * 4)
    unknown2: list[int] = field(default_factory=lambda: [0] * 6)
    vehicle_name: str = ""
    unknown3: list[int] = field(default_factory=lambda: [0] * 7)
    player_name: str = ""
    unknown4: bytes = field(default_factory=lambda: bytes(50))
    grip: int = 0
    speed: int = 0
    handling: int = 0
    brakes: int = 0
    accel: int = 0
    unknown5: int = 0
    unknown6: list[int] = field(default_factory=lambda: [0] * 5)

    def read(self, read: BinaryReader) -> None:
        self.unknown0 = read.i32()
        self.circuit_index = read.i32()
        self.time = read.f()
        self.unknown1 = [read.i32() for _ in range(7)]
        self.race_time = read.f()
        self.start_time = read.f()
        self.lap_times = [read.f() for _ in range(3)]
        self.part_times = [[read.f() for _ in range(4)] for _ in range(3)]
        self.unknown2 = [read.i32() for _ in range(6)]
        self.vehicle_name = read.strbytes(8)
        self.unknown3 = [read.i32() for _ in range(7)]
        self.player_name = read.strbytes(8)
        self.unknown4 = read.bytes(50)
        self.grip = read.u8() ^ 0x7C
        self.speed = read.u8() ^ 0xBD
        self.handling = read.u8() ^ 0x3A
        self.brakes = read.u8() ^ 0xE0
        self.accel = read.u8() ^ 0x1E
        self.unknown5 = read.u8()
        self.unknown6 = [read.i32() for _ in range(5)]

    def write(self, write: BinaryWriter) -> None:
        write.i32(self.unknown0)
        write.i32(self.circuit_index)
        write.f(self.time)
        [write.i32(x) for x in self.unknown1]
        write.f(self.race_time)
        write.f(self.start_time)
        [write.f(x) for x in self.lap_times]
        [[write.f(y) for y in x] for x in self.part_times]
        [write.i32(x) for x in self.unknown2]
        write.strbytes(self.vehicle_name, 8)
        [write.i32(x) for x in self.unknown3]
        write.strbytes(self.player_name, 8)
        write.bytes(self.unknown4)
        write.u8(self.grip ^ 0x7C)
        write.u8(self.speed ^ 0xBD)
        write.u8(self.handling ^ 0x3A)
        write.u8(self.brakes ^ 0xE0)
        write.u8(self.accel ^ 0x1E)
        write.u8(self.unknown5)
        [write.i32(x) for x in self.unknown6]


@dataclass
class SequencePoint:
    time: float = 0.0
    wheel_rotation_x: int = 0
    wheel_rotation_y: int = 0
    wheel_z0: float = 0
    wheel_z1: float = 0
    wheel_z2: float = 0
    wheel_z3: float = 0
    position: vec3 = field(default_factory=vec3_new)
    rotation_x: vec3 = field(default_factory=vec3_new)
    rotation_y: vec3 = field(default_factory=vec3_new)

    def read(self, read: BinaryReader) -> None:
        self.time = read.f()
        self.wheel_rotation_x = read.i32()
        self.wheel_rotation_y = read.i32()
        self.wheel_z0 = read.f()
        self.wheel_z1 = read.f()
        self.wheel_z2 = read.f()
        self.wheel_z3 = read.f()
        self.position = read.vec3()
        self.rotation_x = read.vec3()
        self.rotation_y = read.vec3()

    def write(self, write: BinaryWriter) -> None:
        write.f(self.time)
        write.i32(self.wheel_rotation_x)
        write.i32(self.wheel_rotation_y)
        write.f(self.wheel_z0)
        write.f(self.wheel_z1)
        write.f(self.wheel_z2)
        write.f(self.wheel_z3)
        write.vec3(self.position)
        write.vec3(self.rotation_x)
        write.vec3(self.rotation_y)


@dataclass
class Sequence:
    headers: list[SequenceHeader] = field(default_factory=list)
    info: SequenceInfo = field(default_factory=SequenceInfo)
    points: list[SequencePoint] = field(default_factory=list)

    def read(self, read: BinaryReader) -> None:
        if read.u32() != 0x12345678:
            raise OSError("Invalid sequence file first magic value.")
        if read.u32() != 0x78451236:
            raise OSError("Invalid sequence file second magic value.")
        if read.i32() != 2:
            raise OSError("Invalid sequence file version.")
        info_end = read.i32()
        _ = read.i32()  # info_start
        # Read headers.
        header_count = read.i32()
        read.i32()  # -1
        self.headers = [read.any(SequenceHeader) for _ in range(header_count)]
        # Read info.
        _ = read.i32()  # info_size
        self.info = read.any(SequenceInfo)
        # Read points.
        point_count = (read.file.seek(0, os.SEEK_END) - info_end) // 64
        read.file.seek(info_end)
        self.points = [read.any(SequencePoint) for _ in range(point_count)]

    def write(self, write: BinaryWriter) -> None:
        write.u32(0x12345678)
        write.u32(0x78451236)
        write.i32(2)
        write.i32(316)
        write.i32(60)
        # Write headers.
        write.i32(len(self.headers))
        write.i32(-1)
        [write.any(x) for x in self.headers]
        # Write info.
        write.i32(252)
        write.any(self.info)
        # Write points.
        [write.any(x) for x in self.points]


@dataclass
class Ghost:
    circuit_index: int = 0
    sequences: list[Sequence] = field(default_factory=list)

    def read(self, read: BinaryReader) -> None:
        if read.i32() != 1:
            raise OSError("Invalid ghost file version.")
        if read.u32() != 0x456F1E9C:
            raise OSError("Invalid ghost file first magic value.")
        if read.u32() != 0xFA48EFB4:
            raise OSError("Invalid ghost file first magic value.")
        sequence_count = read.i32()
        self.circuit_index = read.i32()
        # Read sequences.
        for _ in range(sequence_count):
            _ = read.f()  # race_time
            buffer = read.bytes(read.i32())
            with BinaryReader(io.BytesIO(buffer), read.encoding) as sequence_read:
                sequence = sequence_read.any(Sequence)
                self.sequences.append(sequence)

    def write(self, write: BinaryWriter) -> None:
        write.i32(1)
        write.u32(0x456F1E9C)
        write.u32(0xFA48EFB4)
        write.i32(len(self.sequences))
        write.i32(self.circuit_index)
        # Write sequences.
        for sequence in self.sequences:
            write.f(sequence.info.race_time)
            with BinaryWriter(io.BytesIO(), write.encoding) as sequence_write:
                sequence_write.any(sequence)
                write.i32(sequence_write.file.tell())
                sequence_write.file.seek(0)
                write.bytes(sequence_write.file.read())
