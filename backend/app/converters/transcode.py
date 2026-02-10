import asyncio
from pathlib import Path


async def transcode_to_mp4(input_path: Path, output_path: Path, crf: int = 23) -> bool:
    """
    Transcode a video file to H.264/AAC MP4.

    Used when the source video uses a codec that browsers cannot play natively
    (VP9, HEVC, MPEG-2, etc.) and must be fully re-encoded.

    FFmpeg flags used:
        -c:v libx264
            Encode video to H.264.
        -preset medium
            Balance between encoding speed and compression efficiency.
        -crf <crf>
            Constant Rate Factor quality setting (0-51, lower is better).
            23 is visually lossless for most content.
        -c:a aac -b:a 128k
            Encode audio to AAC at 128 kbps.
        -movflags +faststart
            Move the moov atom to the beginning of the file so browsers can
            start playback before the entire file is downloaded.

    Args:
        input_path: Source video file.
        output_path: Destination MP4 file.
        crf: Constant Rate Factor (0-51, lower = better quality, 23 = default).

    Returns:
        True on success, False on failure.
    """
    try:
        proc = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-i",
            str(input_path),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            str(crf),
            "-c:a",
            "aac",
            "-b:a",
            "128k",
            "-movflags",
            "+faststart",
            str(output_path),
            "-y",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        await proc.communicate()
        return proc.returncode == 0 and output_path.is_file()
    except Exception:
        return False
