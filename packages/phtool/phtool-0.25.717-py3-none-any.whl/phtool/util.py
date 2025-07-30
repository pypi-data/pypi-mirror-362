# -*- coding: utf-8 -*-


"""
实现通用函数功能
"""


import os
import numpy as np
import datetime
from astropy.stats import sigma_clipped_stats
import pickle
import re


def filename_split(filename):
    """
    拆分文件名为路径、基本名、扩展名
    """
    pbn, ext = os.path.splitext(filename)
    if ext == ".gz":
        pbn, ext2 = os.path.splitext(pbn)
        ext = ext2 + ext
    pa = os.path.dirname(pbn)
    bn = os.path.basename(pbn)
    suffixs = ("_corr", "_stars", "_phot")
    suff = ""
    for s in suffixs:
        if bn.endswith(s):
            bn = bn[:-len(s)]
            suff = s
            break
    return pa, bn, suff, ext


def ext_check(filename, ext=".fits"):
    """
    判断文件名是否为fits或fits.gz
    """
    _, _, _, fnext = filename_split(filename)
    # 对于fits，考虑了几个变种
    fits_ext = (".fits", ".fits.gz", ".fit", ".fit.gz")
    # 如果只给了一个扩展名，转换为元组
    if isinstance(ext, str):
        ext = (ext,)
    # 逐个测试展开
    exts = []
    for e in ext:
        exts.extend(fits_ext if e in fits_ext else (e,))
    # 最后测试
    res = fnext.lower() in exts
    return res


def checkexist(filename, whenexist="autonum"):
    """
    检查输出文件是否存在
    """
    if os.path.exists(filename):
        if whenexist == "overwrite":
            return filename, f"{filename} exists, overwritten!"
        elif whenexist == "skip":
            return "", f"{filename} exists, skipped!"
        elif whenexist == "append":
            return filename, f"{filename} exists, appended!"
        elif whenexist == "autonum":
            i = 2
            pa, bn, suff, ext = filename_split(filename)
            while os.path.exists(f"{pa}/{bn}_{i:d}{suff}{ext}"):
                i += 1
            nfn = f"{pa}/{bn}_{i:d}{suff}{ext}"
            return nfn, f"{filename} exists, save to {nfn}!"
        else:
            raise FileExistsError(f"{filename} exists!")
    else:
        return filename, f"save to {filename} "


def change_suffix(filename, suffix, ext=None):
    """
    更改文件后缀名
    """
    pa, bn, _, ext0 = filename_split(filename)
    if not ext:
        ext = ext0
    if pa:
        pa += "/"
    return bn, f"{pa}{bn}{suffix}{ext}"


def get_time():
    """
    获取当前时间
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def combine(dat, method="clip"):
    """
    对数据进行组合，允许使用中值、均值、去除最大最小后均值等方法
    """
    if method == "median":
        res = np.nanmedian(dat, axis=0)
    elif method == "mean":
        red = np.nanmean(dat, axis=0)
    else:
        res = (np.nansum(dat, axis=0)
             - np.nanmax(dat, axis=0)
             - np.nanmin(dat, axis=0)
            ) / (np.count_nonzero(~np.isnan(dat), axis=0) - 2)
    res = res.astype(np.float32)
    return res


def normfactor(dat, norm="clip"):
    """
    计算数据的归一化因子，允许使用：
    clip: 截断，使用中值和四分位差进行截断
    mean: 使用平均值进行归一化
    median: 使用中值进行归一化
    """
    if norm == "mean" or norm == "avg" or norm == "average":
        res = np.nanmean(dat)
    elif norm == "median":
        res = np.nanmedian(dat)
    elif norm == "clip":
        res, _, _ = sigma_clipped_stats(dat)
    return res


def pkl_dump(filename:str, *dat):
    """dump variables into pickle file"""
    with open(filename, "wb") as ff:
        pickle.dump(dat, ff)


def pkl_load(filename:str):
    """load var from pickle file"""
    with open(filename, "rb") as ff:
        dat = pickle.load(ff)
    return dat


sitelib = {
    "xinglong": (117.55,40.40),
    "lijiang": (100.03, 26.70),
    "nanshan": (87.17, 43.40),
}
