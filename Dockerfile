FROM python:3.8
ENV IS_DOCKER="True"
COPY . /
WORKDIR /
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app/run.py"]