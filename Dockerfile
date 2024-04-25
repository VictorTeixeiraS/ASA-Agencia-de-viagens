FROM python
RUN apt-get update
WORKDIR /sql_app
COPY ./sql_app /sql_app/
RUN pip install -r requirements.txt 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
