import enum
import os
from typing import (
    Annotated,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
    overload
)

from numpy.typing import ArrayLike
import scipy.sparse


class AABB:
    def __init__(self) -> None: ...

    def init(self, V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], Ele: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> None: ...

    def find(self, V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], Ele: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], q: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], first: bool = False) -> List[int]: ...

    def squared_distance(self, V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], Ele: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]: ...

    def intersect_ray_first(self, V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], Ele: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], orig: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], dir: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], min_t: float = float('inf')) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]: ...

    def intersect_ray(self, V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], Ele: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], orig: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], dir: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)]) -> List[List[Tuple[int, float, float, float]]]: ...

class FileEncoding(enum.Enum):
    Ascii = 1

    Binary = 0

Ascii: FileEncoding = FileEncoding.Ascii

Binary: FileEncoding = FileEncoding.Binary

class MappingEnergyType(enum.Enum):
    ARAP = 0

    LOG_ARAP = 1

    SYMMETRIC_DIRICHLET = 2

    CONFORMAL = 3

    EXP_CONFORMAL = 4

    EXP_SYMMETRIC_DIRICHLET = 5

ARAP: MappingEnergyType = MappingEnergyType.ARAP

LOG_ARAP: MappingEnergyType = MappingEnergyType.LOG_ARAP

SYMMETRIC_DIRICHLET: MappingEnergyType = MappingEnergyType.SYMMETRIC_DIRICHLET

CONFORMAL: MappingEnergyType = MappingEnergyType.CONFORMAL

EXP_CONFORMAL: MappingEnergyType = MappingEnergyType.EXP_CONFORMAL

EXP_SYMMETRIC_DIRICHLET: MappingEnergyType = MappingEnergyType.EXP_SYMMETRIC_DIRICHLET

class MassMatrixType(enum.Enum):
    MASSMATRIX_TYPE_BARYCENTRIC = 0

    MASSMATRIX_TYPE_VORONOI = 1

    MASSMATRIX_TYPE_FULL = 2

    MASSMATRIX_TYPE_DEFAULT = 3

MASSMATRIX_TYPE_BARYCENTRIC: MassMatrixType = MassMatrixType.MASSMATRIX_TYPE_BARYCENTRIC

MASSMATRIX_TYPE_VORONOI: MassMatrixType = MassMatrixType.MASSMATRIX_TYPE_VORONOI

MASSMATRIX_TYPE_FULL: MassMatrixType = MassMatrixType.MASSMATRIX_TYPE_FULL

MASSMATRIX_TYPE_DEFAULT: MassMatrixType = MassMatrixType.MASSMATRIX_TYPE_DEFAULT

class OrientedBoundingBoxMinimizeType(enum.Enum):
    ORIENTED_BOUNDING_BOX_MINIMIZE_VOLUME = 0

    ORIENTED_BOUNDING_BOX_MINIMIZE_SURFACE_AREA = 1

    ORIENTED_BOUNDING_BOX_MINIMIZE_DIAGONAL_LENGTH = 2

ORIENTED_BOUNDING_BOX_MINIMIZE_VOLUME: OrientedBoundingBoxMinimizeType = OrientedBoundingBoxMinimizeType.ORIENTED_BOUNDING_BOX_MINIMIZE_VOLUME

ORIENTED_BOUNDING_BOX_MINIMIZE_SURFACE_AREA: OrientedBoundingBoxMinimizeType = OrientedBoundingBoxMinimizeType.ORIENTED_BOUNDING_BOX_MINIMIZE_SURFACE_AREA

ORIENTED_BOUNDING_BOX_MINIMIZE_DIAGONAL_LENGTH: OrientedBoundingBoxMinimizeType = OrientedBoundingBoxMinimizeType.ORIENTED_BOUNDING_BOX_MINIMIZE_DIAGONAL_LENGTH

def adjacency_list(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], sorted: bool = False) -> List[List[int]]:
    """
    Constructs the graph adjacency list for a given triangle mesh.

    @param[in] F       #F by dim list of mesh faces
    @param[in] sorted  Boolean flag to sort adjacency counter-clockwise
    @return            List of adjacent vertices for each vertex
    """

@overload
def adjacency_matrix(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> scipy.sparse.csc_matrix[int]:
    """
    Constructs the adjacency matrix for a simplicial mesh.

    @param[in] F  #F by dim matrix of mesh simplices
    @return A Sparse adjacency matrix of size max(F)+1 by max(F)+1
    """

@overload
def adjacency_matrix(I: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], C: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)]) -> scipy.sparse.csc_matrix[int]:
    """
    Constructs the adjacency matrix for a polygon mesh.

    @param[in] I  Vectorized list of polygon corner indices into rows of some matrix V
    @param[in] C  Cumulative polygon sizes such that C(i+1)-C(i) = size of the ith polygon
    @return A Sparse adjacency matrix of size max(I)+1 by max(I)+1
    """

def all_pairs_distances(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], U: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], squared: bool) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')]:
    """
    Compute distances between each point i in V and point j in U
        D = all_pairs_distances(V,U)
    @tparam matrix class like MatrixXd
    @param[in] V  #V by dim list of points
    @param[in] U  #U by dim list of points
    @param[in] squared  whether to return squared distances
    @param[out] D  #V by #U matrix of distances, where D(i,j) gives the distance or
        squareed distance between V(i,:) and U(j,:)
    """

class ARAPEnergyType(enum.Enum):
    ARAP_ENERGY_TYPE_DEFAULT = 3

    ARAP_ENERGY_TYPE_SPOKES = 0

    ARAP_ENERGY_TYPE_SPOKES_AND_RIMS = 1

    ARAP_ENERGY_TYPE_ELEMENTS = 2

    NUM_ARAP_ENERGY_TYPES = 4

ARAP_ENERGY_TYPE_DEFAULT: ARAPEnergyType = ARAPEnergyType.ARAP_ENERGY_TYPE_DEFAULT

ARAP_ENERGY_TYPE_SPOKES: ARAPEnergyType = ARAPEnergyType.ARAP_ENERGY_TYPE_SPOKES

ARAP_ENERGY_TYPE_SPOKES_AND_RIMS: ARAPEnergyType = ARAPEnergyType.ARAP_ENERGY_TYPE_SPOKES_AND_RIMS

ARAP_ENERGY_TYPE_ELEMENTS: ARAPEnergyType = ARAPEnergyType.ARAP_ENERGY_TYPE_ELEMENTS

NUM_ARAP_ENERGY_TYPES: ARAPEnergyType = ARAPEnergyType.NUM_ARAP_ENERGY_TYPES

class ARAPData:
    def __init__(self) -> None: ...

    @property
    def n(self) -> int: ...

    @property
    def G(self) -> Annotated[ArrayLike, dict(dtype='int32', shape=(None), order='C')]: ...

    @G.setter
    def G(self, arg: Annotated[ArrayLike, dict(dtype='int32', shape=(None), order='C')], /) -> None: ...

    @property
    def energy(self) -> ARAPEnergyType: ...

    @energy.setter
    def energy(self, arg: ARAPEnergyType, /) -> None: ...

    @property
    def with_dynamics(self) -> bool: ...

    @with_dynamics.setter
    def with_dynamics(self, arg: bool, /) -> None: ...

    @property
    def f_ext(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')]: ...

    @f_ext.setter
    def f_ext(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], /) -> None: ...

    @property
    def vel(self) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')]: ...

    @vel.setter
    def vel(self, arg: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], /) -> None: ...

    @property
    def h(self) -> float: ...

    @h.setter
    def h(self, arg: float, /) -> None: ...

    @property
    def ym(self) -> float: ...

    @ym.setter
    def ym(self, arg: float, /) -> None: ...

    @property
    def max_iter(self) -> int: ...

    @max_iter.setter
    def max_iter(self, arg: int, /) -> None: ...

def arap_precomputation(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], dim: int, b: Annotated[ArrayLike, dict(dtype='int32', shape=(None), writable=False)], data: ARAPData) -> None: ...

def arap_solve(bc: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], data: ARAPData, U: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]: ...

def average_from_edges_onto_vertices(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], E: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], oE: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], uE: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    r"""
    Move a scalar field defined on edges to vertices by averaging

    @param[in] F #F by 3 triangle mesh connectivity
    @param[in] E #E by 3 mapping from each halfedge to each edge
    @param[in] oE #E by 3 orientation as generated by orient_halfedges
    @param[in] uE #E by 1 list of scalars
    @param[out] uV #V by 1 list of  scalar defined on vertices

    \see orient_halfedges
    """

def average_onto_faces(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], S: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Move a scalar field defined on faces to faces by averaging

    @param[in] F #F by 3 triangle mesh connectivity
    @param[in] S #F by 1 scalar field defined on faces
    @param[out] SF #F by 1 scalar field defined on faces
    """

def average_onto_vertices(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], S: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Move a scalar field defined on faces to vertices by averaging

    @param[in] S #V by dim triangle mesh connectivity
    @param[in] F #F by 3 triangle mesh connectivity
    @param[in] S #F by 1 scalar field defined on faces
    @param[out] SV #V by 1 scalar field defined on vertices
    """

def avg_edge_length(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> float:
    """
    Constructs the cotangent stiffness matrix (discrete laplacian) for a given
    mesh (V,F).

      @tparam DerivedV  derived type of eigen matrix for V (e.g. derived from
        MatrixXd)
      @tparam DerivedF  derived type of eigen matrix for F (e.g. derived from
        MatrixXi)
      @tparam Scalar  scalar type for eigen sparse matrix (e.g. double)
      @param[in] V  #V by dim list of mesh vertex positions
      @param[in] F  #F by simplex_size list of mesh elements (triangles or tetrahedra)
      @param[out] L  #V by #V cotangent matrix, each row i corresponding to V(i,:)
    """

def barycenter(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Computes the barycenter of every simplex.

    @param[in] V  #V x dim matrix of vertex coordinates
    @param[in] F  #F x simplex_size  matrix of indices of simplex corners into V
    @param[out] BC  #F x dim matrix of 3d vertices
    """

@overload
def barycentric_coordinates(P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], A: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], B: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], C: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Compute barycentric coordinates of each point in a corresponding triangle

    @param[in] P  #P by 3 Query points in 3d
    @param[in] A  #P by 3 Tri corners in 3d
    @param[in] B  #P by 3 Tri corners in 3d
    @param[in] C  #P by 3 Tri corners in 3d
    @param[out] L  #P by 3 list of barycentric coordinates
    """

@overload
def barycentric_coordinates(P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], A: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], B: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], C: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], D: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Compute barycentric coordinates of each point in a corresponding tetrhedron

    @param[in] P  #P by 3 Query points in 3d
    @param[in] A  #P by 3 Tet corners in 3d
    @param[in] B  #P by 3 Tet corners in 3d
    @param[in] C  #P by 3 Tet corners in 3d
    @param[in] D  #P by 3 Tet corners in 3d
    @param[out] L  #P by 3 list of barycentric coordinates
    """

def bbw(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], Ele: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], b: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], bc: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], W0: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., partition_unity: bool = False, verbosity: int = 0, max_iter: int = 100, inactive_threshold: float = 1e-14, constraint_threshold: float = 1e-14, solution_diff_threshold: float = 1e-14) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Compute Bounded Biharmonic Weights on a given domain (V,Ele) with a given
    set of boundary conditions

    @tparam DerivedV  derived type of eigen matrix for V (e.g. MatrixXd)
    @tparam DerivedF  derived type of eigen matrix for F (e.g. MatrixXi)
    @tparam Derivedb  derived type of eigen matrix for b (e.g. VectorXi)
    @tparam Derivedbc  derived type of eigen matrix for bc (e.g. MatrixXd)
    @tparam DerivedW  derived type of eigen matrix for W (e.g. MatrixXd)
    @param[in] V  #V by dim vertex positions
    @param[in] Ele  #Elements by simplex-size list of element indices
    @param[in] b  #b boundary indices into V
    @param[in] bc #b by #W list of boundary values
    @param[in,out] data  object containing options, initial guess --> solution and results
    @param[out] W  #V by #W list of *unnormalized* weights to normalize use
       igl::normalize_row_sums(W,W)
    """

