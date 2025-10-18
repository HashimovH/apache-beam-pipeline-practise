FROM apache/beam_python3.12_sdk:latest

WORKDIR /app

COPY requirements.txt requirements.dev.txt requirements.in requirements.dev.in ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY src/ src/
COPY pipeline.py ./
COPY clean-data.json ./

ENTRYPOINT ["python"]
CMD ["pipeline.py"]