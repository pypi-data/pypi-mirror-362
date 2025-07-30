import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
#import scipy.stats as st
from dtw_flex.core_cython import dtw_cy
from dtw_flex.core.visual_select import plot_set
import copy 

class Test():
    def __init__(self, nref, nquery):
        self.nref = nref

    @property
    def nref(self):
        return self._nref

    @nref.setter
    def nref(self, nref_new = 1):
        print(nref_new)

        #if nref_new > 20:
        #    print("test")
        self._nref = nref_new

class Dtw():
    def __init__(self, nref_raw, nquery, name = ""):
        self.name = name

        self._nref = 0
        self.nref_raw = nref_raw
        self.ref = np.zeros(self.nref)
        self.wref, self.rep_ref = self.ref_setinit(self.nref, nquery)

        self._nquery = 0
        self.nquery = nquery
        self.query = np.zeros(nquery)
        self.wquery, self.rep_query = self.query_setinit(nquery)

        self.flag = np.array([])
        self.flag_cont = False
        self.lim_err = 0.5
        self.lim_amp = 10**-10

        self.constr_sym = []
        self.constr_disc = []
        self.constr_prop = []

    @property
    def nref(self):
        return self._nref

    @nref.setter
    def nref(self, nref_new):
        if not isinstance(nref_new, int):
            raise TypeError("nref should be an integer.")
        try:
            if not nref_new <= self.nquery:
                raise ValueError("length of reference series (including 2 endpoints) should be equal or smaller than length of query series")
        except AttributeError:
            pass
        
        self._nref = nref_new

    @property
    def nref_raw(self):
        return self._nref - 2
    
    @nref_raw.setter
    def nref_raw(self, nref_raw_new):
        self.nref = nref_raw_new + 2 #add 2 endpoints

    @property
    def nquery(self):
        return self._nquery

    @nquery.setter
    def nquery(self, nquery_new):
        if not isinstance(nquery_new, int):
            raise TypeError("nquery should be an integer.")
        try:
            if not nquery_new >= self.nref:
                raise ValueError("length of query series should be equal or larger than length of ref series")
        except AttributeError:
            pass
        
        self._nquery = nquery_new

    @property
    def ref(self):
        return self._ref

    @ref.setter
    def ref(self, ref_new):
        if not isinstance(ref_new, np.ndarray):
            raise TypeError("ref should be a numpy ndarray.")
        if not all([isinstance(el,float) for el in ref_new]):
            raise ValueError("ref should contain floats only.")
        if not len(ref_new) == self.nref:
            self.nref = len(ref_new)
            self.wref, self.rep_ref = self.ref_setinit(self.nref, self.nquery)

        self._ref = ref_new

    def ref_plotset(self, hide_endpoints = False):
        vals = {'ref': self.ref, 'wref': self.wref, 'rep_ref': self.rep_ref}
        range = [[0,1], [0,1], [min(self.rep_ref), max(max(self.rep_ref), 1)]]
        select = {'flag':self.flag}
        title = '''Customize reference points, reference weights and max datapoint repetition.\n Drag datapoints to desired position.\n select and track reference point with right mouse button'''
        plot_set(self, vals, range, select = select, title = title, hide_endpoints = hide_endpoints)

    def set_endpoints(self):
        ref_endpoint = (self.ref[1] + self.ref[-2])/2
        self.ref[0] = ref_endpoint
        self.ref[-1] = ref_endpoint

    def ref_setinit(self, nref, nquery):
        w = np.ones(nref)
        w_end = 0.25 #1 / ((nquery - (nref - 2)))
        w[0] = w_end
        w[-1] = w_end

        rep = np.zeros(nref, dtype=np.int32)
        rep_end = nquery - nref
        rep[0] = rep_end
        rep[-1] = rep_end

        return w, rep

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query_new):
        if not isinstance(query_new, np.ndarray):
            raise TypeError("query should be a numpy ndarray.")
        if not all([isinstance(el,float) for el in query_new]):
            raise ValueError("query should contain floats only.")
        if not len(query_new) == self.nquery:
            self.nquery = len(query_new)
            self.wquery, self.rep_query = self.query_setinit(self.nquery)

        self._query = query_new

    def query_plotset(self):
        vals = {'query': self.query, 'wquery': self.wquery}
        range = [[min(0, min(self.query)),max(1,max(self.query))],[0,1]] #[min(self.rep_query), max(max(self.rep_query), 1)]
        title = '''Customize query points and query weights.\n Drag datapoints to desired position. '''
        plot_set(self, vals, range, title=title)

    def query_setinit(self, nquery):
        w = np.ones(nquery)
        rep = np.zeros(nquery, dtype=np.int32)

        return w, rep

    @property
    def wref(self):
        return self._wref

    @wref.setter
    def wref(self, wref_new):
        if not isinstance(wref_new, np.ndarray):
            raise TypeError("wref should be a numpy ndarray.")
        if not all([isinstance(el,(np.integer,float)) for el in wref_new]):
            raise TypeError("wref should contain floats only.")
        if not len(wref_new) == self.nref:
            raise ValueError("wref and ref should have the same length.") #logic
        self._wref = wref_new

    @property
    def wquery(self):
        return self._wquery

    @wquery.setter
    def wquery(self, wquery_new):
        if not isinstance(wquery_new, np.ndarray):
            raise TypeError("wquery should be a numpy ndarray.")
        if not all([isinstance(el,(np.integer,float)) for el in wquery_new]):
            raise TypeError("wquery should contain floats only.")
        if not len(wquery_new) == self.nquery:
            raise ValueError("wquery and nquery should have the same length.") #logic
        self._wquery = wquery_new

    @property
    def rep_ref(self):
        return self._rep_ref

    @rep_ref.setter
    def rep_ref(self, rep_ref_new):
        if not isinstance(rep_ref_new, np.ndarray):
            raise TypeError("rep_ref should be a numpy ndarray.")
        if not all([isinstance(el,np.integer) for el in rep_ref_new]):
            raise TypeError("rep_ref should contain integers only.")
        if not len(rep_ref_new) == self.nref:
            raise ValueError("rep_ref and ref should have the same length.")

        self._rep_ref = rep_ref_new

    @property
    def rep_query(self):
        return self._rep_query

    @rep_query.setter
    def rep_query(self, rep_query_new):
        if not isinstance(rep_query_new, np.ndarray):
            raise TypeError("rep_query should be a numpy ndarray.")
        if not all([isinstance(el,np.integer) for el in rep_query_new]):
            raise TypeError("rep_query should contain integers only.")
        if not len(rep_query_new) == self.nquery:
            raise ValueError("rep_query and nquery should have the same length.")
        self._rep_query = rep_query_new

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, flag_new):
        if not isinstance(flag_new, np.ndarray):
            raise TypeError("flag should be a numpy ndarray")
        if not all([isinstance(el,np.integer) for el in flag_new]):
            raise TypeError("flag should contain integers only.")
        self._flag = flag_new

    @property
    def flag_cont(self):
        return self._flag_cont

    @flag_cont.setter
    def flag_cont(self, flag_cont_new):
        if not isinstance(flag_cont_new, bool):
            raise TypeError("flag_cont should be a boolean")
        self._flag_cont = flag_cont_new

    @property
    def lim_err(self):
        return self._lim_err

    @lim_err.setter
    def lim_err(self, lim_err_new):
        if not isinstance(lim_err_new, (int,float)):
            raise TypeError("err_lim should be a float")
        self._lim_err = lim_err_new

    @property
    def lim_amp(self):
        return self._lim_amp

    @lim_amp.setter
    def lim_amp(self, lim_amp_new):
        if not isinstance(lim_amp_new, (int,float)):
            raise TypeError("err_lim should be a float")
        self._lim_amp = lim_amp_new

    @property
    def constr_sym(self):
        return self._constr_sym

    @constr_sym.setter
    def constr_sym(self, constr_sym_new):
        if not isinstance(constr_sym_new, list):
            raise TypeError("constr_sym should be a list.")
        for dict in constr_sym_new:
            if len(dict) != 4:
                raise KeyError("each symmetry constraint should contain 4 keys.")
            for key in dict.keys():
                if key not in ['id_start','id_stop','reps','weight']:
                    raise KeyError("dictionary key {0} in constr_sym "
                                   "is not a valid key ('id_start','id_stop','reps','weight')".format(key))
                if key in ['id_start','id_stop']:
                    if not isinstance(dict[key],int):
                        raise ValueError("constr_sym id_start/stop should be an integer.")
                if key == "reps":
                    if not isinstance(dict[key],list):
                        raise ValueError("constr_sym reps should be a list")
                    if not all([isinstance(el,int) for el in dict[key]]):
                        raise TypeError("constr_sym reps should contain integers only.")
                if key == 'weight':
                    if dict[key] == 'uniform':
                        pass
                    elif not isinstance(dict[key],(int,float)):
                        raise ValueError("constr_sym weight should be a float.")
        self._constr_sym = constr_sym_new

    @property
    def constr_disc(self):
        return self._constr_disc

    @constr_disc.setter
    def constr_disc(self, constr_disc_new):
        if not isinstance(constr_disc_new, list):
            raise TypeError("constr_disc should be a list")
        for dict in constr_disc_new:
            if len(dict) != 4:
                raise KeyError("each discontinuity constraint should contain 4 keys.")
            for key in dict.keys():
                if key not in ['id_start','id_stop','reps','weight']:
                    raise KeyError("dictionary key {0} in constr_disc "
                                   "is not a valid key ('id_start','id_stop','reps','weight')".format(key))
                if key in ['id_start','id_stop']:
                    if not isinstance(dict[key],int):
                        raise ValueError("constr_disc id_start/stop should be an integer.")
                if key == "reps":
                    if not isinstance(dict[key],list):
                        raise ValueError("constr_disc reps should be a list.")
                    if not all([isinstance(el,int) for el in dict[key]]):
                        raise TypeError("constr_disc reps should contain integers only.")
                if key == 'weight':
                    if dict[key] == 'uniform':
                        pass
                    elif not isinstance(dict[key],(int,float)):
                        raise ValueError("constr_disc weight should be a float.")
        self._constr_disc = constr_disc_new

    @property
    def constr_prop(self):
        return self._constr_prop

    @constr_prop.setter
    def constr_prop(self, constr_prop_new):
        if not isinstance(constr_prop_new, list):
            raise TypeError("constr_prop should be a list.")
        for dict in constr_prop_new:
            if len(dict) != 4:
                raise KeyError("each proportionality constraint should contain 4 keys.")
            for key in dict.keys():
                if key not in ['id_start','id_stop','reps','weight']:
                    raise KeyError("dictionary key {0} in constr_prop "
                                   "is not a valid key ('id_start','id_stop','reps','weight')".format(key))
                if key in ['id_start','id_stop']:
                    if not isinstance(dict[key],int):
                        raise ValueError("constr_prop id_start/stop should be an integer.")
                if key == "reps":
                    if not isinstance(dict[key],list):
                        raise ValueError("constr_prop reps should be a list.")
                    if not all([isinstance(el,int) for el in dict[key]]):
                        raise TypeError("constr_prop reps should contain integers only.")
                if key == 'weight':
                    if dict[key] == 'uniform':
                        pass
                    elif not isinstance(dict[key],(int,float)):
                        raise ValueError("constr_prop weight should be a float.")
        self._constr_prop = constr_prop_new

    def __str__(self):
        return self.name

    def prep(self):
        prep_res = dtw_prep(wref=self.wref, wquery=self.wquery, rep_ref=self.rep_ref, rep_query=self.rep_query,
                        symmetry=self.constr_sym, discontinuity=self.constr_disc, proportionality=self.constr_prop)
        self.cost, self.weight, self.step_single, self.step_multiple, self.step_weight, self.rep_step_ref, self.rep_step_query = prep_res
        return prep_res

    def backward_cy(self):
        backward_res = dtw_cy.dtw_backward(query=self.query, ref=self.ref, cost=self.cost.copy(), weight=self.weight,
                               step_single=self.step_single, step_multiple=self.step_multiple,
                               step_weight=self.step_weight, rep_step_ref=self.rep_step_ref,
                               rep_step_query=self.rep_step_query)
        self.a, self.b, self.N, self.sumx, self.sumy, self.sumx2, self.sumy2, self.sumxy, self.cost, self.step = backward_res
        return backward_res
    
    def backward(self):
        backward_res = dtw_backward(query=self.query, ref=self.ref, cost=self.cost.copy(), weight=self.weight,
                               step_single=self.step_single, step_multiple=self.step_multiple,
                               step_weight=self.step_weight, rep_step_ref=self.rep_step_ref,
                               rep_step_query=self.rep_step_query)
        self.a, self.b, self.N, self.sumx, self.sumy, self.sumx2, self.sumy2, self.sumxy, self.cost, self.step = backward_res
        return backward_res

    def path(self):
        path_res = dtw_path(step=self.step, step_single=self.step_single, step_multiple=self.step_multiple)
        self.id_ref, self.id_query = path_res
        return path_res

    def feat_params(self):
        feat_params_res = feat_params(query=self.query, bounds_ref=[1, self.nref - 2], id_query=self.id_query, id_ref=self.id_ref,
                        sumx=self.sumx, sumy=self.sumy, sumx2=self.sumx2, sumy2=self.sumy2, sumxy=self.sumxy, N=self.N, error_rel=True)
        self.a_feat, self.b_feat, self.error = feat_params_res
        return feat_params_res

    def run_dtw(self, plt_fit = True, plt_match = True):
        self.prep()
        self.backward()
        self.path()
        self.feat_params()
        if plt_fit == True:
            plot_fit(self.query, self.ref, self.id_ref, self.id_query, a=self.a_feat, b=self.b_feat)
        if plt_match == True:
            plot_match(self.query, self.flag, self.id_ref, self.id_query)

    def _roll_core(self, data):
        df = dtw_roll(data = data, nquery=self.nquery, ref= self.ref, cost = self.cost, weight = self.weight, step_single = self.step_single,
                           step_multiple = self.step_multiple, step_weight = self.step_weight, rep_step_ref = self.rep_step_ref,
                           rep_step_query = self.rep_step_query, flag = self.flag, flag_cont = self.flag_cont, lim_err = self.lim_err, lim_amp = self.lim_amp)
        return df

    def roll(self, data):
        self.prep()
        df_dtw = self._roll_core(data)
        df_dtw_unique = df_dtw.copy()
        df_dtw_unique.loc[df_dtw.duplicated(['group']), ['dtw_err', 'dtw_amp', 'dtw']] = np.nan
        
        return df_dtw_unique
    
    def roll_blocks(self, data_blocks):
        self.prep()
        df_dtw = pd.DataFrame()
        for block in data_blocks.values():
            df_roll = self._roll_core(block)
            df_dtw = pd.concat([df_dtw, df_roll])

        df_dtw_unique = df_dtw.copy()
        df_dtw_unique.loc[df_dtw.duplicated(['group']), ['dtw_err', 'dtw_amp', 'dtw']] = np.nan
        return df_dtw, df_dtw_unique

