import warnings
from pathlib import Path

import nrrd
import numpy as np
import tifffile

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import nibabel as nib


def to_nii(img, dest_path, scale=None, affine_transform=None):
    # TODO: see if we want also real units scale

    """
    Write the brain volume to disk as a nifty image.

    Parameters
    ----------
    img : nifty image object or np.ndarray
        A nifty image object or numpy array representing a brain.

    dest_path : str
        The file path where to save the brain.

    scale : tuple of floats, optional
        A tuple of floats to indicate the 'zooms' of the nifty image.

    affine_transform : np.ndarray, optional
        A 4x4 matrix indicating the transform to save in the metadata of the
        image. Required only if not nibabel input.
    """
    dest_path = str(dest_path)
    if affine_transform is None:
        affine_transform = np.eye(4)
    if not isinstance(img, nib.Nifti1Image):
        img = nib.Nifti1Image(img, affine_transform)
    if scale is not None:
        img.header.set_zooms(scale)
    nib.save(img, dest_path)


def to_tiff(img_volume, dest_path, photometric="minisblack"):
    """
    Save the image volume (numpy array) to a tiff stack.

    Parameters
    ----------
    img_volume : np.ndarray
        The image to be saved.

    dest_path : str
        The file path where to save the tiff stack.

    photometric: str
        Color space of image (to pass to tifffile.imwrite)
        Use 'minisblack' (default) for grayscale and 'rgb' for rgb
    """
    dest_path = str(dest_path)
    tifffile.imwrite(dest_path, img_volume, photometric=photometric)


def to_tiffs(img_volume, path_prefix, path_suffix="", extension=".tif"):
    """
    Save the image volume (numpy array) as a sequence of tiff planes.
    Each plane will have a filepath of the following format:
    {path_prefix}_{zeroPaddedIndex}{path_suffix}{extension}

    Parameters
    ----------
    img_volume : np.ndarray
        The image to be saved.

    path_prefix : str
        The prefix for each plane.

    path_suffix : str, optional
        The suffix for each plane.

    extension : str, optional
        The file extension for each plane.
    """
    z_size = img_volume.shape[0]
    pad_width = int(round(z_size / 10)) + 1
    for i in range(z_size):
        img = img_volume[i, :, :]
        dest_path = (
            f"{path_prefix}_{str(i).zfill(pad_width)}{path_suffix}{extension}"
        )
        tifffile.imwrite(dest_path, img)


def to_nrrd(img_volume, dest_path):
    """
    Save the image volume (numpy array) as nrrd.

    Parameters
    ----------
    img_volume : np.ndarray
        The image to be saved.

    dest_path : str
        The file path where to save the nrrd image.
    """
    dest_path = str(dest_path)
    nrrd.write(dest_path, img_volume)


def to_tiffs_with_txt(
    img_volume, txt_path, subdir_name="sub", tiff_prefix="image"
):
    """
    Save the image volume (numpy array) as a sequence of tiff planes, and write
    a text file containing all the tiff file paths in order (one per line).

    The tiff sequence will be saved to a sub-folder inside the same folder
    as the text file.

    Parameters
    ----------
    img_volume : np.ndarray
        The image to be saved.

    txt_path : str or pathlib.Path
        Filepath of text file to create.

    subdir_name : str
        Name of subdirectory where the tiff sequence will be written.

    tiff_prefix : str
        The prefix to each tiff file name e.g. 'image' would give files like
        'image_0.tif', 'image_1.tif'...
    """
    txt_path = Path(txt_path)
    directory = txt_path.parent

    # Write tiff sequence to sub-folder
    sub_dir = directory / subdir_name
    sub_dir.mkdir()
    to_tiffs(img_volume, str(sub_dir / tiff_prefix))

    # Write txt file containing all tiff file paths (one per line)
    tiff_paths = sorted(sub_dir.iterdir())
    txt_path.write_text(
        "\n".join([str(sub_dir / fname) for fname in tiff_paths])
    )


def save_any(img_volume, dest_path):
    """
    Save the image volume (numpy array) to the given file path, using the save
    function matching its file extension.

    Parameters
    ----------
    img_volume : np.ndarray
        The image to be saved.

    dest_path : str or pathlib.Path
        The file path to save the image to.
        Supports directories (will save a sequence of tiffs), .tif, .tiff,
        .nrrd, .nii and .txt (will save a sequence of tiffs and a
        corresponding text file containing their paths).
    """
    dest_path = Path(dest_path)

    if dest_path.is_dir():
        to_tiffs(img_volume, str(dest_path / "image"))

    elif dest_path.suffix == ".txt":
        to_tiffs_with_txt(img_volume, dest_path)

    elif dest_path.suffix == ".tif" or dest_path.suffix == ".tiff":
        to_tiff(img_volume, str(dest_path))

    elif dest_path.suffix == ".nrrd":
        to_nrrd(img_volume, str(dest_path))

    elif dest_path.suffix == ".nii":
        to_nii(img_volume, str(dest_path))

    else:
        raise NotImplementedError(
            f"Could not guess data type for path {dest_path}"
        )
