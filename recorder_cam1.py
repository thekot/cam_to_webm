import os
import datetime

import config
from modules.init_logging import init_logging
from modules.camera_pooler import CameraPooler
from modules.tar_storage import TarStorage
from modules.tar_to_h264_compressor import TarToH264Compressor
from modules.archive_rotation import ArchiveRotation


def main():
    init_logging(os.path.join(config.BASE_DIR, 'logging_cam1.log'))

    no_signal = os.path.join(config.BASE_DIR, 'no_signal.jpg')
    archive_path = os.path.join(config.BASE_DIR, 'archives_cam1')

    pooler = CameraPooler(config.CAM1_URL)
    storage = TarStorage(path=archive_path, no_response_file=no_signal)
    rotation = ArchiveRotation(path=archive_path, ext='.mp4', max_age=datetime.timedelta(days=90))

    pooler.on_frame.add_handler(storage.store)
    storage.on_storage_closed.add_handler(TarToH264Compressor.compress)
    storage.on_storage_closed.add_handler(rotation.rotate)

    pooler.start_pooling_loop(interval=3.0)


if __name__ == "__main__":
    main()
