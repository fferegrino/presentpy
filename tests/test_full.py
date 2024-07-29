import difflib
import filecmp
import os
import shutil

from click.testing import CliRunner

from presentpy.__main__ import process


def print_file_diff(file1, file2):
    """
    Prints the differences between two files.

    :param file1: Path to the first file.
    :param file2: Path to the second file.
    """
    with open(file1, "r") as f1, open(file2, "r") as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()

    # Create a Differ object and calculate the differences
    differ = difflib.Differ()
    diff = list(differ.compare(file1_lines, file2_lines))
    print(f"Differences between {file1} and {file2}:")
    for line in diff:
        if line.startswith("- ") or line.startswith("+ ") or line.startswith("? "):
            print(line.strip())


def compare_dirs(dir1, dir2, ignore=None):
    """
    Compare two directories recursively. Files in each directory are
    assumed to be equal if their names and contents are equal.

    :param dir1: First directory path
    :param dir2: Second directory path
    :param ignore: List of names to ignore
    :return: True if the directory trees are the same, False otherwise
    """
    dirs_cmp = filecmp.dircmp(dir1, dir2, ignore=ignore)
    if dirs_cmp.left_only or dirs_cmp.right_only or dirs_cmp.funny_files:
        print(f"Differences found in directories {dir1} and {dir2}")
        print("Left only:", dirs_cmp.left_only)
        print("Right only:", dirs_cmp.right_only)
        print("Mismatched contents:", dirs_cmp.funny_files)
        return False

    # Compare common files
    (match, mismatch, errors) = filecmp.cmpfiles(dir1, dir2, dirs_cmp.common_files, shallow=False)
    if mismatch or errors:
        print(f"Files mismatch or errors encountered in {dir1} and {dir2}")
        print("Mismatched files:", mismatch)
        print("Error files:", errors)
        for file in mismatch:
            print_file_diff(os.path.join(dir1, file), os.path.join(dir2, file))
        return False

    # Recursively compare common subdirectories
    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        if not compare_dirs(new_dir1, new_dir2, ignore):
            return False

    return True


def test_process_notebook(tmp_path):
    runner = CliRunner()

    shutil.copytree("tests/files", tmp_path / "files")
    shutil.copytree("tests/outputs", tmp_path / "outputs")

    input_file = tmp_path / "files" / "test.ipynb"
    expected_folder = tmp_path / "outputs" / "test_odp"
    output_folder = tmp_path / "result_odp"
    output_file = tmp_path / "result.odp"

    with runner.isolated_filesystem(tmp_path):
        result = runner.invoke(
            process, [str(input_file), "--theme", "default", "--output", str(output_file), "--prettify"]
        )

        assert result.exit_code == 0
        assert compare_dirs(expected_folder, output_folder)
