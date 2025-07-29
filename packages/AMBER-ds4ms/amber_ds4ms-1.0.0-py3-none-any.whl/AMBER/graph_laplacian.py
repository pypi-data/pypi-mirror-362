# tools
import numpy as np
import scipy
import torch
from scipy.sparse import lil_matrix, block_diag, csr_array, diags, csr_matrix


def create_laplacian_matrix(nx, ny=None):
    """
    Helper method to create the laplacian matrix for the laplacian
    regularization

    Parameters
    ----------
    :param nx: height of the original image
    :param ny: width of the original image

    Returns
    -------

    :rtype: scipy.sparse.csr_matrix
    :return:the n x n laplacian matrix, where n = nx*ny


    """
    if ny is None:
        ny = nx
    assert (nx > 1)
    assert (ny > 1)
    # Blocks corresponding to the corner of the image (linking row elements)
    top_block = lil_matrix((ny, ny), dtype=np.float32)
    top_block.setdiag([2] + [3] * (ny - 2) + [2])
    top_block.setdiag(-1, k=1)
    top_block.setdiag(-1, k=-1)
    # Blocks corresponding to the middle of the image (linking row elements)
    mid_block = lil_matrix((ny, ny), dtype=np.float32)
    mid_block.setdiag([3] + [4]*(ny - 2) + [3])
    mid_block.setdiag(-1, k=1)
    mid_block.setdiag(-1, k=-1)
    # Construction of the diagonal of blocks
    list_blocks = [top_block] + [mid_block]*(nx-2) + [top_block]
    blocks = block_diag(list_blocks)
    # Diagonals linking different rows
    blocks.setdiag(-1, k=ny)
    return blocks


def delete_from_csr(mat, row_indices=[], col_indices=[]):
    """
    Remove the rows (denoted by ``row_indices``) and columns (denoted by ``col_indices``) from the CSR sparse matrix ``mat``.
    WARNING: Indices of altered axes are reset in the returned matrix
    """
    if not isinstance(mat, csr_matrix):
        raise ValueError("works only for CSR format -- use .tocsr() first")

    rows = []
    cols = []
    if row_indices:
        rows = list(row_indices)
    if col_indices:
        cols = list(col_indices)

    if len(rows) > 0 and len(cols) > 0:
        row_mask = np.ones(mat.shape[0], dtype=bool)
        row_mask[rows] = False
        col_mask = np.ones(mat.shape[1], dtype=bool)
        col_mask[cols] = False
        return mat[row_mask][:, col_mask]
    elif len(rows) > 0:
        mask = np.ones(mat.shape[0], dtype=bool)
        mask[rows] = False
        return mat[mask]
    elif len(cols) > 0:
        mask = np.ones(mat.shape[1], dtype=bool)
        mask[cols] = False
        return mat[:, mask]
    else:
        return mat


def remove_vertex(L, lst_rows=[], lst_cols=[]):
    """
    Function that removes a vertex and adjust the graph laplacian matrix.
    """
    L_cut = delete_from_csr(L.tocsr(), row_indices=lst_rows, col_indices=lst_cols)
    L_cut = L_cut - diags(L_cut.diagonal())
    L_cut = L_cut - diags(L_cut.sum(axis=1).A1)
    assert (L_cut.sum(axis=1).A1 == np.zeros(L_cut.shape[0])).all()

    return L_cut


def laplacian(Y, nx, ny=None):
    """
    Function that removes the vertices corresponding to Nan locations of tensor Y.
    Args:
        - Y: torch.tensor of the observations (Float64)
        - nx,ny: dimensions of the image (Int64)
    """
    # find Nan indices
    Nan_indices = torch.where(torch.isnan(Y.ravel()) == True)[0]

    # get list of indices
    list_idx = list(Nan_indices.detach().numpy())

    # create Laplacian
    L = create_laplacian_matrix(nx, ny=ny)
    L = remove_vertex(L, list_idx, list_idx)
    return L


