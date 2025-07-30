#!/usr/bin/env python3

"""Archiver ZIM - A tool to download videos and podcasts from various platforms and create ZIM archives."""

# Copyright (c) 2025 Sudo-Ivan
# Licensed under the MIT License (see LICENSE file for details)

import asyncio
import json
import logging
import random
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import click
from libzim.writer import Creator, FileProvider, Hint, Item, StringProvider
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)


class OutputFilter(logging.Filter):
    """Add a custom filter to separate debug messages and command line config."""

    def filter(self, record):
        msg = record.getMessage()
        return not any(
            [
                # Debug messages
                msg.startswith("[debug]"),
                msg.startswith("Command-line config:"),
                msg.startswith("Encodings:"),
                # File paths and line numbers
                'File "' in msg and "line" in msg,
                "raise " in msg,
                "~~~~~~~~~~~~~~~~~~~~~" in msg,
                # Internal yt-dlp messages
                "ie_result = self._real_extract" in msg,
                "self.raise_no_formats" in msg,
                "raise ExtractorError" in msg,
                # Redundant download status
                "Downloading webpage" in msg,
                "Downloading tv client config" in msg,
                "Downloading tv player API JSON" in msg,
                "Downloading ios player API JSON" in msg,
                "Extracting URL:" in msg,
                "Writing playlist metadata" in msg,
                "Writing playlist description" in msg,
                "Deleting existing file" in msg,
                "Downloading playlist thumbnail" in msg,
                "Writing playlist thumbnail" in msg,
                "Playlist " in msg and "Downloading" in msg and "items of" in msg,
                # Additional debug patterns
                "Downloading " in msg and "API JSON" in msg,
                "Redownloading playlist API JSON" in msg,
                "page 1: Downloading API JSON" in msg,
                "ios client https formats require a GVS PO Token" in msg,
            ]
        )


class YouTubeAuthError(Exception):
    """Custom exception for YouTube authentication errors."""

    pass


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=False, markup=True, show_time=False)],
)
log = logging.getLogger("archiver")
console = Console()

# Add filter to root logger
logging.getLogger().addFilter(OutputFilter())


def handle_youtube_auth_error(error_msg: str) -> None:
    """Handle YouTube authentication errors with a user-friendly message.

    Args:
        error_msg: The error message from yt-dlp

    """
    log.error(
        "[red]❌ YouTube authentication required. Please use one of these options:[/red]"
    )
    log.error("[yellow]1. Use --cookies-from-browser option (recommended):[/yellow]")
    log.error("   archiver-zim archive URL --cookies-from-browser firefox")
    log.error("   archiver-zim archive URL --cookies-from-browser chrome")
    log.error("   archiver-zim archive URL --cookies-from-browser chromium")
    log.error("   archiver-zim archive URL --cookies-from-browser brave")
    log.error("   archiver-zim archive URL --cookies-from-browser edge")
    log.error("   archiver-zim archive URL --cookies-from-browser opera")
    log.error("   archiver-zim archive URL --cookies-from-browser vivaldi")
    log.error("\n[yellow]2. Use --cookies option with a cookies file:[/yellow]")
    log.error("   archiver-zim archive URL --cookies /path/to/cookies.txt")
    log.error("\n[dim]For more details, see:[/dim]")
    log.error(
        "[blue]https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp[/blue]"
    )
    log.error(
        "\n[yellow]Note:[/yellow] Make sure you are logged into YouTube in your browser before using --cookies-from-browser"
    )
    raise YouTubeAuthError("YouTube authentication required")


def handle_playlist_error(error_msg: str) -> None:
    """Handle playlist download errors with a user-friendly message.

    Args:
        error_msg: The error message from yt-dlp

    """
    log.error("[red]❌ Playlist download failed. Please check:[/red]")
    log.error("[yellow]1. The playlist is public and accessible[/yellow]")
    log.error("[yellow]2. You have proper authentication if required[/yellow]")
    log.error(
        "[yellow]3. Try downloading with a lower concurrent download limit[/yellow]"
    )
    log.error("[yellow]4. Try downloading in smaller batches[/yellow]")


class MediaItem(Item):
    """Custom Item class for media content."""

    def __init__(
        self, title: str, path: str, content: str = "", fpath: Optional[str] = None
    ):
        """Initialize a MediaItem.

        Args:
            title: The title of the media item.
            path: The path for the media item in the ZIM archive.
            content: The HTML content of the media item.
            fpath: The file path to the media item, if it exists.

        """
        super().__init__()
        self.path = path
        self.title = title
        self.content = content
        self.fpath = fpath

    def get_path(self):
        """Return the path of the media item."""
        return self.path

    def get_title(self):
        """Return the title of the media item."""
        return self.title

    @staticmethod
    def get_mimetype():
        """Return the MIME type of the media item."""
        return "text/html"

    def get_contentprovider(self):
        """Return the content provider for the media item."""
        if self.fpath is not None:
            return FileProvider(self.fpath)
        return StringProvider(self.content)

    @staticmethod
    def get_hints():
        """Return hints for the media item."""
        return {Hint.FRONT_ARTICLE: True}


