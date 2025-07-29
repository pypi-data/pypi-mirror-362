[![github](https://img.shields.io/badge/GitHub-ycv-blue.svg)](https://github.com/md-arif-shaikh/ycv)
[![PyPI version](https://badge.fury.io/py/ycv.svg)](https://pypi.org/project/ycv)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/md-arif-shaikh/ycv/blob/main/LICENSE)
[![Build Status](https://github.com/md-arif-shaikh/ycv/actions/workflows/test.yaml/badge.svg)](https://github.com/md-arif-shaikh/ycv/actions/workflows/test.yaml)

# ycv
Build CV and job application materials using yaml files

# Example PDFs
[Here](https://github.com/md-arif-shaikh/ycv/tree/pdflatex/examples/fancyJob) you can find the pdfs built using `yaml` and `bib` files in the `example` directory.

# Installation
```bash
pip install ycv
```

# Requirements
- [Python](https://www.python.org/)
- [PyYAML](https://pyyaml.org/)
- [bibtexparser](https://pypi.org/project/bibtexparser/)
- [TeX](https://www.tug.org/texlive/)

# Usage
After installing `ycv` one can start building application materials using the command `ycv` from the terminal. 
```bash
ycv -j job_name -y doc_type:yaml_file
```
**Note:** The command should be executed inside a directory that contains a `authinfo.yaml` and `style.yaml` file. If these are not present, these will be created on the fly using prompts. See [here](#authinfo-and-style-files) for more about these files.
- `ycv` is designed to be used for multiple job applications and therefore requires a `job_name` to create a directory where all materials related to that job will be stored.
- `ycv` can create multiple application materials for a given job at once. To create different materials one needs to provide the `yaml` files for these materials in the format `doc_type:yaml_file` with a space between different materials. For example, to create a `cv` and `research statement`, provide the yaml files as 
```bash
ycv -j job_name -y cv:/path/to/cv.yaml research_plan:/path/to/research_statement.yaml
```
**Note:** The keys to yaml files should be one of the recognized ones
  - `cv`
  - `research_plan`
  - `publications`

more would be added to this list.

# authinfo and style files
`ycv` requires a `authinfo.yaml` and `style.yaml` file.
- `authinfo.yaml` contains information about the author which is used to a common header for all documents, for example. An example yaml file can be found [here](https://github.com/md-arif-shaikh/ycv/blob/main/examples/authinfo.yaml).
- `style.yaml` file is used to apply customized style to different elements in the `TeX` documents. This gives the user freedom to apply a style of their preference. An example file can be found [here](https://github.com/md-arif-shaikh/ycv/blob/main/examples/style.yaml).
