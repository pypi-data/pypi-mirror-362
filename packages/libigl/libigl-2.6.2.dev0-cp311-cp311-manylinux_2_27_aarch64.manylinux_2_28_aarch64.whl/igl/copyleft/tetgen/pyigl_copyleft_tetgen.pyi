from typing import Annotated

from numpy.typing import ArrayLike


def tetrahedralize(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)] = ..., H: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., VM: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)] = ..., FM: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)] = ..., R: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., flags: str = '') -> tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], int]:
    """
    Mesh the interior of a surface mesh (V,F) using tetgen

    @param[in] V  #V by 3 vertex position list
    @param[in] F  #F list of polygon face indices into V (0-indexed)
    @param[in] H  #H by 3 list of seed points inside holes
    @param[in] VM  #VM list of vertex markers
    @param[in] FM  #FM list of face markers
    @param[in] R  #R by 5 list of region attributes            
    @param[in] flags string of tetgen options (See tetgen documentation) e.g.
        "pq1.414a0.01" tries to mesh the interior of a given surface with
          quality and area constraints
        "" will mesh the convex hull constrained to pass through V (ignores F)
    @param[out] TV  #TV by 3 vertex position list
    @param[out] TT  #TT by 4 list of tet face indices
    @param[out] TF  #TF by 3 list of triangle face indices ('f', else
      `boundary_facets` is called on TT)
    @param[out] TR  #TT list of region ID for each tetrahedron      
    @param[out] TN  #TT by 4 list of indices neighbors for each tetrahedron ('n')
    @param[out] PT  #TV list of incident tetrahedron for a vertex ('m')
    @param[out] FT  #TF by 2 list of tetrahedrons sharing a triface ('nn')
    @param[out] num_regions Number of regions in output mesh
    """
