import click
from upstash_redis import Redis


def get_redis():
    """Create Redis client from environment when needed."""
    return Redis.from_env()


@click.group()
def cli():
    """UpKeys access management CLI."""
    pass


@cli.command()
def list_keys():
    """List all Redis keys."""
    redis = get_redis()
    keys = redis.keys('*')
    for key in keys:
        click.echo(key)


@cli.command()
@click.argument('context_name')
@click.argument('keys', nargs=-1)
def create_context(context_name, keys):
    """Create a context scenario with a group of keys."""
    redis = get_redis()
    context_key = f"context:{context_name}"
    redis.sadd(context_key, *keys)
    click.echo(f"Context '{context_name}' created with keys: {', '.join(keys)}")


if __name__ == '__main__':
    cli()
