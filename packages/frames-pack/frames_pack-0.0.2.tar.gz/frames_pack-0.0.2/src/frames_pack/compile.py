from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from typing import Callable

import numpy as np
import rosbag
from loguru import logger
from pybind11_geobuf import geojson, tf
from tqdm import tqdm

from frames_pack.core import (
    FramesPack,
    FramesPackFeature,
    FramesPackFrame,
    GeoJSONGeometryType,
)
from frames_pack.utils import (
    gps2local,
    interp_func_for_seq,
    interpolate_yaw,
    object_to_json,
    yaw2matrix,
)


def rosbag2framespack(bag_path: str) -> FramesPack:
    assert Path(bag_path).exists(), f"missing rosbag file: {bag_path}"
    rear_axle_to_center: float = 1.3545
    landmark_topics: tuple[str, ...] = (
        (
            "/ddld/landmark_navi",
            "/ddld/landmark",
        ),
    )
    object_topics: tuple[str, ...] = (
        "/perception/fusion/object_auto",
        "/perception/fusion/object",
    )
    with rosbag.Bag(bag_path, "r") as bag:
        egos = []
        topics = ["/mla/egopose"]
        logger.info(f"reading topics={topics}...")
        msgs = list(bag.read_messages(topics, raw=True))
        for _, msg, ts in tqdm(msgs, "parsing egoposes..."):
            msg = msg[-1]().deserialize(msg[1])  # noqa: PLW2901
            yaw_enu = msg.orientation.euler_global.yaw
            yaw_boot = msg.orientation.euler_local.yaw
            pos = msg.position.position_global
            pos_lla = [pos.longitude, pos.latitude]
            pos = msg.position.position_local
            pos_boot = [pos.x, pos.y]
            if rear_axle_to_center != 0.0:
                # 自车基准调整到车体中心
                T_ego2enu = yaw2matrix(yaw_enu)
                dx, dy = T_ego2enu @ [rear_axle_to_center, 0]
                lon, lat = tf.enu2lla([[dx, dy, 0.0]], anchor_lla=[*pos_lla, 0.0])[
                    0, :2
                ]
                pos_lla = [lon, lat]
                T_ego2boot = yaw2matrix(yaw_boot)
                dx, dy = T_ego2boot @ [rear_axle_to_center, 0]
                pos_boot[0] += dx
                pos_boot[1] += dy

            storage_ts = ts.secs + ts.nsecs / 1e9
            sensor_ts = msg.meta.timestamp_us / 1e6
            ego = {
                "ts": sensor_ts,
                "pos": pos_lla,
                "yaw": yaw_enu,
                "storage_ts": storage_ts,
                "pos_boot": pos_boot,
                "yaw_boot": yaw_boot,
            }
            egos.append(ego)
        __interp = __interp_func_for_egos(egos)

        @lru_cache(maxsize=None)
        def interp(ts: float) -> dict:
            return __interp(ts)

        frames = defaultdict(list)
        topics = list(landmark_topics)
        logger.info(f"reading topics={topics}...")
        msgs = []
        for topic in topics:
            msgs = list(bag.read_messages(topic, raw=True))
            if msgs:
                break
        if not msgs:
            logger.error("no landmark (LD) input")
        for _, msg, _ in tqdm(msgs, "parsing landmarks..."):
            msg = msg[-1]().deserialize(msg[1])  # noqa: PLW2901
            sensor_ts = msg.meta.sensor_timestamp_us / 1e6
            features = frames[sensor_ts]
            LSs = {
                "LB": msg.landmarks.lane_boundaries,
                "RB": msg.landmarks.road_boundaries,
            }
            strokes = {
                "LB": "#00FFFF",
                "RB": "#FFA500",
            }
            for line_type, lines in LSs.items():
                stroke = strokes[line_type]
                for idx, line in enumerate(lines):
                    pts_ego = [[pt.x, pt.y] for pt in line.line_points]
                    if rear_axle_to_center != 0.0:
                        pts_ego = [[x - rear_axle_to_center, y] for x, y in pts_ego]
                    f = FramesPackFeature(
                        feature_type=f"{line_type}",
                        feature_id=f"{line_type}/#{idx}/id={line.track_id.id}",
                        geom_type=GeoJSONGeometryType.LINE_STRING,
                        coordinates=pts_ego,
                        stroke=stroke,
                    )
                    line_width = getattr(line, "line_width", None)
                    if line_width is not None:
                        f.stroke_width = round(f.stroke_width * line_width / 0.15, 2)
                    features.append(f)

        topics = list(object_topics)
        logger.info(f"reading topics={topics}...")
        msgs = []
        for topic in topics:
            msgs = list(bag.read_messages(topic, raw=True))
            if msgs:
                break
        if not msgs:
            logger.error("no object (OD) input")
        for _, msg, _ in tqdm(msgs, "parsing objects..."):
            msg = msg[-1]().deserialize(msg[1])  # noqa: PLW2901
            sensor_ts = msg.meta.sensor_timestamp_us / 1e6
            ego = interp(sensor_ts)
            features = frames[sensor_ts]
            objs = msg.perception_fusion_objects_data
            for idx, obj in enumerate(objs):
                pos = [obj.position.x, obj.position.y]
                pos = ego["T_ego2boot"].T @ (pos - ego["pos_boot"])
                f = FramesPackFeature(
                    feature_type="object",
                    feature_id=f"object/#{idx}/id={obj.track_id}",
                    geom_type=GeoJSONGeometryType.POINT,
                    coordinates=pos.tolist(),
                )
                features.append(f)
    fp = FramesPack()
    for ts, features in sorted(frames.items()):
        ego = interp(ts)
        pos, yaw = ego["pos"][:2], ego["yaw"]
        frame_meta = {"ts": ts, "pos": pos, "yaw": yaw}
        fp.meta.frames.append(object_to_json(frame_meta))
        frame = FramesPackFrame(features=features)
        fp.frames.append(frame)
    return fp


