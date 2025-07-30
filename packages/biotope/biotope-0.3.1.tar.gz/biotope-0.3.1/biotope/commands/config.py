"""Configuration management commands for biotope."""

import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from biotope.validation import load_biotope_config


@click.group()
def config() -> None:
    """Manage biotope project configuration."""


@config.command()
@click.option(
    "--field",
    "-f",
    help="Field name to add to required fields",
)
@click.option(
    "--type",
    "-t",
    type=click.Choice(["string", "object", "array"]),
    help="Data type for the field",
)
@click.option(
    "--min-length",
    type=int,
    help="Minimum length for string/array fields",
)
@click.option(
    "--required-keys",
    help="Comma-separated list of required keys for object fields",
)
def set_validation(field: Optional[str], type: Optional[str], min_length: Optional[int], required_keys: Optional[str]) -> None:
    """Set annotation validation requirements."""
    console = Console()
    
    # Find biotope project root
    biotope_root = _find_biotope_root()
    if not biotope_root:
        click.echo("❌ Not in a biotope project. Run 'biotope init' first.")
        raise click.Abort
    
    config_path = biotope_root / ".biotope" / "config" / "biotope.yaml"
    if not config_path.exists():
        click.echo("❌ Biotope configuration not found. Run 'biotope init' first.")
        raise click.Abort
    
    # Load current config
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        click.echo(f"❌ Error reading configuration: {e}")
        raise click.Abort
    
    # Initialize annotation_validation if it doesn't exist
    if "annotation_validation" not in config:
        config["annotation_validation"] = {
            "enabled": True,
            "minimum_required_fields": [],
            "field_validation": {}
        }
    
    # Add field to required fields
    if field:
        if field not in config["annotation_validation"]["minimum_required_fields"]:
            config["annotation_validation"]["minimum_required_fields"].append(field)
            console.print(f"✅ Added '{field}' to required fields")
        else:
            console.print(f"⚠️  Field '{field}' is already required")
    
    # Add field validation rules
    if field and type:
        field_validation = config["annotation_validation"]["field_validation"]
        field_validation[field] = {"type": type}
        
        if min_length is not None:
            field_validation[field]["min_length"] = min_length
        
        if required_keys:
            keys_list = [key.strip() for key in required_keys.split(",")]
            field_validation[field]["required_keys"] = keys_list
        
        console.print(f"✅ Added validation rules for '{field}'")
    
    # Save updated config
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        console.print("✅ Configuration updated successfully")
    except yaml.YAMLError as e:
        click.echo(f"❌ Error writing configuration: {e}")
        raise click.Abort


@config.command()
def show_validation() -> None:
    """Show current annotation validation requirements."""
    console = Console()
    
    # Find biotope project root
    biotope_root = _find_biotope_root()
    if not biotope_root:
        click.echo("❌ Not in a biotope project. Run 'biotope init' first.")
        raise click.Abort
    
    # Load config
    config = load_biotope_config(biotope_root)
    validation_config = config.get("annotation_validation", {})
    
    console.print(f"\n[bold blue]Annotation Validation Configuration[/]")
    console.print(f"Enabled: {'✅' if validation_config.get('enabled', True) else '❌'}")
    
    # Show validation pattern
    from biotope.validation import get_validation_pattern
    pattern = get_validation_pattern(biotope_root)
    console.print(f"Validation Pattern: [bold green]{pattern}[/]")
    
    # Show required fields
    required_fields = validation_config.get("minimum_required_fields", [])
    if required_fields:
        console.print(f"\n[bold green]Required Fields:[/]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Validation Rules", style="yellow")
        
        field_validation = validation_config.get("field_validation", {})
        for field in required_fields:
            rules = field_validation.get(field, {})
            field_type = rules.get("type", "any")
            
            validation_rules = []
            if "min_length" in rules:
                validation_rules.append(f"min_length: {rules['min_length']}")
            if "required_keys" in rules:
                validation_rules.append(f"required_keys: {', '.join(rules['required_keys'])}")
            
            table.add_row(field, field_type, "; ".join(validation_rules) if validation_rules else "none")
        
        console.print(table)
    else:
        console.print(f"\n[bold yellow]No required fields configured[/]")
        console.print("Use 'biotope config set-validation --field <field_name>' to add requirements")


