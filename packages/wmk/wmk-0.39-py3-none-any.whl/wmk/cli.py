import logging

import click

from .loader import Loader
from .packager import Packager

logging.basicConfig(level=logging.NOTSET, format="%(asctime)s - %(levelname)s - %(message)s")


@click.group()
def cli():
    """WMK CLI tool"""
    pass


@cli.command()
@click.option(
    "-t",
    "--target",
    required=False,
    default=None,
    help="Directory containing requirements.txt and where packages will be stored",
)
@click.option(
    "-n", "--name", required=False, default="Build.zip", help="Name of the output ZIP file"
)
@click.option(
    "-p", "--platform", required=False, multiple=True, help="Target platform for dependencies"
)
@click.option(
    "--only-tracked", required=False, default=True, help="Skip files listed in .gitignore"
)
@click.option(
    "-a",
    "--additional-files",
    required=False,
    multiple=True,
    help="Additional files for the archive",
)
@click.option("-v", "--build-version", required=False, default=None, help="Version of the build")
@click.option("--python-version", required=False, default=None, help="Python version to use")
@click.option("--skip", required=False, multiple=True, help="Dependencies to skip during download")
@click.option(
    "--manual", is_flag=True, default=False, help="Pause for confirmation before creating archive"
)
def package(
    target,
    name,
    platform,
    only_tracked,
    additional_files,
    build_version,
    python_version,
    skip,
    manual,
):
    """Download Python packages and create archive"""
    packager = Packager(
        target, platform, only_tracked, additional_files, build_version, python_version, skip
    )
    if packager.download_packages():
        if manual:
            if click.confirm("Packages downloaded. Create archive?"):
                packager.create_archive(name)
            else:
                packager.logger.info("Archive creation cancelled by user")
        else:
            packager.create_archive(name)
    else:
        packager.logger.error("Skipping archive creation due to download errors")


@cli.command()
@click.option("-u", "--url", required=True, help="URL of the file to download")
@click.option("-f", "--filepath", required=True, help="Local path where to save the file")
def download(url, filepath):
    """Download a file from URL to local path"""
    transfer = Loader()
    transfer.download_file(url, filepath)


@cli.command()
@click.option(
    "-c", "--commit-hash", required=False, default="", help="Git commit hash to compare against"
)
@click.option(
    "-p", "--s3-prefix", required=False, default="", help="S3 key prefix for uploaded files"
)
@click.option("-b", "--bucket-name", required=False, help="S3 bucket name for file uploads")
@click.option(
    "-t",
    "--target",
    required=False,
    default=None,
    help="Target directory containing the git repository",
)
@click.option(
    "--manual", is_flag=True, default=True, help="Pause for confirmation before uploading files"
)
def upload_changed_files(commit_hash, s3_prefix, bucket_name, target, manual):
    """Upload changed files to S3 since the specified commit"""
    packager = Packager(target=target)

    try:
        # Get list of changed files
        changed_files = packager.get_list_of_changed_files(commit_hash)

        if not changed_files:
            packager.logger.info("No changed files found")
            return

        # Show the list of files to be uploaded
        packager.logger.info(f"Found {len(changed_files)} changed files:")
        for file in changed_files:
            packager.logger.info(f"  - {file}")

        # Check if bucket name is provided
        if not bucket_name:
            packager.logger.error("S3 bucket name is required")
            return

        # Confirm upload if manual flag is set
        if manual:
            if not click.confirm("Upload these files to S3?"):
                packager.logger.info("Upload cancelled by user")
                return

        # Upload files to S3
        if packager.upload_files_to_s3(changed_files, bucket_name, s3_prefix):
            packager.logger.info("Files uploaded successfully")
        else:
            packager.logger.error("Failed to upload some or all files")

    except Exception as e:
        packager.logger.error(f"Error during upload process: {e}")


if __name__ == "__main__":
    cli()
