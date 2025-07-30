"""Initialize command implementation."""

from datetime import datetime, timezone
from pathlib import Path

import click
import yaml

from biotope.utils import is_git_repo


@click.command()
@click.option(
    "--dir",
    "-d",
    type=click.Path(file_okay=False, path_type=Path),
    default=".",
    help="Directory to initialize biotope project in",
)
def init(dir: Path) -> None:  # noqa: A002
    """
    Initialize a new biotope with interactive configuration in the specified directory.
    """
    # Check if .biotope directory already exists
    biotope_dir = dir / ".biotope"
    if biotope_dir.exists():
        click.echo("❌ A biotope project already exists in this directory.")
        click.echo("To start fresh, remove the .biotope directory first.")
        raise click.Abort

    click.echo("Establishing biotope! Let's set up your project.\n")

    # Project name
    project_name = click.prompt(
        "What's your project name?",
        type=str,
        default=dir.absolute().name,
    )

    # Knowledge sources
    knowledge_sources = []
    if click.confirm("Would you like to add knowledge sources now?", default=True):
        while True:
            source = click.prompt(
                "\nEnter knowledge source (or press enter to finish)",
                type=str,
                default="",
                show_default=False,
            )
            if not source:
                break
            source_type = click.prompt(
                "What type of source is this?",
                type=click.Choice(["database", "file", "api"], case_sensitive=False),
                default="database",
            )
            knowledge_sources.append({"name": source, "type": source_type})

    # Output preferences
    output_format = click.prompt(
        "\nPreferred output format",
        type=click.Choice(["neo4j", "csv", "json"], case_sensitive=False),
        default="neo4j",
    )

    # LLM integration
    use_llm = click.confirm("\nWould you like to set up LLM integration?", default=True)
    if use_llm:
        llm_provider = click.prompt(
            "Which LLM provider would you like to use?",
            type=click.Choice(["openai", "anthropic", "local"], case_sensitive=False),
            default="openai",
        )

        if llm_provider in ["openai", "anthropic"]:
            api_key = click.prompt(
                f"Please enter your {llm_provider} API key",
                type=str,
                hide_input=True,
            )

    # Create user configuration
    user_config = {
        "project": {
            "name": project_name,
            "output_format": output_format,
        },
        "knowledge_sources": knowledge_sources,
    }

    if use_llm:
        user_config["llm"] = {
            "provider": llm_provider,
            "api_key": api_key if llm_provider in ["openai", "anthropic"] else None,
        }

    # Create internal metadata
    metadata = {
        "project_name": project_name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "biotope_version": click.get_current_context().obj.get("version", "unknown"),
        "last_modified": datetime.now(timezone.utc).isoformat(),
        "builds": [],
        "knowledge_sources": knowledge_sources,
    }

    # Create project structure
    try:
        dir.mkdir(parents=True, exist_ok=True)
        create_project_structure(dir, user_config, metadata)
        
        # Initialize Git if not already initialized
        if not is_git_repo(dir):
            if click.confirm("\nWould you like to initialize Git for version control?", default=True):
                _init_git_repo(dir)
                click.echo("✅ Git repository initialized")
        
        click.echo("\n✨ Biotope established successfully! ✨")
        click.echo(
            f"\nYour biotope '{project_name}' has been established. Make sure to water regularly.",
        )
        click.echo("\nNext steps:")
        click.echo("1. Review the configuration in config/biotope.yaml")
        click.echo("2. Add your knowledge sources")
        click.echo("3. Run 'biotope add <file>' to stage data files")
        click.echo("4. Run 'biotope annotate interactive --staged' to create metadata")
        click.echo("5. Run 'biotope commit -m \"message\"' to save changes")
    except (OSError, yaml.YAMLError) as e:
        click.echo(f"\n❌ Error initializing project: {e!s}", err=True)
        raise click.Abort from e


