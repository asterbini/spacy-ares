import os
import spacy_ares

__PACKAGE_BASE_PATH = os.path.dirname(spacy_ares.__file__)


def get_package_basepath():
    return __PACKAGE_BASE_PATH
