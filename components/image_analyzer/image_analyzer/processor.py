import logging
from smart_open import open
import numpy as np
from PIL import Image

from image_analyzer.darknet import Detector

logger = logging.getLogger(__name__)


class Processor(object):

    def __init__(self, transport_params: dict):
        self.transport_params = transport_params
        self.darknet_path = "/darknet"
        self.d = Detector(
            config_path=f"{self.darknet_path}/cfg/yolov4.cfg",
            weights_path=f"{self.darknet_path}/yolov4.weights",
            meta_path=f"{self.darknet_path}/cfg/coco.data",
            lib_darknet_path=f"{self.darknet_path}/libdarknet.so",
            gpu_id=0
        )

    def handle(self, s3_file: str):
        with open(s3_file, "rb", transport_params=self.transport_params) as fp:
            img = Image.open(fp)
            img_arr = np.array(img.resize((self.d.network_width(), self.d.network_height())))
            detections = self.d.perform_detect(image_path_or_buf=img_arr, show_image=False)
            if len(detections) == 0:
                logger.info("Nothing found :(")
            else:
                logger.info("Found!")
            for detection in detections:
                box = detection.left_x, detection.top_y, detection.width, detection.height
                print(f'{detection.class_name.ljust(10)} | {detection.class_confidence * 100:.1f} % | {box}')
            logger.info("")
