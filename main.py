#!/usr/bin/env python3
import questionary
from os import makedirs, path
from sys import stdout
from asyncio import (
    CancelledError,
    Event,
    Lock,
    Semaphore,
    all_tasks,
    create_task,
    current_task,
    gather,
    get_event_loop,
    run,
    sleep,
)
from yt_dlp import YoutubeDL
from itertools import cycle
from uuid import uuid4
from argparse import ArgumentParser
from colorama import init, Fore
from tqdm import tqdm
from functools import partial


init(autoreset=True)

__version__ = "v1.0.2"


def brand():
    """
    Prints the brand presentation of the Eagle Downloader, including the version number.
    The presentation uses colored text with the help of `Fore.LIGHTCYAN_EX`
    to make it visually appealing.
    """
    presentation = (
        Fore.LIGHTCYAN_EX
        + f"""
  +-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+
🦅|E|A|G|L|E| |D|O|W|N|L|O|A|D|E|R| {__version__}
  +-+-+-+-+-+ +-+-+-+-+-+-+-+-+-+-+\n"""
    )
    print(presentation)


def parse_arguments():
    """
    Parses command-line arguments for the Eagle Downloader.
    The parser includes a --version argument that, when called,
    displays the version of the program.
    """
    parser = ArgumentParser(
        description="Eagle Downloader: Download YouTube videos and playlists efficiently."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Eagle Downloader {__version__}",
        help="Show the program's version number and exit.",
    )
    return parser.parse_args()


def create_output_directory(directory_name="downloads"):
    """Creates the output directory if it doesn't exist."""
    output_path = path.abspath(directory_name)
    makedirs(output_path, exist_ok=True)
    return output_path


def sanitize_filename(filename):
    """Sanitizes the filename to ensure it's safe for the filesystem."""
    allowed_chars = (" ", ".", "_")
    return "".join(c if c.isalnum() or c in allowed_chars else "_" for c in filename)


async def get_download_type():
    """Asks the user to select the download type."""
    choice = await questionary.select(
        "Select download type:", choices=["Audio", "Video", "Both"]
    ).ask_async()
    return choice.lower()


async def get_audio_quality():
    """Asks the user to select the audio quality."""
    choices = ["128", "192", "256", "320"]
    quality = await questionary.select(
        "Select audio quality in kbps:", choices=choices, default="320"
    ).ask_async()
    return quality


async def get_video_quality():
    """Asks the user to select the maximum video resolution."""
    choices = ["480", "720", "1080", "1440", "2160"]
    quality = await questionary.select(
        "Select maximum video resolution:", choices=choices, default="1080"
    ).ask_async()
    return quality


async def get_output_directory():
    """Asks the user to enter the output directory."""
    output_dir = await questionary.text(
        "Enter output directory:", default="downloads"
    ).ask_async()
    return output_dir or "downloads"


async def get_video_output_directory():
    """Asks the user if they want to save video files in a different directory."""
    use_different_directory = await questionary.confirm(
        "Do you want to save video files in a different directory?"
    ).ask_async()
    if use_different_directory:
        video_output_dir = await questionary.text(
            "Enter video output directory:", default="videos"
        ).ask_async()
        return video_output_dir or "videos"
    else:
        return None


async def get_rate_limit():
    """Asks the user to select the rate limit for downloads."""
    choices = ["500K", "1M", "2M", "5M", "No limit"]
    rate_limit_choice = await questionary.select(
        "Select rate limit for downloads:", choices=choices, default="No limit"
    ).ask_async()
    return parse_rate_limit(rate_limit_choice)


def parse_rate_limit(rate_limit_str):
    """Parses the rate limit string and converts it to bytes per second."""
    if rate_limit_str == "No limit":
        return None
    units = {"K": 1024, "M": 1024 * 1024}
    unit = rate_limit_str[-1].upper()
    value = rate_limit_str[:-1]
    if unit in units and value.isdigit():
        return int(value) * units[unit]
    print(Fore.RED + "Invalid rate limit. Skipping rate limiting.")
    return None


