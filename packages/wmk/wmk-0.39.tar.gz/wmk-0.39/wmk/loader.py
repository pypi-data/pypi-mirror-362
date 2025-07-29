import concurrent.futures
import logging
import os

import urllib3
from tqdm import tqdm
from urllib3.util import Retry


class Loader:
    """A file download manager with retry capabilities and progress tracking.

    This class provides functionality to download files from URLs with features like:
    - Automatic retries for failed requests
    - Progress bar display
    - Chunk-based downloading for large files
    - Download verification

    Args:
        chunk_size (int): Size of chunks to download at a time, defaults to 1MB

    Attributes:
        http (urllib3.PoolManager): HTTP connection manager
        chunk_size (int): Size of chunks to download at a time, defaults to 1MB
    """

    def __init__(self, chunk_size: int = 1024 * 1024):
        retry_strategy = Retry(
            total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504]
        )
        self.http = urllib3.PoolManager(retries=retry_strategy)
        self.chunk_size = chunk_size
        logging.getLogger("urllib3").setLevel(logging.WARNING)

    def download_file(self, url: str, path: str, headers: dict | None = None):
        """Download a file from a URL to a specified path.

        Args:
            url (str): The URL to download the file from
            path (str): Local path where the file should be saved
            headers (dict, optional): HTTP headers to include in the request

        Returns:
            bool: False if download failed, True otherwise

        Raises:
            Exception: If file verification fails after download
        """
        try:
            response = self.http.request("GET", url, preload_content=False, headers=headers)
            total_length = int(response.headers.get("content-length", 0))

            with (
                open(path, "wb") as out_file,
                tqdm(
                    desc=f"Downloading: {os.path.basename(path)}",
                    total=total_length,
                    unit="iB",
                    unit_scale=True,
                ) as progress_bar,
            ):
                for data in response.stream(self.chunk_size):
                    size = out_file.write(data)
                    progress_bar.update(size)

            response.release_conn()

            # Verify file was created successfully
            if not os.path.exists(path):
                raise Exception("File not found after download")

            # Verify file size with some tolerance
            if abs(total_length - os.path.getsize(path)) > 1024:
                raise Exception("Downloaded file size does not match expected size")

            return True

        except Exception as e:
            logging.error(f"Error downloading {url}: {type(e).__name__} - {str(e)}")

            try:
                if os.path.exists(path):
                    os.remove(path)
            except OSError as e:
                logging.error(f"Error removing file {path}: {str(e)}")
            return False

    def download_files(self, urls: dict, headers: dict | None = None):
        """Download multiple files from URLs to specified paths in parallel.

        Args:
            urls (dict): A dictionary with URL as key and local path as value
            headers (dict, optional): HTTP headers to include in the request

        Returns:
            dict: A dictionary with URL as key and boolean status as value
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                url: executor.submit(self.download_file, url, path, headers)
                for url, path in urls.items()
            }
            return {url: future.result() for url, future in futures.items()}