@config.command()
def show_validation_pattern() -> None:
    """Show validation pattern information for cluster compliance checking."""
    console = Console()
    
    # Find biotope project root
    biotope_root = _find_biotope_root()
    if not biotope_root:
        click.echo("❌ Not in a biotope project. Run 'biotope init' first.")
        raise click.Abort
    
    # Get validation info
    from biotope.validation import get_validation_info
    info = get_validation_info(biotope_root)
    
    console.print(f"\n[bold blue]Validation Pattern Information[/]")
    console.print(f"Pattern: [bold green]{info['validation_pattern']}[/]")
    console.print(f"Enabled: {'✅' if info['enabled'] else '❌'}")
    
    if info['remote_configured']:
        console.print(f"Remote Validation: ✅ Configured")
        console.print(f"  URL: {info['remote_url']}")
        console.print(f"  Cache Duration: {info['cache_duration']} seconds")
        console.print(f"  Fallback to Local: {info['fallback_to_local']}")
    else:
        console.print(f"Remote Validation: ❌ Not configured")
    
    console.print(f"\n[bold green]Required Fields:[/] {len(info['required_fields'])}")
    if info['required_fields']:
        console.print(f"  {', '.join(info['required_fields'])}")
    
    # Show compliance hints for cluster administrators
    pattern = info['validation_pattern']
    if 'cluster' in pattern.lower():
        console.print(f"\n[bold green]✅ Cluster-compliant validation pattern[/]")
    elif 'storage' in pattern.lower():
        console.print(f"\n[bold green]✅ Storage management validation pattern[/]")
    else:
        console.print(f"\n[bold yellow]⚠️  Using default validation pattern[/]")
        console.print("Consider configuring cluster-specific validation if required.")


@config.command()
@click.option(
    "--pattern",
    "-p",
    required=True,
    help="Validation pattern name (e.g., 'default', 'cluster-strict', 'storage-management')",
)
def set_validation_pattern(pattern: str) -> None:
    """Set the validation pattern for this project."""
    console = Console()
    
    # Find biotope project root
    biotope_root = _find_biotope_root()
    if not biotope_root:
        click.echo("❌ Not in a biotope project. Run 'biotope init' first.")
        raise click.Abort
    
    config_path = biotope_root / ".biotope" / "config" / "biotope.yaml"
    if not config_path.exists():
        click.echo("❌ Biotope configuration not found. Run 'biotope init' first.")
        raise click.Abort
    
    # Load current config
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        click.echo(f"❌ Error reading configuration: {e}")
        raise click.Abort
    
    # Initialize annotation_validation if it doesn't exist
    if "annotation_validation" not in config:
        config["annotation_validation"] = {}
    
    config["annotation_validation"]["validation_pattern"] = pattern
    
    # Save updated config
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        console.print(f"✅ Set validation pattern to: [bold green]{pattern}[/]")
        console.print(f"\n💡 Cluster administrators can check compliance with:")
        console.print(f"  biotope config show-validation-pattern")
        
    except yaml.YAMLError as e:
        click.echo(f"❌ Error writing configuration: {e}")
        raise click.Abort


