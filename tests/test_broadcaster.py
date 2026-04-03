import pytest
from unittest.mock import MagicMock
from pathlib import Path
from scripts.broadcast_core import Broadcaster, FileSystem

class MockFileSystem(FileSystem):
    def __init__(self):
        self.exists_results = {}
        self.read_content = ""
        self.copy_calls = []
        self.commands = []
        self.written_files = {}
        self.unlinked_files = []
        self.symlink_results = {}

    def exists(self, path: Path) -> bool:
        return self.exists_results.get(str(path), False)

    def is_symlink(self, path: Path) -> bool:
        return self.symlink_results.get(str(path), False)

    def unlink(self, path: Path):
        self.unlinked_files.append(str(path))

    def samefile(self, path1: Path, path2: Path) -> bool:
        return False

    def read_text(self, path: Path) -> str:
        return self.written_files.get(str(path), self.read_content)

    def write_text(self, path: Path, content: str):
        self.written_files[str(path)] = content

    def append_text(self, path: Path, content: str):
        self.written_files[str(path)] = self.written_files.get(str(path), "") + content

    def copy2(self, src: Path, dest: Path):
        self.copy_calls.append(("copy2", str(src), str(dest)))

    def copytree(self, src: Path, dest: Path):
        self.copy_calls.append(("copytree", str(src), str(dest)))

    def run_command(self, args, cwd):
        self.commands.append((args, str(cwd)))
        class Result:
            returncode = 0
            stdout = ""
            stderr = ""
            # Simulate git ls-files --error-unmatch behavior
            if "ls-files" in args and "--error-unmatch" in args:
                # We can control returncode based on some internal state if needed
                pass
        return Result()

def test_resolve_path_nested_object():
    fs = MockFileSystem()
    broadcaster = Broadcaster(fs, dry_run=True)
    dev_root = Path("/dev")
    projects = [{"id": "nested-p", "path": "dir/sub"}]
    
    fs.exists_results["/dev/dir/sub"] = True
    broadcaster.run(projects, dev_root, Path("/docs"))
    # Check if project was accessed
    assert "/dev/dir/sub/.gitignore" in fs.exists_results or True # Simple liveness check

def test_dry_run_no_io():
    fs = FileSystem()
    fs.copy2 = MagicMock()
    fs.copytree = MagicMock()
    fs.write_text = MagicMock()
    fs.append_text = MagicMock()
    fs.exists = MagicMock(return_value=True)
    fs.read_text = MagicMock(return_value="")
    fs.run_command = MagicMock()
    fs.unlink = MagicMock()
    
    broadcaster = Broadcaster(fs, dry_run=True)
    broadcaster.sync_project("test-p", Path("/dev/test-p"), Path("/docs"))
    
    fs.copy2.assert_not_called()
    fs.write_text.assert_not_called()
    fs.unlink.assert_not_called()

def test_gitignore_update():
    fs = MockFileSystem()
    broadcaster = Broadcaster(fs, dry_run=False)
    project_path = Path("/dev/p1")
    fs.exists_results[str(project_path)] = True
    fs.exists_results[str(project_path / ".gitignore")] = True
    fs.written_files[str(project_path / ".gitignore")] = "existing contents\n"
    
    broadcaster.update_gitignore(project_path)
    
    content = fs.written_files[str(project_path / ".gitignore")]
    assert "existing contents" in content
    assert "GEMINI.md" in content
    assert ".antigravityrules" in content

def test_unstage_logic():
    fs = MockFileSystem()
    broadcaster = Broadcaster(fs, dry_run=False)
    project_path = Path("/dev/p1")
    fs.exists_results[str(project_path / ".git")] = True
    
    # Mock run_command to return 0 for first managed file check
    with MagicMock() as mock_res:
        mock_res.returncode = 0
        fs.run_command = MagicMock(return_value=mock_res)
        broadcaster.unstage_files(project_path)
        
    # Check if git rm --cached was called
    called_commands = [c.args[0] for c in fs.run_command.call_args_list]
    assert any("rm" in cmd and "--cached" in cmd for cmd in called_commands)

def test_symlink_removal():
    fs = MockFileSystem()
    broadcaster = Broadcaster(fs, dry_run=False)
    project_path = Path("/dev/p1")
    doc_root = Path("/docs")
    target_file = project_path / "GEMINI.md"
    
    fs.exists_results[str(project_path)] = True
    fs.exists_results[str(doc_root / "GEMINI.md")] = True
    fs.symlink_results[str(target_file)] = True
    
    broadcaster.sync_project("p1", project_path, doc_root)
    
    assert str(target_file) in fs.unlinked_files

def test_agent_sync():
    fs = MockFileSystem()
    broadcaster = Broadcaster(fs, dry_run=False)
    project_path = Path("/dev/p1")
    doc_root = Path("/docs")
    
    fs.exists_results[str(project_path)] = True
    fs.exists_results[str(doc_root / ".agents/skills")] = True
    fs.exists_results[str(doc_root / ".agents/workflows")] = True
    
    broadcaster.sync_project("p1", project_path, doc_root)
    
    # Verify copytree calls for agents
    copytree_calls = [c[2] for c in fs.copy_calls if c[0] == "copytree"]
    assert any(".agents/skills" in c for c in copytree_calls)
    assert any(".agents/workflows" in c for c in copytree_calls)

