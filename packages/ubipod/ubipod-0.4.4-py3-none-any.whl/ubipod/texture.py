from dataclasses import dataclass, field

from .pbdf import PbdfReader, PbdfWriter


@dataclass
class TextureRegion:
    name: str = ""
    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0
    index: int = 0

    def read(self, read: PbdfReader):
        self.name = read.strbytes(32)
        self.left = read.i32()
        self.top = read.i32()
        self.right = read.i32()
        self.bottom = read.i32()
        self.index = read.i32()

    def write(self, write: PbdfWriter):
        write.strbytes(self.name, 32)
        write.i32(self.left)
        write.i32(self.top)
        write.i32(self.right)
        write.i32(self.bottom)
        write.i32(self.index)


@dataclass
class TextureProject:
    textures: list[list[TextureRegion]] = field(default_factory=list)
    palette: bytes = field(default_factory=lambda: bytes(0))  # RGB888
    texture_pages: list[bytes] = field(default_factory=list)  # RGB565LE or PAL8

    def read(self, read: PbdfReader, texture_size: int) -> None:
        texture_count = read.i32()
        read.i32()  # unused palette count
        self.textures = [[read.any(TextureRegion) for _ in range(read.i32())] for _ in range(texture_count)]
        if read.format.tex_palette:
            self.palette = read.bytes(256 * 3)
        texture_bytes = texture_size * texture_size * read.format.tex_bpp
        self.texture_pages = [read.bytes(texture_bytes) for _ in range(texture_count)]

    def write(self, write: PbdfWriter) -> None:
        write.i32(len(self.textures))
        write.i32(0)
        for texture in self.textures:
            write.i32(len(texture))
            [write.any(region) for region in texture]
        if write.format.tex_palette:
            write.bytes(self.palette)
        [write.bytes(x) for x in self.texture_pages]
