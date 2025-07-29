#%%
import scipy.stats as sps
import pandas as pd
from typing import Union, Hashable, Callable, Tuple, List
import numpy as np
from numpy.typing import ArrayLike
from statsmodels.stats.multitest import multipletests
from functools import partial

class Test:

    def __init__(self, data: pd.DataFrame, y: Hashable, x: Hashable, test: Callable,
        *, pairwise: bool = False, adjust: str = "bh", **kwargs) -> None:
        
        self.data = data
        self.y, self.x = y, x 
        self.test_ = test

        # Find the groups
        self.groups = self.data[x].unique()
        if len(self.groups) < 2:
            raise ValueError(f"Got {len(self.groups)} ({', '.join(self.groups)}), but at least 2 groups are required.")
        # If there are more than two groups, either do pairwise, or pass the multiple groups
        # to a test (ANOVA, Kruskal-Wallis...)
        self.pairwise = (len(self.groups) > 2 and pairwise)
        # Separate Y by groups
        self.values = self.__build_groups(self.data, self.y, self.x, self.groups)

        # Apply test
        if not self.pairwise: 
            self.result = self.__result_to_series(self.test_(*self.values, **kwargs))
        else:
            # Apply the test to each pair of groups
            results = []
            for n, (k, v) in enumerate(zip(self.groups, self.values)):
                for kk,vv in zip(self.groups[n:], self.values[n:]):
                    if k==kk: continue

                    results.append(
                        self.__result_to_series(self.test_(v, vv, **kwargs)) \
                        .to_frame() \
                        .transpose() \
                        .assign(group_1=k, group_2=kk)
                    )

            self.result = pd.concat(results)  
            # Do FDR correction
            if adjust:
                self.result = self.result.assign(p_adjusted=pd.Series(sps.false_discovery_control(
                    self.result.pvalue.astype(float), method=adjust), index=self.result.index)) 
    
    def test(self):
        return self.result

    def __result_to_series(self, result):
        return pd.Series({k: getattr(result, k) for k in dir(result) if 
            not (k.startswith("_") or k in ["count", "index"])})

    def __build_groups(self, data, y, x, groups):
        return [data.loc[data[x].eq(group), y].values for group in groups]


def pairwise_test(X: pd.DataFrame, variable:Hashable, value:Hashable, test:Callable, 
    p_thresh: float=.05, correction: str = "fdr_bh", one_sided: bool = False, 
    fw_error_rate: Union[float, None] = 0.05) -> Tuple[pd.DataFrame, pd.DataFrame, List[Tuple[Hashable, Hashable]]]:

    # Split X into groups
    groups = {grp: X[X[variable].eq(grp)][value] for grp in X[variable].unique()}
    N = len(groups)

    results = []
    for i, (k, v) in enumerate(groups.items()):
        for j, (kk, vv) in enumerate(groups.items()):
            if j == i: continue
            if not one_sided and j > i: continue
            stat, p = test(v, vv)
            results.append([k, kk, stat, p, p < p_thresh])

    results = pd.DataFrame(results, columns=["group_1", "group_2", "statistic", "p", "significant"])

    if correction != "none":
        results["significant"], results["p_corrected"], _, _ = multipletests(
            results["p"], fw_error_rate, method=correction)
    return results


def oneway_anova(X: pd.DataFrame, groups_col: str, values_col: str):

    groups = [X.loc[X[groups_col]==x, values_col] for x in X[groups_col].unique()]
    return sps.f_oneway(*groups)

def node_color(dist: pd.DataFrame, labels: ArrayLike, test: Union[str, Callable] = "permutation", random_state = 23,
    nresamples: int = 1000):
    
    # Test if the pairwise distances between nodes of the same color are smaller than those between nodes of different colors
    label_map = {k: v for k, v in zip(dist.columns, labels)}
    # Take the upper triangular matrix
    mask = np.triu(np.ones(dist.shape), 1).astype(bool)
    tril_d = dist.where(mask).stack().reset_index().rename(columns={0: "distance"})
    # Check if the nodes are of the same color
    tril_d.loc[:,"level_0"] = tril_d["level_0"].replace(label_map)
    tril_d.loc[:,"level_1"] = tril_d["level_1"].replace(label_map)
    tril_d["same_color"] = tril_d["level_0"].eq(tril_d["level_1"])
    tril_d = tril_d.sort_values("same_color")

    if test == "permutation": test = partial(_pairwise_permutation_test, random_state=random_state, 
        nresamples=nresamples)
    return test(tril_d["distance"][~tril_d["same_color"]], tril_d["distance"][tril_d["same_color"]])

def _pairwise_permutation_test(x, y, random_state = 23, nresamples: int = 10000):
    result = sps.permutation_test([x,y], statistic=lambda a,b: np.mean(a)-np.mean(b), 
        alternative="greater", random_state=random_state, n_resamples=nresamples)
    return result.statistic, result.pvalue

# %%
