import pytest
import os
import datetime
from pathlib import Path
from typing import Set, List, Optional, Tuple

import pathspec # Direct import, assume it's installed
# Import the main orchestrator for the helper function, exceptions, and utils
from jinni.core_logic import read_context # Keep for run_read_context_helper
from jinni.exceptions import ContextSizeExceededError, DetailedContextSizeError # Moved exceptions
from jinni.utils import _find_context_files_for_dir # Moved helper
from jinni.config_system import CONTEXT_FILENAME, DEFAULT_RULES # Import constants
from jinni.utils import ensure_no_nul
# SEPARATOR is not directly used/tested here

# --- Test Fixture ---

@pytest.fixture
def test_dir(tmp_path: Path) -> Path:
    """Creates a standard test directory structure."""
    root = tmp_path / "project"
    root.mkdir()

    # Root level files and dirs
    (root / "README.md").write_text("# Project", encoding='utf-8')
    (root / "main.py").write_text("print('main')", encoding='utf-8')
    (root / ".env").write_text("SECRET=123", encoding='utf-8') # Should be excluded by default
    (root / "config.yaml").write_text("key: value", encoding='utf-8')
    (root / "temp.tmp").touch() # Should be excluded by default
    (root / "image.jpg").write_bytes(b'\xff\xd8\xff\xe0') # Binary

    # Src directory
    (root / "src").mkdir()
    (root / "src" / "app.py").write_text("print('app')", encoding='utf-8')
    (root / "src" / "utils.py").write_text("def helper(): pass", encoding='utf-8')
    (root / "src" / "data.json").write_text('{"data": true}', encoding='utf-8')
    (root / "src" / ".hidden_in_src").touch() # Hidden

    # Lib directory (should be excluded by default)
    (root / "lib").mkdir()
    (root / "lib" / "somelib.py").write_text("# Library code", encoding='utf-8')
    (root / "lib" / "binary.dll").write_bytes(b'\x4d\x5a\x90\x00') # Binary

    # Docs directory
    (root / "docs").mkdir()
    (root / "docs" / "index.md").write_text("Docs index", encoding='utf-8')
    (root / "docs" / "config").mkdir()
    (root / "docs" / "config" / "options.md").write_text("Config options", encoding='utf-8')

    # Nested directory to test hierarchy
    (root / "src" / "nested").mkdir()
    (root / "src" / "nested" / "deep.py").write_text("# Deep", encoding='utf-8')
    (root / "src" / "nested" / "other.txt").write_text("Nested text", encoding='utf-8')

    # Build directory (should be excluded by default)
    (root / "build").mkdir()
    (root / "build" / "output.bin").touch()

    # Symlink (if possible)
    symlink_target = root / "main.py"
    symlink_path = root / "main_link.py"
    if symlink_target.exists():
         try:
            symlink_path.symlink_to(symlink_target)
         except OSError:
             print("Warning: Symlink creation failed in test setup.")

    return root

# Helper function to run read_context and normalize output
def run_read_context_helper(
    project_root_rel: str, # Project root relative to tmp_path (required)
    tmp_path: Path,
    target_rel: Optional[str] = None, # Target relative to tmp_path (optional)
    override_rules: Optional[List[str]] = None,
    list_only: bool = False,
    size_limit_mb: Optional[int] = None,
    debug_explain: bool = False,
    include_size_in_list: bool = False # Keep this arg
) -> str:
    """Runs read_context with absolute paths and returns normalized output."""

    project_root_abs_path = str(tmp_path / project_root_rel)
    # Determine the target paths list for the core_logic signature
    if target_rel:
        target_abs_path_str = str(tmp_path / target_rel)
        target_paths_list = [target_abs_path_str]
    else:
        # If no specific target, the project root itself is the target
        target_paths_list = [project_root_abs_path]

    content = read_context(
        target_paths_str=target_paths_list,       # Pass the list of target paths
        project_root_str=project_root_abs_path, # Pass the optional project root for output relativity
        override_rules=override_rules,
        list_only=list_only,
        size_limit_mb=size_limit_mb,
        debug_explain=debug_explain,
        include_size_in_list=include_size_in_list # Pass through
    )
    # Normalize line endings and strip leading/trailing whitespace for comparison
    # For list_only, sort the lines
    if list_only:
        lines = sorted([line.rstrip() for line in content.splitlines() if line.strip()])
        return "\n".join(lines)
    else:
        # For content, just normalize line endings and strip outer whitespace
        normalized_content = "\n".join(line.rstrip() for line in content.splitlines()).strip()
        return normalized_content