def bfs_orient(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Consistently orient faces in orientable patches using BFS.

    @param[in] F  #F by 3 list of faces
    @param[out] FF  #F by 3 list of faces (OK if same as F)
    @param[out] C  #F list of component ids
    """

def biharmonic_coordinates(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], T: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], S: Sequence[Sequence[int]], k: int = 2) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    r"""
    Compute "discrete biharmonic generalized barycentric coordinates" as
    described in "Linear Subspace Design for Real-Time Shape Deformation"
    [Wang et al. 2015]. Not to be confused with "Bounded Biharmonic Weights
    for Real-Time Deformation" [Jacobson et al. 2011] or "Biharmonic
    Coordinates" (2D complex barycentric coordinates) [Weber et al. 2012].
    These weights minimize a discrete version of the squared Laplacian energy
    subject to positional interpolation constraints at selected vertices
    (point handles) and transformation interpolation constraints at regions
    (region handles).
    @tparam SType  should be a simple index type e.g. `int`,`size_t`
    @param[in] V  #V by dim list of mesh vertex positions
    @param[in] T  #T by dim+1 list of / triangle indices into V      if dim=2
                             \ tetrahedron indices into V   if dim=3
    @param[in] S  #point-handles+#region-handles list of lists of selected vertices for
        each handle. Point handles should have singleton lists and region
        handles should have lists of size at least dim+1 (and these points
        should be in general position).
    @param[out] W  #V by #points-handles+(#region-handles * dim+1) matrix of weights so
        that columns correspond to each handles generalized barycentric
        coordinates (for point-handles) or animation space weights (for region
        handles).
    @return true only on success
    """

def bijective_composite_harmonic_mapping(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], b: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], bc: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], min_steps: int = 1, max_steps: int = 200, num_inner_iters: int = 20, test_for_flips: bool = True) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Compute a injective planar mapping of a triangulated polygon (V,F) subjected to
    boundary conditions (b,bc). The mapping should be bijective in the sense
    that no triangles' areas become negative (this assumes they started
    positive). This mapping is computed by "composing" harmonic mappings
    between incremental morphs of the boundary conditions. This is a bit like
    a discrete version of "Bijective Composite Mean Value Mappings" [Schneider
    et al. 2013] but with a discrete harmonic map (cf. harmonic coordinates)
    instead of mean value coordinates. This is inspired by "Embedding a
    triangular graph within a given boundary" [Xu et al. 2011].
    @param[in] V  #V by 2 list of triangle mesh vertex positions
    @param[in] F  #F by 3 list of triangle indices into V
    @param[in] b  #b list of boundary indices into V
    @param[in] bc  #b by 2 list of boundary conditions corresponding to b
    @param[in] min_steps  minimum number of steps to take from V(b,:) to bc
    @param[in] max_steps  minimum number of steps to take from V(b,:) to bc (if
       max_steps == min_steps then no further number of steps will be tried)
    @param[in] num_inner_iters  number of iterations of harmonic solves to run after
       for each morph step (to try to push flips back in)
    @param[in] test_for_flips  whether to check if flips occurred (and trigger more
       steps). if test_for_flips = false then this function always returns
       true
    @param[out] U  #V by 2 list of output mesh vertex locations
    @return true if and only if U contains a successful bijectie mapping
    """

def blue_noise(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], r: float) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    """
    "Fast Poisson Disk Sampling in Arbitrary Dimensions" [Bridson 2007].
    For very dense samplings this is faster than (up to 2x) cyCodeBase's
    implementation of "Sample Elimination for Generating Poisson Disk Sample
    Sets" [Yuksel 2015]. YMMV
    @param[in] V  #V by dim list of mesh vertex positions
    @param[in] F  #F by 3 list of mesh triangle indices into rows of V
    @param[in] r  Poisson disk radius (evaluated according to Euclidean distance on V)
    @param[out] B  #P by 3 list of barycentric coordinates, ith row are coordinates of
                  ith sampled point in face FI(i)
    @param[out] FI  #P list of indices into F 
    @param[out] P  #P by dim list of sample positions.
    """

def boundary_facets(T: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Determine boundary faces (edges) of tetrahedra (triangles) stored in T
    (analogous to qptoolbox's `outline` and `boundary_faces`).

    @param[in] T  tetrahedron (triangle) index list, m by 4 (3), where m is the number of tetrahedra
    @param[out] F  list of boundary faces, n by 3 (2), where n is the number
      of boundary faces. Faces are oriented so that igl::centroid(V,F,…)
    computes the same sign volume as igl::volume(V,T)
    @param[out] J  list of indices into T, n by 1
    @param[out] K  list of indices revealing across from which vertex is this facet
    """

def boundary_loop(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]:
    """
    Compute the ordered boundary loop with the most vertices for a manifold mesh.

    @param[in] F  #F by dim list of mesh faces
    @param[out]  L  ordered list of boundary vertices of longest boundary loop
    """

def boundary_loop_all(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> List[List[int]]:
    """
    Compute all ordered boundary loops for a manifold mesh.

    @param[in] F  #F by dim list of mesh faces
    @return List of lists of boundary vertices, where each sublist represents a loop
    """

def bounding_box(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], pad: float = 0) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Build a triangle mesh of the bounding box of a given list of vertices

    @param[in]  V  #V by dim list of rest domain positions
    @param[in]  pad  padding offset
    @param[out] BV  2^dim by dim list of bounding box corners positions
    @param[out] BF  #BF by dim list of simplex facets
    """

def circulation(e: int, ccw: bool, F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], EMAP: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], EF: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], EI: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[List[int], List[int]]:
    """
    Return lists of "next" vertex indices (Nv) and face indices (Nf) for circulation.

        @param[in] e  index of edge to circulate
        @param[in] ccw  circulate in ccw direction
        @param[in] F  #F by 3 list of mesh faces
        @param[in] EMAP #F*3 list of indices mapping each directed edge to a unique edge in E
        @param[in] EF  #E by 2 list of edge flaps
        @param[in] EI  #E by 2 list of edge flap corners
        @return Tuple containing Nv (next vertex indices) and Nf (face indices)
    """

def circumradius(: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    """
    Compute the circumradius of each triangle in a mesh (V,F)
    @param[in] V  #V by dim list of mesh vertex positions
    @param[in] F  #F by 3 list of triangle indices into V
    @param[out] R  #F list of circumradius
    @param[out] R  #T list of circumradius
    @param[out] C  #T by dim list of circumcenter
    @param[out] B  #T by simplex-size list of barycentric coordinates of circumcenter
    """

def collapse_edge(e: int, p: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None))], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None))], E: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None))], EMAP: Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], EF: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None))], EI: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None))]) -> Tuple[int, int, int, int]:
    """
    Attempt to collapse a given edge of a mesh. Assumes (V,F) is a closed
    manifold mesh (except for previously collapsed faces which should be set
    to: [IGL_COLLAPSE_EDGE_NULL IGL_COLLAPSE_EDGE_NULL
    IGL_COLLAPSE_EDGE_NULL]. Collapses exactly two faces and exactly 3 edges
    from E (e and one side of each face gets collapsed to the other). This is
    implemented in a way that it can be repeatedly called until satisfaction
    and then the garbage in F can be collected by removing NULL faces.

    @param[in] e  index into E of edge to try to collapse. E(e,:) = [s d] or [d s] so
        that s<d, then d is collapsed to s.
    @param[in] p  dim list of vertex position where to place merged vertex
    [mesh inputs]
    @param[in,out] V  #V by dim list of vertex positions, lesser index of E(e,:) will be set
        to midpoint of edge.
    @param[in,out] F  #F by 3 list of face indices into V.
    @param[in,out] E  #E by 2 list of edge indices into V.
    @param[in,out] EMAP #F*3 list of indices into E, mapping each directed edge to unique
        unique edge in E
    @param[in,out] EF  #E by 2 list of edge flaps, EF(e,0)=f means e=(i-->j) is the edge of
        F(f,:) opposite the vth corner, where EI(e,0)=v. Similarly EF(e,1) "
        e=(j->i)
    @param[in,out] EI  #E by 2 list of edge flap corners (see above).
    [mesh inputs]
    @param[out] e1  index into E of edge collpased on left
    @param[out] e2  index into E of edge collpased on right
    @param[out] f1  index into F of face collpased on left
    @param[out] f2  index into F of face collpased on right
    @return true if edge was collapsed

    Because there are side-effects on V,F,E,EMAP,EF,EI, this function will not
    accept all numpy variations and will refuse to copy inputs that don't match
    expected ordering and dtype.
    """

def connected_components(A: scipy.sparse.csc_matrix[int]) -> Tuple[int, Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Determine the connected components of a graph described by the input adjacency matrix.

    @param[in] A  #A by #A adjacency matrix (treated as describing a directed graph)
    @param[out] C (if return_C=True) #A list of component indices in [0,#K-1]
    @param[out] K (if return_K=True) #K list of sizes of each component
    @return number of connected components
    """

@overload
def cotmatrix(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> scipy.sparse.csc_matrix[float]:
    """
    Constructs the cotangent stiffness matrix (discrete laplacian) for a given
    mesh (V,F).

      @tparam DerivedV  derived type of eigen matrix for V (e.g. derived from
        MatrixXd)
      @tparam DerivedF  derived type of eigen matrix for F (e.g. derived from
        MatrixXi)
      @tparam Scalar  scalar type for eigen sparse matrix (e.g. double)
      @param[in] V  #V by dim list of mesh vertex positions
      @param[in] F  #F by simplex_size list of mesh elements (triangles or tetrahedra)
      @param[out] L  #V by #V cotangent matrix, each row i corresponding to V(i,:)
    """

@overload
def cotmatrix(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], I: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], C: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)]) -> Tuple[scipy.sparse.csc_matrix[float], scipy.sparse.csc_matrix[float], scipy.sparse.csc_matrix[float]]:
    r"""
    Cotangent Laplacian (and mass matrix) for polygon meshes according to
    "Polygon Laplacian Made Simple" [Bunge et al.\ 2020]

    @param[in] V  #V by 3 list of mesh vertex positions
    @param[in] I  #I vectorized list of polygon corner indices into rows of some matrix V
    @param[in] C  #polygons+1 list of cumulative polygon sizes so that C(i+1)-C(i) = size of
        the ith polygon, and so I(C(i)) through I(C(i+1)-1) are the indices of
        the ith polygon
    @param[out] L  #V by #V polygon Laplacian made simple matrix
    @param[out] M  #V by #V mass matrix
    @param[out] P  #V+#polygons by #V prolongation operator
    """

@overload
def cotmatrix_entries(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Compute the cotangent contributions for each angle in a mesh.

    @param[in] V  #V by dim matrix of vertex positions
    @param[in] F  #F by {3|4} matrix of {triangle|tetrahedra} indices into V (optional)

    @return C  #F by {3|6} matrix of cotangent contributions
        - For triangles, columns correspond to edges [1,2], [2,0], [0,1]
        - For tets, columns correspond to edges [1,2], [2,0], [0,1], [3,0], [3,1], [3,2]
    """

@overload
def cotmatrix_entries(l: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Compute the cotangent contributions for each angle in a mesh.

    @param[in] l  #F by 3 matrix of triangle edge lengths (optional, alternative to F)
    @return C  #F by {3|6} matrix of cotangent contributions
        - For triangles, columns correspond to edges [1,2], [2,0], [0,1]
        - For tets, columns correspond to edges [1,2], [2,0], [0,1], [3,0], [3,1], [3,2]
    """

def cotmatrix_intrinsic(l: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> scipy.sparse.csc_matrix[float]:
    r"""
    Constructs the cotangent stiffness matrix (discrete laplacian) for a given
    mesh with faces F and edge lengths l.

    @param[in] l  #F by 3 list of (half-)edge lengths
    @param[in] F  #F by 3 list of face indices into some (not necessarily
        determined/embedable) list of vertex positions V. It is assumed #V ==
        F.maxCoeff()+1
    @param[out] L  #V by #V sparse Laplacian matrix

    \see cotmatrix, intrinsic_delaunay_cotmatrix
    """

def crouzeix_raviart_cotmatrix(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], E: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], EMAP: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)]) -> scipy.sparse.csc_matrix[float]:
    r"""
    Compute the Crouzeix-Raviart cotangent stiffness matrix.
    See for example "Discrete Quadratic Curvature Energies" [Wardetzky, Bergou,
    Harmon, Zorin, Grinspun 2007]
    @param[in] V  #V by dim list of vertex positions
    @param[in] F  #F by 3/4 list of triangle/tetrahedron indices
    @param[in] E  #E by 2/3 list of edges/faces
    @param[in] EMAP  #F*3/4 list of indices mapping allE to E
    @param[out] L  #E by #E edge/face-based diagonal cotangent matrix
    \see crouzeix_raviart_massmatrix
    """

def crouzeix_raviart_massmatrix(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], E: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], EMAP: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)]) -> scipy.sparse.csc_matrix[float]:
    r"""
    CROUZEIX_RAVIART_MASSMATRIX Compute the Crouzeix-Raviart mass matrix where
    M(e,e) is just the sum of the areas of the triangles on either side of an
    edge e.
    See for example "Discrete Quadratic Curvature Energies" [Wardetzky, Bergou,
    Harmon, Zorin, Grinspun 2007]
    @param[in] V  #V by dim list of vertex positions
    @param[in] F  #F by 3/4 list of triangle/tetrahedron indices
    @param[in] E  #E by 2/3 list of edges/faces
    @param[in] EMAP  #F*3/4 list of indices mapping allE to E
    @param[out] M  #E by #E edge/face-based diagonal mass matrix
    \see crouzeix_raviart_cotmatrix
    """

def cut_mesh(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], C: Annotated[ArrayLike, dict(dtype='bool', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    r"""
    Given a mesh and a list of edges that are to be cut, the function
    generates a new disk-topology mesh that has the cuts at its boundary.


    \note Assumes mesh is edge-manifold.
    @param[in,out] V  #V by 3 list of the vertex positions
    @param[in,out] F  #F by 3 list of the faces
    @param[in] cuts  #F by 3 list of boolean flags, indicating the edges that need to
        be cut (has 1 at the face edges that are to be cut, 0 otherwise)
    @param[out]  Vn  #V by 3 list of the vertex positions of the cut mesh. This matrix
        will be similar to the original vertices except some rows will be
        duplicated.
    @param[out]  Fn  #F by 3 list of the faces of the cut mesh(must be triangles). This
        matrix will be similar to the original face matrix except some indices
        will be redirected to point to the newly duplicated vertices.
    @param[out]  I   #V by 1 list of the map between Vn to original V index.
    """

def cut_mesh_from_singularities(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], MMatch: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='bool', shape=(None, None), order='C')]:
    """
    Given a mesh (V,F) and the integer mismatch of a cross field per edge
    (mismatch), finds the cut_graph connecting the singularities (seams) and the
    degree of the singularities singularity_index
    @param[in] V  #V by 3 list of mesh vertex positions
    @param[in] F  #F by 3 list of faces
    @param[in] mismatch  #F by 3 list of per corner integer mismatch
    @param[out] seams  #F by 3 list of per corner booleans that denotes if an edge is a
        seam or not
    """

def cut_to_disk(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> List[List[int]]:
    """
    Given a triangle mesh, computes a set of edge cuts sufficient to carve the 
    mesh into a topological disk, without disconnecting any connected components.
    Nothing else about the cuts (including number, total length, or smoothness)
    is guaranteed to be optimal.
    Simply-connected components without boundary (topological spheres) are left
    untouched (delete any edge if you really want a disk). 
    All other connected components are cut into disks. Meshes with boundary are
    supported; boundary edges will be included as cuts.

    The cut mesh itself can be materialized using cut_mesh().

    Implements the triangle-deletion approach described by Gu et al's
    "Geometry Images."

    @tparam Index  Integrable type large enough to represent the total number of faces
        and edges in the surface represented by F, and all entries of F.
    @param[in] F  #F by 3 list of the faces (must be triangles)
    @param[out] cuts  List of cuts. Each cut is a sequence of vertex indices (where
        pairs of consecutive vertices share a face), is simple, and is either
        a closed loop (in which the first and last indices are identical) or
        an open curve. Cuts are edge-disjoint.
    """

def cylinder(axis_devisions: int, height_devisions: int) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Construct a triangle mesh of a cylinder (without caps)
    @param[in] axis_devisions  number of vertices _around the cylinder_
    @param[in] height_devisions  number of vertices _up the cylinder_
    @param[out] V  #V by 3 list of mesh vertex positions
    @param[out] F  #F by 3 list of triangle indices into V
    """

def decimate(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], F: Annotated[ArrayLike, dict(dtype='int32', shape=(None, None), order='F')], max_m: int = 0, block_intersections: bool = False) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='F')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    r"""
    Assumes (V,F) is a manifold mesh (possibly with boundary) collapses edges
    until desired number of faces is achieved. This uses default edge cost and
    merged vertex placement functions {edge length, edge midpoint}.

    See \fileinfo for more details.

    @param[in] V  #V by dim list of vertex positions
    @param[in] F  #F by 3 list of face indices into V.
    @param[in] max_m  desired number of output faces
    @param[in] block_intersections  whether to block intersections (see
      intersection_blocking_collapse_edge_callbacks)
    @param[out] U  #U by dim list of output vertex posistions (can be same ref as V)
    @param[out] G  #G by 3 list of output face indices into U (can be same ref as G)
    @param[out] J  #G list of indices into F of birth face
    @param[out] I  #U list of indices into V of birth vertices
    @return true if m was reached (otherwise #G > m)
    """

