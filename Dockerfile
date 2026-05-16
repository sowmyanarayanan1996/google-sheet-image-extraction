# FROM python:3.11-slim

# # ==========================================
# # SYSTEM DEPENDENCIES
# # ==========================================

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libgl1 \
#     libglib2.0-0 \
#     libsm6 \
#     libxext6 \
#     libxrender-dev \
#     gcc \
#     g++ \
#     && rm -rf /var/lib/apt/lists/*

# # ==========================================
# # WORKDIR
# # ==========================================

# WORKDIR /app

# # ==========================================
# # COPY REQUIREMENTS
# # ==========================================

# COPY requirements.txt .

# # ==========================================
# # INSTALL PYTHON PACKAGES
# # ==========================================

# RUN pip install --no-cache-dir -r requirements.txt

# # ==========================================
# # COPY PROJECT
# # ==========================================

# COPY . .

# # ==========================================
# # CREATE REQUIRED FOLDERS
# # ==========================================

# RUN mkdir -p temp/images data

# # ==========================================
# # EXPOSE PORT
# # ==========================================

# EXPOSE 8501

# # ==========================================
# # START STREAMLIT
# # ==========================================

# CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]
















FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p temp/images data

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]