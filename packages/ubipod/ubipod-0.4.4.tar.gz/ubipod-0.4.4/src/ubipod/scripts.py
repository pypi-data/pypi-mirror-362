import io
from dataclasses import dataclass, field

from .binary import BinaryReader, BinaryWriter


@dataclass
class CircuitInfo:
    name: str = ""
    lev_name: str = ""
    tga_name: str = ""
    scotch: str = ""
    scotch_mirror: str = ""
    visible: bool = False
    mirror: bool = False
    version: int = 0
    id: int = 0
    length: int = 0  # meters
    laps: int = 0
    parts: int = 0

    def read(self, read: BinaryReader) -> None:
        self.name = read.strbytes(20)
        self.lev_name = read.strbytes(64)
        self.tga_name = read.strbytes(13)
        self.scotch = read.strbytes(13)
        self.scotch_mirror = read.strbytes(14)
        flags = read.u8()
        self.visible = flags & 1 << 0 != 0
        self.mirror = flags & 2 << 0 != 0
        self.version = read.u8()
        self.id = read.u8()
        read.u8()  # pad
        self.length = read.u32()
        self.laps = read.u8()
        self.parts = read.u8()
        read.u16()  # pad
        read.u32()  # bank_id (runtime)

    def write(self, write: BinaryWriter) -> None:
        write.strbytes(self.name, 20)
        write.strbytes(self.lev_name, 64)
        write.strbytes(self.tga_name, 13)
        write.strbytes(self.scotch, 13)
        write.strbytes(self.scotch_mirror, 14)
        write.u8(self.visible << 0 | self.mirror << 1)
        write.u8(self.version)
        write.u8(self.id)
        write.u8(0)  # pad
        write.u32(self.length)
        write.u8(self.laps)
        write.u8(self.parts)
        write.u16(0)  # pad
        write.u32(0)  # bank_id (runtime)


@dataclass
class CircuitScript:
    infos: list[CircuitInfo] = field(default_factory=list)

    def read(self, read: BinaryReader) -> None:
        info_data = bytearray(140)
        for _ in range(read.u32()):
            # Read info.
            if read.file.readinto(info_data) != len(info_data):  # type: ignore
                raise OSError("Could not read complete info.")
            # Decipher info.
            for i in range(len(info_data)):
                info_data[i] ^= 0x50
            # Deserialize info.
            with BinaryReader(io.BytesIO(info_data)) as info_read:
                self.infos.append(info_read.any(CircuitInfo))

    def write(self, write: BinaryWriter) -> None:
        info_data = bytearray(140)
        with BinaryWriter(io.BytesIO()) as info_write:
            write.u32(len(self.infos))
            for info in self.infos:
                # Serialize info.
                info_write.file.seek(0)
                info_write.any(info)
                info_write.file.seek(0)
                if info_write.file.readinto(info_data) != len(info_data):  # type: ignore
                    raise OSError("Could not write complete info.")
                # Encipher info.
                for i in range(len(info_data)):
                    info_data[i] ^= 0x50
                # Write info.
                write.bytes(info_data)


@dataclass
class VehicleInfo:
    name: str = ""
    vehicle_name: str = ""
    tga_name: str = ""
    small_e_name: str = ""
    small_a_name: str = ""

    def read(self, read: BinaryReader) -> None:
        self.name = read.strbytes(64)
        self.vehicle_name = read.strbytes(20)
        self.tga_name = read.strbytes(13)
        self.small_e_name = read.strbytes(13)
        self.small_a_name = read.strbytes(13)
        read.u8()  # pad
        read.u32()  # pad

    def write(self, write: BinaryWriter) -> None:
        write.strbytes(self.name, 64)
        write.strbytes(self.vehicle_name, 20)
        write.strbytes(self.tga_name, 13)
        write.strbytes(self.small_e_name, 13)
        write.strbytes(self.small_a_name, 13)
        write.u8(0)  # pad
        write.u32(0)  # pad


@dataclass
class VehicleScript:
    infos: list[VehicleInfo] = field(default_factory=list)

    def read(self, read: BinaryReader) -> None:
        info_data = bytearray(128)
        for _ in range(read.u32()):
            # Read info.
            if read.file.readinto(info_data) != len(info_data):  # type: ignore
                raise OSError("Could not read complete info.")
            # Decipher info.
            for i in range(len(info_data)):
                info_data[i] ^= 0x68
            # Deserialize info.
            with BinaryReader(io.BytesIO(info_data)) as info_read:
                self.infos.append(info_read.any(VehicleInfo))

    def write(self, write: BinaryWriter) -> None:
        info_data = bytearray(128)
        with BinaryWriter(io.BytesIO()) as info_write:
            write.u32(len(self.infos))
            for info in self.infos:
                # Serialize info.
                info_write.file.seek(0)
                info_write.any(info)
                info_write.file.seek(0)
                if info_write.file.readinto(info_data) != len(info_data):  # type: ignore
                    raise OSError("Could not write complete info.")
                # Encipher info.
                for i in range(len(info_data)):
                    info_data[i] ^= 0x68
                # Write info.
                write.bytes(info_data)
