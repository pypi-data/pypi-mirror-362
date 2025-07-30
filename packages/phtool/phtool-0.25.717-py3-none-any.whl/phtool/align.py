# -*- coding: utf-8 -*-


"""
实现图像的平移对齐
"""


from .util import filename_split, change_suffix, pkl_dump, pkl_load
import numpy as np
import logging
import astropy.io.fits as fits
import os
import astroalign as aa


def align(
    filelist, 
    alignfile,
    baseix=0,
):
    """
    图像对齐
    :param filelist: 待对齐的文件列表
    :param alignfile: 偏移文件
    :param baseix: 基准图像索引
    :return: 无
    """
    logger = logging.getLogger("phtool_main")
    # 选多少星进行处理
    ngood = 100
    # load base image
    b_fn, b_star_file = change_suffix(filelist[baseix], "_stars", ".pkl")
    logger.debug(f"Loading base cstalog: {b_star_file}")
    b_cat, _, _ = pkl_load(b_star_file)
    b_ix = np.argsort(b_cat["mag"])
    b_xy = np.c_[b_cat["xcentroid"], b_cat["ycentroid"]][b_ix[:ngood], :]
    # 文件数
    nf = len(filelist)

    # xy offset array
    trans = []
    bjd = np.empty(nf)

    # load images and process
    for k, fc in enumerate(filelist):
        # process data
        bf, k_star_file = change_suffix(fc, "_stars", ".pkl")
        k_cat, _, _ = pkl_load(k_star_file)
        k_ix = np.argsort(k_cat["mag"])
        k_xy = np.c_[k_cat["xcentroid"], k_cat["ycentroid"]][k_ix[:ngood], :] 
        tr, _ = aa.find_transform(k_xy, b_xy)
        trans.append(tr)

        # mjd of obs
        bjd[k] = fits.getval(fc, "BJD")

        logger.debug(f"{k+1:03d}/{nf:03d}: {bjd[k]-245000:10.7f} "
                   f"{tr.rotation:+5.1f} {tr.scale:4.2f} {tr.translation[0]:+6.1f} {tr.translation[1]:+6.1f}"
                   f"  {bf}")

    # 保存align数据
    pkl_dump(alignfile, bjd, trans, filelist, b_fn)
    logger.debug(f"Writing {alignfile}")
