# -*- coding: utf-8 -*-


"""
实现本底合并
"""


from .util import combine, get_time, filename_split
import numpy as np
import logging
import astropy.io.fits as fits
import os


def biascomb(
    filelist, 
    biasfile, 
    combine_method="clip",
):
    """
    本底合并
    :param filelist: 本底文件列表
    :param biasfile: 合并后的文件
    :param method: 合并方法
    :return: 无
    """
    logger = logging.getLogger("phtool_main")
    # 获取头信息
    hdr = fits.getheader(filelist[0])
    _ = f'{hdr}'
    # 获取数据并转换数据类型
    dat = [fits.getdata(f) for f in filelist]
    logger.debug(f"Read {len(filelist)} bias files.")
    # 合并
    masterbias = combine(dat, combine_method)
    # 填补头信息
    hdr["METHOD"] = combine_method
    hdr["COMBTIME"] = get_time()
    hdr["NBIAS"] = len(filelist)
    # 写入文件
    p, f, s, e = filename_split(biasfile)
    if p:
        os.makedirs(p, exist_ok=True)
    fits.writeto(biasfile, masterbias, hdr, overwrite=True)
    logger.debug(f"Combine {len(filelist)} bias files to {biasfile}.")
