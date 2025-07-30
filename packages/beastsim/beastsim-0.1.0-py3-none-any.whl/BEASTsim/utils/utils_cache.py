from typing import Optional, Any, Callable
import os
import pickle
from anndata import read_h5ad,AnnData


def _store(data: Any, file_path: Optional[str]) -> None:
    """
    Stores the given data in a pickle file.

    Args:
        data (Any): The data or object to be serialized and stored.
        file_path (str): The path to the file where the data will be stored.
    """
    base_path = os.path.splitext(file_path)[0]  # Remove extension
    pickle_path = base_path + ".pkl"
    anndata_path = base_path + ".h5ad"
    if isinstance(data, AnnData):
        try:
            with open(anndata_path, 'wb') as f:
                data.write_h5ad(anndata_path)
        except Exception as e:
            raise ValueError(f"Error while storing RegressionModel model: {e}")
    else:
        try:
            with open(pickle_path, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            raise ValueError(f"Error while storing data: {e}")

def _multi_store(datas, file_path):
    dir_name, file_name = os.path.split(file_path)  # Separate path and filename
    for i, data in enumerate(datas):
        new_file_name = f"{i}{file_name}"  # Prepend number to filename
        path = os.path.join(dir_name, new_file_name)  # Reconstruct full path
        _store(data, path)

def _load(file_path: Optional[str]) -> Any:
    """
    Loads and returns data from a pickle file.

    Args:
        file_path (str): The path to the file to be loaded.

    Returns:
        Any: The data that was deserialized from the file.
    """
    base_path = os.path.splitext(file_path)[0]  # Remove extension
    pickle_path = base_path + ".pkl"
    anndata_path = base_path + ".h5ad"

    if os.path.exists(pickle_path):
        try:
            with open(pickle_path, 'rb') as f:
                data = pickle.load(f)
            return data
        except Exception as e:
            raise ValueError(f"Error while loading data from {pickle_path}: {e}")
    elif os.path.exists(anndata_path):
        try:
            with open(anndata_path, 'rb') as f:
                adata = read_h5ad(anndata_path)
            return adata
        except Exception as e:
            raise ValueError(f"Error while loading RegressionModel from {anndata_path}: {e}")
    else:
        return None


def _multi_load(file_path):
    """
    Attempts to load multiple files with numeric prefixes (0-999) added to the filename.

    Args:
        file_path (str): The base file path (without extension).

    Returns:
        tuple: A tuple containing all successfully loaded objects.
    """
    loaded_data = []
    dir_name, file_name = os.path.split(file_path)  # Separate path and filename

    for i in range(1000):
        new_file_name = f"{i}{file_name}"  # Prepend number to filename
        path = os.path.join(dir_name, new_file_name)  # Reconstruct full path

        data = _load(path)
        if data is None:
            break
        else:
            loaded_data.append(data)

    return tuple(loaded_data)

def _use_cache(func: Callable[..., Any]) -> Callable[..., Any]:
    ## TODO: improve path loading
    """
    A decorator that caches the result of a function to a file.
    The file path must be provided as a keyword argument `cache_path` during the function call.
    Optionally, a `skip_cache` flag can be used to skip cache loading and force result computation.

    Args:
        func (Callable[..., Any]): The function to be wrapped by the decorator.
                                   It can take any number of arguments and return any type of result.

    Keyword Args:
        cache_path (str, optional): The file path to store or retrieve the cached result.
                                    If not provided, caching will be skipped.
        skip_cache (bool, optional): If `True`, skips cache loading and forces result computation.
                                     Defaults to `False`.

    Returns:
        Callable[..., Any]: The wrapped function that either retrieves the cached result from a file
                            or computes and caches the result.
    """

    def _wrapper(*args: Any, **kwargs: Any) -> Any:
        # Extract the cache path and skip_cache flag
        file_path = kwargs.pop('cache_path', None)
        use_cache = kwargs.pop('use_cache', False)
        multi_cache = kwargs.pop('multi_cache', False)


        # Handle caching logic
        if use_cache and file_path is not None and os.path.exists(file_path):
            if multi_cache:
                cached_result =_multi_load(file_path)
            else:
                cached_result = _load(file_path)
            if cached_result is not None:
                return cached_result

        # Compute the result if no cache is used or available
        result = func(*args, **kwargs)

        # Store the result in the cache if a file path is provided
        if os.path.exists(file_path):
            if isinstance(result, tuple):
                _multi_store(result, file_path)
            else:
                os.path
                _store(result, file_path)

        return result

    return _wrapper


def _generate_combination_name(datasets) -> str:
    import hashlib
    sorted_names = sorted(data.name for data in datasets)
    # Combine names with a delimiter
    combined_name = "_".join(sorted_names)
    # Optional: Hash the combined name to ensure uniqueness and avoid long names
    hashed_name = hashlib.sha256(combined_name.encode()).hexdigest()[:10]  # First 10 characters of hash
    return f"datasets_{hashed_name}"