# --- Test Cases ---

def test_read_context_no_rules_defaults(test_dir: Path):
    """Test processing with no rules - relies on default exclusions."""
    content = run_read_context_helper("project", test_dir.parent) # Root is project, target is None

    # Check for files expected to be included (not excluded by defaults)
    assert "```path=README.md" in content
    assert "```path=main.py" in content
    assert "```path=config.yaml" in content
    assert "```path=src/app.py" in content
    assert "```path=src/utils.py" in content
    assert "```path=src/data.json" in content
    assert "```path=src/nested/deep.py" in content
    assert "```path=src/nested/other.txt" in content
    assert "```path=docs/index.md" in content
    assert "```path=docs/config/options.md" in content
    assert "```path=temp.tmp" not in content # Now excluded by default !*.tmp rule

    # Check for files/dirs expected to be excluded by defaults or type
    assert "```path=.env" not in content # Excluded by !.*
    assert "```path=image.jpg" not in content # Binary
    # assert "```path=lib/somelib.py" in content # Included by '*' default, not excluded by others - Assertion added below
    assert "```path=lib/binary.dll" not in content # Binary
    assert "```path=src/.hidden_in_src" not in content # Excluded by !.*
    assert "```path=build/output.bin" not in content # Excluded by !build/
    assert "```path=main_link.py" not in content # Symlink

def test_read_context_list_only_defaults(test_dir: Path):
    """Test list_only mode with default exclusions."""
    content = run_read_context_helper("project", test_dir.parent, list_only=True) # Root is project, target is None
    expected_files = sorted([
        "README.md",
        "main.py",
        "config.yaml",
        # "temp.tmp", # Now excluded by default !*.tmp rule
        "src/app.py",
        "src/utils.py",
        "src/data.json",
        "src/nested/deep.py",
        "src/nested/other.txt",
        "lib/somelib.py", # Included by '*' default
        "docs/index.md",
        "docs/config/options.md",
    ])
    assert content == "\n".join(expected_files)

def test_read_context_include_py_files(test_dir: Path):
    """Test including only Python files using a context file."""
    (test_dir / CONTEXT_FILENAME).write_text("**/*.py", encoding='utf-8')
    content = run_read_context_helper("project", test_dir.parent) # Root is project, target is None

    assert "```path=main.py" in content
    assert "```path=src/app.py" in content
    assert "```path=src/utils.py" in content
    assert "```path=src/nested/deep.py" in content
    assert "```path=lib/somelib.py" in content # Now included because of rule

    assert "```path=README.md" in content # Included by default '*'
    assert "```path=config.yaml" in content # Included by default '*'
    assert "```path=src/data.json" in content # Included by default '*'

def test_read_context_exclude_overrides_include(test_dir: Path):
    """Test exclusion pattern overriding inclusion in the same file."""
    (test_dir / CONTEXT_FILENAME).write_text("**/*.py\n!src/utils.py", encoding='utf-8') # Corrected path
    content = run_read_context_helper("project", test_dir.parent) # Root is project, target is None

    assert "```path=main.py" in content
    assert "```path=src/app.py" in content
    assert "```path=src/nested/deep.py" in content
    assert "```path=lib/somelib.py" in content
    assert "```path=src/utils.py" not in content # Excluded

