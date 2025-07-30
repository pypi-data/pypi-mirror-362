import logging
from argparse import ArgumentParser

import SimpleITK as sitk

from . import __version__
from .thickness import compute_thickness_cardiac


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    parser = ArgumentParser()

    parser.add_argument("endo")
    parser.add_argument("epi")
    parser.add_argument("output")
    parser.add_argument("--weights", "-w")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s version {__version__}"
    )
    args = parser.parse_args()

    print("Reading images")
    endo_sitk = sitk.ReadImage(args.endo)
    epi_sitk = sitk.ReadImage(args.epi)
    if args.weights:
        weights = sitk.GetArrayFromImage(sitk.ReadImage(args.weights))
    else:
        weights = None

    endo = sitk.GetArrayFromImage(endo_sitk).astype(bool)
    epi = sitk.GetArrayFromImage(epi_sitk).astype(bool)

    thickness = compute_thickness_cardiac(
        endo,
        epi,
        endo_sitk.GetSpacing()[::-1],  # type:ignore
        weights,
    )

    thickness_sitk = sitk.GetImageFromArray(thickness)
    thickness_sitk.CopyInformation(endo_sitk)  # type:ignore

    print("Writing result")
    sitk.WriteImage(thickness_sitk, args.output, True)


if __name__ == "__main__":
    main()
