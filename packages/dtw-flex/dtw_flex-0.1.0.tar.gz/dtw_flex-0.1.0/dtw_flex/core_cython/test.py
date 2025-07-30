import timeit
import numpy as np
from dtw_flex.core import dtw as dtw_py
from dtw_flex.core_cython import dtw_cy
from numpy.random import Generator, PCG64
import copy

def base(nref=5, nquery=20):
    rng = Generator(PCG64(seed=10))
    dtw_obj = dtw_py.Dtw(nref_raw = nref, nquery=nquery)
    dtw_obj.ref = rng.random(nref+2)
    dtw_obj.query = rng.random(nquery)*10
    dtw_obj.prep()
    return dtw_obj

def f_py(dtw_obj):
    cost_init = copy.deepcopy(dtw_obj.cost)
    res = dtw_obj.backward()
    dtw_obj.cost = cost_init
    return res

def f_cy(dtw_obj):
    cost_init = copy.deepcopy(dtw_obj.cost)
    res = dtw_obj.backward_cy()
    dtw_obj.cost = cost_init
    return res


a, b, N, sumx, sumy2, sumx2, sumy2, sumxy, cost, step = f_py(base())
a_cy, b_cy, N_cy, sumx_cy, sumy2_cy, sumx2_cy, sumy2_cy, sumxy_cy, cost_cy, step_cy = f_cy(base())
print("result identical: {0}".format(np.allclose(cost,cost_cy)))

py = timeit.timeit('f_py(dtw_obj)',globals = globals(),setup = 'dtw_obj=base()',number = 100)
cy = timeit.timeit('f_cy(dtw_obj)',globals = globals(),setup = 'dtw_obj=base()',number = 100)
print('cython is {}x faster'.format(py/cy))





