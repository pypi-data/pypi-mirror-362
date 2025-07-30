import numpy as np
import string
import logging
from typing import List, Dict, Literal, TypedDict

# Set up logger for the package
logger = logging.getLogger('multipca')
# Ensure at least one handler is present to make warnings visible
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def _mode_product_skip_one(array, num_mode, vec_list, mode_skip):
    # helper function for mpca iterations

    # Parameters:
    #  array: the last dimension is N
    #  num_mode = len(array.shape) - 1
    #  vec_list: len = num_mode, a list of vectors in the iterations now, of dim d_0, d_1, ...
    #  mode_skip: the mode to skip, inumerate starts with 0

    # Returns:
    #  array_now: numpy matrix, d_mode_skip * N

    array_now = array.copy()
    for mode in range(mode_skip):
        axes = string.ascii_lowercase[:len(array_now.shape)]
        array_now = np.einsum(axes + ',a->' + axes[1:], array_now, vec_list[mode])
    for mode in range((mode_skip+1), num_mode):
        axes = string.ascii_lowercase[:len(array_now.shape)]
        array_now = np.einsum(axes + ',b->a' + axes[2:], array_now, vec_list[mode])
    return array_now

def _mode_product_all(array, num_mode, vec_list):
    # helper function for mpca_CI

    # Parameters:
    #  array: the last dimension is N
    #  num_mode = len(array.shape) - 1
    #  vec_list: len = num_mode, a list of vectors in the iterations now, of dim d_0, d_1, ...

    # Returns:
    #  array_now: numpy vector, length N

    array_now = array.copy()
    for mode in range(num_mode):
        array_now = np.tensordot(array_now, vec_list[mode], axes=([0],[0]))
    return array_now

def _leading_sv(mat, r):
    # leading r left singular vectors of mat

    U, D, V = np.linalg.svd(mat, full_matrices=False, compute_uv=True, hermitian=False)
    if r==1:
        return U[:, 0]
    else:
        return U[:,:r]

def _ite_one_step(array, num_mode, vec_list_prev):
    # helper function, one step iteration in mpca

    # Parameters:
    #  array: the last dimension is N
    #  num_mode = len(array.shape) - 1
    #  vec_list_prev: len = num_mode, a list of vectors in the iterations now, of dim d_0, d_1, ...

    # Returns:
    #  vec_list_new: len = num_mode, a list of vectors after one step of iteration
    vec_list_new  = []
    for mode in range(num_mode):
        vec_list_new.append(_leading_sv(_mode_product_skip_one(array, num_mode, vec_list_prev, mode), 1))
    return vec_list_new

def _ite_one_step_with_stability(array, num_mode, vec_list_prev, proj_list):
    # helper function, one step iteration in mpca

    # Parameters:
    #  array: the last dimension is N
    #  num_mode = len(array.shape) - 1
    #  vec_list_prev: len = num_mode, a list of vectors in the iterations now, of dim d_0, d_1, ...
    #  proj_list: projection onto the COMPLEMENT of the previous ranks

    # Returns:
    #  vec_list_new: len = num_mode, a list of vectors after one step of iteration
    vec_list_new  = []
    for mode in range(num_mode):
        M = proj_list[mode].dot( _mode_product_skip_one(array, num_mode, vec_list_prev, mode) )
        vec_list_new.append(_leading_sv(M, 1))
    return vec_list_new

def _leading_sv_with_d(mat, r):
    # leading r left singular vectors of mat

    U, D, V = np.linalg.svd(mat, full_matrices=False, compute_uv=True, hermitian=False)
    if r==1:
        return U[:, 0], D[0]
    else:
        return U[:,:r], D[:r]

def _ite_one_step_with_d(array, num_mode, vec_list_prev):
    # helper function, one step iteration in mpca

    # Parameters:
    #  array: the last dimension is N
    #  num_mode = len(array.shape) - 1
    #  vec_list_prev: len = num_mode, a list of vectors in the iterations now, of dim d_0, d_1, ...

    # Returns:
    #  vec_list_new: len = num_mode, a list of vectors after one step of iteration
    vec_list_new  = []
    for mode in range(num_mode):
        if mode == 0:
            u, d = _leading_sv_with_d(_mode_product_skip_one(array, num_mode, vec_list_prev, mode), 1)
            vec_list_new.append(u)
        else:
            vec_list_new.append(_leading_sv(_mode_product_skip_one(array, num_mode, vec_list_prev, mode), 1))
    return vec_list_new, d**2 / array.shape[-1]

