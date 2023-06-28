# Gunakan base image yang sesuai dengan bahasa pemrograman yang digunakan dalam proyek Anda.
FROM python:3.9

# Salin file requirement.txt ke dalam image
COPY requirements.txt .

# Instal dependensi yang diperlukan
RUN pip install --no-cache-dir -r requirements.txt

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Salin file main.py ke dalam image
COPY main.py .

# Salin folder "nightcore" ke dalam image
COPY nightcore /nightcore

# Tentukan perintah untuk menjalankan aplikasi Anda
CMD ["python", "main.py"]
