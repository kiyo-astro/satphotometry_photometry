# satphotometry_photometry

Jupyter notebooks for optical photometry of artificial satellites and
debris, developed by Kyushu University Hanada Lab (SSDL) / University of
Washington / IAU CPS SatHub.

## Notebooks

| Notebook | Purpose |
| --- | --- |
| `SER2FITS.ipynb` | Export one frame of a SharpCap SER video as FITS (CameraSettings metadata is written to the header). |
| `magzero.ipynb` | Plate-solve one frame with astrometry.net and measure the photometric zeropoint (ZP, ZP_exp, ZP_elec) from catalogue stars. |
| `LEO_photometry.ipynb` | Light curve of a bright LEO object from a directory of FITS frames (automatic detection and tracking). |
| `LEO_photometry_single.ipynb` | Single-frame version of the LEO measurement. |
| `GEO_photometry_satTrack.ipynb` | GEO light curve from satellite-tracking data (per-frame plate solve, WCS-aligned field-star subtraction). |
| `GEO_photometry_satTrack_integrated.ipynb` | Satellite-tracking GEO pipeline with automatic target detection (median of sampled frames, persistence ranking), an optional operator review gate, plate solving of star-aligned stacks on the raw frames, an integrated field-star zeropoint, dark/flat calibration after astrometry, and per-frame re-centring. |
| `GEO_photometry_starTrack.ipynb` | GEO light curve from sidereal-tracking data (WCS registration, median field-star subtraction, two-anchor target interpolation). |
| `lightcurve_viewer.ipynb` | KUPT-lightcurveJSON viewer: light curve, Lomb-Scargle periodogram, phase folding, publication figures. |
| `airmass.ipynb` | Atmospheric transmission from zeropoints measured at several altitudes. |

Typical flow: `SER2FITS` → `magzero` → one of the `*_photometry` notebooks →
`lightcurve_viewer`.

## Requirements

* Python 3.11 or later with `numpy`, `scipy`, `astropy`, `photutils`,
  `matplotlib`, `pandas`, `reproject`, `tqdm`, `opencv-python-headless`,
  `jupyterlab` (or `nbconvert` for headless runs)
* [satphotometry](https://github.com/kiyo-astro/satphotometry) library
  (`astrometry` and `serparser` modules) importable from the kernel
* [astrometry.net](https://astrometry.net/) `solve-field` with index files
  (the 5200 series is used at KUBO/KUPT)

## Path settings

Machine-specific locations are kept out of the notebooks. Copy
`paths.example.json` to `paths.json` next to the notebooks and edit it:

```json
{
    "images": "/path/to/observation/images",
    "input": "input",
    "output": "output",
    "work": "output",
    "solve_field_dir": "~/astrometry/bin"
}
```

| Key | Meaning |
| --- | --- |
| `images` | Root of raw captures (SER / FITS). Notebook settings refer to files relative to this root. |
| `input` | Small input files kept with the project. |
| `output` | Products: `magzero/`, `lightcurve/`, `lightcurve_analysis/`, `airmass/`, `astrometry/`. |
| `work` | Large intermediate FITS directories written by the GEO pipelines. |
| `solve_field_dir` | Directory containing `solve-field` when it is not on `PATH`. |

Relative paths are resolved against the notebook folder. Environment
variables `SATPHOT_IMAGES`, `SATPHOT_INPUT`, `SATPHOT_OUTPUT`, `SATPHOT_WORK`
and `SATPHOT_SOLVE_FIELD_DIR` override `paths.json`. `paths.json`, `input/`,
`output/` and `work/` are ignored by git.

Each notebook starts with `from satphot_paths import *`, which provides
`PATH_images`, `PATH_input`, `PATH_output` and `PATH_work`; the target
files for a run are then given relative to those roots in the settings cells.

## Integrated satellite-tracking pipeline

`GEO_photometry_satTrack_integrated.ipynb` runs in two stages. Stage 1 converts
the SER file, builds a detection image (median of frames sampled over the
capture: field stars drift out, the tracked object stays), lists ranked
candidates and saves a review figure under `output/review/`. Stage 2 locates
the target in every frame, estimates the star drift, plate-solves star-aligned
stacks of the raw frames (clean star lists are sent to `solve-field`, with
the telescope position from the SharpCap CameraSettings file as the hint),
interpolates a WCS for every frame, applies dark/flat to calibrated copies,
measures the zeropoint on calibrated stacks, subtracts the field stars and
performs the photometry.

Environment variables for unattended runs:

| Variable | Meaning |
| --- | --- |
| `SATPHOT_STAGE` | `all` (default), `1` or `2` (stage 2 reloads the stage-1 state) |
| `SATPHOT_REQUIRE_CONFIRMATION` | `0` disables the operator review gate |
| `SATPHOT_TARGET_APPROVED` | `1` approves the detected candidate after reviewing the figure |

SharpCap stores 8-bit master darks/flats as 16-bit values (x256); the
notebook detects this and scales the master dark.

## Headless execution

```bash
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=-1 \
    --output executed_magzero.ipynb magzero.ipynb
```

## License

See `LICENSE`.
