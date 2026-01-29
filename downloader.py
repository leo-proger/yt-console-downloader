import ua_generator
import yt_dlp

import config_manager
from file_formats import FileFormat

config = config_manager.get_config()


def download(
        link: str,
        file_format: FileFormat,
        resolution: int | None
):
    options = {
        "outtmpl": f"{config.get("outputFolder")}/{config.get("filenameFormat")}",
        "nocheckcertificate": True,
        "http_headers": {
            "User-Agent": ua_generator.generate()
        }
    }

    if file_format == FileFormat.MP4:
        options.update({
            "format": f"bv*[height={resolution}]+ba/b[height={resolution}]",
            "merge_output_format": "mp4"
        })

    elif file_format == FileFormat.MP3:
        options.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else:
        raise Exception("Incorrect output file format.")

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([link])


def get_available_video_qualities(link: str) -> list[int]:
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)  # Fetch metadata only

    formats = info.get("formats", [])

    resolutions = sorted(
        {
            h for fmt in formats
            if (h := fmt.get("height", 0)) and h >= 144
        },
        reverse=True
    )

    return resolutions