def dihedral_angles(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], T: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    """
    Compute dihedral angles for all tets of a given tet mesh (V,T).
    @param[in] V  #V by dim list of vertex positions
    @param[in] T  #V by 4 list of tet indices
    @param[out] theta  #T by 6 list of dihedral angles (in radians)
    @param[out] cos_theta  #T by 6 list of cosine of dihedral angles (in radians)
    """

def dihedral_angles_intrinsic(A: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], L: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    """
    Compute dihedral angles for all tets of a given tet mesh's intrinsics.
    @param[in] V  #V by dim list of vertex positions
    @param[in] T  #V by 4 list of tet indices
    @param[out] theta  #T by 6 list of dihedral angles (in radians)
    @param[out] cos_theta  #T by 6 list of cosine of dihedral angles (in radians)
    """

@overload
def doublearea(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)] = ...) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Computes twice the area for each input triangle or quad.

    @param[in] V  eigen matrix #V by 3
    @param[in] F  #F by (3|4) list of mesh face indices into rows of V
    @param[out] dblA #F list of triangle double areas
    """

@overload
def doublearea(A: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., B: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., C: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ...) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Computes twice the area for each input triangle or quad.

    @param[in] A #F by dim list of triangle corner positions
    @param[in] B #F by dim list of triangle corner positions
    @param[in] C #F by dim list of triangle corner positions
    @param[out] dblA #F list of triangle double areas
    """

@overload
def doublearea(l: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., nan_replacement: float = float('nan')) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Computes twice the area for each input triangle or quad.

    @param[in] l  #F by dim list of edge lengths using for triangles, columns correspond to edges 23,31,12
    @param[in] nan_replacement  what value should be used for triangles whose given
       edge lengths do not obey the triangle inequality. These may be very
       wrong (e.g., [100 1 1]) or may be nearly degenerate triangles whose
       floating point side length computation leads to breach of the triangle
       inequality. One may wish to set this parameter to 0 if side lengths l
       are _known_ to come from a valid embedding (e.g., some mesh (V,F)). In
       that case, the only circumstance the triangle inequality is broken is
       when the triangle is nearly degenerate and floating point error
       dominates: hence replacing with zero is reasonable.
    @param[out] dblA #F list of triangle double areas
    """

def ears(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Find all ears (faces with two boundary edges) in a given mesh

    @param[in] F  #F by 3 list of triangle mesh indices
    @param[out] ears  #ears list of indices into F of ears
    @param[out] ear_opp  #ears list of indices indicating which edge is non-boundary
        (connecting to flops)
    """

@overload
def edge_flaps(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], uE: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], EMAP: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Determine edge flaps with precomputed unique edge map and edge-face adjacency.

        @param[in] F  #F by 3 list of face indices
        @param[in] uE  #uE by 2 list of unique edge indices
        @param[in] EMAP #F*3 list of indices mapping each directed edge to unique edge in uE
        @return Tuple containing EF and EI matrices, where:
                EF - #E by 2 list of edge flaps
                EI - #E by 2 list of edge flap corners
    """

@overload
def edge_flaps(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Determine edge flaps, unique edge map, and edge-face adjacency from face list only.

        @param[in] F  #F by 3 list of face indices
        @return Tuple containing uE, EMAP, EF, and EI where:
                uE - #uE by 2 list of unique edge indices
                EMAP - #F*3 list mapping each directed edge to unique edge in uE
                EF - #E by 2 list of edge flaps
                EI - #E by 2 list of edge flap corners
    """

def edge_lengths(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Constructs a list of lengths of edges opposite each index in a face
    (triangle/tet) list.

    @param[in] V  eigen matrix #V by 3
    @param[in] F  #F by (2|3|4) list of mesh simplex indices into rows of V
    @param[out] L  #F by {1|3|6} list of edge lengths 
        - For edges, column of lengths
        - For triangles, columns correspond to edges [1,2],[2,0],[0,1]
        - For tets, columns correspond to edges [3 0],[3 1],[3 2],[1 2],[2 0],[0 1]
    """

@overload
def edges(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]:
    """
    Construct a list of unique edges from a given face matrix.

    @param[in] F  #F by (3|4) matrix of mesh face indices
    @return #E by 2 matrix of unique edges
    """

@overload
def edges(I: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], C: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]:
    """
    Construct a list of unique edges from a given list of polygon corner indices.

    @param[in] I  Vectorized list of polygon corner indices
    @param[in] C  #polygons+1 list of cumulative polygon sizes
    @return #E by 2 matrix of unique edges
    """

@overload
def edges(A: scipy.sparse.csc_matrix[int]) -> Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]:
    """
    Construct a list of unique edges from a given adjacency matrix.

    @param[in] A  #V by #V symmetric adjacency matrix
    @return #E by 2 matrix of unique edges
    """

def exact_geodesic(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], VS: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)] = ..., FS: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)] = ..., VT: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)] = ..., FT: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)] = ...) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Exact geodesic algorithm for computing distances on a triangular mesh.

    @param[in] V  #V by 3 matrix of vertex positions
    @param[in] F  #F by 3 matrix of face indices
    @param[in] VS #VS by 1 vector of source vertex indices
    @param[in] FS #FS by 1 vector of source face indices
    @param[in] VT #VT by 1 vector of target vertex indices
    @param[in] FT #FT by 1 vector of target face indices
    @param[out] D  #VT+#FT vector of geodesic distances from each target to the nearest source
    """

def face_areas(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], T: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Constructs a list of face areas of faces opposite each index in a tet list
    @param[in] V  #V by 3 list of mesh vertex positions
    @param[in] T  #T by 3 list of tet mesh indices into V
    @param[out] A   #T by 4 list of face areas corresponding to faces opposite vertices
        0,1,2,3
    """

def facet_adjacency_matrix(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> scipy.sparse.csc_matrix[int]:
    """
    Construct a #F×#F adjacency matrix with A(i,j)>0 indicating that faces i and j
    share an edge.

    @param[in] F  #F by 3 list of facets
    @param[out] A  #F by #F adjacency matrix
    """

def facet_components(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[int, Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Compute connected components of facets based on edge-edge adjacency.

    For connected components on vertices see igl::vertex_components

    @param[in] F  #F by 3 list of triangle indices
    @param[out] C  #F list of connected component ids
    @return number of connected components
    """

def false_barycentric_subdivision(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Refine the mesh by adding the barycenter of each face
    @param[in] V       #V by 3 coordinates of the vertices
    @param[in] F       #F by 3 list of mesh faces (must be triangles)
    @param[out] VD      #V + #F by 3 coordinate of the vertices of the dual mesh
              The added vertices are added at the end of VD (should not be
              same references as (V,F)
    @param[out] FD      #F*3 by 3 faces of the dual mesh
    """

def fast_winding_number(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], Q: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Compute approximate winding number for each query point based on a triangle soup mesh.

    @param[in] V  #V by 3 matrix of mesh vertex positions
    @param[in] F  #F by 3 matrix of triangle indices
    @param[in] Q  #Q by 3 matrix of query positions
    @return W  #Q vector of winding number values for each query point
    """

def gaussian_curvature(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Compute discrete Gaussian curvature at each vertex of a 3D mesh.

    @param[in] V  #V by 3 matrix of vertex positions
    @param[in] F  #F by 3 matrix of face indices
    @return K  #V vector of discrete Gaussian curvature values at each vertex
    """

def grad(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], uniform: bool = False) -> scipy.sparse.csc_matrix[float]:
    """
    Compute the gradient operator on a triangle mesh.

        @param[in] V        #V by 3 list of mesh vertex positions
        @param[in] F        #F by 3 (or #F by 4 for tetrahedrons) list of mesh face indices
        @param[out] G       #F*dim by #V Gradient operator
        @param[in] uniform  boolean indicating whether to use a uniform mesh instead of the vertices V
        @return Sparse gradient operator matrix G
    """

def grid(res: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Construct vertices of a regular grid.

    @param[in] res  Vector containing the number of vertices along each dimension
    @return GV Matrix containing grid vertex positions suitable for input to igl::marching_cubes.
    """

def harmonic(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], b: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], bc: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], k: int) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Compute k-harmonic weight functions "coordinates".

    @param[in] V  #V by dim vertex positions
    @param[in] F  #F by simplex-size list of element indices
    @param[in] b  #b boundary indices into V
    @param[in] bc #b by #W list of boundary values
    @param[in] k  power of harmonic operation (1: harmonic, 2: biharmonic, etc)
    @return W  #V by #W list of weights
    """

class HeatGeodesicsData:
    def __init__(self) -> None: ...

    @property
    def use_intrinsic_delaunay(self) -> bool: ...

    @use_intrinsic_delaunay.setter
    def use_intrinsic_delaunay(self, arg: bool, /) -> None: ...

@overload
def heat_geodesics_precompute(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], t: float, data: HeatGeodesicsData) -> None:
    """
    Precompute factorized solvers for computing a fast approximation of
    geodesic distances on a mesh (V,F). [Crane et al. 2013]

    @param[in] V  #V by dim list of mesh vertex positions
    @param[in] F  #F by 3 list of mesh face indices into V
    @param[in] t  "heat" parameter (smaller --> more accurate, less stable)
    @param[out] data  precomputation data (see heat_geodesics_solve)
    """

@overload
def heat_geodesics_precompute(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], data: HeatGeodesicsData) -> None:
    """
    Precompute factorized solvers for computing a fast approximation of
    geodesic distances on a mesh (V,F). [Crane et al. 2013]

    @param[in] V  #V by dim list of mesh vertex positions
    @param[in] F  #F by 3 list of mesh face indices into V
    @param[out] data  precomputation data (see heat_geodesics_solve)
    """

def heat_geodesics_solve(data: HeatGeodesicsData, gamma: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    r"""
    Compute fast approximate geodesic distances using precomputed data from a
    set of selected source vertices (gamma).

    @param[in] data  precomputation data (see heat_geodesics_precompute)
    @param[in] gamma  #gamma list of indices into V of source vertices
    @param[out] D  #V list of distances to gamma 

    \fileinfo
    """

def icosahedron() -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Construct a icosahedron with radius 1 centered at the origin

    Outputs:
      V  #V by 3 list of vertex positions
      F  #F by 3 list of triangle indices into rows of V
    """

def in_element(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], Ele: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], Q: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], aabb: AABB) -> Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]:
    """
    Determine whether each point in a list of points is in the elements of a
    mesh.

    @tparam  DIM  dimension of vertices in V (# of columns)
    @param[in] V  #V by dim list of mesh vertex positions.
    @param[in] Ele  #Ele by dim+1 list of mesh indices into #V.
    @param[in] Q  #Q by dim list of query point positions
    @param[in] aabb  axis-aligned bounding box tree object (see AABB.h)
    @param[out] I  #Q list of indices into Ele of first containing element (-1 means no
        containing element)
    """