def find_last_index(lst, value):
    #find last index
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1

def detrend(seq, trend = ""):
    """
    :param seq: data sequence
    :param trend: "linear", "quadratic" (linear & quadratic)
    :return: detrended sequence
    """
    if trend == "quadratic":
        #trend = a*x+b*x**2
        #F1 = median(diff(series))
        #F2 = median(diff2(series))
        #minimize: [mean(diff(trend)) - F1]**2 + [mean(diff2(trend)) - F2]**2, given sign(a) == sign(b) or -a*b <= 0
        #solve lagrangian (3 cases)

        diff1 = np.diff(seq)
        diff2 = np.diff(diff1)
        F1 = np.median(diff1) #scipy.stats.trim_mean(diff1,0.35) 
        F2 = np.median(diff2) #scipy.stats.trim_mean(diff2,0.35)
        N = len(seq)
        x1 = 0
        x2 = 1
        x1N = N-2
        xN = N-1

        def case1():
            a = 0
            b = (-F1*N*x1**2 + F1*N*xN**2 + F1*x1**2 - F1*xN**2 + F2*N*x1**2 - F2*N*x1N**2 - F2*N*x2**2 + F2*N*xN**2 - 2*F2*x1**2 + 2*F2*x1N**2 + 2*F2*x2**2 - 2*F2*xN**2)/(2*x1**4 - 2*x1**2*x1N**2 - 2*x1**2*x2**2 + x1N**4 + 2*x1N**2*x2**2 - 2*x1N**2*xN**2 + x2**4 - 2*x2**2*xN**2 + 2*xN**4)
            lam = 2*(F1*N*x1 - F1*N*xN - F1*x1 + F1*xN - F2*N*x1 + F2*N*x1N + F2*N*x2 - F2*N*xN + 2*F2*x1 - 2*F2*x1N - 2*F2*x2 + 2*F2*xN + b*(2*x1**3 - x1**2*x1N - x1**2*x2 - x1*x1N**2 - x1*x2**2 + x1N**3 + x1N**2*x2 - x1N**2*xN + x1N*x2**2 - x1N*xN**2 + x2**3 - x2**2*xN - x2*xN**2 + 2*xN**3))/b
            return a,b,lam
        def case2():
            b = 0
            a = (-F1*N*x1 + F1*N*xN + F1*x1 - F1*xN + F2*N*x1 - F2*N*x1N - F2*N*x2 + F2*N*xN - 2*F2*x1 + 2*F2*x1N + 2*F2*x2 - 2*F2*xN)/(2*x1**2 - 2*x1*x1N - 2*x1*x2 + x1N**2 + 2*x1N*x2 - 2*x1N*xN + x2**2 - 2*x2*xN + 2*xN**2)
            lam = 2*(F1*N*x1**2 - F1*N*xN**2 - F1*x1**2 + F1*xN**2 - F2*N*x1**2 + F2*N*x1N**2 + F2*N*x2**2 - F2*N*xN**2 + 2*F2*x1**2 - 2*F2*x1N**2 - 2*F2*x2**2 + 2*F2*xN**2 + a*(2*x1**3 - x1**2*x1N - x1**2*x2 - x1*x1N**2 - x1*x2**2 + x1N**3 + x1N**2*x2 - x1N**2*xN + x1N*x2**2 - x1N*xN**2 + x2**3 - x2**2*xN - x2*xN**2 + 2*xN**3))/a
            return a,b,lam
        def case3():
            a = (-F1*N*x1**2 + F1*N*x1N**2 + F1*N*x2**2 - F1*N*xN**2 + F1*x1**2 - F1*x1N**2 - F1*x2**2 + F1*xN**2 - F2*N*x1**2 + F2*N*xN**2 + 2*F2*x1**2 - 2*F2*xN**2)/(x1**2*x1N + x1**2*x2 - 2*x1**2*xN - x1*x1N**2 - x1*x2**2 + 2*x1*xN**2 + x1N**2*xN - x1N*xN**2 + x2**2*xN - x2*xN**2)
            b = (F1*N*x1 - F1*N*x1N - F1*N*x2 + F1*N*xN - F1*x1 + F1*x1N + F1*x2 - F1*xN + F2*N*x1 - F2*N*xN - 2*F2*x1 + 2*F2*xN)/(x1**2*x1N + x1**2*x2 - 2*x1**2*xN - x1*x1N**2 - x1*x2**2 + 2*x1*xN**2 + x1N**2*xN - x1N*xN**2 + x2**2*xN - x2*xN**2)
            lam = 0
            return a,b,lam

        cases ={"case1":case1(),"case2":case2(),"case3":case3()}
        for case in cases.keys():
            a,b,lam = cases[case]
            if lam >= 0:
                break

        trend = a * np.arange(0,N) + b * np.arange(0,N)**2
        seq_corr = seq - trend

    elif trend == "linear":

        diff1 = np.diff(seq)
        diff1 = diff1.astype("float64")
        diff1_corr = diff1 - np.mean(diff1)
        seq_corr = seq.copy()
        for id,step in enumerate(diff1_corr,start = 0):
            seq_corr[id+1] = seq_corr[id] + step

    return seq_corr

