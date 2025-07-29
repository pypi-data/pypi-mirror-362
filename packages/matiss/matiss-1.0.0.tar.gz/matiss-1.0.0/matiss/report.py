
#%%
import os
from typing import Dict, Union
import matplotlib.pyplot as plt
import seaborn as sns
from colorcet import glasbey
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
from pathlib import Path
from weasyprint import HTML
import logging
import sys
from IPython.display import display 
import argparse

def parse_args(
    parser: argparse.ArgumentParser
):
    notebook = sys.argv[0].endswith("ipykernel_launcher.py")
    return parser.parse_args("" if notebook else None)

def set_logger(outdir: Path, args, description, level="DEBUG"):
    logfmt = "%(asctime)s | %(levelname)s | %(message)s"
    logging.basicConfig(filename=outdir.joinpath(f"{Path(sys.argv[0]).name[:-3]}.log"), 
        level=level, filemode='w', format=logfmt, force=True)
    logging.info(f"Running the Python script {sys.argv[0]}. {description}.")
    logging.info(":::::::::::::::::::::::::: OPTIONS ::::::::::::::::::::::::::")
    logging.info('\n'.join([str(k)+': '+str(getattr(args, k)) for k in vars(args)]))
    logging.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")

@dataclass
class Report:

    outdir: str
    title: str = ""
    fig_dir_: str = "figures"
    write_pdf: bool = True
    silent: bool = False

    def __post_init__(self):

        self.html = f"<html>\n\t<head>\n\t\t<title class='title'>{self.title}</title>\n\t</head>\n\t<body><div class=holder>\
<div class=report>\n\t\t<h1>{self.title}</h1>"
        self.outdir = Path(self.outdir)
        if not self.outdir.exists(): self.outdir.mkdir()
        self.fig_dir = self.outdir.joinpath(self.fig_dir_)
        if not self.fig_dir.exists(): self.fig_dir.mkdir()
        self.file = self.outdir.joinpath("report.html")

    def __close_tags(self):
        self.html += f"</div></div><div class='generated-on-banner'><p class='generated-on'>Generated on {str(datetime.now())}</p></div></body>"
        self.__add_style()
        self.html += "</html>"

    def __add_style(self):
        self.html += """
<style>
body {
    background-color: lightgrey;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: medium;
}
.holder {
    background-color: white;
    align-items: center;
    max-width: 800pt;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 0px;
    padding: 50pt;
}
p {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: medium;
    margin: 1rem 0rem 1rem 0rem;
}
h1 {
    font-family: Helvetica, "Helvetica Neue", Arial, sans-serif;
    font-size: 300%;
}
h2 {
    font-family: Helvetica, "Helvetica Neue", Arial, sans-serif;
    font-size: 200%;
}
h3 {
    font-family: Helvetica, "Helvetica Neue", Arial, sans-serif;
    font-size: 150%;
}
h4 {
    font-family: Helvetica, "Helvetica Neue", Arial, sans-serif;
    font-size: 100%;
    font-style: bold;
}
img {
    display: block;
    max-width: 80%;
    max-height: 300pt;
    margin-left: auto;
    margin-right: auto;
    margin-top: 3rem;
    margin-bottom: 3rem;
    text-align: center;
}
table {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width: 80%;
    text-align: center;
    border-collapse: collapse;
    margin: auto;
}
table td, table th {
    border: 1px solid #333333;
    padding: 5px 3px;
}
table tbody td {
    font-size: 15px;
}
table thead {
    background: #333333;
}
table thead th {
    font-size: 15px;
    font-weight: bold;
    color: #FFFFFF;
    text-align: center;
}
table tfoot {
    font-size: 14px;
    font-weight: bold;
    color: #333333;
    border-top: 4px solid #333333;
}
table tfoot td {
    font-size: 14px;
}
p.generated-on {
    font-size: .75rem;
    color: white;
}
div.generated-on-banner {
    background-color: #333333;
    margin-left: auto;
    margin-right: auto;
    margin-top: 0px;
    max-width: 800pt;
    padding: 5pt 50pt 5pt 50pt;
}
</style>

"""
    def __call__(self, text: str) -> None:
        return self.add_paragraph(text)

    def write(self):
        self.__close_tags()
        with open(self.file, "w") as file: file.write(self.html)
        if self.write_pdf: HTML(self.file).write_pdf(self.outdir.joinpath("report.pdf"))

    def add_paragraph(self, text: str):

        self.html = self.html + "\n\t\t<p class='paragraph'>" + text + "</p>"
        if not self.silent: print(text)

    def add_header(self, text: str, level: int = 2):

        self.html = self.html + f"\n\t\t<h{level} class='section-header'>" + text + f"</h{level}>"
        if not self.silent: print(text)

    def add_table(self, table: Union[pd.DataFrame, pd.Series]):

        if isinstance(table, pd.Series): table = table.to_frame()
        self.html += "\n\t\t"
        self.html += table.to_html()
        self.html += "\n"
        if not self.silent: display(table)
        return self

    def add_figure(self, fig: plt.Figure, fig_file:str, show:bool = True, figsize=None):

        # Save figure
        fig_loc = self.fig_dir.joinpath(fig_file)
        fig_loc_rel = Path(self.fig_dir_).joinpath(fig_file)
        fig.savefig(fig_loc, bbox_inches="tight")

        # Generate figure in HTML
        if figsize is None:
            self.add_element("img", close=False, src=fig_loc_rel, alt="report_image")
        else:
            self.add_element("img", close=False, src=fig_loc_rel, alt="report_image", width=figsize[0], height=figsize[1])
        if show: plt.show()

    def add_element(self, tag:str, content:str = "", class_:Union[str, None] = None, style_kwargs:Dict[str, str] = {}, close:bool=True,
        **kwargs):
        """Adds an HTML element to the report.

        Args:
            tag (str): HTML tag, without the <>. For instance, instead of '<p>' or '</p>', pass 'p'.
            content (str): placed between the close/open tags.
            class_ (str or None): class to assign to the element. If None, does not assign any class
            style_kwargs (Dict[str, str]): properties included in the 'style' field of the tag.
            close (bool): If False, does not include a close tag nor the content. Useful when placing <img> tags.
            kwargs (dict): other HTML properties.
        """
        class_str = "" if class_ is None else f" class='{class_}'"
        style_str = "" if not len(style_kwargs) else " style='"+";".join([f"{k}:{v}" for k,v in style_kwargs.items()])
        other_attrs_str = "" if not len(kwargs) else " "+" ".join([f"{k}='{v}'" for k,v in kwargs.items()])
        open_tag, close_tag = f"<{tag}{class_str}{style_str}{other_attrs_str}>", f"</{tag}>"
        if close: self.html += open_tag+content+close_tag
        else: self.html += open_tag
        return self
    
    def reset(self):
        self.html = ""
        self.__post_init__()


# %%
