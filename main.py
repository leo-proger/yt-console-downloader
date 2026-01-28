import platform
import shutil

from downloader import *


def main():
    if not check_ffmpg():
        os_name = platform.system()
        base_msg = "Please install ffmpeg. Guide - https://github.com/oop7/ffmpeg-install-guide?tab=readme-ov-file"
        match os_name:
            case "Windows":
                print(base_msg + "#windows-installation")

            case "Darwin":
                print(base_msg + "#macos-installation")

            case "Linux":
                print(base_msg + "#linux-installation")

        return

    user_input = int(input("""Choose number:
1. Download MP4
2. Download MP3
3. Settings
>>> """))

    print("Enter video link.")
    link = input(">>> ")

    if user_input == 1:
        print("Getting video resolutions...")

        resolutions = get_available_video_qualities(link)

        print("Choose video quality:")

        for i, r in enumerate(resolutions):
            print(f"{i + 1}. {r}p")

        quality = int(input(">>> "))

        print("Your video has been started downloading...")

        download(
            link=link,
            file_format=FileFormat.MP4,
            resolution=resolutions[quality - 1]
        )

    elif user_input == 2:
        print("Your video has been started downloading...")

        download(
            link=link,
            file_format=FileFormat.MP3,
            resolution=None
        )
    else:
        print("Incorrect option.\n")
        main()


def check_ffmpg() -> bool:
    return shutil.which("ffmpeg") is not None


if __name__ == "__main__":
    main()
