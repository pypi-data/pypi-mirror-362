import numpy as np
from shps.solve.laplace import laplace_neumann
from shps.solve.poisson import poisson_neumann

class WarpingAnalysis:
    def __init__(self, model):
        self.model = model
        self.nodes = model.nodes
        self.elems = model.elems

        self._solution = None
        self._warping = None 
        self._centroid = None
        self._shear_center = None

        self._nn = None
        self._mm = None 
        self._ww = None
        self._vv = None
        self._nm = None
        self._mw = None
        self._mv = None
        self._nv = None

    def translate(self, vect):
        return WarpingAnalysis(self.model.translate(vect))

    def section_tensor(self):
        owv = np.zeros((1,1))
        return np.block([[self.cnn()  , self.cnm(),   self.cnw(), self.cnv()],
                         [self.cnm().T, self.cmm(),   self.cmw(), self.cmv()],
                         [self.cnw().T, self.cmw().T, self.cww(),      owv  ],
                         [self.cnv().T, self.cmv().T,      owv.T, self.cvv()]])

    def cnn(self):
        if self._nn is not None:
            return self._nn
        e = np.ones(len(self.model.nodes))
        A = self.model.inertia(e,e)
        self._nn = np.array([[A, 0, 0],
                             [0, 0, 0],
                             [0, 0, 0]])
        return self._nn

    def cmm(self):
        if self._mm is not None:
            return self._mm 

        y,z = self.model.nodes.T
        izy = self.model.inertia(z,y)
        izz = self.model.inertia(y,y)
        iyy = self.model.inertia(z,z)
        self._mm = np.array([[izz+iyy,   0,    0],
                             [   0   , iyy, -izy],
                             [   0   ,-izy,  izz]])
        return self._mm

    def cww(self):
        """
        \\int \\varphi \\otimes \\varphi
        """
        if self._ww is None:
            w = self.solution()
            Iw = self.model.inertia(w, w)
            self._ww = np.array([[Iw]])
        return self._ww

    def cvv(self):
        if self._vv is None:
            # w = self.warping()
            w = self.solution()
            Iww = self.model.energy(w, w)
            self._vv = np.array([[Iww]])
        return self._vv

    def cnm(self):
        if self._nm is not None:
            return self._nm
        y,z = self.model.nodes.T
        e  = np.ones(len(self.model.nodes))
        Qy = self.model.inertia(e,z)
        Qz = self.model.inertia(e,y)
        self._nm = np.array([[ 0,  Qy, -Qz],
                             [-Qy,  0,   0],
                             [ Qz,  0,   0]])
        return self._nm

    def cmw(self):
        if self._mw is not None:
            return self._mw
        y,z =  self.model.nodes.T
        w = self.solution()
        iwy = self.model.inertia(w,z)
        iwz = self.model.inertia(w,y)
        self._mw = np.array([[  0 ],
                             [ iwy],
                             [-iwz]])
        return self._mw

    def cmv(self):
        if self._mv is not None:
            return self._mv

        w = self.solution()

        yz  = self.model.nodes
        cxx = self.model.curl(yz, w)
        self._mv = np.array([[cxx],
                             [0.0],
                             [0.0]])
        return self._mv


    def css(self):
        w = self.solution()

        u = poisson_neumann(
            self.model.nodes,
            self.model.elems,
            load_fun = w
        )
        print(len(u))
        return self.model.inertia(u,w)
    def cnv(self):
        if self._nv is not None:
            return self._nv
        w = self.solution()

        i = np.zeros_like(self.model.nodes)
        i[:,1] = -1
        # i[:,0] = 1
        cxy = self.model.curl(i, w)
        # i[:,1] = 1
        # i[:,0] = 0
        i[:,0] = 1
        i[:,1] = 0
        cxz = self.model.curl(i, w)
        self._nv = np.array([[0.0],
                             [cxy],
                             [cxz]])
        return self._nv


    def cnw(self, ua=None)->float:
        # Normalizing Constant = -warpIntegral / A
        c = 0.0

        if ua is not None:
            for i,elem in enumerate(self.model.elems):
                area = self.model.cell_area(i)
                c += sum(ua[elem.nodes])/3.0 * area

        return np.array([[ c ], 
                         [0.0],
                         [0.0]])


    def solution(self):
        """
        # We should have 
        #   self.model.inertia(np.ones(nf), warp) ~ 0.0
        """
        if self._solution is None:
            # self._solution = laplace_neumann(self.model.nodes, self.model.elems)
            self._solution = poisson_neumann(self.model.nodes, self.model.elems)
            cnw = self.cnw(self._solution)[0,0]
            cnn = self.cnn()[0,0]
            self._solution -= cnw/cnn
        return self._solution
    

    def centroid(self):
        if self._centroid is not None:
            return self._centroid
        A = self.cnn()[0,0]
        cnm = self.cnm()
        Qy = cnm[0,1] # int z
        Qz = cnm[2,0] # int y
        self._centroid = float(Qz/A), float(Qy/A)
        return self._centroid

    def shear_center(self):
        if self._shear_center is not None:
            return self._shear_center

        cmm = self.translate(self.centroid()).cmm()
        # cmm = self.cmm()

        I = np.array([[ cmm[1,1],  cmm[1,2]],
                      [ cmm[2,1],  cmm[2,2]]])

        _, iwy, iwz = self.cmw()[:,0]
        # _, iwz, iwy = -cen.cmw()
        ysc, zsc = np.linalg.solve(I, [iwy, iwz])
        self._shear_center = (
            float(ysc), #-c[0,0], 
            float(zsc), #+c[1,0]
        )
        return self._shear_center

    def warping(self):
        if self._warping is not None:
            return self._warping

        w = self.solution() 
        # w = self.translate(self.centroid()).solution()

        y,   z = self.model.nodes.T
        cy, cz = self.centroid()
        yc = y - cy 
        zc = z - cz
        sy, sz = self.shear_center()
        # sy = -sy 
        # sz = -sz
        # w =  w + np.array([ys, -zs])@self.model.nodes.T
        w = w + sy*zc - sz*yc

        self._warping = w

        return self._warping


    def torsion_constant(self):
        """
        Compute St. Venant's constant.
        """
        # J = Io + Irw
        return self.cmm()[0,0] + self.cmv()[0,0]

        nodes = self.model.nodes
        J  = 0
        for i,elem in enumerate(self.model.elems):
            ((y1, y2, y3), (z1, z2, z3)) = nodes[elem.nodes].T

            z23 = z2 - z3
            z31 = z3 - z1
            z12 = z1 - z2
            y32 = y3 - y2
            y13 = y1 - y3
            y21 = y2 - y1

            u1, u2, u3 = warp[elem.nodes]

            # Element area
            area = self.model.cell_area(i)

            # St. Venant constant
            Czeta1  = ( u2*y1 * y13 + u3 *  y1 * y21 + u1 * y1*y32 - u3 * z1 * z12 - u1*z1 * z23 - u2*z1*z31)/(2*area)
            Czeta2  = (u2*y13 *  y2 + u3 *  y2 * y21 + u1 * y2*y32 - u3 * z12 * z2 - u1*z2 * z23 - u2*z2*z31)/(2*area)
            Czeta3  = (u2*y13 *  y3 + u3 * y21 *  y3 + u1 * y3*y32 - u3 * z12 * z3 - u1*z23 * z3 - u2*z3*z31)/(2*area)
            Czeta12 = 2*y1*y2 + 2*z1*z2
            Czeta13 = 2*y1*y3 + 2*z1*z3
            Czeta23 = 2*y2*y3 + 2*z2*z3
            Czeta1s =   y1**2 +   z1**2
            Czeta2s =   y2**2 +   z2**2
            Czeta3s =   y3**2 +   z3**2
            J += ((Czeta1+Czeta2+Czeta3)/3. \
                + (Czeta12+Czeta13+Czeta23)/12. \
                + (Czeta1s+Czeta2s+Czeta3s)/6.)*area

        return float(J)

