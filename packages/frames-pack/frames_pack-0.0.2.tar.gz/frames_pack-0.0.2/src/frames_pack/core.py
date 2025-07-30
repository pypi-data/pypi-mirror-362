from __future__ import annotations

import json
import os
from enum import Enum
from pathlib import Path
from typing import List, Union

import msgpack
import msgspec
import numpy as np
import zstd
from loguru import logger
from pybind11_geobuf import geojson

_COMPRESS_LEVEL = int(os.getenv("FRAMES_PACK_ZSTD_COMPRESSION_LEVEL", "22"))


class FramesPackHeader(msgspec.Struct, kw_only=True):
    version: tuple[int, int, int] = (0, 0, 1)

    def export(self, meta_length: int) -> bytes:
        nums = [*self.version, meta_length]
        nums = np.array(nums, dtype=np.int32)
        header = b"FramesPack" + nums.tobytes()
        assert len(header) == 26
        return header


class FramesPackMeta(msgspec.Struct, kw_only=True):
    frames: list[dict] = msgspec.field(default_factory=list)
    properties: dict = msgspec.field(default_factory=dict)

    def to_bytes(self, lengths: list[tuple[int, int, int]]) -> bytes:
        frames = []
        offset = 0
        for frame, (meta_len, feats_len, props_len) in zip(self.frames, lengths):
            frames.append(
                {
                    **frame,
                    "offset": offset,
                    "lengths": [meta_len, feats_len, props_len],
                }
            )
            offset += meta_len + feats_len + props_len
        meta = {
            "frames": frames,
            "properties": self.properties,
            "frames_length": offset,
        }
        data = msgpack.packb(meta)
        return zstd.compress(data, _COMPRESS_LEVEL)

    def export_json(self) -> dict:
        """
        human readable, only for debug
        """
        return {
            "frames": [
                {k: str(v) if isinstance(v, (list, dict)) else v for k, v in f.items()}
                for f in self.frames
            ],
            "properties": self.properties,
        }


class GeoJSONGeometryType(Enum):
    POINT = "Point"
    MULTI_POINT = "MultiPoint"
    LINE_STRING = "LineString"
    MULTI_LINE_STRING = "MultiLineString"
    POLYGON = "Polygon"
    MULTI_POLYGON = "MultiPolygon"

    @staticmethod
    def from_geometry(geom: geojson.Geometry) -> GeoJSONGeometryType:
        if geom.is_point():
            return GeoJSONGeometryType.POINT
        if geom.is_line_string():
            return GeoJSONGeometryType.LINE_STRING
        if geom.is_multi_line_string():
            return GeoJSONGeometryType.MULTI_LINE_STRING
        if geom.is_multi_point():
            return GeoJSONGeometryType.MULTI_POINT
        if geom.is_polygon():
            return GeoJSONGeometryType.POLYGON
        if geom.is_multi_polygon():
            return GeoJSONGeometryType.MULTI_POLYGON
        err = f"unknown geometry type: {geom.type()}"
        raise ValueError(err)


"""
Point -> [x, y]
LineString -> [[x, y], [x, y], ...]
MultiLineString -> [[[x, y], [x, y], ...], [[x, y], [x, y], ...], ...]
MultiPoint -> [[x, y], [x, y], ...]
Polygon -> [[[x, y], [x, y], ...], [[x, y], [x, y], ...], ...]
MultiPolygon -> [[[[x, y], [x, y], ...], [[x, y], [x, y], ...], ...], [[[x, y], [x, y], ...], [[x, y], [x, y], ...], ...], ...]
"""
GeoJSONGeometryCoordsType = Union[
    List[float],  # Point
    List[List[float]],  # MultiPoint, LineString
    List[List[List[float]]],  # MultiLineString, Polygon
    List[List[List[List[float]]]],  # MultiPolygon
]


