# CAFS Client

CAFS Client is a Python library that provides an asynchronous interface for interacting with CAFS servers.

More information about CAFS protocol can be found in the
[G-CVSNT](https://github.com/GaijinEntertainment/G-CVSNT/tree/master/cvsnt/cvsnt-2.5.05.3744/keyValueServer) repository.

## Usage Example

Below is a complete example demonstrating all major functionality of the CAFSClient:

```python
import asyncio
import logging
from pathlib import Path
from cafs_cache_cdn_client.cafs import CAFSClient, CompressionT


# Configure logging to see detailed operation information
logging.basicConfig(level=logging.DEBUG)

async def cafs_client_demo():
    
    client = CAFSClient(
        server_root='/data',
        servers=['localhost', 'example.com:2403'],
        connection_per_server=2,
        connect_timeout=5.0,
        verbose_debug=True,  # Enable verbose debug logging
    )
    
    async with client:
        # 1. Upload a file (stream operation)
        source_file = Path('./sample.txt')
        blob_hash = await client.stream(
            path=source_file,
            compression=CompressionT.ZSTD,
        )
        print(f'File uploaded with hash: {blob_hash}')
        
        # 2. Check if the file exists on the server
        exists = await client.check(blob_hash)
        print(f'File exists: {exists}')
        
        # 3. Get the file size
        size = await client.size(blob_hash)
        print(f'File size: {size} bytes')
        
        # 4. Download the file (pull operation)
        download_path = Path('./downloaded_sample.txt')
        await client.pull(blob_hash, download_path)

if __name__ == '__main__':
    asyncio.run(cafs_client_demo())
```

## Retry Mechanism

The CAFSClient implements a robust retry mechanism. This feature ensures that operations attempt to complete even if some servers or connections are unavailable:

- When `retry=True` is specified (default for most operations), the client will automatically retry the operation across all available connections in the pool.
- The client will iterate through all available connections until either:
  1. The operation succeeds
  2. All connections in the pool have been exhausted without success

This behavior makes the client resilient to temporary network issues or server unavailability when multiple servers are configured. For critical operations, always use the default `retry=True` setting to maximize the chances of operation success in distributed environments.

If a specific operation needs to fail immediately without attempting other connections, you can disable this behavior by setting `retry=False` when calling methods like `pull()`, `check()`, `size()`, and `stream()` of the client.
