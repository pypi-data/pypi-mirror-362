import re
import asyncio
import configparser
from typing import Any
from pathlib import Path

from aiopath import AsyncPath
from datetime import datetime, date
import xml.etree.ElementTree as xmlEt

from .logger import scanner_logger
from .schemas import MusicDifficultySchema, MusicInfoSchema, ChartDataSchema

c2s_mapping = {
    "CREATOR": "creator",
    "BPM_DEF": "bpm",
    "T_JUDGE_TAP": "tap_count",
    "T_JUDGE_HLD": "hold_count",
    "T_JUDGE_SLD": "slide_count",
    "T_JUDGE_AIR": "air_count",
    "T_JUDGE_FLK": "flick_count",
    "T_JUDGE_ALL": "count",
}


def parse_music_xml(xml_path: AsyncPath, current_version: str) -> tuple[MusicInfoSchema, MusicDifficultySchema]:
    tree = xmlEt.parse(Path(xml_path))
    root = tree.getroot()

    def find_text(path: str) -> str | None:
        el = root.find(path)
        return el.text if el is not None and el.text else None

    def parse_release_date(raw: str | None) -> date | None:
        if not raw or len(raw) != 8:
            return None
        try:
            return datetime.strptime(raw, "%Y%m%d").date()
        except ValueError:
            return None

    def extract_version_tag(tag_str: str | None) -> str | None:
        if not tag_str:
            return None
        match = re.search(r"(\d+)\.(\d+)", tag_str)
        return match.group(0) if match else None

    def get_fumen_level_by_type_id(type_id: int) -> float | None:
        for fumen in root.findall("./fumens/MusicFumenData"):
            fumen_type_id = fumen.findtext("./type/id")
            if fumen_type_id and int(fumen_type_id) == type_id:
                level = fumen.findtext("level") or "0"
                decimal = fumen.findtext("levelDecimal") or "0"
                return float(f"{level}.{decimal}")
        return None

    music_id = int(find_text("./name/id") or 0)
    title = find_text("./name/str") or ""
    artist = find_text("./artistName/str") or ""
    category = find_text("./genreNames/list/StringID/str")
    release_tag = find_text("./releaseTagName/str")
    release_version = extract_version_tag(release_tag)
    release_date = parse_release_date(find_text("./releaseDate"))

    info = MusicInfoSchema(
        music_id=music_id,
        title=title,
        artist=artist,
        category=category,
        version=release_version,
        release_date=release_date,
        is_deleted=False,
    )

    diff = MusicDifficultySchema(
        music_id=music_id,
        version=current_version,
        diff0_const=get_fumen_level_by_type_id(0),
        diff1_const=get_fumen_level_by_type_id(1),
        diff2_const=get_fumen_level_by_type_id(2),
        diff3_const=get_fumen_level_by_type_id(3),
        diff4_const=get_fumen_level_by_type_id(4),
    )

    return info, diff


async def c2s_analyzer(file_path: AsyncPath) -> ChartDataSchema:
    data: dict[str, Any] = {}
    match = re.match(r"(\d{4})_(\d{2})\.c2s$", file_path.name)
    if not match:
        raise ValueError(f"Invalid c2s filename format: {file_path.name}")
    data["music_id"] = int(match.group(1))
    data["difficulty"] = int(match.group(2))
    async with file_path.open("r", encoding="utf-8") as f:
        async for line in f:
            parts = line.strip().split(maxsplit=1)
            if len(parts) < 2:
                continue
            identifier = parts[0]
            value = parts[1]
            if identifier in c2s_mapping:
                field = c2s_mapping[identifier]
                if identifier == "BPM_DEF":
                    data[field] = float(value.split()[0])
                else:
                    data[field] = value
    await scanner_logger.debug(f"Scanned c2s data: {str(file_path)}")
    return ChartDataSchema(**data)


async def option_ver(option_path: AsyncPath) -> str | None:
    config_path = option_path / "data.conf"
    if not await config_path.is_file():
        return None
    content = await config_path.read_text(encoding="utf-8")
    parser = configparser.ConfigParser()
    parser.read_string(content)
    try:
        major = parser.getint("Version", "VerMajor")
        minor = parser.getint("Version", "VerMinor")
        if major <= 2 or minor <= 55:
            return f"{major}.{minor}"
        else:
            return None
    except (configparser.Error, ValueError):
        return None


async def iter_all_files(dir_path: AsyncPath):
    async for entry in dir_path.iterdir():
        if await entry.is_dir():
            async for sub in iter_all_files(entry):
                yield sub
        else:
            yield entry


async def scan_music(
    a000_path: AsyncPath, options_dir: AsyncPath
) -> tuple[list[MusicInfoSchema], list[MusicDifficultySchema], list[ChartDataSchema]]:
    valid_dirs: dict[AsyncPath:str] = {}
    music_infos: list[MusicInfoSchema] = []
    music_diffs: list[MusicDifficultySchema] = []
    chart_data: list[ChartDataSchema] = []
    await scanner_logger.info("Validating option directories...")
    opt_v = await option_ver(a000_path)
    if opt_v:
        valid_dirs[a000_path] = opt_v
    async for option_path in options_dir.iterdir():
        if await option_path.is_dir():
            opt_v = await option_ver(option_path)
            if opt_v:
                valid_dirs[option_path] = opt_v
    await scanner_logger.info("Validated option directories.")
    await scanner_logger.info("Scanning music data...")
    xml_tasks = []
    c2s_tasks = []
    xml_file_infos = []
    for valid_dir, opt_v in valid_dirs.items():
        async for file in iter_all_files(valid_dir):
            if file.name == "Music.xml":
                xml_file_infos.append((file, opt_v))
            elif file.suffix == ".c2s":
                c2s_tasks.append(c2s_analyzer(file))
    for file, opt_v in xml_file_infos:
        xml_tasks.append(asyncio.to_thread(parse_music_xml, file, opt_v))
    results = await asyncio.gather(*xml_tasks, return_exceptions=True)
    for i, result in enumerate(results):
        file, _ = xml_file_infos[i]
        if isinstance(result, Exception):
            await scanner_logger.error(f"[Music.xml error] {file}: {result}")
        else:
            info, diff = result
            music_infos.append(info)
            music_diffs.append(diff)
            await scanner_logger.debug(f"Scanned music data: {file}")

    c2s_results = await asyncio.gather(*c2s_tasks, return_exceptions=True)
    c2s_files = []
    for valid_dir in valid_dirs:
        async for file in iter_all_files(valid_dir):
            if file.suffix == ".c2s":
                c2s_files.append(file)
    for i, result in enumerate(c2s_results):
        file = c2s_files[i] if i < len(c2s_files) else None
        if isinstance(result, Exception):
            await scanner_logger.error(f"[C2S error] {file}: {result}")
        else:
            chart_data.append(result)

    await scanner_logger.info("Scanned music data.")
    return music_infos, music_diffs, chart_data
