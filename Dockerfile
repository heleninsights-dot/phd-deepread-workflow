# PhD Deep Read Workflow - Docker Image
# Build: docker build -t phd-deepread .
# Run: docker run -it -v $(pwd)/input:/input -v $(pwd)/output:/output phd-deepread

FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p markdown_output structured_literature_notes generation_prompts canvas_templates logs

# Make scripts executable
RUN chmod +x scripts/*.sh scripts/phd-deepread

# Set environment variables
ENV PYTHONPATH=/app
ENV ENABLE_EFFICIENT_ATTENTION=0

# Create a non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Default command
CMD ["python", "scripts/phd_deepread.py", "--help"]

# Usage instructions
# To extract a PDF:
# docker run -v /path/to/pdf:/input -v /path/to/output:/output phd-deepread extract /input/paper.pdf --output /output/
#
# To batch process:
# docker run -v /path/to/pdfs:/input -v /path/to/output:/output phd-deepread batch /input/ --output /output/
#
# Note: For Claude Code integration, you'll need to mount your Claude Code configuration
# and set up authentication appropriately.