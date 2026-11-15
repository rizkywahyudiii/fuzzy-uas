import unittest
from dasar import validasi_input, fuzzifikasi, aktivasi_aturan
from mamdani import mamdani
from sugeno import sugeno
from tsukamoto import tsukamoto


class TestDasar(unittest.TestCase):
    """Pengujian independen modul dasar.py (validasi, fuzzifikasi, aturan)."""

    def test_validasi_input_normal(self):
        t, h = validasi_input(28, 55)
        self.assertEqual(t, 28.0)
        self.assertEqual(h, 55.0)

    def test_validasi_input_format_string_dan_koma(self):
        t, h = validasi_input(" 25,5 ", "60.5")
        self.assertAlmostEqual(t, 25.5)
        self.assertAlmostEqual(h, 60.5)

    def test_validasi_input_batas(self):
        # Batas bawah
        t_min, h_min = validasi_input(20, 40)
        self.assertEqual(t_min, 20.0)
        self.assertEqual(h_min, 40.0)
        # Batas atas
        t_max, h_max = validasi_input(40, 80)
        self.assertEqual(t_max, 40.0)
        self.assertEqual(h_max, 80.0)

    def test_validasi_input_di_luar_rentang(self):
        with self.assertRaises(ValueError):
            validasi_input(19.9, 60)
        with self.assertRaises(ValueError):
            validasi_input(40.1, 60)
        with self.assertRaises(ValueError):
            validasi_input(30, 39.9)
        with self.assertRaises(ValueError):
            validasi_input(30, 80.1)

    def test_validasi_input_non_numerik(self):
        with self.assertRaises(ValueError):
            validasi_input("panas", 60)
        with self.assertRaises(ValueError):
            validasi_input(30, "lembab")

    def test_fuzzifikasi_simetris(self):
        mu = fuzzifikasi(30, 60)
        self.assertAlmostEqual(mu["T_rendah"], 0.5)
        self.assertAlmostEqual(mu["T_tinggi"], 0.5)
        self.assertAlmostEqual(mu["H_rendah"], 0.5)
        self.assertAlmostEqual(mu["H_tinggi"], 0.5)

    def test_fuzzifikasi_ekstrim(self):
        mu_min = fuzzifikasi(20, 40)
        self.assertAlmostEqual(mu_min["T_rendah"], 1.0)
        self.assertAlmostEqual(mu_min["T_tinggi"], 0.0)
        self.assertAlmostEqual(mu_min["H_rendah"], 1.0)
        self.assertAlmostEqual(mu_min["H_tinggi"], 0.0)

        mu_max = fuzzifikasi(40, 80)
        self.assertAlmostEqual(mu_max["T_rendah"], 0.0)
        self.assertAlmostEqual(mu_max["T_tinggi"], 1.0)
        self.assertAlmostEqual(mu_max["H_rendah"], 0.0)
        self.assertAlmostEqual(mu_max["H_tinggi"], 1.0)

    def test_aktivasi_aturan(self):
        mu = {"T_rendah": 0.8, "T_tinggi": 0.2, "H_rendah": 0.7, "H_tinggi": 0.3}
        alpha = aktivasi_aturan(mu)
        # R1: min(0.8, 0.7) = 0.7
        # R2: min(0.8, 0.3) = 0.3
        # R3: min(0.2, 0.7) = 0.2
        # R4: min(0.2, 0.3) = 0.2
        self.assertEqual(alpha, [0.7, 0.3, 0.2, 0.2])


class TestMamdani(unittest.TestCase):
    """Pengujian independen modul mamdani.py."""

    def test_alpha_kosong(self):
        self.assertIsNone(mamdani([0, 0, 0, 0]))

    def test_kondisi_simetris(self):
        # Pada alpha simetris, centroid harus tepat di titik tengah (1000 RPM)
        hasil = mamdani([0.5, 0.5, 0.5, 0.5])
        self.assertAlmostEqual(hasil, 1000.0, places=1)

    def test_kondisi_dominan_lambat(self):
        hasil = mamdani([1.0, 0.0, 0.0, 0.0])
        self.assertLess(hasil, 1000.0)
        self.assertAlmostEqual(hasil, 833.0, places=0)

    def test_kondisi_dominan_cepat(self):
        hasil = mamdani([0.0, 0.0, 0.0, 1.0])
        self.assertGreater(hasil, 1000.0)
        self.assertAlmostEqual(hasil, 1167.0, places=0)


class TestSugeno(unittest.TestCase):
    """Pengujian independen modul sugeno.py."""

    def test_alpha_kosong(self):
        self.assertIsNone(sugeno([0, 0, 0, 0]))

    def test_kondisi_simetris(self):
        hasil = sugeno([0.5, 0.5, 0.5, 0.5])
        self.assertAlmostEqual(hasil, 1000.0)

    def test_kondisi_ekstrim(self):
        # Hanya R1 aktif -> 500 RPM
        self.assertAlmostEqual(sugeno([1.0, 0.0, 0.0, 0.0]), 500.0)
        # Hanya R4 aktif -> 1500 RPM
        self.assertAlmostEqual(sugeno([0.0, 0.0, 0.0, 1.0]), 1500.0)


class TestTsukamoto(unittest.TestCase):
    """Pengujian independen modul tsukamoto.py."""

    def test_alpha_kosong(self):
        self.assertIsNone(tsukamoto([0, 0, 0, 0]))

    def test_kondisi_simetris(self):
        hasil = tsukamoto([0.5, 0.5, 0.5, 0.5])
        self.assertAlmostEqual(hasil, 1000.0)

    def test_kondisi_ekstrim(self):
        # R1: z1 = 1500 - 1000(1) = 500
        self.assertAlmostEqual(tsukamoto([1.0, 0.0, 0.0, 0.0]), 500.0)
        # R4: z4 = 500 + 1000(1) = 1500
        self.assertAlmostEqual(tsukamoto([0.0, 0.0, 0.0, 1.0]), 1500.0)


class TestKonsistensiSistem(unittest.TestCase):
    """Pengujian konsistensi dan determinisme keseluruhan sistem."""

    def test_konsistensi_output_berulang(self):
        alpha = aktivasi_aturan(fuzzifikasi(33, 65))
        m1 = mamdani(alpha)
        m2 = mamdani(alpha)
        s1 = sugeno(alpha)
        s2 = sugeno(alpha)
        t1 = tsukamoto(alpha)
        t2 = tsukamoto(alpha)
        self.assertEqual(m1, m2)
        self.assertEqual(s1, s2)
        self.assertEqual(t1, t2)


if __name__ == "__main__":
    unittest.main()
