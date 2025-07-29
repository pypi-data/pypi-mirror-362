from os import path

from ..resources.nxflatfield import update_dataset_info_flats_darks
from ..resources.logger import LoggerOrPrint
from ..resources.dataset_analyzer import analyze_dataset
from ..pipeline.config_validators import convert_to_bool
from ..pipeline.estimators import TranslationsEstimator
from .utils import parse_params_values
from .cli_configs import EstimateMotionConfig


def estimate_motion():
    args = parse_params_values(
        EstimateMotionConfig,
        parser_description="Estimate sample motion and generate 'translation_movements_file' for nabu config file. ",
    )
    try:
        rot_center = float(args["rot_center"])
    except (ValueError, TypeError):
        rot_center = None

    logger = LoggerOrPrint(None)
    dataset_info = analyze_dataset(args["dataset"], logger=logger)
    do_ff = args["flatfield"]

    if do_ff:
        update_dataset_info_flats_darks(dataset_info, True, loading_mode="load_if_present")

    est = TranslationsEstimator(
        dataset_info,
        do_flatfield=do_ff,
        rot_center=rot_center,
        angular_subsampling=args["subsampling"],
        deg_xy=args["deg_xy"],
        deg_z=args["deg_z"],
        shifts_estimator="phase_cross_correlation",
    )

    estimated_shifts_h, estimated_shifts_v, cor = est.estimate_motion()
    if convert_to_bool(args["verbose"]):
        err_vu = est.motion_estimator.get_max_fit_error(cor=rot_center)
        logger.info("Max fit error in 'u': %.2f pix \t\t Max fit error in 'v': %.2f pix" % (err_vu[1], err_vu[0]))
        est.motion_estimator.plot_detector_shifts(cor=rot_center)
        est.motion_estimator.plot_movements(cor=rot_center, angles_rad=dataset_info.rotation_angles)

    out_file = args["output_file"]
    est.generate_translations_movements_file(filename=out_file, only=args["only"] or None)
    logger.info(
        f"Wrote {out_file} - use 'translation_movements_file = {path.abspath(out_file)}' in nabu configuration file to correct for sample movements in the reconstruction'"
    )


if __name__ == "__main__":
    estimate_motion()
