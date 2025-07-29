import yaml
import os
import argparse
from .yamlToTex import cleanup_tex, yamlToTeX


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-j",
        type=str,
        required=True,
        help="Job/position name. A directory with this name will be created to host tex and generated files.")
    parser.add_argument(
        "-y",
        nargs="+",
        required=True,
        help=("yaml files to use. Space separated with format" " <doc>:<yaml>.\n"
              "Example: -y cv:/path/to/cv.yaml research_plan:/path/to/research_plan.yaml"),
        type=lambda kv: kv.split(":"),
    )
    parser.add_argument(
        "-compile_tex",
        action="store_true",
        help="compile tex files",
    )
    parser.add_argument(
        "-clean_tex",
        action="store_true",
        help="clean tex files",
    )
    parser.add_argument(
        "-nasa_ads_token",
        type=str,
        default=None)

    args = parser.parse_args()
    args.y = dict(args.y)
    build_materials(args.j, args.y, args.compile_tex, args.clean_tex, args.nasa_ads_token)


def build_materials(job_name, yaml_files_dict, compile_tex=True, clean_tex=False, token=None):
    if not os.path.exists(job_name):
        os.mkdir(job_name)

    yt = yamlToTeX(authinfo_file="authinfo.yaml",
                   style_file="style.yaml",
                   job=job_name,
                   compile_tex=compile_tex,
                   nasa_ads_token=token)
    doc_dict = {"cv": yt.create_cv,
                "research_plan": yt.create_research_plan,
                "publications": yt.create_list_of_publications}
    for k in yaml_files_dict:
        if k not in doc_dict:
            raise Exception(f"Do not know how to create {k}")
        doc_dict[k](yaml_files_dict[k])

    if clean_tex:
        cleanup_tex(job_name)
