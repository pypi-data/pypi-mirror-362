#!/usr/bin/env python
"""
killMS, a package for calibration in radio interferometry.
Copyright (C) 2013-2017  Cyril Tasse, l'Observatoire de Paris,
SKA South Africa, Rhodes University

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import scipy.linalg
import numpy as np
from killMS.Other import ModColor

def invertChol(A):
    L=np.linalg.cholesky(A)
    Linv=np.linalg.inv(L)
    Ainv=np.dot(Linv.T,Linv)
    return Ainv

def invertLU(A):
    lu,piv=scipy.linalg.lu_factor(A)
    return scipy.linalg.lu_solve((lu,piv),np.eye(A.shape[0],A.shape[0]))

def sqrtSVD(A,Rank=None):
    #u,s,v=np.linalg.svd(A+np.random.randn(*A.shape)*(1e-6*A.max()))
    A=(A+A.T)/2.
    thr=1e-8
    u,s,v=np.linalg.svd(A+np.random.randn(*A.shape)*(thr*A.max()))
    s[s<0.]=0.
    ssq=np.diag(np.sqrt(s))
    if Rank is not None:
        ssq[Rank:]=0
    Asq=np.dot(np.dot(u,ssq),v)
    return Asq

def BatchInverse(A,H=False):
    shapeOut=A.shape
    A=A.reshape((A.size//4,2,2))
    #A.shape=N,2,2
    N,dum,dum=A.shape
    Ainv=np.zeros_like(A)
    if not(H):
        a0=A[:,0,0]
        d0=A[:,1,1]
        b0=A[:,0,1]
        c0=A[:,1,0]
    else:
        a0=A[:,0,0].conj()
        d0=A[:,1,1].conj()
        b0=A[:,1,0].conj()
        c0=A[:,0,1].conj()
        
    det=1./(a0*d0-b0*c0)
    Ainv[:,0,0]=d0*det
    Ainv[:,0,1]=-b0*det
    Ainv[:,1,0]=-c0*det
    Ainv[:,1,1]=a0*det
    Ainv=Ainv.reshape(shapeOut)
    return Ainv
    
def BatchH(A):
    shapeOut=A.shape
    A=A.reshape((A.size//4,2,2))

    N,dum,dum=A.shape
    AH=np.zeros_like(A)

    a0=A[:,0,0].conj()
    d0=A[:,1,1].conj()
    b0=A[:,1,0].conj()
    c0=A[:,0,1].conj()
    AH[:,0,0]=a0
    AH[:,1,1]=d0
    AH[:,0,1]=b0
    AH[:,1,0]=c0

    AH=AH.reshape(shapeOut)
    return AH
    
def BatchDot(A,B):
    shapeOut=A.shape
    A=A.reshape((A.size//4,2,2))
    B=B.reshape((B.size//4,2,2))

    C=np.zeros_like(A)
    # if A.size>=B.size:
    #     C=np.zeros_like(A)
    #     shapeOut=A.shape
    # else:
    #     C=np.zeros_like(B)
    #     shapeOut=B.shape

    # print("A:",A.shape)
    # print("B:",B.shape)
    # print("C:",C.shape)
    
    a0=A[:,0,0]
    b0=A[:,1,0]
    c0=A[:,0,1]
    d0=A[:,1,1]

    a1=B[:,0,0]
    b1=B[:,1,0]
    c1=B[:,0,1]
    d1=B[:,1,1]

    C00=C[:,0,0]
    C01=C[:,0,1]
    C10=C[:,1,0]
    C11=C[:,1,1]

    C00[:]=a0*a1+c0*b1
    C01[:]=a0*c1+c0*d1
    C10[:]=b0*a1+d0*b1
    C11[:]=b0*c1+d0*d1


    C=C.reshape(shapeOut)

    return C
    
def BatchDot2(A,B):
    #A=A.reshape((A.size/4,2,2))
    #B=B.reshape((B.size/4,2,2))

    shapeOut=A.shape

    NDir_a,nf,na,_=shapeOut
    A=A.reshape((NDir_a,nf,na,2,2))
    NDir_b,nf,na,_=B.shape
    B=B.reshape((NDir_b,nf,na,2,2))
    C=np.zeros_like(A)

    # if B.shape[0]==1:
    #     NDir=A.shape[0]
    #     #print("a")
    #     #B=B*np.ones((NDir,1,1,1,1))
    #     #print("b")
    #     #return BatchDot(A,B)
    #     #B=B.reshape((1,B.size/(4*NDir),2,2))
    #     C=np.zeros_like(A)
    # else:
    #     C=np.zeros_like(B)
    #     shapeOut=B.shape

    # print("A:",A.shape)
    # print("B:",B.shape)
    # print("C:",C.shape)
    
    a0=A[:,:,:,0,0]
    b0=A[:,:,:,1,0]
    c0=A[:,:,:,0,1]
    d0=A[:,:,:,1,1]

    a1=B[:,:,:,0,0]
    b1=B[:,:,:,1,0]
    c1=B[:,:,:,0,1]
    d1=B[:,:,:,1,1]

    C00=C[:,:,:,0,0]
    C01=C[:,:,:,0,1]
    C10=C[:,:,:,1,0]
    C11=C[:,:,:,1,1]

    C00[:,:,:]=a0*a1+c0*b1
    C01[:,:,:]=a0*c1+c0*d1
    C10[:,:,:]=b0*a1+d0*b1
    C11[:,:,:]=b0*c1+d0*d1

    C=C.reshape(shapeOut)

    return C

def PlotMatSVD(A,s,Ainv):
    import pylab

    pylab.clf()
    pylab.subplot(2,3,1)
    pylab.imshow(A.real,interpolation="nearest")
    pylab.colorbar()

    pylab.subplot(2,3,2)
    pylab.imshow(A.imag,interpolation="nearest")
    pylab.colorbar()

    ls=np.log10(np.abs(s))
    pylab.subplot(2,3,3)
    pylab.plot(np.abs(s))
    pylab.title("[%f, %f]"%(ls.min(),ls.max()))

    I=np.dot(Ainv,A)

    pylab.subplot(2,3,4)
    pylab.imshow(I.real,interpolation="nearest",vmin=-0.01,vmax=0.01)
    pylab.colorbar()

    pylab.subplot(2,3,5)
    pylab.imshow(I.imag,interpolation="nearest")
    pylab.colorbar()

    pylab.draw()
    pylab.show(False)
    pylab.pause(0.1)        
    


def invSVD(A):


    try:
        u,s,v=np.linalg.svd(np.complex128(A))#+np.random.randn(*A.shape)*(1e-6*A.max()))
    except:
        Name="errSVDArray_%i"%int(np.random.rand(1)[0]*10000)
        print(ModColor.Str("Problem inverting Matrix, saving as %s"%Name))
        print(ModColor.Str("  will make it svd-able"))
        np.save(Name,A)
        # weird - I found a matrix I cannot do svd on... - that works
        Cut=1e-20
        #Ar=np.complex64(Ar)
        u,s,v=np.linalg.svd(np.complex128(A)+np.random.randn(*A.shape)*(1e-10*np.abs(A).max()))


    #s[s<0.]=1.e-6
    s0=s.copy()
    Th=1e-10
    s[s<Th*s.max()]=Th*s.max()
    ssq=(1./s)
    #Asq=np.conj(np.dot(np.dot(v.T,ssq),u.T))
    v0=v.T*ssq.reshape(1,ssq.size)
    Asq=np.conj(np.dot(v0,u.T))
    #PlotMatSVD(A,s0.flatten(),Asq)
    return Asq

def SVDw(A):
    #A=(A+A.T)/2.
    u,s,v=np.linalg.svd(A)
    s[s<0.]=0.
    ssq=np.diag(np.sqrt(s))
    Asq=np.dot(np.dot(u,ssq),u.T)
    return Asq

def EigClean(A):
    
    Lq,Uq=np.linalg.eig(A.copy())
    ind =np.where(Lq<0.)[0]
    if ind.shape[0]>0:
        Lq[ind]=1e-3
    #UqInv=np.linalg.inv(Uq)
    Anew=np.real(np.dot(np.dot(Uq,np.diag(Lq)),Uq.T))
    Lq,Uq=np.linalg.eig(Anew)
#    print(Lq)
    return Anew


def Dot_ListBlockMat_Mat(ListBlocks,Mat):
    n=ListBlocks[0].shape[0]
    m=Mat.shape[1]
    nblock=len(ListBlocks)
    WorkMat=Mat.reshape(nblock,n,m)
    OutMat=np.zeros_like(WorkMat)
    
    for iblock in range(nblock):
        ThisBlock=ListBlocks[iblock]
        OutMat[iblock]=np.dot(ThisBlock.astype(np.float64),WorkMat[iblock].astype(np.float64))

    OutMat=OutMat.reshape(nblock*n,m)
    return OutMat
        
def Dot_ListBlockMat_Mat_Iregular(ListBlocks,Mat):
    m=Mat.shape[1]
    nblock=len(ListBlocks)
    OutMat=np.zeros_like(Mat)
    
    i0=0
    for iblock in range(nblock):
        ThisBlock=ListBlocks[iblock]
        xb,yb=ThisBlock.shape
        i1=i0+xb
        WorkMat=Mat[i0:i1,:]
        OutMat[i0:i1,:]=np.dot(ThisBlock.astype(np.float64),WorkMat.astype(np.float64))
        i0+=xb

    return OutMat

def test_Dot_ListBlockMat_Mat():
    nblocks=50
    n=100
    m=200
    B=np.random.randn(nblocks*n,m)
    ListBlocks=[]
    BlocksMat=np.zeros((nblocks*n,nblocks*n),float)
    for iblock in range(nblocks):
        ThisBlock=np.random.randn(n,n)
        ListBlocks.append(ThisBlock)
        istart=iblock*n
        BlocksMat[istart:istart+n,istart:istart+n]=ThisBlock
        
    import ClassTimeIt
    T=ClassTimeIt.ClassTimeIt()


    print("Dimentions A[%s], B[%s]"%(BlocksMat.shape,B.shape))
    R0=Dot_ListBlockMat_Mat(ListBlocks,B)
    T.timeit("ListProd")
    R1=np.dot(BlocksMat,B)
    T.timeit("NpProd")
    R2=Dot_ListBlockMat_Mat_Iregular(ListBlocks,B)
    T.timeit("ListProdIrregular")

    print(np.allclose(R0,R1))
    print(np.allclose(R2,R1))

    
def test_Dot_ListBlockMat_Mat_Big():
    nblocks=10*50
    n=100
    m=200
    B=np.random.randn(nblocks*n,m)
    ListBlocks=[]

    for iblock in range(nblocks):
        ThisBlock=np.random.randn(n,n)
        ListBlocks.append(ThisBlock)

        
    import ClassTimeIt
    T=ClassTimeIt.ClassTimeIt()


    print("Dimentions A[%ix%s -> %s], B[%s]"%(nblocks,ThisBlock.shape,(nblocks*n,nblocks*n),B.shape))
    R0=Dot_ListBlockMat_Mat(ListBlocks,B)
    T.timeit("ListProd")