def inradius(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Compute the inradius of each triangle in a mesh (V,F)
    @param[in] V  #V by dim list of mesh vertex positions
    @param[in] F  #F by 3 list of triangle indices into V
    @param[out] R  #F list of inradii
    """

def internal_angles(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Compute internal angles for all tets of a given tet mesh (V,T).
    @param[in] V  #V by dim eigen Matrix of mesh vertex nD positions
    @param[in] F  #F by poly-size eigen Matrix of face (triangle) indices
    @param[out] K  #F by poly-size eigen Matrix of internal angles
        for triangles, columns correspond to edges [1,2],[2,0],[0,1]
    """

def intrinsic_delaunay_cotmatrix(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[scipy.sparse.csc_matrix[float], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    r"""
    Computes the discrete cotangent Laplacian of a mesh after converting it
    into its intrinsic Delaunay triangulation (see, e.g., [Fisher et al.
    2007].

    @param[in] V  #V by dim list of mesh vertex positions
    @param[in] F  #F by 3 list of mesh elements (triangles or tetrahedra)
    @param[out] L  #V by #V cotangent matrix, each row i corresponding to V(i,:)
    @param[out] l_intrinsic  #F by 3 list of intrinsic edge-lengths used to compute L
    @param[out] F_intrinsic  #F by 3 list of intrinsic face indices used to compute L

    \see intrinsic_delaunay_triangulation, cotmatrix, cotmatrix_intrinsic
    """

def intrinsic_delaunay_triangulation(l: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], List[List[int]]]:
    r"""
    INTRINSIC_DELAUNAY_TRIANGULATION Flip edges _intrinsically_ until all are
    "intrinsic Delaunay". See "An algorithm for the construction of intrinsic
    delaunay triangulations with applications to digital geometry processing"
    [Fisher et al. 2007].

    @param[in] l_in  #F_in by 3 list of edge lengths (see edge_lengths)
    @param[in] F_in  #F_in by 3 list of face indices into some unspecified vertex list V
    @param[out] l  #F by 3 list of edge lengths
    @param[out] F  #F by 3 list of new face indices. Note: Combinatorially F may contain
        non-manifold edges, duplicate faces and self-loops (e.g., an edge [1,1]
        or a face [1,1,1]). However, the *intrinsic geometry* is still
        well-defined and correct. See [Fisher et al. 2007] Figure 3 and 2nd to
        last paragraph of 1st page. Since F may be "non-eddge-manifold" in the
        usual combinatorial sense, it may be useful to call the more verbose
        overload below if disentangling edges will be necessary later on.
        Calling unique_edge_map on this F will give a _different_ result than
        those outputs.
    @param[out] E  #F*3 by 2 list of all directed edges, such that E.row(f+#F*c) is the
    @param[out]   edge opposite F(f,c)
    @param[out] uE  #uE by 2 list of unique undirected edges
    @param[out] EMAP #F*3 list of indices into uE, mapping each directed edge to unique
    @param[out]   undirected edge
    @param[out] uE2E  #uE list of lists of indices into E of coexisting edges

    \see unique_edge_map
    """

def is_border_vertex(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> List[bool]:
    """
    Determine vertices on the open boundary of a manifold mesh with triangle faces.

    @param[in] F  #F by 3 list of triangle indices
    @return #V vector of bools indicating if vertices are on the boundary
    """

def is_edge_manifold(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[bool, Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='bool', shape=(None), order='C')]]:
    """
    Check if the mesh is edge-manifold (every edge is incident to one or two oppositely oriented faces).

    @param[in] F  #F by 3 list of triangle indices
    @param[out] BF  (if return_BF=True) #F by 3 list of flags for non-manifold edges opposite each vertex
    @param[out] E   (if return_E=True)  #E by 2 list of unique edges
    @param[out] EMAP (if return_EMAP=True) 3*#F list of indices of opposite edges in E
    @param[out] BE  (if return_BE=True)  #E list of flags for whether each edge is non-manifold
    @return True if all edges are manifold, otherwise False
    """

def is_vertex_manifold(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='bool', shape=(None), order='C')]:
    """
    Check if a mesh is vertex-manifold.

    This only checks whether the faces incident on each vertex form exactly one
    connected component. Vertices incident on non-manifold edges are not consider
    non-manifold by this function (see is_edge_manifold). Unreferenced verties are
    considered non-manifold (zero components).

    @param[in] F  #F by 3 list of triangle indices
    @return B  #V list indicate whether each vertex is locally manifold (the mesh is vertex manifold if all(B) == True
    """

def ismember_rows(A: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], B: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='bool', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Determine if row of A exist in rows of B

    @param[in] A  ma by na matrix of Integers
    @param[in] B  mb by nb matrix of Integers
    @param[out] IA  ma by 1 lest of flags whether corresponding element of A
      exists in B
    @param[out] LOCB  ma by 1 list matrix of indices in B locating matching
      element (-1 if not found), indices assume column major ordering
    """

def isolines(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], S: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], vals: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    r"""
    Compute isolines of a scalar field on a triangle mesh.

    Isolines may cross perfectly at vertices. The output should not contain
    degenerate segments (so long as the input does not contain degenerate
    faces). The output segments are *oriented* so that isolines curl
    counter-clockwise around local maxima (i.e., for 2D scalar fields). Unless
    an isoline hits a boundary, it should be a closed loop. Isolines may run
    perfectly along boundaries. Isolines should appear just "above" constants
    regions.

    @param[in] V  #V by dim list of mesh vertex positions
    @param[in] F  #F by 3 list of mesh triangle indices into V
    @param[in] S  #S by 1 list of per-vertex scalar values
    @param[in] vals  #vals by 1 list of values to compute isolines for
    @param[out] iV  #iV by dim list of isoline vertex positions
    @param[out] iE  #iE by 2 list of edge indices into iV
    @param[out] I  #iE by 1 list of indices into vals indicating which value
      each segment belongs to

    \see isolines_intrinsic, edge_crossings
    """

@overload
def isolines_intrinsic(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], S: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], vals: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    r"""
    Compute isolines of a scalar field on a triangle mesh intrinsically.

    See isolines.h for details.

    @param[in] F  #F by 3 list of mesh triangle indices into some V
    @param[in] S  #S by 1 list of per-vertex scalar values
    @param[in] vals  #vals by 1 list of values to compute isolines for
    @param[out] iB  #iB by 3 list of barycentric coordinates so that 
      iV.row(i) = iB(i,0)*V.row(F(iFI(i,0)) +
                  iB(i,1)*V.row(F(iFI(i,1)) +
                  iB(i,2)*V.row(F(iFI(i,2))
    @param[out] iF  #iB list of triangle indices for each row of iB (all
      points will either lie on an edge or vertex: an arbitrary incident face
      will be given).
    @param[out] iE  #iE by 2 list of edge indices into iB
    @param[out] I  #iE by 1 list of indices into vals indicating which value
      each segment belongs to

    \see isolines, edge_crossings
    """

@overload
def isolines_intrinsic(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], S: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], val: float, uE: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], EMAP: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], uEC: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], uEE: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    r"""
    Compute isolines of a scalar field on a triangle mesh intrinsically.

    See isolines.h for details.

    @param[in] F  #F by 3 list of mesh triangle indices into some V
    @param[in] S  #S by 1 list of per-vertex scalar values
    @param[in] val  scalar value to compute isoline at
    @param[in] uE  #uE by 2 list of unique undirected edges
    @param[in] EMAP #F*3 list of indices into uE, mapping each directed edge to unique
        undirected edge so that uE(EMAP(f+#F*c)) is the unique edge
        corresponding to E.row(f+#F*c)
    @param[in] uEC  #uE+1 list of cumulative counts of directed edges sharing each
        unique edge so the uEC(i+1)-uEC(i) is the number of directed edges
        sharing the ith unique edge.
    @param[in] uEE  #E list of indices into E, so that the consecutive segment of
        indices uEE.segment(uEC(i),uEC(i+1)-uEC(i)) lists all directed edges
        sharing the ith unique edge.
    @param[out] iB  #iB by 3 list of barycentric coordinates so that 
      iV.row(i) = iB(i,0)*V.row(F(iFI(i,0)) +
                  iB(i,1)*V.row(F(iFI(i,1)) +
                  iB(i,2)*V.row(F(iFI(i,2))
    @param[out] iF  #iB list of triangle indices for each row of iB (all
      points will either lie on an edge or vertex: an arbitrary incident face
      will be given).
    @param[out] iE  #iE by 2 list of edge indices into iB

    \see unique_edge_map
    """

class BrushType(enum.Enum):
    GRAB = 0

    SCALE = 1

    TWIST = 2

    PINCH = 3

GRAB: BrushType = BrushType.GRAB

SCALE: BrushType = BrushType.SCALE

TWIST: BrushType = BrushType.TWIST

PINCH: BrushType = BrushType.PINCH

def kelvinlets(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], x0: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], f: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], F: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], epsilon: float = 1.0, falloff: float = 1.0, brushType: BrushType = BrushType.GRAB) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Implements Pixar's Regularized Kelvinlets (Pixar Technical Memo #17-03):
    Sculpting Brushes based on Fundamental Solutions of Elasticity, a technique
    for real-time physically based volume sculpting of virtual elastic materials

    @param[in] V  #V by dim list of input points in space
    @param[in] x0  dim-vector of brush tip
    @param[in] f  dim-vector of brush force (translation)
    @param[in] F  dim by dim matrix of brush force matrix  (linear)
    @param[in] params  parameters for the kelvinlet brush like brush radius, scale etc
    @param[out] X  #V by dim list of output points in space
    """

def knn(P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], k: int, point_indices: Sequence[Sequence[int]], CH: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], CN: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], W: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]:
    """
    Given a 3D set of points P, an whole number k, and an octree
    find the indicies of the k nearest neighbors for each point in P.
    Note that each point is its own neighbor.

    The octree data structures used in this function are intended to be the
    same ones output from igl::octree

    @param[in] P  #P by 3 list of point locations
    @param[in] V  #V by 3 list of point locations for which may be neighbors 
    @param[in] k  number of neighbors to find
    @param[in] point_indices  a vector of vectors, where the ith entry is a vector of
                              the indices into P that are the ith octree cell's points
    @param[in] CH     #OctreeCells by 8, where the ith row is the indices of
                      the ith octree cell's children
    @param[in] CN     #OctreeCells by 3, where the ith row is a 3d row vector
                      representing the position of the ith cell's center
    @param[in] W      #OctreeCells, a vector where the ith entry is the width
             of the ith octree cell
    @param[out] I  #P by k list of k-nearest-neighbor indices into V
    """

def lipschitz_octree(origin: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], h0: float, max_depth: int, udf: Callable[[Annotated[ArrayLike, dict(dtype='float64', shape=(None, 3), writable=False)]], Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]]) -> Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]:
    """
    Given a minimum corner position (origin) and a side length (h0) and a
    maximum depth (max_depth), determine the possible active leaf octree cells
    based on an one-Lipschitz non-negative function to a level set (e.g.,
    "unsigned distance function").

      @param[in] origin  3-vector of root cell origin (minimum corner)
      @param[in] h0   side length of root cell
      @param[in] max_depth  maximum depth of octree (root is depth=0)
      @param[in] udf  1-Lipschitz function of (unsigned) distance to level set to a
        list of batched query points
      @param[out] ijk #ijk by 3 list of octree leaf cell minimum corner
        subscripts
    """

def local_basis(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    """
    Compute a local orthogonal reference system for each triangle in the given mesh.

        @param[in] V  #V by 3 eigen matrix of vertex positions
        @param[in] F  #F by 3 list of mesh faces (must be triangles)
        @param[out] B1 #F by 3 matrix of tangent vectors for each triangle
        @param[out] B2 #F by 3 matrix of tangent vectors perpendicular to B1 for each triangle
        @param[out] B3 #F by 3 matrix of normal vectors for each triangle
    """

def loop_matrix(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], n: int = 0) -> Tuple[scipy.sparse.csc_matrix[float], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Subdivide a mesh without moving vertices. Returns the subdivision matrix and new faces.

    @param[in] n_verts Number of mesh vertices
    @param[in] F       #F by 3 matrix of triangle faces
    @return A tuple containing:
            - S: Sparse subdivision matrix
            - NF: Matrix of new faces
    """

def loop(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], number_of_subdivs: int = 1) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Subdivide a mesh without moving vertices using loop subdivision. Returns new vertices and faces.

    @param[in] V               #V by dim matrix of mesh vertices
    @param[in] F               #F by 3 matrix of triangle faces
    @param[in] number_of_subdivs Number of subdivisions (default is 1)
    @return A tuple containing:
            - NV: New vertex positions with original vertices at the top
            - NF: Matrix of new face indices
    """

def lscm(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], b: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], bc: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], scipy.sparse.csc_matrix[float]]:
    """
    Compute a Least-squares conformal map parametrization.

        @param[in] V  #V by 3 list of mesh vertex positions
        @param[in] F  #F by 3 list of mesh faces (must be triangles)
        @param[in] b  #b list of boundary indices into V
        @param[in] bc #b by 2 list of boundary values
        @param[out] V_uv #V by 2 list of 2D mesh vertex positions in UV space
        @param[out] Q  #Vx2 by #Vx2 symmetric positive semi-definite matrix for computing LSCM energy
        @return Tuple containing:
          - V_uv: UV coordinates of vertices
          - Q: Symmetric positive semi-definite matrix for LSCM energy
    """