def test_read_context_directory_exclusion(test_dir: Path):
    """Test excluding a directory prevents processing files within."""
    (test_dir / CONTEXT_FILENAME).write_text("**/*.py\n!lib/", encoding='utf-8') # Corrected path
    content = run_read_context_helper("project", test_dir.parent) # Root is project, target is None

    assert "```path=main.py" in content
    assert "```path=src/app.py" in content
    assert "```path=lib/somelib.py" not in content # Excluded via directory rule

def test_read_context_hierarchy_sub_includes(test_dir: Path):
    """Test sub .contextfiles including files not matched by root."""
    (test_dir / CONTEXT_FILENAME).write_text("project/*.md", encoding='utf-8') # Root includes only root md
    (test_dir / "src" / CONTEXT_FILENAME).write_text("*.json", encoding='utf-8') # Src includes json

    content = run_read_context_helper("project", test_dir.parent) # Root is project, target is None

    assert "```path=README.md" in content
    assert "```path=docs/index.md" in content # Matched by root rule *.md
    assert "```path=src/data.json" in content # Included by sub rule *.json
    assert "```path=main.py" in content # Included by default '*'
    assert "```path=src/app.py" in content # Included by default '*'

def test_read_context_hierarchy_sub_excludes(test_dir: Path):
    """Test sub .contextfiles excluding files matched by root."""
    (test_dir / CONTEXT_FILENAME).write_text("**/*.py", encoding='utf-8') # Root includes all py
    (test_dir / "src" / CONTEXT_FILENAME).write_text("!app.py", encoding='utf-8') # Src excludes app.py

    content = run_read_context_helper("project", test_dir.parent) # Root is project, target is None

    assert "```path=main.py" in content
    assert "```path=src/utils.py" in content # Included by root, not excluded by sub
    assert "```path=src/nested/deep.py" in content # Included by root
    assert "```path=lib/somelib.py" in content # Included by root
    assert "```path=src/app.py" not in content # Excluded by sub rule

def test_read_context_override_rules(test_dir: Path):
    """Test using override rules as additions to context files."""
    (test_dir / CONTEXT_FILENAME).write_text("**/*.py", encoding='utf-8') # File includes py
    override = ["src/app.py", "**/*.md", "**/*.py", "src/"] # Use recursive glob for markdown
    content = run_read_context_helper("project", test_dir.parent, override_rules=override) # Root is project, target is None

    assert "```path=src/app.py" in content # Included by override
    assert "```path=README.md" in content # Included by override
    assert "```path=docs/index.md" in content # Included by override
    assert "```path=docs/config/options.md" in content # Included by override

    # These are included by contextfiles and/or overrides
    assert "```path=main.py" in content # Included by **/*.py
    assert "```path=src/utils.py" in content # Included by **/*.py
    # config.yaml is included by default '*' rule (not excluded by any rule)
    assert "```path=config.yaml" in content

def test_read_context_binary_skip(test_dir: Path):
    """Test binary files are skipped even if rules include them."""
    (test_dir / CONTEXT_FILENAME).write_text("*", encoding='utf-8') # Include everything
    content = run_read_context_helper("project", test_dir.parent) # Root is project, target is None

    assert "```path=image.jpg" not in content
    assert "```path=lib/binary.dll" not in content
    assert "```path=main.py" in content # Text file still included

def test_read_context_symlink_skip(test_dir: Path):
    """Test symlinks are skipped."""
    symlink_path = test_dir / "main_link.py"
    if not symlink_path.exists():
         pytest.skip("Symlink does not exist, skipping test.")
    (test_dir / CONTEXT_FILENAME).write_text("*.py", encoding='utf-8')
    content = run_read_context_helper("project", test_dir.parent) # Root is project, target is None
    assert "```path=main.py" in content
    assert "```path=main_link.py" not in content

