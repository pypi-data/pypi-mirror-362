import os
import warnings

# Check if the excel2img package is available _export_img means its private
try:
    from excel2img import export_img as _export_img
except ImportError:
    _export_img = None


def make_excel_img(file, output_folder, sheetname, range, extension="png"):
    """
    ==============================
    Excel Image Generation Utility
    ==============================

    This function generates an image from a specified range in an Excel sheet and saves it to the output folder.

    :param file: The path to the Excel file.
    :type file: str

    :param output_folder: The folder where the output image will be saved.
    :type output_folder: str

    :param sheetname: The name of the sheet in the Excel file.
    :type sheetname: str

    :param range: The range in the sheet to be converted to an image.
    :type range: str

    :param extension: The file extension for the output image (options: "png", "gif", "bmp").
    :type extension: str

    :returns: None

    **Example Usage**
    -----------------
    .. code-block:: python
        make_excel_img('data.xlsx', 'output', 'Sheet1', 'A1:D10', extension='png')

    **Requirements**
    ----------------
    `pip install excel2img`

    **See Also**
    ------------
    - `excel2img <https://pypi.org/project/excel2img/>`_
    """
    if extension not in ["png", "gif", "bmp"]:
        raise ValueError("Invalid extension. Supported extensions are: 'png', 'gif', 'bmp'.")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    # Absolute file path
    file_path = os.path.abspath(file)

    # Define the output image path (same folder as Excel file)
    output = output_folder + "/" + file_path.rsplit("\\", 1)[1].rsplit(".", 1)[0] + "_image." + extension

    # Clear the output if it already exists
    if os.path.exists(output):
        os.remove(output)

    if _export_img is None:
        warnings.warn(
            "excel2img is not installed. Install it with `pip install excel2img` to use this feature.",
            category=UserWarning,
            stacklevel=2,
        )
        return  # Optionally, handle the missing function gracefully

    # Proceed with the function if excel2img is available
    _export_img(file_path, output, sheetname, range)
