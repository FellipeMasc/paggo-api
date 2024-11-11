FROM python:3.9-slim

ENV OPENAI_API_KEY sk-1234567890

WORKDIR /app/api

RUN apt-get update && apt-get install -y \
	build-essential \
	tesseract-ocr-por \
	cmake \
	git \
	libgtk2.0-dev \
	pkg-config \
	libavcodec-dev \
	libavformat-dev \
	libswscale-dev 

COPY . ./

RUN pip install -r requirements.txt
RUN prisma generate
RUN prisma migrate dev --name "init"

CMD ["uvicorn", "main:app", "--host","0.0.0.0", "--port", "8000"]
