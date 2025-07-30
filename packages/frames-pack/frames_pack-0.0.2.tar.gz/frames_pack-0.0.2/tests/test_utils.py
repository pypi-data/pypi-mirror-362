from __future__ import annotations

from pathlib import Path

import numpy as np
import zstd

from frames_pack.compile import geojson2framespack, rosbag2framespack
from frames_pack.core import (
    _COMPRESS_LEVEL,
    FramesPack,
    FramesPackFeature,
    GeoJSONGeometryType,
)
from frames_pack.treepack import TreeNode, treepack

PWD = Path(__file__).parent.absolute()
TEST_FILE = Path(__file__).name
PROJECT_SOURCE_DIR = PWD.parent


def test_rosbag2framespack():
    path = f"{PROJECT_SOURCE_DIR}/data/65ce63c95fbf245fbffd97419d48af2e.bag"
    fp = rosbag2framespack(path)
    output_bin = f"{PROJECT_SOURCE_DIR}/build/test_rosbag2framespack.bin"
    fp.dump(output_bin)

    output_json1 = f"{PROJECT_SOURCE_DIR}/build/test_rosbag2framespack1.json"
    fp.export_json(output_json1)

    fp = FramesPack().load(output_bin)
    output_json2 = f"{PROJECT_SOURCE_DIR}/build/test_rosbag2framespack2.json"
    fp.export_json(output_json2)


def test_geojson2framespack():
    path = f"{PROJECT_SOURCE_DIR}/data/cloverleaf.pbf.json"
    fp = geojson2framespack(path)
    path1 = f"{PROJECT_SOURCE_DIR}/build/test_geojson2framespack.bin"
    nbytes1 = fp.dump(path1)

    # test tail（你可以按需自己编码这部分数据）
    fp.tail = b"hello world"
    path2 = f"{PROJECT_SOURCE_DIR}/build/test_geojson2framespack_with_tail.bin"
    nbytes2 = fp.dump(path2)
    assert nbytes1 + len(fp.tail) == nbytes2

    fp = FramesPack().load(path2)
    path3 = f"{PROJECT_SOURCE_DIR}/build/test_geojson2framespack.json"
    fp.export_json(path3)


