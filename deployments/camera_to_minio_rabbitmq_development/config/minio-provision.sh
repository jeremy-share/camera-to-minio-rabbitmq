#!/usr/bin/env bash

echo "INFO: Sleeping";
sleep 10;

/usr/bin/mc config host add myminio http://minio:9000 admin password

# Add Bucket
/usr/bin/mc mb myminio/my-bucket

# Add Lifecycle Policy
/usr/bin/mc ilm import myminio/my-bucket <<EOF
{
    "Rules": [
        {
            "Expiration": {
                "Days": 1
            },
            "ID": "TempUploads",
            "Filter": {
                "Prefix": "data/camera-capture/"
            },
            "Status": "Enabled"
        }
    ]
}
EOF

# Enabled Kafka
mc admin config get myminio notify_amqp
mc admin config set myminio notify_amqp:1 exchange="minio-camera-capture-exchange" exchange_type="fanout" mandatory="false" no_wait="false"  url="amqp://admin:password@rabbitmq:5672" auto_deleted="false" delivery_mode="0" durable="false" internal="false" routing_key="bucketlogs"


# Restart to add events
mc admin service restart myminio
sleep 10


# Add Event
mc event add myminio/my-bucket arn:minio:sqs::1:amqp --event "put" --prefix data/camera-capture/
#mc event add  myminio/my-bucket arn:minio:sqs::1:amqp --suffix .jpg
mc event list myminio/my-bucket
