#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""Test for miscellaneous basic functionality.
"""
import numpy as np
import pygimli as pg

from oskar import (VectorSpace, solveLinearElasticity, solve, tr, sym, I,
                   grad, div, asFunction, normL2, dirac, laplace, ScalarSpace)

from oskar.tests.utils import TestCollection, assertEqual
from oskar.elasticity import toLameCoeff, createElasticityTensor


_show_ = False

def solveLinearElasticity_(*args, atol=4e-12, **kwargs):

    """Internal test for solve linear elasticity with different backends."""
    ref = kwargs.pop('ref', None)

    u1 = solveLinearElasticity(*args, **kwargs, core=False)
    print('.', end='', flush=True)
    if ref:
        assertEqual(u1, ref, atol=atol)

    u2 = solveLinearElasticity(*args, **kwargs, core=True)
    print('.', end='', flush=True)
    assertEqual(u1, u2, atol=atol)

    u3 = solveLinearElasticity(*args, **kwargs, useMats=True)
    print('.', end='', flush=True)
    assertEqual(u1, u3, atol=atol)

    return u3


class TestLinearElasticity(TestCollection):
    """Tests for the linear elastics solver.
    """
    def test_MMS(self):
        """Test linear elastics with method of manufactured solutions.
        """
        x = np.linspace(0, 0.75, 3)
        mesh = pg.createGrid(x, x)

        E = 42      # Young's Modulus
        nu = 1/3    # Poisson's ratio

        lam, mu = toLameCoeff(E=E, nu=nu, dim=2)

        u = asFunction(u='(a - y + x)², (b + x +y )²')
        # u = asFunction(u='(a * sin(n * pi * x) * cos(n * pi * y),'
        #                  ' b * sin(n * pi * x) * cos(n * pi * y))')
        u = u(a=0.01, b=0.03, n=2)

        C = createElasticityTensor(E=E, nu=nu, dim=mesh.dim(),
                                   voigtNotation=True)

        def eps(v):
            return sym(grad(v))

        def sigmaV1(v): # wannehave
            return C*eps(v)

        lam, mu = toLameCoeff(E=E, nu=nu, dim=mesh.dim())
        def sigmaV2(v):
            return lam*tr(eps(v))*I(v) + 2.0*mu*eps(v)

        bc = {'Dirichlet':{'*':u}}

        # v = VectorSpace(mesh, p=2, order=3, elastic=True)
        # PDE = lambda u: -div(sigmaV1(u))
        # uh = solve(PDE(v) == PDE(u), bc=bc, useMats=True)
        # assertEqual(normL2(u-uh), 0.0, atol=1e-12)

        v = VectorSpace(mesh, p=2, order=3)
        PDE = lambda u: -div(sigmaV2(u))
        uh = solve(PDE(v) == PDE(u), bc=bc, useMats=True)
        assertEqual(normL2(u-uh), 0.0, atol=1e-12)

        # pg.toc()
        solveLinearElasticity_(mesh, E=E, nu=nu, var=1, bc=bc, f=PDE(u),
                               order=3, ref=uh)
        solveLinearElasticity_(mesh, E=E, nu=nu, var=2, bc=bc, f=PDE(u),
                               order=3, ref=uh)

        #TODO
        # * sigmaV1
        # * sig/eps with var1 and var2
        # * anisotropy?

        if _show_:
            m = mesh
            with pg.tictoc('init'):
                fig, axs = pg.plt.subplots(3,4, figsize=(10,10))

            with pg.tictoc('parse'):
                um = uh(m)
                epm = eps(uh)(m)
                sim = sigmaV2(uh)(m)

            with pg.tictoc('s1'):
                with pg.tictoc('s1.1'):
                    pg.show(m, abs(u), ax=axs[0][0], label=r'$\boldsymbol{u}$')
                with pg.tictoc('s1.2'):
                    pg.show(m, u, ax=axs[0][0])
                with pg.tictoc('s1.3'):
                    pg.show(m, um.T[0], ax=axs[0][1], label=r'$\boldsymbol{u}_{x}$')
                with pg.tictoc('s1.4'):
                    pg.show(m, um.T[1], ax=axs[0][2], label=r'$\boldsymbol{u}_{y}$')

            with pg.tictoc('s2'):
                with pg.tictoc('s2.1'):
                    pg.show(m, epm[:,0,0], ax=axs[1,0], label=r'$\epsilon_{xx}$')
                with pg.tictoc('s2.2'):
                    pg.show(m, epm[:,0,1], ax=axs[1,1], label=r'$\epsilon_{xy}$')
                with pg.tictoc('s2.3'):
                    pg.show(m, epm[:,1,0], ax=axs[1,2], label=r'$\epsilon_{yx}$')
                with pg.tictoc('s2.4'):
                    pg.show(m, epm[:,1,1], ax=axs[1,3], label=r'$\epsilon_{yy}$')

            with pg.tictoc('s3'):
                pg.show(m, sim[:,0,0], ax=axs[2,0], label=r'$\sigma_{xx}$')
                pg.show(m, sim[:,0,1], ax=axs[2,1], label=r'$\sigma_{xy}$')
                pg.show(m, sim[:,1,0], ax=axs[2,2], label=r'$\sigma_{yx}$')
                pg.show(m, sim[:,1,1], ax=axs[2,3], label=r'$\sigma_{yy}$')

            fig.tight_layout()


    def test_BernoulliBeam(self):
        """Test linear elastics with Euler-Bernoulli beam theory.
        """
        L = 25.
        H = 2.33
        W = 0.66
        E = 1e5
        nu = 0.3
        rho = 1e-3
        g = 9.81

        def createMesh(dim=2):
            Nx = 11
            Ny = 2
            if dim == 2:
                mesh = pg.createGrid(x=np.linspace(0, L, Nx+1),
                                        y=np.linspace(0, H, Ny+1))

                mesh = pg.meshtools.refineQuad2Tri(mesh, style=2)
            elif dim == 3:
                mesh = pg.createGrid(x=np.linspace(0, L, Nx+1),
                                        y=np.linspace(0, W, Ny+1),
                                        z=np.linspace(0, H, Ny+1))

                mesh = pg.meshtools.refineHex2Tet(mesh, style=2)
            return mesh

        def _testBodyLoad(dim=2):

            mesh = createMesh(dim)

            f = None
            if dim == 2:
                f = [0., -rho*g]
            elif dim == 3:
                f = [0., 0., -rho*g]

            C = createElasticityTensor(E=E, nu=nu, dim=mesh.dim(),
                                                   voigtNotation=True)

            v = VectorSpace(mesh, p=2, order=3, elastic=True)

            bc = {'Dirichlet': {1: [0.0, 0.0, 0.0]}}
            u = solve(grad(v) * C * grad(v) == v*f, bc=bc,
                      solver='scipy', verbose=_show_, core=True)

            # generic formulation with voigt or kelvin notation
            solveLinearElasticity_(mesh, E=E, nu=nu, rho=rho, var=1, bc=bc,
                                   order=3, ref=u)
            # isotropic formulation with small lineare strain stress
            solveLinearElasticity_(mesh, E=E, nu=nu, rho=rho, var=2, bc=bc,
                                   order=3, ref=u)

            pg.warning('!!also compare sigma and eps')


            #(https://en.wikipedia.org/wiki/Euler%E2%80%93Bernoulli_beam_theory)
            w = asFunction('q*x²*(6*L² - 4*L*x + x²)/(24*EI)')

            self.assertEqual(normL2(u-w(L=L, q=-rho*g*W, EI=E*W*H**2/12)),
                            0, atol=0.06)

            if _show_:
                ax = u.show(deform=u*300)[0]
                x = np.linspace(0, L, 21)
                wx = w(x, L=L, q=-rho*g*W, EI=E*W*H**2/12)
                if dim == 2:
                    ax.plot(x, H/2+300*wx, c='r')
                ax = pg.show()[0]
                ax.plot(x, 1000*wx, lw=1, label='Euler-Bernoulli Body-load')
                ax.plot(x, 1000*u(x)[:,dim-1], marker='.', lw=0.5,
                        label=f'Oscar dim:{dim}')
                ax.set(xlabel='$x$-coordinate in m',
                       ylabel='displacement $u_z$ in mm')
                ax.grid(True)
                ax.legend()


        def _testPointLoad(dim=2):
            mesh = createMesh(dim)

            P = 0.25*rho*g*L*(W*H)
            if dim == 2:
                f = dirac(rs=[L, W])*[0, -P]
            else:
                f = dirac(rs=[L, W])*[0, 0, -P*H]

            C = createElasticityTensor(E=E, nu=nu, dim=mesh.dim(),
                                       voigtNotation=True)

            v = VectorSpace(mesh, p=2, order=3, elastic=True)

            #bc = {'Dirichlet': {1: [0.0, 0.0, 0.0]}}
            bc = {'Fixed': 1} # same like above
            u = solve(grad(v) * C * grad(v) == v*f, bc=bc,
                      solver='scipy', verbose=_show_, core=True)

            # generic formulation with voigt or kelvin notation
            solveLinearElasticity_(mesh, E=E, nu=nu, f=f, var=1, bc=bc,
                                   order=3, atol=2e-11, ref=u)
            # isotropic formulation with small lineare strain stress
            solveLinearElasticity_(mesh, E=E, nu=nu, f=f, var=2, bc=bc,
                                   order=3, atol=2e-11, ref=u)

            pg.warning('!!also compare sigma and eps')

            #(https://en.wikipedia.org/wiki/Euler%E2%80%93Bernoulli_beam_theory)
            w = asFunction('P*x²*(3*L - x)/(6*EI)')

            if dim == 2:
                EI = E * H**3/12
            else:
                EI = E * W*H**2/12
            self.assertEqual(normL2(u-w(L=L, P=-P, EI=EI)),
                             0, atol=0.075)

            if _show_:
                x = np.linspace(0, L, 21)
                ax = u.show(deform=u*300)[0]
                wx = w(x, L=L, P=-P, EI=EI)
                if dim == 2:
                    ax.plot(x, H/2+300*wx, c='r')
                #print(normL2(wx-u(x)[:,dim-1]))
                ax = pg.show()[0]
                ax.plot(x, 1000*wx, lw=1, label='Euler-Bernoulli Point-load')
                ax.plot(x, 1000*u(x)[:,dim-1], marker='.', lw=0.5,
                        label=f'Oscar dim:{dim}')
                ax.set(xlabel='$x$-coordinate in m',
                       ylabel='displacement $u_z$ in mm')
                ax.grid(True)
                ax.legend()

        _testBodyLoad(dim=2)
        _testBodyLoad(dim=3)
        _testPointLoad(dim=2)
        _testPointLoad(dim=3)


class TestThermoElasticity(TestCollection):
    """Tests for the thermo elastic solver.
    """
    def test_thermalExpansion(self):
        """Test linear elastics with thermal expansion.
        """
        L = 1 #m
        H = 0.1
        mesh = pg.meshtools.createGrid(np.linspace(0, L, 11),
                                                [0, H/2, H],
                                                [0, H/2, H])

        mesh = pg.meshtools.refineHex2Tet(mesh)
        T0 = 0 # C
        T1 = 1 # C
        bcT = {'Dirichlet':{1:T0, 2:T1}}
        s = ScalarSpace(mesh, name='T')
        Th = solve(laplace(s) == 0, bc=bcT)

        T = asFunction('T_0 + (T_1-T_0) * x/L')(T_0=T0, T_1=T1, L=L)
        assertEqual(normL2(T-Th), 0, tol=2.5e-13)

        E = 1e5
        nu = 0.3
        beta = 1e-5
        lam, mu = toLameCoeff(E=E, G=None, nu=nu, dim=mesh.dim())

        def eps(v):
            return sym(grad(v))

        def sigma(v):
            return lam*tr(eps(v))*I(v) + 2.0*mu*eps(v)


        def sigmaEff(v, T):
            return sigma(v) - (beta*(3*lam + 2*mu)*T*I(v))




        v = VectorSpace(mesh, p=2)
        bcU = {'Dirichlet':{2:[0, 0, 0],                     # fixed right side
                            '3,4':[None, 0, 0],               # only slide in x
                            '5,6':[None, 0, 0],               # only slide in x
                            }}

        #uh = solve(-div(sigmaEff(v, Th)) == 0, bc=bcU) #wannehave
        uh = solve(grad(v)*sigmaEff(v, Th) == 0, bc=bcU)

        # v2 = VectorSpace(mesh, p=2, elastic=True)
        # C = createElasticityTensor(E=E, nu=nu, dim=mesh.dim(),
        #                            voigtNotation=True)

        # def sigmaEff2(v, T):
        #     return C*(eps(v) - beta*T*I(v))
        # ut = solve(grad(v2)*sigmaEff2(v2, Th) == 0, bc=bcU)
        # assertEqual(uh, ut, 0, tol=1e-12)

        # L = grad(v)*sigmaEff(v, Th)
        # R = L.assemble()
        # pg._g(R)
        # L = grad(v2)*sigmaEff2(v2, Th)
        # R = L.assemble()
        # pg._y(R)
        # assertEqual(uR,uh)


        u = asFunction('beta*(1+nu)/(1-nu)*(theta)/(2*L)*(x²-L²), 0, 0')
        e = eps(u)
        s = sigmaEff(u, T)
        p = dict(beta=beta, nu=nu, theta=T1-T0, L=L)

        assertEqual(normL2(u(**p)-uh), 0, tol=2.6e-15)
        x = np.linspace(0, 1, 20)
        assertEqual(normL2(e(x, **p)[:,0,0]-eps(uh)(x)[:,0,0]), 0, tol=4e-14)
        assertEqual(normL2(s(x, **p)[:,1,1]-sigmaEff(uh, T)(x)[:,1,1]),
                    0, tol=2e-9)


if __name__ == '__main__':
    import sys
    if 'show' in sys.argv:
        sys.argv.remove('show')
        _show_ = True

    import unittest
    pg.tic()
    unittest.main(exit=True)

    print()
    pg.info(f'Absolut tests: {testCount()}, took {pg.dur()} s')
