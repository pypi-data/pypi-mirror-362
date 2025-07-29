from typing import TYPE_CHECKING, List, Literal, Optional, Tuple, Union
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import math
import urllib.parse
import re
import asyncio

if TYPE_CHECKING:
    from . import LastFMClient

OutputMode = Literal["image", "file", "bytes"]
ImageType = Literal["albums", "artists", "tracks"]
ImageFormat = Literal["JPEG", "PNG"]
TimePeriod = Literal["overall", "7day", "1month", "3month", "6month", "12month"]

class OutputStyle:
    def __init__(self, output_mode: OutputMode = "image", image_format: ImageFormat = "JPEG", background_color: str = "black"):
        self.output_mode = output_mode
        self.image_format = image_format
        self.background_color = background_color

class CollageLayout:
    def __init__(self, draw_labels: bool = True, spacing: int = 6, font_size: int = 18):
        self.draw_labels = draw_labels
        self.spacing = spacing
        self.font_size = font_size


class ChartBuilder:
    def __init__(self, *, client: "LastFMClient", style: OutputStyle = OutputStyle(), layout: CollageLayout = CollageLayout()):
        self.client = client
        self.style = style
        self.layout = layout

    async def _search_image_url(self, query: str) -> Optional[str]:
        try:
            url = f"https://search.brave.com/images?q={urllib.parse.quote(query)}"
            headers = {"User-Agent": "Mozilla/5.0"}
            async with self.client.session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    return None
                html = await resp.text()
                matches = re.findall(r'https://[^"]+\.(?:jpg|jpeg|png)', html)
                return matches[0] if matches else None
        except Exception:
            return None

    async def _fetch_image(self, url: str, fallback_query: Optional[str] = None) -> Optional[Image.Image]:
        if url:
            try:
                async with self.client.session.get(url) as resp:
                    if resp.status == 200:
                        return Image.open(BytesIO(await resp.read())).convert("RGB")
            except Exception:
                pass
        if fallback_query:
            fallback_url = await self._search_image_url(fallback_query)
            if fallback_url:
                try:
                    async with self.client.session.get(fallback_url) as resp:
                        if resp.status == 200:
                            return Image.open(BytesIO(await resp.read())).convert("RGB")
                except Exception:
                    pass
        return None

    async def _get_image_data(self, type: ImageType, username: str, limit: int, period: TimePeriod) -> List[Tuple[str, str]]:
        items = []
        if type == "albums":
            data = await self.client.user.get_top_albums(user=username, limit=limit, period=period)
            for album in data:
                label = f"{album.name} — {album.artist}"
                images = album.raw.get("image", [])
                url = next((img["#text"] for img in reversed(images) if img["#text"]), "")
                items.append((url, label))

        elif type == "artists":
            data = await self.client.user.get_top_artists(user=username, limit=limit, period=period)
            for artist in data:
                label = artist.name
                images = artist.raw.get("image", [])
                url = next((img["#text"] for img in reversed(images) if img["#text"]), "")
                items.append((url, label))

        elif type == "tracks":
            data = await self.client.user.get_top_tracks(user=username, limit=limit, period=period)
            for track in data:
                label = f"{track.name} — {track.artist}"
                images = track.raw.get("image", [])
                url = next((img["#text"] for img in reversed(images) if img["#text"]), "")
                items.append((url, label))

        return items

    def _fit_grid(self, count: int) -> Tuple[int, int]:
        cols = math.ceil(math.sqrt(count))
        rows = math.ceil(count / cols)
        return rows, cols

    def _draw_label(self, img: Image.Image, label: str, font: ImageFont.ImageFont) -> Image.Image:
        draw = ImageDraw.Draw(img)
        text_width, text_height = draw.textsize(label, font=font)
        padding = 4
        y_position = img.height - text_height - padding
        draw.rectangle([0, y_position - 2, img.width, img.height], fill=(0, 0, 0, 180))
        draw.text((img.width / 2, y_position), label, fill="white", font=font, anchor="mm")
        return img

    async def build_collage(
        self,
        username: str,
        type: ImageType = "albums",
        period: TimePeriod = "overall",
        limit: int = 25,
        image_size: int = 300,
        output_path: Optional[str] = None
    ) -> Union[Image.Image, bytes, None]:

        items = await self._get_image_data(type, username, limit, period)
        count = len(items)
        rows, cols = self._fit_grid(count)
        spacing = self.layout.spacing

        collage_width = cols * image_size + (cols - 1) * spacing
        collage_height = rows * image_size + (rows - 1) * spacing
        collage = Image.new("RGB", (collage_width, collage_height), self.style.background_color)

        try:
            font = ImageFont.truetype("arial.ttf", self.layout.font_size)
        except:
            font = ImageFont.load_default()

        tasks = []
        for url, label in items:
            tasks.append(self._fetch_image(url, fallback_query=label))

        images = await asyncio.gather(*tasks)
        images = [img.resize((image_size, image_size)) if img else None for img in images]

        for idx, (img, (_, label)) in enumerate(zip(images, items)):
            if img is None:
                continue

            if self.layout.draw_labels:
                img = self._draw_label(img, label[:40], font)

            row = idx // cols
            col = idx % cols
            x = col * (image_size + spacing)
            y = row * (image_size + spacing)
            collage.paste(img, (x, y))

        if self.style.output_mode == "file":
            if not output_path:
                raise ValueError("output_path is required for file output.")
            collage.save(output_path, format=self.style.image_format)
            return None

        elif self.style.output_mode == "bytes":
            buffer = BytesIO()
            collage.save(buffer, format=self.style.image_format)
            buffer.seek(0)
            return buffer.read()

        return collage
