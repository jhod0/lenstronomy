__author__ = 'sibirrer'


from lenstronomy.LensModel.Profiles.coreBurkert import coreBurkert

import numpy as np
import numpy.testing as npt
import pytest

class TestcBurk(object):
    """
    tests the Gaussian methods
    """
    def setup(self):

        self.cb = coreBurkert()

    def _kappa_integrand(self, x, y, Rs, m0, r_core):

        return 2*np.pi*x * self.cb.density_2d(x, y, Rs, m0, r_core)

    def test_mproj(self):

        Rs = 10
        r_core = 0.7*Rs
        Rmax = np.linspace(0.5*Rs, 1.5*Rs, 1000000)
        dr = Rmax[1] - Rmax[0]
        m0 = 1

        m2d = self.cb.mass_2d(Rmax, Rs, m0, r_core)
        integrand = np.gradient(m2d, dr)
        kappa_integrand = self._kappa_integrand(Rmax, 0, Rs, m0, r_core)
        npt.assert_almost_equal(integrand, kappa_integrand, decimal=3)

    def test_potential(self):

        Rs = 10
        rho0 = 1
        r_core = 0.6*Rs
        R = np.linspace(0.1*Rs, 2*Rs, 1000000)
        potential = self.cb.function(R, 0, Rs, rho0, r_core)
        alpha_num = np.gradient(potential, R[1] - R[0])
        alpha = self.cb.derivatives(R, 0, Rs, rho0, r_core)[0]
        npt.assert_almost_equal(alpha_num, alpha, decimal=4)

    def test_derivatives(self):

        Rs = 10
        rho0 = 1
        r_core = 7

        R = np.linspace(0.1*Rs, 4*Rs, 1000)

        alpha = self.cb.coreBurkAlpha(R, Rs, rho0, r_core, R, 0)[0]

        alpha_theory = self.cb.mass_2d(R, Rs, rho0, r_core) / np.pi / R

        npt.assert_almost_equal(alpha/alpha_theory, 1)

if __name__ == '__main__':
    pytest.main()