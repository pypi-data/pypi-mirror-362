#!python
#cython: language_level=3
from cython.parallel import prange
import numpy as np
cimport numpy as np
np.import_array()

cpdef dtw_backward(
                    np.ndarray[np.float64_t, ndim=1] query, np.ndarray[np.float64_t, ndim=1] ref,
                    np.ndarray[np.float64_t, ndim=2] cost, np.ndarray[np.float64_t, ndim=2] weight,
                    np.ndarray[np.int64_t, ndim=2] step_single, np.ndarray[np.int64_t, ndim=2] step_multiple,
                    np.ndarray[np.float64_t, ndim=1] step_weight,
                    np.ndarray[np.int64_t, ndim=2] rep_step_ref, np.ndarray[np.int64_t, ndim=2] rep_step_query):

    ###key dimensions###
    cdef int n, m, rep_lim, n_single, n_multiple, m_multiple
    n, m = len(ref), len(query)
    rep_lim = max(m, n) - 1
    n_single = np.shape(step_single)[1]
    m_multiple = np.shape(step_multiple)[1]
    n_multiple = int(np.shape(step_multiple)[0] / 2)

    cdef np.ndarray[np.float64_t, ndim=2] a = np.ones((n,m), dtype=np.float64) #type_ = numpy type, type_t = type indentifier
    cdef np.ndarray[np.float64_t, ndim=2] b = np.zeros((n,m), dtype=np.float64)
    cdef np.ndarray[np.float64_t, ndim=2] N = np.zeros((n,m), dtype=np.float64)
    cdef np.ndarray[np.float64_t, ndim=2] sumy = np.zeros((n,m), dtype=np.float64)
    cdef np.ndarray[np.float64_t, ndim=2] sumx = np.zeros((n,m), dtype=np.float64)
    cdef np.ndarray[np.float64_t, ndim=2] sumy2 = np.zeros((n,m), dtype=np.float64)
    cdef np.ndarray[np.float64_t, ndim=2] sumx2 = np.zeros((n,m), dtype=np.float64)
    cdef np.ndarray[np.float64_t, ndim=2] sumxy = np.zeros((n,m), dtype=np.float64)
    cdef np.ndarray[np.int64_t, ndim=2] step = -np.ones((n+1,m+1), dtype=np.int64)

    #cdef Py_ssize_t i, ii, j, jj, k, r, s
    cdef int i, ii, j, jj, i_s, j_s, k, r, s
    cdef int step_bool, rep_max
    cdef double a_new, b_new, N_new, sumx_new, sumy_new, sumx2_new, sumy2_new, sumxy_new, cost_new

    ###initiate matrices###
    N[0, 0] = 1 * weight[0, 0]  # weighted number of elements
    sumy[0, 0] = query[0] * weight[0, 0]
    sumx[0, 0] = ref[0] * weight[0, 0]
    sumy2[0, 0] = query[0] ** 2 * weight[0, 0]
    sumx2[0, 0] = ref[0] ** 2 * weight[0, 0]
    sumxy[0, 0] = query[0] * ref[0] * weight[0, 0]
    cost[0, 0] = 0

    for i in range(n):
        for j in range(m):
            if cost[i, j] >= 0: # free
                for k in range(n_single):
                    ii = i - step_single[0, k]
                    jj = j - step_single[1, k]
                    if abs(cost[ii, jj]) < np.inf:  # free and set
                        rep_max = min(rep_step_ref[k, i], rep_step_query[k, j])
                        step_bool = 1
                        if rep_max < rep_lim:
                            step_bool = 0
                            for r in range(1, rep_max + 2):
                                if step[i - r * step_single[0, k], j - r * step_single[1, k]] == k:
                                    pass
                                else:
                                    step_bool = 1
                                    break

                        if step_bool == 1:
                            N_new = N[ii, jj] + 1 * weight[i, j]  # weighted number of elements
                            sumy_new = sumy[ii, jj] + query[j] * weight[i, j]
                            sumx_new = sumx[ii, jj] + ref[i] * weight[i, j]
                            sumy2_new = sumy2[ii, jj] + query[j] ** 2 * weight[i, j]
                            sumx2_new = sumx2[ii, jj] + ref[i] ** 2 * weight[i, j]
                            sumxy_new = sumxy[ii, jj] + query[j] * ref[i] * weight[i, j]

                            if N_new == 0:
                                a_new = 1
                                b_new = 0
                            elif (sumx2_new - sumx_new ** 2 / N_new) == 0 or (sumxy_new - sumx_new * sumy_new / N_new) == 0:
                                a_new = 1
                                b_new = (sumy_new - a_new * sumx_new) / N_new
                            else:
                                a_new = (sumxy_new - sumx_new * sumy_new / N_new) / (sumx2_new - sumx_new ** 2 / N_new)
                                b_new = (sumy_new - a_new * sumx_new) / N_new

                            cost_new = a_new ** 2 * sumx2_new - 2 * a_new * sumxy_new + sumy2_new - 2 * b_new * sumy_new + 2 * a_new * b_new * sumx_new + N_new * b_new ** 2
                            #cost_new = np.round(cost_new, 10)

                            if cost_new < cost[i, j]:
                                a[i, j] = a_new
                                b[i, j] = b_new
                                N[i, j] = N_new
                                sumx[i, j] = sumx_new
                                sumy[i, j] = sumy_new
                                sumy2[i, j] = sumy2_new
                                sumx2[i, j] = sumx2_new
                                sumxy[i, j] = sumxy_new
                                cost[i, j] = cost_new
                                step[i, j] = k

                            ###symmetry logic###
                            # elif cost_new == param["cost"][i,j]:
                            #    if i==1 and (stepx_single[k]==1 and stepy_single[k]==1): #nodig, verschil in gewicht??
                            #        update = True
                            #    elif i==(n-1) and (stepx_single[k]==0 and stepy_single[k]==1): #nodig, verschil in gewicht??
                            #        update = True
                for k in range(n_multiple):
                    ii = max(-1, i - step_multiple[2 * k, 0])
                    jj = max(-1, j - step_multiple[2 * k + 1, 0])
                    if abs(cost[ii, jj]) < np.inf:  # free and set
                        rep_max = min(rep_step_ref[n_single + k, i], rep_step_query[n_single + k, j])
                        step_bool = 1
                        if rep_max < rep_lim:
                            step_bool = 0
                            for r in range(1, rep_max + 2):
                                if step[max(-1, i - r * step_multiple[2 * k, 0]), max(-1, j - r * step_multiple[2 * k + 1, 0])] == (n_single + k):
                                    pass
                                else:
                                    step_bool = 1
                                    break

                        if step_bool == 1:
                            N_new = 0
                            sumy_new = 0
                            sumx_new = 0
                            sumy2_new = 0
                            sumx2_new = 0
                            sumxy_new = 0

                            for s in range(m_multiple):
                                if step_multiple[2 * k, s] == -1:
                                    break
                                i_s = ii + step_multiple[2 * k, s]
                                j_s = jj + step_multiple[2 * k + 1, s]

                                N_new += 1 * weight[i_s, j_s]
                                sumy_new += query[j_s] * weight[i_s, j_s]
                                sumx_new += ref[i_s] * weight[i_s, j_s]
                                sumy2_new += query[j_s] ** 2 * weight[i_s, j_s]
                                sumx2_new += ref[i_s] ** 2 * weight[i_s, j_s]
                                sumxy_new += query[j_s] * ref[i_s] * weight[i_s, j_s]

                            N_new = N_new * step_weight[k] + N[ii, jj]
                            sumy_new = sumy_new * step_weight[k] + sumy[ii, jj]
                            sumx_new = sumx_new * step_weight[k] + sumx[ii, jj]
                            sumy2_new = sumy2_new * step_weight[k] + sumy2[ii, jj]
                            sumx2_new = sumx2_new * step_weight[k] + sumx2[ii, jj]
                            sumxy_new = sumxy_new * step_weight[k] + sumxy[ii, jj]

                            if N_new == 0:
                                a_new = 1
                                b_new = 0
                            elif (sumx2_new - sumx_new ** 2 / N_new) == 0 or (sumxy_new - sumx_new * sumy_new / N_new) == 0:
                                a_new = 1
                                b_new = (sumy_new - a_new * sumx_new) / N_new
                            else:
                                a_new = (sumxy_new - sumx_new * sumy_new / N_new) / (sumx2_new - sumx_new ** 2 / N_new)
                                b_new = (sumy_new - a_new * sumx_new) / N_new

                            cost_new = a_new ** 2 * sumx2_new - 2 * a_new * sumxy_new + sumy2_new - 2 * b_new * sumy_new + 2 * a_new * b_new * sumx_new + N_new * b_new ** 2
                            #cost_new = np.round(cost_new, 10)

                            if cost_new < cost[i, j]:
                                a[i, j] = a_new
                                b[i, j] = b_new
                                N[i, j] = N_new
                                sumx[i, j] = sumx_new
                                sumy[i, j] = sumy_new
                                sumy2[i, j] = sumy2_new
                                sumx2[i, j] = sumx2_new
                                sumxy[i, j] = sumxy_new
                                cost[i, j] = cost_new
                                step[i, j] = n_single + k

    return (a, b, N, sumx, sumy, sumx2, sumy2, sumxy, cost[:-1,:-1], step[:-1,:-1])
