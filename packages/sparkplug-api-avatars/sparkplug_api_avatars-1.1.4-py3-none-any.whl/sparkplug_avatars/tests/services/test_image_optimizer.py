import os
import tempfile
from pathlib import Path

from PIL import Image

from sparkplug_avatars.services.image_optimizer import ImageOptimizer


def create_temp_image(
    size=(2048, 1536), mode="RGB", color=(255, 0, 0), fmt="PNG"
) -> str:
    """Create a temp image file and return its path."""
    fd, path = tempfile.mkstemp(suffix=f".{fmt.lower()}")
    os.close(fd)
    img = Image.new(mode, size, color)
    img.save(path, format=fmt)
    return path


def test_optimize_resizes_and_crops():
    # Image larger than max, should resize and crop
    src_path = create_temp_image(size=(3000, 2000), fmt="PNG")
    optimizer = ImageOptimizer(
        src_path, "testimg", max_long=1920, max_short=1080
    )
    out_path, optimized = optimizer.optimize()

    assert optimized is True
    assert Path(out_path).exists()
    with Image.open(out_path) as img:
        assert img.format == "JPEG"
        # Should match target aspect ratio
        assert abs((img.width / img.height) - (1920 / 1080)) < 0.01
        assert img.width <= 1920
        assert img.height <= 1080

    Path(src_path).unlink()
    Path(out_path).unlink()


def test_optimize_skips_small_image():
    # Image smaller than max, should not optimize
    src_path = create_temp_image(size=(800, 600), fmt="PNG")
    optimizer = ImageOptimizer(
        src_path, "smallimg", max_long=1920, max_short=1080
    )
    out_path, optimized = optimizer.optimize()

    assert optimized is False
    assert Path(out_path).exists()
    with Image.open(out_path) as img:
        # Should still be JPEG (conversion always happens)
        assert img.format == "JPEG"
        assert img.width == 800
        assert img.height == 600

    Path(src_path).unlink()
    Path(out_path).unlink()


def test_optimize_converts_to_jpeg():
    # Image in PNG, should convert to JPEG
    src_path = create_temp_image(size=(1000, 1000), fmt="PNG")
    optimizer = ImageOptimizer(
        src_path, "convertimg", max_long=1920, max_short=1080
    )
    out_path, optimized = optimizer.optimize()

    assert Path(out_path).exists()
    with Image.open(out_path) as img:
        assert img.format == "JPEG"

    Path(src_path).unlink()
    Path(out_path).unlink()


def test_optimize_handles_portrait_orientation():
    # Portrait image, should resize and crop correctly
    src_path = create_temp_image(size=(1000, 2000), fmt="PNG")
    optimizer = ImageOptimizer(
        src_path, "portraitimg", max_long=1920, max_short=1080
    )
    out_path, optimized = optimizer.optimize()

    assert optimized is True
    with Image.open(out_path) as img:
        assert img.format == "JPEG"
        # Should match target aspect ratio
        assert abs((img.width / img.height) - (1920 / 1080)) < 0.01

    Path(src_path).unlink()
    Path(out_path).unlink()


def test_optimize_no_crop_needed():
    # Image already at target aspect ratio, no crop
    src_path = create_temp_image(size=(1920, 1080), fmt="PNG")
    optimizer = ImageOptimizer(
        src_path, "nocropimg", max_long=1920, max_short=1080
    )
    out_path, optimized = optimizer.optimize()

    assert optimized is False
    with Image.open(out_path) as img:
        assert img.width == 1920
        assert img.height == 1080

    Path(src_path).unlink()
    Path(out_path).unlink()


def test_optimize_handles_non_rgb():
    # Grayscale image should be converted to RGB/JPEG
    fd, src_path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    img = Image.new("L", (1200, 900), 128)
    img.save(src_path, format="PNG")
    optimizer = ImageOptimizer(
        src_path, "grayimg", max_long=1920, max_short=1080
    )
    out_path, optimized = optimizer.optimize()

    with Image.open(out_path) as out_img:
        assert out_img.mode == "RGB"
        assert out_img.format == "JPEG"

    Path(src_path).unlink()
    Path(out_path).unlink()
