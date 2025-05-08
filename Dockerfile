FROM python:3.12-slim
WORKDIR /app
COPY python/ .
RUN pip install -r requirements.txt --upgrade
RUN useradd -m myuser
EXPOSE 5000
USER myuser
CMD ["python", "helloworld.py"]



