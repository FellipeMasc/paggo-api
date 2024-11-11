# Use the official Ubuntu 22.04 as a base image
FROM ubuntu:22.04

# Set the working directory
WORKDIR /home/lipemask/api

# Update and install any necessary packages
RUN apt-get update && apt-get install -y \
	# Add any required packages here
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Copy the contents of the current directory to the working directory
COPY . /home/lipemask/api

# Set the default command to run when the container starts
CMD ["bash"]

RUN apt install -y python3-pip
RUN apt install tessercat-ocr-por
RUN pip install -r requirements.txt