class FramesPackFeature(msgspec.Struct, kw_only=True):
    """
    类似 geojson.Feature，把 properties 下和渲染样例相关的属性隔离开。
    导出时，每帧的 features 包含 geometry + 渲染属性，导出为 geobuf，
        其它的属性合并为 list[properties]，导出到 msgpack。
    """

    # 基本属性和几何
    feature_type: str
    feature_id: str
    geom_type: GeoJSONGeometryType
    coordinates: GeoJSONGeometryCoordsType
    # 渲染样式相关，https://github.com/mapbox/simplestyle-spec/tree/master/1.1.0
    stroke: str = "#555555"
    stroke_opacity: float = 1.0
    stroke_width: float = 2.0
    fill: str = "#cc0000"
    fill_opacity: float = 0.6
    paint: dict | None = None
    """
    在 paint 设置一些样式，比如
        -   图标
        -   是否虚线
        -   是否有向
    }
    """

    # 其它都放到这里
    properties: dict = msgspec.field(default_factory=dict)

    def to_geometry(self) -> geojson.Geometry:
        if self.geom_type == GeoJSONGeometryType.POINT:
            return geojson.Geometry(geojson.Point(self.coordinates))
        if self.geom_type == GeoJSONGeometryType.LINE_STRING:
            return geojson.Geometry(geojson.LineString(self.coordinates))
        if self.geom_type == GeoJSONGeometryType.MULTI_LINE_STRING:
            if isinstance(self.coordinates[0][0], (int, float, np.number)):
                coords = [self.coordinates]
            else:
                coords = self.coordinates
            geom = geojson.MultiLineString()
            for ls in coords:
                geom.append(geojson.LineString(ls))
            return geojson.Geometry(geom)
        if self.geom_type == GeoJSONGeometryType.MULTI_POINT:
            return geojson.Geometry(geojson.MultiPoint(self.coordinates))
        if self.geom_type == GeoJSONGeometryType.POLYGON:
            if isinstance(self.coordinates[0][0], (int, float, np.number)):
                coords = [self.coordinates]
            else:
                coords = self.coordinates
            geom = geojson.Polygon()
            for ring in coords:
                geom.append(geojson.LinearRing().from_numpy(ring))
            return geojson.Geometry(geom)
        if self.geom_type == GeoJSONGeometryType.MULTI_POLYGON:
            if isinstance(self.coordinates[0][0], (int, float, np.number)):
                coords = [[self.coordinates]]
            elif isinstance(self.coordinates[0][0][0], (int, float, np.number)):
                coords = [self.coordinates]
            else:
                coords = self.coordinates
            geom = geojson.MultiPolygon()
            for polygon in coords:
                poly = geojson.Polygon()
                for ring in polygon:
                    poly.append(geojson.LinearRing().from_numpy(ring))
                geom.append(poly)
            return geojson.Geometry(geom)
        return geojson.Geometry()

    def to_feature(self):
        f = geojson.Feature()
        f.geometry(self.to_geometry())
        props = f.properties()
        props["feature_type"] = self.feature_type
        props["feature_id"] = self.feature_id
        props["stroke"] = self.stroke
        props["stroke-opacity"] = self.stroke_opacity
        props["stroke-width"] = self.stroke_width
        props["fill"] = self.fill
        props["fill-opacity"] = self.fill_opacity
        paint = self.paint
        if paint:
            props["paint"] = paint
        return f

    @staticmethod
    def from_feature(
        feature: geojson.Feature, properties: dict | None = None
    ) -> FramesPackFeature:
        props = feature.properties()
        ftype = props["feature_type"]() if "feature_type" in props else ""
        fid = props["feature_id"]() if "feature_id" in props else ""
        f = FramesPackFeature(
            feature_type=ftype,
            feature_id=fid,
            geom_type=GeoJSONGeometryType.from_geometry(feature.geometry()),
            coordinates=feature.geometry()()["coordinates"],
        )
        if "stroke" in props:
            f.stroke = props["stroke"]()
        if "stroke-opacity" in props:
            f.stroke_opacity = props["stroke-opacity"]()
        if "stroke-width" in props:
            f.stroke_width = props["stroke-width"]()
        if "fill" in props:
            f.fill = props["fill"]()
        if "fill-opacity" in props:
            f.fill_opacity = props["fill-opacity"]()
        if "paint" in props:
            f.paint = props["paint"]()
        if properties:
            f.properties.update(properties)
        return f

    def export_json(self) -> dict:
        """
        human readable, only for debug
        """

        def strip_z(coords):
            if not len(coords):
                return []
            if not isinstance(coords[0], (int, float, np.number)):
                return [strip_z(c) for c in coords]
            return coords[:2]

        return {
            "feature_type": self.feature_type,
            "feature_id": self.feature_id,
            "geom_type": self.geom_type.value,
            "coordinates": str(strip_z(self.coordinates)),
            "stroke": self.stroke,
            "stroke_opacity": self.stroke_opacity,
            "stroke_width": self.stroke_width,
            "fill": self.fill,
            "fill_opacity": self.fill_opacity,
            "paint": self.paint,
            "properties": self.properties,
        }


