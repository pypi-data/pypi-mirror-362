import enum
import os
import pathlib
import struct
from types import TracebackType
from typing import BinaryIO

from .binary import BinaryReader, BinaryWriter


class PbdfRelease(enum.Enum):
    OEM = enum.auto()
    RETAIL = enum.auto()
    ARCADE = enum.auto()


class PbdfFormat:
    def __init__(self, filename: str, release: PbdfRelease = PbdfRelease.RETAIL) -> None:
        path = pathlib.Path(filename)
        self.type = path.suffix[2].upper()
        self.version = int(path.suffix[3])
        self.release = release
        # Determine type specific differences.
        if self.type == "L":
            self.buf_size = 0x4000 if self.version < 8 else 0x2400
            self.key = 0x0F7E if self.version < 8 else 0xD13F
            self.ofs_count = 4 if self.release == PbdfRelease.OEM else 10
        elif self.type == "V":
            self.buf_size = 0x4000 if self.version < 8 else 0x1800
            self.key = 0x0F2E if self.version < 8 else 0xEFA9
            self.ofs_count = 1
        # Determine version specific differences.
        if self.version in (4, 7, 9):
            self.voodoo = True
            self.tex_bpp = 2
            self.tex_size_small = 128
            self.tex_palette = False
        else:
            self.voodoo = False
            self.tex_bpp = 1
            self.tex_size_small = 256
            self.tex_palette = True


class PbdfReader(BinaryReader):
    key: int
    buf_size: int
    encoding: str
    ofs: list[int]
    file: BinaryIO
    format: PbdfFormat
    _buf: bytearray
    _buf_index: int
    _buf_pos: int

    def __init__(self, file: BinaryIO, key: int = 0, buf_size: int = 0, encoding: str = "cp1252") -> None:
        super().__init__(file, encoding)
        self.key = key
        self.buf_size = buf_size
        self._buf_index = -1

    def __enter__(self) -> "PbdfReader":
        # Determine file size.
        start = self.file.tell()
        self.file.seek(0, os.SEEK_END)
        file_size = self.file.tell() - start
        self.file.seek(start)

        # Determine key.
        if not self.key:
            self.key = struct.unpack("<I", self.file.read(4))[0] ^ file_size
            self.file.seek(start)

        # Determine buffer size.
        if not self.buf_size:
            checksum = 0
            pos = start
            while pos < file_size:
                dword = struct.unpack("<I", self.file.read(4))[0]
                pos = self.file.tell()
                if dword == checksum and file_size % pos == 0:
                    self.buf_size = pos
                    self.file.seek(start)
                    break
                checksum += dword ^ self.key
                checksum &= 0xFFFFFFFF
            if not self.buf_size:
                raise OSError("Could not determine PBDF buffer size.")
        self._buf = bytearray(self.buf_size)
        self._buf_pos = self.buf_size

        # Read header.
        if self.u32() != file_size:
            raise OSError("Bad PBDF file size.")
        self.ofs = [self.u32() for _ in range(self.u32())]
        return self

    def offset(self, idx: int) -> None:
        # Seek to offset.
        offset = self.ofs[idx]
        # Update buffer status.
        buf_index = offset // self.buf_size
        if buf_index == self._buf_index:
            self._buf_pos = offset % self.buf_size
        else:
            self._buf_index = buf_index
            self._buf_pos = self.buf_size
            self.file.seek(self._buf_index * self.buf_size)

    def bytes(self, count: int) -> bytearray:
        result = bytearray(count)
        pos = 0
        while pos < count:
            bytes_remain = self.buf_size - 4 - self._buf_pos
            if bytes_remain > 0:
                size = min(bytes_remain, count - pos)
                result[pos:pos + size] = self._buf[self._buf_pos:self._buf_pos + size]
                pos += size
                self._buf_pos += size
            else:
                self._read_buf()
        return result

    def _read_buf(self) -> None:
        self._buf_index += 1
        self._buf_pos = 0
        if self.file.readinto(self._buf) != self.buf_size:  # type: ignore
            raise OSError("Could not read complete PBDF buffer.")

        # Decrypt buffer.
        i = 0
        checksum = 0
        if self._buf_index and self.key in [0x5CA8, 0xD13F]:
            # Special cipher for specific keys in second and later blocks.
            prev = 0
            for i in range(0, self.buf_size - 4, 4):
                cmd = prev >> 16 & 3
                dec = 0
                if cmd == 0:
                    dec = (prev - 0x50A4A89D)
                elif cmd == 1:
                    dec = (0x3AF70BC4 - prev)
                elif cmd == 2:
                    dec = (prev + 0x07091971) << 1
                elif cmd == 3:
                    dec = (0x11E67319 - prev) << 1
                enc = struct.unpack_from("<I", self._buf, i)[0]
                cmd = prev & 3
                if cmd == 0:
                    dec = ~enc ^ dec
                elif cmd == 1:
                    dec = ~enc ^ ~dec
                elif cmd == 2:
                    dec = enc ^ ~dec
                elif cmd == 3:
                    dec = enc ^ dec ^ 0xFFFF
                dec &= 0xFFFFFFFF
                struct.pack_into("<I", self._buf, i, dec)
                checksum += dec
                checksum &= 0xFFFFFFFF
                prev = enc
        else:
            # Simple cipher for most keys in all blocks.
            for i in range(0, self.buf_size - 4, 4):
                enc = struct.unpack_from("<I", self._buf, i)[0]
                dec = enc ^ self.key
                struct.pack_into("<I", self._buf, i, dec)
                checksum += dec
                checksum &= 0xFFFFFFFF
        # Validate the checksum.
        if checksum != struct.unpack_from("<I", self._buf, i + 4)[0]:
            raise OSError("Bad PBDF buffer checksum.")