def dtw_prep(wref, wquery, rep_ref, rep_query, symmetry=[], discontinuity=[], proportionality=[]):
    '''
    dtw_prep creates all necessary input for the dtw algorithm
    :param wref: weight for each point in the reference series.
    :param wquery: weight for each point in the query series.
    :param rep_ref: allowable repetition for each point in the reference series.
            e.g. repetition value equal to 0 means the point will match maximum once with a query point
    :param rep_query: allowable repetition for each point in the query series.
    :param symmetry: list of tuples. each tuple consists of the ref starting point, ref ending point, list with allowable repetitions and step weight
            The algorithm is greedy and will not generate a perfectly symmetric reference section (defining optimal match) which consists of more than one data point repetition
            A symmetry constraint between a given start and end point solves this issue if perfect symmetry with multiple (>1) pont repetitions is needed.
    :param discontinuity: list of tuples. each tuple consists of the ref starting point, ref ending point, list with allowable jumps and step weight
            A discontinuity consraint allows a data jump (over the query series) between a given starting and ending ref point
    :param proportionality: list of tuples. each tuple consists of the ref starting point, ref ending point, list with allowable repetitions and step weight.
            A proportionality constraint forces the ref series to match the query in a proportionate manner. It also disables all other step alternatives for the given section.
            If we set the repetition parameter to 3 in a given section. each ref point in that section will be repeated exaclty 3 times and optimally matched with the query series.
            So there will be no distortion in the given section.
    :return: cost, weight, step_single, step_multiple, step_weight, rep_step_ref, rep_step_query
        cost: initialized cost matrix
        weight: weight matrix
        step_single = matrix with single step
        step_multiple = matrix with complex data steps
        step_weight = penalities/weights for multiple/complex steps
        rep_step_ref = matrix with allowable repetitions for all steps (rows) and each ref data point (columns)
        rep_step_query = matrix with allowable repetitions for all steps (rows) and each query data point (columns)

    '''
    ### TODO: integrate step_single and step_multiple into a one step_pattern matrix. One can use step_weight (as matrix) to distinguish between single and complex steps

    ###intiate###
    n,m = len(wref),len(wquery)
    rep_lim = max(m,n)-1
    step_single = np.array([[0,1,1],[1,0,1]])
    n_single = np.shape(step_single)[1]
    single_tuple = [(i,j) for i,j in zip(step_single[0,:], step_single[1,:])] #np.concatenate([[stepx_single, stepy_single]])
    step_multiple = np.zeros((0,0),dtype=int)
    step_weight = np.array([])

    step_prop = {}
    step_sym = {}
    step_disc = {}

    rep_step_ref = np.ones((n_single,n),dtype=int)*rep_lim
    rep_step_query = np.ones((n_single,m),dtype=int)*rep_lim
    rep_step_prop = {}
    rep_step_sym = {}
    rep_step_disc = {}

    ###create data weight matrix###
    weight = np.ones((n,m))
    for i in np.arange(n):
        for j in np.arange(m):
            weight[i,j] = min(wref[i],wquery[j]) #if conflict, take the minimum

    ###create cost matrix###
    cost = np.ones((n+1,m+1)) * np.inf
    cost[:,m] = -np.inf
    cost[n,:] = -np.inf

    #if cumulative repetition of ref. is smaller than the query length, we can exclude these points (in most cases, except discontinuities)
    for i in np.arange(n):
        id = sum(rep_ref[:i+1] + 1) #no validation that rep_ref[0,:] actually corresponds with (0,1)
        if id < m:
            cost[i, id:] = -np.inf
        else:
            break

    for i in np.arange(n-1, -1, -1):
        id = sum(rep_ref[i:] + 1)
        if id < m:
            cost[i, : m - id] = -np.inf
        else:
            break

    #if cumulative repetition of query is smaller than the ref. length, we can exclude these points (in most cases, except discontinuities)
    for j in np.arange(m):
        id = sum(rep_query[:j+1] + 1)
        if id < n:
            cost[id:, j] = -np.inf
        else:
            break

    for j in np.arange(m-1, -1, -1):
        id = sum(rep_query[j:] + 1)
        if id < n:
            cost[:n - id, j] = -np.inf
        else:
            break

    ###set single step repetitions###
    for id_single,single in enumerate(single_tuple):
        if single == (0,1):
            rep_step_ref[id_single,:] = rep_ref - 1
        elif single == (1,0):
            rep_step_query[id_single,:] = rep_query - 1
    ###set symmetry steps###

    for sym in symmetry:
        #for i1_ref, i2_ref in zip(np.arange(sym[0],sym[1]),np.arange(sym[0]+1,sym[1]+1)):
        for rep in sym['reps']:
            if rep not in step_sym.keys():
                stepx_sym = np.ones(rep) #np.concatenate([np.array([0]),np.ones(rep)])#np.concatenate([np.zeros(rep-1),np.ones(rep)])
                stepy_sym = np.arange(1,len(stepx_sym)+1)
                step_sym_new = np.concatenate([[stepx_sym, stepy_sym]])
                step_sym_new = np.int32(np.fliplr(step_sym_new))

                step_sym[rep] = step_sym_new
                rep_step_sym[rep] = - np.ones(n,dtype=int)
                if sym['weight'] == 'uniform':
                    step_weight = np.append(step_weight, 1)
                else:
                    step_weight = np.append(step_weight, sym['weight'])

            rep_step_sym[rep][sym['id_start']:sym['id_stop']+1] = rep_lim

    for elem in rep_step_sym.values():
        rep_step_ref = np.concatenate([rep_step_ref,elem.reshape(1,n)])
    for elem in step_sym.values():
        _, dimy = step_multiple.shape
        _, dimy_new = elem.shape
        if dimy_new > dimy:
            step_multiple = np.pad(step_multiple, ((0, 0), (0, dimy_new-dimy)), constant_values=-1)
            step_multiple = np.concatenate([step_multiple,elem])
        else:
            elem = np.pad(elem, ((0, 0), (0, dimy-dimy_new)), constant_values=-1)
            step_multiple = np.concatenate([step_multiple,elem])

    ###set discontinuity steps###
    for disc in discontinuity:
        for jump in disc['reps']:
            if jump not in step_disc.keys():
                stepx_disc = np.array([1,1,2,2])
                stepy_disc = np.array([1,2,3 + jump,4 + jump])
                step_disc_new = np.concatenate([[stepx_disc, stepy_disc]])
                step_disc_new = np.int32(np.fliplr(step_disc_new))

                step_disc[jump] = step_disc_new
                rep_step_disc[jump] = - np.ones(n,dtype=int)
                if disc['weight'] == 'uniform':
                    step_weight = np.append(step_weight, (2 + jump)/2)
                else:
                    step_weight = np.append(step_weight, disc['weight'])
            rep_step_disc[jump][disc['id_start']+1:disc['id_stop']+1] = 0

    for elem in rep_step_disc.values():
        rep_step_ref = np.concatenate([rep_step_ref,elem.reshape(1,n)])
    for elem in step_disc.values():
        _, dimy = step_multiple.shape
        _, dimy_new = elem.shape
        if dimy_new > dimy:
            step_multiple = np.pad(step_multiple, ((0, 0), (0, dimy_new-dimy)), constant_values=-1)
            step_multiple = np.concatenate([step_multiple,elem])
        else:
            elem = np.pad(elem, ((0, 0), (0, dimy-dimy_new)), constant_values=-1)
            step_multiple = np.concatenate([step_multiple,elem])

    ###set proportionality steps###
    for prop in proportionality:
        for rep in prop['weight']:
            if rep not in step_prop.keys():
                #check if repetition constraint is consisten with proportionality constraint
                if any(rep_ref[prop['id_start']:prop['id_stop']+1] < rep):
                    raise ValueError("Allowable replicates of reference points less than proportionality constraint")
                elif prop['id_start'] == 0 or prop['id_stop'] == n-1:
                    raise ValueError("proportionality constraint not allowed in the endpoints")
                stepx_prop = np.zeros((1), dtype=int)
                for i in range(1,(prop['id_stop'] - prop['id_start'])+2):
                    stepx_prop = np.concatenate([stepx_prop, np.ones(rep+1,dtype=int)*(i)])
                stepx_prop = np.concatenate([stepx_prop, np.ones(1,dtype=int)*(i+1)])
                stepy_prop = np.arange(1,len(stepx_prop)+1)
                step_prop_new = np.concatenate([[stepx_prop, stepy_prop]]) #create extended vector
                step_prop_new = np.int32(np.fliplr(step_prop_new))

                step_prop[rep] = step_prop_new
                rep_step_prop[rep] = - np.ones(n,dtype=int)
                if prop[3] == 'uniform':
                    step_weight = np.append(step_weight, 1)
                else:
                    step_weight = np.append(step_weight, prop['weight'])

            rep_step_prop[rep][prop['id_stop']+1] = 0
        #exclude any other step pattern which could interfere with the proportionality constraint
        for i in range(prop['id_start'],prop['id_stop']+1):
            rep_step_ref[:,i] = -1
        for i,val in enumerate(step_single[0,:]):
            if val > 0:
                rep_step_ref[i,prop['id_stop']+1] = -1
        for i,row in enumerate(step_multiple[::2,:]):
            if row[0] > 0:
                rep_step_ref[step_single.shape[1]+i,prop['id_stop']+1] = -1


    for elem in rep_step_prop.values():
        rep_step_ref = np.concatenate([rep_step_ref, elem.reshape(1, n)])
    for elem in step_prop.values():
        _, dimy = step_multiple.shape
        _, dimy_new = elem.shape
        if dimy_new > dimy:
            step_multiple = np.pad(step_multiple, ((0, 0), (0, dimy_new-dimy)), constant_values=-1)
            step_multiple = np.concatenate([step_multiple,elem])
        else:
            elem = np.pad(elem, ((0, 0), (0, dimy-dimy_new)), constant_values=-1)
            step_multiple = np.concatenate([step_multiple,elem])
            #(step_single == np.array([[1], [0]])).all(axis=0).any()

    dim_diff = np.shape(rep_step_ref)[0] - np.shape(rep_step_query)[0]
    rep_step_query = np.pad(rep_step_query, ((0, dim_diff), (0, 0)), constant_values=rep_lim)

    return (cost, weight, step_single, step_multiple, step_weight, rep_step_ref, rep_step_query)

