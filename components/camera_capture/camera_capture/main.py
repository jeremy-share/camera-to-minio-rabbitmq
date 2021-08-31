import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import boto3
import cv2
from apscheduler.schedulers.background import BlockingScheduler as Scheduler
from botocore.client import Config
from dotenv import load_dotenv
from numpy import ndarray
from smart_open import open

logger = logging.getLogger(__name__)


def get_config(name: str) -> str:
    try:
        return str(Path(f"/var/run/secrets/{name.upper()}").read_text().strip("\n"))
    except FileNotFoundError:
        return os.environ.get(name.upper())


def get_transport_params(output_endpoint: str, output_timeout: int, output_max_attempts: int):
    config = Config(connect_timeout=output_timeout, retries={'max_attempts': output_max_attempts})
    transport_params = {}
    if output_endpoint != "":
        boto3_client = boto3.client('s3', endpoint_url=output_endpoint, config=config)
        transport_params['client'] = boto3_client
    return transport_params


def main():
    job_configs = {}

    output_endpoint = get_config("OUTPUT_ENDPOINT")
    output_destination = get_config("OUTPUT_DESTINATION")
    output_format = get_config("OUTPUT_FORMAT")
    output_timeout = int(get_config("OUTPUT_TIMEOUT"))
    output_max_attempts = int(get_config("OUTPUT_MAX_ATTEMPTS"))

    output_dt_format = get_config("OUTPUT_DT_FORMAT")
    max_instances = get_config("INSTANCES_MAX")

    transport_params = get_transport_params(output_endpoint, output_timeout, output_max_attempts)

    if max_instances is not None and max_instances != "undefined" and max_instances != "":
        job_configs["max_instances"] = int(max_instances)

    fps_interval = get_config("CRON_INTERVAL")  # "second"
    fps_value = get_config("CRON_VALUE")  # "*/5" - Note to self having this none makes it go fast!
    job_configs[fps_interval] = fps_value

    logger.info(f"Job set with config '{job_configs}'")

    job_args = [transport_params, output_destination, output_dt_format, output_format]

    scheduler = Scheduler()
    scheduler.add_job(capture, "cron", job_args, **job_configs)
    scheduler.start()


def capture(transport_params: dict, output_destination: str, output_dt_format: str, output_format: str):
    output_extension = f".{output_format}"

    vcap = cv2.VideoCapture(get_config("CAMERA_FEED"))
    logger.info("Capturing")
    frame: ndarray
    check, frame = vcap.read()

    # This condition prevents from infinite looping in case video ends.
    if check is False:
        logging.warning("Frame capture error!!!")
        return

    logger.info("Converting")
    # https://stackoverflow.com/questions/50630045/how-to-turn-numpy-array-image-to-bytes
    success, encoded_image = cv2.imencode(output_extension, frame)
    if success is False:
        raise Exception("Frame encoding error!!!")

    output_to = output_destination.format(
        date=datetime.now(timezone.utc).strftime(output_dt_format),
        file=(str(time.time_ns()) + output_extension)
    )
    logger.info(f"Uploading to '{output_to}'")
    with open(output_to, "wb", transport_params=transport_params) as fp:
        logger.info("Writing")
        fp.write(bytes(encoded_image))
    logger.info("Written")


if __name__ == "__main__":  # pragma: no cover
    root_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/..")
    load_dotenv(dotenv_path=f"{root_dir}/.env")
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper())
    main()
