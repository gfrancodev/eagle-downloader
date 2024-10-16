import os
import re
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, Mock
from main import (
    create_output_directory,
    sanitize_filename,
    get_download_type,
    get_audio_quality,
    get_video_quality,
    get_output_directory,
    get_video_output_directory,
    get_rate_limit,
    parse_rate_limit,
    get_max_concurrent,
    get_url,
    get_cookies_file,
    get_user_input,
    get_ydl_options,
    initialize_ydl_options,
    get_format_string,
    get_postprocessors,
    download_entry,
    is_valid_entry,
    update_output_template,
    create_progress_bar,
    progress_hook,
    update_progress_bar,
    complete_progress_bar,
    perform_download,
    process_entries,
    create_download_tasks,
    download_with_semaphore,
    determine_if_playlist,
    get_quality,
    prepare_ydl_options,
    show_spinner,
    extract_info,
    handle_playlist,
    download_media,
    shutdown,
)


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


def test_create_output_directory(tmp_path):
    dir_name = tmp_path / "downloads"
    output_path = create_output_directory(str(dir_name))
    assert os.path.exists(output_path)
    assert os.path.isdir(output_path)


def test_sanitize_filename():
    filename = "Test: Video/Name?"
    sanitized = sanitize_filename(filename)
    assert sanitized == "Test_ Video_Name_"


@pytest.mark.asyncio
async def test_get_download_type_audio(mocker):
    mocker.patch(
        "questionary.select",
        return_value=AsyncMock(ask_async=AsyncMock(return_value="Audio")),
    )
    result = await get_download_type()
    assert result == "audio"


@pytest.mark.asyncio
async def test_get_download_type_video(mocker):
    mocker.patch(
        "questionary.select",
        return_value=AsyncMock(ask_async=AsyncMock(return_value="Video")),
    )
    result = await get_download_type()
    assert result == "video"


@pytest.mark.asyncio
async def test_get_audio_quality(mocker):
    mocker.patch(
        "questionary.select",
        return_value=AsyncMock(ask_async=AsyncMock(return_value="256")),
    )
    result = await get_audio_quality()
    assert result == "256"


@pytest.mark.asyncio
async def test_get_video_quality(mocker):
    mocker.patch(
        "questionary.select",
        return_value=AsyncMock(ask_async=AsyncMock(return_value="720")),
    )
    result = await get_video_quality()
    assert result == "720"


@pytest.mark.asyncio
async def test_get_output_directory(mocker):
    mocker.patch(
        "questionary.text",
        return_value=AsyncMock(ask_async=AsyncMock(return_value="my_downloads")),
    )
    result = await get_output_directory()
    assert result == "my_downloads"


@pytest.mark.asyncio
async def test_get_video_output_directory_yes(mocker):
    mocker.patch(
        "questionary.confirm",
        return_value=AsyncMock(ask_async=AsyncMock(return_value=True)),
    )
    mocker.patch(
        "questionary.text",
        return_value=AsyncMock(ask_async=AsyncMock(return_value="videos")),
    )
    result = await get_video_output_directory()
    assert result == "videos"


@pytest.mark.asyncio
async def test_get_video_output_directory_no(mocker):
    mocker.patch(
        "questionary.confirm",
        return_value=AsyncMock(ask_async=AsyncMock(return_value=False)),
    )
    result = await get_video_output_directory()
    assert result is None


@pytest.mark.asyncio
async def test_get_rate_limit(mocker):
    mocker.patch(
        "questionary.select",
        return_value=AsyncMock(ask_async=AsyncMock(return_value="1M")),
    )
    result = await get_rate_limit()
    assert result == 1024 * 1024


def test_parse_rate_limit_valid():
    assert parse_rate_limit("500K") == 500 * 1024
    assert parse_rate_limit("2M") == 2 * 1024 * 1024


def test_parse_rate_limit_no_limit():
    assert parse_rate_limit("No limit") is None


def test_parse_rate_limit_invalid(capfd):
    result = parse_rate_limit("Invalid")
    out, err = capfd.readouterr()
    assert "Invalid rate limit" in out
    assert result is None


@pytest.mark.asyncio
async def test_get_max_concurrent(mocker):
    mocker.patch(
        "questionary.select",
        return_value=AsyncMock(ask_async=AsyncMock(return_value="5")),
    )
    result = await get_max_concurrent()
    assert result == 5


@pytest.mark.asyncio
async def test_get_url(mocker):
    mocker.patch(
        "questionary.text",
        return_value=AsyncMock(ask_async=AsyncMock(return_value="https://example.com")),
    )
    result = await get_url()
    assert result == "https://example.com"


