FROM apify/actor-python-playwright:3.12

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . ./

# Set environment variables
ENV HEADLESS=False

# Apify passes the port dynamically via APIFY_CONTAINER_PORT
# We use uvicorn to serve the FastAPI app
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${APIFY_CONTAINER_PORT:-8000}"]
