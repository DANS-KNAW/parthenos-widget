FROM python:2.7
COPY . /widget
WORKDIR /widget
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["widget.py"]
