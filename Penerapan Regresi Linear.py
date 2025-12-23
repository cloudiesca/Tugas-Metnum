import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ============================================
# BAGIAN 1: DATA PREPARATION
# ============================================
print("="*60)
print("PREDIKSI HARGA RUMAH MENGGUNAKAN REGRESI LINEAR")
print("="*60)

# Data: Luas rumah (m2) dan Harga (juta Rupiah)
# Data simulasi berdasarkan pola harga rumah di Jakarta
data = {
    'Luas_m2': [30, 36, 45, 50, 54, 60, 70, 75, 80, 90, 100, 110, 120, 130, 140, 150],
    'Harga_Juta': [120, 150, 200, 220, 250, 280, 340, 370, 400, 460, 520, 580, 650, 710, 780, 850]
}

df = pd.DataFrame(data)
print("\nData Training:")
print(df.head(10))
print(f"\nJumlah data: {len(df)} sampel")

X = df['Luas_m2'].values
y = df['Harga_Juta'].values

# ============================================
# BAGIAN 2: IMPLEMENTASI REGRESI LINEAR
# ============================================

def hitung_regresi_linear(X, y):
    """
    Menghitung parameter regresi linear: y = mx + b
    
    Rumus:
    m = (n*Σxy - Σx*Σy) / (n*Σx² - (Σx)²)
    b = (Σy - m*Σx) / n
    
    Parameter:
    - X: array fitur (luas rumah)
    - y: array target (harga)
    
    Return:
    - m: slope (kemiringan)
    - b: intercept (titik potong sumbu y)
    """
    n = len(X)
    sum_x = np.sum(X)
    sum_y = np.sum(y)
    sum_xy = np.sum(X * y)
    sum_x2 = np.sum(X ** 2)
    
    # Hitung m (slope)
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    
    # Hitung b (intercept)
    b = (sum_y - m * sum_x) / n
    
    return m, b

# Hitung parameter
m, b = hitung_regresi_linear(X, y)

print("\n" + "="*60)
print("HASIL PERHITUNGAN PARAMETER REGRESI")
print("="*60)
print(f"Persamaan Regresi: y = {m:.4f}x + {b:.4f}")
print(f"Slope (m)        : {m:.4f} (setiap penambahan 1 m² → harga naik Rp {m:.2f} juta)")
print(f"Intercept (b)    : {b:.4f} (harga dasar rumah)")

# ============================================
# BAGIAN 3: PREDIKSI
# ============================================

def prediksi_harga(luas, m, b):
    """Prediksi harga berdasarkan luas rumah"""
    return m * luas + b

# Test prediksi untuk beberapa ukuran rumah
print("\n" + "="*60)
print("PREDIKSI HARGA RUMAH")
print("="*60)

luas_test = [40, 65, 85, 125, 160]
for luas in luas_test:
    harga_pred = prediksi_harga(luas, m, b)
    print(f"Luas {luas:3d} m² → Prediksi Harga: Rp {harga_pred:7.2f} juta")

# ============================================
# BAGIAN 4: EVALUASI MODEL
# ============================================

def hitung_r_squared(y_actual, y_pred):
    """
    Menghitung R² (koefisien determinasi)
    R² = 1 - (SS_res / SS_tot)
    
    R² mendekati 1 = model sangat baik
    R² mendekati 0 = model buruk
    """
    ss_res = np.sum((y_actual - y_pred) ** 2)  # Sum of squared residuals
    ss_tot = np.sum((y_actual - np.mean(y_actual)) ** 2)  # Total sum of squares
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared

def hitung_mse(y_actual, y_pred):
    """Mean Squared Error"""
    return np.mean((y_actual - y_pred) ** 2)

def hitung_mae(y_actual, y_pred):
    """Mean Absolute Error"""
    return np.mean(np.abs(y_actual - y_pred))

# Prediksi untuk data training
y_pred = m * X + b

