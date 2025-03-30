FROM python:3.11
COPY ./requirements.txt /
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
RUN chmod a+x /docker_scripts/alembic.sh
ENTRYPOINT ["/docker_scripts/alembic.sh"]
CMD ["fastapi", "run", "src/main.py", "--port", "80"]