def _ite_one_step_with_stability_with_d(array, num_mode, vec_list_prev, proj_list):
    # helper function, one step iteration in mpca

    # Parameters:
    #  array: the last dimension is N
    #  num_mode = len(array.shape) - 1
    #  vec_list_prev: len = num_mode, a list of vectors in the iterations now, of dim d_0, d_1, ...
    #  proj_list: projection onto the COMPLEMENT of the previous ranks

    # Returns:
    #  vec_list_new: len = num_mode, a list of vectors after one step of iteration
    vec_list_new  = []
    for mode in range(num_mode):
        M = proj_list[mode].dot( _mode_product_skip_one(array, num_mode, vec_list_prev, mode) )
        if mode == 0:
            u, d = _leading_sv_with_d(_mode_product_skip_one(array, num_mode, vec_list_prev, mode), 1)
            vec_list_new.append(u)
        else:
            vec_list_new.append(_leading_sv(M, 1))
    return vec_list_new, d**2 / array.shape[-1]

def _dist_vec_list(vec_list_now, vec_list_prev, num_mode):
    # sum of dist between vec_list_now and vec_list_prev
    d = 0.0
    for mode in range(num_mode):
        d += np.linalg.norm(vec_list_now[mode] - vec_list_prev[mode])
    return d

def _ini_simple(array):
    # helper function for the initialization for mpca
    # initialize with one vec_list for each rank

    dim = array.shape
    num_mode = len(dim) - 1

    ini_vec_list = []
    ini_vec_list.append( _leading_sv(array.reshape((dim[0], -1), order = 'F'), 1) )

    for mode in range(1,num_mode):
        array_now = array.copy()
        for previous_mode in range(mode):
            array_now = np.tensordot(array_now, ini_vec_list[previous_mode], axes=([0],[0]))
        ini_vec_list.append( _leading_sv(array_now.reshape((dim[mode], -1), order = 'F'), 1) )

    return ini_vec_list

def _ini_multi(array, r_pca, num_multi = None, seed = 42):
    # helper function for the initialization for mpca
    # initialize with multiple vec_list for each rank

    # parameters:
    #  array
    #  r_pca: the rank for the PCA step for multiple initialization. if larger than array.shape[0], it will be capped at array.shape[0]
    #  num_multi: int, number of multiple initialization, default to r_pca+3

    # returns:
    #  ini_vec_list_list: a list of ini_vec_list, outside list length = num_multi, inside list length = num_mode

    # guardrail
    r_pca = min(r_pca, array.shape[0])
    
    if num_multi is None:
        num_multi = r_pca + 3

    dim = array.shape
    num_mode = len(dim) - 1

    np.random.seed(seed)

    U = _leading_sv(array.reshape((dim[0], -1), order = 'F'), r_pca)
    # use columns of U and U times a random matrix (nrow = r_pca, ncol = num_multi - r_pca) as starting points
    randm = np.random.randn(r_pca, num_multi - r_pca)
    randm = randm / np.linalg.norm(randm, axis=0)
    starts = U.dot( np.concatenate((np.eye(r_pca), randm), axis=1) )  # shape = (dim[0], num_multi)

    ini_vec_list_list = []

    for strt in range(num_multi):
        ini_vec_list_now = []
        ini_vec_list_now.append(starts[:,strt])

        for mode in range(1,num_mode):
            array_now = array.copy()
            for previous_mode in range(mode):
                array_now = np.tensordot(array_now, ini_vec_list_now[previous_mode], axes=([0],[0]))
            ini_vec_list_now.append(_leading_sv(array_now.reshape((dim[mode], -1), order = 'F'), 1))

        ini_vec_list_list.append(ini_vec_list_now)

    return ini_vec_list_list

def _match_vec(vec_list_list1, vec_list_list2):
    # match vec_list_list2 to vec_list_list1, and change the sign of vec_list_list2[i], i = 1,...,r if necessary
    r = len(vec_list_list1)
    num_mode = len(vec_list_list1[0])
    fetched = []
    return_vec_list_list = []
    for i in range(r):
        # all unfetched indices
        sum_abs = np.zeros(r)
        for j in list(set(range(r)).difference(fetched)):
            for mode in range(num_mode):
                sum_abs[j] = sum_abs[j] + abs( np.inner(vec_list_list1[i][mode], vec_list_list2[j][mode]))

        # which maximize sum of absolute value of inner products
        index_now = np.argmax(sum_abs)
        fetched.append(index_now)
        return_vec_list_list.append([])
        for mode in range(num_mode):
            return_vec_list_list[i].append( vec_list_list2[index_now][mode] * np.sign( np.inner(vec_list_list1[i][mode], vec_list_list2[index_now][mode])))

    return return_vec_list_list

