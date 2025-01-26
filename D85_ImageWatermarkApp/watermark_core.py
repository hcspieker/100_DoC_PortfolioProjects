"""Contains the logic to add a watermark to an existing image file.

This contains the following classes:
- WatermarkSourceImage
- WatermarkDefinition
- WatermarkManager

"""

import errno
import os
import os.path
import textwrap

from typing import Callable

from PIL import Image, ImageFont, ImageDraw, ImageOps

class WatermarkSourceImage:
    """Represents a source image onto which the watermark will be applied
    """
    def __init__(self, file_name):
        self.source_file = file_name

    def determine_output_filename(self, out_dir) -> str:
        """generates the target filename based on the source filename and output directory

        Args:
            out_dir (str): output directory

        Returns:
            str: target filename including the output path
        """
        _, tail = os.path.split(self.source_file)
        return os.path.join(out_dir, tail)

class WatermarkDefinition:
    """Contains the configuration of a watermark (e.g. watermark text, color, font)
    """
    def __init__(
            self,
            watermark_text: str,
            text_color: str = "#ffffff",
            shadow_color: str = "#000000",
            shadow_distance: int = 3,
            font_name: str = "arial.ttf",
            start_in_center: bool = True):
        self.text_color = text_color
        self.shadow_color = shadow_color
        self.shadow_distance = shadow_distance
        self.font_name = font_name
        self.anchor = "ms"
        self.start_in_center = start_in_center
        self.text = "\n".join(
            [
                "\n".join(textwrap.wrap(line, 15, break_long_words=False))
                for line in watermark_text.splitlines()
            ])

class WatermarkManager:
    """Contains the logic to add a watermark to existing files
    """
    def __init__(
            self,
            watermark: WatermarkDefinition,
            out_dir: str):
        self._w_config = watermark
        self._out_dir = out_dir

    def convert_files(
            self,
            images: list[WatermarkSourceImage],
            notify:Callable[[str, int, int], None] = None):
        """Adds a watermark to the supplied images list and 
        notifies via the callback method after every image.

        Args:
            images (list[WatermarkSourceImage]): list of images
            notify (Callable[[str, int, int], None], optional): 
                notification callback. Defaults to None.
        """
        if not os.path.exists(self._out_dir):
            os.makedirs(self._out_dir)

        amount_of_images = len(images)

        notify(f"Adding a watermark to {amount_of_images} images")
        for i in range(amount_of_images):
            if notify:
                notify(
                    f"Adding a watermark to image {i+1} of {amount_of_images}",
                    i+1,
                    amount_of_images
                )

            self._convert_file(images[i])

        notify(
            f"Added a watermark to {amount_of_images} images",
            amount_of_images,
            amount_of_images
        )

    def _convert_file(self, file: WatermarkSourceImage):
        """Adds a watermark to the supplied file

        Args:
            file (WatermarkSourceImage): file onto which the watermark will be applied

        Raises:
            FileNotFoundError: if the file doesn't exist
        """
        if not os.path.isfile(file.source_file):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file.source_file)

        source_image = Image.open(file.source_file)
        rotated_image = ImageOps.exif_transpose(source_image)
        draw = ImageDraw.Draw(rotated_image)

        w, h = rotated_image.size
        w_font_size = h / 2 / 6
        w_font = ImageFont.truetype(self._w_config.font_name, w_font_size)
        x_pos = int(w/2)

        if self._w_config.start_in_center:
            y_pos = int(h/2)
        else:
            y_pos = w_font_size

        draw.multiline_text(
            (x_pos + self._w_config.shadow_distance, y_pos + self._w_config.shadow_distance),
            self._w_config.text,
            fill=self._w_config.shadow_color,
            font=w_font,
            anchor=self._w_config.anchor
        )

        draw.multiline_text(
            (x_pos, y_pos),
            self._w_config.text,
            fill=self._w_config.text_color,
            font=w_font,
            anchor=self._w_config.anchor
        )

        rotated_image.save(file.determine_output_filename(self._out_dir))
