"""Create yaml files from bib files."""
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import author, convert_to_unicode
import yaml
import argparse
import os
import urllib.request
import json
import requests
from urllib.parse import urlencode, quote_plus

def format_authors(list_of_authors, special_author):
    authors = ""
    num_authors = len(list_of_authors)
    for idx, author in enumerate(list_of_authors):
        last, first = author.split(", ")
        if first == "":
            continue
        initials = "".join([x[0] + ". " for x in first.split(" ")])
        if idx <= (num_authors - 3):
            joining_string = ", "
        elif idx == (num_authors - 2):
            joining_string = " \& "
        else:
            joining_string = ""
        author_name = initials + last
        if author_name == special_author:
            author_name = r"\underline{" + author_name + "}"
        authors += author_name + joining_string
    return authors

def customizations(record):
    record = author(record)
    record = convert_to_unicode(record)
    return record

def format_entries(entries_dict, special_author):
    for k in entries_dict.keys():
        if "collaboration" not in entries_dict[k]:
            entries_dict[k]["author"] = format_authors(
                entries_dict[k]["author"], special_author)


def get_citation_from_inspirehep_using_arxiv_no(arxiv_no):
    with urllib.request.urlopen(
            f"https://inspirehep.net/api/arxiv/{arxiv_no}") as url:
        citation = json.loads(
            url.read().decode())['metadata']['citation_count']
    return citation

def get_citation_from_nasa_ads_using_arxiv_no(arxiv_no, token):
    query = {"q": f"identifier:arXiv:{arxiv_no}",
             "fl": "citation_count"}
    encoded_query = urlencode(query)
    results = requests.get(
        "https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
        headers={'Authorization': 'Bearer ' + token})
    if len(results.json()["response"]["docs"]) > 0:
        return results.json()["response"]["docs"][0]["citation_count"]
    else:
        0

def get_publication_dict_from_bib(bibfile, special_author, token=None):
    bib_file = open(bibfile, "r")
    parser = BibTexParser()
    parser.customization = customizations
    bib_database = bibtexparser.load(bib_file, parser=parser)
    bib_file.close()
    entries_dict = bib_database.entries_dict
    format_entries(entries_dict, special_author)
    #for k in entries_dict:
    #    citations_inspirehep = get_citation_from_inspirehep_using_arxiv_no(
    #        entries_dict[k]['eprint'])
    #    entries_dict[k].update({"citation_count_inspirehep": citations_inspirehep})
    #    if token is not None:
    #        citations_nasaads = get_citation_from_nasa_ads_using_arxiv_no(
    #            entries_dict[k]['eprint'], token)
    #        entries_dict[k].update({"citation_count_nasaads": citations_nasaads})
    return entries_dict

def get_publication_list_from_dict(pub_dict, token=None):
    publist = "\\begin{enumerate}\n"
    for k in pub_dict:
        d = pub_dict[k]
        if "collaboration" in d:
            d["author"] = d["collaboration"]
        p = "\\item "
        p += d["author"] + ", " + "``" + d["title"] + "\"" + ", "
        if "journal" in d:
            p += "\href{" + "https://doi.org/" + d["doi"] + "}{" + d["journal"] + "}" + ", "
            p += "{\\bfseries " + d["volume"] + "}" + ", " + d["pages"] + ", "
        p += "(" + d["year"] + "), "
        p += "\href{" + "https://arxiv.org/abs/" + d["eprint"] + "}{arXiv:" + d["eprint"] + " [" + d["primaryclass"] +"]}"
        # p += f"cited by {{\\itshape {d['citations_count_inspirehep']}}} (INSPIRE HEP)"
        #if token is not None:
        #    p += f" {{\\itshape {d['citations_count_nasaads']}}} (NASA/ADS)"
        publist += "\\end{enumerate}\n"
