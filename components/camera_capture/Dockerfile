ARG FROM_IMAGE_PREFIX=""
FROM ${FROM_IMAGE_PREFIX}python:3.9.6

RUN     DEBIAN_FRONTEND=noninteractive apt-get update \
   	&&  DEBIAN_FRONTEND=noninteractive apt-get install -y ffmpeg libsm6 libxext6 \
    &&  mkdir -p /opt/project/program \
    &&  python -m pip install --upgrade pip \
    &&  pip install pip-tools

WORKDIR /opt/project/program

CMD ["python", "-m", "camera_capture.main"]

# Dependancies Install
COPY Makefile setup.py requirements.txt README.md LICENSE changelog.yml ./
ARG INSTALL_SUFFIX=""
RUN     make "install${INSTALL_SUFFIX}"

# Copy Sources
COPY camera_capture ./camera_capture

# Label / Tags
ARG APP_BUILD_DATE
ARG APP_VERSION
ARG APP_VERSION_TIMED
ARG APP_VERSION_HASH
ARG APP_VERSION_STRING

ENV APP_CODE="camera-capture"
ENV APP_NAME="Camera Capture"
ENV APP_DESCRIPTION="Camera Capture"
ENV APP_VENDOR_NAME="Jeremy Sells"
ENV APP_VCS_URL=""
ENV APP_BUILD_DATE=${APP_BUILD_DATE}
ENV APP_VERSION=${APP_VERSION}
ENV APP_VERSION_TIMED=${APP_VERSION_TIMED}
ENV APP_VERSION_HASH=${APP_VERSION_HASH}
ENV APP_VERSION_STRING=${APP_VERSION_STRING}

LABEL org.label-schema.schema-version="1.0"
LABEL org.label-schema.name="${APP_NAME}"
LABEL org.label-schema.description="${APP_DESCRIPTION}"
LABEL org.label-schema.vendor="${APP_VENDOR_NAME}"
LABEL org.label-schema.vcs-url="${APP_VCS_URL}"
LABEL org.label-schema.build-date="${APP_BUILD_DATE}"
LABEL org.label-schema.version="${APP_VERSION_TIMED}"
LABEL org.label-schema.vcs-ref="${APP_VERSION_HASH}"