def unnormalized_laplacian(y, nx, ny=None, method='inverse'):
    """Construct numpy array with non zeros weights and non zeros indices.

        Args:
            - y: np.array for observations of size (size_x*size_y)
            - method: str indicating how to compute the weight of the unnormalized laplacian
    """
    # create laplacian matrix
    lapl_tmp = laplacian(y, nx, ny)
    lapl_tmp.setdiag(np.zeros(nx*ny))

    # select the non nan indices
    y_tmp = y[torch.isnan(y) == False]

    # store non zero indices
    idx_rows = np.array(lapl_tmp.nonzero()[0])
    idx_cols = np.array(lapl_tmp.nonzero()[1])

    # construct the set of weights
    nnz_w = np.zeros_like(idx_rows, dtype=np.float32)

    # construction of the non zeros weights
    if method == 'inverse':
        nnz_w = 1/(np.abs(y_tmp[idx_rows] - y_tmp[idx_cols]) + 1e-4)
    else:
        nnz_w = np.exp(-np.abs(y_tmp[idx_rows] - y_tmp[idx_cols]))

    # construct the non diagonal terms of the Laplacian
    lapl_nondiag = csr_array((nnz_w, (idx_rows, idx_cols)), shape=(lapl_tmp.shape[0], lapl_tmp.shape[0]), dtype=np.float32)

    # construct the diagonal terms of the Laplacian
    lapl_diag = diags(lapl_nondiag.sum(axis=0))

    # construct the Laplacian
    L = lapl_diag - lapl_nondiag

    return L


def laplacian_chain(nb_vertices):
    """
    Construct the Laplacian matrix of a chain.
    """
    L = np.zeros((nb_vertices, nb_vertices))

    # First vertex
    L[0, 0] = 1
    L[0, 1] = -1

    # Toeplitz matrix
    if nb_vertices > 2:
        first_row = torch.zeros(nb_vertices)
        first_row[0] = -1
        first_row[1] = 2
        first_row[2] = -1

        first_col = torch.zeros(nb_vertices-2)
        first_col[0] = -1

        D = scipy.linalg.toeplitz(first_col, r=first_row)

        L[1:nb_vertices-1, :] = D

    # Last vertex
    L[-1, -2] = -1
    L[-1, -1] = 1

    return L


def unnormalized_laplacian_chain(y, nx, method='inverse'):
    """Construct numpy array with non zeros weights and non zeros indices.

        Args:
            - y: np.array for aggregated observations of size (nb_bins)
            - method: str indicating how to compute the weight of the unnormalized laplacian
    """
    # create laplacian matrix
    lapl_tmp = csr_matrix(laplacian_chain(nx))
    lapl_tmp.setdiag(np.zeros(nx*nx))

    # select the non nan indices
    y_tmp = np.nan_to_num(y)

    # store non zero indices
    idx_rows = np.array(lapl_tmp.nonzero()[0])
    idx_cols = np.array(lapl_tmp.nonzero()[1])

    # construct the set of weights
    nnz_w = np.zeros_like(idx_rows, dtype=np.float32)

    # construction of the non zeros weights
    if method == 'inverse':
        nnz_w = 1/(np.abs(y_tmp[idx_rows] - y_tmp[idx_cols]))
    else:
        nnz_w = np.exp(-np.abs(y_tmp[idx_rows] - y_tmp[idx_cols]))

    # construct the non diagonal terms of the Laplacian
    lapl_nondiag = csr_array((nnz_w, (idx_rows, idx_cols)), shape=(lapl_tmp.shape[0], lapl_tmp.shape[0]), dtype=np.float32)

    # construct the diagonal terms of the Laplacian
    lapl_diag = diags(lapl_nondiag.sum(axis=0))

    # construct the Laplacian
    L = lapl_diag - lapl_nondiag

    return L
