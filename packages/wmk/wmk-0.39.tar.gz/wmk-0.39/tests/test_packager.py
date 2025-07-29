import json
import subprocess
import unittest
from unittest.mock import MagicMock, Mock, mock_open, patch

from wmk.packager import Packager


class TestPackager(unittest.TestCase):
    def setUp(self):
        self.test_dir = "/test/dir"
        self.packager = Packager(
            target=self.test_dir,
            platform=["linux_x86_64"],
            build_version="1.0.0",
            python_version="3.9",
            skip=["skip_pkg"],
        )

    def test_init(self):
        # Test initialization with default values
        packager = Packager()
        self.assertEqual(packager.platform, ["manylinux2014_x86_64", "manylinux_2_17_x86_64"])
        self.assertTrue(packager.only_tracked)
        self.assertIsNone(packager.additional_files)
        self.assertIsNone(packager.build_version)
        self.assertIsNone(packager.python_version)

        # Test initialization with custom values
        packager = Packager(
            target="/custom/dir",
            platform=["win_amd64"],
            only_tracked=False,
            additional_files=["extra.txt"],
            build_version="2.0.0",
            python_version="3.10",
        )
        self.assertEqual(packager.target_dir, "/custom/dir")
        self.assertEqual(packager.platform, ["win_amd64"])
        self.assertFalse(packager.only_tracked)
        self.assertEqual(packager.additional_files, ["extra.txt"])
        self.assertEqual(packager.build_version, "2.0.0")
        self.assertEqual(packager.python_version, "3.10")
        self.assertEqual(packager.dependencies_dir, "/custom/dir/dependencies")

        # Test initialization with skip parameter
        packager = Packager(skip=["pkg1", "pkg2"])
        self.assertEqual(packager.skip, ["pkg1", "pkg2"])

    @patch("wmk.packager.subprocess.run")
    @patch("wmk.packager.subprocess.Popen")
    @patch("wmk.packager.Path")
    @patch("wmk.packager.os.path.exists")
    def test_download_packages(self, mock_exists, mock_path, mock_popen, mock_run):
        # Test when requirements file doesn't exist
        mock_exists.return_value = False
        self.assertFalse(self.packager.download_packages())

        # Test successful download
        mock_exists.return_value = True
        mock_run.return_value = Mock(returncode=0)
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stderr.readline.return_value = ""
        mock_process.poll.return_value = 0
        mock_popen.return_value = mock_process

        report_data = {
            "install": [
                {
                    "metadata": {"name": "pkg1", "version": "1.0"},
                    "download_info": {"url": "pkg1.whl"},
                },
                {
                    "metadata": {"name": "pkg2", "version": "2.0"},
                    "download_info": {"url": "pkg2.tar.gz"},
                },
            ]
        }
        mocked_open = mock_open(read_data=json.dumps(report_data))
        with patch("builtins.open", mocked_open):
            self.assertTrue(self.packager.download_packages())

        # Test download failure
        mock_run.return_value = Mock(returncode=1, stderr="Download error")
        self.assertFalse(self.packager.download_packages())

    @patch("wmk.packager.subprocess.run")
    @patch("wmk.packager.subprocess.Popen")
    @patch("wmk.packager.Path")
    @patch("wmk.packager.os.path.exists")
    def test_skip_packages(self, mock_exists, mock_path, mock_popen, mock_run):
        mock_exists.return_value = True
        mock_run.return_value = Mock(returncode=0)
        mock_process = Mock()
        mock_process.returncode = 0
        mock_process.stderr.readline.return_value = ""
        mock_process.poll.return_value = 0
        mock_popen.return_value = mock_process

        report_data = {
            "install": [
                {
                    "metadata": {"name": "skip_pkg", "version": "1.0"},
                    "download_info": {"url": "skip_pkg.whl"},
                },
                {
                    "metadata": {"name": "pkg2", "version": "2.0"},
                    "download_info": {"url": "pkg2.whl"},
                },
            ]
        }
        mocked_open = mock_open(read_data=json.dumps(report_data))
        with patch("builtins.open", mocked_open):
            self.assertTrue(self.packager.download_packages())
            # Verify that only pkg2 was processed
            write_calls = [call[0][0] for call in mocked_open().write.call_args_list]
            self.assertTrue(any("pkg2==2.0" in call for call in write_calls))
            self.assertFalse(any("skip_pkg==1.0" in call for call in write_calls))

    def test_generate_manifest(self):
        manifest = self.packager.generate_manifest()

        self.assertEqual(manifest["runtime"], "python")
        self.assertEqual(manifest["runtimeRequirements"]["platform"], ["linux_x86_64"])
        self.assertEqual(manifest["runtimeRequirements"]["pythonVersion"], "3.9")
        self.assertEqual(manifest["buildVersion"], "1.0.0")
        self.assertEqual(manifest["entities"], [])
        self.assertIn("timeStamp", manifest)
        self.assertIn("scripts", manifest)
        self.assertIn("install", manifest["scripts"])

    @patch("wmk.packager.ZipFile")
    @patch("wmk.packager.subprocess.check_output")
    @patch("wmk.packager.os.path.exists")
    def test_create_archive(self, mock_exists, mock_check_output, mock_zipfile):
        mock_exists.return_value = True
        mock_zip = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_zip

        # Test with git-tracked files
        mock_check_output.return_value = "file1.py\nfile2.py"
        self.assertTrue(self.packager.create_archive("test.zip"))
        self.assertEqual(mock_zip.write.call_count, 2)

        # Test with git command failure
        mock_check_output.side_effect = subprocess.CalledProcessError(128, "git")
        self.assertFalse(self.packager.create_archive("test.zip"))

        # Test with additional files
        mock_check_output.side_effect = None
        mock_check_output.return_value = ""
        packager = Packager(
            target=self.test_dir, only_tracked=False, additional_files=["extra.txt"]
        )

        with (
            patch("wmk.packager.os.path.isfile") as mock_isfile,
            patch("wmk.packager.os.path.isdir") as mock_isdir,
        ):
            mock_isfile.return_value = True
            mock_isdir.return_value = False
            self.assertTrue(packager.create_archive("test.zip"))

        # Test archive creation failure
        mock_zipfile.side_effect = Exception("ZIP error")
        self.assertFalse(self.packager.create_archive("test.zip"))

    @patch("wmk.packager.subprocess.check_output")
    def test_get_list_of_changed_files(self, mock_check_output):
        # Test with default commit hash (empty string)
        mock_check_output.return_value = b"file1.py\nfile2.py\nfile3.py"
        changed_files = self.packager.get_list_of_changed_files()
        self.assertEqual(changed_files, ["file1.py", "file2.py", "file3.py"])
        mock_check_output.assert_called_with(["git", "diff", "--name-only", ""])

        # Test with specific commit hash
        mock_check_output.reset_mock()
        mock_check_output.return_value = b"file4.py\nfile5.py"
        changed_files = self.packager.get_list_of_changed_files("abc123")
        self.assertEqual(changed_files, ["file4.py", "file5.py"])
        mock_check_output.assert_called_with(["git", "diff", "--name-only", "abc123"])

        # Test with git command failure
        mock_check_output.side_effect = subprocess.CalledProcessError(128, "git")
        with self.assertRaises(subprocess.CalledProcessError):
            self.packager.get_list_of_changed_files()

    @patch("sys.modules", {"boto3": None})
    def test_upload_files_to_s3_boto3_import_error(self):
        # Test boto3 import error
        with self.assertRaises(ImportError) as context:
            self.packager.upload_files_to_s3(["file1.py"], "test-bucket", "test-prefix")
        self.assertIn("boto3 is required for S3 uploads", str(context.exception))

    @patch("sys.modules", {"boto3": MagicMock()})
    @patch("wmk.packager.os.path.exists")
    def test_upload_files_to_s3_success(self, mock_exists):
        # Setup mocks
        mock_exists.return_value = True

        # Create a mock boto3 module
        mock_boto3 = MagicMock()
        mock_s3_client = MagicMock()
        mock_boto3.client.return_value = mock_s3_client

        # Patch the boto3 import
        with patch.dict("sys.modules", {"boto3": mock_boto3}):
            mocked_open = mock_open(read_data=b"file content")
            with patch("builtins.open", mocked_open):
                result = self.packager.upload_files_to_s3(
                    ["file1.py", "file2.py"], "test-bucket", "test-prefix"
                )
                self.assertTrue(result)

                # Verify S3 client was created
                mock_boto3.client.assert_called_once_with("s3")

                # Verify files were uploaded
                self.assertEqual(mock_s3_client.put_object.call_count, 2)
                mock_s3_client.put_object.assert_any_call(
                    Bucket="test-bucket", Key="test-prefix/file1.py", Body=mocked_open.return_value
                )
                mock_s3_client.put_object.assert_any_call(
                    Bucket="test-bucket", Key="test-prefix/file2.py", Body=mocked_open.return_value
                )

    @patch("sys.modules", {"boto3": MagicMock()})
    @patch("wmk.packager.os.path.exists")
    def test_upload_files_to_s3_file_not_found(self, mock_exists):
        # Setup mocks
        mock_exists.side_effect = [False, True]  # First file doesn't exist, second does

        # Create a mock boto3 module
        mock_boto3 = MagicMock()
        mock_s3_client = MagicMock()
        mock_boto3.client.return_value = mock_s3_client

        # Patch the boto3 import
        with patch.dict("sys.modules", {"boto3": mock_boto3}):
            mocked_open = mock_open(read_data=b"file content")
            with patch("builtins.open", mocked_open):
                result = self.packager.upload_files_to_s3(
                    ["missing.py", "file2.py"], "test-bucket", "test-prefix"
                )
                self.assertTrue(result)

                # Verify only one file was uploaded
                self.assertEqual(mock_s3_client.put_object.call_count, 1)
                mock_s3_client.put_object.assert_called_once_with(
                    Bucket="test-bucket", Key="test-prefix/file2.py", Body=mocked_open.return_value
                )

    @patch("sys.modules", {"boto3": MagicMock()})
    @patch("wmk.packager.os.path.exists")
    def test_upload_files_to_s3_upload_error(self, mock_exists):
        # Setup mocks
        mock_exists.return_value = True

        # Create a mock boto3 module
        mock_boto3 = MagicMock()
        mock_s3_client = MagicMock()
        mock_s3_client.put_object.side_effect = Exception("S3 error")
        mock_boto3.client.return_value = mock_s3_client

        # Patch the boto3 import
        with patch.dict("sys.modules", {"boto3": mock_boto3}):
            mocked_open = mock_open(read_data=b"file content")
            with patch("builtins.open", mocked_open):
                result = self.packager.upload_files_to_s3(
                    ["file1.py"], "test-bucket", "test-prefix"
                )
                # Method should still return True even if individual uploads fail
                self.assertTrue(result)
                mock_s3_client.put_object.assert_called_once()

    def test_upload_files_to_s3_general_error(self):
        # Create a mock boto3 module that raises an exception
        mock_boto3 = MagicMock()
        mock_boto3.client.side_effect = Exception("General error")

        # Patch the boto3 import
        with patch.dict("sys.modules", {"boto3": mock_boto3}):
            result = self.packager.upload_files_to_s3(["file1.py"], "test-bucket", "test-prefix")
            self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
