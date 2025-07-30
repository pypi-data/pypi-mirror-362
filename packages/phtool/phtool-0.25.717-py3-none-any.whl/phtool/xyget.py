# -*- coding: utf-8 -*-


"""
显示图像，并交互点击选择星
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
from astropy.stats import sigma_clipped_stats
from matplotlib.widgets import Button, Slider


def xyget(
    filelist,
    baseix=0,
    pickbox=20,
    xyfile=None,
    display=False,
):
    """
    找源
    :param filelist: 待测光的文件列表
    :param baseix: 基准图像索引
    :param pickbox: 选源范围
    :param xyfile: 选源结果文件
    :param display: 是否最后在屏幕显示结果，适用于从终端调用的情况
    :return: 选中的源的x、y数组
    """
    logger = logging.getLogger("phtool_main")
    # 确定具体文件名
    basefile = filelist[baseix]
    p, bf, suff, e = filename_split(basefile)
    # 加载图像，确认图像背景显示范围
    data = fits.getdata(basefile)
    vmin, vmax = np.percentile(data, [5, 95])
    # 加载找源结果
    star_pkl_file = os.path.join(p, bf + "_stars.pkl")
    sources, _, _ = pkl_load(star_pkl_file)
    x, y, m = sources["xcentroid"], sources["ycentroid"], sources["mag"]
    goodix = np.argsort(m)
    ngood = min(50, int(len(m)*0.25))
    x, y, m = x[goodix], y[goodix], m[goodix]
    # 画星图
    fig = plt.figure(figsize=(8.5, 6))
    ax = fig.add_axes([0.1, 0.05, 0.8, 0.9])
    img = ax.imshow(data, vmin=vmin, vmax=vmax, origin="lower", cmap="gray")
    fig.colorbar(img, ax=ax)
    ax.set_title(f"[{baseix:03d}] {bf}")
    # 标注源
    # 标注图中所有源（总数可变）
    cir_star = ax.scatter(x[:ngood], y[:ngood],
        s=15, #transform=ax.transData,
        facecolors="none", edgecolors="y",
    )
    # 标注选中的源，红圈，大一点点
    cir_select = ax.scatter([], [], marker="o",
        s=20, #transform=ax.transData,
        facecolors="none", edgecolors="r",
    )
    # 选中的源右上角加数字序号
    txt_select = {}
    # 选择源个数
    sli_ngood = Slider(
        fig.add_axes([0.005, 0.05, 0.04, 0.3]),
        '0',
        valinit=ngood,
        valmin=10, valmax=len(m), valstep=1,
        orientation="vertical",
    )
    # 选中的序号
    sel_ix = []
    # 选目标的半径
    sli_pickbox = Slider(
        fig.add_axes([0.005, 0.45, 0.04, 0.3]),
        'Box',
        valinit=pickbox,
        valmin=1, valmax=100, valstep=1,
        orientation="vertical",
    )
    # 图像序号
    sli_baseix = Slider(
        fig.add_axes([0.92, 0.05, 0.04, 0.9]),
        'Base',
        valinit=baseix,
        valmin=0, valmax=len(filelist)-1, valstep=1,
        orientation="vertical",
    )

    # 刷新图案
    def flush_image():
        nonlocal x, y, m, goodix
        # 根据当前图像编号，读取图像和星象数据，然后更新数据，刷新画布
        basefile = filelist[baseix]
        p, bf, suff, e = filename_split(basefile)
        # 加载图像，确认图像背景显示范围
        data = fits.getdata(basefile)
        vmin, vmax = np.percentile(data, [5, 95])
        # 加载找源结果
        star_pkl_file = os.path.join(p, bf + "_stars.pkl")
        sources, _, _ = pkl_load(star_pkl_file)
        x, y, m = sources["xcentroid"], sources["ycentroid"], sources["mag"]
        goodix = np.argsort(m)
        x, y, m = x[goodix], y[goodix], m[goodix]
        # 画星图
        img.set_data(data)
        img.set_clim(vmin, vmax)
        ax.set_title(f"[{baseix:03d}] {bf}")
        # 标注图中所有源（总数可变）
        cir_star.set_offsets(np.c_[x[:ngood], y[:ngood]])
        # 标注选中的源，红圈，大一点点，全部清空
        cir_select.set_offsets(np.c_[[], []])
        for ix in sel_ix:
            # 删除标签
            txt_select[ix].remove()
            del txt_select[ix]
        sel_ix.clear()
        fig.canvas.draw()

    def baseix_change(val):
        nonlocal baseix
        baseix = int(val)
        flush_image()

    # 鼠标点击事件
    def onclick(event):
        # 先判定是否是在画布区域，并且xy有效
        if event.inaxes != ax or event.xdata is None or event.ydata is None:
            return
        # 计算所有图中点和点击位置的距离
        dis = (x[:ngood] - event.xdata) ** 2 + (y[:ngood] - event.ydata) ** 2
        # print(len(dis), np.min(dis))
        # 如果不靠近任何点，则不操作
        if np.min(dis) > pickbox ** 2:
            return
        # 找到最近的点
        ix = np.argmin(dis)
        if ix in sel_ix:
            # 如果已经存在，那么从列表中删去，并且删除标签，重绘其他标签
            sel_ix.remove(ix)
            txt_select[ix].remove()
            del txt_select[ix]
            for i, ii in enumerate(sel_ix):
                txt_select[ii].set_text(f"{i+1:2d}")
        else:
            # 如果是新点，添加到列表中，并且新增标签
            sel_ix.append(ix)
            txt = ax.text(x[ix], y[ix], f"{len(sel_ix):2d}",
                ha="left", va="bottom", color="r", fontsize=8)
            txt_select[ix] = txt
        # 不论添加还是删除，都重新绘制选中的点，并刷新总点数的标签
        cir_select.set_offsets(np.c_[x[sel_ix], y[sel_ix]])
        sli_ngood.label.set_text(f"{len(sel_ix):2d}")
        fig.canvas.draw()
    
    def ngood_change(val):
        nonlocal ngood
        ngood = val
        cir_star.set_offsets(np.c_[x[:ngood], y[:ngood]])
        fig.canvas.draw()
    
    def pickbox_change(val):
        nonlocal pickbox
        pickbox = val
    
    def key_press(event):
        if (event.key) == "shift+up":
            sli_baseix.set_val(baseix + 1)
        elif (event.key) == "shift+down":
            sli_baseix.set_val(baseix - 1)
    
    # 关联事件
    fig.canvas.mpl_connect("button_press_event", onclick)
    fig.canvas.mpl_connect("key_press_event", key_press)
    sli_ngood.on_changed(ngood_change)
    sli_pickbox.on_changed(pickbox_change)
    sli_baseix.on_changed(baseix_change)
    # 显示图
    plt.show()

    p, bf, suff, e = filename_split(filelist[baseix])
    # 结束选择，如果选中了，就酌情输出
    if len(sel_ix) > 0:
        # 输出到屏幕
        if display:
            print(f"======== {len(sel_ix):d} sources selectd ========")
            for i, ii in enumerate(sel_ix):
                print(f"    {i:2d}[{ii:3d}]  ({x[ii]:6.1f},{y[ii]:6.1f})")
        logger.info(",".join([f"({x[ii]:6.1f},{y[ii]:6.1f})" for i, ii in enumerate(sel_ix)]))
        # 输出到文件
        if xyfile:
            with open(xyfile, "w") as ff:
                ff.write(f"{bf}\n")
                for i, ii in enumerate(sel_ix):
                    ff.write(f"{x[ii]:6.1f} {y[ii]:6.1f}\n")

    return bf, x[sel_ix], y[sel_ix]
