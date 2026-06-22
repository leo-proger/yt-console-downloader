import ua_generator
import yt_dlp

import config_manager
from file_formats import FileFormat

config = config_manager.get_config()


def _base_options() -> dict:
    return {
        "nocheckcertificate": True,
        "http_headers": {"User-Agent": ua_generator.generate()},
        "js_runtimes": {"node": {}},
    }


def _format_options(file_format: FileFormat, resolution: int | None) -> dict:
    if file_format == FileFormat.MP4:
        return {
            "format": f"bv*[height={resolution}]+ba/b[height={resolution}]",
            "merge_output_format": "mp4",
        }
    if file_format == FileFormat.MP3:
        return {
            "format": "bestaudio/best",
            # Скачиваем обложку видео, чтобы встроить её в итоговый MP3
            "writethumbnail": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
                # Приводим обложку к JPG — формат, который корректно встраивается в MP3
                {
                    "key": "FFmpegThumbnailsConvertor",
                    "format": "jpg",
                },
                # Встраиваем обложку в аудиофайл
                {
                    "key": "EmbedThumbnail",
                    "already_have_thumbnail": False,
                },
            ],
        }
    raise ValueError(f"Unsupported file format: {file_format}")


def download(link: str, file_format: FileFormat, resolution: int | None) -> None:
    options = {
        **_base_options(),
        "outtmpl": f"{config.get('outputFolder')}/{config.get('filenameFormat')}",
        **_format_options(file_format, resolution),
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([link])


def get_available_video_qualities(link: str) -> list[int]:
    options = {
        **_base_options(),
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(link, download=False)

    return sorted(
        {h for fmt in info.get("formats", []) if (h := fmt.get("height")) and h >= 144},
        reverse=True,
    )
