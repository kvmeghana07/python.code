import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

from display_contents import get_item_type, display_directory


class TestDisplayContents(unittest.TestCase):

    def test_get_item_type_dir_and_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            file_path = tmp_path / "test_file.txt"
            file_path.write_text("hello")

            sub_dir = tmp_path / "sub_dir"
            sub_dir.mkdir()

            self.assertEqual(get_item_type(file_path), "File")
            self.assertEqual(get_item_type(sub_dir), "Directory")

    def test_get_item_type_symlink(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            file_path = tmp_path / "target.txt"
            file_path.write_text("hello")
            symlink_path = tmp_path / "link.txt"

            try:
                symlink_path.symlink_to(file_path)
                self.assertEqual(get_item_type(symlink_path), "Symlink")
            except OSError:
                # Symlinks might require elevated privileges on some platforms/Windows environments
                self.skipTest("Symlinks not supported in environment")

    def test_display_directory_recursive_structure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)

            # Create subfolder structure:
            # root/
            # ├── dir1/
            # │   └── file1.txt
            # ├── .hidden_dir/
            # │   └── hidden_file.txt
            # └── file2.txt

            dir1 = root / "dir1"
            dir1.mkdir()
            (dir1 / "file1.txt").write_text("file1 content")

            hidden_dir = root / ".hidden_dir"
            hidden_dir.mkdir()
            (hidden_dir / "hidden_file.txt").write_text("hidden file content")

            (root / "file2.txt").write_text("file2 content")

            # Capture stdout without hidden files
            captured_output = io.StringIO()
            sys.stdout = captured_output
            try:
                display_directory(root, show_hidden=False)
            finally:
                sys.stdout = sys.__stdout__

            output = captured_output.getvalue()

            self.assertIn("dir1 [Directory]", output)
            self.assertIn("file1.txt [File]", output)
            self.assertIn("file2.txt [File]", output)
            self.assertNotIn(".hidden_dir", output)
            self.assertNotIn("hidden_file.txt", output)

            # Capture stdout with hidden files
            captured_output_all = io.StringIO()
            sys.stdout = captured_output_all
            try:
                display_directory(root, show_hidden=True)
            finally:
                sys.stdout = sys.__stdout__

            output_all = captured_output_all.getvalue()

            self.assertIn("dir1 [Directory]", output_all)
            self.assertIn("file1.txt [File]", output_all)
            self.assertIn("file2.txt [File]", output_all)
            self.assertIn(".hidden_dir [Directory]", output_all)
            self.assertIn("hidden_file.txt [File]", output_all)


if __name__ == "__main__":
    unittest.main()
