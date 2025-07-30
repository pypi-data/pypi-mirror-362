from __future__ import annotations

import os
import socket

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from loguru import logger

fallback_frames_pack_path: str = os.getenv(
    "FALLBACK_FRAMES_PACK_PATH",
    "build/frames_pack.bin",
)
logger.info(f"fallback_frames_pack_path: {fallback_frames_pack_path}")

app = FastAPI(title="Frames Pack Server", version="0.0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


def parse_range_header(range_header: str, file_size: int) -> tuple[int, int]:
    """解析HTTP Range头"""
    if not range_header.startswith("bytes="):
        raise ValueError("Invalid range header")

    range_spec = range_header[6:]  # 去掉"bytes="

    if "-" not in range_spec:
        raise ValueError("Invalid range format")

    start_str, end_str = range_spec.split("-", 1)

    if start_str == "":
        # 后缀范围，例如：bytes=-500
        if end_str == "":
            raise ValueError("Invalid range format")
        suffix_length = int(end_str)
        start = max(0, file_size - suffix_length)
        end = file_size - 1
    elif end_str == "":
        # 前缀范围，例如：bytes=500-
        start = int(start_str)
        end = file_size - 1
    else:
        # 完整范围，例如：bytes=500-999
        start = int(start_str)
        end = int(end_str)

    # 验证范围
    if start < 0 or end >= file_size or start > end:
        raise ValueError("Invalid range values")

    return start, end


def create_file_stream(file_path: str, start: int, end: int, chunk_size: int = 8192):
    """创建文件流生成器"""
    logger.info(f"http-range {file_path}[{start}:{end}]")
    with open(file_path, "rb") as file:  # noqa: PTH123
        file.seek(start)
        remaining = end - start + 1

        while remaining > 0:
            chunk = file.read(min(chunk_size, remaining))
            if not chunk:
                break
            remaining -= len(chunk)
            yield chunk


@app.get("/")
async def serve_index():
    if not os.path.exists("index.html"):  # noqa: PTH110
        raise HTTPException(status_code=404, detail="index.html not found")
    return FileResponse("index.html", media_type="text/html")


@app.get("/frames_pack.bin")
async def serve_frames_pack(request: Request):
    """提供fallback_frames_pack文件，支持范围请求"""
    if not fallback_frames_pack_path:
        raise HTTPException(
            status_code=404, detail="Fallback frames pack not configured"
        )

    if not os.path.exists(fallback_frames_pack_path):  # noqa: PTH110
        raise HTTPException(
            status_code=404, detail="Fallback frames pack file not found"
        )

    file_size = os.path.getsize(fallback_frames_pack_path)  # noqa: PTH202
    range_header = request.headers.get("range")
    if not range_header:
        headers = {
            "Accept-Ranges": "bytes",
            "Content-Length": str(file_size),
            "Content-Type": "application/octet-stream",
        }
        return FileResponse(fallback_frames_pack_path, headers=headers)

    cache_headers = {
        "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
        "Pragma": "no-cache",
        "Expires": "0",
    }

    try:
        start, end = parse_range_header(range_header, file_size)
        content_length = end - start + 1

        # 创建响应头
        headers = {
            "Content-Range": f"bytes {start}-{end}/{file_size}",
            "Accept-Ranges": "bytes",
            "Content-Length": str(content_length),
            "Content-Type": "application/octet-stream",
            **cache_headers,
        }

        # 创建流式响应
        file_stream = create_file_stream(fallback_frames_pack_path, start, end)
        return StreamingResponse(
            file_stream,
            status_code=206,  # Partial Content
            headers=headers,
        )

    except ValueError:
        return Response(
            status_code=416,  # Range Not Satisfiable
            headers={
                "Content-Range": f"bytes */{file_size}",
                "Accept-Ranges": "bytes",
                **cache_headers,
            },
        )


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "ok"}


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main(
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = True,
):
    logger.info(f"serving at: http://{get_local_ip()}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
    )


if __name__ == "__main__":
    import fire

    fire.core.Display = lambda lines, out: print(*lines, file=out)
    fire.Fire(main)
