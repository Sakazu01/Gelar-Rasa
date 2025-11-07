FMCG Personal Care - Synthetic Dataset (Transactional 1,000,000 rows)
================================================================================
Deskripsi:
Dataset ini mensimulasikan transaksi penjualan kategori Personal Care (FMCG personal care)
periode 2020-01-01 hingga 2025-12-31. Tujuan: inovation radar, trend forecasting,
dan analisis product cannibalization.

File di paket:
- products.csv        : Master produk (product_id, product_name, brand, type, size_ml, base_price, launch_date)
- marketing.csv       : Kampanye pemasaran (campaign_id, product_id, spend, channel, engagement_rate)
- reviews.csv         : Sampel review pelanggan (~10k rows)
- sales.csv           : Transaksi penjualan (~1,000,000 rows) -- kolom-kolom penting ada di bawah.
- README_FMCG_Personal_Care.txt : Dokumen ini.

Spesifikasi file sales.csv (kolom & arti):
- transaction_id : Unique UUID untuk setiap transaksi.
- date           : Tanggal transaksi (YYYY-MM-DD).
- product_id     : Kode produk (PC001 .. PC015).
- region         : Kota/region tempat transaksi (Jakarta, Bandung, ...).
- channel        : Channel penjualan (Shopee, Tokopedia, Official Store, Alfamart, Indomaret, Hypermarket).
- units_sold     : Jumlah unit terjual dalam transaksi tersebut.
- avg_price      : Harga rata-rata per unit setelah diskon (IDR).
- discount_pct   : Persentase diskon yang diberikan pada transaksi.
- revenue        : units_sold * avg_price.
- days_since_launch : Selisih hari antara tanggal transaksi dan tanggal launch produk (negatif jika sebelum launch).

Creator: Shella Theresya Pandiangan
Generated on: 2025-10-23 13:53 UTC
