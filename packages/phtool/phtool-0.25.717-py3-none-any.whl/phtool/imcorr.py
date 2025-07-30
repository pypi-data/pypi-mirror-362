# -*- coding: utf-8 -*-


"""
实现图像的本底平场改正
"""


from .util import get_time, filename_split, sitelib
import numpy as np
import logging
import astropy.io.fits as fits
import os
from astropy.coordinates import SkyCoord
from astropy.coordinates import EarthLocation
import astropy.units as u
from astropy.time import Time
from astropy.utils import iers
iers.conf.auto_download = False


def imcorr(
    filelist, 
    biasfile, 
    flatfile, 
    outdir,
    keyradec=None,
    radec=None,
    sitename="xinglong",
    sitecoord="117.55,40.40",
):
    """
    本底平场改正
    :param filelist: 待平场改正的文件列表
    :param biasfile: 本底文件
    :param flatfile: 平场文件
    :param radeckey: 坐标关键字
    :param radec: 坐标
    :param sitename: 观测地点
    :param sitecoord: 观测地点坐标
    :return: 无
    """
    logger = logging.getLogger("phtool_main")
    # 加载合并后的本底和平场
    masterbias = fits.getdata(biasfile)
    masterflat = fits.getdata(flatfile)

    # 分析坐标系统字段
    rakey, deckey = keyradec.replace(",", " ").split() if keyradec else "RA", "DEC"
    ra0, dec0 = radec.replace(",", " ").split() if radec else (None, None)

    # 分析观测台站信息
    if sitename and sitename in sitelib:
        sitelon, sitelat = sitelib[sitename]
    elif sitecoord:
        sitelon, sitelat = sitecoord.replace(",", " ").split()
    else:
        sitelon, sitelat = 117.55, 40.40
    site = EarthLocation(lon=sitelon, lat=sitelat)

    # 逐个进行平场改正
    os.makedirs(outdir, exist_ok=True)
    for f in filelist:
        # 读取文件
        dat = fits.getdata(f)
        hdr = fits.getheader(f)
        _ = f"{hdr}"
        # 扣除本底
        dat_corr = (dat - masterbias) / masterflat
        # 坐标信息：hdr中的RA/Dec--hdr中的CRVAL1/2--hdr中指定的字段--参数中的字段--nan
        if "RA" in hdr and "DEC" in hdr:
            ra = hdr["RA"]
            dec = hdr["DEC"]
        elif "CRVAL1" in hdr and "CRVAL2" in hdr:
            ra = hdr["CRVAL1"]
            dec = hdr["CRVAL2"]
        elif rakey in hdr and deckey in hdr:
            ra = hdr[rakey]
            dec = hdr[deckey]
        elif ra0 and dec0:
            ra = ra0
            dec = dec0
        else:
            ra = None
            dec = None
        if ra and dec:
            if isinstance(ra, str) and ":" in ra:
                coord = SkyCoord(ra, dec, unit=(u.hourangle, u.deg))
            else:
                coord = SkyCoord(ra, dec, unit=(u.deg, u.deg))
        else:
            coord = None

        # 获取观测时间，转为JD/MJD，然后转成BJD-TBD
        obsdtstr = (hdr.get("DATE-OBS","") + "T" + hdr.get("TIME-OBS","")).strip("T")
        obs_jd = Time(obsdtstr, format="isot", scale="utc", location=site)
        if coord:
            # 计算光行时间
            ltt = obs_jd.light_travel_time(coord, 'barycentric')
            bjd = obs_jd.tdb + ltt.tdb
        else:
            bjd = obs_jd.tdb
        # 填补头信息
        hdr["BIASFILE"] = biasfile
        hdr["FLATFILE"] = flatfile
        hdr["PROCTIME"] = get_time()
        # 填写文件头
        if coord:
            hdr["RA"] = coord.ra.to_string(unit=u.hour, sep=':', precision=2)
            hdr["DEC"] = coord.dec.to_string(unit=u.deg, sep=":",precision=1)
            hdr["BJD"] = bjd.tdb.jd
        else:
            hdr["BJD"] = np.nan
        hdr["JD"] = obs_jd.jd
        hdr["MJD"] = obs_jd.mjd
        # 新文件名
        p, fn, suff, e = filename_split(f)
        f_corr = os.path.join(outdir, fn+"_corr"+e)
        fits.writeto(f_corr, dat_corr, hdr, overwrite=True)
        logger.debug(f"Correct {f} -> {f_corr}")
