FROM python:3.12
WORKDIR /cafeproject
COPY . /cafeproject
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python","main.py"]