FROM python:3.8-slim
COPY . /webapp
WORKDIR /webapp
RUN python -m pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app/run.py"]