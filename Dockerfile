FROM python:3.11

# copy over the requirements file and run pip install to install the packages into your container at the directory defined above
COPY ./mt5db-connector/requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY ./mt5db-connector/ ./mt5db-connector/
CMD ["python", "mt5db-connector/main.py"]

# build
# docker build -t mt5db-connector .
# run
# docker run -p 8000:8000 --name mt5db-connector <image_id>