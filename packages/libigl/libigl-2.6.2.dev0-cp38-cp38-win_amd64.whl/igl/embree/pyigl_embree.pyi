from typing import Annotated, List, Tuple, overload

from numpy.typing import ArrayLike


class EmbreeIntersector:
    def __init__(self) -> None: ...

    def init(self, V: Annotated[ArrayLike, dict(dtype='float32', shape=(None, 3), order='F')], F: Annotated[ArrayLike, dict(dtype='int32', shape=(None, 3), order='F')], isStatic: bool = False) -> None: ...

    def intersectRay_first(self, origin: Annotated[ArrayLike, dict(dtype='float32', shape=(3), order='C')], direction: Annotated[ArrayLike, dict(dtype='float32', shape=(3), order='C')], tnear: float = 0, tfar: float = float('inf')) -> Tuple[int, float, float, float]: ...

    def intersectRay(self, origin: Annotated[ArrayLike, dict(dtype='float32', shape=(3), order='C')], direction: Annotated[ArrayLike, dict(dtype='float32', shape=(3), order='C')], tnear: float = 0, tfar: float = float('inf')) -> Tuple[List[Tuple[int, float, float, float]], int]: ...

@overload
def ambient_occlusion(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], N: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], num_samples: int) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Compute ambient occlusion per given point

    @param[in] V  #V by 3 list of mesh vertex positiosn
    @param[in] F  #F by 3 list of mesh triangle indices into rows of V
    @param[in] P  #P by 3 list of origin points
    @param[in] N  #P by 3 list of origin normals
    @param[out] S  #P list of ambient occlusion values between 1 (fully occluded) and
         0 (not occluded)
    """

@overload
def ambient_occlusion(ei: EmbreeIntersector, P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], N: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], num_samples: int) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Compute ambient occlusion per given point

    @param[in] ei  EmbreeIntersector containing (V,F)
    @param[in] P  #P by 3 list of origin points
    @param[in] N  #P by 3 list of origin normals
    @param[out] S  #P list of ambient occlusion values between 1 (fully occluded) and
         0 (not occluded)
    """

def reorient_facets_raycast(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], rays_total: int = -1, rays_minimum: int = 10, facet_wise: bool = False, use_parity: bool = False, is_verbose: bool = False) -> Tuple[Annotated[ArrayLike, dict(dtype='bool', shape=(None), order='C')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Orient each component (identified by C) of a mesh (V,F) using ambient
    occlusion such that the front side is less occluded than back side, as
    described in "A Simple Method for Correcting Facet Orientations in
    Polygon Meshes Based on Ray Casting" [Takayama et al. 2014].

    @param[in] V  #V by 3 list of vertex positions
    @param[in] F  #F by 3 list of triangle indices
    @param[in] rays_total  Total number of rays that will be shot
    @param[in] rays_minimum  Minimum number of rays that each patch should receive
    @param[in] facet_wise  Decision made for each face independently, no use of patches
        (i.e., each face is treated as a patch)
    @param[in] use_parity  Use parity mode
    @param[in] is_verbose  Verbose output to cout
    @param[out] I  #F list of whether face has been flipped
    @param[out] C  #F list of patch ID (output of bfs_orient > manifold patches)
    """

@overload
def shape_diameter_function(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], F: Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), writable=False)], P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], N: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], num_samples: int) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Compute shape diameter function per given point

    @param[in] V  #V by 3 list of mesh vertex positiosn
    @param[in] F  #F by 3 list of mesh triangle indices into rows of V
    @param[in] P  #P by 3 list of origin points
    @param[in] N  #P by 3 list of origin normals
    @param[out] S  #P list of ambient occlusion values between 1 (fully occluded) and
         0 (not occluded)
    """

@overload
def shape_diameter_function(ei: EmbreeIntersector, P: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], N: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), writable=False)], num_samples: int) -> Annotated[ArrayLike, dict(dtype='float64', shape=(None), order='C')]:
    """
    Compute shape diameter function per given point

    @param[in] ei  EmbreeIntersector containing (V,F)
    @param[in] P  #P by 3 list of origin points
    @param[in] N  #P by 3 list of origin normals
    @param[out] S  #P list of ambient occlusion values between 1 (fully occluded) and
         0 (not occluded)
    """
