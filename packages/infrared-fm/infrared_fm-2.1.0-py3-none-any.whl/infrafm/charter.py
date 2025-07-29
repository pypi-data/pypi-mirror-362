from dataclasses import dataclass
from typing import List, Literal, Optional, Union, TYPE_CHECKING
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import math
import textwrap

if TYPE_CHECKING:
    from . import LastFMClient

OutputMode = Literal["image", "file", "bytes"]
ImageType = Literal["albums", "artists", "tracks"]
ImageFormat = Literal["JPEG", "PNG"]
TimePeriod = Literal["overall", "7day", "1month", "3month", "6month", "12month"]


@dataclass
class OutputStyle:
    output_mode: OutputMode = "image"
    image_format: ImageFormat = "JPEG"
    background_color: str = "black"
    label_color: str = "white"
    font_path: Optional[str] = None


@dataclass
class CollageLayout:
    draw_labels: bool = True
    spacing: int = 10
    label_wrap: int = 20
    font_size: int = 14


class ChartBuilder:
    def __init__(
        self,
        client: "LastFMClient",
        style: OutputStyle = OutputStyle(),
        layout: CollageLayout = CollageLayout()
    ):
        self.client = client
        self.style = style
        self.layout = layout

        self.font = (
            ImageFont.load_default()
            if self.style.font_path is None
            else ImageFont.truetype(self.style.font_path, size=self.layout.font_size)
        )
        self._fallback_image = Image.new("RGB", (300, 300), color="#222222")

    async def _fetch_image(self, url: str) -> Optional[Image.Image]:
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
    ) -> List[tuple[str, str]]:
        items = []

        if type == "albums":
            data = await self.client.user.get_top_albums(user=username, limit=limit, period=period)
            for album in data:
                images = album.raw.get("image", [])
                url = next((img["#text"] for img in reversed(images) if img["#text"]), "")
                items.append((url, album.name))

        elif type == "artists":
            data = await self.client.user.get_top_artists(user=username, limit=limit, period=period)
            for artist in data:
                images = artist.raw.get("image", [])
                url = next((img["#text"] for img in reversed(images) if img["#text"]), "")
                items.append((url, artist.name))

        elif type == "tracks":
            data = await self.client.user.get_top_tracks(user=username, limit=limit, period=period)
            for track in data:
                images = track.raw.get("image", [])
                url = next((img["#text"] for img in reversed(images) if img["#text"]), "")
                items.append((url, track.name))

        return items

    def _draw_label(self, draw: ImageDraw.Draw, text: str, x: int, y: int, max_width: int):
        lines = textwrap.wrap(text, width=self.layout.label_wrap)
        for i, line in enumerate(lines):
            draw.text(
                (x, y + i * self.layout.font_size),
                line,
                font=self.font,
                fill=self.style.label_color
            )

    async def build_collage(
        self,
        username: str,
        type: ImageType = "albums",
        period: TimePeriod = "overall",
        limit: int = 25,
        image_size: int = 300,
        output_path: Optional[str] = None
    ) -> Union[Image.Image, bytes, None]:
        items = await self._get_image_urls(type, username, limit, period)

        count = min(len(items), limit)
        grid = math.ceil(math.sqrt(count))
        total_slots = grid * grid
        items = items[:total_slots]

        full_image_height = image_size + (self.layout.font_size * 2 if self.layout.draw_labels else 0)

        collage = Image.new(
            "RGB",
            (
                grid * (image_size + self.layout.spacing) - self.layout.spacing,
                grid * (full_image_height + self.layout.spacing) - self.layout.spacing
            ),
            color=self.style.background_color
        )

        for idx, (url, label) in enumerate(items):
            img = await self._fetch_image(url)
            if not img:
                img = self._fallback_image

            img = img.resize((image_size, image_size))
            row = idx // grid
            col = idx % grid

            x = col * (image_size + self.layout.spacing)
            y = row * (full_image_height + self.layout.spacing)

            collage.paste(img, (x, y))

            if self.layout.draw_labels:
                draw = ImageDraw.Draw(collage)
                self._draw_label(
                    draw,
                    text=label,
                    x=x,
                    y=y + image_size + 2,
                    max_width=image_size
                )

        if self.style.output_mode == "file":
            if not output_path:
                raise ValueError("output_path is required when output_mode='file'")
            collage.save(output_path, format=self.style.image_format)
            return None

        elif self.style.output_mode == "bytes":
            buffer = BytesIO()
            collage.save(buffer, format=self.style.image_format)
            buffer.seek(0)
            return buffer.read()

        elif self.style.output_mode == "image":
            return collage

        raise ValueError(f"Invalid output_mode: {self.style.output_mode}")
