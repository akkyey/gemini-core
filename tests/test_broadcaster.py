import pytest
from pathlib import Path
from scripts.broadcast_core import Broadcaster, FileSystem

class MockFileSystem(FileSystem):
    def __init__(self):
        self.exists_results = {}
        self.read_content = ""
        self.copy_calls = []
        self.commands = []
        self.written_files = {}

    def exists(self, path: Path) -> bool:
        return self.exists_results.get(str(path), True)

    def is_symlink(self, path: Path) -> bool:
        return False

    def samefile(self, path1: Path, path2: Path) -> bool:
        return False

    def read_text(self, path: Path) -> str:
        return self.read_content

    def write_text(self, path: Path, content: str):
        self.written_files[str(path)] = content

    def append_text(self, path: Path, content: str):
        self.written_files[str(path)] = self.written_files.get(str(path), "") + content

    def copy2(self, src: Path, dest: Path):
        self.copy_calls.append((src, dest))

    def copytree(self, src: Path, dest: Path):
        self.copy_calls.append((src, dest))

    def run_command(self, args, cwd):
        self.commands.append((args, cwd))
        class Result:
            returncode = 0
            stdout = ""
            stderr = ""
        return Result()

def test_resolve_path_nested_object():
    fs = MockFileSystem()
    broadcaster = Broadcaster(fs, dry_run=True)
    dev_root = Path("/dev")
    projects = [{"id": "nested-p", "path": "dir/sub"}]
    
    # Enable project existence
    fs.exists_results["/dev/dir/sub"] = True
    broadcaster.run(projects, dev_root, Path("/docs"))
    # In dry-run + run calls sync_project, we can see if it proceeded.
    # Check if update_gitignore was logged or similar.
    # (Actually we can't easily check prints here without capsys)

def test_dry_run_no_io(mocker):
    fs = FileSystem()
    # Mock all destructive methods
    mocker.patch.object(fs, 'copy2')
    mocker.patch.object(fs, 'copytree')
    mocker.patch.object(fs, 'write_text')
    mocker.patch.object(fs, 'append_text')
    mocker.patch.object(fs, 'exists', return_value=True)
    mocker.patch.object(fs, 'read_text', return_value="")
    mocker.patch.object(fs, 'run_command')
    
    broadcaster = Broadcaster(fs, dry_run=True)
    broadcaster.sync_project("test-p", Path("/dev/test-p"), Path("/docs"))
    
    # In dry-run, side-effects should NOT be called
    fs.copy2.assert_not_called()
    fs.write_text.assert_not_called()

def test_real_io_prevention_on_fail_docs(mocker):
    fs = FileSystem()
    mocker.patch.object(fs, 'copy2')
    mocker.patch.object(fs, 'write_text') # Crucial fix
    mocker.patch.object(fs, 'append_text')
    mocker.patch.object(fs, 'exists', side_effect=lambda p: str(p) == "/dev/p") # Docs don't exist
    mocker.patch.object(fs, 'read_text', return_value="")
    
    broadcaster = Broadcaster(fs, dry_run=False)
    broadcaster.sync_project("p", Path("/dev/p"), Path("/docs"))
    
    # Copy should not happen because master source doesn't exist
    fs.copy2.assert_not_called()

def test_path_resolution_logic():
    fs = MockFileSystem()
    broadcaster = Broadcaster(fs, dry_run=True)
    dev_root = Path("/dev")
    doc_root = Path("/docs")
    
    fs.exists_results = {
        str(dev_root / "p1"): True,
        str(dev_root / "nested/path"): True,
        str(doc_root / "GEMINI.md"): True
    }
    
    projects = ["p1", {"id": "p2", "path": "nested/path"}]
    broadcaster.run(projects, dev_root, doc_root)
    # Success means no exception
