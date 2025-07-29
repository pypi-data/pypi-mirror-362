import logging
import os
import tempfile

from PIL import Image

log = logging.getLogger(__name__)


class ImageOptimizer:
    def __init__(
        self,
        source: str,
        filename: str,
        max_long: int = 1920,
        max_short: int = 1080,
    ) -> None:
        self.source = source
        self.filename = filename
        self.max_long = max_long
        self.max_short = max_short
        # Use a secure temporary path for the output file
        fd, self.filepath = tempfile.mkstemp(
            suffix=".jpg", prefix=f"{filename}_"
        )
        os.close(fd)
        self.optimized = False

    def optimize(self) -> tuple[str, bool]:
        with Image.open(self.source) as source_img:
            self.img = source_img
            self.image_width, self.image_height = self.img.size

            log.debug(
                "image width/height",
                extra={
                    "image_width": self.image_width,
                    "image_height": self.image_height,
                },
            )

            if (
                self.image_width > self.max_long
                or self.image_height > self.max_short
            ):
                self._resize_image()
                self._crop_to_aspect_ratio()
            else:
                msg = (
                    "Image is smaller than max dimensions, "
                    "skipping resizing and cropping."
                )
                log.debug(msg)

            self._convert_to_jpeg()

            if self.optimized:
                self._save_image()

            log.debug("image optimized", extra={"optimized": self.optimized})

        return self.filepath, self.optimized

    def _determine_orientation(self) -> tuple[bool, int, int]:
        """Determine image orientation and return dimensions."""
        if self.image_width < self.image_height:
            landscape = False
            side_long = self.image_height
            side_short = self.image_width
        else:
            landscape = True
            side_long = self.image_width
            side_short = self.image_height

        log.debug("landscape", extra={"landscape": landscape})
        log.debug(
            "side long/short",
            extra={
                "side_long": side_long,
                "side_short": side_short,
            },
        )
        return landscape, side_long, side_short

    def _resize_image(self) -> None:
        """Resize the image if necessary to fit within max dimensions."""
        landscape, side_long, side_short = self._determine_orientation()

        if (side_long > self.max_long) or (side_short > self.max_short):
            if side_long / self.max_long > side_short / self.max_short:
                scale_factor = self.max_long / side_long
            else:
                scale_factor = self.max_short / side_short

            target_long = int(side_long * scale_factor)
            target_short = int(side_short * scale_factor)

            log.debug(
                "target long/short after scaling",
                extra={
                    "target_long": target_long,
                    "target_short": target_short,
                },
            )

            if landscape:
                calc_width = target_long
                calc_height = target_short
            else:
                calc_width = target_short
                calc_height = target_long

            log.debug(
                "calc width/height",
                extra={
                    "calc_width": calc_width,
                    "calc_height": calc_height,
                },
            )

            self.img = self.img.resize((calc_width, calc_height))
            self.optimized = True
        else:
            log.debug(
                "Image is smaller than max dimensions, skipping resizing.",
                extra={
                    "image_width": self.image_width,
                    "image_height": self.image_height,
                    "max_long": self.max_long,
                    "max_short": self.max_short,
                },
            )

    def _crop_to_aspect_ratio(self) -> None:
        """Crop the image to match the target aspect ratio."""
        target_aspect_ratio = self.max_long / self.max_short
        current_aspect_ratio = self.img.width / self.img.height

        if current_aspect_ratio > target_aspect_ratio:
            # Image is too wide, crop horizontally
            new_width = int(self.img.height * target_aspect_ratio)
            left = (self.img.width - new_width) // 2
            right = left + new_width
            top = 0
            bottom = self.img.height
        elif current_aspect_ratio < target_aspect_ratio:
            # Image is too tall, crop vertically
            new_height = int(self.img.width / target_aspect_ratio)
            top = (self.img.height - new_height) // 2
            bottom = top + new_height
            left = 0
            right = self.img.width
        else:
            # Aspect ratio matches, no cropping needed
            return

        log.debug(
            "Cropping image",
            extra={
                "left": left,
                "top": top,
                "right": right,
                "bottom": bottom,
            },
        )
        self.img = self.img.crop((left, top, right, bottom))
        self.optimized = True

    def _convert_to_jpeg(self) -> None:
        """Convert the image to JPEG format if necessary."""
        if self.img.format != "JPEG":
            log.debug(
                "Converting image format to JPEG",
                extra={"original_format": self.img.format},
            )
            self.img = self.img.convert("RGB")
            self.optimized = True

    def _save_image(self) -> None:
        """Save the optimized image to the specified filepath."""
        self.img.save(self.filepath, quality=80, optimize=True)
        log.debug(
            "Image saved",
            extra={"filepath": self.filepath},
        )
