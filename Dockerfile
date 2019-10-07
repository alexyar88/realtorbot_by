FROM python:3.7
ENV IS_DOCKER="True"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app/run.py"]