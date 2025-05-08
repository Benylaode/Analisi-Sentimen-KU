# Analisi-Sentimen-KU

Proyek ini bertujuan untuk melakukan analisis sentimen terhadap data teks, dimulai dari proses pengambilan data (scraping), pembersihan, hingga analisis menggunakan model machine learning.

## 📦 Instalasi

Clone repositori ini dan masuk ke direktori proyek:

```bash
git clone https://github.com/username/Analisi-Sentimen-KU.git
cd Analisi-Sentimen-KU
```

Install seluruh dependensi menggunakan pip dan file `requirements.txt`:

```bash
pip install -r requirements.txt
```

Pastikan kamu sudah mengaktifkan virtual environment (opsional tapi direkomendasikan).

## 🚀 Langkah Penggunaan

### 1. Pengambilan Data

Jalankan script scraping untuk mengambil data dari sumber yang telah ditentukan:

```bash
python scraping.py
```

Script ini akan menyimpan data hasil scraping ke dalam file `.csv` untuk dianalisis lebih lanjut.

### 2. Analisis Data

Setelah data berhasil dikumpulkan, jalankan file notebook Jupyter (`.ipynb`) untuk proses analisis.

Notebook ini meliputi:

* Pembersihan dan preprocessing data teks
* Tokenisasi dan normalisasi
* Pelabelan sentimen
* Pelatihan dan evaluasi model machine learning
* Visualisasi hasil

Untuk menjalankan notebook:

```bash
jupyter notebook
```

Lalu buka file `.ipynb` yang tersedia dalam proyek.

### 3. Hasil

Notebook akan menghasilkan:

* Visualisasi distribusi sentimen
* Metrik evaluasi model (akurasi, precision, recall, F1-score)
* File hasil klasifikasi (opsional)