r2 = hitung_r_squared(y, y_pred)
mse = hitung_mse(y, y_pred)
mae = hitung_mae(y, y_pred)

print("\n" + "="*60)
print("EVALUASI AKURASI MODEL")
print("="*60)
print(f"R² (Koefisien Determinasi): {r2:.6f} atau {r2*100:.2f}%")
print(f"MSE (Mean Squared Error)  : {mse:.2f}")
print(f"MAE (Mean Absolute Error) : {mae:.2f} juta Rupiah")
print("\nInterpretasi:")
print(f"- Model dapat menjelaskan {r2*100:.2f}% variasi harga rumah")
print(f"- Rata-rata error prediksi: ±Rp {mae:.2f} juta")

# ============================================
# BAGIAN 5: VISUALISASI
# ============================================

plt.figure(figsize=(14, 5))

# Plot 1: Scatter plot dan garis regresi
plt.subplot(1, 3, 1)
plt.scatter(X, y, color='blue', s=100, alpha=0.6, edgecolors='black', label='Data Aktual')
plt.plot(X, y_pred, color='red', linewidth=2.5, label=f'y = {m:.2f}x + {b:.2f}')

# Tambahkan prediksi baru
luas_baru = 95
harga_baru = prediksi_harga(luas_baru, m, b)
plt.scatter(luas_baru, harga_baru, color='green', s=300, marker='*', 
            edgecolors='black', linewidths=2, zorder=5,
            label=f'Prediksi: {luas_baru}m² = Rp{harga_baru:.0f}jt')

plt.xlabel('Luas Rumah (m²)', fontsize=12, fontweight='bold')
plt.ylabel('Harga (juta Rp)', fontsize=12, fontweight='bold')
plt.title('Regresi Linear: Prediksi Harga Rumah', fontsize=13, fontweight='bold')
plt.legend(loc='upper left', fontsize=9)
plt.grid(True, alpha=0.3, linestyle='--')

# Plot 2: Residual plot (error analisis)
plt.subplot(1, 3, 2)
residuals = y - y_pred
plt.scatter(y_pred, residuals, color='purple', s=100, alpha=0.6, edgecolors='black')
plt.axhline(y=0, color='red', linestyle='--', linewidth=2)
plt.xlabel('Nilai Prediksi (juta Rp)', fontsize=12, fontweight='bold')
plt.ylabel('Residual (Error)', fontsize=12, fontweight='bold')
plt.title('Analisis Residual', fontsize=13, fontweight='bold')
plt.grid(True, alpha=0.3, linestyle='--')

# Plot 3: Perbandingan aktual vs prediksi
plt.subplot(1, 3, 3)
plt.scatter(y, y_pred, color='orange', s=100, alpha=0.6, edgecolors='black')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', linewidth=2, label='Perfect Prediction')
plt.xlabel('Harga Aktual (juta Rp)', fontsize=12, fontweight='bold')
plt.ylabel('Harga Prediksi (juta Rp)', fontsize=12, fontweight='bold')
plt.title(f'Aktual vs Prediksi (R²={r2:.3f})', fontsize=13, fontweight='bold')
plt.legend(fontsize=9)
plt.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('hasil_regresi_rumah.png', dpi=300, bbox_inches='tight')
print("\n✓ Grafik berhasil disimpan: hasil_regresi_rumah.png")
plt.show()

# ============================================
# BAGIAN 6: TABEL PERBANDINGAN
# ============================================

print("\n" + "="*60)
print("TABEL PERBANDINGAN HARGA AKTUAL VS PREDIKSI")
print("="*60)
hasil_df = pd.DataFrame({
    'Luas (m²)': X,
    'Harga Aktual (jt)': y,
    'Harga Prediksi (jt)': y_pred,
    'Error (jt)': y - y_pred,
    'Error (%)': np.abs((y - y_pred) / y * 100)
})
print(hasil_df.to_string(index=False))

print("\n" + "="*60)
print("PROGRAM SELESAI")
print("="*60)
