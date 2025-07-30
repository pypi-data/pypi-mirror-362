import sys
import json
import asyncio
import argparse
import traceback

from aiopath import AsyncPath

from .scanner import scan_music
from .sa.engine import DatabaseEngine
from .logger import main_logger as logger, scanner_logger
from .sa.tables import ChunithmMusicDBBase, ChunithmMusic, ChunithmMusicDifficulty, ChunithmChartData


engine: DatabaseEngine | None = None
a000_path: AsyncPath | None = None
options_dir: AsyncPath | None = None


async def init(config_path: AsyncPath) -> None:
    if not await config_path.is_file():
        await logger.error(f"Config file not found: {config_path}")
        sys.exit(1)

    global engine, a000_path, options_dir
    content = await config_path.read_text(encoding="utf-8")
    data = json.loads(content)
    try:
        a000_path, options_dir = AsyncPath(data["a000_path"]), AsyncPath(data["options_dir"])
        await logger.info("Loaded A000 and options directory configuration.")
    except Exception as e:
        traceback.print_exc()
        await logger.error("Failed to load A000 and options directory configuration.")
        sys.exit(1)
    try:
        await logger.info("Initializing database engine...")
        db_host, db_port, db_user, db_pass, db_name = (
            data["host"],
            data["port"],
            data["user"],
            data["password"],
            data["database"],
        )
        engine = DatabaseEngine(
            url_scheme="mysql+asyncmy://{user}:{password}@{host}:{port}/{database}".format(
                user=db_user, password=db_pass, host=db_host, port=db_port, database=db_name
            ),
            table_base=ChunithmMusicDBBase,
        )
        await engine.init_engine()
        await logger.info("Initialized database engine.")
    except Exception as e:
        traceback.print_exc()
        await logger.error("Failed to initialize database engine.")
        sys.exit(1)


async def update_database() -> None:
    music_infos, music_diffs, chart_data = await scan_music(a000_path, options_dir)
    music_infos = [ChunithmMusic(**(m.model_dump(exclude_none=True))) for m in music_infos]
    music_diffs = [ChunithmMusicDifficulty(**(m.model_dump(exclude_none=True))) for m in music_diffs]
    chart_data = [ChunithmChartData(**(m.model_dump(exclude_none=True))) for m in chart_data]
    await logger.info("Upserting music data to database...")
    await engine.upsert(music_infos)
    await engine.upsert(music_diffs)
    await engine.upsert(chart_data)
    await logger.info("Upserted music data to database.")


async def async_main():
    await logger.start()
    await scanner_logger.start()
    parser = argparse.ArgumentParser(description="Chunithm Music Scanner")
    parser.add_argument(
        "--config",
        type=AsyncPath,
        default=AsyncPath("configs.json"),
        help="Path to configs.json (default: ./configs.json)",
    )

    args = parser.parse_args()
    await init(args.config)
    await update_database()
    await logger.info("Terminating Chunithm Music Scanner...")
    await scanner_logger.stop()
    await logger.stop()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
    sys.exit(0)