@config.command()
@click.option(
    "--field",
    "-f",
    required=True,
    help="Field name to remove from required fields",
)
def remove_validation(field: str) -> None:
    """Remove a field from annotation validation requirements."""
    console = Console()
    
    # Find biotope project root
    biotope_root = _find_biotope_root()
    if not biotope_root:
        click.echo("❌ Not in a biotope project. Run 'biotope init' first.")
        raise click.Abort
    
    config_path = biotope_root / ".biotope" / "config" / "biotope.yaml"
    if not config_path.exists():
        click.echo("❌ Biotope configuration not found. Run 'biotope init' first.")
        raise click.Abort
    
    # Load current config
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        click.echo(f"❌ Error reading configuration: {e}")
        raise click.Abort
    
    # Remove field from required fields
    if "annotation_validation" in config:
        if field in config["annotation_validation"].get("minimum_required_fields", []):
            config["annotation_validation"]["minimum_required_fields"].remove(field)
            console.print(f"✅ Removed '{field}' from required fields")
        else:
            console.print(f"⚠️  Field '{field}' is not in required fields")
        
        # Remove field validation rules
        if "field_validation" in config["annotation_validation"]:
            if field in config["annotation_validation"]["field_validation"]:
                del config["annotation_validation"]["field_validation"][field]
                console.print(f"✅ Removed validation rules for '{field}'")
    
    # Save updated config
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        console.print("✅ Configuration updated successfully")
    except yaml.YAMLError as e:
        click.echo(f"❌ Error writing configuration: {e}")
        raise click.Abort


@config.command()
@click.option(
    "--enabled/--disabled",
    default=True,
    help="Enable or disable annotation validation",
)
def toggle_validation(enabled: bool) -> None:
    """Enable or disable annotation validation."""
    console = Console()
    
    # Find biotope project root
    biotope_root = _find_biotope_root()
    if not biotope_root:
        click.echo("❌ Not in a biotope project. Run 'biotope init' first.")
        raise click.Abort
    
    config_path = biotope_root / ".biotope" / "config" / "biotope.yaml"
    if not config_path.exists():
        click.echo("❌ Biotope configuration not found. Run 'biotope init' first.")
        raise click.Abort
    
    # Load current config
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        click.echo(f"❌ Error reading configuration: {e}")
        raise click.Abort
    
    # Initialize annotation_validation if it doesn't exist
    if "annotation_validation" not in config:
        config["annotation_validation"] = {}
    
    config["annotation_validation"]["enabled"] = enabled
    
    # Save updated config
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        status = "enabled" if enabled else "disabled"
        console.print(f"✅ Annotation validation {status}")
    except yaml.YAMLError as e:
        click.echo(f"❌ Error writing configuration: {e}")
        raise click.Abort


@config.command()
@click.option(
    "--url",
    "-u",
    required=True,
    help="URL to remote validation configuration",
)
@click.option(
    "--cache-duration",
    type=int,
    default=3600,
    help="Cache duration in seconds (default: 3600)",
)
@click.option(
    "--fallback-to-local/--no-fallback",
    default=True,
    help="Fall back to local config if remote fails (default: true)",
)
def set_remote_validation(url: str, cache_duration: int, fallback_to_local: bool) -> None:
    """Set remote validation configuration URL."""
    console = Console()
    
    # Find biotope project root
    biotope_root = _find_biotope_root()
    if not biotope_root:
        click.echo("❌ Not in a biotope project. Run 'biotope init' first.")
        raise click.Abort
    
    config_path = biotope_root / ".biotope" / "config" / "biotope.yaml"
    if not config_path.exists():
        click.echo("❌ Biotope configuration not found. Run 'biotope init' first.")
        raise click.Abort
    
    # Load current config
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        click.echo(f"❌ Error reading configuration: {e}")
        raise click.Abort
    
    # Initialize annotation_validation if it doesn't exist
    if "annotation_validation" not in config:
        config["annotation_validation"] = {}
    
    # Set remote configuration
    config["annotation_validation"]["remote_config"] = {
        "url": url,
        "cache_duration": cache_duration,
        "fallback_to_local": fallback_to_local
    }
    
    # Save updated config
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        console.print(f"✅ Set remote validation URL: {url}")
        console.print(f"   Cache duration: {cache_duration} seconds")
        console.print(f"   Fallback to local: {fallback_to_local}")
        
        # Test the remote configuration
        console.print("\n[bold blue]Testing remote configuration...[/]")
        try:
            from biotope.validation import _load_remote_validation_config
            remote_config = _load_remote_validation_config(
                config["annotation_validation"]["remote_config"], 
                biotope_root
            )
            if remote_config:
                console.print("✅ Remote configuration loaded successfully")
                required_fields = remote_config.get("minimum_required_fields", [])
                console.print(f"   Required fields: {', '.join(required_fields)}")
            else:
                console.print("⚠️  Remote configuration not available (using fallback)")
        except Exception as e:
            console.print(f"❌ Error testing remote configuration: {e}")
            
    except yaml.YAMLError as e:
        click.echo(f"❌ Error writing configuration: {e}")
        raise click.Abort