def map_vertices_to_circle(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], bnd: Annotated[ArrayLike, dict(dtype='int32', shape=(None), order='C')]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')]:
    """
    Map the vertices whose indices are in a given boundary loop (bnd) on the
    unit circle with spacing proportional to the original boundary edge
    lengths.
    @param[in] V  #V by dim list of mesh vertex positions
    @param[in] b  #W list of vertex ids
    @param[out] UV   #W by 2 list of 2D position on the unit circle for the vertices in b
    """

@overload
def marching_cubes(S: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], GV: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], nx: int, ny: int, nz: int, isovalue: float = 0) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Dict[int, int]]:
    """
    Performs marching cubes reconstruction on a grid defined by values, and
    points, and generates a mesh defined by vertices and faces

    @param[in] S   nx*ny*nz list of values at each grid corner
                   i.e. S(x + y*xres + z*xres*yres) for corner (x,y,z)
    @param[in] GV  nx*ny*nz by 3 array of corresponding grid corner vertex locations
    @param[in] nx  resolutions of the grid in x dimension
    @param[in] ny  resolutions of the grid in y dimension
    @param[in] nz  resolutions of the grid in z dimension
    @param[in] isovalue  the isovalue of the surface to reconstruct
    @param[out] V  #V by 3 list of mesh vertex positions
    @param[out] F  #F by 3 list of mesh triangle indices into rows of V
    @param[out] E2V  map from edge key to index into rows of V

    # unpack keys into (i,j,v) index triplets
    EV = np.array([[k & 0xFFFFFFFF, k >> 32, v] for k, v in E2V.items()], dtype=np.int64)
    """

@overload
def marching_cubes(S: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], GV: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], GI: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], isovalue: float = 0.0) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Performs marching cubes reconstruction on a grid defined by values, and
    points, and generates a mesh defined by vertices and faces

    @param[in] S #S list of scalar field values
    @param[in] GV  #S by 3 list of referenced grid vertex positions
    @param[in] GI  #GI by 8 list of grid corner indices into rows of GV
    @param[in] isovalue  the isovalue of the surface to reconstruct
    @param[out] V  #V by 3 list of mesh vertex positions
    @param[out] F  #F by 3 list of mesh triangle indices into rows of V
    """

def massmatrix(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], type: MassMatrixType = MassMatrixType.MASSMATRIX_TYPE_DEFAULT) -> scipy.sparse.csc_matrix[float]:
    r"""
    Constructs the mass (area) matrix for a given mesh (V,F).

    @tparam DerivedV  derived type of eigen matrix for V (e.g. derived from
        MatrixXd)
    @tparam DerivedF  derived type of eigen matrix for F (e.g. derived from
        MatrixXi)
    @tparam Scalar  scalar type for eigen sparse matrix (e.g. double)
    @param[in] V  #V by dim list of mesh vertex positions
    @param[in] F  #F by simplex_size list of mesh elements (triangles or tetrahedra)
    @param[in] type  one of the following ints:
        MASSMATRIX_TYPE_BARYCENTRIC  barycentric {default for tetrahedra}
        MASSMATRIX_TYPE_VORONOI voronoi-hybrid {default for triangles}
        MASSMATRIX_TYPE_FULL full
    @param[out] M  #V by #V mass matrix

    \see cotmatrix
    """

def massmatrix_intrinsic(l: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], type: MassMatrixType = MassMatrixType.MASSMATRIX_TYPE_DEFAULT) -> scipy.sparse.csc_matrix[float]:
    r"""
    Constructs the mass matrix  for a given
    mesh with faces F and edge lengths l.

    @param[in] l  #F by 3 list of (half-)edge lengths
    @param[in] F  #F by 3 list of face indices into some (not necessarily
        determined/embedable) list of vertex positions V. It is assumed #V ==
        F.maxCoeff()+1
    @param[out] L  #V by #V sparse Laplacian matrix

    \see massmatrix, intrinsic_delaunay_massmatrix
    """

@overload
def matlab_format(M: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], name: str = '') -> str:
    """Format a dense matrix for MATLAB-style output."""

@overload
def matlab_format(M: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], name: str = '') -> str:
    """Format a dense matrix for MATLAB-style output."""

@overload
def matlab_format(S: scipy.sparse.csc_matrix[float], name: str = '') -> str:
    """Format a sparse matrix for MATLAB-style output in IJV format."""

@overload
def matlab_format(v: float, name: str = '') -> str:
    """Format a double scalar for MATLAB-style output."""

@overload
def matlab_format_index(M: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], name: str = '') -> str:
    """Format a matrix for MATLAB-style output with 1-based indexing."""

@overload
def matlab_format_index(M: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], name: str = '') -> str: ...

class min_quad_with_fixed_data:
    def __init__(self) -> None: ...

def min_quad_with_fixed_solve(data: min_quad_with_fixed_data, B: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., Y: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., Beq: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ...) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """Solve the precomputed convex quadratic optimization problem."""

def min_quad_with_fixed_precompute(A: scipy.sparse.csc_matrix[float] = ..., known: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)] = ..., Aeq: scipy.sparse.csc_matrix[float] = ..., pd: bool = True, data: min_quad_with_fixed_data) -> None:
    """Precompute convex quadratic optimization problem."""

def min_quad_with_fixed(A: scipy.sparse.csc_matrix[float] = ..., B: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., known: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)] = ..., Y: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., Aeq: scipy.sparse.csc_matrix[float] = ..., Beq: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., pd: bool = True) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Minimize a convex quadratic energy subject to fixed values and linear equality constraints.

    The function minimizes trace(0.5 * Z' * A * Z + Z' * B) subject to:
        Z(known,:) = Y, and
        Aeq * Z = Beq

    @param[in] A  n by n matrix of quadratic coefficients
    @param[in] B  n by k matrix of linear coefficients
    @param[in] known  list of indices to known rows in Z
    @param[in] Y  n by k matrix of fixed values corresponding to known rows in Z
    @param[in] Aeq  m by n matrix of linear equality constraint coefficients
    @param[in] Beq  m by k matrix of linear equality constraint target values
    @param[in] pd  flag specifying whether A(unknown,unknown) is positive definite
    @param[out] Z  solution matrix that minimizes the objective under constraints
    @return Z solution matrix
    """

def moments(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[float, Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    r"""
    Computes the moments of mass for a solid object bound by a triangle mesh.

    @param[in] V  #V by 3 list of rest domain positions
    @param[in] F  #F by 3 list of triangle indices into V
    @param[out] m0  zeroth moment of mass, total signed volume of solid.
    @param[out] m1  first moment of mass, center of mass (centroid) times total mass
    @param[out] m2  second moment of mass, moment of inertia with center of mass as reference point

    \see centroid
    """

def noop(N: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., I: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)] = ..., SN: scipy.sparse.csc_matrix[float] = ..., SI: scipy.sparse.csc_matrix[int] = ...) -> object:
    """Dummy function that does nothing. Useful for timing bindings overhead."""

def octree(P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)]) -> Tuple[List[List[int]], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]]:
    """
    Given a set of 3D points P, generate data structures for a pointerless
    octree. Each cell stores its points, children, center location and width.
    Our octree is not dense. We use the following rule: if the current cell
    has any number of points, it will have all 8 children. A leaf cell will
    have -1's as its list of child indices.

    We use a binary numbering of children. Treating the parent cell's center
    as the origin, we number the octants in the following manner:
    The first bit is 1 iff the octant's x coordinate is positive
    The second bit is 1 iff the octant's y coordinate is positive
    The third bit is 1 iff the octant's z coordinate is positive

    For example, the octant with negative x, positive y, positive z is:
    110 binary = 6 decimal

    @param[in] P  #P by 3 list of point locations
    @param[out] point_indices  a vector of vectors, where the ith entry is a
      vector of the indices into P that are the ith octree cell's points
    @param[out] CH  #OctreeCells by 8, where the ith row is the indices of the
      ith octree cell's children
    @param[out] CN  #OctreeCells by 3, where the ith row is a 3d row vector
      representing the position of the ith cell's center
    @param[out] W  #OctreeCells, a vector where the ith entry is the width of
      the ith octree cell
    """

def offset_surface(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], isolevel: float, s: int, signed_distance_type: SignedDistanceType) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    """
    Compute a triangulated offset surface using matching cubes on a grid of signed distance values from the input triangle mesh.

    @param[in] V  #V by 3 list of mesh vertex positions
    @param[in] F  #F by 3 list of mesh triangle indices into V
    @param[in] isolevel  iso level to extract (signed distance: negative inside)
    @param[in] s  number of grid cells along longest side (controls resolution)
    @param[in] signed_distance_type  type of signing to use one of SIGNED_DISTANCE_TYPE_PSEUDONORMAL, SIGNED_DISTANCE_TYPE_WINDING_NUMBER, SIGNED_DISTANCE_TYPE_DEFAULT, SIGNED_DISTANCE_TYPE_UNSIGNED, SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER

    @return Tuple containing:
       - SV: #SV by 3 list of output surface mesh vertex positions
       - SF: #SF by 3 list of output mesh triangle indices into SV
       - GV: #GV=side(0)*side(1)*side(2) by 3 list of grid cell centers
       - side: list of number of grid cells in x, y, and z directions
       - so: #GV by 3 list of signed distance values _near_ `isolevel` ('far' from `isolevel` these values are incorrect)
    """