class FramesPackFrame(msgspec.Struct, kw_only=True):
    meta: dict = msgspec.field(default_factory=dict)
    features: list[FramesPackFeature] = msgspec.field(default_factory=list)

    def to_bytes(self) -> tuple[list[int], bytes]:
        meta = self.__meta_bytes()
        feats = self.__feats_bytes()
        props = self.__props_bytes()
        lengths = [len(meta), len(feats), len(props)]
        data = meta + feats + props
        return lengths, data

    def __meta_bytes(self) -> bytes:
        data = msgpack.packb(self.meta)
        return zstd.compress(data, _COMPRESS_LEVEL)

    def __feats_bytes(self) -> bytes:
        """
        可视化的部分，编译为 geobuf 并压缩
        """

        fc = geojson.FeatureCollection()
        for f in self.features:
            fc.append(f.to_feature())
        data = fc.to_geobuf(precision=3, only_xy=True)
        return zstd.compress(data, _COMPRESS_LEVEL)

    def __props_bytes(self) -> bytes:
        props_list = [f.properties for f in self.features]
        data = msgpack.packb(props_list)
        return zstd.compress(data, _COMPRESS_LEVEL)


class FramesPack(msgspec.Struct, kw_only=True):
    header: FramesPackHeader = msgspec.field(default_factory=FramesPackHeader)
    meta: FramesPackMeta = msgspec.field(default_factory=FramesPackMeta)
    frames: list[FramesPackFrame] = msgspec.field(default_factory=list)
    tail: bytes = b""

    def dump(self, path: str) -> int:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as f:
            logger.info(f"writing to {path} ...")
            data = self.export()
            f.write(data)
            nbytes = len(data)
            logger.info(f"writing to {path} ... DONE (#bytes: {nbytes:,} bytes)")
            logger.info(
                "Tip: you can use `python3 -m frames_pack.compile framespack2json frames_pack.bin` to export human readable text (for debug)"
            )
            return nbytes

    def export(self) -> bytes:
        lengths = []
        frames_data = []
        for f in self.frames:
            frame_lengths, frame_data = f.to_bytes()
            lengths.append(frame_lengths)
            frames_data.append(frame_data)
        meta = self.meta.to_bytes(lengths)
        header = self.header.export(len(meta))
        ret = header + meta
        for frame_data in frames_data:
            ret += frame_data
        if self.tail:
            ret += self.tail
        return ret

    def load(self, path: str) -> FramesPack:
        assert len(self.meta.frames) == len(self.frames) == 0, (
            "FramesPack must be empty before loading"
        )
        with Path(path).open("rb") as f:
            data = f.read()
        # header
        header_length = 26
        header = data[:header_length]
        assert header[:10] == b"FramesPack"
        *version, meta_length = np.frombuffer(header[10:], dtype=np.int32).tolist()
        self.header.version = tuple(version)
        # meta
        offset = header_length
        meta_data = data[offset : offset + meta_length]
        meta = msgpack.unpackb(zstd.decompress(meta_data))
        frames_length = meta["frames_length"]
        self.meta.frames = meta["frames"]
        self.meta.properties = meta["properties"]
        # frames
        offset += meta_length
        frames_data = data[offset : offset + frames_length]
        for frame in self.meta.frames:
            off = frame["offset"]
            len1, len2, len3 = frame["lengths"]
            f_meta = frames_data[off : off + len1]
            off += len1
            f_feats = frames_data[off : off + len2]
            off += len2
            f_props = frames_data[off : off + len3]
            # decode
            f_meta = msgpack.unpackb(zstd.decompress(f_meta))
            f_feats = geojson.FeatureCollection().from_geobuf(zstd.decompress(f_feats))
            f_props = msgpack.unpackb(zstd.decompress(f_props))
            assert len(f_feats) == len(f_props)
            features = []
            for ff, pp in zip(f_feats, f_props):
                features.append(FramesPackFeature.from_feature(ff, pp))
            f = FramesPackFrame(
                meta=f_meta,
                features=features,
            )
            self.frames.append(f)
        # tail
        offset += frames_length
        self.tail = data[offset:]
        return self

    def export_json(self, path: str | None = None) -> dict | None:
        """
        human readable, only for debug
        """
        ret = {
            "header": {
                "version": str(self.header.version),
            },
            "meta": self.meta.export_json(),
        }
        frames = []
        for f in self.frames:
            frames.append(
                {
                    "meta": f.meta,
                    "features": [f.export_json() for f in f.features],
                }
            )
        ret["frames"] = frames
        if self.tail:
            ret["#tail"] = len(self.tail)
        if not path:
            return ret

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            json.dump(ret, f, indent=4)
        logger.info(f"wrote to {path}")
        return None


__all__ = [
    "FramesPack",
    "FramesPackFeature",
    "FramesPackFrame",
    "FramesPackHeader",
    "FramesPackMeta",
    "GeoJSONGeometryType",
]