def dtw_path(step, step_single, step_multiple):
    '''
    dtwp_path: retract the dtw path from the result step matrix and the allowable step patterns
    :param step: result step matrix
    :param step_single: single stap patterns
    :param step_multiple: multi step patterns
    :return: id_ref, id_query
        id_ref: dtw path ref series (ref ids)
        id_query: dtw path query series (query ids)
    '''
    i_old = step.shape[0] - 1 #last row index
    j_old = step.shape[1] - 1 #last column index
    id_ref = [i_old]
    id_query = [j_old]
    n_single = np.shape(step_single)[1]
    m_multiple = np.shape(step_multiple)[1]

    while True:
        i = id_ref[-1]
        j = id_query[-1]

        if step[i,j] < n_single:
            i_new = i - step_single[0,step[i, j]]
            j_new = j - step_single[1,step[i, j]]
            id_ref.append(i_new)
            id_query.append(j_new)
        else:
            ii = i - step_multiple[2*(step[i, j]-n_single),0]
            jj = j - step_multiple[2*(step[i, j]-n_single)+1,0]
            for k in range(1,m_multiple):
                if step_multiple[2*(step[i, j]-n_single), k] < 0:
                    break
                i_new = ii + step_multiple[2*(step[i, j]-n_single), k]
                j_new = jj + step_multiple[2*(step[i, j]-n_single)+1, k]
                id_ref.append(i_new)
                id_query.append(j_new)
            i_new = ii
            j_new = jj
            id_ref.append(i_new)
            id_query.append(j_new)
        if i_new == 0 and j_new == 0:
            break

    id_ref.reverse()
    id_query.reverse()

    return (id_ref, id_query)