def __interp_func_for_egos(egos: list[dict]) -> Callable[[float], dict]:
    assert len(egos) >= 2
    interp = interp_func_for_seq([e["ts"] for e in egos])

    @lru_cache(maxsize=None)
    def interp_ego(ts: float) -> dict:
        idx, t = interp.idx_t(ts)
        ego = {"ts": ts}
        prev = egos[idx]
        curr = egos[idx + 1]
        for k in ["storage_ts"]:
            if k not in prev or k not in curr:
                continue
            v = prev[k] * (1.0 - t) + curr[k] * t
            ego[k] = v
        for k in ["pos", "pos_boot"]:
            v1, v2 = (np.array(o[k]) for o in [prev, curr])
            ego[k] = v1 * (1.0 - t) + v2 * t
        for k in ["yaw", "yaw_boot"]:
            v1, v2 = prev[k], curr[k]
            yaw = interpolate_yaw(v1, v2, t)
            ego[k] = yaw
        ego["T_ego2enu"] = yaw2matrix(ego["yaw"])
        if "yaw_boot" in ego:
            ego["T_ego2boot"] = yaw2matrix(ego["yaw_boot"])
        return ego

    return interp_ego


def geojson2bbox(path: str) -> tuple[float, float, float, float]:
    """
    计算 geojson 文件的 bbox
    """
    fc = geojson.FeatureCollection()
    assert fc.load(path), f"failed to load geojson file: {path}"
    assert len(fc) > 0, f"geojson file must contain at least one feature: {path}"
    xmin, ymin, xmax, ymax = fc[0].geometry().bbox()
    for f in fc[1:]:
        b = f.geometry().bbox()
        xmin = min(xmin, b[0])
        ymin = min(ymin, b[1])
        xmax = max(xmax, b[2])
        ymax = max(ymax, b[3])
    return xmin, ymin, xmax, ymax


def geojson2framespack(
    frames: str | dict[tuple[float, float, float, float], str],
    *,
    convert_feature: Callable[
        [geojson.Feature], FramesPackFeature
    ] = FramesPackFeature.from_feature,
) -> FramesPack:
    """
    一个 geojson 文件，会把中心设置为数据 bbox 中心
    多个 geojson 文件，需要为每一个文件（帧）设置一个 ts (timestamp), lon, lat, yaw

    可以在 feature.properties 中指定样式，参考
        https://github.com/mapbox/simplestyle-spec/tree/master/1.1.0
    也可以自定义 convert_feature 函数，来设置样式
    """
    if isinstance(frames, str):
        geojson_path = frames
        assert Path(geojson_path).exists(), f"missing geojson file: {geojson_path}"
        ts = 0.0
        bbox = geojson2bbox(geojson_path)
        lon = (bbox[0] + bbox[2]) / 2
        lat = (bbox[1] + bbox[3]) / 2
        yaw = 0.0
        frames = {(ts, lon, lat, yaw): geojson_path}

    assert isinstance(frames, dict), (
        f"frames must be a dict (or str), got {type(frames)}"
    )

    fp = FramesPack()
    for (ts, lon, lat, yaw), geojson_path in frames.items():
        frame_meta = {"ts": ts, "pos": [lon, lat], "yaw": yaw}
        fp.meta.frames.append(object_to_json(frame_meta))
        fc = geojson.FeatureCollection()
        assert fc.load(geojson_path), f"failed to load geojson file: {geojson_path}"
        features = [convert_feature(f) for f in fc]
        # convert wgs84 to local coordinates
        k = tf.cheap_ruler_k(lat)[:2]
        c, s = np.cos(yaw), np.sin(yaw)
        for f in features:
            f.coordinates = gps2local(f.coordinates, (lon, lat), k, c, s)
        frame = FramesPackFrame(features=features)
        frame.meta["geojson_path"] = geojson_path
        fp.frames.append(frame)
    return fp


def framespack2json(frames_pack: str, json_path: str | None = None):
    fp = FramesPack().load(frames_pack)
    if not json_path:
        json_path = Path(frames_pack).with_suffix(".json")
    fp.export_json(json_path)
    return json_path


__all__ = ["framespack2json", "geojson2framespack", "rosbag2framespack"]


if __name__ == "__main__":
    import fire

    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(
        {
            "rosbag2framespack": rosbag2framespack,
            "geojson2framespack": geojson2framespack,
            "framespack2json": framespack2json,
        }
    )
