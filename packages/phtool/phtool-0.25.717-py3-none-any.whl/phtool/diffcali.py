# -*- coding: utf-8 -*-


"""
从测光结果中选出目标星
"""


from .util import filename_split, pkl_dump, pkl_load
import numpy as np
import logging
import matplotlib.pyplot as plt
from astropy.stats import sigma_clipped_stats


def diffcali(
    pickfile, 
    califile,
    tgt_idx,
    ref_idx,
    chk_idx,
    ):
    """
    进行较差分析并输出较差结果
    :param pickfile: 星等文件
    :param califile: 差校文件
    :param tgt_idx: 目标星索引
    :param ref_idx: 参考星索引
    :param chk_idx: 检查星索引
    :return: 无
    """
    logger = logging.getLogger("phtool_main")

    # 读取数据
    mag_cube, magerr_cube, bf0, x0, y0, apers, real_aper, bjd, bff = pkl_load(pickfile)
    # 提取数据：图号、星号、孔径号
    mag_tgt = mag_cube[:, tgt_idx, :]
    mag_ref = mag_cube[:, ref_idx, :]
    mag_chk = mag_cube[:, chk_idx, :]

    # 计算较差改正量
    cali_const = np.mean(mag_ref, axis=1)
    # 计算差校后的星等
    mag_tgt_cali = mag_tgt - np.broadcast_to(cali_const[:, np.newaxis, :], mag_tgt.shape)
    mag_chk_cali = mag_chk - np.broadcast_to(cali_const[:, np.newaxis, :], mag_chk.shape)

    # 保存结果
    pkl_dump(califile, mag_tgt_cali, mag_chk_cali, cali_const, bjd, bff)
    logger.debug(f"Diff calibration saved to {califile}")

    # todo 输出的时候带上BJD、文件名。加上输出各孔径的光变曲线
    # 画图准备，计算每颗目标星、检验星的较差星等进行sigma-clip之后的中值和标准差
    _, mag_tgt_cali_med, mag_tgt_cali_std = sigma_clipped_stats(mag_tgt_cali, axis=0)
    _, mag_chk_cali_med, mag_chk_cali_std = sigma_clipped_stats(mag_chk_cali, axis=0)

    # 画图各光变曲线之间的间隔
    lc_sep = 0.05
    # 计算各曲线的中点位置
    tgt_mid = []
    
    tgt_mid = [np.sum(mag_tgt_cali_std[:i+1], axis=0) * 3 + i * lc_sep for i in range(len(tgt_idx)+1)]
    chk_mid = [np.sum(mag_chk_cali_std[:i+1], axis=0) * 3 + (i+1) * lc_sep for i in range(len(chk_idx)+1)]
    # 颜色序列
    colors = lambda c: "rgbmyc"[c % 6]
    # 画图
    for j, a in enumerate(apers):
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        for i in range(len(tgt_idx)):
            ax.scatter(bjd, mag_tgt_cali[:, i, j] - mag_tgt_cali_med[i][j] - tgt_mid[i][j], 
                marker="*", color=colors(i), label=f"Target {i+1} $\\sigma=${mag_tgt_cali_std[i][j]:.3f}")
        for i in range(len(chk_idx)):
            ax.scatter(bjd, mag_chk_cali[:, i, j] - mag_chk_cali_med[i][j] + chk_mid[i][j], 
                marker=".", color=colors(1-i), label=f"Check {i+1} $\\sigma=${mag_chk_cali_std[i][j]:.3f}")
        ax.legend()
        ax.set_xlabel("BJD")
        ax.set_ylabel("Magnitude")
        ax.set_title(f"Diff Calibration of Aper {a:04.1f}")
        ax.set_ylim(chk_mid[-1][j], -tgt_mid[-1][j])
        fig.savefig(califile.replace(".pkl", f"_{a:04.1f}.png"))
    