class PbdfWriter(BinaryWriter):
    key: int
    buf_size: int
    crypt_tail: bool
    format: PbdfFormat
    _buf: bytearray
    _buf_pos: int
    _ofs_count: int
    _ofs: list[int]

    def __init__(self, file: BinaryIO, key: int, buf_size: int, ofs_count: int, encoding: str = "cp1252",
                 crypt_tail: bool = True) -> None:
        super().__init__(file, encoding)
        self.key = key
        self.buf_size = buf_size
        self._ofs_count = ofs_count
        self._ofs = []
        self.crypt_tail = crypt_tail

    def __enter__(self) -> "PbdfWriter":
        # Initialize buffering and reserve header.
        self._buf = bytearray(self.buf_size)
        self._buf_pos = 4 + 4 + 4 * self._ofs_count
        return self

    def __exit__(self, type: type[BaseException] | None, value: BaseException | None, traceback: TracebackType | None) -> None:
        if len(self._ofs) != self._ofs_count:
            super().__exit__(type, value, traceback)
            raise OSError(f"{self._ofs_count - len(self._ofs)} PBDF offsets have not been satisfied.")

        # Write a pending buffer.
        data_size = self.file.tell() + self._buf_pos
        if self._buf_pos > 0:
            self._write_buf()

        # Update header.
        file_size = self.file.tell()
        self.file.seek(0)
        self.file.write(struct.pack("<I", file_size))
        self.file.write(struct.pack("<I", self._ofs_count))
        self.file.write(struct.pack(f"<{self._ofs_count}I", *self._ofs))

        # Enrypt buffers.
        self.file.seek(0)
        for buf_index in range(file_size // self.buf_size):
            self.file.readinto(self._buf)  # type: ignore
            i = 0
            checksum = 0
            if buf_index and self.key in [0x5CA8, 0xD13F]:
                # Special cipher for specific keys in second and later blocks.
                prev = 0
                for i in range(0, self.buf_size - 4, 4):
                    dec = struct.unpack_from("<I", self._buf, i)[0]
                    if self.crypt_tail or buf_index * self.buf_size + i < data_size:
                        cmd = prev >> 16 & 3
                        enc = 0
                        if cmd == 0:
                            enc = (prev - 0x50A4A89D)
                        elif cmd == 1:
                            enc = (0x3AF70BC4 - prev)
                        elif cmd == 2:
                            enc = (prev + 0x07091971) << 1
                        elif cmd == 3:
                            enc = (0x11E67319 - prev) << 1
                        cmd = prev & 3
                        if cmd == 0:
                            enc = ~dec ^ enc
                        elif cmd == 1:
                            enc = ~dec ^ ~enc
                        elif cmd == 2:
                            enc = dec ^ ~enc
                        elif cmd == 3:
                            enc = dec ^ enc ^ 0xFFFF
                        enc &= 0xFFFFFFFF
                        struct.pack_into("<I", self._buf, i, enc)
                        prev = enc
                    else:
                        dec ^= self.key
                    checksum += dec
                    checksum &= 0xFFFFFFFF
            else:
                # Simple cipher for most keys in all blocks.
                for i in range(0, self.buf_size - 4, 4):
                    dec = struct.unpack_from("<I", self._buf, i)[0]
                    if self.crypt_tail or buf_index * self.buf_size + i < data_size:
                        struct.pack_into("<I", self._buf, i, dec ^ self.key)
                    else:
                        dec ^= self.key
                    checksum += dec
                    checksum &= 0xFFFFFFFF
            # Write the checksum and buffer.
            struct.pack_into("<I", self._buf, i + 4, checksum)
            self.file.seek(-self.buf_size, os.SEEK_CUR)
            self.file.write(self._buf)

        super().__exit__(type, value, traceback)

    def offset(self) -> None:
        if len(self._ofs) == self._ofs_count:
            raise OSError("No more PBDF offsets available.")
        self._ofs.append(self.file.tell() + self._buf_pos)

    def bytes(self, value: bytes) -> None:
        pos = 0
        while pos < len(value):
            bytes_remain = self.buf_size - 4 - self._buf_pos
            if bytes_remain > 0:
                size = min(bytes_remain, len(value) - pos)
                self._buf[self._buf_pos:self._buf_pos + size] = value[pos:pos + size]
                pos += size
                self._buf_pos += size
            else:
                self._write_buf()

    def _write_buf(self) -> None:
        # Simply write raw data, checksum and encryption must be done on close.
        self.file.write(self._buf)
        self._buf_pos = 0
