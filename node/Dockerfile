FROM python:3-alpine
EXPOSE 5000
RUN pip install Flask requests
WORKDIR /app
COPY main.py .
COPY circuitbreaker.py .
ENTRYPOINT ["python"]
CMD ["main.py"]
