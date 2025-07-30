import chart_studio
from chart_studio.utils import validate_fid, parse_file_id_args, ensure_path_exists
from chart_studio.api import v2
from io import BytesIO
from _plotly_utils.optional_imports import get_module


class ext_file_ops:
    """
    A class to handle external file operations.
    """

    @classmethod
    def download(cls, url_or_fid):
        """
        Download an external file from Figlinq.
        :param (str) url_or_fid: The file ID or URL of the file to download.
        :return: The downloaded file content as file-like object.
        """

        if validate_fid(url_or_fid):
            fid = url_or_fid
        else:
            fid = parse_file_id_args(None, url_or_fid)

        response = v2.external_files.content(fid)
        return BytesIO(response.content)

    @classmethod
    def upload(cls, file, filename=None, world_readable="false", return_type="url"):

        parent_path = None
        if filename:
            filename, new_parent_path = ensure_path_exists(filename)
            if new_parent_path:
                parent_path = new_parent_path

        response = v2.external_files.create(
            file, filename, parent_path=parent_path, world_readable=world_readable
        )

        file = response["file"]
        if return_type == "url":
            return file["web_url"]
        elif return_type == "fid":
            return file["fid"]
        return file


class ext_images_ops:
    """
    A class to handle external image operations.
    """

    @classmethod
    def download(cls, url_or_fid):
        """
        Download an external image from Figlinq.
        :param (str) url_or_fid: The file ID or URL of the file to download.
        :return: The downloaded file content as file-like object.
        """

        if validate_fid(url_or_fid):
            fid = url_or_fid
        else:
            fid = parse_file_id_args(None, url_or_fid)

        response = v2.external_images.content(fid)
        return BytesIO(response.content)

    @classmethod
    def upload(
        cls,
        file,
        filename=None,
        world_readable="false",
        return_type="url",
        is_figure=False,
    ):

        parent_path = None
        filename, new_parent_path = ensure_path_exists(filename)
        if new_parent_path:
            parent_path = new_parent_path

        response = v2.external_images.create(
            file,
            filename,
            parent_path=parent_path,
            world_readable=world_readable,
            is_figure=is_figure,
        )

        file = response["file"]
        if return_type == "url":
            return file["web_url"]
        elif return_type == "fid":
            return file["fid"]
        return file


class html_text_ops:
    """
    A class to handle HTML text operations.
    """

    @classmethod
    def download(cls, url_or_fid):
        """
        Download an HTML text from Figlinq.
        :param (str) url_or_fid: The file ID or URL of the file to download.
        :return: The downloaded file content as file-like object.
        """

        if validate_fid(url_or_fid):
            fid = url_or_fid
        else:
            fid = parse_file_id_args(None, url_or_fid)

        response = v2.html_text.content(fid)
        parsed_content = response.json()
        return BytesIO(parsed_content["content"].encode("utf-8"))

    @classmethod
    def upload(
        cls,
        file,
        filename=None,
        world_readable="false",
        return_type="url",
        category="text",
    ):
        parent_path = None
        filename, new_parent_path = ensure_path_exists(filename)
        if new_parent_path:
            parent_path = new_parent_path

        response = v2.html_text.create(
            file,
            filename,
            parent_path=parent_path,
            world_readable=world_readable,
            category=category,
        )

        file = response["file"]
        if return_type == "url":
            return file["web_url"]
        elif return_type == "fid":
            return file["fid"]
        return file


