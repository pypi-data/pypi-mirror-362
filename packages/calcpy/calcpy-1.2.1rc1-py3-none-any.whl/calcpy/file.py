import hashlib


def get_hash(path, *, method="sha256", batchsize=4096):
    """Get the hash value of a file.

    Parameters:
        path (str): Path of the file.
        method (str): Hash method. Default is "sha256".
        batchsize (int): Size of each read chunk. Default is 4096 bytes.

    Returns:
        str:

    Example:
        >>> from tempfile import NamedTemporaryFile
        >>> with NamedTemporaryFile(delete=False) as tfile: # Create a temporary file
        ...     tfile.write(b'Hello world!')
        ...     filepath = tfile.file.name
        12
        >>> get_hash(filepath, method="sha256")
        'c0535e4be2b79ffd93291305436bf889314e4a3faec05ecffcbb7df31ad9e51a'
    """
    hasher = getattr(hashlib, method)()
    with open(path, "rb") as f:
        def fun():
            return f.read(batchsize)
        for chunk in iter(fun, b""):
            hasher.update(chunk)
    result = hasher.hexdigest()
    return result
