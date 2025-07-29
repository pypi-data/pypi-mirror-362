import pytest
import numpy as np
from nabu.testutils import get_data

from nabu.cuda.utils import __has_pycuda__
from nabu.reconstruction.mlem import MLEMReconstructor, __have_corrct__


@pytest.fixture(scope="class")
def bootstrap(request):
    cls = request.cls
    datafile = get_data("test_mlem.npz")
    cls.data_wvu = datafile["data_wvu"]
    cls.angles_rad = datafile["angles_rad"]
    cls.pixel_size_cm = datafile["pixel_size"] * 1e4  # pixel_size originally in um
    cls.true_cor = datafile["true_cor"]
    cls.mlem_cor_None_nosh = datafile["mlem_cor_None_nosh"]
    cls.mlem_cor_truecor_nosh = datafile["mlem_cor_truecor_nosh"]
    cls.mlem_cor_truecor_shifts_v0 = datafile["mlem_cor_truecor_shifts_v0"]
    cls.shifts_uv_v0 = datafile["shifts_uv_v0"]
    cls.shifts_uv = datafile["shifts_uv"]

    cls.tol = 1.3e-4


@pytest.mark.skipif(not (__has_pycuda__ and __have_corrct__), reason="Need pycuda and corrct for this test")
@pytest.mark.usefixtures("bootstrap")
class TestMLEMReconstructor:
    """These tests test the general MLEM reconstruction algorithm
    and the behavior of the reconstruction with respect to horizontal shifts.
    Only horizontal shifts are tested here because vertical shifts are handled outside
    the reconstruction object, but in the embedding reconstruction pipeline. See FullFieldReconstructor
    It is compared against a reference reconstruction generated with the `rec_mlem` function
    defined in the `generate_test_data.py` script.
    """

    def _rec_mlem(self, cor, shifts_uv, data_wvu, angles_rad):
        n_angles, n_z, n_x = data_wvu.shape

        mlem = MLEMReconstructor(
            (n_z, n_angles, n_x),
            angles_rad,
            shifts_uv=shifts_uv,
            cor=cor,
            n_iterations=50,
            extra_options={"centered_axis": True, "clip_outer_circle": True, "scale_factor": 1 / self.pixel_size_cm},
        )
        rec_mlem = mlem.reconstruct(data_wvu.swapaxes(0, 1))
        return rec_mlem

    def test_simple_mlem_recons_cor_None_nosh(self):
        slice_index = 25
        rec = self._rec_mlem(None, None, self.data_wvu, self.angles_rad)[slice_index]
        delta = np.abs(rec - self.mlem_cor_None_nosh)
        assert np.max(delta) < self.tol

    def test_simple_mlem_recons_cor_truecor_nosh(self):
        slice_index = 25
        rec = self._rec_mlem(self.true_cor, None, self.data_wvu, self.angles_rad)[slice_index]
        delta = np.abs(rec - self.mlem_cor_truecor_nosh)
        assert np.max(delta) < 2.6e-4

    def test_compare_with_fbp(self):
        from nabu.reconstruction.fbp import Backprojector

        def _rec_fbp(cor, shifts_uv, data_wvu, angles_rad):
            n_angles, n_z, n_x = data_wvu.shape

            if shifts_uv is None:
                fbp = Backprojector(
                    (n_angles, n_x),
                    angles=angles_rad,
                    rot_center=cor,
                    halftomo=False,
                    padding_mode="edges",
                    extra_options={
                        "centered_axis": True,
                        "clip_outer_circle": True,
                        "scale_factor": 1 / self.pixel_size_cm,
                    },
                )
            else:
                fbp = Backprojector(
                    (n_angles, n_x),
                    angles=angles_rad,
                    rot_center=cor,
                    halftomo=False,
                    padding_mode="edges",
                    extra_options={
                        "centered_axis": True,
                        "clip_outer_circle": True,
                        "scale_factor": 1 / self.pixel_size_cm,  # convert um to cm
                        "axis_correction": shifts_uv[:, 0],
                    },
                )

            rec_fbp = np.zeros((n_z, n_x, n_x), "f")
            for i in range(n_z):
                rec_fbp[i] = fbp.fbp(data_wvu[:, i])

            return rec_fbp

        fbp = _rec_fbp(self.true_cor, None, self.data_wvu, self.angles_rad)[25]
        mlem = self._rec_mlem(self.true_cor, None, self.data_wvu, self.angles_rad)[25]
        delta = np.abs(fbp - mlem)
        assert (
            np.max(delta) < 400
        )  # These two should not be really equal. But the test should test that both algo FBP and MLEM behave similarly.

    def test_mlem_zeroshifts_equal_noshifts(self):
        shifts = np.zeros((len(self.angles_rad), 2))
        rec_nosh = self._rec_mlem(self.true_cor, None, self.data_wvu, self.angles_rad)
        rec_zerosh = self._rec_mlem(self.true_cor, shifts, self.data_wvu, self.angles_rad)
        delta = np.abs(rec_nosh - rec_zerosh)
        assert np.max(delta) < self.tol

    def test_mlem_recons_with_u_shifts(self):
        slice_index = 25
        rec = self._rec_mlem(self.true_cor, self.shifts_uv_v0, self.data_wvu, self.angles_rad)[slice_index]
        delta = np.abs(rec - self.mlem_cor_truecor_shifts_v0)
        assert np.max(delta) < self.tol