class jupyter_notebook_ops:
    """
    A class to handle Jupyter notebook operations.
    """

    @classmethod
    def download(cls, url_or_fid):
        """
        Download a Jupyter notebook from Figlinq.
        :param (str) url_or_fid: The file ID or URL of the file to download.
        :return: The downloaded file content as file-like object.
        """

        if validate_fid(url_or_fid):
            fid = url_or_fid
        else:
            fid = parse_file_id_args(None, url_or_fid)

        response = v2.jupyter_notebooks.content(fid)
        parsed_content = response.json()
        return parsed_content

    @classmethod
    def upload(
        cls,
        file,
        filename=None,
        world_readable="false",
        return_type="url",
    ):

        parent_path = None
        filename, new_parent_path = ensure_path_exists(filename)
        if new_parent_path:
            parent_path = new_parent_path

        response = v2.jupyter_notebooks.create(
            file, filename, parent_path=parent_path, world_readable=world_readable
        )

        file = response["file"]
        if return_type == "url":
            return file["web_url"]
        elif return_type == "fid":
            return file["fid"]
        return file


def upload(
    file,
    filetype,
    filename=None,
    world_readable=False,
    return_type="url",
    **kwargs,
):
    """
    Upload an file to Figlinq. A wrapper around the Plotly API v2 upload functions for all file types.

    :param (file) file: The file to upload. This can be a file-like object
    (e.g., open(...), Grid, JSON or BytesIO).
    :param (str) filetype: The type of the file being uploaded. This can be "plot", "grid", "image", "figure", "notebook", "html_text", "other"
    :param (str) filename: The name of the file to upload.
    :param (bool) world_readable: If True, the file will be publicly accessible.
    :param (str) return_type: The type of response to return.
    Can be "url" or "fid". If "url", the URL of the uploaded file will be returned.
    If "fid", the file ID will be returned.
    :return: The URL or file ID of the uploaded file, depending on the return_type.
    """

    world_readable_header = "true" if world_readable else "false"

    if filetype not in [
        "plot",
        "grid",
        "image",
        "figure",
        "jupyter_notebook",
        "html_text",
        "external_file",
    ]:
        raise ValueError(
            "Invalid filetype. Must be one of: 'plot', 'grid', 'image', 'figure', 'jupyter_notebook', 'html_text', 'external_file'."
        )
    if filetype == "plot":
        return chart_studio.plotly.plot(
            file,
            filename=filename,
            world_readable=world_readable,
            return_type=return_type,
            auto_open=False,
            **kwargs,
        )
    elif filetype == "grid":
        pd = get_module("pandas")

        if pd and isinstance(file, pd.DataFrame):
            file = chart_studio.grid_objs.Grid(file)
        elif isinstance(file, chart_studio.grid_objs.Grid):
            file = file        
        else:
            raise ValueError("Invalid file type for grid upload. Must be Grid or DataFrame.")
        
        return chart_studio.plotly.plotly.grid_ops.upload(
            file,
            filename=filename,
            world_readable=world_readable,
            return_type=return_type,
            **kwargs,
        )
    elif filetype == "image":
        return ext_images_ops.upload(
            file,
            filename=filename,
            world_readable=world_readable_header,
            return_type=return_type,
            **kwargs,
        )
    elif filetype == "figure":
        return ext_images_ops.upload(
            file,
            filename=filename,
            world_readable=world_readable_header,
            return_type=return_type,
            is_figure=True,
        )
    elif filetype == "jupyter_notebook":
        return jupyter_notebook_ops.upload(
            file,
            filename=filename,
            world_readable=world_readable_header,
            return_type=return_type,
        )
    elif filetype == "html_text":
        return html_text_ops.upload(
            file,
            filename=filename,
            world_readable=world_readable_header,
            return_type=return_type,
        )
    elif filetype == "external_file":
        return ext_file_ops.upload(
            file,
            filename=filename,
            world_readable=world_readable_header,
            return_type=return_type,
        )


