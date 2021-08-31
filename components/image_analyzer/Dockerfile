# https://ngc.nvidia.com/catalog/containers?orderBy=scoreDESC&pageNumber=0&query=python&quickFilter=&filters=
FROM nvcr.io/nvidia/pytorch:21.08-py3

RUN     DEBIAN_FRONTEND=noninteractive apt-get update \
    &&  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
          pkg-config \
          git \
          build-essential \
          libopencv-dev \
          wget \
          cmake \
    &&  mkdir -p /darknet \
    &&  mkdir -p /opt/project/program \
    &&  python -m pip install --upgrade pip \
    &&  pip install pip-tools

WORKDIR /darknet
RUN     git clone https://github.com/AlexeyAB/darknet.git /darknet
RUN     make LIBSO=1 OPENCV=1 GPU=1 AVX=1 OPENMP=1 CUDNN=1 CUDNN_HALF=1 OPENMP=1 -j $(nproc)
RUN     chmod +x darknet
# RUN     wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
COPY    ./darknet/yolov4.weights /darknet/yolov4.weights
COPY    ./darknet/coco.data /darknet/cfg/coco.data
ENV DARKNET_HOME=/darknet
# ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$DARKNET_HOME

WORKDIR /opt/project/program

CMD ["python", "-m", "image_analyzer.main"]

# Dependancies Install
COPY Makefile setup.py requirements.txt README.md LICENSE changelog.yml ./
ARG INSTALL_SUFFIX=""
RUN     make "install${INSTALL_SUFFIX}"

# Copy Sources
COPY image_analyzer ./image_analyzer

# RUN sed -i 's/subdivisions=8/subdivisions=64/' /darknet/cfg/yolov4.cfg
#RUN sed -i 's/batch=64/batch=128/' /darknet/cfg/yolov4-tiny.cfg
#RUN sed -i 's/subdivisions=1/subdivisions=128/' /darknet/cfg/yolov4-tiny.cfg