def test_framespack_feature():
    kwargs = dict(  # noqa: C408
        feature_type="",
        feature_id="",
        properties={},
    )
    # Point
    f = FramesPackFeature(
        **kwargs,
        geom_type=GeoJSONGeometryType.POINT,
        coordinates=[1.2, 3.4],
    )
    assert f.to_geometry()()["coordinates"][:2] == [1.2, 3.4]
    f = FramesPackFeature(
        **kwargs,
        geom_type=GeoJSONGeometryType.POINT,
        coordinates=[1.2, 3.4, 5.6],
    )
    assert f.to_geometry()()["coordinates"] == [1.2, 3.4, 5.6]
    f = FramesPackFeature(
        **kwargs,
        geom_type=GeoJSONGeometryType.POINT,
        coordinates=np.array(
            [1.2, 3.4],
        ),
    )
    assert f.to_geometry()()["coordinates"][:2] == [1.2, 3.4]

    # MultiPoint
    coords = [[1.2, 3.4], [5.6, 7.8]]
    f = FramesPackFeature(
        **kwargs,
        geom_type=GeoJSONGeometryType.MULTI_POINT,
        coordinates=coords,
    )
    assert f.to_geometry()()["coordinates"] == [[1.2, 3.4, 0.0], [5.6, 7.8, 0.0]]
    # LineString
    coords = [[1.2, 3.4], [5.6, 7.8]]
    f = FramesPackFeature(
        **kwargs,
        geom_type=GeoJSONGeometryType.LINE_STRING,
        coordinates=coords,
    )
    assert f.to_geometry()()["coordinates"] == [[1.2, 3.4, 0.0], [5.6, 7.8, 0.0]]
    # MultiLineString
    coords = [[[1.2, 3.4], [5.6, 7.8]], [[2.3, 4.5], [6.7, 8.9]]]
    f = FramesPackFeature(
        **kwargs,
        geom_type=GeoJSONGeometryType.MULTI_LINE_STRING,
        coordinates=coords,
    )
    assert f.to_geometry()()["coordinates"] == [
        [[1.2, 3.4, 0.0], [5.6, 7.8, 0.0]],
        [[2.3, 4.5, 0.0], [6.7, 8.9, 0.0]],
    ]
    f = FramesPackFeature(
        **kwargs,
        geom_type=GeoJSONGeometryType.MULTI_LINE_STRING,
        coordinates=coords[0],  # ok if only one line_string (not nested)
    )
    assert f.to_geometry()()["coordinates"] == [[[1.2, 3.4, 0.0], [5.6, 7.8, 0.0]]]

    # Polygon
    A = [0, 0, 0]
    B = [10, 0, 0]
    C = [10, 10, 0]
    a = [1, 1, 0]
    b = [2, 1, 0]
    c = [2, 2, 0]
    ring0 = [A, B, C, A]
    ring1 = [a, b, c, a]
    coords = [ring0, ring1]
    f = FramesPackFeature(
        **kwargs,
        geom_type=GeoJSONGeometryType.POLYGON,
        coordinates=coords,
    )
    assert f.to_geometry()()["coordinates"] == coords
    f = FramesPackFeature(
        **kwargs,
        geom_type=GeoJSONGeometryType.POLYGON,
        coordinates=coords[0],
    )
    assert f.to_geometry()()["coordinates"] == coords[:1]

    # Polygon
    polygon = [ring0, ring1]
    coords = [polygon]
    f = FramesPackFeature(
        **kwargs,
        geom_type=GeoJSONGeometryType.MULTI_POLYGON,
        coordinates=coords,
    )
    assert f.to_geometry()()["coordinates"] == coords
    f = FramesPackFeature(
        **kwargs,
        geom_type=GeoJSONGeometryType.MULTI_POLYGON,
        coordinates=polygon,
    )
    assert f.to_geometry()()["coordinates"] == [polygon]
    f = FramesPackFeature(
        **kwargs,
        geom_type=GeoJSONGeometryType.MULTI_POLYGON,
        coordinates=ring0,
    )
    assert f.to_geometry()()["coordinates"] == [[ring0]]


def test_treepack():
    tree = {
        "file1.txt": TreeNode("file1.txt", "hello world"),
        "key1": "value1",
        "key2": "value2",
        "subdir": {
            "key3": "value3",
            "file2.json": TreeNode("file2.json", {"hello": "world"}),
            "file3.bin": TreeNode("file3.bin", b"hello world", "summary of file3.bin"),
        },
    }
    output = b""
    nodes = []

    def writer(node: TreeNode):
        nonlocal output
        data = node.content
        data = zstd.compress(data, _COMPRESS_LEVEL)
        output += data
        nonlocal nodes
        nodes.append(node)
        return len(data)

    offset, index = treepack(tree, writer)
    assert len(nodes) == 3
    assert len(output) == offset

    range_list = []

    def unpack_tree(tree: dict) -> dict:
        for _, value in tree.items():
            if not isinstance(value, dict):
                continue
            if "range" in value:
                range_list.append(value["range"])
                value["range"] = "</>"
                continue
            unpack_tree(value)
        return tree

    index = unpack_tree(index)
    assert index == {
        "file1.txt": {"range": "</>"},
        "key1": "value1",
        "key2": "value2",
        "subdir": {
            "key3": "value3",
            "file2.json": {"range": "</>"},
            "file3.bin": {"range": "</>", "summary": "summary of file3.bin"},
        },
    }
    assert len(range_list) == len(nodes)
    for (s, e), n in zip(range_list, nodes):
        d0 = n.content
        d1 = zstd.decompress(output[s:e])
        assert d0 == d1


if __name__ == "__main__":
    from utilities import pytest_main

    pytest_main(PWD, test_file=TEST_FILE)
