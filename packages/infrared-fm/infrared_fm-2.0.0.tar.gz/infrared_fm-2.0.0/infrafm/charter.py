from PIL import Image
from typing import List, Literal, Optional, Union, TYPE_CHECKING
from io import BytesIO
import math

if TYPE_CHECKING:
    from . import LastFMClient

OutputMode = Literal["image", "file", "bytes"]
ImageType = Literal["albums", "artists", "tracks"]
ImageFormat = Literal["JPEG", "PNG"]
TimePeriod = Literal["overall", "7day", "1month", "3month", "6month", "12month"]

class ChartBuilder:
    def __init__(
        self,
        *,
        client: "LastFMClient",
        output_mode: OutputMode = "image",
        image_format: ImageFormat = "JPEG",
        background_color: str = "black"
    ):
        """
        Builds image collages from a user's top albums, artists, or tracks.

        Args:
            client: An instance of LastFMClient.
            output_mode: What to return — a PIL Image, raw bytes, or save to file.
            image_format: Format used for bytes or file output.
            background_color: Background fill color (default: black).
        """
        self.client = client
        self.output_mode = output_mode
        self.image_format = image_format
        self.background_color = background_color

    async def _fetch_image(self, url: str) -> Optional[Image.Image]:
        if not url:
            return None
        try:
            async with self.client.session.get(url) as resp:
                if resp.status != 200:
                    return None
                data = await resp.read()
                return Image.open(BytesIO(data)).convert("RGB")
        except Exception:
            return None

    async def _get_image_urls(
        self,
        type: ImageType,
        username: str,
        limit: int,
        period: TimePeriod
    ) -> List[str]:
        urls = []

        if type == "albums":
            data = await self.client.user.get_top_albums(user=username, limit=limit, period=period)
            for album in data:
                images = album.raw.get("image", [])
                url = next((img["#text"] for img in reversed(images) if img["#text"]), "")
                urls.append(url)

        elif type == "artists":
            data = await self.client.user.get_top_artists(user=username, limit=limit, period=period)
            for artist in data:
                images = artist.raw.get("image", [])
                url = next((img["#text"] for img in reversed(images) if img["#text"]), "")
                urls.append(url)

        elif type == "tracks":
            data = await self.client.user.get_top_tracks(user=username, limit=limit, period=period)
            for track in data:
                images = track.raw.get("image", [])
                url = next((img["#text"] for img in reversed(images) if img["#text"]), "")
                urls.append(url)

        return urls

    async def build_collage(
        self,
        username: str,
        type: ImageType = "albums",
        period: TimePeriod = "overall",
        limit: int = 25,
        grid_size: Optional[int] = None,
        image_size: int = 300,
        output_path: Optional[str] = None
    ) -> Union[Image.Image, bytes, None]:
        """
        Builds and returns or saves a collage from Last.fm data.

        Args:
            username: Last.fm username to fetch data for.
            type: 'albums', 'artists', or 'tracks'.
            period: 'overall', '7day', '1month', '3month', '6month', or '12month'.
            limit: Number of items to fetch.
            grid_size: Optional grid dimension (auto if not given).
            image_size: Size of each image in pixels.
            output_path: File path (required if output_mode='file').

        Returns:
            - PIL.Image.Image if output_mode is 'image'
            - bytes if output_mode is 'bytes'
            - None if output_mode is 'file'
        """
        urls = await self._get_image_urls(type, username, limit, period)

        count = min(len(urls), limit)
        grid = grid_size or math.isqrt(count)
        total_slots = grid * grid
        urls = urls[:total_slots]

        images = []
        for url in urls:
            img = await self._fetch_image(url)
            if img:
                img = img.resize((image_size, image_size))
                images.append(img)

        collage = Image.new(
            "RGB",
            (grid * image_size, grid * image_size),
            color=self.background_color
        )

        for idx, img in enumerate(images):
            row = idx // grid
            col = idx % grid
            collage.paste(img, (col * image_size, row * image_size))

        if self.output_mode == "file":
            if not output_path:
                raise ValueError("output_path is required when output_mode='file'")
            collage.save(output_path, format=self.image_format)
            return None

        elif self.output_mode == "bytes":
            buffer = BytesIO()
            collage.save(buffer, format=self.image_format)
            buffer.seek(0)
            return buffer.read()

        elif self.output_mode == "image":
            return collage

        else:
            raise ValueError(f"Invalid output_mode: {self.output_mode}")
