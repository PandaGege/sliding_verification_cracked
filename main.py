# coding: utf-8
# ----------------------------------------------
# author            : regan
# email             : x-regan@qq.com
# create at         : 2019-07-06 15:31
# last modify       : 2019-07-06 15:31
# ----------------------------------------------

import numpy as np
from PIL import Image


def draw(mask, sep=''):
    for i in range(mask.shape[0]):
        print sep.join(str(i) for i in list(mask[i]))


def findit(f1, f2, y, ind):
    whole = np.array(Image.open(f1))
    piece = np.array(Image.open(f2))
    mask = (piece[:, :, 3] == 0).astype(int)
    mask = mask[:, :, np.newaxis] * [1, 1, 1]
    piece = piece[:, :, 0:3]

    max_x, max_std = -1, 2**63-1
    for i in range(whole.shape[1]-piece.shape[1]):
        p = whole[y:(y+piece.shape[0]), i:(i+piece.shape[1])]
        t = np.ma.masked_array((piece-p), mask)
        t = t.sum(axis=2).sum(axis=1)
        std = t.std()
        if max_std > std:
            max_x, max_std = i, std

    whole[y:y+piece.shape[0], max_x:max_x+piece.shape[1]] = piece
    im = Image.fromarray(whole)
    im.save('result/'+str(ind)+'.jpg')


def main():
    with open('case', 'r') as fobj:
        i = 0
        for line in fobj:
            i += 1
            m, id, f1, f2, y = line.strip().split('\t')
            findit(f1, f2, int(y), i)


if __name__ == '__main__':
    main()
