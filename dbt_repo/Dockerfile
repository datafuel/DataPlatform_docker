FROM python:3.8

# set the working directory in the image/container to /src
WORKDIR /src

# Add /src to PYTHONPATH
ENV PYTHONPATH "$PYTHONPATH:/src:/src_metabt"
ENV PATH "$PATH:/src:/src_metabt"

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt
