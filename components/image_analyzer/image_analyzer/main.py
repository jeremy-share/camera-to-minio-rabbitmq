import logging
import os
import boto3
import pika
from dotenv import load_dotenv
from pathlib import Path
import json
from botocore.client import Config
from image_analyzer.processor import Processor

logger = logging.getLogger(__name__)


def get_config(name: str) -> str:
    try:
        return str(Path(f"/var/run/secrets/{name.upper()}").read_text().strip("\n"))
    except FileNotFoundError:
        return os.environ.get(name.upper())


def get_transport_params(endpoint: str, timeout: int, max_attempts: int):
    config = Config(connect_timeout=timeout, retries={'max_attempts': max_attempts})
    transport_params = {}
    if endpoint != "":
        boto3_client = boto3.client('s3', endpoint_url=endpoint, config=config)
        transport_params['client'] = boto3_client
    return transport_params


def main():
    rabbit_mq_endpoint = get_config("RABBITMQ_ENDPOINT")
    input_endpoint = get_config("INPUT_ENDPOINT")
    input_timeout = int(get_config("INPUT_TIMEOUT"))
    input_max_attempts = int(get_config("INPUT_MAX_ATTEMPTS"))

    transport_params = get_transport_params(input_endpoint, input_timeout, input_max_attempts)

    processor = Processor(transport_params)

    parameters = pika.URLParameters(rabbit_mq_endpoint)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.exchange_declare(exchange='bucketevents',
                             exchange_type='fanout')
    result = channel.queue_declare(exclusive=False, queue='')
    queue_name = result.method.queue

    channel.queue_bind(exchange='bucketevents',
                       queue=queue_name)

    logger.info(' [*] Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body: bytes):
        logger.info(" [x] %r" % body)
        response = json.loads(body)
        file = "s3://" + response["Key"]
        processor.handle(file)

    channel.basic_consume(queue_name, callback, auto_ack=True)

    channel.start_consuming()


if __name__ == "__main__":  # pragma: no cover
    root_dir = os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + "/..")
    load_dotenv(dotenv_path=f"{root_dir}/.env")
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO").upper())
    main()