def on_boundary(T: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='bool', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='bool', shape=(None, None), order='F')]]:
    """
    Determine boundary facets of mesh elements stored in T.

    @param[in] T  m by 3|4 list of triangle or tetrahedron indices, where m is the number of elements
    @return Tuple containing:
      - I: m-length vector of bools indicating if each element is on the boundary
      - C: m by 3|4 matrix of bools indicating if each opposite facet is on the boundary
    """

def orient_halfedges(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    r"""
    Orients halfedges for a triangle mesh, assigning them to a unique edge.

    @param[in] F #F by 3 input mesh connectivity
    @param[out] E  #F by 3 a mapping from each halfedge to each edge
    @param[out] oE #F by 3 the orientation (e.g., -1 or 1) of each halfedge compared to
      the orientation of the actual edge. Every edge appears positively oriented
      exactly once.

    \see unique_simplices
    """

def oriented_bounding_box(P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], n: int = 10000, minimize_type: OrientedBoundingBoxMinimizeType = OrientedBoundingBoxMinimizeType.ORIENTED_BOUNDING_BOX_MINIMIZE_VOLUME) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Given a set of points compute the rotation transformation of them such
    that their axis-aligned bounding box is as small as possible.

    Consider passing the points on the convex hull of original list of points.

       @param[in] P  #P by 3 list of point locations
       @param[in] n  number of rotations to try
       @param[in] minimize_type  which quantity to minimize
       @param[out] R  rotation matrix
    """

def oriented_facets(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]:
    """
    Determines all directed facets of a given set of simplicial elements.

    @param[in] F  #F by simplex_size matrix of simplices
    @return E  #E by (simplex_size-1) matrix of directed facets, such that each row in E
               represents a facet opposite to a vertex in F
    """

@overload
def per_face_normals(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], Z: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)] = ...) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Compute face normals via vertex position list, face list

    @param[in] V  #V by 3 eigen Matrix of mesh vertex 3D positions
    @param[in] F  #F by 3 eigen Matrix of face (triangle) indices
    @param[in] Z  3 vector normal given to faces with degenerate normal.
    @param[out] N  #F by 3 eigen Matrix of mesh face (triangle) 3D normals
    """

@overload
def per_face_normals(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], I: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], C: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Compute face normals via vertex position list, polygon stream

    @param[in] V  #V by 3 eigen Matrix of mesh vertex 3D positions
    @param[in] I  #I vectorized list of polygon corner indices into rows of some matrix V
    @param[in] C  #polygons+1 list of cumulative polygon sizes so that C(i+1)-C(i) = size of
        the ith polygon, and so I(C(i)) through I(C(i+1)-1) are the indices of
        the ith polygon
    @param[out] N  #F by 3 eigen Matrix of mesh face (triangle) 3D normals
    @param[out] VV  #I+#polygons by 3 list of auxiliary triangle mesh vertex positions
    @param[out] FF  #I by 3 list of triangle indices into rows of VV
    @param[out] J  #I list of indices into original polygons
    """

class PerVertexNormalsWeightingType(enum.Enum):
    PER_VERTEX_NORMALS_WEIGHTING_TYPE_UNIFORM = 0

    PER_VERTEX_NORMALS_WEIGHTING_TYPE_AREA = 1

    PER_VERTEX_NORMALS_WEIGHTING_TYPE_ANGLE = 2

    PER_VERTEX_NORMALS_WEIGHTING_TYPE_DEFAULT = 3

PER_VERTEX_NORMALS_WEIGHTING_TYPE_UNIFORM: PerVertexNormalsWeightingType = PerVertexNormalsWeightingType.PER_VERTEX_NORMALS_WEIGHTING_TYPE_UNIFORM

PER_VERTEX_NORMALS_WEIGHTING_TYPE_AREA: PerVertexNormalsWeightingType = PerVertexNormalsWeightingType.PER_VERTEX_NORMALS_WEIGHTING_TYPE_AREA

PER_VERTEX_NORMALS_WEIGHTING_TYPE_ANGLE: PerVertexNormalsWeightingType = PerVertexNormalsWeightingType.PER_VERTEX_NORMALS_WEIGHTING_TYPE_ANGLE

PER_VERTEX_NORMALS_WEIGHTING_TYPE_DEFAULT: PerVertexNormalsWeightingType = PerVertexNormalsWeightingType.PER_VERTEX_NORMALS_WEIGHTING_TYPE_DEFAULT

@overload
def per_vertex_normals(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], weighting: PerVertexNormalsWeightingType = PerVertexNormalsWeightingType.PER_VERTEX_NORMALS_WEIGHTING_TYPE_DEFAULT) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Compute per-vertex normals with optional weighting and face normals.

    @param[in] V  #V by 3 matrix of vertex positions
    @param[in] F  #F by 3 matrix of face indices
    @param[in] weighting Optional string for weighting type ("uniform", "area", "angle", or "default")
    @return N  #V by 3 matrix of vertex normals
    """

@overload
def per_vertex_normals(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], weighting: PerVertexNormalsWeightingType = PerVertexNormalsWeightingType.PER_VERTEX_NORMALS_WEIGHTING_TYPE_DEFAULT, FN: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Compute per-vertex normals with optional weighting and face normals.

    @param[in] V  #V by 3 matrix of vertex positions
    @param[in] F  #F by 3 matrix of face indices
    @param[in] weighting Optional string for weighting type ("uniform", "area", "angle", or "default")
    @param[in] FN Optional #F by 3 matrix of face normals
    @return N  #V by 3 matrix of vertex normals
    """

def point_mesh_squared_distance(P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], Ele: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    r"""
    Compute distances from a set of points P to a triangle mesh (V,F)

    @param[in] P  #P by 3 list of query point positions
    @param[in] V  #V by 3 list of vertex positions
    @param[in] Ele  #Ele by (3|2|1) list of (triangle|edge|point) indices
    @param[out] sqrD  #P list of smallest squared distances
    @param[out] I  #P list of primitive indices corresponding to smallest distances
    @param[out] C  #P by 3 list of closest points

    \bug This only computes distances to given primitives. So
    unreferenced vertices are ignored. However, degenerate primitives are
    handled correctly: triangle [1 2 2] is treated as a segment [1 2], and
    triangle [1 1 1] is treated as a point. So one _could_ add extra
    combinatorially degenerate rows to Ele for all unreferenced vertices to
    also get distances to points.
    """

def polar_svd(A: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], include_reflections: bool = False) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    """
    Computes the polar decomposition of a NxN matrix A using SVD.

        @param[in] A  NxN matrix to be decomposed
        @param[in] includeReflections  Whether to allow R to be a reflection (default is False)
        @param[in] return_U  If true, include the left-singular vectors U in the output (default is False)
        @param[in] return_S  If true, include the singular values S in the output (default is False)
        @param[in] return_V  If true, include the right-singular vectors V in the output (default is False)
        @return Tuple containing (R,T) and selected outputs in the order specified by the flags
    """

@overload
def polygon_corners(P: Sequence[Sequence[int]]) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Convert a list-of-lists polygon mesh faces representation to list of
    polygon corners and sizes

    @param[in] P  #P list of lists of vertex indices into rows of some matrix V
    @param[out] I  #I vectorized list of polygon corner indices into rows of some matrix V
    @param[out] C  #P+1 list of cumulative polygon sizes so that C(i+1)-C(i) = size of
        the ith polygon, and so I(C(i)) through I(C(i+1)-1) are the indices of
        the ith polygon
    """

@overload
def polygon_corners(Q: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    r"""
    \brief Convert a pure k-gon list of polygon mesh indices to list of
    polygon corners and sizes
    @param[in] Q  #Q by k list of polygon indices (ith row is a k-gon, unless Q(i,j) =
      -1 then it's a j-gon)
    @param[out] I  #I vectorized list of polygon corner indices into rows of some matrix V
    @param[out] C  #P+1 list of cumulative polygon sizes so that C(i+1)-C(i) = size of
        the ith polygon, and so I(C(i)) through I(C(i+1)-1) are the indices of
        the ith polygon
    """

def polygons_to_triangles(I: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)], C: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Given a polygon mesh, trivially triangulate each polygon with a fan. This
    purely combinatorial triangulation will work well for convex/flat polygons
    and degrade otherwise.

    @param[in] I  #I vectorized list of polygon corner indices into rows of some matrix V
    @param[in] C  #polygons+1 list of cumulative polygon sizes so that C(i+1)-C(i) =
        size of the ith polygon, and so I(C(i)) through I(C(i+1)-1) are the
        indices of the ith polygon
    @param[out] F  #F by 3 list of triangle indices into rows of V
    @param[out] J  #F list of indices into 0:#P-1 of corresponding polygon
    """

def principal_curvature(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], radius: int = 5, useKring: bool = True) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], List[int]]:
    """
    Compute principal curvature directions and magnitudes for each vertex in a 3D mesh.

    @param[in] V  #V by 3 matrix of vertex positions
    @param[in] F  #F by 3 matrix of face indices (triangular mesh)
    @param[in] radius  controls the size of the neighborhood, where 1 corresponds to average edge length
    @param[in] useKring  boolean to use Kring neighborhood instead of ball neighborhood
    @return Tuple containing:
      - PD1: #V by 3 maximal curvature direction for each vertex
      - PD2: #V by 3 minimal curvature direction for each vertex
      - PV1: #V vector of maximal curvature values for each vertex
      - PV2: #V vector of minimal curvature values for each vertex
      - bad_vertices: list of indices of bad vertices, if any
    """

def project(scene: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], model: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], proj: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], viewport: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Eigen reimplementation of gluUnproject for batch processing.

    @param[in] scne #P by 3 matrix of screen space x, y, and z coordinates
    @param[in] model  4x4 model-view matrix
    @param[in] proj  4x4 projection matrix
    @param[in] viewport  4-long viewport vector
    @return win #P by 3 matrix of the projected x, y, and z coordinates
    """

def project_to_line(P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], S: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], D: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]]:
    """
    Project multiple points onto a line defined by points S and D.

        @param[in] P  #P by dim list of points to be projected
        @param[in] S  1 by dim starting position of line
        @param[in] D  1 by dim ending position of line
        @return Tuple containing:
                - t: #P by 1 list of parameters along the line for each point
                - sqrD: #P by 1 list of squared distances from each point to the line
    """

def project_to_line_segment(P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], S: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], D: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]]:
    """
    Project points onto a line segment defined by points S and D.

        @param[in] P  #P by dim list of points to be projected
        @param[in] S  1 by dim starting position of line segment
        @param[in] D  1 by dim ending position of line segment
        @return Tuple containing:
                - t: #P by 1 list of parameters along the line segment for each point
                - sqrD: #P by 1 list of squared distances from each point to its projection
    """

def qslim(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], F: Annotated[ArrayLike, dict(dtype='int32', shape=(None, None), order='F')], max_m: int = 0, block_intersections: bool = False) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='F')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    r"""
    Assumes (V,F) is a manifold mesh (possibly with boundary) collapses edges
    until desired number of faces is achieved. This uses default edge cost and
    merged vertex placement functions {edge length, edge midpoint}.

    See \fileinfo for more details.

    @param[in] V  #V by dim list of vertex positions
    @param[in] F  #F by 3 list of face indices into V.
    @param[in] max_m  desired number of output faces
    @param[in] block_intersections  whether to block intersections (see
      intersection_blocking_collapse_edge_callbacks)
    @param[out] U  #U by dim list of output vertex posistions (can be same ref as V)
    @param[out] G  #G by 3 list of output face indices into U (can be same ref as G)
    @param[out] J  #G list of indices into F of birth face
    @param[out] I  #U list of indices into V of birth vertices
    @return true if m was reached (otherwise #G > m)
    """

def quad_grid(nx: int, ny: int) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    r"""
    Create a regular quad quad_grid of elements (only 2D supported, currently) Vertex
    position order is compatible with `igl::quad_grid`

    @param[in] nx  number of vertices in the x direction
    @param[in] ny  number of vertices in the y direction
    @param[out] V  nx*ny by 2 list of vertex positions
    @param[out] Q  (nx-1)*(ny-1) by 4 list of quad indices into V
    @param[out] E  (nx-1)*ny+(ny-1)*nx by 2 list of undirected quad edge indices into V

    \see quad_grid, triangulated_quad_grid
    """