class Archiver:
    """Main class for media archiving functionality."""

    def __init__(
        self,
        output_dir: str,
        quality: str = "best",
        retry_count: int = 3,
        retry_delay: int = 5,
        max_retries: int = 10,
        max_concurrent_downloads: int = 3,
        dry_run: bool = False,
        cookies: Optional[str] = None,
        cookies_from_browser: Optional[str] = None,
    ):
        """Initialize the Archiver.

        Args:
            output_dir: Directory to store downloaded media and ZIM files.
            quality: Video quality setting (e.g., "best", "720p", "480p").
            retry_count: Number of retries for failed downloads.
            retry_delay: Base delay between retries in seconds.
            max_retries: Maximum number of retries before giving up.
            max_concurrent_downloads: Maximum number of concurrent downloads.
            dry_run: If True, only simulate operations without downloading.
            cookies: Path to cookies file.
            cookies_from_browser: Browser to extract cookies from (e.g., "firefox", "chrome").

        """
        self.output_dir = Path(output_dir)
        self.quality = quality
        self.media_dir = self.output_dir / "media"
        self.metadata_dir = self.output_dir / "metadata"
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.max_retries = max_retries
        self.max_concurrent_downloads = max_concurrent_downloads
        self.download_semaphore = asyncio.Semaphore(max_concurrent_downloads)
        self.download_progress: dict[str, float] = {}
        self.dry_run = dry_run
        self.cookies = cookies
        self.cookies_from_browser = cookies_from_browser
        self.logger = logging.getLogger("archiver")

        try:
            yt_dlp_path = shutil.which("yt-dlp")
            if not yt_dlp_path:
                raise RuntimeError("yt-dlp is not installed or not in PATH")

            result = subprocess.run(
                [yt_dlp_path, "--version"], capture_output=True, text=True, check=True
            )
            self.logger.info("Using yt-dlp version: %s", result.stdout.strip())
        except Exception as e:
            raise RuntimeError(f"Failed to check yt-dlp installation: {e}")

        if not dry_run:
            self.media_dir.mkdir(parents=True, exist_ok=True)
            self.metadata_dir.mkdir(parents=True, exist_ok=True)

    def get_archive_info(self) -> dict[str, Any]:
        """Get information about the current archive state.

        Returns:
            Dict containing archive information.

        """
        return {
            "output_dir": str(self.output_dir),
            "media_count": len(list(self.media_dir.glob("*")))
            if self.media_dir.exists()
            else 0,
            "metadata_count": len(list(self.metadata_dir.glob("*")))
            if self.metadata_dir.exists()
            else 0,
            "last_update": datetime.now().isoformat()
            if self.media_dir.exists()
            else None,
        }

    @staticmethod
    def _get_random_user_agent() -> str:
        """Get a random user agent to avoid detection."""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        ]
        return random.choice(user_agents)  # noqa: S311

    @staticmethod
    def _add_random_delay():
        """Add a random delay to avoid rate limiting."""
        delay = random.uniform(1, 3)  # noqa: S311
        time.sleep(delay)

    async def _download_video_async(
        self, url: str, date: Optional[str] = None, title_filter: Optional[str] = None
    ) -> bool:
        """Asynchronously download a video with retry logic.

        Args:
            url: The URL of the video or playlist/channel to download.
            date: An optional date to filter the video by.
            title_filter: Filter videos by title (case-insensitive partial match).

        Returns:
            True if the download process completed without fatal errors (even if no files were downloaded due to filters), False otherwise.

        """
        if self.dry_run:
            self.logger.info("[DRY RUN] Would download from %s", url)
            return True

        async with self.download_semaphore:
            retries = 0
            download_occurred = False  # Flag to track if any download started

            while retries < self.max_retries:
                try:
                    cmd = [
                        "yt-dlp",
                        "--write-description",
                        "--write-info-json",
                        "--write-thumbnail",
                        "--user-agent",
                        self._get_random_user_agent(),
                        "--socket-timeout",
                        "60",
                        "--retries",
                        str(self.retry_count),
                        "--fragment-retries",
                        str(self.retry_count),
                        "--file-access-retries",
                        str(self.retry_count),
                        "--extractor-retries",
                        str(self.retry_count),
                        "--ignore-errors",
                        "--no-warnings",
                        "--progress",
                        "--newline",
                        "--write-sub",
                        "--write-auto-sub",
                        "--embed-chapters",
                        "--max-filesize",
                        "2G",
                        "--retry-sleep",
                        "5",
                        "-o",
                        str(self.media_dir / "%(id)s.%(ext)s"),
                        "--merge-output-format",
                        "mp4",
                        "--verbose",
                        "--yes-playlist",
                        "--break-on-existing",
                        "--concurrent-fragments",
                        "1",
                        "--extractor-args",
                        "youtube:formats=missing_pot",
                    ]

                    if self.cookies:
                        cmd.extend(["--cookies", self.cookies])
                    elif self.cookies_from_browser:
                        cmd.extend(
                            ["--cookies-from-browser", self.cookies_from_browser]
                        )

                    if self.quality != "best":
                        cmd.extend(
                            [
                                "-f",
                                f"bestvideo[height<={self.quality[:-1]}]+bestaudio/best[height<={self.quality[:-1]}]",
                            ]
                        )

                    if date:
                        cmd.extend(["--date", date])

                    if title_filter:
                        cmd.extend(["--match-filter", f"title ~= '(?i){title_filter}'"])

                    cmd.append(url)

                    # Reset flag for this attempt
                    download_occurred = False
                    process = await asyncio.create_subprocess_exec(
                        *cmd,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )

                    output_lines = []
                    error_lines = []
                    current_progress = 0
                    current_file = ""
                    filter_rejection_logged = False

                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        TaskProgressColumn(),
                        TimeRemainingColumn(),
                        console=console,
                        transient=True,
                        refresh_per_second=10,
                        expand=True,
                    ) as progress:
                        task = progress.add_task("Processing...", total=None)

                        while True:
                            try:
                                stdout_line = await asyncio.wait_for(
                                    process.stdout.readline(), timeout=300
                                )
                                stderr_line = await asyncio.wait_for(
                                    process.stderr.readline(), timeout=300
                                )

                                if not stdout_line and not stderr_line:
                                    break

                                if stdout_line:
                                    line_str = stdout_line.decode().strip()
                                    output_lines.append(line_str)

                                    if "[download] Destination:" in line_str:
                                        download_occurred = True  # Set flag
                                        current_file = line_str.split("Destination:")[
                                            1
                                        ].strip()
                                        progress.update(
                                            task,
                                            description=f"Downloading {Path(current_file).name}",
                                            total=100,
                                            completed=0,
                                        )
                                    elif "[download]" in line_str and "%" in line_str:
                                        # Progress update logic... (unchanged)
                                        try:
                                            if "of" in line_str:
                                                parts = line_str.split()
                                                percent = float(
                                                    parts[1].replace("%", "")
                                                )
                                                current_progress = percent
                                            else:
                                                percent = float(
                                                    line_str.split("%")[0].split()[-1]
                                                )
                                                current_progress = percent
                                            progress.update(
                                                task, completed=current_progress
                                            )
                                        except (ValueError, IndexError):
                                            pass
                                    elif (
                                        "[download]" in line_str
                                        and "has already been downloaded" in line_str
                                    ):
                                        # Already downloaded logic... (unchanged)
                                        current_file = (
                                            line_str.split("download]")[1]
                                            .split("has")[0]
                                            .strip()
                                        )
                                        progress.update(
                                            task,
                                            completed=100,
                                            description=f"Skipped {Path(current_file).name} (exists)",
                                        )
                                        progress.reset(
                                            task, description="Processing..."
                                        )
                                    # Log info messages sparingly (unchanged)
                                    elif "[info] Downloading playlist:" in line_str:
                                        self.logger.info(
                                            "[yellow]📋 %s[/yellow]",
                                            line_str.split("[info]")[1].strip(),
                                        )
                                        progress.update(
                                            task,
                                            description="Fetching playlist items...",
                                        )
                                    elif (
                                        "[info] Downloading" in line_str
                                        and " items " in line_str
                                    ):
                                        self.logger.info(
                                            "[cyan]📥 %s[/cyan]",
                                            line_str.split("[info]")[1].strip(),
                                        )
                                    elif "[info] Downloading item " in line_str:
                                        item_desc = line_str.split("[info]")[1].strip()
                                        progress.update(
                                            task,
                                            description=item_desc,
                                            total=None,
                                            completed=0,
                                        )
                                    elif (
                                        "[yt-dlp]" in line_str
                                        and "Downloading" in line_str
                                        and "webpage" in line_str
                                    ):
                                        progress.update(
                                            task, description="Fetching page info..."
                                        )

                                if stderr_line:
                                    line_str = stderr_line.decode().strip()
                                    error_lines.append(line_str)
                                    # Log errors and warnings (unchanged)
                                    if "ERROR:" in line_str:
                                        # Check for filter rejection message
                                        if (
                                            "Did not match filter" in line_str
                                            and not filter_rejection_logged
                                        ):
                                            self.logger.info(
                                                "[yellow]ℹ️ Item rejected by filter: %s[/yellow]",
                                                line_str.split("ERROR:")[1].strip(),
                                            )
                                            filter_rejection_logged = True  # Log only the first one to avoid spam
                                        # Handle specific errors (unchanged)
                                        elif any(
                                            x in line_str.lower()
                                            for x in [
                                                "sign in to confirm you're not a bot",
                                                "authentication required",
                                                "login required",
                                                "private video",
                                                "video unavailable",
                                                "this video is private",
                                                "this video is unavailable",
                                                "this playlist is private",
                                                "this playlist is unavailable",
                                            ]
                                        ):
                                            handle_youtube_auth_error(line_str)
                                        elif "playlist" in url.lower() and any(
                                            x in line_str.lower()
                                            for x in ["failed", "error", "not found"]
                                        ):
                                            handle_playlist_error(line_str)
                                        # Log general errors
                                        else:
                                            self.logger.error(
                                                "[red]❌ %s[/red]",
                                                line_str.split("ERROR:")[1].strip(),
                                            )
                                    elif not line_str.startswith("[debug]"):
                                        self.logger.warning(
                                            "[yellow]⚠️ %s[/yellow]", line_str
                                        )

                            except asyncio.TimeoutError:
                                self.logger.warning(
                                    "[yellow]⚠️ Process timeout, retrying...[/yellow]"
                                )
                                if process and process.returncode is None:
                                    process.terminate()
                                    await process.wait()
                                raise TimeoutError("yt-dlp operation timed out")
                            except Exception as e:
                                self.logger.error(
                                    "[red]Error reading process output: %s[/red]", e
                                )
                                if process and process.returncode is None:
                                    process.terminate()
                                    await process.wait()
                                raise

                    await process.wait()

                    # Check results after process finishes
                    if process.returncode == 0:
                        if not download_occurred:
                            # yt-dlp succeeded but didn't download anything
                            if title_filter:
                                self.logger.info(
                                    "[yellow]ℹ️ yt-dlp finished successfully for %s, but no videos matched the title filter.[/yellow]",
                                    url,
                                )
                            elif date:
                                self.logger.info(
                                    "[yellow]ℹ️ yt-dlp finished successfully for %s, but no videos matched the date filter.[/yellow]",
                                    url,
                                )
                            else:
                                self.logger.info(
                                    "[yellow]ℹ️ yt-dlp finished successfully for %s, but found no videos to download (maybe empty or already downloaded).[/yellow]",
                                    url,
                                )
                        # Consider success even if nothing new downloaded
                        # Move metadata if any exists from previous runs or info gathering
                        for file in (
                            self.media_dir.glob(f"{Path(url).name}*")
                            if not Path(url).suffix
                            else self.media_dir.glob(f"{Path(url).stem}*")
                        ):  # Guess pattern
                            if file.suffix.lower() in [
                                ".description",
                                ".info.json",
                                ".jpg",
                                ".webp",
                                ".vtt",
                                ".srt",
                            ]:
                                try:
                                    new_path = self.metadata_dir / file.name
                                    if not new_path.exists():
                                        file.rename(new_path)
                                except Exception as e:
                                    self.logger.warning(
                                        "Could not move metadata file %s: %s",
                                        file.name,
                                        e,
                                    )
                        return True  # Process completed without fatal error

                    elif process.returncode == 101:
                        # Exit code 101 specifically means all items were filtered out
                        self.logger.info(
                            "[yellow]ℹ️ All items from %s were filtered out by specified filters (title, date, etc.).[/yellow]",
                            url,
                        )
                        return True  # Not a failure state for the archiver itself

                    else:  # Actual error
                        error_msg = (
                            "\\n".join(error_lines)
                            if error_lines
                            else "\\n".join(output_lines[-10:])
                        )
                        self.logger.error(
                            "[red]yt-dlp exited with code %s for %s[/red]",
                            process.returncode,
                            url,
                        )
                        raise subprocess.CalledProcessError(
                            process.returncode, cmd, error_msg
                        )

                except YouTubeAuthError:
                    raise  # Propagate auth errors immediately
                except (TimeoutError, subprocess.CalledProcessError, Exception) as e:
                    retries += 1
                    if retries >= self.max_retries:
                        error_msg = str(e)
                        if isinstance(
                            e, subprocess.CalledProcessError
                        ):  # Check if it has output attribute
                            error_output = getattr(e, "output", None) or getattr(
                                e, "stderr", None
                            )
                            if error_output:
                                if isinstance(error_output, bytes):
                                    try:
                                        error_output = error_output.decode()
                                    except Exception as decode_err:  # Catch specific decode errors if possible, fallback to Exception
                                        self.logger.warning(
                                            "Could not decode error output: %s",
                                            decode_err,
                                        )  # Log the decoding error
                                        pass  # Keep as bytes if decode fails
                                error_msg += f"\nOutput:\n{error_output}"

                        self.logger.error(
                            "[red]❌ Failed download/processing for %s after %s attempts: %s[/red]",
                            url,
                            self.max_retries,
                            error_msg,
                        )
                        return False  # Indicate failure for this URL

                    delay = self.retry_delay * (2**retries)
                    self.logger.warning(
                        "[yellow]⚠️ Download/processing failed for %s, retrying in %s seconds... (Attempt %s/%s)[/yellow]",
                        url,
                        delay,
                        retries,
                        self.max_retries,
                    )
                    await asyncio.sleep(delay)
                    self._add_random_delay()

            # If loop finishes after max_retries without success
            self.logger.error(
                "[red]❌ Failed download/processing for %s after exhausting retries.[/red]",
                url,
            )
            return False

    async def download_media_async(
        self,
        urls: list[str],
        date: Optional[str] = None,
        date_limit: Optional[int] = None,
        month_limit: Optional[int] = None,
        title_filter: Optional[str] = None,
    ) -> dict[str, bool]:
        """Download multiple media items concurrently.

        Args:
            urls: A list of media URLs to download.
            date: An optional date to filter videos by.
            date_limit: Download only podcast episodes from the last N days.
            month_limit: Download only podcast episodes from the last N months.
            title_filter: Filter videos by title (case-insensitive partial match).

        Returns:
            A dictionary mapping each URL to a boolean indicating download process completion status.

        """
        tasks = []
        results_dict = {}
        for url in urls:
            if any(url.endswith(ext) for ext in [".xml", ".atom", ".json", ".rss"]):
                tasks.append(self._download_podcast_async(url, date_limit, month_limit))
                # Associate task with URL for result mapping later if needed, though podcasts are simpler
            else:
                # Create task and store it with its URL
                task = asyncio.create_task(
                    self._download_video_async(url, date, title_filter)
                )
                tasks.append(task)
                results_dict[task] = url  # Map task back to URL

        # Gather results
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results and map back to URLs
        final_results = {}
        task_to_url = dict(results_dict.items())
        podcast_urls = [
            url for url in urls if url.endswith((".xml", ".atom", ".json", ".rss"))
        ]
        podcast_idx = 0

        for i, result in enumerate(results):
            url = ""
            is_podcast = False
            # Find the URL associated with this result/exception
            # This mapping is a bit complex because gather mixes results and exceptions
            # Attempt to map based on task identity if possible
            original_task = tasks[i]
            if original_task in task_to_url:
                url = task_to_url[original_task]
            elif podcast_idx < len(podcast_urls):
                url = podcast_urls[podcast_idx]
                is_podcast = True
                podcast_idx += 1

            if isinstance(result, Exception):
                self.logger.error(
                    "[red]❌ Unhandled exception during processing %s: %s[/red]",
                    url,
                    result,
                )
                final_results[url] = False
            elif is_podcast:
                # Assume podcast result corresponds to the next podcast URL
                final_results[url] = result  # result is the boolean status
            else:
                # Video result
                final_results[url] = result  # result is the boolean status

        # Ensure all original URLs have a result (important if some task failed very early)
        for url in urls:
            if url not in final_results:
                final_results[url] = False  # Assume failure if no result mapped

        return final_results

    def download_media(
        self,
        urls: list[str],
        date: Optional[str] = None,
        date_limit: Optional[int] = None,
        month_limit: Optional[int] = None,
        title_filter: Optional[str] = None,
    ) -> dict[str, bool]:
        """Download multiple media items with progress tracking.

        Args:
            urls: A list of media URLs to download.
            date: An optional date to filter videos by.
            date_limit: Download only podcast episodes from the last N days.
            month_limit: Download only podcast episodes from the last N months.
            title_filter: Filter videos by title (case-insensitive partial match).

        Returns:
            A dictionary mapping each URL to a boolean indicating download process completion status.

        """
        return asyncio.run(
            self.download_media_async(urls, date, date_limit, month_limit, title_filter)
        )

    @staticmethod
    def verify_download(file_path: Path) -> bool:
        """Verify the download of a media file.

        Args:
            file_path: The path to the downloaded file.

        Returns:
            True if the file exists and is a file, False otherwise.

        """
        return file_path.exists() and file_path.is_file()

    def _get_media_metadata(self, media_file: Path) -> dict[str, Any]:
        """Extract media metadata including chapters and subtitles.

        Args:
            media_file: The path to the media file.

        Returns:
            A dictionary containing the media metadata.

        """
        metadata = {}
        json_file = media_file.with_suffix(".info.json")

        if json_file.exists():
            try:
                with open(json_file) as f:
                    metadata = json.load(f)
                    if "title" in metadata:
                        metadata["title"] = metadata["title"].strip()
                    if "description" in metadata:
                        metadata["description"] = metadata["description"].strip()
                    if "upload_date" in metadata:
                        try:
                            date = datetime.strptime(metadata["upload_date"], "%Y%m%d")
                            metadata["upload_date"] = date.strftime("%B %d, %Y")
                        except ValueError:
                            pass
                    if "playlist" in metadata and isinstance(
                        metadata["playlist"], dict
                    ):
                        metadata["playlist_title"] = metadata["playlist"].get(
                            "title", ""
                        )
                        metadata["playlist_index"] = metadata["playlist"].get(
                            "index", 0
                        )
                        metadata["playlist_id"] = metadata["playlist"].get("id", "")
                    elif (
                        "playlist" in metadata
                    ):  # Handle cases where 'playlist' might be a string or other non-dict type
                        self.logger.warning(
                            "Unexpected type for 'playlist' in metadata for %s: %s. Skipping playlist metadata.",
                            media_file.name,
                            type(metadata["playlist"]).__name__,
                        )
            except Exception as e:
                self.logger.error(
                    "Error reading metadata for %s: %s", media_file.name, e
                )
                return metadata

        subtitle_files = list(self.metadata_dir.glob(f"{media_file.stem}*.vtt")) + list(
            self.metadata_dir.glob(f"{media_file.stem}*.srt")
        )
        if subtitle_files:
            metadata["subtitles"] = [str(f.name) for f in subtitle_files]
        else:
            self.logger.info("No subtitles found for %s", media_file.name)

        if "chapters" not in metadata:
            self.logger.info("No chapters found for %s", media_file.name)

        return metadata

    def create_zim(self, title: str, description: str) -> bool:
        """Create a ZIM file from downloaded media.

        Args:
            title: The title of the ZIM archive.
            description: A description of the ZIM archive.

        Returns:
            True if the ZIM archive was created successfully, False otherwise.

        """
        if self.dry_run:
            self.logger.info("[DRY RUN] Would create ZIM archive with title: %s", title)
            return True

        try:
            zim_path = self.output_dir / f"{title.lower().replace(' ', '_')}.zim"
            lock = threading.Lock()

            with Creator(str(zim_path)).config_indexing(True, "eng") as creator:
                metadata = {
                    "creator": "Archiver ZIM",
                    "description": description,
                    "name": title.lower().replace(" ", "_"),
                    "publisher": "Archiver",
                    "title": title,
                    "language": "eng",
                    "date": datetime.now().strftime("%Y-%m-%d"),
                }

                for name, value in metadata.items():
                    creator.add_metadata(name.title(), value)

                creator.set_mainpath("index")

                # Only get media files (video and audio)
                media_files = [
                    f
                    for f in self.media_dir.glob("*.*")
                    if f.suffix.lower()
                    in [".mp4", ".webm", ".mkv", ".mp3", ".m4a", ".wav", ".ogg"]
                ]
                playlist_groups = {}
                standalone_videos = []

                for media_file in media_files:
                    media_metadata = self._get_media_metadata(media_file)
                    if media_metadata.get("playlist_id"):
                        playlist_id = media_metadata["playlist_id"]
                        if playlist_id not in playlist_groups:
                            playlist_groups[playlist_id] = {
                                "title": media_metadata.get("playlist_title", ""),
                                "videos": [],
                            }
                        playlist_groups[playlist_id]["videos"].append(
                            (media_file, media_metadata)
                        )
                    else:
                        standalone_videos.append((media_file, media_metadata))

                for playlist in playlist_groups.values():
                    playlist["videos"].sort(key=lambda x: x[1].get("playlist_index", 0))

                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    TimeRemainingColumn(),
                    console=console,
                    transient=True,
                    refresh_per_second=10,
                    expand=True,
                ) as progress:
                    task = progress.add_task(
                        "Creating ZIM archive...", total=len(media_files)
                    )

                    for media_file, media_metadata in standalone_videos + [
                        v for p in playlist_groups.values() for v in p["videos"]
                    ]:
                        with lock:
                            try:
                                mime_type = (
                                    "video/mp4"
                                    if media_file.suffix == ".mp4"
                                    else "audio/mpeg"
                                )

                                html_content = f"""
                                <!DOCTYPE html>
                                <html>
                                <head>
                                    <title>{media_metadata.get("title", media_file.stem)}</title>
                                    <meta charset="utf-8">
                                    <style>
                                        body {{
                                            font-family: Arial, sans-serif;
                                            line-height: 1.6;
                                            max-width: 1200px;
                                            margin: 0 auto;
                                            padding: 20px;
                                            background-color: #f9f9f9;
                                        }}
                                        .media-container {{
                                            width: 100%;
                                            margin: 20px 0;
                                            background-color: #000;
                                            position: relative;
                                            padding-top: 56.25%; /* 16:9 Aspect Ratio */
                                        }}
                                        video, audio {{
                                            position: absolute;
                                            top: 0;
                                            left: 0;
                                            width: 100%;
                                            height: 100%;
                                        }}
                                        .video-info {{
                                            margin: 20px 0;
                                            padding: 20px;
                                            background: #fff;
                                            border-radius: 8px;
                                            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                                        }}
                                        .video-title {{
                                            font-size: 24px;
                                            font-weight: bold;
                                            margin-bottom: 10px;
                                            color: #030303;
                                        }}
                                        .video-meta {{
                                            color: #606060;
                                            font-size: 14px;
                                            margin-bottom: 20px;
                                        }}
                                        .playlist-info {{
                                            margin-bottom: 20px;
                                            padding: 10px;
                                            background: #f8f8f8;
                                            border-radius: 4px;
                                        }}
                                        .playlist-info a {{
                                            color: #065fd4;
                                            text-decoration: none;
                                        }}
                                        .playlist-info a:hover {{
                                            text-decoration: underline;
                                        }}
                                        .video-description {{
                                            white-space: pre-wrap;
                                            word-wrap: break-word;
                                            color: #030303;
                                            font-size: 14px;
                                            line-height: 1.5;
                                            border-top: 1px solid #e5e5e5;
                                            padding-top: 20px;
                                        }}
                                        .chapters {{
                                            margin: 20px 0;
                                            padding: 20px;
                                            background: #fff;
                                            border-radius: 8px;
                                            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                                        }}
                                        .chapters h3 {{
                                            margin: 0 0 15px 0;
                                            color: #030303;
                                        }}
                                        .chapters ul {{
                                            list-style-type: none;
                                            padding: 0;
                                            margin: 0;
                                        }}
                                        .chapters li {{
                                            margin: 8px 0;
                                            padding: 8px 12px;
                                            cursor: pointer;
                                            border-radius: 4px;
                                            transition: background-color 0.2s;
                                        }}
                                        .chapters li:hover {{
                                            background-color: #f2f2f2;
                                        }}
                                    </style>
                                </head>
                                <body>
                                    <div class="video-info">
                                        <h1 class="video-title">{media_metadata.get("title", media_file.stem)}</h1>
                                        <div class="video-meta">
                                            {media_metadata.get("upload_date", "")}
                                        </div>
                                """

                                if media_metadata.get("playlist_id"):
                                    playlist = playlist_groups[
                                        media_metadata["playlist_id"]
                                    ]
                                    html_content += f"""
                                        <div class="playlist-info">
                                            Part of playlist: <a href="playlist_{media_metadata["playlist_id"]}">{playlist["title"]}</a>
                                            (Video {media_metadata.get("playlist_index", 0)} of {len(playlist["videos"])})
                                        </div>
                                    """

                                html_content += """
                                    </div>
                                    <div class="media-container">
                                """

                                if mime_type.startswith("video/"):
                                    html_content += f"""
                                        <video controls>
                                            <source src="{media_file.name}" type="{mime_type}">
                                            Your browser does not support the video tag.
                                        </video>
                                    """
                                else:
                                    html_content += f"""
                                        <audio controls>
                                            <source src="{media_file.name}" type="{mime_type}">
                                            Your browser does not support the audio tag.
                                        </audio>
                                    """

                                html_content += "</div>"

                                if "subtitles" in media_metadata:
                                    for subtitle in media_metadata["subtitles"]:
                                        html_content += f'<track src="{subtitle}" kind="subtitles" label="{subtitle.split(".")[-1].upper()}">\n'

                                if "chapters" in media_metadata:
                                    html_content += (
                                        '<div class="chapters"><h3>Chapters</h3><ul>\n'
                                    )
                                    for chapter in media_metadata["chapters"]:
                                        start_time = chapter.get("start_time", 0)
                                        title = chapter.get("title", "Untitled")
                                        html_content += f"<li onclick=\"document.querySelector('video,audio').currentTime = {start_time}\">{title}</li>\n"
                                    html_content += "</ul></div>\n"

                                if "description" in media_metadata:
                                    html_content += f"""
                                        <div class="video-info">
                                            <div class="video-description">{media_metadata["description"]}</div>
                                        </div>
                                    """

                                html_content += """
                                </body>
                                </html>
                                """

                                media_item = MediaItem(
                                    title=media_metadata.get("title", media_file.stem),
                                    path=f"media/{media_file.stem}",
                                    content=html_content,
                                )
                                creator.add_item(media_item)

                                media_file_item = MediaItem(
                                    title=media_file.name,
                                    path=f"media/{media_file.name}",
                                    fpath=str(media_file),
                                )
                                media_file_item.get_mimetype = lambda m=mime_type: m
                                creator.add_item(media_file_item)

                                if "subtitles" in media_metadata:
                                    for subtitle in media_metadata["subtitles"]:
                                        subtitle_path = self.metadata_dir / subtitle
                                        if subtitle_path.exists():
                                            subtitle_item = MediaItem(
                                                title=subtitle,
                                                path=f"media/{subtitle}",
                                                fpath=str(subtitle_path),
                                            )
                                            subtitle_item.get_mimetype = (
                                                lambda s=subtitle: "text/vtt"
                                                if s.endswith(".vtt")
                                                else "text/srt"
                                            )
                                            creator.add_item(subtitle_item)

                            except Exception as e:
                                self.logger.error(
                                    "Error processing media %s: %s", media_file.name, e
                                )
                                continue

                            progress.update(task, advance=1)

                for playlist_id, playlist in playlist_groups.items():
                    playlist_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>{playlist["title"]}</title>
                        <meta charset="utf-8">
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                line-height: 1.6;
                                max-width: 1200px;
                                margin: 0 auto;
                                padding: 20px;
                                background-color: #f9f9f9;
                            }}
                            h1 {{
                                color: #030303;
                                margin-bottom: 20px;
                            }}
                            .playlist-info {{
                                color: #606060;
                                margin-bottom: 30px;
                            }}
                            .video-grid {{
                                display: grid;
                                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                                gap: 20px;
                                padding: 0;
                            }}
                            .video-item {{
                                background: #fff;
                                border-radius: 8px;
                                overflow: hidden;
                                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                                transition: transform 0.2s;
                            }}
                            .video-item:hover {{
                                transform: translateY(-2px);
                            }}
                            .video-item a {{
                                text-decoration: none;
                                color: inherit;
                            }}
                            .video-thumbnail {{
                                width: 100%;
                                padding-top: 56.25%;
                                background-color: #000;
                                position: relative;
                            }}
                            .video-thumbnail img {{
                                position: absolute;
                                top: 0;
                                left: 0;
                                width: 100%;
                                height: 100%;
                                object-fit: cover;
                            }}
                            .video-info {{
                                padding: 12px;
                            }}
                            .video-title {{
                                font-weight: bold;
                                color: #030303;
                                margin-bottom: 4px;
                                display: -webkit-box;
                                -webkit-line-clamp: 2;
                                -webkit-box-orient: vertical;
                                overflow: hidden;
                            }}
                            .video-date {{
                                color: #606060;
                                font-size: 12px;
                            }}
                            .video-index {{
                                color: #606060;
                                font-size: 12px;
                                margin-top: 4px;
                            }}
                        </style>
                    </head>
                    <body>
                        <h1>{playlist["title"]}</h1>
                        <div class="playlist-info">
                            {len(playlist["videos"])} videos in this playlist
                        </div>
                        <div class="video-grid">
                    """

                    for media_file, media_metadata in playlist["videos"]:
                        title = media_metadata.get("title", media_file.stem)
                        date = media_metadata.get("upload_date", "")
                        thumbnail = media_metadata.get("thumbnail", "")
                        index = media_metadata.get("playlist_index", 0)

                        playlist_content += f"""
                        <div class="video-item">
                            <a href="media/{media_file.stem}">
                                <div class="video-thumbnail">
                                    <img src="{thumbnail}" alt="{title}">
                                </div>
                                <div class="video-info">
                                    <div class="video-title">{title}</div>
                                    <div class="video-date">{date}</div>
                                    <div class="video-index">Video {index}</div>
                                </div>
                            </a>
                        </div>
                        """

                    playlist_content += """
                        </div>
                    </body>
                    </html>
                    """

                    playlist_item = MediaItem(
                        title=playlist["title"],
                        path=f"playlist_{playlist_id}",
                        content=playlist_content,
                    )
                    creator.add_item(playlist_item)

                index_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{title}</title>
                    <meta charset="utf-8">
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                            max-width: 1200px;
                            margin: 0 auto;
                            padding: 20px;
                            background-color: #f9f9f9;
                        }}
                        h1 {{
                            color: #030303;
                            margin-bottom: 20px;
                        }}
                        .description {{
                            color: #606060;
                            margin-bottom: 30px;
                        }}
                        .section {{
                            margin-bottom: 40px;
                        }}
                        .section-title {{
                            font-size: 24px;
                            font-weight: bold;
                            color: #030303;
                            margin-bottom: 20px;
                            padding-bottom: 10px;
                            border-bottom: 1px solid #e5e5e5;
                        }}
                        .video-grid {{
                            display: grid;
                            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                            gap: 20px;
                            padding: 0;
                        }}
                        .video-item {{
                            background: #fff;
                            border-radius: 8px;
                            overflow: hidden;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                            transition: transform 0.2s;
                        }}
                        .video-item:hover {{
                            transform: translateY(-2px);
                        }}
                        .video-item a {{
                            text-decoration: none;
                            color: inherit;
                        }}
                        .video-thumbnail {{
                            width: 100%;
                            padding-top: 56.25%;
                            background-color: #000;
                            position: relative;
                        }}
                        .video-thumbnail img {{
                            position: absolute;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                            object-fit: cover;
                        }}
                        .video-info {{
                            padding: 12px;
                        }}
                        .video-title {{
                            font-weight: bold;
                            color: #030303;
                            margin-bottom: 4px;
                            display: -webkit-box;
                            -webkit-line-clamp: 2;
                            -webkit-box-orient: vertical;
                            overflow: hidden;
                        }}
                        .video-date {{
                            color: #606060;
                            font-size: 12px;
                        }}
                        .playlist-card {{
                            background: #fff;
                            border-radius: 8px;
                            overflow: hidden;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                            transition: transform 0.2s;
                        }}
                        .playlist-card:hover {{
                            transform: translateY(-2px);
                        }}
                        .playlist-card a {{
                            text-decoration: none;
                            color: inherit;
                        }}
                        .playlist-thumbnail {{
                            width: 100%;
                            padding-top: 56.25%;
                            background-color: #000;
                            position: relative;
                        }}
                        .playlist-thumbnail img {{
                            position: absolute;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                            object-fit: cover;
                        }}
                        .playlist-info {{
                            padding: 12px;
                        }}
                        .playlist-title {{
                            font-weight: bold;
                            color: #030303;
                            margin-bottom: 4px;
                        }}
                        .playlist-count {{
                            color: #606060;
                            font-size: 12px;
                        }}
                    </style>
                </head>
                <body>
                    <h1>{title}</h1>
                    <div class="description">{description}</div>
                """

                if playlist_groups:
                    index_content += """
                        <div class="section">
                            <h2 class="section-title">Playlists</h2>
                            <div class="video-grid">
                    """
                    for playlist_id, playlist in playlist_groups.items():
                        # Use the first video's thumbnail as playlist thumbnail
                        first_video = playlist["videos"][0]
                        thumbnail = first_video[1].get("thumbnail", "")

                        index_content += f"""
                            <div class="playlist-card">
                                <a href="playlist_{playlist_id}">
                                    <div class="playlist-thumbnail">
                                        <img src="{thumbnail}" alt="{playlist["title"]}">
                                    </div>
                                    <div class="playlist-info">
                                        <div class="playlist-title">{playlist["title"]}</div>
                                        <div class="playlist-count">{len(playlist["videos"])} videos</div>
                                    </div>
                                </a>
                            </div>
                        """
                    index_content += """
                            </div>
                        </div>
                    """

                if standalone_videos:
                    index_content += """
                        <div class="section">
                            <h2 class="section-title">Videos</h2>
                            <div class="video-grid">
                    """
                    for media_file, media_metadata in standalone_videos:
                        title = media_metadata.get("title", media_file.stem)
                        date = media_metadata.get("upload_date", "")
                        thumbnail = media_metadata.get("thumbnail", "")

                        index_content += f"""
                            <div class="video-item">
                                <a href="media/{media_file.stem}">
                                    <div class="video-thumbnail">
                                        <img src="{thumbnail}" alt="{title}">
                                    </div>
                                    <div class="video-info">
                                        <div class="video-title">{title}</div>
                                        <div class="video-date">{date}</div>
                                    </div>
                                </a>
                            </div>
                        """
                    index_content += """
                            </div>
                        </div>
                    """

                index_content += """
                </body>
                </html>
                """

                index_item = MediaItem(
                    title=title,
                    path="index",
                    content=index_content,
                )
                creator.add_item(index_item)

            log.info("Created ZIM archive at %s", zim_path)
            return True

        except Exception as e:
            log.error("Failed to create ZIM archive: %s", e)
            return False

    def cleanup(self) -> None:
        """Delete all downloaded files and directories after ZIM creation.

        This method attempts to remove all files within the media and metadata directories,
        and then removes the directories themselves. It logs each deletion attempt and
        any errors encountered. If directory removal fails, it lists any remaining files
        in those directories.
        """
        try:
            if self.media_dir.exists():
                for file in self.media_dir.glob("*"):
                    try:
                        file.unlink()
                        log.info("Deleted media file: %s", file.name)
                    except Exception as e:  # noqa: PERF203
                        log.warning("Could not delete file %s: %s", file.name, e)

            if self.metadata_dir.exists():
                for file in self.metadata_dir.glob("*"):
                    try:
                        file.unlink()
                        log.info("Deleted metadata file: %s", file.name)
                    except Exception as e:  # noqa: PERF203
                        log.warning("Could not delete file %s: %s", file.name, e)

            try:
                if self.media_dir.exists():
                    self.media_dir.rmdir()
                if self.metadata_dir.exists():
                    self.metadata_dir.rmdir()
                log.info("Cleanup completed successfully")
            except Exception as e:
                log.warning("Could not remove directories: %s", e)
                if self.media_dir.exists():
                    remaining = list(self.media_dir.glob("*"))
                    if remaining:
                        log.warning(
                            "Remaining files in media directory: %s",
                            [f.name for f in remaining],
                        )
                if self.metadata_dir.exists():
                    remaining = list(self.metadata_dir.glob("*"))
                    if remaining:
                        log.warning(
                            "Remaining files in metadata directory: %s",
                            [f.name for f in remaining],
                        )

        except Exception as e:
            log.error("Error during cleanup: %s", e)
            try:
                if self.media_dir.exists():
                    log.error(
                        "Files still in media directory: %s",
                        [f.name for f in self.media_dir.glob("*")],
                    )
                if self.metadata_dir.exists():
                    log.error(
                        "Files still in metadata directory: %s",
                        [f.name for f in self.metadata_dir.glob("*")],
                    )
            except Exception as e:
                log.error("Failed to list remaining files: %s", e)