async def get_max_concurrent():
    """Asks the user to select the maximum number of concurrent downloads."""
    choices = ["1", "2", "5", "10"]
    max_concurrent_choice = await questionary.select(
        "Select max concurrent downloads:", choices=choices, default="5"
    ).ask_async()
    return int(max_concurrent_choice)


async def get_url():
    """Asks the user to enter the video or playlist URL."""
    brand()
    url = await questionary.text("Enter video or playlist URL:").ask_async()
    return url.strip()


async def get_cookies_file():
    """Asks the user if they want to use a cookies file for age-restricted videos."""
    use_cookies = await questionary.confirm(
        "Do you need to use cookies to download age-restricted videos?"
    ).ask_async()
    if use_cookies:
        cookies_file = await questionary.text(
            "Enter the path to your cookies.txt file:"
        ).ask_async()
        if path.isfile(cookies_file):
            return cookies_file
        else:
            print(Fore.YELLOW + "Cookies file not found. Proceeding without cookies.")
    return None


async def get_user_input():
    """Collects all user inputs."""
    url = await get_url()
    cookies_file = await get_cookies_file()
    return {"url": url, "cookies_file": cookies_file}


def get_ydl_options(
    output_path,
    rate_limit,
    download_type,
    audio_quality,
    video_quality,
    video_output_dir=None,
    cookies_file=None,
):
    """Prepares the options for yt-dlp based on user inputs."""
    ydl_opts = initialize_ydl_options(output_path, video_output_dir, cookies_file)
    ydl_opts["format"] = get_format_string(download_type, video_quality)
    ydl_opts["postprocessors"] = get_postprocessors(download_type, audio_quality)
    if rate_limit:
        ydl_opts["ratelimit"] = rate_limit
    if download_type in ["video", "both"]:
        ydl_opts["merge_output_format"] = "mp4"
    return ydl_opts


def initialize_ydl_options(output_path, video_output_dir=None, cookies_file=None):
    """Initializes the yt-dlp options with default settings."""
    paths = {"home": output_path}
    if video_output_dir:
        video_output_path = create_output_directory(video_output_dir)
        paths["video"] = video_output_path
    ydl_opts = {
        "outtmpl": "%(id)s_%(title)s.%(ext)s",
        "paths": paths,
        "ignoreerrors": True,
        "quiet": True,
        "no_warnings": True,
        "progress_hooks": [],
        "concurrent_fragment_downloads": 1,
    }
    if cookies_file:
        ydl_opts["cookiefile"] = cookies_file
    return ydl_opts


def get_format_string(download_type, video_quality):
    """Determines the format string for yt-dlp based on download type and quality."""
    if download_type == "audio":
        return "bestaudio/best"
    elif download_type in ["video", "both"]:
        return f"bestvideo[height<={video_quality}]+bestaudio/best[height<={video_quality}]"
    return "best"


def get_postprocessors(download_type, audio_quality):
    """Configures postprocessors for yt-dlp."""
    if download_type == "audio":
        return [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": audio_quality,
            }
        ]
    elif download_type == "both":
        return [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            }
        ]
    return []


async def download_entry(entry, ydl_opts, lock):
    """Downloads a single entry (video/audio)."""
    if not is_valid_entry(entry):
        print(Fore.YELLOW + "Invalid entry detected. Skipping.")
        return
    sanitized_title = sanitize_filename(entry["title"])
    unique_id = entry.get("id", str(uuid4()))
    output_template = update_output_template(sanitized_title, unique_id)
    ydl_opts["outtmpl"] = output_template
    progress = create_progress_bar(sanitized_title)
    ydl_opts["progress_hooks"] = [lambda d: progress_hook(d, progress)]
    await perform_download(entry["webpage_url"], ydl_opts, progress, lock)


def is_valid_entry(entry):
    return "webpage_url" in entry and "title" in entry


