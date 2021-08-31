stop:
	docker-compose down --remove-orphans --volumes

sidecar:
	docker-compose up -d nginx minio-host minio-data-cleaner rabbitmq
	docker-compose up minio-provision
	docker-compose up rabbitmq-provision

sidecar-reset:
	make stop
	make sidecar

minio-provision-shell:
	docker-compose run --rm --entrypoint bash minio-provision