@config.command()
def remove_remote_validation() -> None:
    """Remove remote validation configuration."""
    console = Console()
    
    # Find biotope project root
    biotope_root = _find_biotope_root()
    if not biotope_root:
        click.echo("❌ Not in a biotope project. Run 'biotope init' first.")
        raise click.Abort
    
    config_path = biotope_root / ".biotope" / "config" / "biotope.yaml"
    if not config_path.exists():
        click.echo("❌ Biotope configuration not found. Run 'biotope init' first.")
        raise click.Abort
    
    # Load current config
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        click.echo(f"❌ Error reading configuration: {e}")
        raise click.Abort
    
    # Remove remote configuration
    if "annotation_validation" in config and "remote_config" in config["annotation_validation"]:
        del config["annotation_validation"]["remote_config"]
        console.print("✅ Removed remote validation configuration")
    else:
        console.print("⚠️  No remote validation configuration found")
    
    # Save updated config
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
    except yaml.YAMLError as e:
        click.echo(f"❌ Error writing configuration: {e}")
        raise click.Abort


@config.command()
def clear_validation_cache() -> None:
    """Clear cached remote validation configurations."""
    console = Console()
    
    # Find biotope project root
    biotope_root = _find_biotope_root()
    if not biotope_root:
        click.echo("❌ Not in a biotope project. Run 'biotope init' first.")
        raise click.Abort
    
    cache_dir = biotope_root / ".biotope" / "cache" / "validation"
    if cache_dir.exists():
        import shutil
        shutil.rmtree(cache_dir)
        console.print("✅ Cleared validation cache")
    else:
        console.print("ℹ️  No validation cache found")


@config.command()
def show_remote_validation() -> None:
    """Show remote validation configuration status."""
    console = Console()
    
    # Find biotope project root
    biotope_root = _find_biotope_root()
    if not biotope_root:
        click.echo("❌ Not in a biotope project. Run 'biotope init' first.")
        raise click.Abort
    
    # Load config
    config = load_biotope_config(biotope_root)
    validation_config = config.get("annotation_validation", {})
    remote_config = validation_config.get("remote_config", {})
    
    if remote_config:
        console.print(f"\n[bold blue]Remote Validation Configuration[/]")
        console.print(f"URL: {remote_config.get('url', 'N/A')}")
        console.print(f"Cache Duration: {remote_config.get('cache_duration', 3600)} seconds")
        console.print(f"Fallback to Local: {remote_config.get('fallback_to_local', True)}")
        
        # Check cache status
        from biotope.validation import _get_cache_file_path
        cache_file = _get_cache_file_path(remote_config["url"], biotope_root)
        if cache_file.exists():
            cache_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
            console.print(f"Cache Status: ✅ Cached ({cache_age.total_seconds():.0f}s ago)")
        else:
            console.print("Cache Status: ❌ Not cached")
        
        # Show merged configuration
        console.print(f"\n[bold green]Effective Configuration (Remote + Local)[/]")
        required_fields = validation_config.get("minimum_required_fields", [])
        if required_fields:
            console.print(f"Required Fields: {', '.join(required_fields)}")
        else:
            console.print("Required Fields: None configured")
    else:
        console.print(f"\n[bold yellow]No remote validation configuration[/]")
        console.print("Use 'biotope config set-remote-validation --url <url>' to add one")


def _find_biotope_root() -> Optional[Path]:
    """Find the biotope project root directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / ".biotope").exists():
            return current
        current = current.parent
    return None 