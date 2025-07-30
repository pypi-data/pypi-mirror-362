# -*- coding: utf-8 -*-


"""
实现平场合并
"""


from .util import normfactor, combine, get_time, filename_split
import numpy as np
import logging
import os
import astropy.io.fits as fits


def flatcomb(
    filelist, 
    biasfile, 
    flatfile, 
    combine_method="clip", 
    norm_method="clip"
    ):
    """
    平场合并
    :param filelist: 平场文件列表
    :param masterbias: 合并后的本底
    :param masterflat: 合并后的平场
    :param method: 平场合并方法
    :param norm: 平场归一化方法
    :return: 无
    """
    logger = logging.getLogger("phtool_main")
    # 加载合并后的本底
    masterbias = fits.getdata(biasfile)
    # 获取头信息
    hdr = fits.getheader(filelist[0])
    _ = f"{hdr}"
    # 获取数据并扣除本底
    dat = [fits.getdata(f) - masterbias for f in filelist]
    logger.debug(f"Read {len(filelist)} flat files.")
    # 归一化因子
    nf = [normfactor(d, norm_method) for d in dat]
    logger.debug(f"Normalization factor:" + " ".join([f"{n:.2f}" for n in nf]))
    # 归一化
    dat = [d / n for d, n in zip(dat, nf)]
    # 合并
    masterflat = combine(dat, combine_method)
    # 填补头信息
    hdr["COMBINE"] = combine_method
    hdr["NORM"] = norm_method
    hdr["COMBTIME"] = get_time()
    hdr["NFLAT"] = len(filelist)
    # 写入文件
    p, f, suff, e = filename_split(flatfile)
    if p:
        os.makedirs(p, exist_ok=True)
    fits.writeto(flatfile, masterflat, hdr, overwrite=True)
    logger.debug(f"Combine {len(filelist)} flat files to {flatfile}.")