def random_points_on_mesh(n: int, V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], seed: Optional[int] = None) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    """
    Randomly sample a mesh (V,F) n times.

    @param[in] n  number of samples
    @param[in] V  #V by dim list of mesh vertex positions
    @param[in] F  #F by 3 list of mesh triangle indices
    @param[out] B  n by 3 list of barycentric coordinates, ith row are coordinates of
        ith sampled point in face FI(i)
    @param[in] urbg An instance of UnformRandomBitGenerator (e.g.,
     `std::minstd_rand(0)`)
    @param[out] FI  n list of indices into F 
    @param[in,out] urbg An instance of UnformRandomBitGenerator.
    @param[out] X  n by dim list of sample positions.
    """

def ray_mesh_intersect(source: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], dir: Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], first: bool = False) -> List[Tuple[int, float, float, float]]:
    """
    Shoot a ray against a mesh (V, F) and collect hits.

    @param[in] source  3-vector origin of the ray
    @param[in] dir     3-vector direction of the ray
    @param[in] V       #V by 3 list of mesh vertex positions
    @param[in] F       #F by 3 list of mesh face indices into V
    @param[in] first If True, only return the first hit (if any)
    @return Sorted list of hits if any exist, otherwise None
    """

def readDMAT(file_name: Union[str, os.PathLike]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Read a matrix from a .dmat file.

        @param[in] file_name  path to .dmat file
        @return Eigen matrix containing read-in coefficients
    """

def readMESH(mesh_file_name: Union[str, os.PathLike]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Load a tetrahedral volume mesh from a .mesh file.

    @param[in] mesh_file_name  Path of the .mesh file to read
    @return Tuple containing:
      - V: #V by 3 matrix of vertex positions
      - T: #T by 4 matrix of tetrahedral indices into vertices
      - F: #F by 3 matrix of face indices into vertices
    @throws std::runtime_error if file reading fails
    """

def readMSH(msh_file_name: Union[str, os.PathLike]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], List[str], List[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]], List[str], List[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]], List[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]]:
    r"""
    read triangle surface mesh and tetrahedral volume mesh from .msh file

    @param[in] msh - file name
    @param[out] X  eigen double matrix of vertex positions  #X by 3
    @param[out] Tri  #Tri eigen integer matrix of triangular faces indices into vertex positions
    @param[out] Tet  #Tet eigen integer matrix of tetrahedral indices into vertex positions
    @param[out] TriTag #Tri eigen integer vector of tags associated with surface faces
    @param[out] TetTag #Tet eigen integer vector of tags associated with volume elements
    @param[out] XFields #XFields list of strings with field names associated with nodes
    @param[out] XF      #XFields list of eigen double matrices, fields associated with nodes 
    @param[out] EFields #EFields list of strings with field names associated with elements
    @param[out] TriF    #EFields list of eigen double matrices, fields associated with surface elements
    @param[out] TetF    #EFields list of eigen double matrices, fields associated with volume elements
    @return true on success
    \bug only version 2.2 of .msh file is supported (gmsh 3.X)
    \bug only triangle surface elements and tetrahedral volumetric elements are supported
    \bug only 3D information is supported
    \bug only the 1st tag per element is returned (physical) 
    \bug same element fields are expected to be associated with surface elements and volumetric elements
    """

def readOBJ(filename: Union[str, os.PathLike]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Read a mesh from an ascii obj file, filling in vertex positions, normals
    and texture coordinates. Mesh may have faces of any number of degree

    @param[in] str  path to .obj file
    @param[out] V  double matrix of vertex positions  #V by 3
    @param[out] TC  double matrix of texture coordinats #TC by 2
    @param[out] N  double matrix of corner normals #N by 3
    @param[out] F  #F list of face indices into vertex positions
    @param[out] FTC  #F list of face indices into vertex texture coordinates
    @param[out] FN  #F list of face indices into vertex normals
    """

def readOFF(filename: Union[str, os.PathLike]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    """
    Read mesh from an ascii .off file

    @param[in] filename path to file
    @param[out] V  double matrix #V by 3
    @param[out] F  int matrix #F by 3
    @param[out] N,C  double matrix #V by 3 normals or colors
    @return true iff success
    """

def read_triangle_mesh(filename: Union[str, os.PathLike]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Read mesh from an ascii file with automatic detection of file format
    among: mesh, msh obj, off, ply, stl, wrl.

    @param[in] filename path to file
    @param[out] V  double matrix #V by 3
    @param[out] F  int matrix #F by 3
    @return true iff success
    """

@overload
def remove_duplicate_vertices(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], epsilon: float) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Remove duplicate vertices up to a uniqueness tolerance (epsilon).

        @param[in] V  #V by dim list of vertex positions
        @param[in] epsilon  Uniqueness tolerance used coordinate-wise
        @return Tuple containing:
                - SV: #SV by dim new list of unique vertex positions
                - SVI: #SV list of indices so SV = V(SVI,:)
                - SVJ: #V list of indices so V = SV(SVJ,:)
    """

@overload
def remove_duplicate_vertices(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], epsilon: float) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Remove duplicate vertices and remap faces to new indices.

        @param[in] V  #V by dim list of vertex positions
        @param[in] F  #F by dim list of face indices
        @param[in] return_SVJ  If true, return the SVJ mapping indices
        @return Tuple containing:
                - SV: #SV by dim new list of unique vertex positions
                - SVI: #SV list of indices so SV = V(SVI,:)
                - SVJ: #V list of indices so V = SV(SVJ,:)
                - SF: #F by dim list of remapped face indices into SV
    """

