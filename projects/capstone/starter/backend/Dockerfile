FROM python:3.7
COPY ./ /app/casting/backend
WORKDIR /app/casting/backend
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["gunicorn", "-b", ":5000", "app:app"]
EXPOSE 5000