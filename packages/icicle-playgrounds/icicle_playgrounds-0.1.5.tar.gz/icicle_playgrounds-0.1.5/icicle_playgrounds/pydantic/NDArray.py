import base64
import io
import gzip
import numpy as np
from pydantic import BaseModel, ConfigDict
from torch._numpy import _dtypes

class PipelineIO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    _ndims: int = None  # Change from PrivateAttr to class variable
    _dtypes: set[np.dtype] = None  # Change from PrivateAttr to class variable
    _dict_keys: set[frozenset[str]] = None  # Change from PrivateAttr to class variable

    @classmethod
    def _ndarray_to_base64(cls, array: np.ndarray, compress: bool = False) -> str:
        """
        Encode a numpy array to a base64 string.

        Args:
            array: The numpy array to encode
            compress: Whether to use gzip compression (default: False)

        Returns:
            A base64 encoded string representation of the array
        """
        try:
            buffer = io.BytesIO()
            tag = "base64"
            if compress:
                with gzip.GzipFile(fileobj=buffer, mode="wb") as f:
                    np.save(f, array)
                tag += "-compressed"
            else:
                np.save(buffer, array)
            return tag + ":" + base64.b64encode(buffer.getvalue()).decode("utf-8")
        except Exception as e:
            raise e

    @classmethod
    def _base64_to_ndarray(
        cls, encoded_str: str, compressed: bool = False
    ) -> np.ndarray:
        """
        Decode a base64 string back to a numpy array.

        Args:
            encoded_str: The base64 encoded string
            compressed: Whether the string was compressed with gzip (default: False)

        Returns:
            The decoded numpy array
        """
        try:
            tag, encoded_str = encoded_str.split(":", 1)
            if tag == "base64-compressed":
                compressed = True
            decoded = base64.b64decode(encoded_str)
            buffer = io.BytesIO(decoded)
            if compressed:
                with gzip.GzipFile(fileobj=buffer, mode="rb") as f:
                    arr = np.load(f)
            else:
                arr = np.load(buffer)
            return arr
        except Exception as e:
            raise e

    @classmethod
    def _validate_ndarray(cls, array: np.array) -> None:
        if array.ndim != cls._ndims:
            raise ValueError(
                f"Input array must be {cls._ndims} dimensional, got {array.ndim}"
            )
        if array.dtype not in _dtypes:
            raise ValueError(
                f"Input array must be one of the following dtypes: {_dtypes}"
            )