@pytest.mark.asyncio
async def test_get_cookies_file_exists(mocker):
    mocker.patch(
        "questionary.confirm",
        return_value=AsyncMock(ask_async=AsyncMock(return_value=True)),
    )
    mocker.patch(
        "questionary.text",
        return_value=AsyncMock(ask_async=AsyncMock(return_value="cookies.txt")),
    )
    mocker.patch("os.path.isfile", return_value=True)
    result = await get_cookies_file()
    assert result == "cookies.txt"


@pytest.mark.asyncio
async def test_get_cookies_file_not_exists(mocker, capfd):
    mocker.patch(
        "questionary.confirm",
        return_value=AsyncMock(ask_async=AsyncMock(return_value=True)),
    )
    mocker.patch(
        "questionary.text",
        return_value=AsyncMock(ask_async=AsyncMock(return_value="cookies.txt")),
    )
    mocker.patch("os.path.isfile", return_value=False)
    result = await get_cookies_file()
    captured = capfd.readouterr()
    assert "Cookies file not found" in captured.out
    assert result is None


@pytest.mark.asyncio
async def test_get_cookies_file_not_used(mocker):
    mocker.patch(
        "questionary.confirm",
        return_value=AsyncMock(ask_async=AsyncMock(return_value=False)),
    )
    result = await get_cookies_file()
    assert result is None


@pytest.mark.asyncio
async def test_get_user_input(mocker):
    mocker.patch("main.get_url", AsyncMock(return_value="https://example.com"))
    mocker.patch("main.get_cookies_file", AsyncMock(return_value="cookies.txt"))
    result = await get_user_input()
    assert result["url"] == "https://example.com"
    assert result["cookies_file"] == "cookies.txt"


def test_get_ydl_options(tmp_path):
    output_path = tmp_path / "downloads"
    video_output_path = tmp_path / "videos"
    ydl_opts = get_ydl_options(
        output_path=str(output_path),
        rate_limit=1024,
        download_type="audio",
        audio_quality="192",
        video_quality="720",
        video_output_dir=str(video_output_path),
        cookies_file="cookies.txt",
    )
    assert ydl_opts["paths"]["home"] == str(output_path)
    assert ydl_opts["paths"]["video"] == str(video_output_path)
    assert ydl_opts["format"] == "bestaudio/best"
    assert ydl_opts["postprocessors"][0]["preferredquality"] == "192"
    assert ydl_opts["ratelimit"] == 1024
    assert ydl_opts["cookiefile"] == "cookies.txt"


def test_initialize_ydl_options(tmp_path):
    output_path = tmp_path / "downloads"
    video_output_path = tmp_path / "videos"
    ydl_opts = initialize_ydl_options(
        str(output_path), str(video_output_path), "cookies.txt"
    )
    assert ydl_opts["paths"]["home"] == str(output_path)
    assert ydl_opts["paths"]["video"] == str(video_output_path)
    assert ydl_opts["cookiefile"] == "cookies.txt"


