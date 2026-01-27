import yt_dlp

from file_formats import FileFormat


def download(
        link: str,
        file_format: FileFormat,
        resolution: int | None
):
    filename_template = "%(creator)s - %(title)s.%(ext)s"
    options = {
        "outtmpl": f"/Users/leo_proger/Downloads/{filename_template}"
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
