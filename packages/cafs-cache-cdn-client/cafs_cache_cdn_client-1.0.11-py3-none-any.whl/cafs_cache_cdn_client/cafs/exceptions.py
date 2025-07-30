__all__ = (
    'CAFSClientError',
    'BlobNotFoundError',
    'UnexpectedResponseError',
    'EmptyConnectionPoolError',
)


class CAFSClientError(Exception):
    pass


class BlobNotFoundError(CAFSClientError):
    blob_hash: str

    def __init__(self, blob_hash: str) -> None:
        self.blob_hash = blob_hash
        super().__init__(f'Blob not found: {blob_hash}')


class UnexpectedResponseError(CAFSClientError):
    response: bytes

    def __init__(self, response: bytes) -> None:
        self.response = response
        super().__init__('Unexpected response: %s', self.response)


class EmptyConnectionPoolError(CAFSClientError):
    pass
