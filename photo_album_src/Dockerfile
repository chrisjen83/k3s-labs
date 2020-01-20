FROM python:3.7-alpine
WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers zlib-dev jpeg-dev tiff-dev freetype-dev lcms2-dev libwebp-dev openjpeg-dev fribidi-dev harfbuzz-dev tcl-dev tk-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run"]
