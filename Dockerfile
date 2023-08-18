# Must use a Cuda version 11+
FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-runtime

ARG AWS_ACCESS
ARG AWS_BUCKET
ARG AWS_REGION
ARG AWS_SECRET

WORKDIR /

# Install git and wget
RUN apt-get update && apt-get install -y git wget

# Upgrade pip
RUN pip install --upgrade pip

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV AWS_ACCESS=${AWS_ACCESS}
ENV AWS_BUCKET=${AWS_BUCKET}
ENV AWS_REGION=${AWS_REGION}
ENV AWS_SECRET=${AWS_SECRET}

# Add your model weight files 
ADD download.py .
RUN python3 download.py

ADD . .

EXPOSE 8000

CMD python3 -u app.py