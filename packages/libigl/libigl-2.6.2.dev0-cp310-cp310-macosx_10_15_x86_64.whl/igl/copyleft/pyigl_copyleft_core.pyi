from typing import Annotated

from numpy.typing import ArrayLike


def progressive_hulls(V: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], F: Annotated[ArrayLike, dict(dtype='int32', shape=(None, None), order='F')], max_m: int = 0) -> tuple[Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F')], Annotated[ArrayLike, dict(dtype='int64', shape=(None, None), order='F')], Annotated[ArrayLike, dict(dtype='int64', shape=(None), order='C')]]:
    """
    Performs progressive hull simplification on a mesh, collapsing edges until a target number of faces is reached.

        @param[in] V  #V by dim list of vertex positions
        @param[in] F  #F by 3 list of face indices into V
        @param[in] max_m Target number of output faces
        @param[out] U Output vertex positions
        @param[out] G Output face indices into U
        @param[out] J Indices into F indicating the birth face for each face in G
    """
