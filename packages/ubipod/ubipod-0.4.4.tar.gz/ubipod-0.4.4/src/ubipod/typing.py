mat33 = tuple[float, ...]
vec2 = tuple[float, ...]
vec2i32 = tuple[int, ...]
vec3 = tuple[float, ...]


def mat33_new() -> mat33:
    return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0


def vec2_new() -> vec2:
    return 0.0, 0.0


def vec3_new() -> vec3:
    return 0.0, 0.0, 0.0