def test_read_context_size_limit_exceeded(test_dir: Path):
    """Test exceeding size limit raises error."""
    (test_dir / CONTEXT_FILENAME).write_text("**/*.py", encoding='utf-8')
    limit_mb = 0.0001 # ~100 bytes
    with pytest.raises(DetailedContextSizeError):
        run_read_context_helper("project", test_dir.parent, size_limit_mb=limit_mb) # Root is project, target is None

def test_read_context_target_file(test_dir: Path):
    """Test processing a specific target file within the project root."""
    (test_dir / CONTEXT_FILENAME).write_text("!**/*.py", encoding='utf-8') # Exclude all py
    # Target main.py directly, root is project
    content = run_read_context_helper(project_root_rel="project", tmp_path=test_dir.parent, target_rel="project/main.py")
    # Rule doesn't apply to target file itself, only binary/size checks
    assert "```path=main.py" in content # Path relative to project root
    assert "print('main')" in content
    assert "```path=src/app.py" not in content # Other files not included

def test_read_context_target_dir(test_dir: Path):
    """Test processing a specific target directory within the project root."""
    # Add a rule in the root context file that should apply when targeting src
    (test_dir / CONTEXT_FILENAME).write_text("!**/utils.py", encoding='utf-8')
    # Add a context file inside the target directory
    (test_dir / "src" / CONTEXT_FILENAME).write_text("!data.json", encoding='utf-8') # Exclude data.json locally

    # Target src directory directly, root is project
    content = run_read_context_helper(project_root_rel="project", tmp_path=test_dir.parent, target_rel="project/src")

    # Files inside should be processed with rules from project root downwards
    # since src is within the project.
    # Output paths are still relative to the original project root.
    assert "```path=src/app.py" in content
    # utils.py should be EXCLUDED because the root rule !**/utils.py applies
    assert "```path=src/utils.py" not in content
    # data.json should be EXCLUDED by the local src/.contextfiles
    assert "```path=src/data.json" not in content
    assert "```path=src/nested/deep.py" in content
    assert "```path=src/nested/other.txt" in content
    # Hidden file should still be excluded by default rules
    assert "```path=src/.hidden_in_src" not in content
    # Files outside target dir src/ should not be included
    assert "```path=main.py" not in content
    assert "```path=README.md" not in content

# Test removed as core logic now handles a single effective target path
# def test_read_context_multiple_targets(test_dir: Path):

def test_read_context_target_file_relativity(test_dir: Path):
    """Test output path relativity when project_root is different from target's parent."""
    (test_dir / CONTEXT_FILENAME).write_text("project/src/app.py", encoding='utf-8')
    # Set project root to project/, target is project/src/app.py
    content = run_read_context_helper(
        project_root_rel="project",
        tmp_path=test_dir.parent,
        target_rel="project/src/app.py"
    )
    # Path in header should be relative to project/
    assert "```path=src/app.py" in content
    assert "```path=app.py" not in content

def test_read_context_target_outside_root_error(test_dir: Path):
    """Test providing a target outside the project_root raises ValueError."""
    with pytest.raises(ValueError, match=r"Target path .* is outside the specified project root .*"): # Match full error
        run_read_context_helper(
            project_root_rel="project/src", # Root is src
            tmp_path=test_dir.parent,
            target_rel="project/main.py"    # Target is main.py (outside src)
        )

def test_find_context_files_helper(test_dir: Path):
    """Test the _find_context_files_for_dir helper directly."""
    root = test_dir
    src = test_dir / "src"
    nested = test_dir / "src" / "nested"
    docs = test_dir / "docs"

    (root / CONTEXT_FILENAME).touch()
    (src / CONTEXT_FILENAME).touch()
    (nested / CONTEXT_FILENAME).touch()
    # No context file in docs

    # Check from nested
    files = _find_context_files_for_dir(nested, root)
    assert files == [
        root / CONTEXT_FILENAME,
        src / CONTEXT_FILENAME,
        nested / CONTEXT_FILENAME,
    ]

    # Check from src
    files = _find_context_files_for_dir(src, root)
    assert files == [
        root / CONTEXT_FILENAME,
        src / CONTEXT_FILENAME,
    ]

    # Check from root
    files = _find_context_files_for_dir(root, root)
    assert files == [
        root / CONTEXT_FILENAME,
    ]

    # Check from docs (should only find root)
    files = _find_context_files_for_dir(docs, root)
    assert files == [
        root / CONTEXT_FILENAME,
    ]

    # Check outside root (should be empty)
    files = _find_context_files_for_dir(root.parent, root)
    assert files == []

