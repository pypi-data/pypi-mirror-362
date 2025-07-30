import click
import redis
import os
from dotenv import load_dotenv  # added import

@click.group()
@click.option('--env', default='.env', help='Specify the environment file to load')
def cli(env):
    load_dotenv(env)  # load environment from specified .env file

redis_client = redis.Redis(
    host=os.environ.get('UPSTASH_HOST', 'localhost'),
    port=int(os.environ.get('UPSTASH_PORT', 6379)),
    password=os.environ.get('UPSTASH_PASSWORD'),
    decode_responses=True,
    ssl=True  # added for Upstash connection
)


@cli.command()
def list_keys():
    """List all Redis keys."""
    keys = redis_client.keys('*')
    for key in keys:
        click.echo(key)


@cli.command()
@click.argument('context_name')
@click.argument('keys', nargs=-1)
@click.option('--prefix', default="", help="Optional prefix for CSV content")
@click.option('--suffix', default="", help="Optional suffix for CSV content")
def create_context(context_name, keys, prefix, suffix):
    """Create a context scenario with CSV content using optional prefix/suffix."""
    context_key = f"context:{context_name}"
    if prefix or suffix:
        if prefix and suffix:
            keys_csv = f"{prefix} {','.join(keys)} {suffix}"
        elif prefix:
            keys_csv = f"{prefix} {','.join(keys)}"
        else:
            keys_csv = f"{','.join(keys)} {suffix}"
    else:
        keys_csv = ",".join(keys)
    redis_client.set(context_key, keys_csv)
    click.echo(f"Context '{context_key}' created with keys:{keys_csv}")


@cli.command()
@click.argument('pattern')
def search_keys(pattern):
    """Search and filter Redis keys based on a pattern."""
    keys = redis_client.keys(pattern)
    for key in keys:
        click.echo(key)


@cli.command()
@click.argument('key')
def delete_key(key):
    """Delete a specific Redis key."""
    redis_client.delete(key)
    click.echo(f"Key '{key}' deleted.")


@cli.command()
@click.argument('key')
def view_key_details(key):
    """View the details and value of a specific Redis key."""
    value = redis_client.get(key)
    click.echo(f"Key: {key}\nValue: {value}")


@cli.command()
@click.argument('file_path')
def export_contexts(file_path):
    """Export context scenarios to a file."""
    import json
    contexts = {}
    keys = redis_client.keys('context:*')
    for key in keys:
        contexts[key] = list(redis_client.smembers(key))
    try:
        with open(file_path, 'w') as file:
            json.dump(contexts, file, indent=2)
        click.echo(f"Contexts exported to {file_path}")
    except Exception as e:
        click.echo(f"Error exporting contexts: {e}")


@cli.command()
@click.argument('file_path')
def import_contexts(file_path):
    """Import context scenarios from a file."""
    try:
        import json
        with open(file_path, 'r') as file:
            contexts = json.load(file)
        for key, members in contexts.items():
            redis_client.sadd(key, *members)
        click.echo(f"Contexts imported from {file_path}")
    except json.JSONDecodeError as e:
        click.echo(f"Error: Invalid JSON format - {e}")
    except Exception as e:
        click.echo(f"Error importing contexts: {e}")


@cli.command()
def interactive_mode():
    """Interactive mode for navigating through options and performing actions."""
    while True:
        click.echo("\nOptions:")
        click.echo("1. List keys")
        click.echo("2. Create context")
        click.echo("3. Search keys")
        click.echo("4. Delete key")
        click.echo("5. View key details")
        click.echo("6. Export contexts")
        click.echo("7. Import contexts")
        click.echo("8. Exit")
        choice = click.prompt("Choose an option", type=int)
        if choice == 1:
            list_keys()
        elif choice == 2:
            context_name = click.prompt("Enter context name")
            keys = click.prompt("Enter keys (comma separated)").split(',')
            create_context(context_name, keys)
        elif choice == 3:
            pattern = click.prompt("Enter pattern")
            search_keys(pattern)
        elif choice == 4:
            key = click.prompt("Enter key to delete")
            delete_key(key)
        elif choice == 5:
            key = click.prompt("Enter key to view details")
            view_key_details(key)
        elif choice == 6:
            file_path = click.prompt("Enter file path to export contexts")
            export_contexts(file_path)
        elif choice == 7:
            file_path = click.prompt("Enter file path to import contexts")
            import_contexts(file_path)
        elif choice == 8:
            break
        else:
            click.echo("Invalid option. Please try again.")


@cli.command()
@click.argument('context_name')
@click.argument('new_name')
def rename_context(context_name, new_name):
    """Rename an existing context scenario."""
    context_key = f"context:{context_name}"
    new_context_key = f"context:{new_name}"
    members = redis_client.smembers(context_key)
    redis_client.sadd(new_context_key, *members)
    redis_client.delete(context_key)
    click.echo(f"Context '{context_name}' renamed to '{new_name}'")


@cli.command()
@click.argument('context_name')
@click.argument('keys', nargs=-1)
def update_context(context_name, keys):
    """Update an existing context scenario with new keys."""
    context_key = f"context:{context_name}"
    redis_client.sadd(context_key, *keys)
    click.echo(f"Context '{context_name}' updated with keys: {', '.join(keys)}")


@cli.command()
@click.argument('context_name')
def delete_context(context_name):
    """Delete an existing context scenario."""
    context_key = f"context:{context_name}"
    redis_client.delete(context_key)
    click.echo(f"Context '{context_name}' deleted")


if __name__ == '__main__':
    cli()
