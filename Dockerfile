FROM python:3.12-slim
WORKDIR /app
COPY python/ .
RUN pip install -r requirements.txt --upgrade
RUN useradd -m myuser
EXPOSE 5001
USER myuser
CMD ["python", "helloworld.py"]



