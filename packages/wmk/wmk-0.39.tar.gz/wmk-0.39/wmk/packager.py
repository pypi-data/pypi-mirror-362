import json
import logging
import os
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile


class Packager:
    """
    A class for packaging Python dependencies and project files into a distributable archive.

    The Packager handles downloading platform-specific Python packages, generating build manifests,
    and creating ZIP archives containing the project and its dependencies.

    Args:
        target (str, optional): Target directory path. Defaults to current working directory.
        platform (str, optional): Target platforms for packages. Defaults to "manylinux2014_x86_64".
        only_tracked (bool, optional): Include only git-tracked files. Defaults to True.
        additional_files (list, optional): Additional files/directories to include in the archive.
        build_version (str, optional): Version identifier for the build.
        python_version (str, optional): Target Python version for packages.

    Attributes:
        target_dir (str): Directory where the packaging operations take place
        platform (str): Target platform identifier
        only_tracked (bool): Flag to include only git-tracked files
        additional_files (list): List of additional files to include
        build_version (str): Build version identifier
        python_version (str): Target Python version
        dependencies_dir (str): Directory for downloaded dependencies
        logger (Logger): Logger instance for the class
    """

    def __init__(
        self,
        target=None,
        platform=None,
        only_tracked=True,
        additional_files=None,
        build_version=None,
        python_version=None,
        skip=None,
    ):
        if platform is None:
            platform = ["manylinux2014_x86_64", "manylinux_2_17_x86_64"]
        self.target_dir = target or os.getcwd()
        self.platform = platform
        self.only_tracked = only_tracked
        self.additional_files = additional_files
        self.build_version = build_version
        self.python_version = python_version
        self.dependencies_dir = os.path.join(self.target_dir, "dependencies")
        self.skip = skip or []
        self.logger = logging.getLogger(__name__)

    def download_packages(self):
        """
        Download packages with specific platform constraints.

        This method looks for dependency specifications in requirements.txt, pyproject.toml,
        or setup.py and downloads all required packages using pip. Downloads are platform-specific
        and stored in the dependencies directory.

        Returns:
            bool: True if packages were downloaded successfully, False otherwise.

        Raises:
            FileNotFoundError: If no dependency specification file is found.
        """
        try:
            # Ensure dependencies directory exists
            Path(self.dependencies_dir).mkdir(parents=True, exist_ok=True)

            # Get project dependencies information
            dependencies_params, python_version_params, extra_index_urls = (
                self._get_project_dependencies_info()
            )

            # Create temporary directory for requirements files
            temp_dir = tempfile.TemporaryDirectory()

            # Run dry-run install to check package availability
            dry_run_cmd = [
                "pip",
                "install",
                *dependencies_params,
                "--dry-run",
                "--ignore-installed",
                "--report",
                os.path.join(temp_dir.name, "report.json"),
            ]
            self.logger.info("Loading package information...")
            process = subprocess.run(dry_run_cmd, capture_output=True, text=True, check=False)
            if process.returncode != 0:
                self.logger.error(f"Dry run failed: {process.stderr}")
                return False

            # Read the report to get package info
            with open(os.path.join(temp_dir.name, "report.json")) as f:
                report = json.load(f)

            # Parse report to separate wheels and source distributions
            wheel_packages, source_packages = self._parse_installation_report(report)

            temp_path = Path(temp_dir.name)
            wheels_req = temp_path / "wheels.txt"
            sources_req = temp_path / "sources.txt"

            with open(wheels_req, "w") as f:
                content = extra_index_urls + "\n".join(wheel_packages)
                f.write(content)

            with open(sources_req, "w") as f:
                content = extra_index_urls + "\n".join(source_packages)
                f.write(content)

            # Download wheel packages if any
            if wheel_packages:
                self.logger.info("Downloading wheel packages...")
                wheel_cmd = [
                    "pip",
                    "download",
                    "-r",
                    wheels_req,
                    "-d",
                    self.dependencies_dir,
                    *[f"--platform={p}" for p in self.platform],
                    *python_version_params,
                    "--only-binary=:all:",
                ]
                if not self._run_cmd_with_output(wheel_cmd):
                    return False

            # Download source packages if any
            if source_packages:
                self.logger.info("Building wheels for source distribution packages...")
                wheel_cmd = ["pip", "wheel", "-r", sources_req, "-w", self.dependencies_dir]
                if not self._run_cmd_with_output(wheel_cmd):
                    return False
            # Clean up temporary directory
            temp_dir.cleanup()

            self.logger.info("All packages processed successfully")
            return True

        except Exception as e:
            self.logger.error(f"Download packages unexpected error: {e}")
            return False

    def _get_project_dependencies_info(self):
        """
        Get package information from requirements file.
        """
        requirements_path = os.path.join(self.target_dir, "requirements.txt")
        has_requirements_txt = os.path.exists(requirements_path)
        has_other_configs = os.path.exists(
            os.path.join(self.target_dir, "pyproject.toml")
        ) or os.path.exists(os.path.join(self.target_dir, "setup.py"))
        dependencies_params = (
            ["-r", requirements_path]
            if has_requirements_txt
            else ["."]
            if has_other_configs
            else None
        )
        if not dependencies_params:
            raise FileNotFoundError(
                "No dependency specification file found (requirements.txt, pyproject.toml, or setup.py)"
            )

        python_version_params = (
            ["--python-version", self.python_version] if self.python_version else []
        )

        # Collect extra index urls from requirements.txt
        extra_index_urls = ""
        if has_requirements_txt:
            with open(requirements_path) as f:
                for line in f:
                    if line.startswith("--extra-index-url"):
                        extra_index_urls += line
        self.logger.info(f"Extra index urls: {extra_index_urls}")

        return dependencies_params, python_version_params, extra_index_urls

    def _parse_installation_report(self, report):
        """
        Parse the installation report to separate wheel and source packages.
        """
        wheel_packages: list[str] = []
        source_packages: list[str] = []
        self.logger.info("Processing package information...")
        for install in report.get("install", []):
            pkg_name = install["metadata"]["name"]

            pkg_version = install["metadata"]["version"]
            # Normalise package version to remove extra specifiers like +, etc.
            if "+" in pkg_version:
                self.logger.warning(f"Normalising version for package {pkg_name}=={pkg_version}")
                pkg_version = re.split(r"[+]", pkg_version)[0]

            # Skip if package is in skip list
            if pkg_name in self.skip:
                self.logger.info(f"Skipping package {pkg_name} as requested")
                continue

            pkg_full_name = f"{pkg_name}=={pkg_version}"
            download_url: str = install.get("download_info", {}).get("url", None)
            if not download_url:
                self.logger.warning(f"Package {pkg_full_name} not found.")
                continue

            if download_url.endswith(".whl"):
                wheel_packages.append(pkg_full_name)
            else:
                source_packages.append(pkg_full_name)

        return wheel_packages, source_packages

    def generate_manifest(self):
        """
        Generate a manifest file containing package metadata.

        Creates a JSON manifest containing build timestamp, runtime requirements,
        and other metadata about the package.

        Returns:
            dict: A dictionary containing the manifest data with the following structure:
                {
                    "timeStamp": str,
                    "entities": list,
                    "runtime": str,
                    "runtimeRequirements": dict,
                    "buildVersion": str
                }
        """
        manifest = {
            "timeStamp": datetime.now().isoformat(),
            "entities": [],
            "runtime": "python",
            "runtimeRequirements": {
                "platform": self.platform,
                "pythonVersion": self.python_version or "",
            },
            # TODO: Support pyproject.toml and setup.py
            "scripts": {
                "install": "pip install --no-index --find-links dependencies/ -r requirements.txt"
            },
            "buildVersion": self.build_version or "",
        }

        self.logger.info("Manifest generated successfully")
        return manifest

    def create_archive(self, archive_name):
        """
        Create a ZIP archive of the downloaded packages and project files.

        Args:
            archive_name (str): Name of the archive file to create

        Returns:
            bool: True if archive was created successfully, False otherwise.

        The archive includes:
            - All specified project files (git-tracked or all, based on only_tracked)
            - Downloaded dependencies
            - Additional files specified during initialization
            - BuildManifest.json containing package metadata
        """
        try:
            dir_to_archive = Path(self.target_dir)
            archive_path = os.path.join(self.target_dir, archive_name)

            # Generate manifest as JSON string
            manifest = self.generate_manifest()
            manifest_str = json.dumps(manifest, indent=2)

            if self.only_tracked:
                # Get tracked files using git
                files = subprocess.check_output(
                    ["git", "ls-files", "--exclude-standard"], cwd=dir_to_archive, text=True
                ).splitlines()
            else:
                # Get all files in the directory
                files = self._get_nested_files(dir_to_archive, dir_to_archive)

            # Add dependencies directory
            if os.path.exists(self.dependencies_dir):
                dependencies_files = self._get_nested_files(self.dependencies_dir, dir_to_archive)
                files.extend(file for file in dependencies_files if file not in files)

            # Add additional files
            if self.additional_files:
                for path in self.additional_files:
                    full_path = os.path.join(dir_to_archive, path)
                    if os.path.isfile(full_path):
                        files.append(path)
                    elif os.path.isdir(full_path):
                        additional_files = self._get_nested_files(full_path, dir_to_archive)
                        files.extend(file for file in additional_files if file not in files)

            with ZipFile(archive_path, "w") as zip_file:
                # Add manifest directly as string
                zip_file.writestr("Build/BuildManifest.json", manifest_str)

                # Add files
                for file in files:
                    file_path = os.path.join(dir_to_archive, file)
                    zip_path = os.path.join("Build", file)
                    zip_file.write(file_path, zip_path)

            self.logger.info(f"Archive created successfully: {archive_name}")
            return True

        except Exception as e:
            self.logger.error(f"Error creating archive: {e}")
            return False

    def _get_nested_files(self, target_dir, base_dir):
        """
        Recursively get all files in a directory relative to a base directory.

        Args:
            target_dir (str): Directory to scan for files
            base_dir (str): Base directory for creating relative paths

        Returns:
            list: List of relative file paths
        """
        files = []
        for root, _, filenames in os.walk(target_dir):
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), base_dir)
                files.append(rel_path)
        return files

    def _run_cmd_with_output(self, cmd):
        """
        Run the download command and print warnings and errors in real-time.

        Args:
            cmd (list): download command and arguments
        """
        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

            while True:
                if process.stderr is None:
                    break

                stderr_line = process.stderr.readline()
                if stderr_line:
                    if "warning" in stderr_line.lower():
                        self.logger.warning(stderr_line.strip())
                    elif "error" in stderr_line.lower():
                        self.logger.error(stderr_line.strip())
                    else:
                        # Catch-all for other stderr content
                        self.logger.error(stderr_line.strip())

                # Check if process is complete
                if stderr_line == "" and process.poll() is not None:
                    break

            if process.returncode == 0:
                self.logger.info("Package download completed successfully")
                return True
            else:
                self.logger.error(f"Package download failed with return code {process.returncode}")
                return False

        except Exception as e:
            self.logger.error(f"Error in running download command: {e}")
            return False

    def get_list_of_changed_files(self, commit_hash: str = "") -> list[str]:
        """
        Get a list of changed files in the current git repository.

        Args:
            commit_hash (str): The git commit hash to compare against. If empty,
                               compares against the current HEAD.

        Returns:
            list[str]: A list of filenames that have changed since the specified commit.
                      Each filename is relative to the repository root.

        Raises:
            subprocess.CalledProcessError: If the git command fails.
        """
        return (
            subprocess.check_output(["git", "diff", "--name-only", commit_hash])
            .decode()
            .splitlines()
        )

    def upload_files_to_s3(self, files: list[str], bucket_name: str, s3_key: str):
        """
        Upload files to S3 bucket.

        Args:
            files (list[str]): List of file paths to upload.
            bucket_name (str): Name of the S3 bucket to upload files to.
            s3_key (str): Prefix to add to the S3 object keys. If provided, files will be
                          uploaded to s3://{bucket_name}/{s3_key}/{filename}.

        Returns:
            bool: True if the upload process completed (even if some individual files failed),
                  False if there was a general error in the upload process.
        """
        try:
            import boto3
        except ImportError as error:
            raise ImportError(
                "boto3 is required for S3 uploads. Please install it with 'pip install boto3' "
                "or install wmk with the S3 extras: 'pip install wmk[s3]'"
            ) from error

        try:
            self.logger.info(f"Uploading files to S3 bucket: {bucket_name} with prefix: {s3_key}")
            s3_client = boto3.client("s3")

            for file_path in files:
                if not os.path.exists(file_path):
                    self.logger.warning(f"File not found: {file_path}, skipping upload")
                    continue

                # Construct the S3 object key by combining the prefix with the filename
                object_key = f"{s3_key.rstrip('/')}/{file_path}" if s3_key else file_path

                self.logger.info(f"Uploading {file_path} to s3://{bucket_name}/{object_key}")

                try:
                    # Use the correct method to upload file to S3
                    with open(file_path, "rb") as file_data:
                        s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=file_data)
                    self.logger.info(f"Successfully uploaded {file_path} to S3")
                except Exception as e:
                    self.logger.error(f"Failed to upload {file_path} to S3: {e}")

            self.logger.info("S3 upload process completed")
            return True

        except Exception as e:
            self.logger.error(f"Error in S3 upload process: {e}")
            return False
