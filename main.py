from downloader import *


def main():
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
        if not check_ffmpg(): # TODO
            ...

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
    ...

if __name__ == "__main__":
    main()
