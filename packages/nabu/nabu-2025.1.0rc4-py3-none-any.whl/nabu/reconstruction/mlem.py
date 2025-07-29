import numpy as np


try:
    import corrct as cct

    __have_corrct__ = True
except ImportError:
    __have_corrct__ = False


class MLEMReconstructor:
    """
    A reconstructor for MLEM reconstruction using the CorrCT toolbox.

    Parameters
    ----------
    data_vwu_shape : tuple
        Shape of the input data, expected to be (n_slices, n_angles, n_dets). Raises an error if the shape is not 3D.
    angles_rad : numpy.ndarray
        Angles in radians for the projections. Must match the second dimension of `data_vwu_shape`.
    shifts_vu : numpy.ndarray, optional.
        Shifts in the v and u directions for each angle. If provided, must have the same number of cols as `angles_rad`. Each col is (tv,tu)
    cor : float, optional
        Center of rotation, which will be adjusted based on the sinogram width.
    n_iterations : int, optional
        Number of iterations for the MLEM algorithm. Default is 50.
    extra_options : dict, optional
        Additional options for the reconstruction process. Default options include:
        - scale_factor (float, default is 1.0): Scale factor for the reconstruction.
        - compute_shifts (boolean, default is False): Whether to compute shifts.
        - tomo_consistency (boolean, default is False): Whether to enforce tomographic consistency.
        - v_min_for_v_shifts (number, default is 0): Minimum value for vertical shifts.
        - v_max_for_v_shifts (number, default is None): Maximum value for vertical shifts.
        - v_min_for_u_shifts (number, default is 0): Minimum value for horizontal shifts.
        - v_max_for_u_shifts (number, default is None): Maximum value for horizontal shifts.
    """

    default_extra_options = {
        "compute_shifts": False,
        "tomo_consistency": False,
        "v_min_for_v_shifts": 0,
        "v_max_for_v_shifts": None,
        "v_min_for_u_shifts": 0,
        "v_max_for_u_shifts": None,
        "scale_factor": 1.0,
        "centered_axis": False,
        "clip_outer_circle": False,
        "outer_circle_value": 0.0,
        "filter_cutoff": 1.0,
        "padding_mode": None,
        "crop_filtered_data": True,
    }

    def __init__(
        self,
        data_vwu_shape,
        angles_rad,
        shifts_uv=None,
        cor=None,  # absolute
        n_iterations=50,
        extra_options=None,
    ):
        if not (__have_corrct__):
            raise ImportError("Need corrct package")
        self.angles_rad = angles_rad
        self.n_iterations = n_iterations
        self.scale_factor = extra_options.get("scale_factor", 1.0)

        self._configure_extra_options(extra_options)
        self._set_sino_shape(data_vwu_shape)
        self._set_shifts(shifts_uv, cor)

    def _configure_extra_options(self, extra_options):
        self.extra_options = self.default_extra_options.copy()
        self.extra_options.update(extra_options or {})

    def _set_sino_shape(self, sinos_shape):
        if len(sinos_shape) != 3:
            raise ValueError("Expected a 3D shape")
        self.sinos_shape = sinos_shape
        self.n_sinos, self.n_angles, self.prj_width = sinos_shape
        if self.n_angles != len(self.angles_rad):
            raise ValueError(
                f"Number of angles ({len(self.angles_rad)}) does not match size of sinograms ({self.n_angles})."
            )

    def _set_shifts(self, shifts_uv, cor):
        if shifts_uv is None:
            self.shifts_vu = None
        else:
            if shifts_uv.shape[0] != self.n_angles:
                raise ValueError(
                    f"Number of shifts given ({shifts_uv.shape[0]}) does not mathc the number of projections ({self.n_angles})."
                )
            self.shifts_vu = -shifts_uv.copy().T[::-1]
        if cor is None:
            self.cor = 0.0
        else:
            self.cor = (
                -cor + (self.sinos_shape[-1] - 1) / 2.0
            )  # convert absolute to relative in the ASTRA convention, which is opposite to Nabu relative convention.

    def reset_rot_center(self, cor):
        self.cor = -cor + (self.sinos_shape[-1] - 1) / 2.0

    def reconstruct(self, data_vwu):
        """
        data_align_vwu: numpy.ndarray or pycuda.gpuarray
            Raw data, with shape (n_sinograms, n_angles, width)
        output: optional
            Output array. If not provided, a new numpy array is returned
        """
        if not isinstance(data_vwu, np.ndarray):
            data_vwu = data_vwu.get()
        # data_vwu /= data_vwu.mean()

        # MLEM recons
        self.vol_geom_align = cct.models.VolumeGeometry.get_default_from_data(data_vwu)
        if self.shifts_vu is not None:
            self.prj_geom_align = cct.models.ProjectionGeometry.get_default_parallel()
            # Vertical shifts were handled in pipeline. Set them to ZERO
            self.shifts_vu[:, 0] = 0.0
            self.prj_geom_align.set_detector_shifts_vu(self.shifts_vu, self.cor)
        else:
            self.prj_geom_align = None

        variances_align = cct.processing.compute_variance_poisson(data_vwu)
        self.weights_align = cct.processing.compute_variance_weight(variances_align, normalized=True)  # , use_std=True
        self.data_term_align = cct.data_terms.DataFidelity_wl2(self.weights_align)
        solver = cct.solvers.MLEM(verbose=True, data_term=self.data_term_align)
        self.solver_opts = dict(lower_limit=0)  # , x_mask=cct.processing.circular_mask(vol_geom_align.shape_xyz[:-2])

        with cct.projectors.ProjectorUncorrected(
            self.vol_geom_align, self.angles_rad, rot_axis_shift_pix=self.cor, prj_geom=self.prj_geom_align
        ) as A:
            rec, _ = solver(A, data_vwu, iterations=self.n_iterations, **self.solver_opts)
        return rec * self.scale_factor
