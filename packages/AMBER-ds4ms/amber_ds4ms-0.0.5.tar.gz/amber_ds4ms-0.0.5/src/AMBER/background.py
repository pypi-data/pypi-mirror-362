import numpy as np
import scipy
import os.path

# graph Laplacian functions
from AMBER.graph_laplacian import laplacian, unnormalized_laplacian, unnormalized_laplacian_chain, \
    laplacian_chain, remove_vertex

import matplotlib.pyplot as plt


class background():
    """Background estimation for a given 3D dataset"""

    # range of bins
    r_range = None

    # signal values
    X = None

    # background values
    b = None
    b_grid = None

    # define
    u = None

    # list of Laplacian
    L_list = None

    def __init__(self, dtype=np.float32):

        """
        Initialize the class instance.
        """

        # define type
        self.dtype = dtype

    def set_gridcell_size(self, dqx=0.03, dqy=0.03, dE=0.1):
        """
        Set the volume voxel resolution.

        Args:
        - dqx: Resolution in the qx direction (default is 0.03).
        - dqy: Resolution in the qy direction (default is 0.03).
        - dE: Energy resolution (default is 0.1).
        """
        self.dqx = dqx
        self.dqy = dqy
        self.dE = dE

    def set_volume_from_limits(self, d_min, d_max):
        """
        Set the volume of the data.

        Args:
        - d_min: np.array, Minimum values for the volume.
        - d_max: np.array, Maximum values for the volume.
        """
        self.d_min = d_min
        self.d_max = d_max

        # by default the dimensions are Qx, Qy and E
        self.Qx = np.arange(d_min[0], d_max[0], self.dqx, dtype=self.dtype)
        self.Qy = np.arange(d_min[1], d_max[1], self.dqy, dtype=self.dtype)
        self.E = np.arange(d_min[2], d_max[2], self.dE, dtype=self.dtype)

    def set_binned_data(self, Qx, Qy, E, Int):
        """
        Set the grid data for the class instance: X2dgrid, Xgrid and Ygrid.
        Args:
        - I: np.array (3D array)
            Input data array.
        """
        # Get minimum and maximum values for intensity
        self.fmax = np.max(Int)
        self.fmin = 0.0  # Setting minimum intensity to 0.0

        # Extract coordinates in (Qx, Qy, E) dimensions
        self.Qx = Qx
        self.Qy = Qy
        self.E = E

        # Extract dimensions
        self.Qx_size = self.Qx.shape[0]
        self.Qy_size = self.Qy.shape[0]
        self.E_size = self.E.shape[0]

        # Construct the grid in 3D
        self.gridQx, self.gridQy, self.gridE = np.meshgrid(self.Qx, self.Qy, self.E, indexing='ij')
        self.Xgrid = np.concatenate([self.gridQx.ravel().reshape(-1, 1),
                                     self.gridQy.ravel().reshape(-1, 1),
                                     self.gridE.ravel().reshape(-1, 1)], axis=1)

        # Construct the grid in 2D
        self.grid2dQx, self.grid2dQy = np.meshgrid(self.Qx, self.Qy, indexing='ij')
        self.X2dgrid = np.concatenate([self.grid2dQx.ravel().reshape(-1, 1),
                                       self.grid2dQy.ravel().reshape(-1, 1)], axis=1)

        # Flatten the intensity data for the entire volume
        self.Ygrid = np.copy(Int)
        self.Ygrid = self.Ygrid.reshape(-1, self.Ygrid.shape[-1]).T

    def set_variables(self):
        """
        Initialize variable values.
        """
        # Define signal values as zeros
        self.X = np.zeros_like(self.Ygrid, dtype=self.dtype)

        # Define background values as zeros
        self.b = np.zeros((self.E_size, self.n_bins), dtype=self.dtype)

        # Initialize the values of the propagated background as zeros
        self.b_grid = np.zeros_like(self.Ygrid, dtype=self.dtype)

    def set_radial_bins(self, max_radius=6.0, n_bins=100):
        """
        Define ranges for radial bins.

        Args:
            - max_radius: float
                Maximum radial distance for the bins.
            - n_bins: int
                Number of bins to create.
        """
        # Set the maximum radial distance and the number of bins
        self.max_radius = max_radius
        self.n_bins = n_bins

        # Generate radial bins using torch linspace
        # The range starts from 0 and goes up to the square root of max_radius, creating n_bins+1 points
        self.r_range = np.linspace(0, self.max_radius, self.n_bins + 1, dtype=self.dtype)

    def R_operator(self, b):
        """
        Take the current background estimation and propagate it in 3D.

        Args:
            - Y_r: np.array
                Array representing the 2D grid of the signal.
            - b: np.array
                Array representing the background estimation.
            - e_cut: int or None
                If specified, represents the index of the energy cut; otherwise, None.

        Returns:
            np.array:
                Array representing the propagated background.
        """

        # Define the set of radii
        # Vector of aggregated values
        rX = np.sqrt(self.Xgrid[:, 0] ** 2 + self.Xgrid[:, 1] ** 2)

        # Compute the indices of grid vector in a range of radial values
        indices = np.digitize(rX, self.r_range) - 1
        indices[indices == self.n_bins] -= 1

        # Store the values at each index location
        b_grid = np.ones((self.E_size, self.Qx_size * self.Qy_size), dtype=self.dtype)
        indices_tmp = indices.T.reshape(self.Qx_size, self.Qy_size, self.E_size)
        indices_tmp = indices_tmp.reshape(-1, self.E_size).T

        for e in range(self.E_size):
            b_grid[e, :] = b[e, indices_tmp[e, :]]

        # Return the values corresponding to the bin
        b_grid = b_grid.T.reshape(self.Qx_size, self.Qy_size, self.E_size)
        b_grid = b_grid.reshape(-1, self.E_size).T

        return b_grid

    def Rstar_operator(self, X):
        """
        Compute the aggregated value of X on a radial line. Basically, sum for each radial bin.

        Args:
            - Y_r: np.array
                Array representing the signal value on a grid.
            - X: np.array
                Array representing the signal values on the grid (size_E, size_Qx * size_Qy * size_E).
            - e_cut: int or None
                If specified, represents the index of the energy cut; otherwise, None.

        Returns:
            np.array:
                Array representing the aggregated values on the 2D plane (size_E x nb_radial_bins).
        """
        # Define the set of radius
        rX = np.sqrt(self.Xgrid[:, 0] ** 2 + self.Xgrid[:, 1] ** 2)

        # Compute the indices of grid vector in a range of radial values
        indices = np.digitize(rX, self.r_range) - 1
        indices[indices == self.n_bins] -= 1

        indices_tmp = indices.T.reshape(self.Qx_size, self.Qy_size, self.E_size)
        indices_tmp = indices_tmp.reshape(-1, self.E_size).T

        v_agg = np.zeros((X.shape[0], self.n_bins), dtype=self.dtype)

        for i, r in enumerate(range(self.n_bins)):
            for e in range(self.E_size):
                if np.nansum(indices_tmp[e, :] == i) > 0:
                    v_agg[e, i] = np.nansum(X[e, indices_tmp[e, :] == i])

        return v_agg

    def Radial_mean_operator(self, X):
        """
        Returns the background define as a single line given a background defined on a 3D grid (or 2D grid if e_cut is given).
        This function is used to define the background to plot within plotQvE function.
        Args:
            - Y_r: np.array
                Array representing the signal value on a grid.
            - X: np.array
                Array representing the signal values on the grid (size_E, size_Qx * size_Qy).

        Returns:
            np.array:
                Array corresponding to the mean values on 2D grid (size_E x nb_radial_bins).
        """

        # Define the set of radius
        rX = np.sqrt(self.Xgrid[:, 0] ** 2 + self.Xgrid[:, 1] ** 2)

        # Compute the indices of grid vector in a range of radial values
        indices = np.digitize(rX, self.r_range) - 1
        indices[indices == self.n_bins] -= 1

        indices_tmp = indices.T.reshape(self.Qx_size, self.Qy_size, self.E_size)
        indices_tmp = indices_tmp.reshape(-1, self.E_size).T

        v_agg = np.zeros((X.shape[0], self.n_bins), dtype=self.dtype)

        for i, r in enumerate(range(self.n_bins)):
            for e in range(self.E_size):
                if np.nansum(indices_tmp[e, :] == i) > 0:
                    v_agg[e, i] = np.nanmean(X[e, indices_tmp[e, :] == i])

        return v_agg

    def Radial_quantile_operator(self, X, q=0.75):
        """
        Returns the background define as a single line given a background defined on a 3D grid (or 2D grid if e_cut is given).
        This function is used to define the background to plot within plotQvE function.
        Args:
            - Y_r: np.array
                Array representing the signal value on a grid.
            - X: np.array
                Array representing the signal values on the grid (size_E, size_Qx * size_Qy * size_E).
            - e_cut: int or None
                If specified, represents the index of the energy cut; otherwise, None.

        Returns:
            np.array:
                Array corresponding to the mean values on 2D grid (size_E x nb_radial_bins).
        """

        # Define the set of radius
        rX = np.sqrt(self.Xgrid[:, 0] ** 2 + self.Xgrid[:, 1] ** 2)

        # Compute the indices of grid vector in a range of radial values
        indices = np.digitize(rX, self.r_range) - 1
        indices[indices == self.n_bins] -= 1

        indices_tmp = indices.T.reshape(self.Qx_size, self.Qy_size, self.E_size)
        indices_tmp = indices_tmp.reshape(-1, self.E_size).T

        v_agg = np.zeros((X.shape[0], self.n_bins), dtype=self.dtype)

        for i, r in enumerate(range(self.n_bins)):
            for e in range(self.E_size):
                if np.nansum(indices_tmp[e, :] == i) > 0:
                    v_agg[e, i] = np.nanquantile(X[e, indices_tmp[e, :] == i], q=q)

        return v_agg

    def mask_nans(self, x):
        """
        Mask out the image pixels where the observations are NaNs.

        Args:
            - x: np.array
                Input tensor (size_E x (size_Qx * size_Qy)).

        Returns:
            np.array:
                Output tensor with NaNs (size_E x (size_Qx * size_Qy)).
        """
        # Find non-NaN indices
        Nan_indices = np.where(np.isnan(self.Ygrid) == True)
        Unan_idx = np.concatenate([Nan_indices[0].reshape(-1, 1), Nan_indices[1].reshape(-1, 1)], axis=1)

        x_temp = np.copy(x)
        x_temp[Unan_idx[:, 0], Unan_idx[:, 1]] = float('nan')

        return x_temp

    def S_lambda(self, x, lambda_):
        """
        Define the soft-thresholding function.

        Args:
            - x: np.array
                Input tensor.
            - lambda_: np.array
                Threshold parameter.

        Returns:
            np.array:
                Output tensor after applying the soft-thresholding function.
        """
        return np.sign(x) * np.maximum(np.abs(x) - lambda_, 0.0)

    def L_b(self, e_cut, normalized=True, method='inverse'):
        """
        Define Laplacian matrix L_b of a chain along the radial line. (number of vertices = number of bins)

        Args:
            - e_cut: int
                Index of the energy cut.
            - normalized: bool
                Whether to use a normalized Laplacian matrix or not.
            - method: str
                Method for computing unormalized Laplacian matrix ('inverse' or 'eigen').
                'inverse' computes the inverse

        Returns:
            np.array:
                Output tensor representing the Toeplitz matrix of a discrete differentiator filter.
        """
        # Identify the nonzero elements
        u_cut = self.u[e_cut, :]
        idx_z = list(np.where(u_cut < 0.1)[0].ravel())
        idx_nz = list(np.where(u_cut > 0.0)[0].ravel())

        if normalized:
            # Define the Laplacian matrix of a chain
            D = scipy.sparse.csr_matrix(laplacian_chain(self.n_bins))

            # Remove the vertices
            D = remove_vertex(D, lst_rows=idx_z, lst_cols=idx_z).toarray()
            L = np.zeros((self.n_bins, self.n_bins))
            L[np.ix_(idx_nz, idx_nz)] = D
        else:
            v_agg = self.Radial_mean_operator(self.Ygrid)
            D = unnormalized_laplacian_chain(v_agg[e_cut, :], self.n_bins, method)
            L = D.toarray()

        return L

    def gamma_matrix(self, e_cut=None):
        """
        Define the gamma matrix, which corresponds to the matrix associated with the operator R^*R.

        Args:
            - e_cut: int, default=None
                Index of the energy cut.

        Returns:
            np.array:
                Gamma matrix defined as the number of measurements for each radial bin.
                The number of non-NaNs values along the wedges for each radius.
        """
        gamma = np.ones(self.n_bins, dtype=self.dtype)

        if e_cut is not None:
            # Extract the 2D slice of Ygrid for the specified energy cut
            Ygrid2D = self.Ygrid[e_cut, :]
            grid = self.X2dgrid[np.isnan(Ygrid2D) == False]

            # Define the set of radii
            r = np.sqrt(grid[:, 0] ** 2 + grid[:, 1] ** 2)

            # Compute the histogram of the matrix X
            histo = np.histogram(r, self.r_range)
            gamma = histo[0]

        else:
            # Define the set of radii
            r = np.sqrt(self.X2dgrid[:, 0] ** 2 + self.X2dgrid[:, 1] ** 2)

            # Compute the histogram of the matrix X
            histo = np.histogram(r, self.r_range)
            gamma = histo[0]

        gamma_mat = np.diag(gamma)
        return gamma_mat

    def set_radial_nans(self, Y):
        """
        Define the radial nans given the observation matrix self.Ygrid

        Args: None.
        """

        # Create a binary map that indicates the NaNs of self.Ygrid
        z = np.zeros_like(Y, dtype=self.dtype)
        z[np.isnan(Y) == False] += 1
        z[np.isnan(Y) == True] = float('nan')

        # Define a self.E_size x self.n_bins matrix counting the number of measurement for each radial bin
        self.u = self.Rstar_operator(z)

        # Doesn't count the radial bin containing less than 2 measurement points
        self.u[self.u < 2.0] = 0.0

    def set_b_design_matrix(self, beta_, e_cut, normalized=True, method='inverse'):
        """
        Define the inverted design matrix of the problem: (Γ + β D)^{-1}.

        Args:
            - beta_: background smoothness penalty coefficient (float64)
            - e_cut: Int, default=None
                Index of the energy cut.
            - normalized: Boolean, default=True
                Flag to determine whether to use a normalized Laplacian.
            - method: String, default='inverse'
                Method to compute Laplacian ('inverse' or 'eigen').
        """
        # Compute gamma matrix
        gam = self.gamma_matrix(e_cut)

        # Compute L_b matrix
        L = self.L_b(e_cut, normalized, method)

        # Compute the inverse of the matrix

        if self.u is None:
            self.set_radial_nans(self.Ygrid)
        else:
            u_cut = self.u[e_cut, :]
            # idx_z = list(np.where(u_cut < 0.1)[0].ravel())
            idx_nz = list(np.where(u_cut > 0.0)[0].ravel())

        # Define identity matrix for non zero element
        W = np.eye(self.n_bins)

        # Compute the matrix to invert for background update (Γ + β L_b + \alpha I)^{-1}
        A = beta_ * L[np.ix_(idx_nz, idx_nz)] + gam[np.ix_(idx_nz, idx_nz)]
        W[np.ix_(idx_nz, idx_nz)] = A

        return W.copy()

    def compute_laplacian(self, Y_r, normalized=True, method='inverse'):
        """
        Compute the Graph Laplacian of the problem.

        Args:
            - Y_r: np.array
                Signal values on the grid.
            - normalized: Boolean, default=True
                Flag to determine whether to use a normalized Laplacian.
            - method: String, default='inverse'
                Method to compute Laplacian ('inverse' or 'eigen').

        Returns:
            np.array:
                Graph Laplacian matrix.
        """
        # If method is true, then compute the graph laplacian
        if normalized:
            L = laplacian(Y_r, self.Qx_size, self.Qy_size)
        else:
            L = unnormalized_laplacian(Y_r, self.Qx_size, self.Qy_size, method)

        L = L.toarray()
        return L

    def compute_all_laplacians(self, Y_r, normalized=True, method='inverse'):
        """
        Compute the graph Laplacians for each energy cut.

        Args:
            - Y_r: np.array
                Signal values on the grid.
            - normalized: Boolean, default=True
                Flag to determine whether to use a normalized Laplacian.
            - method: String, default='inverse'
                Method to compute Laplacian ('inverse' or 'eigen').
        """
        self.L_list = []

        for e in range(self.E_size):
            self.L_list.append(self.compute_laplacian(Y_r[e, :], normalized, method))

    def TV_denoising(self, X, gamma_, n_epochs=10, verbose=True):
        """
        Iterative reweighted least square solve the total variation denoising Problem.

        Args:
            - gamma_: torch.tensor(float64)
                    Penalty coefficient for denoising level
            - n_epochs: Int (integer)
                    Number of iterations
            - verbose: Bool
                    Display convergence logs
        """

        # initialize the signal values
        X_denoised = X.copy()

        #################################

        # loop over the energy cuts
        for e in range(self.E_size)[5:]:

            # Extract the energy cut values
            X_l = X[e, :].detach().clone()

            # set notnan indices
            idx_notnan = np.where(np.isnan(X_l) == False)[0]
            Y_r = X[e, idx_notnan]

            # loss function
            loss = 0.0

            # start loop of iterative reweighted least square
            for it in range(n_epochs):

                # compute the laplacian
                L_tmp = self.compute_laplacian(X_l, normalized=False, method='inverse')
                L_tmp = np.eye(L_tmp.shape[0], dtype=self.dtype) + gamma_[e] * L_tmp  # add the regularization

                # compute the signal
                X_tmp = np.linalg.solve(L_tmp, Y_r)

                X_l[idx_notnan] = X_tmp.copy()

            # set the signal values
            X_denoised[e, :] = X_l.copy()

            if verbose:
                print("======= energy cut denoised: ", str(e), " ========")

        return X_denoised

    def L_e(self):

        # Define graph Laplacian along energy axis
        return laplacian_chain(self.E_size)

    def set_e_design_matrix(self, mu_=1.0):

        L = self.L_e()

        # return I + mu L
        return np.eye(L.shape[0], dtype=self.dtype) + mu_*L

    def MAD_lambda(self):
        """
        Compute the MAD (Median absolute deviation) to set lambda values for each energy slice.
        The scaling factor k=1.4826 enables to ensure the robustness of the variance estimator.
        This does not work well.

        Returns:
            np.array:
                Lambda values.
        """
        return 1.4826 * np.nanmedian(np.abs(self.Ygrid - np.nanmedian(self.Ygrid)))

    def mu_estimator(self):
        r"""
        Compute an estimator of $\mu = Mean(Var(Y, axis=energy))$.

        Returns:
            torch.scalar:
                mu values.
        """
        return np.nanmean(np.var(self.Ygrid, axis=0))

    def denoising(self, Y_r, lambda_, beta_, mu_=1.0, n_epochs=20, verbose=True):
        """
        Run coordinate descent to solve optimization Problem (3).

        Args:
            - Y_r: Observations as torch.tensor (float64)
            - lambda_: Penalty coefficient for signal sparsity E_size x 1 (float64)
            - beta_: Penalty coefficient for the background's smoothness E_size x 1 (float64)
            - mu_: Penalty coefficient for the graph Laplacian regularization (float64)
            - e_cut: Range of energy cuts (numpy array)
            - n_epochs: Maximum number of iterations (integer)
            - verbose: Display convergence logs

        Returns:
            None
        """
        # ################### Initialize variable values ###############################
        # Define signal values
        self.X = np.zeros_like(Y_r, dtype=self.dtype)

        # Define background values
        self.b = np.zeros((self.E_size, self.n_bins), dtype=self.dtype)
        b_tmp = self.R_operator(self.b)

        # #############################################################################

        # Initialize the values of the propagated background
        self.b_grid = np.zeros_like(Y_r, dtype=self.dtype)

        # Compute non-zero pixels in radial background ##
        self.set_radial_nans(Y_r)

        # Define lists of matrices to invert for background update
        Lb_lst = [self.L_b(e_cut=e) for e in range(self.E_size)]
        Mb_lst = [self.set_b_design_matrix(beta_, e_cut=e) for e in range(self.E_size)]

        # Define matrix to invert for signal smoothness
        Le = self.L_e()
        Me = self.set_e_design_matrix(mu_)

        # Loss function
        loss = []#np.zeros(n_epochs, dtype=self.dtype)
        old_loss = 2000000
        new_loss = 1000000
        k = 0

        while (old_loss - new_loss > 1e-3) and (k < n_epochs):
            # Compute A = Y - B by filling the nans with 0s
            A = np.where(np.isnan(Y_r - b_tmp) == True, 0.0, Y_r - b_tmp)

            # Update the X values
            self.X = np.linalg.solve(Me, self.S_lambda(A, lambda_))

            # Projection step
            self.X = np.maximum(self.X, 0.0)

            # Update b values with b:= (beta*L_b + R^* R)^{-1} R^*(Y-X)
            b_agg = self.Rstar_operator(Y_r - self.X)

            # Update b values
            for e in range(self.E_size):
                self.b[e, :] = np.linalg.solve(Mb_lst[e], b_agg[e, :].T).T

            # Projection step
            self.b = np.maximum(self.b, 0.0)

            # Propagate in 3D
            b_tmp = self.R_operator(self.b)

            # ######################### Compute loss function ##################
            loss.append(0.5 * np.nansum((Y_r - self.X - b_tmp) ** 2) + lambda_ * np.nansum(np.abs(self.X)))

            for e in range(self.E_size):
                loss[-1] += (beta_/2) * np.matmul(self.b[e, :], np.matmul(Lb_lst[e], self.b[e, :].T))

            loss[-1] += (mu_ / 2) * np.trace(np.matmul(self.X.T, np.matmul(Le, self.X)))

            if verbose:
                print(" Iteration ", str(k+1))
                print(" Loss function: ", loss[-1].item())
            old_loss = new_loss
            new_loss = loss[-1]
            k += 1

        # Compute the propagated background
        self.b_grid = self.R_operator(self.b).copy()
        self.b_grid = self.mask_nans(self.b_grid)

        # Mask the nan values
        self.X = self.mask_nans(self.X)

    def median_bg(self, Y):
        """
        Compute the median value along the wedges. Basically, we sum for each radial bin.

        Args: None

        Returns:
            - med_bg: torch.tensor (size_e x nb_radial_bins)
                Background computed using the median-based approach
        """
        # Define the set of radius
        rX = np.sqrt(self.X2dgrid[:, 0] ** 2 + self.X2dgrid[:, 1] ** 2)

        # Compute the indices of grid vector in a range of radial values
        indices = np.digitize(rX, self.r_range) - 1
        indices[indices == self.n_bins] -= 1

        indices_tmp = indices.T.reshape(self.Qx_size, self.Qy_size, self.E_size)
        indices_tmp = indices_tmp.reshape(-1, self.E_size).T

        # Initiate median background
        med_bg = np.zeros((self.Ygrid.shape[0], self.n_bins), dtype=self.dtype)

        # Compute the median across the wedges
        for i, r in enumerate(self.r_range):
            if Y[:, indices == i].shape[1] > 0:
                med_bg[:, i] = np.nanmedian(Y[:, indices == i], dim=1)[0]

        # assign 0 to nan values (enables to plot the QvE map)
        med_bg = np.nan_to_num(med_bg)

        # Computed median background
        return med_bg

    def compute_signal_to_noise(self, b):
        """
        Compute and returns the signal to noise ratio as X^2/background^2.

        Args:
            - b: torch.tensor (float64)
                background values

        Returns: None
        """
        # compute the background defined on the grid
        b_grid = self.R_operator(self.Ygrid, b)

        # compute signal values as Yobs - B
        Signal = self.Ygrid - b_grid

        # compute snr
        snr = Signal**2/b_grid**2

        return snr

    def plot_snr(self, b, e_cut=range(40, 44), fmin=0.0, fmax=0.1):
        """
        Compute and returns the signal to noise ratio as X^2/background^2.

        Args:
            - b: torch.tensor (float64)
                background values

        Returns:
            - snr: torch.tensor (float64)
                Signal-to-noise ratio as a 3D tensor
        """
        # compute the snr
        snr = self.compute_signal_to_noise(b)

        # For 2D case (no propagation along the energy axis)
        snrplot = snr.T.reshape(self.Qx_size, self.Qy_size, self.E_size)[:, :, e_cut]
        fplot = np.mean(snrplot, axis=2)

        # Create a 3x2 subplot for various plots
        fig0 = plt.figure(figsize=(16, 9))

        # Plot 1: Observations Y
        ax0 = fig0.add_subplot(1, 1, 1)
        ax0.set_title('Observations Y')
        im0 = ax0.pcolormesh(self.grid2dQx, self.grid2dQy, fplot, vmin=fmin, vmax=fmax)
        plt.colorbar(im0, ax=ax0)
        ax0.set_xlabel(r'x')
        ax0.set_ylabel(r'y')

    def save_arrays(self, median=True):
        """
        Save radial background as numpy arrays in folder "/arrays".

        Args:
            - median: Boolean
                True if we want to save the median background line as "bg_med.py"
        """
        if not os.path.exists('arrays'):
            os.makedirs('arrays')

        if self.str_dataset == "VanadiumOzide":
            with open('arrays/' + self.str_dataset + '_' + self.str_option + '_bg.npy', 'wb') as f:
                np.save(f, self.b.detach().numpy())

            with open('arrays/' + self.str_dataset + '_' + self.str_option + '_radial_bins.npy', 'wb') as f:
                np.save(f, self.r_range.detach().numpy())

            if median:
                med_bg = self.median_bg(self.Ygrid)
                with open('arrays/' + self.str_dataset + '_' + self.str_option + '_bg_med.npy', 'wb') as f:
                    np.save(f, med_bg.detach().numpy())

        else:
            with open('arrays/' + self.str_dataset + '_bg.npy', 'wb') as f:
                np.save(f, self.b.detach().numpy())

            with open('arrays/' + self.str_dataset + '_radial_bins.npy', 'wb') as f:
                np.save(f, self.r_range.detach().numpy())

            if median:
                med_bg = self.median_bg(self.Ygrid)
                with open('arrays/' + self.str_dataset + '_bg_med.npy', 'wb') as f:
                    np.save(f, med_bg.detach().numpy())

    def compute_signal_to_obs(self, b):
        """
        Compute and returns the signal X^2/background^2.

        Args:
            - b: torch.tensor (float64)
                background values

        Returns: None
        """
        # compute the background defined on the grid
        b_grid = self.R_operator(self.Ygrid, b)

        # compute signal values as Yobs - B
        Signal = self.Ygrid - b_grid

        # compute snr
        snr = np.abs(Signal)**2 / np.abs(b_grid + 0.1)**2

        return snr

    def cross_validation(self, q=0.75, beta_range=np.array([1.0]), lambda_=1.0, mu_=1.0, n_epochs=15, verbose=True):
        """
        Runs cross-validation procedure to get the best set of hyperparameters.

        Args:
            - q: scalar
                quantile level
            - lambda_range: array
                potential lambda values.
            - beta_range: array
                potential beta values.
            - mu_range: array
                potential mu values.
            - b_truth: array
                background groundtruth.

        Returns:
            - rmse: rmse of all possible combinations of hyperparaneter values
            - lambda, alpha, beta, mu: best possible
        """
        # Define test set
        lambda_r = np.nanquantile(self.Ygrid, q)

        # Define test set
        b_test_index_upper = np.where((self.Ygrid.ravel() > lambda_r) & (np.isnan(self.Ygrid.ravel()) == False))[0]

        # compute error
        rmse = np.zeros(beta_range.shape[0], dtype=self.dtype)

        # iterate in the beta range
        for idx_beta, beta_tmp in enumerate(beta_range):
            print("Test - (", beta_tmp, ")")

            # run the optimization
            self.denoising(self.Ygrid, lambda_, beta_tmp, mu_, n_epochs, verbose)

            # compute rmse on the test set
            self.b_prop = self.R_operator(self.b)
            self.b_prop = self.mask_nans(self.b_prop)

            # Background
            B = self.b_prop.copy().ravel()
            B[b_test_index_upper] = float('nan')
            B = B.reshape(self.E_size, self.Qx_size * self.Qy_size)

            # Test set
            Y_tmp = self.Ygrid.ravel().astype(self.dtype)
            Y_tmp[b_test_index_upper] = float('nan')
            Y_tmp = Y_tmp.reshape(self.E_size, self.Qx_size * self.Qy_size)

            # ########################### rmse ###############################
            rmse[idx_beta] = np.sqrt(np.nanmean((Y_tmp - B)**2))

            print("RMSE - (", lambda_, beta_tmp, mu_, ") : ", rmse[idx_beta])

        return rmse

    def compute_mask(self, q=0.75):
        """
        Return the masked dataset where data points for which Y > quantile_{alpha}(Y) are NaN values.
        This is an alternative to the mask processing function.
        If no mask of the spurious intensities is provided by the user, then this function can be seen as an alternative.

        Args:
            - alpha: scalar value in (0,1)
                quantile level to define the threshold.
            - e_cut: integer
                index of the energy cut

        Returns:
            - X_mask: torch.tensor
                masked signal
        """
        X_mask = self.Ygrid.copy()
        X_mask[X_mask > np.nanquantile(X_mask, q)] = float('nan')
        X_mask[np.isnan(self.Ygrid) == True] = float('nan')

        return X_mask
