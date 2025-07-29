from typing import Any, Optional
import io
import gzip
import base64
from enum import Enum, auto()
import numpy as np
import torch
from pydantic import BaseModel, ConfigDict, field_validator, field_serializer


class BoundingBoxFormat(Enum):
    XYXY = auto()
    XYWH = auto()
    XYXYN = auto()
    XYWHN = auto()


class BoundingBox(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    box: np.ndarray | torch.Tensor | None = None
    format: BoundingBoxFormat = BoundingBoxFormat.XYXY

    def to_tensor(self) -> torch.Tensor:
        if self.box is None:
            raise ValueError("Cannot convert None to tensor")
        return torch.from_numpy(self.box)

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
            if not encoded_str:
                return None
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

    @field_validator("box", mode="before")
    @classmethod
    def _validate_input_value(cls, value: Any) -> Optional[np.ndarray | torch.Tensor]:
        if value is None or (isinstance(value, str) and not value):
            return None
        if isinstance(value, np.ndarray):
            return value
        if isinstance(value, torch.Tensor):
            return value  # Return tensor as is
        if isinstance(value, str):
            return cls._base64_to_ndarray(value)
        if isinstance(value, (list, tuple)):
            try:
                return np.array(value)
            except Exception:
                raise ValueError("Error converting list/tuple to numpy array")

        raise TypeError("Invalid input type")

    @field_serializer("box")
    def _serialize_box(self, box: Optional[np.ndarray | torch.Tensor]) -> str:
        if box is None:
            return ""
        if isinstance(box, torch.Tensor):
            box = box.cpu().numpy()
        return self._ndarray_to_base64(box)