def update_output_template(sanitized_title, unique_id):
    """Updates the output template for yt-dlp."""
    return f"{unique_id}_{sanitized_title}.%(ext)s"


def create_progress_bar(title):
    """Creates a progress bar for the download."""
    return tqdm(
        total=100,
        desc=Fore.GREEN + f"Downloading: {title}",
        unit="%",
        ncols=100,
        leave=False,
    )


def progress_hook(d, progress):
    """Updates the progress bar based on yt-dlp's progress hooks."""
    if d["status"] == "downloading":
        update_progress_bar(d, progress)
    elif d["status"] == "finished":
        complete_progress_bar(progress)
        d["filename"] = d.get("filename")


def update_progress_bar(d, progress):
    """Calculates and updates the progress bar percentage."""
    total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
    downloaded_bytes = d.get("downloaded_bytes", 0)
    percentage = downloaded_bytes / total_bytes * 100
    progress.n = percentage
    progress.refresh()


def complete_progress_bar(progress):
    """Completes and closes the progress bar."""
    progress.n = 100
    progress.refresh()
    progress.close()


async def perform_download(url, ydl_opts, progress, lock):
    loop = get_event_loop()
    try:
        with YoutubeDL(ydl_opts) as ydl:
            func = partial(ydl.extract_info, url, download=True)
            async with lock:
                info = await loop.run_in_executor(None, func)
            output_file = ydl.prepare_filename(info)
            print(Fore.GREEN + f"\nCompleted: {output_file}")
    except CancelledError:
        print(Fore.YELLOW + f"Download cancelled: {ydl_opts['outtmpl']}")
    except Exception as e:
        print(Fore.RED + f"Error downloading: {e}")
    finally:
        progress.close()


async def process_entries(entries, ydl_opts, max_concurrent, shutdown_event):
    """Processes multiple entries (e.g., a playlist)."""
    if not entries:
        print(Fore.YELLOW + "No entries found to download.")
        return
    lock = Lock()
    tasks = create_download_tasks(
        entries, ydl_opts, max_concurrent, shutdown_event, lock
    )
    await gather(*tasks, return_exceptions=True)


def create_download_tasks(entries, ydl_opts, max_concurrent, shutdown_event, lock):
    """Creates asynchronous tasks for downloading entries."""
    semaphore = Semaphore(max_concurrent)
    tasks = []
    for entry in entries:
        task = create_task(
            download_with_semaphore(entry, ydl_opts, semaphore, shutdown_event, lock)
        )
        tasks.append(task)
    return tasks


async def download_with_semaphore(entry, ydl_opts, semaphore, shutdown_event, lock):
    """Downloads an entry while respecting the semaphore limit."""
    async with semaphore:
        if shutdown_event.is_set():
            return
        await download_entry(entry, ydl_opts, lock)


def determine_if_playlist(info):
    """Determines if the provided URL is a playlist."""
    return "entries" in info


async def gather_user_options(is_playlist):
    """Collects user options based on whether the input is a playlist."""
    output_dir = await get_output_directory()
    rate_limit = await get_rate_limit()
    download_type = await get_download_type()
    video_output_dir = None
    if download_type in ["video", "both"]:
        video_output_dir = await get_video_output_directory()
    qualities = await get_quality(download_type)
    max_concurrent = await get_max_concurrent() if is_playlist else 1
    user_options = {
        "output_dir": output_dir,
        "rate_limit": rate_limit,
        "download_type": download_type,
        "video_output_dir": video_output_dir,
        "audio_quality": qualities.get("audio"),
        "video_quality": qualities.get("video"),
        "max_concurrent": max_concurrent,
    }
    return user_options


async def get_quality(download_type):
    """Gets the quality settings based on the download type."""
    qualities = {}
    if download_type == "audio":
        qualities["audio"] = await get_audio_quality()
        qualities["video"] = None
    elif download_type == "video":
        qualities["video"] = await get_video_quality()
        qualities["audio"] = None
    elif download_type == "both":
        qualities["audio"] = await get_audio_quality()
        qualities["video"] = await get_video_quality()
    else:
        qualities["audio"] = None
        qualities["video"] = None
    return qualities


