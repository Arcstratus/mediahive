import asyncio
from pathlib import Path


async def remux_to_mp4(input_path: Path, output_path: Path) -> bool:
    """
    Remux a video file to MP4 container without re-encoding.

    Uses ``ffmpeg -c copy`` to copy both video and audio streams into an MP4
    container. This is extremely fast because no re-encoding takes place.

    Suitable when the source already contains H.264 video but is wrapped in a
    different container (MKV, AVI, MOV, FLV, WebM, TS).

    FFmpeg flags used:
        -fflags +genpts+discardcorrupt
            Regenerate presentation timestamps and discard corrupt packets.
        -c copy
            Copy all streams without re-encoding (fast).
        -movflags +faststart
            Move the moov atom to the beginning of the file so browsers can
            start playback before the entire file is downloaded.
        -avoid_negative_ts make_zero
            Shift timestamps so that the first timestamp is zero, fixing
            negative timestamp offsets that some containers produce.

    Args:
        input_path: Path to the source video file.
        output_path: Path where the remuxed MP4 will be written.

    Returns:
        True on success, False on failure.
    """
    try:
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-fflags",
            "+genpts+discardcorrupt",
            "-i",
            str(input_path),
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            "-avoid_negative_ts",
            "make_zero",
            str(output_path),
            "-y",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        return proc.returncode == 0 and output_path.is_file()
    except Exception:
        return False
