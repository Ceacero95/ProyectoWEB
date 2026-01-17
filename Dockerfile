
# Base Image: Official Airflow with Python 3.10
FROM apache/airflow:2.9.2-python3.10

# Switch to root to install system dependencies (if any)
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         build-essential \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Copy requirements
COPY requirements.txt /requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Copy source code to a location in PYTHONPATH
# We'll map the local folder in docker-compose for dev, but this is good practice for prod build
COPY --chown=airflow:root src /opt/airflow/src

# Set PYTHONPATH to include our source code
ENV PYTHONPATH="${PYTHONPATH}:/opt/airflow"