def dtw_backward(query, ref, cost, weight, step_single, step_multiple, step_weight, rep_step_ref, rep_step_query):
    '''
    dtw_backward: scaled dtw algorithm with backward propagation. Find optimal match between (a*ref + b) and query, given weight and step constraints
    :param query: query series
    :param ref: reference series
    :param cost: initiated cost matrix
    :param weight: weight matrix
    :param step_single: single step patterns
    :param step_multiple: complex/multi-step patterns
    :param step_weight: complex/multi-step patterns weight
    :param rep_step_ref: allowable repetition for each step (row) and each reference point (column)
    :param rep_step_query : allowable repetition for each step (row) and each query point (column)
    :return: (param["a"], param["b"], param["N"], param["sumx"], param["sumy"], param["sumx2"], param["sumy2"], param["sumxy"], param["cost"][:-1,:-1], param["step"][:-1,:-1])
        param["a"] =  scale matrix
        param["b"] =  offset matrix
        param["N"] = (weighted) step number
        param["sumx"] = sum of (weighted) reference values
        param["sumy"] = sum of (weighted) query values
        param["sumx2"] = sum of (weighted) squared reference values
        param["sumy2"] = sum of (weighted) squared query values
        param["sumxy"] = sum of (weighted) ref and query product values
        param["cost"][:-1,:-1] = cost matrix
        param["step"][:-1,:-1]) = step path matrix
    '''
    n, m = len(ref), len(query)
    rep_lim = max(m, n) - 1
    n_single = np.shape(step_single)[1]
    n_multiple = int(np.shape(step_multiple)[0] / 2)
    m_multiple = np.shape(step_multiple)[1]

    param_names = ["a", "b", "N", "sumx", "sumy", "sumx2", "sumy2", "sumxy", "cost"]
    param = {name: None for name in param_names}
    param["a"] = np.ones((n, m))
    param["b"] = np.zeros((n, m))
    param["N"] = np.zeros((n, m))
    param["sumx"] = np.zeros((n, m))
    param["sumy"] = np.zeros((n, m))
    param["sumy2"] = np.zeros((n, m))
    param["sumx2"] = np.zeros((n, m))
    param["sumxy"] = np.zeros((n, m))
    param["cost"] = cost #np.pad(cost, ((1, 0), (1, 0)), constant_values=(-np.inf))
    param["step"] = -np.ones((n + 1, m + 1), dtype=int)

    param["N"][0, 0] = 1 * weight[0, 0]  # weighted number of elements
    param["sumy"][0, 0] = query[0] * weight[0, 0]
    param["sumx"][0, 0] = ref[0] * weight[0, 0]
    param["sumy2"][0, 0] = query[0] ** 2 * weight[0, 0]
    param["sumx2"][0, 0] = ref[0] ** 2 * weight[0, 0]
    param["sumxy"][0, 0] = query[0] * ref[0] * weight[0, 0]
    param["cost"][0, 0] = 0

    id = np.ndindex(n, m)

    for i, j in id:
        if param["cost"][i, j] >= 0: # free
            for k in range(n_single):
                ii = i - step_single[0, k]
                jj = j - step_single[1, k]
                if abs(param["cost"][ii, jj]) < np.inf:  # free and set
                    rep_max = min(rep_step_ref[k, i], rep_step_query[k, j])
                    step_bool = 1
                    if rep_max < rep_lim:
                        step_bool = 0
                        for r in range(1, rep_max + 2):
                            if param["step"][i - r * step_single[0, k], j - r * step_single[1, k]] == k:
                                pass
                            else:
                                step_bool = 1
                                break

                    if step_bool == 1:
                        N_new = param["N"][ii, jj] + 1 * weight[i, j]  # weighted number of elements
                        sumy_new = param["sumy"][ii, jj] + query[j] * weight[i, j]
                        sumx_new = param["sumx"][ii, jj] + ref[i] * weight[i, j]
                        sumy2_new = param["sumy2"][ii, jj] + query[j] ** 2 * weight[i, j]
                        sumx2_new = param["sumx2"][ii, jj] + ref[i] ** 2 * weight[i, j]
                        sumxy_new = param["sumxy"][ii, jj] + query[j] * ref[i] * weight[i, j]

                        if N_new == 0:
                            a_new = 1
                            b_new = 0
                        elif (sumx2_new - sumx_new ** 2 / N_new) == 0 or (sumxy_new - sumx_new * sumy_new / N_new) == 0:
                            a_new = 1
                            b_new = (sumy_new - a_new * sumx_new) / N_new
                        else:
                            a_denom = (sumx2_new - sumx_new ** 2 / N_new)
                            a_new = (sumxy_new - sumx_new * sumy_new / N_new) / a_denom
                            b_new = (sumy_new - a_new * sumx_new) / N_new

                        cost_new = a_new ** 2 * sumx2_new - 2 * a_new * sumxy_new + sumy2_new - 2 * b_new * sumy_new + 2 * a_new * b_new * sumx_new + N_new * b_new ** 2
                        cost_new = np.round(cost_new, 10)

                        if cost_new < param["cost"][i, j]:
                            param["a"][i, j] = a_new
                            param["b"][i, j] = b_new
                            param["N"][i, j] = N_new
                            param["sumx"][i, j] = sumx_new
                            param["sumy"][i, j] = sumy_new
                            param["sumy2"][i, j] = sumy2_new
                            param["sumx2"][i, j] = sumx2_new
                            param["sumxy"][i, j] = sumxy_new
                            param["cost"][i, j] = cost_new
                            param["step"][i, j] = k

                        ###symmetry logic###
                        # elif cost_new == param["cost"][i,j]:
                        #    if i==1 and (stepx_single[k]==1 and stepy_single[k]==1): #nodig, verschil in gewicht??
                        #        update = True
                        #    elif i==(n-1) and (stepx_single[k]==0 and stepy_single[k]==1): #nodig, verschil in gewicht??
                        #        update = True
            for k in range(n_multiple):
                ii = max(-1, i - step_multiple[2 * k, 0])
                jj = max(-1, j - step_multiple[2 * k + 1, 0])
                if abs(param["cost"][ii, jj]) < np.inf:  # free and set
                    rep_max = min(rep_step_ref[n_single + k, i], rep_step_query[n_single + k, j])
                    step_bool = 1
                    if rep_max < rep_lim:
                        step_bool = 0
                        for r in range(1, rep_max + 2):
                            if param["step"][max(-1, i - r * step_multiple[2 * k, 0]), max(-1, j - r * step_multiple[2 * k + 1, 0])] == (n_single + k):
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

                        N_new = N_new * step_weight[k] + param["N"][ii, jj]
                        sumy_new = sumy_new * step_weight[k] + param["sumy"][ii, jj]
                        sumx_new = sumx_new * step_weight[k] + param["sumx"][ii, jj]
                        sumy2_new = sumy2_new * step_weight[k] + param["sumy2"][ii, jj]
                        sumx2_new = sumx2_new * step_weight[k] + param["sumx2"][ii, jj]
                        sumxy_new = sumxy_new * step_weight[k] + param["sumxy"][ii, jj]

                        #to_do: calculate a (multiplier) and b (offset) before applying step_weight.
                        #Hereafter one can penalize steps by introducing step_weight in the cost calculation

                        if N_new == 0:
                            a_new = 1
                            b_new = 0
                        elif (sumx2_new - sumx_new ** 2 / N_new) == 0 or (sumxy_new - sumx_new * sumy_new / N_new) == 0:
                            a_new = 1
                            b_new = (sumy_new - a_new * sumx_new) / N_new
                        else:
                            a_denom = (sumx2_new - sumx_new ** 2 / N_new)
                            a_new = (sumxy_new - sumx_new * sumy_new / N_new) / a_denom
                            b_new = (sumy_new - a_new * sumx_new) / N_new

                        cost_new = a_new ** 2 * sumx2_new - 2 * a_new * sumxy_new + sumy2_new - 2 * b_new * sumy_new + 2 * a_new * b_new * sumx_new + N_new * b_new ** 2
                        cost_new = np.round(cost_new, 10)

                        if cost_new < param["cost"][i, j]:
                            param["a"][i, j] = a_new
                            param["b"][i, j] = b_new
                            param["N"][i, j] = N_new
                            param["sumx"][i, j] = sumx_new
                            param["sumy"][i, j] = sumy_new
                            param["sumy2"][i, j] = sumy2_new
                            param["sumx2"][i, j] = sumx2_new
                            param["sumxy"][i, j] = sumxy_new
                            param["cost"][i, j] = cost_new
                            param["step"][i, j] = n_single + k

    return (param["a"], param["b"], param["N"], param["sumx"], param["sumy"], param["sumx2"], param["sumy2"], param["sumxy"], param["cost"][:-1,:-1], param["step"][:-1,:-1])

