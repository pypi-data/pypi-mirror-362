# -*- coding: utf-8 -*-


"""
从测光结果中选出目标星
"""


from .util import change_suffix, filename_split, pkl_dump, pkl_load
import numpy as np
import logging
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import os
from scipy.spatial import cKDTree
from qmatch import match2d


def pick(
    filelist,
    alignfile,
    pickfile,
    baseix=0,
    pickbox=20,
    xyfile=None,
):
    """
    从找到的源中选出想要进行后续较差分析的源
    :param filelist: 待处理文件列表
    :param alignfile: 对齐文件
    :param pickfile: 星等文件
    :param baseix: 基准图像索引
    :param pickbox: 选源范围
    :param xyfile: 源位置文件
    :return: 无
    """
    logger = logging.getLogger("phtool_main")

    # 如果没有xy坐标，那么就现场读
    if xyfile and os.path.isfile(xyfile):
        bf0 = open(xyfile).readline().strip()
        x0, y0 = np.loadtxt(xyfile, unpack=True, skiprows=1)
    else:
        print("xyget")
        from .xyget import xyget
        bf0, x0, y0 = xyget(filelist, baseix=baseix, pickbox=pickbox)
    n_star = len(x0)
    if n_star == 0:
        return

    # 加载对齐结果
    abjd, atrans, afilelist, abff = pkl_load(alignfile)
    abfilelist = [filename_split(f)[1] for f in afilelist]
    atransd = dict(zip(abfilelist, atrans))
    abjdd = dict(zip(abfilelist, abjd))

    # 根据0号文件确定数据的结构，假设所有数据都是一样的孔径（要不然没法继续）
    bf, phot_pkl_file = change_suffix(filelist[0], "_phot", ".pkl")
    sources, _ , apers, real_aper = pkl_load(phot_pkl_file)
    n_aper = len(apers)
    # 建立星等保存数组
    mag_cube = np.zeros((len(filelist), n_star, n_aper)) + np.nan  # nan表示找不到对应的星
    magerr_cube = np.zeros((len(filelist), n_star, n_aper))
    bjd = np.empty(len(filelist)) + np.nan
    bff = [filename_split(f)[1] for f in filelist]

    # 将输入的xy转化成align基准图上的xy
    if abff != bf0:
        # 如果两个基准不一致才需要转换，并且要指定xy的基准图也在转换记录中，否则就不转换了
        tr = atransd.get(bf0, None)
        if tr:
            x0, y0 = tr(np.c_[x0, y0]).T

    for k, f in enumerate(filelist):
        # 加载数据
        bf, phot_pkl_file = change_suffix(f, "_phot", ".pkl")
        sources, _, _, _ = pkl_load(phot_pkl_file)
        # 找偏移
        k_xy = np.c_[sources["xcentroid"], sources["ycentroid"]]
        bjd[k] = abjdd.get(bf, np.nan)-2450000.0
        tr = atransd.get(bf, None)
        # 把目标星转换到基准框架，然后匹配
        if tr:
            k_x_b, k_y_b = tr(k_xy).T
        else:
            k_x_b, k_y_b = k_xy.T
        ixk, ix0 = match2d(k_x_b, k_y_b, x0, y0, dislimit=pickbox)
        for a in range(n_aper):
            mag_cube[k, ix0, a] = sources[ixk][f"mag_{a+1}"]
            magerr_cube[k, ix0, a] = sources[ixk][f"mag_err_{a+1}"]
        logger.debug(f"pick {k}/{len(filelist)} {len(ix0)}")

    # 保存数据
    pkl_dump(pickfile, mag_cube, magerr_cube, bf0, x0, y0, apers, real_aper, bjd, bff)
    picktxt = os.path.splitext(pickfile)[0]
    for i, a in enumerate(apers):
        with open(f"{picktxt}_{a:04.1f}.txt", "w") as ff:
            # 表头
            ff.write(f"# {bf0}\n")
            ff.write("# BJD-245000.0\n")
            for j, (x, y) in enumerate(zip(x0, y0)):
                ff.write(f"# {j+1:2d}  {x:6.1f} {y:6.1f}\n")
            # 数据
            for f in range(len(filelist)):
                ff.write(f"{bjd[f]-245000:13.7f}")
                for s in range(n_star):
                    ff.write(f" {mag_cube[f, s, i]:6.3f}")
                ff.write(f" {bff[i]}\n")
    # 输出日志
    logger.info(f"{n_star} sources, {n_aper} apers, {len(filelist)} files")

    # todo 把文件名、BJD等补充到输出文件，方便后面一次性调用。不同孔径输出文件名用孔径大小，不用序号
