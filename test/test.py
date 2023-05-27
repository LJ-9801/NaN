from nan.lib import matgen as mg
from nan.lib import ops as op
from nan.matrix import matrix
from colorama import Fore
import numpy as np
import numpy.linalg as la
import time

# font colors
red = Fore.RED
green = Fore.GREEN
success = green + 'Success' + Fore.RESET
fail = red + 'Fail' + Fore.RESET

class test:
    def __init__(self) -> None:
        self.t1 = time.monotonic()
        self.t2 = None
        self.normal = lambda i,j:mg.rand((i,j),(0,5))
        self.eye = lambda i:mg.eye(i)
        self.zeros = lambda i,j:mg.zeros((i,j))
        self.randn = lambda i,j:mg.randn((i,j),(0,5))
        self.rot2 = lambda i:mg.rot2(i)
        self.rot3 = lambda i:mg.rot3(i, 2)
        self.mat = lambda i,j,k:matrix([[i,j,k],[i,k,j],[j,k,i]])
        self.N = 24

    def test_matmul(self):
        title = "Testing matrix multiplication"
        for i in range(1,self.N):
            for j in range(1,self.N):
                a = self.normal(i,j)
                b = self.normal(j,i)
                c = a*b
                an = np.ctypeslib.as_array(a.data, (i,j))
                bn = np.ctypeslib.as_array(b.data, (j,i))
                cn = np.ctypeslib.as_array(c.data, (i,i))
                assert np.allclose(cn, an @ bn)
        print(title, success)

    def test_matadd(self):
        title = "Testing matrix addition"
        for i in range(1,self.N):
            for j in range(1,self.N):
                a = self.randn(i,j)
                b = self.normal(i,j)
                c = a+b
                an = np.ctypeslib.as_array(a.data, (i,j))
                bn = np.ctypeslib.as_array(b.data, (i,j))
                cn = np.ctypeslib.as_array(c.data, (i,j))
                assert np.allclose(cn, an + bn)
        print(title, success)

    def test_matmuladd(self):
        title = "Testing matrix multiplication and addition"
        for i in range(1,self.N):
            for j in range(1,self.N):
                a = self.randn(i,j)
                b = self.normal(j,i)
                c = self.randn(i,i)
                d = a*b+c
                an = np.ctypeslib.as_array(a.data, (i,j))
                bn = np.ctypeslib.as_array(b.data, (j,i))
                cn = np.ctypeslib.as_array(c.data, (i,i))
                dn = np.ctypeslib.as_array(d.data, (i,i))
                assert np.allclose(dn, an @ bn + cn)
        print(title, success)

    def test_matmuladdsub(self):
        title = "Testing matrix multiplication, addition and subtraction"
        for i in range(1,self.N):
            for j in range(1,self.N):
                a = self.randn(i,j)
                b = self.normal(j,i)
                c = self.randn(i,i)
                d = self.randn(i,i)
                e = a*b+c-d
                an = np.ctypeslib.as_array(a.data, (i,j))
                bn = np.ctypeslib.as_array(b.data, (j,i))
                cn = np.ctypeslib.as_array(c.data, (i,i))
                dn = np.ctypeslib.as_array(d.data, (i,i))
                en = np.ctypeslib.as_array(e.data, (i,i))
                assert np.allclose(en, an @ bn + cn - dn)
        print(title, success)

    def test_eigendecomp(self):
        title = "Testing eigen decomposition"
        for i in range(2,self.N):
            for j in range(2,self.N):
                for k in range(2, self.N):
                    ma = self.mat(i,j,k)
                    wr, wi,v = op.eig(ma)
                    an = np.ctypeslib.as_array(ma.data, (3,3))
                    wn = np.ctypeslib.as_array(wr.data, (3,))
                    vn = np.ctypeslib.as_array(v.data, (9,)).reshape(3,3)
                    wnn, vnn = la.eig(an)
                    wn = np.sort(wn); wnn = np.sort(wnn)
                    vn = la.norm(np.sort(vn, axis=0), axis=1); vnn = la.norm(np.sort(vnn, axis=0), axis=1)
                    assert np.allclose(wn, wnn.real, atol=1e-2)
        print(title, success)

    def test_svd(self):
        title = "Testing singular value decomposition"
        for i in range(2,self.N):
            for j in range(2,self.N):
                a = self.randn(i,j)
                u,s,v = op.svd(a)
                an = u*s*v
                a = np.ctypeslib.as_array(a.data, (i,j))
                an = np.ctypeslib.as_array(an.data, (i,j))
                assert np.allclose(a, an, atol=1e-3)
        print(title, success)

    def test_transpose(self):
        title = "Testing transpose"
        for i in range(2,self.N):
            for j in range(2,self.N):
                a = self.randn(i,j)
                b = a.T()
                an = np.ctypeslib.as_array(a.data, (i,j))
                bn = np.ctypeslib.as_array(b.data, (j,i))
                assert np.allclose(an.T, bn)
        print(title, success)

    def test_all(self):
        self.test_matmul()
        self.test_matadd()
        self.test_matmuladd()
        self.test_matmuladdsub()
        self.test_eigendecomp()
        self.test_svd()
        self.test_transpose()


if __name__ == "__main__":
    t = test()
    t.test_all()

                
        