class MpcaCIResult(TypedDict):
    components: List[List[np.ndarray]]
    asymptotic_parameters: np.ndarray
    debiasing_factors: np.ndarray

def mpca(array: np.ndarray, 
         r: int, 
         max_iterations: int = 20, 
         threshold: float = 1e-5, 
         initialization: Literal['simple', 'multi'] = 'multi') -> List[List[np.ndarray]]:
    """ The algorithm for multipca, calculating the multiway PCs.

    Parameters:
    -----------
    array: numpy array
        d0 by d1 by d2 ... by N
    r: int
        targeted number of rank, should be no larger than min(d1, d2, ...)
    max_iterations: int
        maximum number of iterations
    threshold: float
        when the results are closer than this number, iteration stops
    initialization: str
        either 'simple' or 'multi',
        corresponding to initialize once for each component or initialize with multiple threads, then choose the best one

    Returns:
    --------
    components: list
        a list of length r, each element is also a list (sublist)
        each sublist has length equal to the number of modes, i.e., len(array.shape)-1,
        components[i][j] is a (dj,) numpy vector, corresponding to the j-th mode PC component of rank i
    """
    dim = array.shape
    num_mode = len(dim) - 1

    array_now = array.copy()
    components = []
    if initialization not in {'simple', 'multi'}:
        raise('mpca: initialization has to be \'simple\' or \'multi\'')

    for pc in range(r):
        logger.info(f'Estimating Principal Component at rank {pc+1}')
        if initialization == 'simple':
            vec_list_prev = _ini_simple(array_now)
            for _ in range(max_iterations):
                vec_list_now = _ite_one_step(array_now, num_mode, vec_list_prev)
                if _dist_vec_list(vec_list_now, vec_list_prev, num_mode) < threshold:
                    break
                vec_list_prev = vec_list_now

            components.append(vec_list_now)

        else:
            vec_list_list_now = []
            ini_vec_list_list = _ini_multi(array_now, r-pc+1)
            strt_num = len(ini_vec_list_list)
            score = [0]*strt_num
            for strt in range(strt_num):
                vec_list_prev = ini_vec_list_list[strt]
                for _ in range(max_iterations):
                    vec_list_now = _ite_one_step(array_now, num_mode, vec_list_prev)
                    if _dist_vec_list(vec_list_now, vec_list_prev, num_mode) < threshold:
                        break
                    vec_list_prev = vec_list_now

                vec_list_list_now.append(vec_list_now)
                # calculate score
                array_now_copy = array_now.copy()
                for mode in range(num_mode):
                    array_now_copy = np.tensordot(array_now_copy, vec_list_now[mode], axes=([0],[0]))
                score[strt] = np.sum(array_now_copy**2)

            components.append( vec_list_list_now[np.argmax(score)] )

        # update the array
        axes = string.ascii_lowercase[:(num_mode+1)]
        for mode in range(num_mode):
            vec_now = components[pc][mode]
            proj_now = np.identity(dim[mode]) - np.outer(vec_now, vec_now)
            subscripts = axes + ',' + chr(ord('a')+mode) + 'z' + '->' + axes[:mode] + 'z' + axes[(mode+1):]
            array_now = np.einsum(subscripts, array_now, proj_now)

    return components


