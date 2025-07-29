"""Tools for export with videos."""

import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

from kili_formats.exceptions import NotExportableAssetError
from kili_formats.media.image import get_frame_dimensions

if TYPE_CHECKING:
    import ffmpeg

ffmpeg_installed = True
try:
    import ffmpeg
except ImportError:
    ffmpeg_installed = False


class FFmpegError(Exception):
    """Errors related to ffmpeg."""


def get_video_and_frame_dimensions(
    asset: Dict,
) -> Tuple[int, int]:
    """Get a video width and height, and a frame width and height."""
    width = height = 0
    if "resolution" in asset and asset["resolution"] is not None:
        width = asset["resolution"]["width"]
        height = asset["resolution"]["height"]
        return width, height
    if isinstance(asset["jsonContent"], list) and Path(asset["jsonContent"][0]).is_file():
        width, height = get_frame_dimensions(asset)
    elif Path(asset["content"]).is_file():
        width, height = get_video_dimensions(asset)
    else:
        raise NotExportableAssetError(
            f"Could not find video dimensions for asset with externalId '{asset['externalId']}'. Please"
            " use `kili.update_properties_in_assets()` to update the resolution of your asset. Or use"
            " `kili.export_labels(with_assets=True).`"
        )
    return width, height


def get_video_dimensions(asset: Dict) -> Tuple:
    """Get a video width and height."""
    if not ffmpeg_installed:
        raise ImportError("Install with `pip install kili-formats[video]` to use this feature.")
    if "resolution" in asset and asset["resolution"] is not None:
        return (asset["resolution"]["width"], asset["resolution"]["height"])

    if Path(asset["content"]).is_file():
        probe = ffmpeg.probe(str(asset["content"]))
        video_info = next(s for s in probe["streams"] if s["codec_type"] == "video")
        width = video_info["width"]
        height = video_info["height"]
        return width, height

    raise NotExportableAssetError(
        f"Could not find video dimensions for asset with externalId '{asset['externalId']}'. Please"
        " use `kili.update_properties_in_assets()` to update the resolution of your asset. Or use"
        " `kili.export_labels(with_assets=True).`"
    )


def cut_video(
    video_path: Path, asset: Dict, leading_zeros: int, output_dir: Optional[Path]
) -> List[Path]:
    """Download and cut video into frames."""
    if not ffmpeg_installed:
        raise ImportError("Install with `pip install kili-formats[video]` to use this feature.")
    output_dir = output_dir or video_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    if (
        "jsonMetadata" in asset
        and "processingParameters" in asset["jsonMetadata"]
        and "framesPlayedPerSecond" in asset["jsonMetadata"]["processingParameters"]
    ):
        metadata = asset["jsonMetadata"]
        final_framerate = metadata["processingParameters"]["framesPlayedPerSecond"]
    else:
        try:
            probe = ffmpeg.probe(str(video_path))
            video_info = next(s for s in probe["streams"] if s["codec_type"] == "video")
            # avg_frame_rate is total # of frames / total duration
            # r_frame_rate is the lowest framerate with which all timestamps can be represented
            # accurately (it is the least common multiple of all framerates in the stream)
            frame_rate_string = video_info["r_frame_rate"].split("/")
            final_framerate = int(frame_rate_string[0]) / int(frame_rate_string[1])
        except ffmpeg.Error as error:
            raise FFmpegError(f"ffmpeg error for asset {video_path.name}: {error}") from error

    output_frames = []
    try:
        with TemporaryDirectory() as temp_dir:
            ffmpeg.input(str(video_path)).filter("fps", fps=final_framerate, round="up").output(
                os.path.join(str(temp_dir), "%d.jpg"), start_number=0
            ).run(capture_stdout=True, capture_stderr=True)
            for file in os.listdir(temp_dir):
                idx = int(Path(file).stem)
                new_filename = f"{asset['externalId']}_{str(idx + 1).zfill(leading_zeros)}.jpg"
                shutil.move(str(Path(temp_dir) / file), str(output_dir / new_filename))
                output_frames.append(output_dir / new_filename)
    except ffmpeg.Error as error:
        raise FFmpegError(f"ffmpeg error for asset {video_path.name}: {error}") from error

    return sorted(output_frames)
