#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""Utility functions for elastic problems

TODO DOCUMENT ME
"""
import numpy as np
import pygimli as pg

from . feaSolution import FEASolution
from . elementMats import symE
from . mathOp import tr, identity
from . units import ParameterDict


class ElasticityTensor(np.ndarray):
    """ Elasticity tensor.

    Just an ndarray with an additional bool attribute voigtNotation.
    """
    def __new__(cls, input_array, voigtNotation=False):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # add the new attribute to the created instance
        obj.voigtNotation = voigtNotation
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # see InfoArray.__array_finalize__ for comments
        if obj is None: return
        self.voigtNotation = getattr(obj, 'voigtNotation', False)


ConstitutiveMatrix = ElasticityTensor


def toLameCoeff(E=None, G=None, nu=None, dim=2):
    r"""Convert elastic parameters to Lame' constants $\lambda$ and $\mu$

    Args
    ----
    E: float, dict(marker, val) [None]
        Young's Modulus
    nu: float, dict(marker, val) [None]
        Poisson's ratio
    G: float, dict(marker, val) [None]
        Shear modulus

    Returns
    -------
    lam, mu
        lam is 1. Lame' constant and mu is 2. Lame' constant (shear modulus)
        If one of the input args is a dictionary of marker and value, the returning values are are dictionary too.

    """
    lam = None
    mu = None

    markers = []

    if isinstance(E, dict):
        markers = list(E.keys())
    if isinstance(G, dict):
        markers += list(G.keys())
    if isinstance(nu, dict):
        markers += list(nu.keys())

    if len(markers) > 0:
        markers = pg.utils.unique(markers)

        lam = ParameterDict()
        mu = ParameterDict()

        for m in markers:

            try:
                _E = E[m]
            except:
                _E = E

            try:
                _G = G[m]
            except:
                _G = G

            try:
                _nu = nu[m]
            except:
                _nu = nu

            _l, _m = toLameCoeff(E=_E, G=_G, nu=_nu, dim=dim)
            lam[m] = _l
            mu[m] = _m

    else:

        if E is not None and G is not None:
            if G < 1/3 * E or G > 1/2 * E:
                pg.error(f'G need to be between {E*1/3:e} and {E*0.5:e}')

            lam = G*(E-2*G) /(3*G-E)
            mu = G
        elif E is not None and nu is not None:
            if nu == 0.5 or nu >= 1.0:
                pg.critical('nu should be greater or smaller than 0.5 and < 1')

            lam = (E * nu) / ((1 + nu) * (1 - 2*nu))
            mu  = E / (2*(1 + nu))

            if dim == 2:
                lam = 2*mu*lam/(2*mu + lam)
        else:
            print(E, G, nu, dim)
            pg.critical('implementme')

    return lam, mu


@pg.deprecate(toLameCoeff)
def toLameConstants(E=None, G=None, nu=None, dim=2):
    pass


@pg.deprecate(toLameCoeff)
def toLamMu(E=None, G=None, nu=None, dim=2):
    pass


def createElasticityTensor(lam=None, mu=None, E=None, nu=None, dim=2,
                             voigtNotation=False):
    """Create elasticity tensor for 2 or 3D isotropic media.

    Either give lam and mu or E and nu.

    TODO
    ----
        * dim == 1
        * Tests
        * Examples
        * compare Voigts/Kelvin Notation
        * anisotropy

    Parameters
    ----------
    lam: float [None]
        1. Lame' constant
    mu: float [None]
        2. Lame' constant (shear modulus G)
    E: float [None]
        Young's Modulus
    nu: float [None]
        Poisson's ratio
    voigtNotation: bool [False]
        Return in Voigt's notation instead of Kelvin's notation [default].

    Returns
    -------
    C: mat
        Either 3x3 or 6x6 matrix depending on the dimension
    """
    if voigtNotation is True:
        # pg._r('C-Voigt')
        a = 1 # Voigts notation
    else:
        # pg._y('C-Kelvin')
        a = 2 # Kelvins' notation

    if E is not None and nu is not None:
        lam, mu = toLameCoeff(E=E, nu=nu, dim=dim)

    if lam is None or mu is None:
        pg.critical("Can't find mu and lam")

    if dim == 1:
        pg.critical('C for dim==1 not yet implemented')

    elif dim == 2:
        #2d plane:
        ## for pure 2d plane stress
        C = ElasticityTensor(np.zeros((3, 3)),
                             voigtNotation=voigtNotation)
        C[0][0:2] = lam
        C[1][0:2] = lam
        C[0][0] += 2. * mu
        C[1][1] += 2. * mu
        C[2][2] = mu * a

        # C[0, 0] = 1
        # C[1, 1] = 1
        # C[0, 1] = nu
        # C[1, 0] = nu
        # C[2, 2] = (1-nu)/2 * a
        # C *= E/(1-nu**2)

    elif dim == 3:
        C = ElasticityTensor(np.zeros((6, 6)),
                             voigtNotation=voigtNotation)
        C[0][0:3] = lam
        C[1][0:3] = lam
        C[2][0:3] = lam
        C[0][0] += 2. * mu
        C[1][1] += 2. * mu
        C[2][2] += 2. * mu

        C[3][3] = mu * a
        C[4][4] = mu * a
        C[5][5] = mu * a

    #print('c2', C)

    return C


@pg.deprecate(createElasticityTensor)
def createConstitutiveMatrix(lam=None, mu=None, E=None, nu=None, dim=2,
                             voigtNotation=False):
    pass


def isMapped(v):
    """TODO."""
    return not hasattr(v, '__iter__') and v[0].ndim == 2


def asNoMapping(v):
    """Return strain or stress in matrix form for single or iterable.

    Check if v is already list of full matrix, then return v itself.

    TODO
    ----
        * TESTS.
        * rename to better name

    """
    def isFull(v):
        #    [[v00, v11], [v01, v10]]
        # or [[v00, v01, v02], [v10, v11, v12], [v20, v21, v22]]
        return v.ndim == 2 and (v.shape == [2, 2] or v.shape == [3, 3])

    if isFull(v):
        return v

    if pg.isArray(v, 3):
        #[v0, v1, v2] = v
        return np.array([[v[0], v[2]],
                         [v[2], v[1]]])
    elif pg.isArray(v, 6):
        #[v0, v1, v2, v3, v4, v5]
        return np.array([[v[0], v[3], v[5]],
                         [v[3], v[1], v[4]],
                         [v[5], v[4], v[2]]])

    ### check if already list of full
    if hasattr(v, '__iter__' ) and isFull(v[0]):
        return v

    ret = [None]*len(v)
    for i, vi in enumerate(v):
        ret[i] = asNoMapping(vi)

    return np.array(ret)


@pg.deprecate(asNoMapping)
def ensureNoMapping(v):
    pass


def asVoigtMapping(v):
    """ Return strain or stress values in Voigt mapping form.

    Return v is its already tin Voigt mapping form.
    """
    ### check if already voigt
    if pg.isArray(v, 3) or pg.isArray(v, 6):
        return v

    if pg.isArray(v, 4):
        # [xx, xy, yx, yy]
        return np.array([v[0], v[2], v[1]])
    elif pg.isArray(v, 9):
        # [xx, xy, xz, yx, yy, yz, zx, zy, zz]
        return np.array([v[0], v[4], v[8], v[1], v[3], v[2]])
    elif pg.isMatrix(v, (2,2)):
        # [[xx, xy],[yx, yy]]
        return np.array([v[0][0], v[1][1], v[0][1]])
    elif pg.isMatrix(v, (3,3)):
        # [[xx, xy, xz], [yx, yy, yz], [yx, yy, yz]]
        return np.array([v[0][0], v[1][1], v[2][2], v[0][1], v[1][2], v[0][2]])

    ### check if already list of voigt
    if isMapped(v) is True:
        pg._b(isMapped(v))
        return v

    ret = [None]*len(v)
    for i, vi in enumerate(v):
        ret[i] = asVoigtMapping(vi)

    return np.array(ret)


@pg.deprecate(asVoigtMapping)
def ensureVoigtMapping(v):
    pass


def strain(u, mesh=None, useMapping=None):
    r"""Create [strain]('link to overview doku') for displacement :math:`\textbf{u}`.

    Create strain :math:`\epsilon = \dfrac{1}{2} (\nabla \textbf{u} + (\nabla \textbf{u})^{\text{T}})`
    for each cell of the mesh associated to a FEASolution displacement
    :math:`\textbf{u}` depending on the used mapping (Kelvin or Voigt).
    :math:`\epsilon = [\epsilon_{xx}, \epsilon_{yy}, \epsilon_{xy}]` for 2D and
    :math:`\epsilon = [\epsilon_{xx}, \epsilon_{yy}, \epsilon_{zz}, \epsilon_{yx}, \epsilon_{zy}, \epsilon_{zx}]` for 3D meshes.

    Return flattend strain tensor if no mapping is used
    with :math:`\epsilon = [\epsilon_{xx}, \epsilon_{xy}, \epsilon_{yx}, \epsilon_{yy}]` for 2D
    and :math:`\epsilon = [\epsilon_{xx}, \epsilon_{xy}, \epsilon_{xz}, \epsilon_{yx}, \epsilon_{yy}, \epsilon_{yz},         \epsilon_{zx}, \epsilon_{zy}, \epsilon_{zz}]` for 3D meshes.

    Arguments
    ---------
    u: FEASolution | iterable [Nx3]
        Displacement solution or array for optional Mesh nodes
    mesh: pygimli.Mesh
        Optional mesh if u as an array
    useMapping: bool [None]
        If set to None guess the mapping from FEASpace.
        False don't use any mapping and return full eps tensor.

    Returns
    -------
    sigma: np.ndarray
        Strain values of depending on used mapping (mesh.cellCount(), C.rows()).
    """
    #pg.error('in use?') ## only used by some tests?

    if useMapping is None:
        useMapping = u.space.elastic

    if mesh is None:
        mesh = u.space.mesh

    if mesh.dim() == 2:
        if isinstance(u, FEASolution):
            ux = u.values[:,0]
            uy = u.values[:,1]
        else:
            ux = u[:,0]
            uy = u[:,1]
        uFlat = pg.cat(ux, uy)

        if useMapping:
            sDim = 3
        else:
            sDim = 4

    elif mesh.dim() == 3:
        if isinstance(u, FEASolution):
            ux = u.values[:,0]
            uy = u.values[:,1]
            uz = u.values[:,2]
        else:
            ux = u[:,0]
            uy = u[:,1]
            uz = u[:,2]
        uFlat = pg.cat(pg.cat(ux, uy), uz)

        if useMapping:
            sDim = 6
        else:
            sDim = 9
    else:
        pg.critical('implement me')

    eps = [None] * mesh.cellCount()

    oldElastic = u.space.elastic

    if useMapping == True:
        u.space.elastic = True
    else:
        u.space.elastic = False

    for c in mesh.cells():
        if useMapping: # use voigt or kelvin mapping
            du = u.space.gradE(c)
            du.integrate()

            eps[c.id()] = np.array(du.mat()).T @ uFlat[du.rowIDs()] / c.size()

            if u.space.voigt is False:
                # assume Kevin's notation
                a = 1./np.sqrt(2)
            else:
                # assume Voigt's mapping to match values without mapping
                a = 0.5

            if u.space.calcMesh.dim() == 2:
                eps[c.id()][2:] *= a
            elif u.space.calcMesh.dim() == 3:
                eps[c.id()][3:] *= a

        else:
            # eps = sym(grad(v)) = 1/2 (grad(v) + grad(v).T)
            if sDim == 6:
                implementme

            du = symE(u.space.gradE(c))
            du.integrate()

            # print(du)
            # print(np.array(du.mat()).T)
            # print(uFlat[du.rowIDs()])
            ep = np.array(du.mat()).T @ uFlat[du.rowIDs()] / c.size()

            ## fails operator for strain(u) * tr()
            #eps[c.id()] = ep.reshape(mesh.dim(), mesh.dim())

            eps[c.id()] = ep # single flatten

    u.space.elastic = oldElastic
    return np.array(eps)


def stress(u, C=None, lam=None, mu=None, mesh=None, var='plain',
           useMapping=None):
    r"""Create per cell stress values.

    TODO
    ----
        * Refactor with generic sigma expression

    Create stress values :math:`\sigma`: for each cell of the mesh based on the constitutive matrix and displacement u.
    :math:`\sigma = [\sigma_{xx}, \sigma_{yy}, \sigma_{xy}]` for 2D and
    :math:`\sigma = [\sigma_{xx}, \sigma_{yy}, \sigma_{zz}, \sigma_{yx}, \sigma_{zy}, \sigma_{zx}]` for 3D meshes.

    Arguments
    ---------
    mesh: {ref}`pg.Mesh`
        2D or 3D Mesh to calculate stress for
    u: iterable | FEASolution
        Displacement, i.e., deformation values, for each node in the mesh and need to be of size (mesh.nodeCount(), mesh.dim()).
    C: {ref}`pg.Matrix` | ndarray
        Constitutive matrix of size 3x3 for 2D and 6x6 for 3D.
    lam: float, default=None
        First Lame's parameter for isotropic material only.
    mu: float, default=None
        Second Lame's parameter for isotropic material only.
    var: str, default='plain'
        Stress variant for each cell
        - 'mean': mean stress values
        - 'plain': complete stress tensor (see description)
        - 'mises': Von Mises stress
    useMapping: bool, default=None
        If set to None Guess the mapping from FEASpace.
        For useMapping=False, don't use any mapping and return full sigma tensor.

    Returns
    -------
    sigma: ndarray
        Stress values sigma of size (mesh.cellCount(), C.rows()).
    """
    # pg.error('in use?')## only used by some old tests?
    eps = strain(u, useMapping=useMapping)

    if useMapping is None:
        useMapping = u.space.elastic

    if isinstance(C, dict):
        C = [C[m] for m in u.space.mesh.cellMarkers()]

    if useMapping and C is None:
        pg.critical('We need constitutive matrix C for stress calculation with mapping')
    # if u.space.voigt is True:
    #     pg._r('sig Voigt')
    # else:
    #     pg._y('sig Kelvin')

    s = np.zeros_like(eps)

    for i, e in enumerate(eps):

        if useMapping:
            if len(C) == u.space.mesh.cellCount():
                C_ = C[i]
            else:
                C_ = C

            if u.space.voigt is True:
                et = np.copy(e)

                if u.space.calcMesh.dim() == 2:
                    #et[2:] *= 2.0
                    #pg.warn('missing factor 2 .. please check')
                    pass
                elif u.space.calcMesh.dim() == 3:
                    et[3:] *= 2.0

                s[i] = C_@et
            else:
                s[i] = C_@e
        else:
            # print(e)
            # ## identity(v)*tr(eps(v))*lam + eps(v)*(2.0*mu)

            # print(identity(e))
            # print(tr(e))
            # if u.space.calcMesh.dim() == 2:
            #     s[i] += lam * tr(e)
            #     # tr = lam*(e[0] + e[3])
            #     # s[i][0] += tr
            #     # s[i][3] += tr
            # elif u.space.calcMesh.dim() == 3:
            #     tr = lam*(e[0] + e[4] + e[8])
            #     s[i][0] += tr
            #     s[i][4] += tr
            #     s[i][8] += tr
            if lam is None and mu is None:
                lam = C_[0][1]
                mu = (C_[0][0] -lam)/2.0

            s[i] = e*(2.0*mu) + identity(e) * lam * tr(e)

    # M x M * M x 1 = 1 x M
    # M x M * K x (M x 1) = K x (1 x M)
    #s = C@eps[:]
    #s = np.tensordot(C, eps, axes=2)

    if var.lower() != 'plain':
        return stressTo(s, var)

    return s


def stressTo(s, var):
    """ Convert stress values to mean values or Mises values.

    Arguments
    ---------
    s: iterable, ndarray
        List of stresses, in full matrix or voigt-mapped form.

    var: str, default='mean'
        Stress variant for each cell
        - 'mean': mean stress values
        - 'mises': Von Mises stress

    """
    if hasattr(s, '__iter__') and s[0].ndim == 2:
        # list of full stress matrices
        return np.array([stressTo(_s, var=var) for _s in s])
    else:
        # list of mapped values
        if var.lower() == 'mean':
            s = asNoMapping(s)
            s[1,0] = -s[0,1]
            return np.mean(s)
            # lead to unsymmetric results
            s = asVoigtMapping(s)
            return np.mean(s, axis=1)

        if var.lower() == 'mises':
            s = asVoigtMapping(s)
            if len(s) == 3:
                return np.sqrt(s[0]**2 + s[1]**2
                               - s[0]*s[1]
                               + 3*s[2]**2)
            elif len(s) == 6:
                return np.sqrt(s[0]**2 + s[1]**2 + s[2]**2
                              - s[0]*s[1] - s[1]*s[2] - s[2]*s[0]
                              + 3*(s[3]**2 + s[4]**2 + s[5]**2))
            else:
                pg._r(s[0])
                pg.critical('not yet implemented:')

    pg._r(var)
    pg.critical('not yet implemented:')


def principalStrainAxisField(eps, pos):
    """Return field for principal strain axes.

    TODO
    ----
        * Tests
        * Examples
        * docu
    """
    if isinstance(pos, pg.Mesh):
        pos = pos.positions()

    if len(eps) != len(pos):
        pg.critical('eps and pos need to have the same length')

    eps = asVoigtMapping(eps)
    exx = eps[:,0]
    eyy = eps[:,1]
    exy = eps[:,2]
    eyx = eps[:,2]

    #np.linalg.eigvals(self.matrix)
    # Mandal&Charkraborty 1990, 5(a)
    a = np.arctan2(exx - eyy, (1 + exx)*eyx + (1 + eyy)*exy)
    r = pg.abs(pos)
    c = pg.utils.toComplex(r, a) / r
    return c.real, c.imag