def mpca_CI(array: np.ndarray,
           r: int,
           max_iterations: int = 20,
           threshold: float = 1e-5,
           initialization: Literal['simple', 'multi'] = 'multi',
           debias: Literal['simple', 'sample-split'] = 'sample-split',
           stability: bool = True,
           seed: int = 42) -> MpcaCIResult:
    """ The algorithm for multipca with confidence interval.

    Parameters:
    -----------
    array: numpy array
        d0 by d1 by d2 ... by N
    r: int
        targeted number of rank, should be no larger than min(d1, d2, ...)
    max_iterations: int
        maximum number of iterations
    threshold: float
        when the results are closer than this number, iteration stops
    initialization: str
        either 'simple' or 'multi',
        corresponding to initialize once for each component or initialize with multiple threads, then choose the best one
    debias: str
        either 'simple' or 'sample-split',
        corresponding to the debiasing method used
    stability: bool
        True or False
    seed: int
        Random seed for reproducibility

    Returns:
    --------
    MpcaCIResult
        A dictionary containing:
        - components: list of lists, each sublist has length equal to the number of modes
            components[i][j] is a (dj,) numpy vector, corresponding to the j-th mode PC component of rank i
        - asymptotic_parameters: numpy array of shape (r,)
            Asymptotic parameters for confidence intervals
        - debiasing_factors: numpy array of shape (r, num_mode)
            Debiasing factors for each component and mode
    """
    dim = array.shape
    num_mode = len(dim) - 1
    N = dim[num_mode]

    np.random.seed(seed)
    permu = np.random.permutation(N)
    mid = int(N/2)

    array1 = array[..., :mid]
    array2 = array[..., mid:]
    logger.info(f'Running initial MPCA on full dataset (N={N} samples)')
    vec_list_list = mpca(array, r, max_iterations, threshold, initialization)
    logger.info(f'Running MPCA on first half of randomly split data (N={mid} samples)')
    vec_list_list1 = mpca(array1, r, max_iterations, threshold, initialization)
    logger.info(f'Running MPCA on second half of randomly split data (N={N-mid} samples)')
    vec_list_list2 = mpca(array2, r, max_iterations, threshold, initialization)
    # match
    vec_list_list1 = _match_vec(vec_list_list, vec_list_list1)
    vec_list_list2 = _match_vec(vec_list_list, vec_list_list2)

    # Calculate the debiasing factors and asymptotic parameters
    logger.info(f'Calculating debiasing factors and asymptotic parameters')
    
    # estimation of sigma0
    sigma0 = np.sqrt((array**2).mean())

    # one step update
    # check_u, they are norm 1
    check_u = []

    tilde_vec_list_list1 = []
    tilde_vec_list_list2 = []
    sigma = np.zeros(r)
    asymp_para = np.zeros(r)

    # projection matrix list for stability
    P_list = []
    for mode in range(num_mode):
        P_list.append(np.identity(dim[mode]))


    for rank in range(r):
        if stability == False:
            tilde_vec_list_list1.append(_ite_one_step(array1, num_mode, vec_list_list2[rank]))
            tilde_vec_list_list2.append(_ite_one_step(array2, num_mode, vec_list_list1[rank]))
        else:
            tilde_vec_list_list1.append(_ite_one_step_with_stability(array1, num_mode, vec_list_list2[rank], P_list))
            tilde_vec_list_list2.append(_ite_one_step_with_stability(array2, num_mode, vec_list_list1[rank], P_list))

        # put them in check_u
        check_u.append([])
        for mode in range(num_mode):
            v1 = tilde_vec_list_list1[rank][mode].copy()
            v2 = tilde_vec_list_list2[rank][mode].copy()
            v12 = (v1 + v2) / np.linalg.norm(v1 + v2)
            check_u[rank].append(v12)

        # sigma
        if stability == False:
            _, signal = _ite_one_step_with_d(array, num_mode, check_u[rank])
        else:
            _, signal = _ite_one_step_with_stability_with_d(array, num_mode, check_u[rank], P_list)
        sigma[rank] =  np.sqrt(max(0, signal - sigma0**2))
        if sigma[rank] == 0:
            asymp_para[rank] = np.inf
            logger.warning(f'Estimated signal strength of rank {rank+1} is zero.')
        else:
            asymp_para[rank] = np.sqrt( (sigma0**2) * (sigma[rank]**2+sigma0**2) / sigma[rank]**4) / np.sqrt(N)

        # update P_list
        if stability == True:
            for mode in range(num_mode):
                uuu = np.zeros((dim[mode], rank+1))
                for r_prev in range(rank+1):
                    uuu[:,r_prev] = check_u[r_prev][mode]
                P_list[mode] = np.identity(dim[mode]) - np.dot(uuu, uuu.T)

    if debias == 'sample-split':
        debias_factor = np.sqrt( 1 + np.outer(asymp_para, dim[:num_mode])**2)
    else:
        debias_factor = np.zeros((r, num_mode))  # Fixed shape specification
        for rank in range(r):
            for mode in range(num_mode):
                debias_factor[rank, mode] = 1 / np.sqrt(np.inner(tilde_vec_list_list1[rank][mode], tilde_vec_list_list2[rank][mode]))

    # Return a dictionary with descriptive keys
    return {
        'components': check_u,
        'asymptotic_parameters': asymp_para,
        'debiasing_factors': debias_factor
    }