def remove_unreferenced(F: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], n: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)] = 0) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Remove unreferenced vertices from V, updating F accordingly
    @param[in] V  #V by dim list of mesh vertex positions
    @param[in] F  #F by ss list of simplices (Values of -1 are quitely skipped)
    @param[out] NV  #NV by dim list of simplices
    @param[out] NF  #NF by ss list of simplices
    @param[out] I   #V by 1 list of indices such that: NF = IM(F) and NT = IM(T)
         and V(find(IM<=size(NV,1)),:) = NV
    @param[out] J  #NV by 1 list, such that NV = V(J,:)
    """

class SignedDistanceType(enum.Enum):
    SIGNED_DISTANCE_TYPE_PSEUDONORMAL = 0

    SIGNED_DISTANCE_TYPE_WINDING_NUMBER = 1

    SIGNED_DISTANCE_TYPE_UNSIGNED = 3

    SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER = 4

    SIGNED_DISTANCE_TYPE_DEFAULT = 2

SIGNED_DISTANCE_TYPE_PSEUDONORMAL: SignedDistanceType = SignedDistanceType.SIGNED_DISTANCE_TYPE_PSEUDONORMAL

SIGNED_DISTANCE_TYPE_WINDING_NUMBER: SignedDistanceType = SignedDistanceType.SIGNED_DISTANCE_TYPE_WINDING_NUMBER

SIGNED_DISTANCE_TYPE_UNSIGNED: SignedDistanceType = SignedDistanceType.SIGNED_DISTANCE_TYPE_UNSIGNED

SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER: SignedDistanceType = SignedDistanceType.SIGNED_DISTANCE_TYPE_FAST_WINDING_NUMBER

SIGNED_DISTANCE_TYPE_DEFAULT: SignedDistanceType = SignedDistanceType.SIGNED_DISTANCE_TYPE_DEFAULT

def signed_distance(P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], sign_type: SignedDistanceType = SignedDistanceType.SIGNED_DISTANCE_TYPE_DEFAULT, lower_bound: float = float('-inf'), upper_bound: float = float('inf')) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    """
    Computes signed distance to a mesh.

    @param[in] P  #P by (2|3) list of query point positions
    @param[in] V  #V by (2|3) list of vertex positions
    @param[in] F  #F by ss list of triangle indices
    @param[in] sign_type  method for computing distance sign: "pseudonormal", "winding_number", "unsigned", "fast_winding_number", or "default"
    @param[in] lower_bound  lower bound of distances needed (default: -inf)
    @param[in] upper_bound  upper bound of distances needed (default: inf)
    @return Tuple containing:
      - S: #P list of smallest signed distances
      - I: #P list of facet indices corresponding to smallest distances
      - C: #P by (2|3) list of closest points
      - N: #P by (2|3) list of closest normals (empty unless sign_type="pseudonormal")
    """

class SLIMData:
    def __init__(self, arg0: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], arg1: Annotated[ArrayLike, dict(dtype='int32', shape=(None, None), order='F')], /) -> None: ...

def slim_precompute(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], F: Annotated[ArrayLike, dict(dtype='int32', shape=(None, None), order='F')], V_init: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], slim_energy: MappingEnergyType, b: Annotated[ArrayLike, dict(dtype='int32', shape=(None), order='C')], bc: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], soft_p: float = 100000.0) -> SLIMData:
    """
    Precompute data for SLIM optimization.

        @param[in] V  #V by 3 list of mesh vertex positions
        @param[in] F  #F by (3|4) list of mesh elements (triangles or tetrahedra)
        @param[in] V_init  #V by 3 list of initial mesh vertex positions
        @param[in] slim_energy  Energy to minimize
        @param[in] b  list of boundary indices into V
        @param[in] bc  #b by 3 list of boundary conditions
        @param[in] soft_p  Soft penalty factor (can be zero
    """

def slim_solve(data: SLIMData, iter_num: int = 1) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')]:
    """
    Run iterations of SLIM optimization.

        @param[in] data  Precomputation data structure
        @param[in] iter_num  Number of iterations to run
        @return #V by 3 list of mesh vertex positions
    """

def sparse_map_noop(A: scipy.sparse.csc_matrix[int]) -> scipy.sparse.csc_matrix[int]:
    """"Returns input A"""

def sparse_map_shape(A: scipy.sparse.csc_matrix[int]) -> Annotated[ArrayLike, dict(dtype='int64', shape=(2), order='C')]:
    """"Returns shape of A as 2-vector"""

def sparse_noop(A: scipy.sparse.csc_matrix[int]) -> scipy.sparse.csc_matrix[int]:
    """"Returns input A"""

def sparse_shape(A: scipy.sparse.csc_matrix[int]) -> Annotated[ArrayLike, dict(dtype='int64', shape=(2), order='C')]:
    """"Returns shape of A as 2-vector"""

@overload
def split_nonmanifold(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Split a non-manifold (or non-orientable) mesh into a orientable manifold
    mesh possibly with more connected components and geometrically duplicate
    vertices.
    @param[in] F  #F by 3 list of mesh triangle indices into rows of some V
    @param[out] SF  #F by 3 list of mesh triangle indices into rows of a new vertex list
                  SV = V(SVI,:)
    @param[out] SVI  #SV list of indices into V identifying vertex positions
    """

@overload
def split_nonmanifold(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Split a non-manifold (or non-orientable) mesh into a orientable manifold
    mesh possibly with more connected components and geometrically duplicate
    vertices.
    @param[in] V  #V by dim explicit list of vertex positions
    @param[in] F  #F by 3 list of mesh triangle indices into rows of some V
    @param[out] SV  #SV by dim explicit list of vertex positions
    @param[out] SF  #F by 3 list of mesh triangle indices into rows of a new vertex list
                  SV = V(SVI,:)
    @param[out] SVI  #SV list of indices into V identifying vertex positions
    """

def squared_edge_lengths(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Constructs a list of squared lengths of edges opposite each index in a face (triangle/tet) list.

    @param[in] V  #V by 3 eigen matrix of vertex positions
    @param[in] F  #F by (2|3|4) list of mesh edges, triangles, or tets
    @return L  #F by {1|3|6} matrix of squared edge lengths
        - For edges, a single column of lengths
        - For triangles, columns correspond to edges [1,2], [2,0], [0,1]
        - For tets, columns correspond to edges [3 0], [3 1], [3 2], [1 2], [2 0], [0 1]
    """

def triangle_fan(E: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]:
    """
    Given a list of faces tessellate all of the "exterior" edges forming another
    list of 
    @param[in] E  #E by simplex_size-1  list of exterior edges (see exterior_edges.h)
    @param[out] cap  #cap by simplex_size  list of "faces" tessellating the boundary edges
    """

def triangle_triangle_adjacency(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> tuple:
    """
    Constructs the triangle-triangle adjacency matrix for a given mesh (V,F).

    @param[in] F  #F by 3 list of mesh faces (must be triangles)
    @param[out] TT  #F by 3 adjacent matrix, where each element represents the id of the triangle adjacent to the corresponding edge
    @param[out] TTi (if return_TTi=True) #F by 3 adjacent matrix, where each element represents the id of the edge of the adjacent triangle that shares an edge with the current triangle

    - If `use_lists=True`, returns adjacency data as lists of lists for compatibility with non-manifold meshes.
    """

def triangle_triangle_adjacency_lists(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[List[List[List[int]]], List[List[List[int]]]]:
    """
    Constructs the triangle-triangle adjacency matrix for a given mesh (V,F).

    @param[in] F  #F by 3 list of mesh faces (must be triangles)
    @param[out] TT  #F by 3 adjacent matrix, where each element represents the id of the triangle adjacent to the corresponding edge
    @param[out] TTi (if return_TTi=True) #F by 3 adjacent matrix, where each element represents the id of the edge of the adjacent triangle that shares an edge with the current triangle

    - If `use_lists=True`, returns adjacency data as lists of lists for compatibility with non-manifold meshes.
    """

def triangulated_grid(nx: int, ny: int) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    r"""
    Create a regular grid of elements (only 2D supported, currently) Vertex
    position order is compatible with `igl::grid`

    @param[in] nx  number of vertices in the x direction
    @param[in] ny  number of vertices in the y direction
    @param[out] GV  nx*ny by 2 list of mesh vertex positions.
    @param[out] GF  2*(nx-1)*(ny-1) by 3  list of triangle indices

    \see grid, quad_grid
    """

def unique_edge_map(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> tuple:
    """
    Construct relationships between facet "half"-(or rather "viewed")-edges E
    to unique edges of the mesh seen as a graph.

    @param[in] F  #F by 3 list of simplices
    @param[out] E  #F*3 by 2 list of all directed edges
    @param[out] uE  #uE by 2 list of unique undirected edges
    @param[out] EMAP #F*3 list of indices into uE, mapping each directed edge to a unique
      undirected edge so that uE(EMAP(f+#F*c)) is the unique edge
      corresponding to E.row(f+#F*c)
    @param[out] uE2E  (if return_uE2E=True) #uE list of lists of indices into E of coexisting edges
    """

def unique_edge_map_lists(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], List[List[int]]]:
    """
    Construct relationships between facet "half"-(or rather "viewed")-edges E
    to unique edges of the mesh seen as a graph.

    @param[in] F  #F by 3 list of simplices
    @param[out] E  #F*3 by 2 list of all directed edges
    @param[out] uE  #uE by 2 list of unique undirected edges
    @param[out] EMAP #F*3 list of indices into uE, mapping each directed edge to a unique
      undirected edge so that uE(EMAP(f+#F*c)) is the unique edge
      corresponding to E.row(f+#F*c)
    @param[out] uE2E  (if return_uE2E=True) #uE list of lists of indices into E of coexisting edges
    """

def unique_simplices(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> tuple:
    """
    Find combinatorially unique simplices in F. Order independent.

    @param[in] F  #F by simplex-size list of simplices
    @param[out] FF  #FF by simplex-size list of unique simplices in F
    @param[out] IA (if return_IA=True) #FF index vector so that FF == sort(F(IA,:),2)
    @param[out] IC (if return_IC=True) #F index vector so that sort(F,2) == FF(IC,:)
    """

def unique_sparse_voxel_corners(origin: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)], h0: float, depth: int, ijk: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]]:
    """
    Give a list of octree cells subscripts (ijk) (minimum corners) at a given depth,
    determine a unique list of subscripts to all incident corners of those
    cells (de-replicating shared corners).

     @param[in] origin  3-vector of root cell minimum
     @param[in] h0   side length of current depth level
     @param[in] depth  current depth (single root cell is depth = 0)
     @param[in] ijk #ijk by 3 list of octree leaf cell minimum corner
       subscripts
     @param[out] unique_ijk #unique_ijk by 3 list of unique corner subscripts
     @param[out] J  #ijk by 8 list of indices into unique_ijk in yxz binary
       counting order
     @param[out] unique_corners #unique_ijk by 3 list of unique corner
       positions
    """

def unproject(win: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], model: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], proj: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], viewport: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')]:
    """
    Eigen reimplementation of gluUnproject for batch processing.

    @param[in] win  #P by 3 matrix of screen space x, y, and z coordinates
    @param[in] model  4x4 model-view matrix
    @param[in] proj  4x4 projection matrix
    @param[in] viewport  4-long viewport vector
    @return scene  #P by 3 matrix of the unprojected x, y, and z coordinates
    """

def upsample_matrix(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], n: int = 0) -> Tuple[scipy.sparse.csc_matrix[float], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Subdivide a mesh without moving vertices. Returns the subdivision matrix and new faces.

    @param[in] n_verts Number of mesh vertices
    @param[in] F       #F by 3 matrix of triangle faces
    @return A tuple containing:
            - S: Sparse subdivision matrix
            - NF: Matrix of new faces
    """

def upsample(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], number_of_subdivs: int = 1) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')]]:
    """
    Subdivide a mesh without moving vertices using loop subdivision. Returns new vertices and faces.

    @param[in] V               #V by dim matrix of mesh vertices
    @param[in] F               #F by 3 matrix of triangle faces
    @param[in] number_of_subdivs Number of subdivisions (default is 1)
    @return A tuple containing:
            - NV: New vertex positions with original vertices at the top
            - NF: Matrix of new face indices
    """

def vertex_components(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]:
    """
    Compute the connected components of a graph using an adjacency matrix, returning component IDs and counts.

    @param[in] F       Matrix of triangle indices
    @return            Vector C of component IDs per vertex
    """

def vertex_triangle_adjacency(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], n: int = 0) -> Tuple[Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    vertex_face_adjacency constructs the vertex-face topology of a given mesh (V,F)

     @param[in] F  #F by dim list of mesh faces (must be triangles)
     @param[in] n  number of vertices #V (e.g. `F.maxCoeff()+1` or `V.rows()`)
     @param[out] VF  #V list of lists of incident faces (adjacency list)
     @param[out] VI  #V list of lists of index of incidence within incident faces listed
         in VF
        );
    """

def vertex_triangle_adjacency_lists(F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], n: int = 0) -> Tuple[List[List[int]], List[List[int]]]:
    """
    vertex_face_adjacency constructs the vertex-face topology of a given mesh (V,F)

     @param[in] F  #F by dim list of mesh faces (must be triangles)
     @param[in] n  number of vertices #V (e.g. `F.maxCoeff()+1` or `V.rows()`)
     if using lists
     @param[out] VF  #V list of lists of incident faces (adjacency list)
     @param[out] VI  #V list of lists of index of incidence within incident faces listed
         in VF
    """

@overload
def volume(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., T: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)] = ...) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Compute volume for tetrahedrons in various input formats.

    @param[in] V  #V by dim list of vertex positions or first corner positions
    @param[in] T  #T by 4 list of tet indices 
    @return vol #T list of tetrahedron volumes
    """

@overload
def volume(L: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ...) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Compute volume for tetrahedrons in various input formats.

    @param[in] L  #V by 6 list of edge lengths (see edge_lengths)
    @return vol #T list of tetrahedron volumes
    """

@overload
def volume(A: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., B: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., C: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., D: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ...) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Compute volume for tetrahedrons in various input formats.

    @param[in] A  #A by dim list of vertex positions or first corner positions
    @param[in] B  #A by dim list of second corner positions 
    @param[in] C  #A by dim list of third corner positions 
    @param[in] D  #A by dim list of fourth corner positions 

    @return vol #T list of tetrahedron volumes
    """

def voxel_grid(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], offset: float = 0.0, s: int, pad_count: int = 0) -> Tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Constructs a voxel grid with an offset applied to each cell center.

    @param[in] V         Matrix of input vertices
    @param[in] offset    Offset to add to each cell center
    @param[in] s         Number of cell centers on the largest side
    @param[in] pad_count Number of cells beyond the box
    @return              Tuple (GV, side) where GV contains cell center positions and side defines grid dimensions
    """

@overload
def winding_number(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], O: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)]) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Computes the generalized winding number at each query point with respect to the mesh.

        @param[in] V  #V by dim list of mesh vertex positions
        @param[in] F  #F by dim list of mesh facets as indices into rows of V
        @param[in] O  #O by dim list of query points
        @return Vector of winding numbers for each query point
    """

@overload
def winding_number(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], o: Annotated[ArrayLike, dict(dtype='float64', shape=(None), writable=False)]) -> float:
    """
    Computes the generalized winding number at each query point with respect to the mesh.

        @param[in] V  #V by dim list of mesh vertex positions
        @param[in] F  #F by dim list of mesh facets as indices into rows of V
        @param[in] o  dim-vector of query point
        @return winding number
    """

def writeDMAT(file_name: Union[str, os.PathLike], W: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], ascii: bool = True) -> bool:
    """
    Write a matrix to a .dmat file in ASCII or binary format.

        @param[in] file_name  path to .dmat file
        @param[in] W  Eigen matrix containing coefficients to write
        @param[in] ascii  flag for ASCII format (default: true)
        @return True if the operation is successful
    """

def writeMESH(mesh_file_name: Union[str, os.PathLike], V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., T: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)] = ..., F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)] = ...) -> None:
    """
    Save a tetrahedral volume mesh to a .mesh file.

    @param[in] mesh_file_name  Path to the .mesh file to save
    @param[in] V  #V by 3 matrix of vertex positions
    @param[in] T  #T by 4 matrix of tetrahedral indices
    @param[in] F  #F by 3 matrix of face indices
    @throws std::runtime_error if file writing fails
    """

def writeMSH(mesh_file_name: Union[str, os.PathLike], V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., Tri: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)] = ..., Tet: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)] = ..., TriTag: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)] = ..., TetTag: Annotated[ArrayLike, dict(dtype='int64', shape=(None), writable=False)] = ...) -> None:
    """
    Save a tetrahedral volume mesh to a .msh file.

    @param[in] mesh_file_name  Path to the .mesh file to save
    @param[in] V  #V by 3 matrix of vertex positions
    @param[in] Tri  #Tri by 3 matrix of face indices
    @param[in] Tet  #Tet by 4 matrix of tetrahedral indices
    @param[in] TriTag  #Tri vector of face tags
    @param[in] TetTag  #Tet vector of tetrahedral tags
    @throws std::runtime_error if file writing fails
    """

def writeOBJ(filename: Union[str, os.PathLike], V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], CN: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., FN: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)] = ..., TC: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)] = ..., FTC: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)] = ...) -> None:
    r"""
    Write a mesh in an ascii obj file

    @param[in] str  path to outputfile
    @param[in] V  #V by 3 mesh vertex positions
    @param[in] F  #F by 3|4 mesh indices into V
    @param[in] CN #CN by 3 normal vectors
    @param[in] FN  #F by 3|4 corner normal indices into CN
    @param[in] TC  #TC by 2|3 texture coordinates
    @param[in] FTC #F by 3|4 corner texture coord indices into TC
    @return true on success, false on error

    \bug Horrifyingly, this does not have the same order of parameters as
    readOBJ.

    \see readOBJ
    """

def writePLY(filename: Union[str, os.PathLike], V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')] = ..., F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')] = ..., E: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='C')] = ..., N: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')] = ..., UV: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')] = ..., VD: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')] = ..., VDheader: Sequence[str] = [], FD: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')] = ..., FDheader: Sequence[str] = [], ED: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='C')] = ..., EDheader: Sequence[str] = [], comments: Sequence[str] = [], encoding: FileEncoding = FileEncoding.Binary) -> None:
    """
    Write a mesh to a .ply file.

     @tparam Derived from Eigen matrix parameters
     @param[in] ply_stream  ply file output stream
     @param[in] V  (#V,3) matrix of vertex positions
     @param[in] F  (#F,3) list of face indices into vertex positions
     @param[in] E  (#E,2) list of edge indices into vertex positions
     @param[in] N  (#V,3) list of normals
     @param[in] UV (#V,2) list of texture coordinates
     @param[in] VD (#V,*) additional vertex data
     @param[in] Vheader (#V) list of vertex data headers
     @param[in] FD (#F,*) additional face data
     @param[in] Fheader (#F) list of face data headers
     @param[in] ED (#E,*) additional edge data
     @param[in] Eheader (#E) list of edge data headers
     @param[in] comments (*) file comments
     @param[in] encoding - enum, to set binary or ascii file format
    """

def write_triangle_mesh(filename: Union[str, os.PathLike], V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], encoding: FileEncoding = FileEncoding.Ascii) -> None:
    """
    write mesh to a file with automatic detection of file format.  supported:
    obj, off, stl, wrl, ply, mesh).

    @tparam Scalar  type for positions and vectors (will be read as double and cast
               to Scalar)
    @tparam Index  type for indices (will be read as int and cast to Index)
    @param[in] str  path to file
    @param[in] V  eigen double matrix #V by 3
    @param[in] F  eigen int matrix #F by 3
    @param[in] encoding  set file encoding (ascii or binary) when both are available
    """
