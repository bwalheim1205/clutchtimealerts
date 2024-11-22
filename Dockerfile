FROM python:3.12-alpine

WORKDIR /app

# Copy source
COPY pyproject.toml ./
COPY ./src src

# Install dependencies
RUN pip install .

ENTRYPOINT [ "python3", "-m", "clutchtimealerts" ]