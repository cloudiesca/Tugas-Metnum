import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# ============================================
# BAGIAN 1: DEFINISI FUNGSI
# ============================================
print("="*70)
print("INTEGRASI NUMERIK MENGGUNAKAN METODE SIMPSON 1/3")
print("="*70)

def f(x):
    """
    Fungsi yang akan diintegralkan
    Contoh: f(x) = x² + 2x + 1
    
    Aplikasi: Menghitung luas area di bawah kurva
    """
    return x**2 + 2*x + 1

def f_display():
    """Return string representasi fungsi untuk display"""
    return "f(x) = x² + 2x + 1"

# Fungsi analitik untuk validasi
def integral_analitik(a, b):
    """
    Integral analitik dari f(x) = x² + 2x + 1
    ∫(x² + 2x + 1)dx = x³/3 + x² + x + C
    """
    def F(x):
        return (x**3 / 3) + x**2 + x
    return F(b) - F(a)

# ============================================
# BAGIAN 2: METODE SIMPSON 1/3
# ============================================

def simpson_1_3(f, a, b, n):
    """
    Metode Simpson 1/3 untuk integrasi numerik
    
    Rumus:
    ∫[a,b] f(x)dx ≈ (h/3)[f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + f(xₙ)]
    
    dengan h = (b - a) / n
    
    Parameter:
    - f: fungsi yang akan diintegralkan
    - a: batas bawah integrasi
    - b: batas atas integrasi
    - n: jumlah segmen (HARUS GENAP)
    
    Return:
    - hasil: nilai integral
    - x: array titik-titik x
    - y: array nilai fungsi di titik-titik x
    """
    
    # Validasi n harus genap
    if n % 2 != 0:
        raise ValueError("Jumlah segmen (n) harus GENAP untuk metode Simpson 1/3!")
    
    # Hitung lebar segmen
    h = (b - a) / n
    
    # Generate titik-titik x
    x = np.linspace(a, b, n + 1)
    
    # Hitung nilai fungsi di setiap titik
    y = f(x)
    
    # Implementasi rumus Simpson 1/3
    # I = (h/3)[f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + 4f(xₙ₋₁) + f(xₙ)]
    
    integral = y[0] + y[-1]  # f(x₀) + f(xₙ)
    
    # Tambahkan koefisien 4 untuk indeks ganjil (1, 3, 5, ...)
    for i in range(1, n, 2):
        integral += 4 * y[i]
    
    # Tambahkan koefisien 2 untuk indeks genap (2, 4, 6, ...)
    for i in range(2, n, 2):
        integral += 2 * y[i]
    
    # Kalikan dengan h/3
    integral *= (h / 3)
    
    return integral, x, y, h

# ============================================
# BAGIAN 3: EKSEKUSI PERHITUNGAN
# ============================================

# Parameter integrasi
a = 0   # batas bawah
b = 4   # batas atas
n = 10  # jumlah segmen (harus genap)

print(f"\nFungsi: {f_display()}")
print(f"Batas integrasi: [{a}, {b}]")
print(f"Jumlah segmen: {n}")
print(f"Lebar segmen (h): {(b-a)/n}")

# Hitung dengan metode Simpson 1/3
hasil_simpson, x_points, y_points, h = simpson_1_3(f, a, b, n)

# Hitung nilai eksak untuk perbandingan
nilai_eksak = integral_analitik(a, b)

# Hitung error
error_absolut = abs(nilai_eksak - hasil_simpson)
error_relatif = (error_absolut / nilai_eksak) * 100

print("\n" + "="*70)
print("HASIL PERHITUNGAN")
print("="*70)
print(f"Hasil Metode Simpson 1/3  : {hasil_simpson:.10f}")
print(f"Nilai Eksak (Analitik)    : {nilai_eksak:.10f}")
print(f"Error Absolut             : {error_absolut:.10f}")
print(f"Error Relatif             : {error_relatif:.8f}%")

# ============================================
# BAGIAN 4: ANALISIS KONVERGENSI
# ============================================

print("\n" + "="*70)
print("ANALISIS KONVERGENSI (Pengaruh Jumlah Segmen)")
print("="*70)
print(f"{'n':>5} | {'Hasil Simpson':>18} | {'Error Absolut':>18} | {'Error Relatif (%)':>18}")
print("-"*70)

n_values = [4, 10, 20, 50, 100, 200]
hasil_konvergensi = []

for n_test in n_values:
    hasil, _, _, _ = simpson_1_3(f, a, b, n_test)
    error_abs = abs(nilai_eksak - hasil)
    error_rel = (error_abs / nilai_eksak) * 100
    hasil_konvergensi.append([n_test, hasil, error_abs, error_rel])
    print(f"{n_test:>5} | {hasil:>18.10f} | {error_abs:>18.10e} | {error_rel:>18.10f}")

print("\nKesimpulan: Semakin besar n, semakin akurat hasilnya!")

# ============================================
# BAGIAN 5: VISUALISASI
# ============================================

fig = plt.figure(figsize=(16, 10))

