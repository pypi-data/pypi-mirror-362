# -*- coding: utf-8 -*-


"""
实现图像的平移对齐
"""


from .util import filename_split, pkl_dump
import numpy as np
import logging
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import os
import qmatch
from datetime import datetime


def offset(
    filelist, 
    offsetfile,
    baseix=0,
    maxoffset=500,
):
    """
    图像对齐
    :param filelist: 待对齐的文件列表
    :param offsetfile: 偏移文件
    :param baseix: 基准图像索引
    :param maxoffset: 最大偏移
    :return: 无
    """
    logger = logging.getLogger("phtool_main")
    # load base image
    logger.debug(f"Loading base image: {filelist[baseix]}")
    base_x, base_y = qmatch.mean_xy(fits.getdata(filelist[baseix]))
    # 文件数
    nf = len(filelist)

    # xy offset array
    offset_x = np.empty(nf, int)
    offset_y = np.empty(nf, int)
    bjd = np.empty(nf)

    # load images and process
    for i, fc in enumerate(filelist):
        # process data
        _, bf, _, _ = filename_split(fc)
        bf_x, bf_y = qmatch.mean_xy(fits.getdata(fc))
        offset_x[i] = int(qmatch.mean_offset1d(base_x, bf_x, max_d=maxoffset))
        offset_y[i] = int(qmatch.mean_offset1d(base_y, bf_y, max_d=maxoffset))

        # mjd of obs
        bjd[i] = fits.getval(fc, "BJD")

        logger.debug(f"{i+1:03d}/{nf:03d}: "
                   f"{bjd[i]:12.7f}  {offset_x[i]:+5d} {offset_y[i]:+5d}  "
                   f"{bf}")

    # 保存offset数据
    with open(offsetfile, "w") as ff:
        for d, x, y, fc in zip(bjd, offset_x, offset_y, filelist):
            ff.write(f"{d:12.7f}  {x:+5d} {y:+5d}  {filename_split(fc)[1]}\n")
    offset_pkl = os.path.splitext(offsetfile)[0] + ".pkl"
    pkl_dump(offset_pkl, bjd, offset_x, offset_y, filelist)
    logger.debug(f"Writing {offset_pkl}")

    # 绘制offset图
    ix = np.argsort(bjd)
    offset_png = os.path.splitext(offsetfile)[0] + ".png"
    fig = plt.figure(figsize=(6, 6))
    ax_xy = fig.add_axes([0.05, 0.05, 0.60, 0.60])
    ax_xt = fig.add_axes([0.05, 0.70, 0.60, 0.25])
    ax_ty = fig.add_axes([0.70, 0.05, 0.25, 0.60])
    ax_xy.plot(offset_x[ix], offset_y[ix], "k.:")
    ax_xt.plot(offset_x[ix], bjd[ix], "k.:")
    ax_ty.plot(bjd[ix], offset_y[ix], "k.:")
    ax_xy.set_xlabel("X offset")
    ax_xy.set_ylabel("Y offset")
    ax_xt.set_ylabel("MJD")
    ax_ty.set_xlabel("MJD")
    ax_xt.set_title(f"{filename_split(offsetfile)[1]}")
    fig.savefig(offset_png)
