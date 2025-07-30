# -*- coding: utf-8 -*-


"""
实现找源
"""


from .util import filename_split, pkl_dump
import numpy as np
import logging
import astropy.io.fits as fits
import matplotlib.pyplot as plt
import os
from scipy.optimize import curve_fit
from astropy.stats import sigma_clipped_stats
# import glob
# from astropy.stats import SigmaClip
from photutils.background import Background2D, MMMBackground
from photutils.detection import DAOStarFinder
# from photutils.aperture import CircularAperture #, ApertureStats


def find(
    filelist, 
):
    """
    找源
    :param filelist: 待找源的文件列表
    :return: 无
    """
    logger = logging.getLogger("phtool_main")

    def gauss2(xy, amplitude, x_mean, y_mean, stddev2):
        x, y = xy
        r2 = (x - x_mean)**2 + (y - y_mean)**2
        return amplitude * np.exp(-0.5 * r2 / stddev2)

    # 标准差转半高全宽
    std2fwhm = 2 * np.sqrt(2 * np.log(2))

    for k, f in enumerate(filelist):
        # 加载数据
        data = fits.getdata(f)
        ny, nx = data.shape
        p, bf, suff, e = filename_split(f)
        # 背景分析
        # sigma_clip = SigmaClip(sigma=3.0)
        bkg_estimator = MMMBackground()
        bkg = Background2D(data, (50, 50), filter_size=(3, 3), bkg_estimator=bkg_estimator)

        background = bkg.background
        # background_rms = bkg.background_rms
        bkg_std = bkg.background_rms_median
        # 图像减去背景
        data_sub = data - background
        # 第一次找源
        daofind = DAOStarFinder(fwhm=3, threshold=10.*bkg_std)
        sources = daofind(data_sub)
        # 选出最亮的一批
        goodix = np.argsort(sources["mag"])
        goodix = goodix[:min(50, int(len(goodix)*0.25))]
        sources = sources[goodix]

        # 拟合星象
        r = 10  # 经验数据，21x21的子图足够得到稳定的gauss2d拟合
        fwhms = np.empty(len(sources), np.float32) + np.nan
        ctx = np.empty(len(sources), np.float32) + np.nan
        cty = np.empty(len(sources), np.float32) + np.nan
        peaks = np.empty(len(sources), np.float32) + np.nan
        for i, ss in enumerate(sources):
            x0, y0 = int(ss["xcentroid"]), int(ss["ycentroid"])
            # 确保子图像不会超出边界
            x_min, x_max = max(0, x0 - r), min(nx, x0 + r+1)
            y_min, y_max = max(0, y0 - r), min(ny, y0 + r+1)
            data_stamp = data_sub[y_min:y_max, x_min:x_max]
            # 检查子图像是否包含足够的数据点
            if data_stamp.size < 6:
                continue
            # 创建网格数据
            yy, xx = np.mgrid[y_min-y0:y_max-y0, x_min-x0:x_max-x0]
            # 扁平化，因为curve_fit只接受一维数组
            xx_flat = xx.flatten()
            yy_flat = yy.flatten()
            data_stamp_flat = data_stamp.flatten()
            try:
                popt, pcov = curve_fit(gauss2, 
                    (xx_flat, yy_flat), data_stamp_flat, 
                    p0=[np.max(data_stamp), 0, 0, 4])
                peaks[i], ctx[i], cty[i], std2 = popt
                fwhms[i] = np.sqrt(std2) * std2fwhm
            except Exception as e:
                pass
        # f2 = ",".join([f"{f:3.1f}" for f in fwhms])
        # f1 = np.nanmean(fwhms)
        # print(f"{r*2:2d} {f1:5.2f} {f1/r:4.2f} -- {f2}")


        # 计算FWHM的裁剪后均值
        _, fwhms_med, _ = sigma_clipped_stats(fwhms)
        # 用中值重新进行找星
        daofind = DAOStarFinder(fwhm=fwhms_med, threshold=5.*bkg_std)
        sources = daofind(data_sub)
        # 删去边缘的目标
        x, y = sources["xcentroid"], sources["ycentroid"]
        bordercut = max((10, 3 * fwhms_med))
        ix = (x > bordercut) & (x < nx - bordercut) & (y > bordercut) & (y < ny - bordercut)
        sources = sources[ix]
        # 保存结果
        star_pkl_file = os.path.join(p, bf + "_stars.pkl")
        pkl_dump(star_pkl_file, sources, fwhms, fwhms_med)
        # 输出日志
        logger.debug(f"{bf}--> {len(sources)} Sources FWHM={fwhms_med:5.2f} pix")

        # positions = np.transpose((sources['xcentroid'], sources['ycentroid']))
        # circ = CircularAperture(positions, r=2 * fwhms_med)

        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        ax.imshow(data_sub, vmin=-bkg_std, vmax=bkg_std*3, cmap="gray", origin="lower")
        # circ.plot(color='blue', lw=1.5, alpha=0.5, ax=ax)
        ax.scatter(sources['xcentroid'], sources['ycentroid'],
            s=5*fwhms_med, transform=ax.transData,
            facecolors="none", edgecolors="r",
        )
        png_file = os.path.join(p, bf + "_stars.png")
        ax.set_title(f"{bf}--> {len(sources)} Sources FWHM={fwhms_med:5.2f} pix")
        plt.savefig(png_file)
