# Cache CDN Client
A Python client library for interacting with the Cache CDN service based on CAFS, allowing efficient pushing and pulling of cached content.
## Installation
``` bash
pip install cafs-cache-cdn-client
```
## Features
- Asynchronous API for high-performance operations
- Push local directories to cache
- Pull cached content to local directories
- Check existence of cached references
- Tag references for easier access
- Attach additional files to existing references
- Delete references when no longer needed

## Usage Example
```python
import asyncio
import logging
from pathlib import Path
from cafs_cache_cdn_client import CacheCdnClient, CompressionT

# Configure logging to see detailed operation information
logging.basicConfig(level=logging.DEBUG)


async def main():
    # Initialize the client with the server URL
    # The connection_per_cafs_server parameter controls concurrency
    client = CacheCdnClient(
        'http://cache-server.example.com:8300',
        connection_per_cafs_server=10,
        verbose_debug=True,
    )

    # Use as an async context manager to ensure proper resource cleanup
    async with client:
        # Push a local directory to cache with a 2-hour TTL and preferred ZSTD compression
        await client.push('project_name', 'build_artifacts',
                          '/path/to/build/output', ttl_hours=2,
                          comment='Build artifacts from CI run #123',
                          compression=CompressionT.ZSTD)

        # Check if a reference exists
        exists = await client.check('project_name', 'build_artifacts')
        print(f"Reference exists: {exists}")

        # Pull cached content to a local directory
        await client.pull('project_name', 'build_artifacts',
                          '/path/to/destination')

        # Tag a reference for easier access later
        await client.tag('project_name', 'build_artifacts', 'latest_stable')

        # Attach an additional file to an existing reference
        await client.attach('project_name', 'build_artifacts',
                            Path('/path/to/metadata.json'))

        # Delete a reference when no longer needed
        await client.delete('project_name', 'old_artifacts')


# Run the example
if __name__ == '__main__':
    asyncio.run(main())
```

## API Reference
### `CacheCdnClient`
- **Constructor**: `CacheCdnClient(server: str, connection_per_cafs_server: int = 1)`
    - `server`: URL of the cache server
    - `connection_per_cafs_server`: Number of concurrent connections per CAFS server
    - `logger`: Optional logger for custom logging
    - `verbose_debug`: Enable verbose debug logging (default: `False`)

- **Methods**:
    - `push(repo: str, ref: str, directory: Path | str, ttl_hours: int = 0, comment: str | None = None, compression: CompressionT = CompressionT.NONE)` - Push a local directory to cache
    - `pull(repo: str, ref: str, directory: Path | str)` - Pull cached content to a local directory
    - `check(repo: str, ref: str) -> bool` - Check if a reference exists
    - `tag(repo: str, ref: str, tag: str)` - Create a tag for a reference
    - `attach(repo: str, ref: str, file_path: Path)` - Attach a file to an existing reference
    - `delete(repo: str, ref: str)` - Delete a reference
