import asyncio
import json
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ProbeResult:
    video_codec: str | None   # e.g. "h264", "hevc", "vp9"
    audio_codec: str | None   # e.g. "aac", "opus", "mp3"
    container: str | None     # e.g. "matroska", "mpegts", "mov"
    duration: float | None    # seconds
    width: int | None
    height: int | None

    @property
    def is_h264(self) -> bool:
        return self.video_codec == "h264"

    @property
    def is_aac(self) -> bool:
        return self.audio_codec == "aac"

    @property
    def is_mp4_ready(self) -> bool:
        """Already H.264+AAC — can be remuxed or is already MP4."""
        return self.is_h264 and (self.is_aac or self.audio_codec is None)


async def probe_video(path: Path) -> ProbeResult | None:
    """Run ffprobe on a file and return parsed codec info. Returns None on failure."""
    try:
        proc = await asyncio.create_subprocess_exec(
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )
        stdout, _ = await proc.communicate()

        if proc.returncode != 0:
            return None

        data = json.loads(stdout)

        streams = data.get("streams", [])
        fmt = data.get("format", {})

        video_stream = next(
            (s for s in streams if s.get("codec_type") == "video"), None
        )
        audio_stream = next(
            (s for s in streams if s.get("codec_type") == "audio"), None
        )

        video_codec = video_stream.get("codec_name") if video_stream else None
        audio_codec = audio_stream.get("codec_name") if audio_stream else None
        container = fmt.get("format_name")

        raw_duration = fmt.get("duration")
        duration = float(raw_duration) if raw_duration is not None else None

        width = video_stream.get("width") if video_stream else None
        height = video_stream.get("height") if video_stream else None

        return ProbeResult(
            video_codec=video_codec,
            audio_codec=audio_codec,
            container=container,
            duration=duration,
            width=width,
            height=height,
        )
    except Exception:
        return None
