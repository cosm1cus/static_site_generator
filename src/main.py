import os
import sys

from catalogs_management import copy_static_to_public
from md_to_html_node import generate_all_htmls

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

def main():
    print(basepath)
    copy = copy_static_to_public()

    generate_all_htmls(
        os.path.join(dir_path_content),
        template_path,
        os.path.join(dir_path_public),
        basepath
    )


main()