def calc_param(seq_y,seq_x):
    '''
    calc_param: calculate optimal scale and offset for 2 data sequences
    :param seq_y: first sequence
    :param seq_x: second sequence
    :return: a, b
        a = scale
        b = offset
    '''
    if len(seq_y) != len(seq_x):
        raise ValueError("list seq_x and seq_y must have the same length")

    sumx = np.sum(seq_x)
    sumy = np.sum(seq_y)
    sumxy = np.sum(seq_y*seq_x)
    sumx2 = np.sum(seq_x*seq_x)
    sum2xy = 0
    sum2xx = 0
    N = len(seq_y)

    for i in range(N):
        for j in range(N):
            sum2xy += seq_y[i]*seq_x[j]
            sum2xx += seq_x[i] * seq_x[j]

    a = (sumxy - sum2xy/N)/(sumx2 - sum2xx/N)
    b = ( sumy - a * sumx )/N

    return a,b

def feat_params(query, bounds_ref, id_query, id_ref, sumx, sumy, sumx2, sumy2, sumxy, N, error_rel=True):
    '''
    feat_params: calculate parameters and error for a bounded (or partial) reference sequence
        and its correspondent partial query sequence
    :param query: query series
    :param id_query: id path query series
    :param id_ref: id path ref series
    :param bounds_ref: id bounds for the reference series.
    :param sumx: sum of (weighted) reference values
    :param sumy: sum of (weighted) query values
    :param sumx2: sum of (weighted) squared reference values
    :param sumy2: sum of (weighted) squared query values
    :param sumxy: sum of (weighted) ref and query product values
    :param N: (weighted) step number
    :param error_rel: bool calculate relative error
    :return: a, b, error
        a: scale
        b: offset
        error: (relative )error
    '''

    path_lbound = id_ref.index(bounds_ref[0]) #dtw path left bound index
    path_rbound = find_last_index(id_ref, bounds_ref[1]) #dtw path right bound index

    #feat_start: subtract one from the index, otherwise the first value of the data serie will be lost in the difference of summed parameters!
    feat_start = (id_ref[path_lbound - 1], id_query[path_lbound - 1])
    feat_end = (id_ref[path_rbound], id_query[path_rbound])
    ### recalculate dtw parameters
    sumx = sumx[feat_end] - sumx[feat_start]
    sumy = sumy[feat_end] - sumy[feat_start]
    sumx2 = sumx2[feat_end] - sumx2[feat_start]
    sumy2 = sumy2[feat_end] - sumy2[feat_start]
    sumxy = sumxy[feat_end] - sumxy[feat_start]
    N = N[feat_end] - N[feat_start]

    a_denom = (sumx2 - sumx ** 2 / N)
    a_nom = (sumxy - sumx * sumy / N)
    if N == 0:
        a = 1
        b = 0
    if a_denom == 0 or a_nom==0:
        a = 0
        b = (sumy - a * sumx) / N
    else:
        a = (sumxy - sumx * sumy / N) / a_denom
        b = (sumy - a * sumx) / N

    ### calculate error. SSE: sum of squared errors. MAE: mean absolute error.
    #if error == "SSE":
    error = a ** 2 * sumx2 - 2 * a * sumxy + sumy2 - 2 * b * sumy + 2 * a * b * sumx + N * b ** 2
    if error_rel == True:
        query_sel = query[id_query[path_lbound]:id_query[path_rbound + 1]]
        query_mean = np.mean(query_sel) #the matched (bounded) reference sequence equal to the mean of the (bounded) query sequence defines the worst possible match
        error_max = sum((query_sel - query_mean)**2)
        #If the bounded query is uniform, error_max and error will be close to zero. This could also cause issues due to float rounding.
        #In order to prevent undesirable results, small values are filtered with an if statement
        if error_max < 10**-10:
            error=0
        else:
            error = error/error_max

    #if error == "MAE":
    #    error = 0
    #    for i,j in zip(id_ref[path_lbound:path_rbound + 1],id_query[path_lbound:path_rbound + 1]):
    #        error += abs(ref[i]-(a*query[j]+b))

    return a, b, error

