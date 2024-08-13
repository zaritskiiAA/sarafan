import os
import re
import glob

from PIL import Image
from django.conf import settings


class ResizeImg:
    """
    Класс для изменения размера изображения.
    """

    def __init__(self, source_image) -> None:

        self.source_image = source_image

    def resize(self, size: tuple[int], save_file: str) -> None:

        new_w, new_h = size
        img = Image.open(self.source_image.path)
        img_resized = img.resize((new_w, new_h))
        img_resized.save(save_file)

    @staticmethod
    def clear(pattern: str) -> None:

        """Очищает директорию media от неиспользуемых изображений."""

        path = os.path.join(settings.MEDIA_ROOT, pattern)
        img_objs = glob.glob(path.replace('.', '*.'), recursive=True)

        for obj in img_objs:

            name, format = os.path.splitext(os.path.basename(pattern))
            regex = re.compile(f'^{name}(?:_mid|_small)?\{format}$') # noqa W605
            obj_name = os.path.basename(obj)
            if os.path.isfile(obj) and regex.match(obj_name):
                os.remove(obj)
