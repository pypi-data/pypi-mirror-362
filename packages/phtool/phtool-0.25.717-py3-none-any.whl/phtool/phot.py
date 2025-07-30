# -*- coding: utf-8 -*-


"""
测光
"""


from .util import filename_split, pkl_dump, pkl_load
import numpy as np
import logging
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import os
import glob
from photutils.background import Background2D, MMMBackground
from photutils.aperture import CircularAperture, aperture_photometry


def phot(
    filelist,
    apers,
):
    """
    找源
    :param filelist: 待测光的文件列表
    :param apers: 测光孔径
    :return: 无
    """
    logger = logging.getLogger("phtool_main")
    # 让apers是数组
    if isinstance(apers, (int, float)):
        apers = [apers]
    n_aper = len(apers)
    for k, f in enumerate(filelist):
        # 加载数据
        data = fits.getdata(f)
        ny, nx = data.shape
        p, bf, suff, e = filename_split(f)
        # 背景分析
        bkg_estimator = MMMBackground()
        bkg = Background2D(data, (50, 50), filter_size=(3, 3), bkg_estimator=bkg_estimator)

        # 图像减去背景
        data_sub = data - bkg.background
        data_error = np.sqrt(data_sub + bkg.background_rms**2)
        # 读取找源结果
        star_pkl_file = os.path.join(p, bf + "_stars.pkl")
        sources, fwhms, fwhms_med = pkl_load(star_pkl_file)
        # 设置位置和孔径
        real_aper = [a if a > 0 else -a * fwhms_med for a in apers]
        positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
        apertures = [CircularAperture(positions, r=aper) for aper in real_aper]
        # 测光
        apers_phot = aperture_photometry(data_sub, apertures, error=data_error)
        # 转星等和误差
        for a in range(n_aper):
            sources[f"flux_{a+1}"] = apers_phot[f"aperture_sum_{a}"]
            sources[f"flux_err_{a+1}"] = apers_phot[f"aperture_sum_err_{a}"]
            # 计算星等
            sources[f"mag_{a+1}"] = 25-2.5*np.log10(sources[f"flux_{a+1}"])
            sources[f"mag_err_{a+1}"] = 1.0857 * sources[f"flux_err_{a+1}"]/sources[f"flux_{a+1}"]
        # 保存结果
        phot_pkl_file = os.path.join(p, bf + "_phot.pkl")
        pkl_dump(phot_pkl_file, sources, fwhms_med, apers, real_aper)
        # 输出日志
        logger.debug(f"{bf}--> {len(sources)} Sources FWHM={fwhms_med:5.2f} pix")
