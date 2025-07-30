import asyncio
from collections.abc import Callable
from contextlib import AsyncExitStack
from typing import Any
from tqdm import tqdm
from PIL import Image, UnidentifiedImageError
import pyheif
from pillow_heif import register_heif_opener
from io import BytesIO
import filetype
from ..flow import FlowComponent
from ...exceptions import (
    ConfigError,
    ComponentError,
    FileError
)
# Parrot Image Processing plug-ins
from parrot.interfaces.images.plugins import PLUGINS, ImagePlugin

register_heif_opener()  # HEIF support

class ImageFeatures(FlowComponent):
    """
    ImageFeatures is a component for extracting image features.
    It extends the FlowComponent class and implements a Plugin system for various image processing tasks.

    Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Attributes:
        _model_name (str): The name of the model used for feature extraction.
    """
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self._plugins_list: list = kwargs.get("plugins")
        self._plugins: list = []
        self._semaphore = asyncio.Semaphore(8)   # limit GPU tasks
        if not self._plugins_list:
            raise ConfigError("Plugins list is required.")
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """
        start.

            Initialize Task.
        """
        if self.previous:
            self.data = self.input
        if self.data_column not in self.data.columns:
            raise ValueError(
                f'Data column {self.data_column} not found in data.'
            )
        # Check plugin Names:
        plugins = []
        for n in self._plugins_list:
            # n is a dictionary with the plugin name and args
            if isinstance(n, dict):
                name = list(n.keys())[0].lower()
                args = n[name]
            plugin = PLUGINS.get(name)
            if not plugin:
                raise ConfigError(
                    f'Plugin {n} not found in available plugins.'
                )
            if not issubclass(plugin, ImagePlugin):
                raise ConfigError(
                    f'Plugin {n} is not a subclass of ImagePlugin.'
                )
            if not args:
                args = {}
            if not isinstance(args, dict):
                raise ConfigError(
                    f'Plugin {n} args must be a dictionary.'
                )
            plugins.append(
                {
                    "plugin": plugin,
                    "args": args
                }
            )
        self._plugins = plugins

    async def close(self):
        pass

    def get_bio(self, bio: Any) -> BytesIO:
        """Return a BytesIO object for a payload."""
        if isinstance(bio, Image.Image):
            return bio
        if isinstance(bio, bytes):
            bio = BytesIO(bio)
        if isinstance(bio, str):
            bio = BytesIO(bio.encode('utf-8'))
        if isinstance(bio, BytesIO):
            return bio
        if hasattr(bio, "read"):
            bio = BytesIO(bio.read())
        if hasattr(bio, "getvalue"):
            bio = BytesIO(bio.getvalue())
        else:
            raise TypeError(
                f"Expected bytes, str, or BytesIO, got {type(bio)}"
            )
        if not bio.readable():
            raise TypeError("BytesIO is not readable.")
        bio.seek(0)
        return bio

    async def _run_plugin(self, plugin, img: Image.Image, heif: Any = None, **kwargs):
        """
        Call plugin.analyze(); transparently await if it's an async def.
        """
        if asyncio.iscoroutinefunction(plugin.analyze):
            return await plugin.analyze(img, heif=heif, **kwargs)
        return plugin.analyze(img, heif)

    async def run(self):
        """
        run.

            Execute the plugin List to extract image features.
        """
        # Iterate over all plugins (create one single instance of each plugin):
        _plugins = []
        async with AsyncExitStack() as stack:
            for spec in self._plugins:
                cls, args = spec["plugin"], spec["args"]
                if cls.column_name not in self.data.columns:
                    # Create a new column in the DataFrame for the plugin's results
                    self.data[cls.column_name] = None
                plugin = cls(**args)
                try:
                    await plugin.start()
                except Exception as e:
                    raise ComponentError(
                        f"Error starting plugin {plugin}: {str(e)}"
                    ) from e
                # If the plugin implements .open() returning an async‑context
                if hasattr(plugin, "open"):
                    plugin = await stack.enter_async_context(plugin)  # ⇦ one‑time open
                _plugins.append(plugin)

        # Iterate over all rows in the DataFrame:
        # - Convert the image to a PIL Image
        # - Call the plugin's analyze method
        # - Store the result in the DataFrame
        # - Use a semaphore to limit concurrent tasks
        # - Use asyncio.gather to run the tasks concurrently
        # - Use a memoryview to avoid copying the image data
        # Convert BytesIO → bytes/PIL *one* time per row.
        async def process_row(idx, row):
            bio = row[self.data_column]
            if not bio:
                return
            async with self._semaphore:
                try:
                    try:
                        bio = self.get_bio(bio)
                    except Exception as e:
                        self._logger.error(
                            f"Error getting BytesIO from {bio}: {e}"
                        )
                        return
                    kind = filetype.guess(bio)
                    heic = None
                    if kind == 'image/heic':
                        try:
                            heic = pyheif.read_heif(bio)
                        except Exception as e:
                            self._logger.error(
                                "Unable to parse Apple Heic Photo"
                            )
                            return
                    if isinstance(bio, Image.Image):
                        image = bio
                    elif kind == 'image/heic':
                        image = Image.frombytes(
                            mode=heic.mode,
                            size=heic.size,
                            data=heic.data
                        )
                    else:
                        # Decode the image once
                        try:
                            image = Image.open(bio)
                        except UnidentifiedImageError:
                            raise FileError(
                                f"PIL cannot identify image file. MIME: {kind.mime}"
                            )
                    # Results from all plugins for this row
                    for plugin in _plugins:
                        result = await self._run_plugin(plugin, image, heic)
                        self.data.at[idx, plugin.column_name] = result
                except FileError as e:
                    self._logger.error(
                        f"Image Error on {row}: {e}"
                    )
                    return
                except Exception as e:
                    self._logger.error(
                        f'Error processing image at index {idx}: {e}'
                    )
                    return
        # Kick off tasks – DataFrame scanned exactly once
        tasks = []
        for idx, row in self.data.iterrows():
            tasks.append(process_row(idx, row))
        try:
            _ = await self._processing_tasks(tasks, ': ImageFeatures :', show_progress=True)
            self._print_data_(self.data, ':: Image Features ::')
            self._result = self.data
            return self._result
        except Exception as e:
            raise ComponentError(
                f"Error in ImageFeatures run: {str(e)}"
            ) from e
        finally:
            # Dispose of all plugins
            for plugin in _plugins:
                if hasattr(plugin, "dispose"):
                    try:
                        await plugin.dispose()
                    except Exception as e:
                        self._logger.error(
                            f"Error disposing plugin {plugin}: {str(e)}"
                        )
