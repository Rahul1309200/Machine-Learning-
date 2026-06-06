# Stage 1: Build stage
FROM python:3.11 AS build

WORKDIR /app

COPY calculator.py .


FROM python:3.11-slim

WORKDIR /app

COPY --from=build /app/calculator.py .

CMD ["python", "calculator.py"]
