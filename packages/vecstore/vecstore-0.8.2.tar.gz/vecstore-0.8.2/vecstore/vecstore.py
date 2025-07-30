import math
from time import time
from collections import Counter
import numpy as np
from hnswlib import Index


class VecStore(Index):
    def __init__(self, fname, space='cosine', dim=512):  # 512 for sbert
        """
        creates empty store, serializable to file named "fname"
        containing vectors of size "dim"
        """
        super().__init__(space=space, dim=dim)
        self.fname = fname
        self.initialized = False
        self.times=Counter()

    def load(self):
        """ loads store content from file named "fname" """
        self.load_index(self.fname)
        self.initialized = True

    def save(self):
        """ saves store content to file named "fname" """
        self.save_index(self.fname)

    def init(self, N=1024):
        """
        initializes store to default parameters
        and max_elements=N
        """
        if self.initialized: return
        self.init_index(max_elements=N,
                        ef_construction=200,
                        M=64,
                        allow_replace_deleted=True
                        )
        self.set_ef(100)
        self.set_num_threads(8)
        self.initialized = True

    def __repr__(self):
        assert self.initialized
        count = self.element_count
        size = self.max_elements
        return f"VecSore(at:{self.fname},dim:{self.dim},has:{count}/{size})"

    def add(self, xss):
        """
        adds numpy array of numpy vectors to store
        """
        t1=time()
        self.init()
        if isinstance(xss, list): xss = np.array(xss)

        assert xss.shape[1] == self.dim, f"shape: {xss.shape[1]}, dim: {self.dim}"
        N = xss.shape[0]
        N += self.element_count
        if N > self.max_elements:
            N = max(2 * self.max_elements, 2 ** math.ceil(math.log2(N)))
            self.resize_index(N)
        self.add_items(xss)
        t2=time()
        self.times['add']+=(t2-t1)

    def ids(self):
        """
        returns list of ids (natural numbers) for vecs in store
        """
        return sorted(self.get_ids_list())

    def vecs(self, as_list=False):
        """
        returns the list or numpy array of vectors in the store
        """
        assert self.initialized
        return_type = 'list' if as_list else 'numpy'
        return self.get_items(self.ids(), return_type=return_type)

    def delete(self, i):
        """ deletes vector of id=i from the store """
        assert self.initialized
        self.mark_deleted(i)

    def query(self, qss, k=3):
        """
         returns ids and knn similarity scores for k neares neightbor
         for each numpy vector (ok also in list form) in qss
        """
        assert self.initialized
        assert isinstance(k, int)

        if isinstance(qss, list): qss = np.array(qss)
        distss, vect_idss = self.knn_query(qss, k, filter=None)

        return distss, vect_idss

    def query_one(self, qs, k=3):
        """
        returns knns for given k as pairss of (vector id,score)
        """
        t1 = time()
        assert self.initialized
        dists, vect_ids = self.query([qs], k=k)
        res= list(zip(dists[0], vect_ids[0]))
        t2 = time()
        self.times['query_one'] += (t2 - t1)
        return res

    def all_knns(self, k=3, as_weights=True):
        """
        computes k id,dist for all vectors in the store
        """
        t1=time()
        assert self.initialized
        k += 1  # as we drove knn to itself
        xss = self.vecs()

        vect_idss, vect_distss = self.query(xss, k=k)
        pairss = []
        for i, ids in enumerate(vect_idss):
            dists = vect_distss[i]
            pairs = []
            for k, j in enumerate(ids):
                if i == j: continue
                d = float(dists[k])
                if as_weights:
                    d = 1 - d
                pair = int(j), d
                pairs.append(pair)
            pairss.append(pairs)
        t2 = time()
        self.times['all_knns'] += (t2 - t1)
        return pairss


def normarr(xss):
    """
    normalizes an array - just for testing
    """
    xss = np.array(xss)
    return xss / np.linalg.norm(xss)


def test_vecstore():
    """
    simple test of all operations excpe delete
    """
    vs = VecStore('temp.bin', dim=3)
    xss = [[0.1, 0.2, 0.2], [11, 0.22, 33], [4, 5, 6], [7, 8, 0.9], [0.10, 11, 12]]
    yss = [[1, 2, 3], [30, 40, 50]]
    qs = [7, 8, 9]
    print(xss)
    print()

    print(yss)
    print()

    print(qs)
    print()

    x = normarr([0.33333334, 0.6666667, 0.6666667])
    print('norm arr:', x)

    # qs = normarr(qs)

    vs.add(xss)
    vs.add(yss)

    print('IDS:\n', vs.ids())
    print('\nVECS:\n', vs.vecs())

    vs.save()
    vs_ = VecStore('temp.bin', dim=3)
    vs_.load()
    r = vs_.query_one(qs)
    print()
    print(r)
    print('TIMES:',vs.times)

    ps = vs_.all_knns()
    print('\nKNN PAIRS:')
    for p in ps:
        print(p)

    print('\nSTORE:', vs_)
    print('TIMES:', vs_.times)


if __name__ == "__main__":
    test_vecstore()
