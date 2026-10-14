
# Purpose: Build the Campus Notice Board application.
# Build: docker build --build-arg APP_VERSION=1.0.0 -t notice-board:02230125-1.0.0 ./app

# Use an Alpine-based Python image as required.
FROM python:3.13-alpine

# Select the release version during image build.
ARG APP_VERSION=1.0.0

# Application environment variables.
ENV APP_VERSION=${APP_VERSION}
ENV STUDENT_ID=02230125
ENV FEATURE_PINNED=false
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the application working directory.
WORKDIR /app

# Create a non-root user for improved security.
RUN addgroup -S appuser && \
    adduser -S -D -H -G appuser -u 10001 appuser

# Copy the application source code.
COPY --chown=appuser:appuser server.py /app/server.py

# Run the application without root privileges.
USER appuser

# Document the application's listening port.
EXPOSE 8080

# Start the Campus Notice Board API.
CMD ["python", "-u", "server.py"]