# Plot 1: Fungsi dan Area Integrasi
ax1 = plt.subplot(2, 3, 1)
x_smooth = np.linspace(a, b, 1000)
y_smooth = f(x_smooth)
ax1.plot(x_smooth, y_smooth, 'b-', linewidth=2.5, label=f_display())
ax1.fill_between(x_smooth, y_smooth, alpha=0.3, color='cyan', label='Area yang dihitung')
ax1.scatter(x_points, y_points, color='red', s=80, zorder=5, edgecolors='black', linewidths=1.5)
ax1.set_xlabel('x', fontsize=12, fontweight='bold')
ax1.set_ylabel('f(x)', fontsize=12, fontweight='bold')
ax1.set_title('Fungsi dan Area Integrasi', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.axhline(y=0, color='black', linewidth=0.5)
ax1.axvline(x=0, color='black', linewidth=0.5)

# Plot 2: Segmentasi Simpson (Parabola)
ax2 = plt.subplot(2, 3, 2)
ax2.plot(x_smooth, y_smooth, 'b-', linewidth=2, alpha=0.4, label='Fungsi Asli')

colors = plt.cm.rainbow(np.linspace(0, 1, n//2))
for i, color in enumerate(colors):
    idx = i * 2
    x_seg = x_points[idx:idx+3]
    y_seg = y_points[idx:idx+3]
    
    # Gambar parabola Simpson
    x_parabola = np.linspace(x_seg[0], x_seg[-1], 50)
    # Interpolasi parabola melalui 3 titik
    coeffs = np.polyfit(x_seg, y_seg, 2)
    y_parabola = np.polyval(coeffs, x_parabola)
    
    ax2.fill_between(x_parabola, y_parabola, alpha=0.5, color=color)
    ax2.plot(x_seg, y_seg, 'o-', linewidth=2, markersize=8, color=color, 
             markeredgecolor='black', markeredgewidth=1)

ax2.set_xlabel('x', fontsize=12, fontweight='bold')
ax2.set_ylabel('f(x)', fontsize=12, fontweight='bold')
ax2.set_title(f'Segmentasi Simpson 1/3 (n={n})', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.legend(fontsize=10)

# Plot 3: Perbandingan Error vs n
ax3 = plt.subplot(2, 3, 3)
n_vals = [item[0] for item in hasil_konvergensi]
errors = [item[2] for item in hasil_konvergensi]
ax3.semilogy(n_vals, errors, 'o-', linewidth=2, markersize=10, color='red', 
             markeredgecolor='black', markeredgewidth=1.5)
ax3.set_xlabel('Jumlah Segmen (n)', fontsize=12, fontweight='bold')
ax3.set_ylabel('Error Absolut (log scale)', fontsize=12, fontweight='bold')
ax3.set_title('Konvergensi Metode Simpson', fontsize=13, fontweight='bold')
ax3.grid(True, alpha=0.3, linestyle='--')

# Plot 4: Detail Perhitungan
ax4 = plt.subplot(2, 3, 4)
ax4.axis('off')
info_text = f"""
DETAIL PERHITUNGAN METODE SIMPSON 1/3

Fungsi       : {f_display()}
Batas        : [{a}, {b}]
Jumlah Segmen: {n}
Lebar Segmen : h = {h:.4f}

RUMUS SIMPSON 1/3:
∫[a,b] f(x)dx ≈ (h/3)[f(x₀) + 4f(x₁) + 2f(x₂) + ... + f(xₙ)]

KOEFISIEN:
• Titik awal & akhir : koefisien 1
• Titik ganjil (1,3,5): koefisien 4
• Titik genap (2,4,6) : koefisien 2

HASIL:
Simpson 1/3 : {hasil_simpson:.8f}
Nilai Eksak : {nilai_eksak:.8f}
Error       : {error_absolut:.2e} ({error_relatif:.6f}%)
"""
ax4.text(0.1, 0.5, info_text, fontsize=10, family='monospace', 
         verticalalignment='center', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Plot 5: Titik-titik Evaluasi
ax5 = plt.subplot(2, 3, 5)
colors_points = ['green' if i == 0 or i == n else 'red' if i % 2 == 1 else 'blue' 
                 for i in range(len(x_points))]
labels_points = ['Awal/Akhir (×1)' if i == 0 or i == n else 'Ganjil (×4)' if i % 2 == 1 else 'Genap (×2)' 
                 for i in range(len(x_points))]
scatter = ax5.scatter(x_points, y_points, c=colors_points, s=150, edgecolors='black', linewidths=2, zorder=5)
ax5.plot(x_smooth, y_smooth, 'k-', linewidth=1, alpha=0.3)

# Legend manual
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, 
           markeredgecolor='black', markeredgewidth=2, label='Awal/Akhir (×1)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, 
           markeredgecolor='black', markeredgewidth=2, label='Ganjil (×4)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, 
           markeredgecolor='black', markeredgewidth=2, label='Genap (×2)')
]
ax5.legend(handles=legend_elements, fontsize=9)
ax5.set_xlabel('x', fontsize=12, fontweight='bold')
ax5.set_ylabel('f(x)', fontsize=12, fontweight='bold')
ax5.set_title('Titik Evaluasi dan Koefisien', fontsize=13, fontweight='bold')
ax5.grid(True, alpha=0.3, linestyle='--')

# Plot 6: Tabel Hasil
ax6 = plt.subplot(2, 3, 6)
ax6.axis('off')
table_data = []
for i in range(min(11, len(x_points))):
    koef = 1 if (i == 0 or i == n) else (4 if i % 2 == 1 else 2)
    table_data.append([f'x_{i}', f'{x_points[i]:.2f}', f'{y_points[i]:.4f}', f'{koef}'])

table = ax6.table(cellText=table_data, 
                  colLabels=['Titik', 'x', 'f(x)', 'Koef'],
                  cellLoc='center', loc='center',
                  colWidths=[0.15, 0.2, 0.25, 0.15])
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2)
ax6.set_title(f'Tabel Perhitungan (n={n})', fontsize=13, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('hasil_simpson_integrasi.png', dpi=300, bbox_inches='tight')
print("\n✓ Grafik berhasil disimpan: hasil_simpson_integrasi.png")
plt.show()

print("\n" + "="*70)
print("PROGRAM SELESAI")
print("="*70)
