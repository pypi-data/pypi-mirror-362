import unittest
import numpy as np
from AMBER.background import background


class TestBackground(unittest.TestCase):
    def setUp(self):
        """Set up mock data for testing."""
        self.bg = background(dtype=np.float32)
        self.bg.set_gridcell_size(dqx=0.03, dqy=0.03, dE=0.1)
        Qx = np.linspace(-1, 1, 10)
        Qy = np.linspace(-1, 1, 10)
        E = np.linspace(0, 1, 5)
        Int = np.random.rand(len(Qx), len(Qy), len(E))
        self.bg.set_binned_data(Qx, Qy, E, Int)
        self.bg.set_radial_bins(max_radius=3.0, n_bins=100)

    def test_cross_validation(self):
        """Test the cross_validation method."""
        q = 0.75
        beta_range = np.array([1.0, 2.0])
        lambda_ = 0.01
        mu_ = 0.001
        n_epochs = 5
        rmse = self.bg.cross_validation(q, beta_range, lambda_, mu_, n_epochs, verbose=False)
        self.assertEqual(len(rmse), len(beta_range))
        self.assertTrue(np.all(rmse >= 0))

    def test_set_gridcell_size(self):
        """Test set_gridcell_size method."""
        self.bg.set_gridcell_size(dqx=0.05, dqy=0.05, dE=0.2)
        self.assertEqual(self.bg.dqx, 0.05)
        self.assertEqual(self.bg.dqy, 0.05)
        self.assertEqual(self.bg.dE, 0.2)

    def test_set_binned_data(self):
        """Test set_binned_data method."""
        Qx = np.linspace(-2, 2, 20)
        Qy = np.linspace(-2, 2, 20)
        E = np.linspace(0, 2, 10)
        Int = np.random.rand(len(Qx), len(Qy), len(E))
        self.bg.set_binned_data(Qx, Qy, E, Int)
        self.assertEqual(self.bg.Qx_size, len(Qx))
        self.assertEqual(self.bg.Qy_size, len(Qy))
        self.assertEqual(self.bg.E_size, len(E))

    def test_set_radial_bins(self):
        """Test set_radial_bins method."""
        self.bg.set_radial_bins(max_radius=5.0, n_bins=50)
        self.assertEqual(self.bg.max_radius, 5.0)
        self.assertEqual(self.bg.n_bins, 50)
        self.assertEqual(len(self.bg.r_range), 51)

    def test_R_operator(self):
        """Test R_operator method."""
        b = np.random.rand(self.bg.E_size, self.bg.n_bins)
        b_grid = self.bg.R_operator(b)
        self.assertEqual(b_grid.shape, (self.bg.E_size, self.bg.Qx_size * self.bg.Qy_size))

    def test_Rstar_operator(self):
        """Test Rstar_operator method."""
        X = np.random.rand(self.bg.E_size, self.bg.Qx_size * self.bg.Qy_size)
        v_agg = self.bg.Rstar_operator(X)
        self.assertEqual(v_agg.shape, (self.bg.E_size, self.bg.n_bins))

    def test_gamma_matrix(self):
        """Test gamma_matrix method."""
        gamma_mat = self.bg.gamma_matrix()
        self.assertEqual(gamma_mat.shape, (self.bg.n_bins, self.bg.n_bins))

    def test_mask_nans(self):
        """Test mask_nans method."""
        x = np.random.rand(self.bg.E_size, self.bg.Qx_size * self.bg.Qy_size)
        x[0, 0] = np.nan
        masked_x = self.bg.mask_nans(x)
        self.assertTrue(np.isnan(masked_x[0, 0]))

    def test_S_lambda(self):
        """Test S_lambda method."""
        x = np.array([1.0, -2.0, 0.5])
        lambda_ = 1.0
        result = self.bg.S_lambda(x, lambda_)
        expected = np.array([0.0, -1.0, 0.0])
        np.testing.assert_array_almost_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