def prepare_ydl_options(user_options, cookies_file=None):
    """Prepares yt-dlp options based on user inputs."""
    output_path = create_output_directory(user_options["output_dir"])
    ydl_opts = get_ydl_options(
        output_path,
        user_options["rate_limit"],
        user_options["download_type"],
        user_options["audio_quality"],
        user_options["video_quality"],
        user_options["video_output_dir"],
        cookies_file,
    )
    return ydl_opts


async def perform_downloads(
    info, ydl_opts, is_playlist, max_concurrent, shutdown_event
):
    """Performs downloads based on whether the input is a playlist or a single video."""
    if is_playlist:
        await handle_playlist(info, ydl_opts, max_concurrent, shutdown_event)
    else:
        await download_entry(info, ydl_opts, Lock())


async def show_spinner(message, stop_event):
    """Displays a spinner while processing."""
    spinner = cycle(["-", "\\", "|", "/"])
    while not stop_event.is_set():
        stdout.write(next(spinner) + " " + message + "    \r")
        stdout.flush()
        await sleep(0.1)
    stdout.write(" " * (len(message) + 4) + "\r")
    stdout.flush()


async def extract_info(url, ydl_opts, shutdown_event):
    """Extracts video or playlist information using yt-dlp."""
    loop = get_event_loop()
    stop_event = Event()
    spinner_task = create_task(show_spinner("Processing your request...", stop_event))
    try:
        with YoutubeDL(ydl_opts) as ydl:
            func = partial(ydl.extract_info, url, download=False)
            info = await loop.run_in_executor(None, func)
        stop_event.set()
        await spinner_task
        return info
    except Exception as e:
        stop_event.set()
        await spinner_task
        if not shutdown_event.is_set():
            print(Fore.RED + f"Error processing the URL: {e}")
        return None


async def handle_playlist(info, ydl_opts, max_concurrent, shutdown_event):
    """Handles the download of a playlist."""
    entries = info.get("entries", [])
    if not entries:
        print(Fore.YELLOW + "The playlist appears to be empty.")
        return
    print(Fore.CYAN + f"Found {len(entries)} items. Starting downloads...")
    await process_entries(entries, ydl_opts, max_concurrent, shutdown_event)


async def download_media(user_input, shutdown_event):
    """Main function to orchestrate the download process."""
    url = user_input["url"]
    cookies_file = user_input.get("cookies_file")
    temp_ydl_opts = initialize_ydl_options(".", cookies_file=cookies_file)
    info = await extract_info(url, temp_ydl_opts, shutdown_event)
    if not info or shutdown_event.is_set():
        return
    is_playlist = determine_if_playlist(info)
    user_options = await gather_user_options(is_playlist)
    if shutdown_event.is_set():
        return
    ydl_opts = prepare_ydl_options(user_options, cookies_file)
    await perform_downloads(
        info, ydl_opts, is_playlist, user_options["max_concurrent"], shutdown_event
    )


async def shutdown(loop, signal=None):
    """Handles graceful shutdown of the program."""
    print(Fore.YELLOW + "\nShutting down...")
    tasks = [t for t in all_tasks(loop) if t is not current_task()]
    [task.cancel() for task in tasks]
    await gather(*tasks, return_exceptions=True)
    loop.stop()


def main():
    """Entry point of the script."""
    parse_arguments()
    loop = get_event_loop()
    shutdown_event = Event()
    try:
        run(main_async(shutdown_event))
    except KeyboardInterrupt:
        shutdown_event.set()
        loop.run_until_complete(shutdown(loop))
        print(Fore.RED + "\nDownload interrupted by user.")
    finally:
        loop.close()


async def main_async(shutdown_event):
    """Asynchronous main function."""
    user_input = await get_user_input()
    await download_media(user_input, shutdown_event)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(Fore.RED + "\nInterrupted.")
