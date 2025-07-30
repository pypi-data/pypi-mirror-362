"""Add command implementation for tracking data files and metadata."""

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import click
import yaml

from biotope.utils import find_biotope_root, is_git_repo


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path))
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="Add directories recursively",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force add even if file already tracked",
)
def add(paths: tuple[Path, ...], recursive: bool, force: bool) -> None:
    """
    Add data files to biotope project and stage for metadata creation.
    
    This command calculates checksums for data files and prepares them for metadata
    annotation. Files are tracked in the .biotope/datasets/ directory with their
    checksums embedded in Croissant ML metadata.
    
    Args:
        paths: Files or directories to add
        recursive: Add directories recursively
        force: Force add even if already tracked
    """
    if not paths:
        click.echo("❌ No paths specified. Use 'biotope add <file_or_directory>'")
        raise click.Abort

    # Find biotope project root
    biotope_root = find_biotope_root()
    if not biotope_root:
        click.echo("❌ Not in a biotope project. Run 'biotope init' first.")
        raise click.Abort

    # Check if we're in a Git repository
    if not is_git_repo(biotope_root):
        click.echo("❌ Not in a Git repository. Initialize Git first with 'git init'.")
        raise click.Abort

    datasets_dir = biotope_root / ".biotope" / "datasets"
    datasets_dir.mkdir(parents=True, exist_ok=True)

    added_files = []
    skipped_files = []

    for path in paths:
        if path.is_file():
            result = _add_file(path, biotope_root, datasets_dir, force)
            if result:
                added_files.append(path)
            else:
                skipped_files.append(path)
        elif path.is_dir() and recursive:
            for file_path in path.rglob("*"):
                if file_path.is_file():
                    result = _add_file(file_path, biotope_root, datasets_dir, force)
                    if result:
                        added_files.append(file_path)
                    else:
                        skipped_files.append(file_path)
        elif path.is_dir():
            click.echo(f"⚠️  Skipping directory '{path}' (use --recursive to add contents)")
            skipped_files.append(path)

    # Stage changes in Git
    if added_files:
        _stage_git_changes(biotope_root)

    # Report results
    if added_files:
        click.echo(f"\n✅ Added {len(added_files)} file(s) to biotope project:")
        for file_path in added_files:
            click.echo(f"  + {file_path}")
    
    if skipped_files:
        click.echo(f"\n⚠️  Skipped {len(skipped_files)} file(s):")
        for file_path in skipped_files:
            click.echo(f"  - {file_path}")

    if added_files:
        click.echo(f"\n💡 Next steps:")
        click.echo(f"  1. Run 'biotope status' to see staged files")
        click.echo(f"  2. Run 'biotope annotate interactive --staged' to create metadata")
        click.echo(f"  3. Run 'biotope commit -m \"message\"' to save changes")


def _add_file(
    file_path: Path, 
    biotope_root: Path, 
    datasets_dir: Path, 
    force: bool
) -> bool:
    """Add a single file to the biotope project."""
    
    # Resolve the file path to absolute path if it's relative
    if not file_path.is_absolute():
        file_path = file_path.resolve()
    
    # Calculate checksum
    sha256_hash = calculate_file_checksum(file_path)
    
    # Check if already tracked
    if not force and is_file_tracked(file_path, biotope_root):
        click.echo(f"⚠️  File '{file_path}' already tracked (use --force to override)")
        return False
    
    # Create basic metadata entry
    metadata = {
        "@context": {"@vocab": "https://schema.org/"},
        "@type": "Dataset",
        "name": file_path.stem,
        "description": f"Dataset for {file_path.name}",
        "distribution": [
            {
                "@type": "sc:FileObject",
                "@id": f"file_{sha256_hash[:8]}",
                "name": file_path.name,
                "contentUrl": str(file_path.relative_to(biotope_root)),
                "sha256": sha256_hash,
                "contentSize": file_path.stat().st_size,
                "dateCreated": datetime.now(timezone.utc).isoformat()
            }
        ]
    }
    
    # Save metadata to datasets directory
    metadata_file = datasets_dir / f"{file_path.stem}.jsonld"
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)
    
    click.echo(f"📁 Added {file_path} (SHA256: {sha256_hash[:8]}...)")
    return True


def calculate_file_checksum(file_path: Path) -> str:
    """Calculate SHA256 checksum of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


def is_file_tracked(file_path: Path, biotope_root: Path) -> bool:
    """Check if a file is already tracked in biotope."""
    # Resolve the file path to absolute path if it's relative
    if not file_path.is_absolute():
        file_path = file_path.resolve()
    
    # Check datasets directory
    datasets_dir = biotope_root / ".biotope" / "datasets"
    for dataset_file in datasets_dir.glob("*.jsonld"):
        try:
            with open(dataset_file) as f:
                metadata = json.load(f)
                for distribution in metadata.get("distribution", []):
                    if distribution.get("contentUrl") == str(file_path.relative_to(biotope_root)):
                        return True
        except (json.JSONDecodeError, KeyError):
            continue
    
    return False


def _stage_git_changes(biotope_root: Path) -> None:
    """Stage .biotope/ changes in Git."""
    try:
        subprocess.run(
            ["git", "add", ".biotope/"],
            cwd=biotope_root,
            check=True
        )
    except subprocess.CalledProcessError as e:
        click.echo(f"⚠️  Warning: Could not stage changes in Git: {e}")


 