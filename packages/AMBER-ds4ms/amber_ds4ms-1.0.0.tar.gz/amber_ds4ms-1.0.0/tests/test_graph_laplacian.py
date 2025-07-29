import unittest
import numpy as np
import torch
from scipy.sparse import lil_matrix, csr_matrix, coo_matrix
import os
import sys

from AMBER.graph_laplacian import create_laplacian_matrix, delete_from_csr, \
    remove_vertex, laplacian, unnormalized_laplacian, laplacian_chain, \
    unnormalized_laplacian_chain


class TestGraphLaplacian(unittest.TestCase):

    def test_create_laplacian_matrix(self):
        nx, ny = 3, 3
        L = create_laplacian_matrix(nx, ny)
        self.assertEqual(L.shape, (nx*ny, nx*ny))
        self.assertIsInstance(L, coo_matrix)

    def test_delete_from_csr(self):
        mat = lil_matrix((4, 4), dtype=np.float32)
        mat.setdiag([1, 2, 3, 4])
        mat = mat.tocsr()
        print(mat)
        mat = delete_from_csr(mat, row_indices=[1], col_indices=[2])
        print(mat)
        self.assertEqual(mat.shape, (3, 3))
        self.assertEqual(mat[1, 1], 0.0)

    def test_remove_vertex(self):
        nx, ny = 3, 3
        L = create_laplacian_matrix(nx, ny)
        L_cut = remove_vertex(L, lst_rows=[0], lst_cols=[0])
        self.assertEqual(L_cut.shape, (nx*ny-1, nx*ny-1))
        self.assertTrue((L_cut.sum(axis=1).A1 == np.zeros(L_cut.shape[0])).all())

    def test_laplacian(self):
        Y = torch.tensor([[1.0, np.nan, 3.0], [4.0, 5.0, np.nan], [7.0, 8.0, 9.0]])
        nx, ny = Y.shape
        L = laplacian(Y, nx, ny)
        self.assertEqual(L.shape, (nx*ny-2, nx*ny-2))
        self.assertTrue((L.sum(axis=1).A1 == np.zeros(L.shape[0])).all())

    def test_unnormalized_laplacian(self):
        y = torch.tensor([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]])
        nx, ny = y.shape
        L = unnormalized_laplacian(y, nx, ny, method='inverse')
        self.assertEqual(L.shape, (nx*ny, nx*ny))
        self.assertIsInstance(L, csr_matrix)

    def test_laplacian_chain(self):
        nb_vertices = 5
        L = laplacian_chain(nb_vertices)
        self.assertEqual(L.shape, (nb_vertices, nb_vertices))
        self.assertEqual(L[0, 0], 1)
        self.assertEqual(L[0, 1], -1)
        self.assertEqual(L[-1, -2], -1)
        self.assertEqual(L[-1, -1], 1)

    def test_unnormalized_laplacian_chain(self):
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        nx = len(y)
        L = unnormalized_laplacian_chain(y, nx, method='inverse')
        self.assertEqual(L.shape, (nx, nx))
        self.assertIsInstance(L, csr_matrix)


if __name__ == '__main__':
    unittest.main()
