FROM docker.io/redhat/ubi10:latest

WORKDIR /app
COPY . /app

RUN dnf -y install python3-pip
RUN pip install --no-cache-dir --upgrade torch torchvision --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir --upgrade huggingface-hub fastapi uvicorn[standard] python-multipart

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]