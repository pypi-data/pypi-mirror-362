# import numpy as np
# from tqdm import tqdm
# import h5py
# from ..ressources.odftt.io import load_series, slice_geometry
# from ..ressources.odftt.io.mumott_fileformat_loader import get_probed_coordinates
# from ..ressources.odftt.texture import grids, point_groups, odfs
# from ..ressources.odftt.tomography_models import FromArrayModel
# from ..ressources.odftt.optimization import FISTA
# from mumott.data_handling import DataContainer

# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# # from ..odftt import plot_tools

# from ..config import n_threads

# def make_difflets( mum_file, chi, two_theta_values, h_vectors, grid_resolution=10, kernel_sigma=0.1 ):

#     dc = DataContainer( mum_file )
#     geom = dc.geometry
#     geom.detector_angles = chi
#     coordinates = []
#     for two_theta in two_theta_values:
#         geom.two_theta = two_theta
#     # for ii, filename in enumerate(filenames):
#         # data_container = DataContainer(data_path=filename, data_type='h5')
#         # geom = data_container.geometry
#         coordinates.append(get_probed_coordinates(geom)[:, :, 0, :])
#     coordinates = np.stack(coordinates, axis=-1)

#     # Transpose coordinates to a format matching the two other arrays
#     coordinates = coordinates.transpose((0, 1, 3, 2))[:, np.newaxis, np.newaxis, :, :]

#     # grid_resolution = 10 # (the heuristic way I do the griding tends to perform better with odd numbers)
#     # kernel_sigma = 0.1
#     # print(kernel_sigma)
#     grid = grids.hopf_for_cubic(grid_resolution)
#     odf = odfs.Brownian(grid, point_groups.octahedral, kernel_sigma)
#     # print(f'The grid contains {odf.n_modes} orientations.')

#     basis_function_arrays = odf.compute_polefigure_matrices_parallel(coordinates, h_vectors, num_processes=n_threads) 
#     return np.array(basis_function_arrays), grid
#     # with h5py.File('analysis/difflets.h5', 'w') as hf:
#     #     hf.create_dataset( 'difflets', data=basis_function_arrays )
