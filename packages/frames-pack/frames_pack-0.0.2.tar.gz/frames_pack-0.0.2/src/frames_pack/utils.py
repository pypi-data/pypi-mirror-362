from __future__ import annotations

from pathlib import Path

import numpy as np
from loguru import logger
from scipy.interpolate import interp1d


def help(
    *,
    module_name: str,
    source_dir: str,
    ignores: set[str],
    ignore_docs: bool = False,
):
    logging = logger.bind(format="{message}").opt(raw=True, colors=True)
    files = sorted(
        [
            f.name
            for f in Path(source_dir).iterdir()
            if f.name.endswith(".py") and f.name not in ignores
        ]
    )
    logging.info(f"{module_name}:\n")
    for i, f in enumerate(files):
        logging.info(
            f"\t{i:3d}:\tpython3 -m {module_name}.{f[: f.index('.')]} --help\n"
        )
    if not ignore_docs:
        doc_url = "TODO"

        logging.info("\n===== Frames Pack =====\n\n  - ")
        logging.info(
            "\n  - ".join(
                [
                    f"文档: {doc_url}",
                    "安装方法: python3 -m pip install frames-pack -U",
                ]
            )
        )
        logging.info("\n")


def interp_func_for_seq(
    sequence: np.ndarray,
    *,
    kind: str = "linear",
    fill_value: str = "extrapolate",
):
    assert len(sequence) >= 2, f"invalid seq, #seq: {len(sequence)}"
    sequence = np.array(sequence)
    sequence.flags.writeable = False
    indices = np.arange(len(sequence))
    interp_func = interp1d(sequence, indices, kind=kind, fill_value=fill_value)
    interp_func.sequence = sequence

    def idx_t(source: np.ndarray | float | list[float]):
        single = False
        if isinstance(source, (int, float, np.number)):
            source = [source]
            single = True
        source = np.asarray(source)
        interpolated = interp_func(source)
        base = np.floor(np.clip(interpolated, 0, len(sequence) - 2)).astype(int)
        frac = interpolated - base
        if single:
            return base[0], frac[0]
        return base, frac

    interp_func.idx_t = idx_t

    return interp_func


def yaw2matrix(yaw: float) -> np.ndarray:
    T_local2world = np.eye(2)
    c, s = np.cos(yaw), np.sin(yaw)
    T_local2world[:, 0] = [c, s]
    T_local2world[:, 1] = [-s, c]
    return T_local2world


def object_to_json(obj: dict | list) -> dict | list:
    if hasattr(obj, "items") and callable(obj.items):
        ret = {}
        for k, v in obj.items():
            if not isinstance(k, str):
                k = str(k)  # noqa: PLW2901
            ret[k] = object_to_json(v)
        return ret
    if isinstance(obj, str):
        return obj
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if hasattr(obj, "__iter__") or hasattr(obj, "__getitem__"):
        return [object_to_json(e) for e in obj]
    return obj


def normalize_yaw(yaw: float) -> float:
    return float((yaw + np.pi) % (2 * np.pi) - np.pi)


def interpolate_yaw(yaw1: float, yaw2: float, t: float) -> float:
    """
    Interpolate between two yaw angles, ensuring the shortest path around the unit circle.

    Args:
        yaw1 (float): First yaw angle in radians (will be normalized to range [-π, π])
        yaw2 (float): Second yaw angle in radians (will be normalized to range [-π, π])
        t (float): Interpolation factor between 0 and 1

    Returns:
        float: Interpolated yaw angle in radians, normalized to range [-π, π]
    """
    # Normalize input angles to ensure they're in range [-π, π]
    yaw1 = normalize_yaw(yaw1)
    yaw2 = normalize_yaw(yaw2)

    # Calculate the difference between angles
    diff = yaw2 - yaw1

    # Normalize the difference to ensure shortest path
    # If diff > π, going the other way around is shorter
    if diff > np.pi:
        diff -= 2 * np.pi
    # If diff < -π, going the other way around is shorter
    elif diff < -np.pi:
        diff += 2 * np.pi

    # Interpolate and normalize the result
    result = yaw1 + t * diff
    return normalize_yaw(result)


def gps2local(
    coords,
    anchor: tuple[float, float],
    k: tuple[float, float],
    cos: float = 1.0,
    sin: float = 0.0,
):
    if not len(coords):
        return []
    if not isinstance(coords[0], (int, float, np.number)):
        return [gps2local(c, anchor, k, cos, sin) for c in coords]
    x, y, *z = coords
    x = (x - anchor[0]) * k[0]
    y = (y - anchor[1]) * k[1]
    x = cos * x - sin * y
    y = sin * x + cos * y
    return [x, y, *z]


if __name__ == "__main__":
    import fire

    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire()