def test_gitignore_respected_and_overridden(test_dir: Path):
    """Ensure .gitignore excludes files unless overridden by .contextfiles."""
    (test_dir / ".gitignore").write_text("lib/\n", encoding="utf-8")

    # Without context override, lib/ should be excluded
    content = run_read_context_helper("project", test_dir.parent)
    assert "```path=lib/somelib.py" not in content

    # Add context file that re-includes lib/
    (test_dir / CONTEXT_FILENAME).write_text("lib/\n", encoding="utf-8")
    content = run_read_context_helper("project", test_dir.parent)
    assert "```path=lib/somelib.py" in content

def test_gitignore_directory_pattern_applies_to_subdirs(test_dir: Path):
    """Test that a directory pattern like 'dirtobeignored/' in top-level .gitignore applies to subdirectories."""
    # Create the directory structure
    subdir = test_dir / "subdir"
    subdir.mkdir()
    ignored_in_root = test_dir / "dirtobeignored"
    ignored_in_root.mkdir()
    ignored_in_subdir = subdir / "dirtobeignored"
    ignored_in_subdir.mkdir()
    
    # Create test files
    (ignored_in_root / "file.txt").write_text("Should be ignored", encoding="utf-8")
    (ignored_in_subdir / "file.txt").write_text("Should also be ignored", encoding="utf-8")
    (subdir / "included.txt").write_text("Should be included", encoding="utf-8")
    
    # Create .gitignore with directory pattern
    (test_dir / ".gitignore").write_text("dirtobeignored/\n", encoding="utf-8")
    
    # Run jinni and check results
    content = run_read_context_helper("project", test_dir.parent)
    
    # Files in dirtobeignored/ at any level should be excluded
    assert "```path=dirtobeignored/file.txt" not in content
    assert "```path=subdir/dirtobeignored/file.txt" not in content
    
    # But other files should be included
    assert "```path=subdir/included.txt" in content

# Test removed as project_root is now mandatory
# def test_read_context_project_root_default(test_dir: Path):

def test_read_context_project_root_invalid(test_dir: Path):
    """Test providing an invalid project_root raises ValueError."""
    # Non-existent path
    with pytest.raises(ValueError, match="does not exist or is not a directory"):
        run_read_context_helper(
            project_root_rel="project/nonexistent", # Non-existent path
            tmp_path=test_dir.parent,
            target_rel=None # Target defaults to root
        )
    # Path is a file, not a directory
    with pytest.raises(ValueError, match="does not exist or is not a directory"):
        run_read_context_helper(
            project_root_rel="project/main.py", # Invalid root (is a file)
            tmp_path=test_dir.parent,
            target_rel=None # Target defaults to root
        )

def test_read_context_target_nonexistent(test_dir: Path):
    """Test providing a non-existent target raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match=r"Target path does not exist: .* \(resolved to .*\)"): # Revert to single backslash escape
        run_read_context_helper(
            project_root_rel="project",
            tmp_path=test_dir.parent,
            target_rel="project/nonexistent.txt" # Non-existent target
        )

# --- Test ensure_no_nul utility ---
def test_ensure_no_nul_utils():
    # Should not raise
    ensure_no_nul("abc", "test-field")
    # Should raise ValueError on NUL
    import pytest
    with pytest.raises(ValueError):
        ensure_no_nul("a\x00b", "test-field")