#!/bin/bash
# Builds the GNU Backgammon neural-net engine (gnubg-nn) as a Python module.
# Usage: bash setup.sh [build_dir]   (default /tmp/gbuild). Needs gcc/g++ and python3 headers.
set -e
B=${1:-/tmp/gbuild}; SRC=/tmp/gnubg-nn-pypi
[ -d $SRC ] || git clone -q --depth 1 https://github.com/StonesAndDice/gnubg-nn-pypi.git $SRC
[ -f $SRC/src/gnubg-nn/gnubg/eval.c ] || { rm -rf $SRC/src/gnubg-nn; git clone -q --depth 1 https://github.com/StonesAndDice/gnubg-nn.git $SRC/src/gnubg-nn; cp -rf $SRC/patches/gnubg-nn/* $SRC/src/gnubg-nn/; }
mkdir -p $B/gnubg_nn/data && cd $B
printf '#define _CRT_SECURE_NO_WARNINGS 1\n#define NOMINMAX 1\n#define LOADED_BO 1\n#define OS_BEAROFF_DB 1\n#define HAVE_CONFIG_H 1\n' > config.h
S=$SRC/src; INC="-I$S/gnubg-nn -I$S/gnubg-nn/gnubg -I$S/gnubg-nn/gnubg/lib -I$S/gnubg-nn/analyze -I$S/gnubg-nn/py -I. $(python3-config --includes) -include config.h -fPIC -O2 -w"
for f in gnubg/bearoffdb.c gnubg/eggmoveg.c gnubg/eval.c gnubg/inputs.c gnubg/mt19937int.c gnubg/positionid.c gnubg/pub_eval.c gnubg/lib/hash.c gnubg/lib/neuralnet.c gnubg/lib/nsse.c; do gcc $INC -c $S/gnubg-nn/$f -o $(basename $f .c).o; done
for f in $S/gnubgmodule/gnubgmodule.cpp $S/gnubg-nn/analyze/{analyze,bm,bms,danalyze,dice_gen,equities,mec,player}.cc $S/gnubg-nn/gnubg/{bearoffgammon,racebg,osr}.cc; do b=$(basename $f); g++ -std=c++14 -fpermissive $INC -c $f -o ${b%.*}.o; done
g++ -shared *.o -o gnubg_nn/_gnubg_nn$(python3-config --extension-suffix)
cp $S/gnubgmodule/__init__.py gnubg_nn/ && cp $S/gnubgmodule/data/* gnubg_nn/data/ && echo '__version__="local"' > gnubg_nn/__version__.py
python3 -c "import sys;sys.path.insert(0,'$B');import gnubg_nn as g;b=g.board_from_position_id('4HPwATDgc/ABMA');print('engine ok, 3-1 ->',g.best_move(b,3,1,n=2))"