@click.group()
def cli():
    """Archiver ZIM - Download videos and podcasts and create ZIM archives."""
    pass


@cli.command()
@click.argument("urls", nargs=-1, required=True)
@click.option("--output-dir", "-o", default="./archive", help="Output directory")
@click.option(
    "--quality", "-q", default="best", help="Video quality (e.g., 720p, 480p)"
)
@click.option("--date", "-d", help="Filter by specific date (YYYY-MM-DD)")
@click.option(
    "--date-limit", "-dl", type=int, help="Download only episodes from the last N days"
)
@click.option(
    "--month-limit",
    "-ml",
    type=int,
    help="Download only episodes from the last N months",
)
@click.option("--title", "-t", help="Title for the ZIM archive")
@click.option(
    "--description", "--desc", default="Media archive", help="ZIM archive description"
)
@click.option("--retry-count", default=3, help="Number of retries for failed downloads")
@click.option("--retry-delay", default=5, help="Base delay between retries in seconds")
@click.option(
    "--max-retries", default=10, help="Maximum number of retries before giving up"
)
@click.option(
    "--skip-download",
    is_flag=True,
    help="Skip download phase and create ZIM from existing media",
)
@click.option(
    "--cleanup", is_flag=True, help="Delete downloaded files after ZIM creation"
)
@click.option("--dry-run", is_flag=True, help="Simulate operations without downloading")
@click.option("--cookies", help="Path to cookies file")
@click.option(
    "--cookies-from-browser",
    help="Browser to extract cookies from (e.g., firefox, chrome)",
)
def archive(
    urls: list[str],
    output_dir: str,
    quality: str,
    date: Optional[str],
    date_limit: Optional[int],
    month_limit: Optional[int],
    title: Optional[str],
    description: str,
    retry_count: int,
    retry_delay: int,
    max_retries: int,
    skip_download: bool,
    cleanup: bool,
    dry_run: bool,
    cookies: Optional[str],
    cookies_from_browser: Optional[str],
):
    """Download media and create a ZIM archive."""
    archiver = Archiver(
        output_dir,
        quality,
        retry_count,
        retry_delay,
        max_retries,
        dry_run=dry_run,
        cookies=cookies,
        cookies_from_browser=cookies_from_browser,
    )

    if not title:
        title = f"Media_Archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    if not skip_download:
        success = True
        results = archiver.download_media(urls, date, date_limit, month_limit)
        for url, result in results.items():
            if not result:
                success = False
                log.error("Failed to download: %s", url)

        if not success:
            log.warning("Some downloads failed, but continuing with ZIM creation...")
    else:
        log.info("Skipping download phase, creating ZIM from existing media...")

    if archiver.create_zim(title, description):
        log.info("Archive completed successfully")

        if cleanup and not dry_run:
            log.info("Cleaning up downloaded files...")
            archiver.cleanup()
    else:
        log.error("Failed to create archive")
        sys.exit(1)


@cli.command()
@click.option("--config", "-c", default="config.yml", help="Path to configuration file")
def manage(config: str):
    """Run the archive manager in continuous mode."""
    from manager import ArchiveManager

    manager = ArchiveManager(config)
    asyncio.run(manager.run())


if __name__ == "__main__":
    cli()