def test_get_format_string():
    assert get_format_string("audio", "1080") == "bestaudio/best"
    assert (
        get_format_string("video", "720")
        == "bestvideo[height<=720]+bestaudio/best[height<=720]"
    )
    assert (
        get_format_string("both", "1080")
        == "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    )
    assert get_format_string("other", "480") == "best"


def test_get_postprocessors():
    audio_pps = get_postprocessors("audio", "256")
    assert audio_pps[0]["preferredquality"] == "256"

    both_pps = get_postprocessors("both", "256")
    assert both_pps[0]["key"] == "FFmpegVideoConvertor"

    video_pps = get_postprocessors("video", "256")
    assert video_pps == []


def test_is_valid_entry():
    valid_entry = {"webpage_url": "http://example.com", "title": "Test Video"}
    invalid_entry = {"webpage_url": "http://example.com"}
    assert is_valid_entry(valid_entry) is True
    assert is_valid_entry(invalid_entry) is False


def test_update_output_template():
    template = update_output_template("Test_Video", "12345")
    assert template == "12345_Test_Video.%(ext)s"


def test_create_progress_bar():
    bar = create_progress_bar("Test Video")
    assert bar.total == 100
    bar.close()


def test_progress_hook_downloading():
    progress = Mock()
    d = {"status": "downloading", "downloaded_bytes": 50, "total_bytes": 100}
    progress_hook(d, progress)
    assert progress.n == 50.0
    progress.refresh.assert_called_once()


def test_progress_hook_finished():
    progress = Mock()
    d = {"status": "finished"}
    progress_hook(d, progress)
    assert progress.n == 100
    progress.refresh.assert_called_once()
    progress.close.assert_called_once()


def test_determine_if_playlist():
    assert determine_if_playlist({"entries": []}) is True
    assert determine_if_playlist({"id": "abc"}) is False


@pytest.mark.asyncio
async def test_get_quality_audio(mocker):
    mocker.patch("main.get_audio_quality", AsyncMock(return_value="320"))
    qualities = await get_quality("audio")
    assert qualities["audio"] == "320"
    assert qualities["video"] is None


@pytest.mark.asyncio
async def test_get_quality_video(mocker):
    mocker.patch("main.get_video_quality", AsyncMock(return_value="1080"))
    qualities = await get_quality("video")
    assert qualities["video"] == "1080"
    assert qualities["audio"] is None


@pytest.mark.asyncio
async def test_get_quality_both(mocker):
    mocker.patch("main.get_audio_quality", AsyncMock(return_value="256"))
    mocker.patch("main.get_video_quality", AsyncMock(return_value="720"))
    qualities = await get_quality("both")
    assert qualities["audio"] == "256"
    assert qualities["video"] == "720"


def test_prepare_ydl_options(tmp_path):
    output_path = tmp_path / "downloads"
    video_output_path = tmp_path / "videos"
    user_options = {
        "output_dir": str(output_path),
        "rate_limit": 1024,
        "download_type": "audio",
        "audio_quality": "192",
        "video_quality": "720",
        "video_output_dir": str(video_output_path),
    }
    ydl_opts = prepare_ydl_options(user_options, cookies_file="cookies.txt")
    assert ydl_opts["paths"]["home"] == str(output_path)
    assert ydl_opts["paths"]["video"] == str(video_output_path)
    assert ydl_opts["cookiefile"] == "cookies.txt"


@pytest.mark.asyncio
async def test_extract_info_success(mocker):
    # Mock the event loop's run_in_executor to return a Future with desired result
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    future.set_result({"id": "123", "title": "Test Video"})
    mocker.patch.object(loop, "run_in_executor", return_value=future)
    mocker.patch("asyncio.get_event_loop", return_value=loop)

    # Mock yt_dlp.YoutubeDL context manager and extract_info method
    ydl_mock = MagicMock()
    ydl_instance = MagicMock()
    ydl_instance.extract_info = MagicMock()
    ydl_mock.return_value.__enter__.return_value = ydl_instance
    mocker.patch("yt_dlp.YoutubeDL", ydl_mock)

    # Mock show_spinner to prevent actual spinner
    mocker.patch("main.show_spinner", return_value=AsyncMock())

    info = await extract_info("http://example.com", {}, asyncio.Event())
    assert info["id"] == "123"


@pytest.mark.asyncio
async def test_extract_info_error(mocker, capsys):
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    future.set_exception(Exception("Error"))
    mocker.patch.object(loop, "run_in_executor", return_value=future)
    mocker.patch("asyncio.get_event_loop", return_value=loop)

    ydl_mock = MagicMock()
    ydl_instance = MagicMock()
    ydl_instance.extract_info = MagicMock()
    ydl_mock.return_value.__enter__.return_value = ydl_instance
    mocker.patch("yt_dlp.YoutubeDL", ydl_mock)

    mocker.patch("main.show_spinner", return_value=AsyncMock())

    info = await extract_info("http://example.com", {}, asyncio.Event())
    out, err = capsys.readouterr()
    assert "Error processing the URL" in out
    assert info is None


@pytest.mark.asyncio
async def test_download_entry_valid(mocker):
    entry = {"webpage_url": "http://example.com", "title": "Test Video", "id": "123"}
    mocker.patch("main.is_valid_entry", return_value=True)
    mocker.patch("main.sanitize_filename", return_value="Test_Video")
    mocker.patch("main.update_output_template", return_value="123_Test_Video.%(ext)s")
    mocker.patch("main.create_progress_bar", return_value=Mock())
    mock_perform_download = mocker.patch("main.perform_download", AsyncMock())
    await download_entry(entry, {}, asyncio.Lock())
    mock_perform_download.assert_awaited_once()


@pytest.mark.asyncio
async def test_download_entry_invalid(mocker, capfd):
    entry = {"webpage_url": "http://example.com"}
    mocker.patch("main.is_valid_entry", return_value=False)
    await download_entry(entry, {}, asyncio.Lock())
    out, err = capfd.readouterr()
    combined_output = out + err
    ansi_escape = re.compile(r"\x1b\[[0-9;]*m")
    output_stripped = ansi_escape.sub("", combined_output)
    output_cleaned = output_stripped.strip()
    print(combined_output)
    assert "Invalid entry detected. Skipping." in output_cleaned


def test_update_progress_bar():
    progress = Mock()
    d = {"downloaded_bytes": 50, "total_bytes": 100}
    update_progress_bar(d, progress)
    assert progress.n == 50.0
    progress.refresh.assert_called_once()


def test_complete_progress_bar():
    progress = Mock()
    complete_progress_bar(progress)
    assert progress.n == 100
    progress.refresh.assert_called_once()
    progress.close.assert_called_once()


@pytest.mark.asyncio
async def test_perform_download_success(mocker):
    ytdl_mock = MagicMock()
    ytdl_instance = MagicMock()
    ytdl_instance.extract_info = MagicMock(
        return_value={"id": "123", "title": "Test Video"}
    )
    ytdl_instance.prepare_filename = MagicMock(return_value="Test_Video.mp4")
    ytdl_mock.return_value.__enter__.return_value = ytdl_instance
    mocker.patch("yt_dlp.YoutubeDL", ytdl_mock)
    progress = Mock()
    await perform_download("http://example.com", {}, progress, asyncio.Lock())
    progress.close.assert_called_once()


@pytest.mark.asyncio
async def test_perform_download_cancelled(mocker, capsys):
    # Define mock_extract_info as a synchronous function
    def mock_extract_info(*args, **kwargs):
        raise asyncio.CancelledError()

    # Mock yt_dlp.YoutubeDL context manager and methods
    ydl_mock = MagicMock()
    ydl_instance = MagicMock()
    ydl_instance.extract_info = mock_extract_info
    ydl_instance.prepare_filename = MagicMock()
    ydl_mock.return_value.__enter__.return_value = ydl_instance
    mocker.patch("yt_dlp.YoutubeDL", ydl_mock)

    progress = Mock()
    await perform_download(
        "http://example.com", {"outtmpl": "template"}, progress, asyncio.Lock()
    )
    out, err = capsys.readouterr()
    assert "Download cancelled" in out
    progress.close.assert_called_once()


@pytest.mark.asyncio
async def test_perform_download_exception(mocker, capsys):
    def mock_extract_info(*args, **kwargs):
        raise Exception("Error")

    ytdl_mock = MagicMock()
    ytdl_instance = MagicMock()
    ytdl_instance.extract_info = mock_extract_info
    ytdl_instance.prepare_filename = MagicMock()
    ytdl_mock.return_value.__enter__.return_value = ytdl_instance
    mocker.patch("yt_dlp.YoutubeDL", ytdl_mock)

    progress = Mock()
    await perform_download(
        "http://example.com", {"outtmpl": "template"}, progress, asyncio.Lock()
    )
    out, err = capsys.readouterr()
    assert "Error downloading: Error" in out
    progress.close.assert_called_once()


@pytest.mark.asyncio
async def test_process_entries_no_entries(capfd):
    await process_entries([], {}, 5, asyncio.Event())
    out, err = capfd.readouterr()
    assert "No entries found to download." in out


@pytest.mark.asyncio
async def test_create_download_tasks(mocker):
    entries = [{"id": "1"}, {"id": "2"}]
    asyncio.Semaphore(2)
    shutdown_event = asyncio.Event()
    lock = asyncio.Lock()
    tasks = create_download_tasks(entries, {}, 2, shutdown_event, lock)
    assert len(tasks) == 2


@pytest.mark.asyncio
async def test_download_with_semaphore(mocker):
    entry = {"webpage_url": "http://example.com", "title": "Test Video"}
    mock_download_entry = mocker.patch("main.download_entry", AsyncMock())
    await download_with_semaphore(
        entry, {}, asyncio.Semaphore(1), asyncio.Event(), asyncio.Lock()
    )
    mock_download_entry.assert_awaited_once()


@pytest.mark.asyncio
async def test_show_spinner():
    stop_event = asyncio.Event()
    spinner_task = asyncio.create_task(show_spinner("Processing...", stop_event))
    await asyncio.sleep(0.2)
    stop_event.set()
    await spinner_task


@pytest.mark.asyncio
async def test_handle_playlist_empty(capfd):
    await handle_playlist({"entries": []}, {}, 5, asyncio.Event())
    out, err = capfd.readouterr()
    assert "The playlist appears to be empty." in out


@pytest.mark.asyncio
async def test_handle_playlist_entries(mocker):
    mock_process_entries = mocker.patch("main.process_entries", AsyncMock())
    await handle_playlist({"entries": [{"id": "1"}]}, {}, 5, asyncio.Event())
    mock_process_entries.assert_awaited_once()


@pytest.mark.asyncio
async def test_download_media_no_info(mocker):
    mocker.patch("main.extract_info", AsyncMock(return_value=None))
    mocker.patch("main.gather_user_options", AsyncMock())
    mock_shutdown_event = asyncio.Event()
    await download_media({"url": "http://example.com"}, mock_shutdown_event)
    # Ensure that no exception is raised


@pytest.mark.asyncio
async def test_shutdown(mocker):
    loop = asyncio.get_event_loop()
    mock_task = asyncio.create_task(asyncio.sleep(0.1))
    await shutdown(loop)
    assert mock_task.cancelled()
