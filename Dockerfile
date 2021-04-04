FROM gorialis/discord.py:minimal
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt --upgrade
CMD ["python", "main.py"]