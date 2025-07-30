# -*- coding: utf-8 -*-
"""
    v0 20250607, Dr/Prof Jie Zheng & Dr/Prof Linqiao Jiang
    Photometry Tools
"""


from ast import parse
import sys
import argparse
import os
import glob
import logging
from .util import filename_split, ext_check

import warnings
warnings.filterwarnings('ignore')


def _short_match_(s):
    """用短名字匹配命令"""
    tasks = [
        "biascombine",
        "flatcombine",
        "imcorrect",
        "offset",
        "find",
        "align",
        "phot",
        "xyget",
        "pick",
        "diffcali",
    ]
    tt = [t for t in tasks if t.startswith(s)]
    if len(tt) == 1:
        return tt[0]
    elif len(tt) > 1:
        raise ValueError(f"Ambiguous task: {s}")
    else:
        raise ValueError(f"Unknown task: {s}")


def _out_dir_file_(filename, defaultname, *ext):
    """
    处理输出目录和文件名
    """
    if not filename:
        filename = defaultname
    filename = os.path.expanduser(filename)
    if not ext_check(filename, ext):
        filename += ext[0]
    return filename


def str_or_int(value):
    """test str or int, for argparse"""
    try:
        return int(value)
    except ValueError:
        return value


def pos_xy(coord_str):
    """converts a string 'x,y' to a float tuple (x, y)"""
    try:
        x, y = coord_str.split(',')
        return float(x.strip()), float(y.strip())
    except ValueError:
        raise argparse.ArgumentTypeError(f"Cannot convert '{coord_str}' to a x,y position.")


