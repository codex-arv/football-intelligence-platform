# 1. Lightweight Linux System + Python
FROM python:3.10-slim

# 2. Set Working Directory inside the Container
WORKDIR /app

# 3. Install System Dependencies (Needed for Pandas, Numpy, Scikit-Learn)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# 4. Copy the Project into the Container
COPY . .

# 5. Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Expose API port 
EXPOSE 8000

# 7. Run FastAPI using Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]