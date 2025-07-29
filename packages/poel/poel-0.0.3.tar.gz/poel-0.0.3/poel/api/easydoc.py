# -*- coding: UTF-8 -*-
from poel.core.parse import parse


def parse_files(api_key, file_path, mode=None):
    p_utils = parse(api_key)
    res_json = p_utils.parse_files(file_path, mode)
    return res_json
