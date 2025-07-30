from dataclasses import dataclass, field

from .binary import BinaryReader, BinaryWriter


@dataclass
class Image:
    width: int = 0
    height: int = 0
    id: int = 0
    ptr: int = 0
    palette: int = -1

    def read(self, read: BinaryReader) -> None:
        self.width = read.u16()
        self.height = read.u16()
        self.id = read.u32()
        self.ptr = read.u32()
        self.palette = read.i16()
        read.u16()

    def write(self, write: BinaryWriter) -> None:
        write.u16(self.width)
        write.u16(self.height)
        write.u32(self.id)
        write.u32(self.ptr)
        write.i16(self.palette)
        write.u16(0)


@dataclass
class ImageFile:
    images: list[Image] = field(default_factory=list)
    palettes: list[bytes] = field(default_factory=list)  # RGB555LE
    data: bytes = field(default_factory=lambda: bytes(0))  # RGB555LE or PAL8

    def read(self, read: BinaryReader) -> None:
        image_count = read.u32()
        data_size = read.u32()
        palette_count = read.u32()
        self.images = [read.any(Image) for _ in range(image_count)]
        self.palettes = [read.bytes(256 * 2) for _ in range(palette_count)]
        self.data = read.bytes(data_size)

    def write(self, write: BinaryWriter) -> None:
        write.u32(len(self.images))
        write.u32(len(self.data))
        write.u32(len(self.palettes))
        [write.any(x) for x in self.images]
        [write.bytes(x) for x in self.palettes]
        write.bytes(self.data)