def func_roll(query, ref, cost, weight, step_single, step_multiple, step_weight, rep_step_ref, rep_step_query, flag_ref, flag_fill):
    '''
    :param query: query series
    :param ref: reference series
    :param cost: initial cost matrix
    :param weight: weight matrix
    :param step_single: single step patterns
    :param step_multiple: multi step patterns
    :param step_weight: multi step weight
    :param rep_step_ref: allowable repetitions at each reference index for all steps
    :param rep_step_query: allowable repetitions at each query index for all steps
    :param flag_ref: flag ref indices and corresponding query indices. flagged query indices will hold the cost result
    :return: array containing the error, amplitude and a nested array which contains flagged query ids matching the flagged ref ids.

    '''

    a, b, N, sumx, sumy, sumx2, sumy2, sumxy, cost, step = \
        dtw_cy.dtw_backward(query, ref, cost.copy(), weight, step_single, step_multiple, step_weight, rep_step_ref, rep_step_query)

    id_ref, id_query = dtw_path(step, step_single, step_multiple)
    bounds_ref = [1, len(ref) - 2]  # start bound (id) and stop bound (id) of the reference series
    a_feat, b_feat, error_rel = feat_params(query=query, bounds_ref=bounds_ref, id_query=id_query, id_ref=id_ref,
                       sumx=sumx, sumy=sumy, sumx2=sumx2, sumy2=sumy2, sumxy=sumxy, N=N, error_rel=True)

    #find all indices from id (path) query that match with flagged ref elements
    #TODO: flag query indices are only unique if no query reps are allowed.
    flag_query = []
    j = 0
    for i in range(len(flag_ref)):
        match = False
        try:
            while True:
                if flag_ref[i] == id_ref[j]:
                    match = True
                    flag_query.append(id_query[j])
                elif match == True:
                    break
                j = j + 1
        except:
            break #if j exceeds the maximum range the loop breaks

    if flag_fill:
        flag_query = np.arange(flag_query[0],flag_query[-1] + 1)

    return np.array([error_rel, a_feat, np.array(flag_query)],dtype=object) #np.ones(len(flag_query)) *

