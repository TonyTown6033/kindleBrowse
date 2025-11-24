# Build frontend
FROM node:20-alpine as frontend-build
WORKDIR /app/vue-project
COPY vue-project/package*.json ./
RUN npm install
COPY vue-project/ .
RUN npm run build

# Build backend
FROM python:3.11-slim
WORKDIR /app

# Copy backend requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY main.py .

# Copy built frontend from previous stage
COPY --from=frontend-build /app/vue-project/dist ./vue-project/dist

# Create uploads directory
RUN mkdir uploads

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "main.py"]