def main():
    """
    A cli tool to run the pipeline.
    """
    if len(sys.argv) == 1:
        print("""Photometry Tools
Usage: python -m phtool command arguments
Commands:
    biascombine
        py -m phtool biascombine
""")
    else:
        # cmd = _short_match_(sys.argv[1])
        # parse arguments
        parser = argparse.ArgumentParser(description="Photometry Tools")
        parser.add_argument("task", type=str, nargs=1,
            help="Task to run")
        parser.add_argument("--whenexist", type=str.lower, nargs="?", default="autonum",
            choices=["overwrite", "skip", "append", "autonum", "error"],
            help="What to do when output file exists")
        parser.add_argument("--log", type=str.upper, nargs="?", default="INFO",
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Log level")
        parser.add_argument("files", type=str, nargs="*",
            help="Raw data files")
        parser.add_argument("-l", "--list", type=str, nargs="?", default=None,
            help="Raw data list")
        parser.add_argument("-o", "--outdir", type=str, nargs="?", default="./",
            help="Output directory")
        parser.add_argument("--bias", type=str, nargs="?", default=None,
            help="Master bias filename")
        parser.add_argument("--flat", type=str, nargs="?", default=None,
            help="Master flat filename")
        parser.add_argument("--combine", type=str.lower, nargs="?", default="clip",
            choices=["clip", "median", "mean", "avg", "average"],
            help="Bias & flat combine method")
        parser.add_argument("--norm", type=str.lower, nargs="?", default="clip",
            choices=["clip", "median", "mean", "avg", "average"],
            help="Flat normalizing method")
        parser.add_argument("--radec", type=str, nargs="?", default=None,
            help="RA and Dec of the target, e.g. '12:34:56.78,-12:34:56.78' or '12.3456,+23.4567'")
        parser.add_argument("--keyradec", type=str, nargs="?", default=None,
            help="Header key of RA and Dec of the target, e.g. 'RA,DEC'")
        parser.add_argument("--sitename", type=str.lower, nargs="?", default="xinglong",
            help="Site name, e.g. 'xinglong'")
        parser.add_argument("--sitecoord", type=str, nargs="?", default="117.55,40.40",
            help="Site coordinate, e.g. '117.55,40.40' or '117:33:01,40:28:23'")
        parser.add_argument("--offset", type=str, nargs="?", default=None,
            help="Offset file")
        parser.add_argument("--baseix", type=int, nargs="?", default=0,
            help="Base image index for offset")
        parser.add_argument("--maxoffset", type=int, nargs="?", default=500,
            help="Max offset for offset")
        parser.add_argument("--align", type=str, nargs="?", default=None,
            help="Align file")
        parser.add_argument("--apers", type=float, nargs="*", default=[-2.5],
            help="Aperture(s) for photometry")
        parser.add_argument("--xyfile", type=str, nargs="?", default=None,
            help="XY file of selected sources")
        parser.add_argument("--pickbox", type=float, nargs="?", default=20,
            help="Pick box size for selecting sources")
        parser.add_argument("--pickfile", type=str, nargs="?", default=None,
            help="Pick file of selected sources")
        parser.add_argument("--califile", type=str, nargs="?", default=None,
            help="Calibration file of selected sources")
        parser.add_argument("--tgtidx", type=int, nargs="*", default=None,
            help="Target star index")
        parser.add_argument("--refidx", type=int, nargs="*", default=None,
            help="Reference star index")
        parser.add_argument("--chkidx", type=int, nargs="*", default=None,
            help="Check star index")
        
        args = parser.parse_args()

        # 配置日志
        logger = logging.getLogger("phtool_main")
        # 新建一个控制台 Handler
        ch = logging.StreamHandler()
        ch.setLevel(args.log)              # 让 Handler 也接受 DEBUG 级别
        # 可选：设置格式
        # fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # ch.setFormatter(fmt)
        # 把 Handler 挂到 Logger 上
        logger.addHandler(ch)
        logger.setLevel(args.log)

        # logging.debug(f"{args}")
        # 解析命令
        task = _short_match_(args.task[0])
        # 输出文件存在处理模式
        whenexist = args.whenexist
        # 处理列表
        files = args.files
        if args.list and os.path.exists(args.list):
            with open(args.list, "r") as f:
                files.extend([line.strip() for line in f.readlines()])
        efiles = []
        for f in files:
            efiles.extend(glob.glob(os.path.expanduser(f)))
        efiles.sort()

        if task == "biascombine":
            # 合并本底
            # 处理合并后的文件名
            biasfile = _out_dir_file_(args.bias, "BIAS", ".fits")
            from .biascomb import biascomb
            # print(task, efiles, biasfile, args.combine)
            biascomb(efiles, args.bias, args.combine)
        elif task == "flatcombine":
            # 处理合并后的文件名
            biasfile = _out_dir_file_(args.bias, "BIAS", ".fits")
            flatfile = _out_dir_file_(args.flat, "FLAT", ".fits")
            from .flatcomb import flatcomb
            # print(task, efiles, biasfile, flatfile, args.combine, args.norm)
            flatcomb(efiles, biasfile, flatfile, args.combine, args.norm)
        elif task == "imcorrect":
            # 处理合并后的文件名
            biasfile = _out_dir_file_(args.bias, "BIAS", ".fits")
            flatfile = _out_dir_file_(args.flat, "FLAT", ".fits")
            keyradec = args.keyradec
            radec = args.radec
            sitename = args.sitename
            sitecoord = args.sitecoord
            from .imcorr import imcorr
            # print(task, efiles, biasfile, flatfile, args.outdir)
            imcorr(efiles, biasfile, flatfile, args.outdir, 
                keyradec=keyradec, radec=radec, 
                sitename=sitename, sitecoord=sitecoord)
        elif task == "offset":
            # 处理偏移文件
            baseix = args.baseix
            maxoffset = args.maxoffset
            offsetfile = _out_dir_file_(args.offset, "offset", ".txt")
            from .offset import offset
            offset(efiles, offsetfile, baseix, maxoffset)
        elif task == "find":
            # 找源，暂无其他参数
            from .find import find
            find(efiles)
        elif task == "align":
            # 图像对齐
            baseix = args.baseix
            alignfile = _out_dir_file_(args.align, "align", ".pkl")
            from .align import align
            align(efiles, alignfile, baseix)
        elif task == "phot":
            # 找源，暂无其他参数
            from .phot import phot
            phot(efiles, apers=args.apers)
        elif task == "xyget":
            # 选择目标星
            baseix = args.baseix
            pickbox = args.pickbox
            xyfile = args.xyfile
            from .xyget import xyget
            xyget(efiles, baseix=baseix, pickbox=pickbox, xyfile=xyfile, display=True)
        elif task == "pick":
            # 选择目标星
            baseix = args.baseix
            pickfile = _out_dir_file_(args.pickfile, "pick", ".pkl")
            alignfile = _out_dir_file_(args.align, "align", ".pkl")
            xyfile = args.xyfile
            pickbox = args.pickbox
            from .pick import pick
            pick(efiles, baseix=baseix, pickfile=pickfile, alignfile=alignfile, pickbox=pickbox, xyfile=xyfile)
        elif task == "diffcali":
            # 差校
            pickfile = _out_dir_file_(args.pickfile, "pick", ".pkl")
            califile = _out_dir_file_(args.califile, "cali", ".pkl")
            tgtidx = args.tgtidx
            refidx = args.refidx
            chkidx = args.chkidx
            from .diffcali import diffcali
            diffcali(pickfile=pickfile, califile=califile, tgt_idx=tgtidx, ref_idx=refidx, chk_idx=chkidx)
            

if __name__ == "__main__":
    main()