def dtw_roll(data, nquery, ref, cost, weight, step_single, step_multiple, step_weight, rep_step_ref, rep_step_query, flag, flag_cont, lim_err, lim_amp):
    '''
    calculate dtw in a running data frame
    :param data: pandas series or numpy ndarray
    :return:
        df: dataframe with the result
    '''
    window_step = nquery // 2

    data = copy.deepcopy(data)
    if isinstance(data, np.ndarray) and data.ndim == 1:
        data_dtw = data
        data = pd.Series(data)
    elif isinstance(data, pd.Series) and data.ndim == 1:
        data_dtw = data.to_numpy()
        data = data
    else:
        raise ValueError("data should be a 1D numpy array or pandas series")

    data_lext = np.ones(window_step-1) * data_dtw[0] #left extension
    data_rext = np.ones(window_step-1) * data_dtw[-1] #right extension
    data_dtw = np.concatenate([data_lext, data_dtw, data_rext]) #extended data

    # create and select frames
    frames = np.lib.stride_tricks.sliding_window_view(data_dtw, window_shape=nquery)  # np_ext.rolling(block['data'][var].values, win_AO, as_array=True)
    #id_frames = np.arange(0, len(frames) - 1, window_step)  # select subset of sliding windows
    #id_frames = np.append(id_frames, len(frames) - 1)
    
    num_frames = int(np.floor((len(frames)-1) / window_step))
    id_frames = np.linspace(0, len(frames) - 1, num_frames, dtype=int)

    queries = frames[id_frames]

    # run dtw
    res_dtw = np.apply_along_axis(func_roll, axis=1, arr=queries, ref=ref, cost=cost,
                                  weight=weight,
                                  step_single=step_single, step_multiple=step_multiple,
                                  step_weight=step_weight,
                                  rep_step_ref=rep_step_ref, rep_step_query=rep_step_query,
                                  flag_ref=flag, flag_fill=flag_cont)

    # process dtw_result
    res_dtw[:, 2][0] = np.delete(res_dtw[:, 2][0], np.where(res_dtw[:, 2][0] < (window_step - 1)))
    res_dtw[:, 2][-1] = np.delete(res_dtw[:, 2][-1], np.where(res_dtw[:, 2][-1] > (nquery - window_step)))
    id = res_dtw[:, 2] + data.iloc[id_frames].index - (window_step-1)  # convert index query frame to dataframe index and correct for data extension
    id = np.concatenate(id)  # dataframe indices

    err = np.concatenate(res_dtw[:, 2] * 0 + res_dtw[:, 0])  # match error
    err = np.where(err > lim_err, np.nan, err)  # error values higher than error limit are reset to NaN

    amp = np.concatenate(res_dtw[:, 2] * 0 + res_dtw[:, 1])  # match amplitude
    amp = np.where(abs(amp) < lim_amp, np.nan, amp) # amplitude values lower than a given treshold are reset to NaN

    param = (1 - err) * amp  # combined (amplitude and match) parameter

    group = np.concatenate(res_dtw[:, 2] * 0 + np.arange(data.index[0], data.index[0] + len(res_dtw)))  # feature entitity id (=group id): group id for each corresponding index

    df_dtw = pd.DataFrame({'group': group, 'id': id, 'val': param, 'err': err, 'amp': amp})
    df_dtw = df_dtw.dropna()  # drop NaN outcome values

    # Select and remove overlapping indices. Select according to best match
    df_dtw.loc[:, 'abs_val'] = df_dtw['val'].apply(lambda x: abs(x))
    df_dtw = df_dtw.sort_values(['id', 'abs_val'])  # sort: highest values sorted last
    mask_last = df_dtw['id'].duplicated(keep='last')  # mark all overlapping indices corresponding to the lowest values
    id_group = df_dtw[mask_last].index  # indices of the corresponding groups that show lower values
    group_rmv = df_dtw.loc[id_group, 'group']  # correspondig group
    mask_df = ~df_dtw['group'].isin(group_rmv)  # remove these groups
    df_dtw = df_dtw[mask_df]

    #mask_dup = df_dtw.duplicated(subset='group')
    #df_dtw_unique = df_dtw[~ mask_dup]

    ###assign dtw to input dataframe#
    df = data.to_frame(name='data')
    df.loc[df_dtw['id'], "group"] = df_dtw['group'].values
    df.loc[df_dtw['id'], "dtw" + "_err"] = df_dtw['err'].values
    df.loc[df_dtw['id'], "dtw" + "_amp"] = df_dtw['amp'].values
    df.loc[df_dtw['id'], "dtw"] = df_dtw['val'].values

    #df.loc[df_dtw['id'], "group"] = df_dtw['group'].values
    #df.loc[df_dtw_unique['id'], "dtw" + "_err"] = df_dtw_unique['err'].values
    #df.loc[df_dtw_unique['id'], "dtw" + "_amp"] = df_dtw_unique['amp'].values
    #df.loc[df_dtw_unique['id'], "dtw"] = df_dtw_unique['val'].values

    return df

def dtw_plot(query, ref, id_ref, id_query):
    '''
    :param query: query series
    :param ref: reference series
    :param id_ref: id path reference
    :param id_query: id path query
    :return: plot showing reference, query and dtw path in one graph
    '''
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 2, width_ratios=[1, 3], height_ratios=[3, 1])
    axr = plt.subplot(gs[0])
    ax = plt.subplot(gs[1])
    axq = plt.subplot(gs[3])

    axq.plot(np.arange(len(query)), query)  # query, horizontal, bottom
    axq.set_xlabel('Query')

    axr.plot(ref,np.arange(len(ref)))  # ref, vertical
    axr.invert_xaxis()
    axr.set_ylabel('Ref')

    ax.plot(id_query, id_ref)

def plot_match(query, flag, id_ref, id_query):
    id_sel = np.array([],dtype = int)
    for id in flag:
        id_find = np.where(id_ref == id)[0]
        id_sel = np.concatenate([id_sel, id_find])
    id_sel = id_sel.astype(np.int32)
    fig, ax = plt.subplots(1)
    ax.plot(id_query, query,label="query")
    ax.scatter(np.array(id_query)[id_sel],np.array(query)[id_sel],color = "r",label='match')
    ax.legend()

def plot_fit(query, ref, id_ref, id_query, a=1, b=0):
    '''
    :param query: query series
    :param ref: reference series
    :param id_ref: id path reference
    :param id_query: id path query
    :param a: scale
    :param b: offset
    :return: plot showing matched reference and query series.
        The match is defined by scale, offset and dtw path. duplicated elements are color marked
    '''
    idref_pd = pd.Series(id_ref)
    idref_pd_dup = idref_pd[idref_pd.duplicated("first")]
    idref_dup = idref_pd_dup.values
    ref_dupval = ref[idref_dup]
    ref_dupid = idref_pd_dup.index.to_numpy()
    for k,val in enumerate(ref_dupid):
        ref_dupid[k] =  id_query[val]

    idquery_pd = pd.Series(id_query)
    idquery_pd_dup = idquery_pd[idquery_pd.duplicated("first")]
    idquery_dup = idquery_pd_dup.values
    query_dupval = query[idquery_dup]
    query_dupid = idquery_pd_dup.index.to_numpy()
    for k,val in enumerate(query_dupid):
        query_dupid[k] =  id_query[val]

    fig, ax = plt.subplots(1)
    id_sel = np.argwhere((np.array(id_ref) > 0) & (np.array(id_ref) < len(ref)-1)).flatten()
    ax.plot(np.asarray(id_query)[id_sel],ref[np.asarray(id_ref)[id_sel]]*a+b,label="ref")
    ax.plot(id_query,query[id_query],label="query", linestyle = '--')
    msk = np.in1d(ref_dupid,id_sel)
    ax.scatter(ref_dupid[msk],ref_dupval[msk]*a+b,color = "g", label='reps')
    ax.scatter(query_dupid,query_dupval,color = "g",marker = "x")
    ax.legend()

def show_matrix(A):
    '''
    visualize a matrix
    :param A: a matrix
    :return:
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(A, interpolation='nearest')
    fig.colorbar(cax)

if __name__ == "__main__":  
    None

