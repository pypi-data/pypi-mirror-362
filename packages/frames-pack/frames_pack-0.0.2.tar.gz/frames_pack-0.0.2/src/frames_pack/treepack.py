from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable


class TreeNode:
    def __init__(
        self,
        filename: str,
        content: str | bytes | dict | None = None,
        summary: str | None = None,
    ):
        self.filename: str = filename
        self.__content = content
        self.summary: str | None = summary

    @property
    def content(self) -> bytes:
        if self.__content is None:
            with Path(self.filename).open("rb") as f:
                data = f.read()
        else:
            data = self.__content
        if isinstance(data, str):
            return data.encode("utf-8")
        if isinstance(data, bytes):
            return data
        if isinstance(data, dict):
            return json.dumps(data).encode("utf-8")
        return str(data).encode("utf-8")

    def info(self, start: int, end: int) -> dict:
        ret = {"range": [start, end]}
        if self.summary is not None:
            ret["summary"] = self.summary
        return ret


Tree = dict[str, TreeNode | dict | Any]
"""
Tree is a tree of TreeNode and dict.
Similar to the tree of a file system.
"""


def treepack(
    tree: Tree,
    writer: Callable[[TreeNode], int],
    offset: int = 0,
) -> tuple[int, dict]:
    """
    writer should zstd compress the data, and return the length of the compressed data.
    """
    ret = {}
    assert isinstance(tree, dict), "tree must be a dict"
    for key, value in tree.items():
        if key == "summary":
            assert isinstance(value, str), "summary must be a string"
            ret["summary"] = value
            continue
        if not isinstance(value, TreeNode):
            if isinstance(value, dict):
                offset, ret[key] = treepack(value, writer, offset)
                continue
            ret[key] = value
            continue
        value: TreeNode
        length = writer(value)
        ret[key] = value.info(offset, offset + length)
        offset += length
    return offset, ret