def download(fid_or_url, raw=False):
    """
    Download a file from Figlinq.

    :param (str) fid_or_url: The file ID or URL of the file to download.
    :param (bool) raw: If True, return the raw content of the file.
    :return: The downloaded file content or a Grid instance.
    """

    # Check if is fid or url
    if validate_fid(fid_or_url):
        fid = fid_or_url
    else:
        fid = parse_file_id_args(None, fid_or_url)

    # Get the file object first to determine the filetype
    response = v2.files.retrieve(fid)
    file_obj = response.json()
    file_type = file_obj["filetype"]

    if file_type == "grid":  # Returns Grid object
        grid = chart_studio.plotly.plotly.get_grid(fid_or_url, raw=raw)
        grid = Grid(grid)
        if raw:
            return _coerce_raw_grid_numbers(grid)
        else:
            return _coerce_grid_numbers(grid)
    elif file_type == "plot":  # Returns Plotly figure object
        split_fid = fid.split(":")
        owner = split_fid[0]
        idlocal = int(split_fid[1])
        return chart_studio.plotly.plotly.get_figure(owner, idlocal, raw=raw)
    elif file_type == "external_image":  # Returns BytesIO object
        return ext_images_ops.download(fid_or_url)
    elif file_type == "jupyter_notebook":  # Returns JSON object
        return jupyter_notebook_ops.download(fid_or_url)
    elif file_type == "html_text":  # Returns BytesIO object
        return html_text_ops.download(fid_or_url)
    elif file_type == "external_file":  # Returns BytesIO object
        return ext_file_ops.download(fid_or_url)
    else:
        raise ValueError(
            "Invalid filetype. Must be one of: 'plot', 'grid', 'image', 'jupyter_notebook', 'html_text', 'external_file'."
        )


def get_plot_template(template_name):
    """
    Get the plot template for the current user.

    :return: The plot template as a dictionary.
    """

    return chart_studio.tools.get_template(template_name)


def apply_plot_template(fig, template_name):
    """
    Apply the plot template to a Plotly figure.

    :param fig: The Plotly figure to apply the template to.
    :param template_name: The name of the template to apply.
    :return: The modified Plotly figure.
    """

    template = get_plot_template(template_name)
    fig.update_layout(template["layout"])
    return fig


def _coerce_grid_numbers(grid):
    """
    Coerce numbers in the grid to their appropriate types.
    :param grid: The grid to coerce numbers in. Plotly Grid object.
    :return: The modified grid with coerced numbers. Plotly Grid object.
    """
    for col in grid:
        col.data = [_coerce_number_or_keep(s) for s in col.data]
    return grid


def _coerce_raw_grid_numbers(grid):
    """
    e.g. {'cols': {'time': {'data': ['1', '2', '3'], 'order': 0, 'uid': '188549'}, 'voltage': {'data': [4, 2, 5], 'order': 1, 'uid': '4b9e4d'}}}

    Coerce numbers in the grid to their appropriate types.
    :param grid: The grid to coerce numbers in.
    :return: The modified grid with coerced numbers.
    """

    for col, meta in grid.get("cols", {}).items():
        meta["data"] = [_coerce_number_or_keep(x) for x in meta.get("data", [])]

    return grid


def _coerce_number_or_keep(s):
    if not isinstance(s, str):
        return s  # Pass through non-strings unchanged
    s = s.strip().replace(",", "")  # handle commas
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return s


# def get_svg_node_string(fid, filetype, x, y, width, height):

#     fid_split = fid.split(":")
#     owner = fid_split[0]
#     idlocal = int(fid_split[1])
#     url_part = f"~{owner}/{idlocal}"
#     svg_id = f"svg_{fid}"
#     return f"""<image xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none" id="{svg_id}" class="fq-{filetype}" xlink:href="https://plotly.local/{url_part}.svg" width="{width}" height="{height}" x="{x}" y="{y}" data-original_dimensions="{width},{height}" data-fid="{fid}" data-content_href="https://plotly.local/{url_part}.embed"></image>
	# """

from chart_studio.grid_objs import Grid as _Grid, Column as _Column


class Grid(_Grid):
    """Plotly Grid object exposed in figlinq module.

    Inherits from chart_studio.grid_objs.grid_objs.Grid.
    """    

class Column(_Column):
    """Plotly Column object exposed in figlinq module.

    Inherits from chart_studio.grid_objs.grid_objs.Column.
    """
    pass
