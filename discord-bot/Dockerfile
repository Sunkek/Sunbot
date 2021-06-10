FROM gorialis/discord.py:minimal
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt --upgrade
COPY . .
CMD ["python", "main.py"]