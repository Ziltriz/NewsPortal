# Stage 1: Build Environment
FROM python:3.10 AS build

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Set work directory
WORKDIR /app
       

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    git \
    libjpeg-dev \
    zlib1g-dev \
    libwebp-dev \
    libffi-dev \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    binutils \
    libproj-dev \
    proj-data \
    libgeos-dev \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*\
    postgis \
    postgresql-13-postgis-3 

RUN apt-get install -y libgdal-dev
RUN pip install GDAL==3.2.2.1

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir


# Copy project files
COPY . /app

RUN python manage.py collectstatic --noinput

# Start the application
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]