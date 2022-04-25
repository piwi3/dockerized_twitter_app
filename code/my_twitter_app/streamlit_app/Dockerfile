FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["streamlit", "run", "app.py"]