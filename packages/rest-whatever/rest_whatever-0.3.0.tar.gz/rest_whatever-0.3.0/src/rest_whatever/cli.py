#!/usr/bin/env python3
"""
REST Whatever CLI
使用 Fire 库提供命令行接口
"""
import sys

import fire
import uvicorn


def serve(
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = True,
    workers: int = 1,
    log_level: str = "info",
    access_log: bool = True,
):
    uvicorn.run(
        "rest_whatever.main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else None,
        log_level=log_level,
        access_log=access_log,
    )


def main():
    """CLI 入口点"""
    try:
        fire.Fire(serve)
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