def create_project_structure(directory: Path, config: dict, metadata: dict) -> None:
    """
    Create the project directory structure and configuration files.

    Args:
        directory: Project directory path
        config: User-facing configuration dictionary
        metadata: Internal metadata dictionary

    """
    # Create directory structure - git-on-top layout
    dirs = [
        ".biotope",
        ".biotope/config",  # Configuration for biotope project
        ".biotope/datasets",  # Stores Croissant ML JSON-LD files
        ".biotope/workflows",  # Bioinformatics workflow definitions
        ".biotope/logs",  # Command execution logs
        "config",
        "data",
        "data/raw",
        "data/processed",
        "schemas",
        "outputs",
    ]

    for d in dirs:
        (directory / d).mkdir(parents=True, exist_ok=True)

    # Create files
    (directory / "config" / "biotope.yaml").write_text(
        yaml.dump(config, default_flow_style=False),
    )

    (directory / ".biotope" / "metadata.yaml").write_text(
        yaml.dump(metadata, default_flow_style=False),
    )

    # Create initial biotope config
    biotope_config = {
        "version": "1.0",
        "croissant_schema_version": "1.0",
        "default_metadata_template": "scientific",
        "data_storage": {
            "type": "local",
            "path": "data"
        },
        "checksum_algorithm": "sha256",
        "auto_stage": True,
        "commit_message_template": "Update metadata: {description}",
        "annotation_validation": {
            "enabled": True,
            "minimum_required_fields": [
                "name",
                "description", 
                "creator",
                "dateCreated",
                "distribution"
            ],
            "field_validation": {
                "name": {"type": "string", "min_length": 1},
                "description": {"type": "string", "min_length": 10},
                "creator": {"type": "object", "required_keys": ["name"]},
                "dateCreated": {"type": "string", "format": "date"},
                "distribution": {"type": "array", "min_length": 1}
            }
        }
    }
    
    (directory / ".biotope" / "config" / "biotope.yaml").write_text(
        yaml.dump(biotope_config, default_flow_style=False),
    )

    # Note: No custom refs needed - Git handles all version control

    # Create README
    readme_content = f"""# {config["project"]["name"]}

A BioCypher knowledge graph project managed with biotope.

## Project Structure

- `config/`: User configuration files
- `data/`: Data files
  - `raw/`: Raw input data
  - `processed/`: Processed data
- `schemas/`: Knowledge schema definitions
- `outputs/`: Generated knowledge graphs
- `.biotope/`: Biotope project management (Git-tracked)
  - `datasets/`: Croissant ML metadata files
  - `workflows/`: Bioinformatics workflow definitions
  - `config/`: Biotope configuration
  - `logs/`: Command execution history

## Git Integration

This project uses Git for metadata version control. The `.biotope/` directory is tracked by Git, allowing you to:
- Version control your metadata changes
- Collaborate with others on metadata
- Use standard Git tools and workflows

## Getting Started

1. Add data files: `biotope add <data_file>`
2. Create metadata: `biotope annotate interactive --staged`
3. Check status: `biotope status`
4. Commit changes: `biotope commit -m "Add new dataset"`
5. View history: `biotope log`
6. Push/pull: `biotope push` / `biotope pull`

## Standard Git Commands

You can also use standard Git commands:
- `git status` - See all project changes
- `git log -- .biotope/` - View metadata history
- `git diff .biotope/` - See metadata changes
"""
    (directory / "README.md").write_text(readme_content)





def _init_git_repo(directory: Path) -> None:
    """Initialize a Git repository in the directory."""
    try:
        import subprocess
        subprocess.run(
            ["git", "init"],
            cwd=directory,
            check=True
        )
        
        # Create initial commit
        subprocess.run(
            ["git", "add", "."],
            cwd=directory,
            check=True
        )
        
        subprocess.run(
            ["git", "commit", "-m", "Initial biotope project setup"],
            cwd=directory,
            check=True
        )
        
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        click.echo(f"⚠️  Warning: Could not initialize Git: {e}")
