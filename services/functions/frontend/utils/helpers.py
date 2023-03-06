# -*- coding: utf-8 -*-
""""""
import os.path
import markdown


def openfile(filename):
    """

    :param filename:
    :return:
    """
    filepath = os.path.join("pages/", filename)
    with open(filepath, "r", encoding="utf-8") as input_file:
        text = input_file.read()

    html = markdown.markdown(text)
    data = {"text": html}
    return data
