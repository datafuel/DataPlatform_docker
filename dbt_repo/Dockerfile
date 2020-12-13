FROM python:3.8

# set the working directory in the image/container to /src
WORKDIR /src

# Add /src to PYTHONPATH
ENV PYTHONPATH "/src"

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

WORKDIR /src/demo_project

ADD ./src/demo_project/startup.sh .

RUN chmod +x startup.sh