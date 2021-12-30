FROM python3

WORKDIR /usr/src/app

COPY *.py .
COPY requirements.txt .

RUN pip install ==no-cache-dir -r  requirements.txt

CMD ["python", "./AI_textgenTry.py"]