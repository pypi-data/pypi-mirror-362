// killMS, a package for calibration in radio interferometry.
// Copyright (C) 2013-2017  Cyril Tasse, l'Observatoire de Paris,
// SKA South Africa, Rhodes University
// 
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

/* A file to test imorting C modules for handling arrays to Python */
#include <Python.h>
#include <math.h>
#include <time.h>
#include "arrayobject.h"
#include "Gridder.h"
#include "complex.h"
#include <omp.h>

clock_t start;

void initTime(){start=clock();}

void timeit(char* Name){
  clock_t diff;
  diff = clock() - start;
  start=clock();
  float msec = diff * 1000 / CLOCKS_PER_SEC;
  printf("%s: %f\n",Name,msec);
}

double AppendTimeit(){
  clock_t diff;
  diff = clock() - start;
  double msec = diff * 1000000 / CLOCKS_PER_SEC;
  return msec;
}



/* #### Globals #################################### */

/* ==== Set up the methods table ====================== */
static PyMethodDef _pyGridder[] = {
	{"pyGridderWPol", pyGridderWPol, METH_VARARGS},
	{"pyGridderPoints", pyGridderPoints, METH_VARARGS},
	{"pyDeGridderWPol", pyDeGridderWPol, METH_VARARGS},
	{"pyTestMatrix", pyTestMatrix, METH_VARARGS},
	{"pyAddArray", pyAddArray, METH_VARARGS},
	{"pyWhereMax", pyWhereMax, METH_VARARGS},
	{NULL, NULL}     /* Sentinel - marks the end of this structure */
};

static struct PyModuleDef cMod_pyGridder =
{
    PyModuleDef_HEAD_INIT,
    "_pyGridder",    /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    _pyGridder,
    NULL,
    NULL,
    NULL,
    NULL
};


/* ==== Initialize the C_test functions ====================== */
// Module name must be _C_arraytest in compile and linked 
PyMODINIT_FUNC PyInit__pyGridder(void)
{
    PyObject * m = PyModule_Create(&cMod_pyGridder);
    import_array();
    return m;
}

static PyObject *pyWhereMax(PyObject *self, PyObject *args)
{
  PyArrayObject *A, *Blocks,*Ans;
  PyObject *ObjAns;
  int doabs;

  if (!PyArg_ParseTuple(args, "O!O!Oi", 
			&PyArray_Type,  &A,
			&PyArray_Type,  &Blocks,
			&ObjAns,
			&doabs
			))  return NULL;
  
  //  A = (PyArrayObject *) PyArray_ContiguousFromObject(ObjA, PyArray_FLOAT32, 0, 4);
  
  Ans = (PyArrayObject *) PyArray_ContiguousFromObject(ObjAns, PyArray_FLOAT32, 0, 4);
  
  int nx,ny,NX,NY,np;
  
  NX=A->dimensions[0];
  NY=A->dimensions[1];
  //printf("dims %i %i\n",NX,NY);
  



  long iblock;
  int* pBlocks=p_int32(Blocks);
  int nblocks=Blocks->dimensions[0];
  float *MaxBlock;
  int *xMaxBlock;
  int *yMaxBlock;
  MaxBlock=malloc((nblocks-1)*sizeof(float));
  xMaxBlock=malloc((nblocks-1)*sizeof(int));
  yMaxBlock=malloc((nblocks-1)*sizeof(int));

  {
#pragma omp parallel for
    for (iblock = 0; iblock < nblocks-1; iblock++){
      int i0=pBlocks[iblock];
      int i1=pBlocks[iblock+1];
      if(i1>=NX){i1=NX;};
      
      //printf("- block %i->%i\n",i0,i1);
      
      float* a = p_float32(A);
      int i_a,j_a;
      float ThisMax=0.;
      int ThisxMax=0;
      int ThisyMax=0;
      float ThisVal;
      for (i_a = i0; i_a < i1; i_a++)
      	{
      	  for (j_a = 0; j_a < NY; j_a++)
      	    {
      	      int ii=i_a*NY+j_a;
      	      /* ThisMax  = ((a[ii] > ThisMax) ? a[ii] : ThisMax); */
      	      /* ThisxMax = ((a[ii] > ThisMax) ? i_a : ThisxMax); */
      	      /* ThisyMax = ((a[ii] > ThisMax) ? j_a : ThisyMax); */
	      ThisVal=a[ii];
	      if(doabs==1){
		ThisVal=fabs(ThisVal);
	      }
	      //printf("%f, %f \n",a[ii],ThisVal);
	      if (ThisVal > ThisMax){
		ThisMax=ThisVal;
		ThisxMax=i_a;
		ThisyMax=j_a;
	      }
	      

      	      /* printf("%i %i %i\n",i_a,j_a,ii); */
	      /* printf("%i %i %f\n",ThisxMax,ThisyMax,ThisMax); */
      	    }
      	}

      MaxBlock[iblock]=ThisMax;
      xMaxBlock[iblock]=ThisxMax;
      yMaxBlock[iblock]=ThisyMax;
      //printf("maxc loop: %i %i %f\n",xMaxBlock[iblock],yMaxBlock[iblock],MaxBlock[iblock]);
      //printf("maxc loop2: %i %i %f\n",ThisxMax,ThisyMax,ThisMax);

    }
  }
  
  float Max=0;
  int xMax=0;
  int yMax=0;
  float* ans = p_float32(Ans);
  for (iblock = 0; iblock < nblocks-1; iblock++){
    if(MaxBlock[iblock]>Max){
      Max=MaxBlock[iblock];
      xMax=xMaxBlock[iblock];
      yMax=yMaxBlock[iblock];
    }
  }

  //printf("maxc: %i %i %f\n",xMax,yMax,Max);
  ans[0]=(float)xMax;
  ans[1]=(float)yMax;
  ans[2]=(float)Max;

  return PyArray_Return(Ans);

}


static PyObject *pyAddArray(PyObject *self, PyObject *args)
{
  PyObject *ObjA;
  PyArrayObject *A, *B, *Aedge, *Bedge, *Blocks;
  float factor;

  if (!PyArg_ParseTuple(args, "OO!O!O!fO!", 
			&ObjA,
			&PyArray_Type,  &Aedge,
			&PyArray_Type,  &B,
			&PyArray_Type,  &Bedge,
			&factor,
			&PyArray_Type,  &Blocks
			))  return NULL;
  
  A = (PyArrayObject *) PyArray_ContiguousFromObject(ObjA, PyArray_FLOAT32, 0, 4);
  
  
  int nx,ny,NX,NY,np;
  
  NX=A->dimensions[0];
  NY=A->dimensions[1];
  //printf("dims %i %i\n",NX,NY);
  
  int * aedge = p_int32(Aedge);
  int a_x0=aedge[0];
  int a_x1=aedge[1];
  int a_y0=aedge[2];
  int a_y1=aedge[3];

  int * bedge = p_int32(Bedge);
  int b_x0=bedge[0];
  int b_x1=bedge[1];
  int b_y0=bedge[2];
  int b_y1=bedge[3];



  long iblock;
  int* pBlocks=p_int32(Blocks);
  int nblocks=Blocks->dimensions[0];

/* for (i = 0; i < nx; i++) */
/*   { */
/* for (j = 0; j < ny; j++) */
/*   { */
/* a[i*ny+j] += b[i*ny+j];// * 2;//(factor); */
/* } */
/* } */

  {
#pragma omp parallel for
    for (iblock = 0; iblock < nblocks-1; iblock++){
      int i0=pBlocks[iblock];
      int i1=pBlocks[iblock+1];
      if(i1>=a_x1){i1=a_x1;};
      
      //printf("- block %i->%i\n",i0,i1);
      
      float* a = p_float32(A);
      float* b = p_float32(B);
      int i_a,j_a;

      for (i_a = i0; i_a < i1; i_a++)
	{
	  int di=i_a-a_x0;
	  int i_b=b_x0+di;
	  for (j_a = a_y0; j_a < a_y1; j_a++)
	    {
	      int dj=j_a-a_y0;
	      int j_b=b_y0+dj;
	      //printf("a[%i,%i] = b[%i,%i]\n",i_a,j_a,i_b,j_b); 
	      a[i_a*NY+j_a] += b[i_b*NY+j_b]*(factor);
	      //printf("- %f\n",a[i*ny+j]);
	      
	    }
	}
      
    }
  }


/* float* a = p_float32(A); */

/* for (i = 0; i < nx; i++) */
/*   { */
/* for (j = 0; j < ny; j++) */
/*   { */
/* printf("%f\n",a[i*ny+j]); */
/* } */
/* } */
  

  return PyArray_Return(A);//,PyArray_Return(np_grid);

}



static PyObject *pyGridderPoints(PyObject *self, PyObject *args)
{
  PyArrayObject *ObjGridIn,*ObjWIn;
  PyArrayObject *np_grid, *np_w, *w,*np_u,*np_v, *np_freqs,*np_flags, *np_uvcell;
  double R = 0.0;
  int Mode = 0;
  if (!PyArg_ParseTuple(args, "OO!O!O!OdiO!O!", 
			&ObjGridIn,
			&PyArray_Type,  &np_flags, 
			&PyArray_Type,  &np_u, 
			&PyArray_Type,  &np_v, 
			&ObjWIn,
			//&PyArray_Type,  &w,
			&R,
			&Mode,
			&PyArray_Type,  &np_freqs,
			&PyArray_Type,  &np_uvcell
			))  return NULL;
  np_grid = (PyArrayObject *) PyArray_ContiguousFromObject(ObjGridIn, PyArray_FLOAT64, 0, 4);
  np_w = (PyArrayObject *) PyArray_ContiguousFromObject(ObjWIn, PyArray_FLOAT64, 0, 4);

  int* flags=p_int32(np_flags);

  int nx,ny;
  long np;
  nx=np_grid->dimensions[0];
  ny=np_grid->dimensions[1];
  double* grid = p_float64(np_grid);
  double* wp= p_float64(np_w);

  
  double *u=p_float64(np_u);
  double *v=p_float64(np_v);
  float *freqs=p_float32(np_freqs);;
  int nch=np_freqs->dimensions[0];
  //printf("nch=%i\n",nch);
  //printf("nx=%i\n",nx);


  double *uvcell = p_float64(np_uvcell);
  double ucell=uvcell[0];
  double vcell=uvcell[1];


  int xp;
  int yp;
  np=np_u->dimensions[0];
  double sumw=0;
  
  //printf("grid dims (%i,%i)\n",nx,ny);
  //printf("nvis dims (%i)\n",np);

  long i=0;
  long irow=0;
  long ich=0;
  int xc,yc;
  xc=nx/2;
  yc=ny/2;
  size_t ii,jj;
  float ThisW=0.;
  size_t iii;
  float C=299792458.;
  

  for (irow=0; irow<np; irow++) {
    for (ich=0; ich<nch; ich++) {
      i=irow*nch+ich;
      if(flags[i]==1){continue;}

      //xp=round((u[irow]*freqs[ich]/C)/ucell);
      //yp=round((v[irow]*freqs[ich]/C)/vcell);

      xp=floor((u[irow]*freqs[ich]/C)/ucell+0.5);
      yp=floor((v[irow]*freqs[ich]/C)/vcell+0.5);

      /* printf("[%i,%i]: u=%f f=%f ucell=%f xp=%i\n",(int)irow,(int)ich,(float)u[irow],(float)freqs[ich],(float)ucell,(int)xp); */
      /* printf("[%i,%i]: v=%f f=%f ucell=%f yp=%i\n",(int)irow,(int)ich,(float)v[irow],(float)freqs[ich],(float)vcell,(int)yp); */
      /* printf("\n"); */
      ii=xp+xc;
      jj=yp+yc;
      //printf("%i: (x,y)=(%i,%i)\n",(int)i,ii,jj);
      if((ii<0)|(ii>nx-1)){continue;}
      if((jj<0)|(jj>ny-1)){continue;}
      

      iii=ii+nx*jj;
      grid[iii]+=wp[i];
      //grid[iii]=1;//wp[i];
      //printf("%i: (x,y)=(%i,%i): %f %f\n",(int)i,ii,jj,wp[i],grid[ii+nx*jj]);

      ii=-xp+xc;
      jj=-yp+yc;
      iii=ii+nx*jj;
      grid[iii]+=wp[i];

      //printf("%i: (x,y)=(%i,%i): %f %f\n",(int)i,ii,jj,wp[i],grid[ii+nx*jj]);
      //printf("\n");
      ThisW=wp[i];
      sumw+=ThisW*2.;//(2.*(wp[i]));
    }
  }


  /* double Wk; */
  /* double sumWk=0; */
  /* for (irow=0; irow<np; irow++) { */
  /*   for (ich=0; ich<nch; ich++) { */
  /*     i=irow*nch+ich; */
  /*     if(flags[i]==1){continue;} */
  /*     xp=round((u[irow]*freqs[ich]/C)/ucell); */
  /*     yp=round((v[irow]*freqs[ich]/C)/vcell); */
  /*     ii=xp+xc; */
  /*     jj=yp+yc; */
  /*     if((ii<0)|(ii>nx-1)){continue;} */
  /*     if((jj<0)|(jj>ny-1)){continue;} */


  /*     iii=ii+nx*jj; */
  /*     Wk=grid[iii]; */
  /*     sumWk+=Wk*Wk; */
  /*     ii=-xp+xc; */
  /*     jj=-yp+yc; */
  /*     iii=ii+nx*jj; */
  /*     Wk=grid[iii]; */
  /*     sumWk+=Wk*Wk; */
  /*   } */
  /* } */

  double Wk;
  double sumWk=0;
  for (ii=0; ii<nx; ii++) {
    for (jj=0; jj<nx; jj++) {
      iii=ii+nx*jj;
      Wk=grid[iii];
      sumWk+=Wk*Wk;
    }
  }


  double fact=  (sumw/sumWk)*pow(5.*pow(10.,-R),2.);
  //printf("fact=(%f)\n",fact);
  //printf("sumw,sumWk=%f,%f\n",sumw,sumWk);


  if(Mode==0){
  //printf("Mode=(%i)\n",Mode);
    for (irow=0; irow<np; irow++) {
      for (ich=0; ich<nch; ich++) {
  	i=irow*nch+ich;
  	if(flags[i]==1){continue;}
  	xp=round((u[irow]*freqs[ich]/C)/ucell);
  	yp=round((v[irow]*freqs[ich]/C)/vcell);
  	ii=xp+xc;
  	jj=yp+yc;
  	if((ii<0)|(ii>nx-1)){continue;}
  	if((jj<0)|(jj>ny-1)){continue;}
  	iii=ii+nx*jj;
  	if(wp[i]>0.){
  	  Wk=grid[iii];
  	  wp[i]/=(1.+fact*Wk);
  	}
  	//wp[i]/=(Wk);
      }
    }
  }else{
    //printf("Mode=(%i)\n",Mode);
    for (irow=0; irow<np; irow++) {
      for (ich=0; ich<nch; ich++) {
	i=irow*nch+ich;
	if(flags[i]==1){continue;}
	xp=round((u[irow]*freqs[ich]/C)/ucell);
	yp=round((v[irow]*freqs[ich]/C)/vcell);
	ii=xp+xc;
	jj=yp+yc;
	if((ii<0)|(ii>nx-1)){continue;}
	if((jj<0)|(jj>ny-1)){continue;}
	
	
	iii=ii+nx*jj;
	Wk=grid[iii];
  	if(Wk>0.){
  	  wp[i]/=(Wk);
  	  //wp[i]=(Wk);
  	  //printf("@[%i, %i] %f,%f\n",(int)ii,(int)jj,wp[i],Wk);
  	}

      }
    }
  };


  //PyObject* PyList_New(Py_ssize_t len)
  

  return PyArray_Return(np_w);
  //return PyArray_Return(np_grid);

}









static PyObject *pyGridderWPol(PyObject *self, PyObject *args)
{
  PyObject *ObjGridIn;
  PyArrayObject *np_grid, *vis, *uvw, *cfs, *flags, *weights, *sumwt, *increment, *freqs,*WInfos;

  PyObject *Lcfs;
  PyObject *LJones,*Lmaps;
  PyObject *LcfsConj;
  int dopsf;

  if (!PyArg_ParseTuple(args, "OO!O!O!O!O!iO!O!O!O!O!O!O!", 
			&ObjGridIn,
			&PyArray_Type,  &vis, 
			&PyArray_Type,  &uvw, 
			&PyArray_Type,  &flags, 
			&PyArray_Type,  &weights,
			&PyArray_Type,  &sumwt, 
			&dopsf, 
			&PyList_Type, &Lcfs,
			&PyList_Type, &LcfsConj,
			&PyArray_Type,  &WInfos,
			&PyArray_Type,  &increment,
			&PyArray_Type,  &freqs,
			&PyList_Type, &Lmaps,
			&PyList_Type, &LJones
			))  return NULL;
  int nx,ny,nz,nzz;
  //initTime();
  np_grid = (PyArrayObject *) PyArray_ContiguousFromObject(ObjGridIn, PyArray_COMPLEX64, 0, 4);
  //timeit("declare np_grid");
  /* nx=np_grid->dimensions[0]; */
  /* ny=np_grid->dimensions[1]; */
  /* nz=np_grid->dimensions[2]; */
  /* nzz=np_grid->dimensions[3]; */
  /* printf("grid dims (%i,%i,%i,%i)\n",nx,ny,nz,nzz); */
  /* nx=vis->dimensions[0]; */
  /* ny=vis->dimensions[1]; */
  /* nz=vis->dimensions[2]; */
  /* printf("vis  dims (%i,%i,%i)\n",nx,ny,nz); */
  /* /\* nx=uvw->dimensions[0]; *\/ */
  /* /\* ny=uvw->dimensions[1]; *\/ */
  /* /\* nz=uvw->dimensions[2]; *\/ */
  /* /\* printf("uvw  dims (%i,%i)\n",nx,ny); *\/ */

  
  /* //bool * visPtr  = p_bool(vis); */
  /* bool * flagPtr  = p_bool(flags); */
  /* /\* printf("VV= (%f,%f)\n",creal(*visPtr),cimag(*visPtr)); *\/ */
  /* /\* printf("VV= (%f,%f)\n",crealf(*visPtr),cimagf(*visPtr)); *\/ */

  /* int x,y,z; */
  /* for(x=0; x<nx; x++){ */
  /* for(y=0; y<ny; y++){ */
  /* for(z=0; z<nz; z++){ */
  /*   /\* printf("\n"); *\/ */
  /*   /\* printf("flag [%i,%i,%i]= (%i)\n",x,y,z,(int)*flagPtr); *\/ */
  /*   /\* flagPtr++; *\/ */

  /*   int doff = (x * ny + y) * nz; */
  /*   printf("flag [%i,%i,%i]= (%i)\n",x,y,z,(int)flagPtr[doff+z]); */
  /*   int truth; */
  /*   truth=((int)flagPtr[doff+z]==1); */
  /*   printf("equal1? %i",truth); */
  /* }}} */

  gridderWPol(np_grid, vis, uvw, flags, weights, sumwt, dopsf, Lcfs, LcfsConj, WInfos, increment, freqs, Lmaps, LJones);
  //timeit("grid");
  
  return PyArray_Return(np_grid);

}

double PI=3.14159265359;

//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////


void MatInv(float complex *A, float complex* B, int H ){
  float complex a,b,c,d,ff;

  if(H==0){
      a=A[0];
      b=A[1];
      c=A[2];
      d=A[3];}
  else{
    a=conj(A[0]);
    b=conj(A[2]);
    c=conj(A[1]);
    d=conj(A[3]);
  }  
  ff=1./((a*d-c*b));
  B[0]=ff*d;
  B[1]=-ff*b;
  B[2]=-ff*c;
  B[3]=ff*a;
}

void MatH(float complex *A, float complex* B){
  float complex a,b,c,d;

  a=conj(A[0]);
  b=conj(A[2]);
  c=conj(A[1]);
  d=conj(A[3]);
  B[0]=a;
  B[1]=b;
  B[2]=c;
  B[3]=d;
}

void MatDot(float complex *A, float complex* B, float complex* Out){
  float complex a0,b0,c0,d0;
  float complex a1,b1,c1,d1;

  a0=A[0];
  b0=A[1];
  c0=A[2];
  d0=A[3];
  
  a1=B[0];
  b1=B[1];
  c1=B[2];
  d1=B[3];
  
  Out[0]=a0*a1+b0*c1;
  Out[1]=a0*b1+b0*d1;
  Out[2]=c0*a1+d0*c1;
  Out[3]=c0*b1+d0*d1;

}

static PyObject *pyTestMatrix(PyObject *self, PyObject *args)
{
  PyArrayObject *Anp;

  if (!PyArg_ParseTuple(args, "O!",
			&PyArray_Type,  &Anp
			)
      )  return NULL;

  float complex* A  = p_complex64(Anp);
  float complex B[4];
  MatInv(A,B,1);
  int i;
  printf("inverse of input matrix:\n");
  for (i=0; i<4; i++){
    printf("%i: (%f,%f)\n",i,(float)creal(B[i]),(float)cimag(B[i]));
  };
   
  printf("\ndot product A.A^-1:\n");
  float complex Out[4];
  MatDot(A,B,Out);
  for (i=0; i<4; i++){
    printf("%i: (%f,%f)\n",i,(float)creal(Out[i]),(float)cimag(Out[i]));
  };

  printf("\n A^H:\n");
  MatH(A,B);
  for (i=0; i<4; i++){
    printf("%i: (%f,%f)\n",i,(float)creal(B[i]),(float)cimag(B[i]));
  };
  


  return Py_None;

}

//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////

void GiveJones(float complex *ptrJonesMatrices, int *JonesDims, float *ptrCoefs, int i_t, int i_ant0, int i_dir, int Mode, float complex *Jout){
  int nd_Jones,na_Jones,nch_Jones;
  nd_Jones=JonesDims[1];
  na_Jones=JonesDims[2];
  nch_Jones=JonesDims[3];
  
  int ipol,idir;
  if(Mode==0){
    int offJ0=i_t*nd_Jones*na_Jones*nch_Jones*4
      +i_dir*na_Jones*nch_Jones*4
      +i_ant0*nch_Jones*4;
    for(ipol=0; ipol<4; ipol++){
      Jout[ipol]=*(ptrJonesMatrices+offJ0+ipol);
    }
  }

  if(Mode==1){
    for(idir=0; idir<nd_Jones; idir++){
      int offJ0=i_t*nd_Jones*na_Jones*nch_Jones*4
	+idir*na_Jones*nch_Jones*4
	+i_ant0*nch_Jones*4;
      for(ipol=0; ipol<4; ipol++){
	Jout[ipol]+=ptrCoefs[idir]*(*(ptrJonesMatrices+offJ0+ipol));
	
	//printf("%i, %f, %f, %f\n",ipol,ptrCoefs[idir],creal(Jout[ipol]),cimag(Jout[ipol]));
      }
      
    }
  }
}


void gridderWPol(PyArrayObject *grid,
	      PyArrayObject *vis,
	      PyArrayObject *uvw,
	      PyArrayObject *flags,
	      PyArrayObject *weights,
	      PyArrayObject *sumwt,
	      int dopsf,
	      PyObject *Lcfs,
	      PyObject *LcfsConj,
	      PyArrayObject *Winfos,
	      PyArrayObject *increment,
		 PyArrayObject *freqs,
		 PyObject *Lmaps, PyObject *LJones)
  {
    // Get size of convolution functions.
    int nrows     = uvw->dimensions[0];
    PyArrayObject *cfs;
    PyArrayObject *NpPolMap;
    NpPolMap = (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(Lmaps, 0), PyArray_INT32, 0, 4);

    PyArrayObject *NpFacetInfos;
    NpFacetInfos = (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(Lmaps, 1), PyArray_FLOAT64, 0, 4);


    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    int LengthJonesList=PyList_Size(LJones);
    int DoApplyJones=0;
    PyArrayObject *npJonesMatrices, *npTimeMappingJonesMatrices, *npA0, *npA1, *npJonesIDIR, *npCoefsInterp,*npModeInterpolation;
    float complex* ptrJonesMatrices;
    int *ptrTimeMappingJonesMatrices,*ptrA0,*ptrA1,*ptrJonesIDIR;
    float *ptrCoefsInterp;
    int i_dir;
    int nd_Jones,na_Jones,nch_Jones,nt_Jones;

    //    printf("len %i",LengthJonesList);
    int JonesDims[4];
    int ModeInterpolation=1;
    int *ptrModeInterpolation;

    if(LengthJonesList>0){
      DoApplyJones=1;

      npTimeMappingJonesMatrices  = (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 0), PyArray_INT32, 0, 4);
      ptrTimeMappingJonesMatrices = p_int32(npTimeMappingJonesMatrices);

      npA0 = (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 1), PyArray_INT32, 0, 4);
      ptrA0 = p_int32(npA0);
      int ifor;
      


      npA1= (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 2), PyArray_INT32, 0, 4);
      ptrA1=p_int32(npA1);
 
      
      // (nt,nd,na,1,2,2)
      npJonesMatrices = (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 3), PyArray_COMPLEX64, 0, 6);
      ptrJonesMatrices=p_complex64(npJonesMatrices);
      nt_Jones=(int)npJonesMatrices->dimensions[0];
      nd_Jones=(int)npJonesMatrices->dimensions[1];
      na_Jones=(int)npJonesMatrices->dimensions[2];
      nch_Jones=(int)npJonesMatrices->dimensions[3];
      JonesDims[0]=nt_Jones;
      JonesDims[1]=nd_Jones;
      JonesDims[2]=na_Jones;
      JonesDims[3]=nch_Jones;

      npJonesIDIR= (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 4), PyArray_INT32, 0, 4);
      ptrJonesIDIR=p_int32(npJonesIDIR);
      i_dir=ptrJonesIDIR[0];

      npCoefsInterp= (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 5), PyArray_FLOAT32, 0, 4);
      ptrCoefsInterp=p_float32(npCoefsInterp);

      npModeInterpolation= (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 6), PyArray_INT32, 0, 4);
      ptrModeInterpolation=p_int32(npModeInterpolation);
      ModeInterpolation=ptrModeInterpolation[0];
      
      /* // check */
      /* for(ifor=0;ifor<nrows;ifor++){ */
      /* 	int A0=ptrA0[ifor]; */
      /* 	int A1=ptrA1[ifor]; */
      /* 	int iTime=ptrTimeMappingJonesMatrices[ifor]; */
      /* 	int offJ0=iTime*nd_Jones*na_Jones*nch_Jones*4 */
      /* 	  +i_dir*na_Jones*nch_Jones*4 */
      /* 	  +A0*nch_Jones*4; */
      /* 	float complex* J0; */
      /* 	printf(" %i - (%i, %i) [%i]\n",iTime,A0,A1, i_dir); */

      /* 	J0=ptrJonesMatrices+offJ0; */
      /* 	int ipol; */
      /* 	for (ipol=0; ipol<4; ipol++){ */
      /* 	  printf("     %i: (%f,%f)\n",ipol,(float)creal(J0[ipol]),(float)cimag(J0[ipol])); */
      /* 	}; */
      /* }; */


    };
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    
    double* ptrFacetInfos=p_float64(NpFacetInfos);
    double Cu=ptrFacetInfos[0];
    double Cv=ptrFacetInfos[1];
    double l0=ptrFacetInfos[2];
    double m0=ptrFacetInfos[3];
    double n0=sqrt(1-l0*l0-m0*m0)-1;


    double VarTimeGrid=0;
    int Nop=0;

    int npolsMap=NpPolMap->dimensions[0];
    int* PolMap=I_ptr(NpPolMap);
    
    //    printf("npols=%i %i\n",npolsMap,PolMap[3]);

    // Get size of grid.
    double* ptrWinfo = p_float64(Winfos);
    double WaveRefWave = ptrWinfo[0];
    double wmax = ptrWinfo[1];
    double NwPlanes = ptrWinfo[2];
    int OverS=floor(ptrWinfo[3]);


    //    printf("WaveRef=%f, wmax=%f \n",WaveRefWave,wmax);
    int nGridX    = grid->dimensions[3];
    int nGridY    = grid->dimensions[2];
    int nGridPol  = grid->dimensions[1];
    int nGridChan = grid->dimensions[0];

    // Get visibility data size.
    int nVisPol   = flags->dimensions[2];
    int nVisChan  = flags->dimensions[1];
    //    printf("(nrows, nVisChan, nVisPol)=(%i, %i, %i)\n",nrows,nVisChan,nVisPol);


    // Get oversampling and support size.
    int sampx = OverS;//int (cfs.sampling[0]);
    int sampy = OverS;//int (cfs.sampling[1]);

    double* __restrict__ sumWtPtr = p_float64(sumwt);//->data;
    double complex psfValues[4];
    psfValues[0] = psfValues[1] = psfValues[2] = psfValues[3] = 1;

    //uint inxRowWCorr(0);

    double offset_p[2],uvwScale_p[2];

    offset_p[0]=nGridX/2;//(nGridX-1)/2.;
    offset_p[1]=nGridY/2;
    float fnGridX=nGridX;
    float fnGridY=nGridY;
    double *incr=p_float64(increment);
    double *Pfreqs=p_float64(freqs);
    uvwScale_p[0]=fnGridX*incr[0];
    uvwScale_p[1]=fnGridX*incr[1];
    //printf("uvscale=(%f %f)\n",uvwScale_p[0],uvwScale_p[1]);
    double C=2.99792458e8;
    int inx;
    // Loop over all visibility rows to process.

    for (inx=0; inx<nrows; inx++) {
      int irow = inx;//rows[inx];
      //printf("\n");
      //printf("irow=%i/%i\n",irow,nrows);
      //const double*  __restrict__ uvwPtr   = GetDp(uvw) + irow*3;
      double*  __restrict__ uvwPtr   = p_float64(uvw) + irow*3;
      double*   imgWtPtr = p_float64(weights) +
	                                  irow  * nVisChan;

      //printf("u=%f",*uvwPtr);
      int visChan;
      for (visChan=0; visChan<nVisChan; ++visChan) {
        int gridChan = 0;//chanMap_p[visChan];
        int CFChan = 0;//ChanCFMap[visChan];
	double recipWvl = Pfreqs[visChan] / C;
	double ThisWaveLength=C/Pfreqs[visChan];
	//printf("visChan=%i \n",visChan);
	

	//W-projection
	double wcoord=uvwPtr[2];
	
	int iwplane = floor((NwPlanes-1)*abs(wcoord)*(WaveRefWave/ThisWaveLength)/wmax);
	int skipW=0;
	if(iwplane>NwPlanes-1){skipW=1;continue;};

	//int iwplane = floor((NwPlanes-1)*abs(wcoord)/wmax);

	//printf("wcoord=%f, iw=%i \n",wcoord,iwplane);

	if(wcoord>0){
	  cfs=(PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(Lcfs, iwplane), PyArray_COMPLEX64, 0, 2);
	} else{
	  cfs=(PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LcfsConj, iwplane), PyArray_COMPLEX64, 0, 2);
	}
	int nConvX = cfs->dimensions[0];
	int nConvY = cfs->dimensions[1];
	int supx = (nConvX/OverS-1)/2;
	int supy = (nConvY/OverS-1)/2;

	int SupportCF=nConvX/OverS;


	/* printf("%i %i %i\n",nConvX,sampx,supx); */
	/* assert(1==0); */



	//printf("wcoord=%f, iw=%i, nConvX=%i ,revert=%i\n",wcoord,iwplane,nConvX,revert);


	//	printf("\n");

	//chanMap_p[visChan]=0;

        if (gridChan >= 0  &&  gridChan < nGridChan) {

	  // Change coordinate and shift visibility to facet center
	  double complex UVNorm=2.*I*PI/ThisWaveLength;
	  double U=uvwPtr[0];
	  double V=uvwPtr[1];
	  double W=uvwPtr[2];
	  double complex corr=cexp(-UVNorm*(U*l0+V*m0+W*n0));
	  U+=W*Cu;
	  V+=W*Cv;

	  //	  printf("uvw = (%f, %f, %f)\n",U,V,W);


          // Determine the grid position from the UV coordinates in wavelengths.
	  double posx,posy;

	  //For Even/Odd take the -1 off
	  posx = uvwScale_p[0] * U * recipWvl + offset_p[0];//#-1;
	  posy = uvwScale_p[1] * V * recipWvl + offset_p[1];//-1;

	  //printf("u=%8.2f, v=%8.2f, uvsc=%f, recip=%f, offset_p=%f, %f %f\n",uvwPtr[0],uvwPtr[1],uvwScale_p[0],recipWvl,offset_p[0],fnGridX,incr[0]);
	  //printf("posx=%6.2f, posy=%6.2f\n",posx,posy);
          int locx = nint (posx);    // location in grid
          int locy = nint (posy);
	  //printf("locx=%i, locy=%i\n",locx,locy);
          double diffx = locx - posx;
          double diffy = locy - posy;
	  //printf("diffx=%f, diffy=%f\n",diffx,diffy);
	  
          int offx = nint (diffx * sampx); // location in
          int offy = nint (diffy * sampy); // oversampling
	  //printf("offx=%i, offy=%i\n",offx,offy);
          offx += (nConvX-1)/2;
          offy += (nConvY-1)/2;
          // Scaling with frequency is not necessary (according to Cyril).
          double freqFact = 1;
          int fsampx = nint (sampx * freqFact);
          int fsampy = nint (sampy * freqFact);
          int fsupx  = nint (supx / freqFact);
          int fsupy  = nint (supy / freqFact);

          // Only use visibility point if the full support is within grid.
	  
	  //printf("offx=%i, offy=%i\n",offx,offy);
	  //assert(1==0);

          if (locx-supx >= 0  &&  locx+supx < nGridX  &&
              locy-supy >= 0  &&  locy+supy < nGridY) {

	    //printf("inside loc!");
            // Get pointer to data and flags for this channel.
            int doff = (irow * nVisChan + visChan) * nVisPol;

            float complex* __restrict__ visPtr_Uncorr  = p_complex64(vis)  + doff;
            float complex visPtr[4];
	    int ThisPol;
	    for(ThisPol =0; ThisPol<4;ThisPol++){
	      visPtr[ThisPol]=visPtr_Uncorr[ThisPol];
	    }	    

	    
	    //	    printf("First value: (%f,%f)\n",creal(*visPtr),cimag(*visPtr));

            bool* __restrict__ flagPtr = p_bool(flags) + doff;

            // Handle a visibility if not flagged.
	    int ipol;

	    
	    //float WeightFromGains;
	    
	    if(DoApplyJones){
	      // Shape: nt,nd,na,1,2,2
	      int i_t=ptrTimeMappingJonesMatrices[irow];
	      int i_ant0=ptrA0[irow];
	      int i_ant1=ptrA1[irow];
	      
	      float complex J0[4]={0},J1[4]={0},J0inv[4]={0},J1H[4]={0},J1Hinv[4]={0},JJ[4]={0};
	      GiveJones(ptrJonesMatrices, JonesDims, ptrCoefsInterp, i_t, i_ant0, i_dir, ModeInterpolation, J0);
	      GiveJones(ptrJonesMatrices, JonesDims, ptrCoefsInterp, i_t, i_ant1, i_dir, ModeInterpolation, J1);
	      
	      MatInv(J0,J0inv,0);
	      MatH(J1,J1H);
	      MatInv(J1H,J1Hinv,0);
	      MatDot(J0inv,visPtr_Uncorr,visPtr);
	      MatDot(visPtr,J1Hinv,visPtr);
	      
	      //MatDot(J0inv,J1Hinv,JJ);
	      //WeightFromGains=1./cabs(JJ[0]);
	      //WeightFromGains*=WeightFromGains;
	      //ThisWeight*=WeightFromGains;
	      
	      /* int ifor; */
	      /* /\* printf("(A0,A1)=%i, %i\n",i_ant0,i_ant1); *\/ */
	      /* /\* for (ifor=0; ifor<4; ifor++){ *\/ */
	      /* /\* 	printf("   %i: (%f,%f)\n",ifor,(float)creal(visPtr[ifor]),(float)cimag(visPtr[ifor])); *\/ */
	      /* /\* }; *\/ */
	    };
	    



            for (ipol=0; ipol<nVisPol; ++ipol) {

	      //printf("flag=%i [on pol %i, doff=%i]\n",(int)flagPtr[ipol],ipol,doff);

	      //printf(".. (row, chan, pol)=(%i, %i, %i): F=%i \n",inx,visChan,ipol,flagPtr[ipol]);
              if (((int)flagPtr[ipol])==0) {
		//printf("take %i on pol %i\n",flagPtr[ipol],ipol);
		//printf("flag: %i",flagPtr[ipol]);
		double complex VisVal;

		double ThisWeight=*imgWtPtr;
		
		if (dopsf==1) {
		  VisVal = 1.;
		}else{
		  
		  VisVal =visPtr[ipol];

		}
		VisVal*=ThisWeight;
		VisVal*=corr;
		//		printf(".. (row, chan, pol)=(%i, %i, %i), VisVal=(%f,%f) \n",inx,visChan,ipol,creal(VisVal),cimag(VisVal));
		//printf(" \n");
		//printf("Vis: %f %f \n",creal(VisVal),cimag(VisVal));
		
                // Map to grid polarization. Only use pol if needed.
                int gridPol = PolMap[ipol];//0;//polMap_p(ipol);
                if (gridPol >= 0  &&  gridPol < nGridPol) {

  		  //cout<<"ipol: "<<ipol<<endl;
                  // Get the offset in the grid data array.
                  int goff = (gridChan*nGridPol + gridPol) * nGridX * nGridY;
                  // Loop over the scaled support.
		  int sy;

		  //initTime();
		  float complex* __restrict__ gridPtr;
		  const float complex* __restrict__ cf;


		  const float complex* __restrict__ cf0;

		  // // no jumps
		  int io=(offy - fsupy*fsampy);
		  int jo=(offx - fsupx*fsampx);
		  int cfoff = io * OverS * SupportCF*SupportCF + jo * SupportCF*SupportCF;
		  //cf0 =  __builtin_assume_aligned(p_complex64(cfs) + cfoff,8);
		  cf0 =  p_complex64(cfs) + cfoff;

                  for (sy=-fsupy; sy<=fsupy; ++sy) {
                    // Get the pointer in the grid for the first x in this y.
                    //double complex __restrict__ *gridPtr = grid.data() + goff + (locy+sy)*nGridX + locx-supx;
		    // Fast version
		    //gridPtr = p_complex64(grid) + goff + (locy+sy)*nGridX + locx-supx;
		    //gridPtr =  __builtin_assume_aligned(p_complex64(grid) + goff + (locy+sy)*nGridX + locx-supx,8);
		    gridPtr =  p_complex64(grid) + goff + (locy+sy)*nGridX + locx-supx;

		    //##################################
                    //int cfoff = (offy + supy)*nConvX + offx - fsupx;
		    
		    //##################################

		    //printf("start off CF: (%3.3i,%3.3i) -> CFoff: %i \n",offx,offy,cfoff);
		    //printf("(offy, sy, fsampy, nConvX, offx, fsupx, fsampx) = (%i, %i, %i, %i, %i, %i, %i) \n",offy, sy,fsampy,nConvX,offx,fsupx,fsampx);

		    //cf[0] = (*cfs.vdata)[CFChan][0][0].data() + cfoff;
		    
		    //int cfoff = (offy + sy*fsampy)*nConvX + offx - fsupx*fsampx;
		    //cf0 =  p_complex64(cfs) + cfoff;
		    //cf0 =  __builtin_assume_aligned(p_complex64(cfs) + cfoff,8);
		    int sx;
                    for (sx=-fsupx; sx<=fsupx; ++sx) {
		      //printf("(%3.3i,%3.3i) CF=(%f, %f) \n",sx,sy,creal(*cf[0]),cimag(*cf[0])); 
                      // Loop over polarizations to correct for leakage.
                      //complex polSum(0,0);
  		      //polSum *= *imgWtPtr;
		      //printf(".. Chan=%i, gridin=(%f, %f), VisVal=(%f,%f) \n",visChan,creal(*gridPtr),cimag(*gridPtr),creal(VisVal),cimag(VisVal));
		      //printf(".. %i/%i   CF=(%f,%f) \n",inx,nrows,creal(*cf0),cimag(*cf0));

                      *gridPtr++ += VisVal * *cf0;// * *imgWtPtr;
		      //printf(" ... gridout=(%f, %f) \n",creal(*gridPtr),cimag(*gridPtr));
		      cf0 ++;
		      //cf0 +=fsampx;
		      //Nop+=1;

		      /* polSum += VisVal * *cf[0]; */
		      /* cf[0] += fsampx; */
  		      /* polSum *= *imgWtPtr; */
                      /* *gridPtr++ += polSum; */
                    }

                  }
		  //VarTimeGrid+=AppendTimeit();
                  sumWtPtr[gridPol+gridChan*nGridPol] += ThisWeight;//*imgWtPtr;
		  /* if{*imgWtPtr>2.}{ */
		  //printf(" [%i,%i,%f] ",inx,visChan,*imgWtPtr);
		  /* } */
                } // end if gridPol
              } // end if !flagPtr
            } // end for ipol
          } // end if ongrid
        } // end if gridChan
        imgWtPtr++;
      } // end for visChan
    } // end for inx
    //    printf(" timegrid %f %i \n",VarTimeGrid,Nop);
  }




////////////////////

static PyObject *pyDeGridderWPol(PyObject *self, PyObject *args)
{
  PyObject *ObjGridIn;
  PyObject *ObjVis;
  PyArrayObject *np_grid, *np_vis, *uvw, *cfs, *flags, *sumwt, *increment, *freqs,*WInfos;

  PyObject *Lcfs;
  PyObject *Lmaps,*LJones;
  PyObject *LcfsConj;
  int dopsf;

  if (!PyArg_ParseTuple(args, "O!OO!O!O!iO!O!O!O!O!O!O!", 
			//&ObjGridIn,
			&PyArray_Type,  &np_grid,
			&ObjVis,//&PyArray_Type,  &vis, 
			&PyArray_Type,  &uvw, 
			&PyArray_Type,  &flags, 
			//&PyArray_Type,  &rows, 
			&PyArray_Type,  &sumwt, 
			&dopsf, 
			&PyList_Type, &Lcfs,
			&PyList_Type, &LcfsConj,
			&PyArray_Type,  &WInfos,
			&PyArray_Type,  &increment,
			&PyArray_Type,  &freqs,
			&PyList_Type, &Lmaps, &PyList_Type, &LJones
			))  return NULL;
  int nx,ny,nz,nzz;

  np_vis = (PyArrayObject *) PyArray_ContiguousFromObject(ObjVis, PyArray_COMPLEX64, 0, 3);

  
  /* int nVisRow  = np_vis->dimensions[0]; */
  /* int nVisChan = np_vis->dimensions[1]; */
  /* int nVisPol  = np_vis->dimensions[2]; */
  /* int ix,iy,iz; */
  /* for(ix=0; ix<nVisRow; ix++){ */
  /*   for(iy=0; iy<nVisChan; iy++){ */
  /*     int doff = (ix * nVisChan + iy) * nVisPol; */
  /*     double complex* visPtr  = Complex_pyvector_to_Carrayptrs(np_vis)  + doff; */
  /*     for(iz=0; iz<nVisPol; iz++){ */
  /* 	//double complex Vis=visPtr[iz]; */
  /* 	printf("[%i,%i,%i] (%f , %f)      ",ix,iy,iz,creal(visPtr[iz]),cimag(visPtr[iz])); */
  /* 	visPtr[iz]=1.+(1.*I); */
  /* 	printf("[%i,%i,%i] (%f , %f)\n",ix,iy,iz,creal(visPtr[iz]),cimag(visPtr[iz])); */
  /*     }  */
  /*   }  */
  /* }  */


  DeGridderWPol(np_grid, np_vis, uvw, flags, sumwt, dopsf, Lcfs, LcfsConj, WInfos, increment, freqs, Lmaps, LJones);
  
  //return PyArray_Return(np_vis);

  return Py_None;

}





void DeGridderWPol(PyArrayObject *grid,
		   PyArrayObject *vis,
		   PyArrayObject *uvw,
		   PyArrayObject *flags,
		   //PyArrayObject *rows,
		   PyArrayObject *sumwt,
		   int dopsf,
		   PyObject *Lcfs,
		   PyObject *LcfsConj,
		   PyArrayObject *Winfos,
		   PyArrayObject *increment,
		   PyArrayObject *freqs,
		   PyObject *Lmaps, PyObject *LJones)
  {
    // Get size of convolution functions.
    PyArrayObject *cfs;
    PyArrayObject *NpPolMap;
    NpPolMap = (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(Lmaps, 0), PyArray_INT32, 0, 4);
    int npolsMap=NpPolMap->dimensions[0];
    int* PolMap=I_ptr(NpPolMap);
    
    PyArrayObject *NpFacetInfos;
    NpFacetInfos = (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(Lmaps, 1), PyArray_FLOAT64, 0, 4);

    PyArrayObject *NpRows;
    NpRows = (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(Lmaps, 2), PyArray_INT32, 0, 4);
    int* ptrRows=I_ptr(NpRows);
    int row0=ptrRows[0];
    int row1=ptrRows[1];


    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    int LengthJonesList=PyList_Size(LJones);
    int DoApplyJones=0;
    PyArrayObject *npJonesMatrices, *npTimeMappingJonesMatrices, *npA0, *npA1, *npJonesIDIR, *npCoefsInterp,*npModeInterpolation;
    float complex* ptrJonesMatrices;
    int *ptrTimeMappingJonesMatrices,*ptrA0,*ptrA1,*ptrJonesIDIR;
    float *ptrCoefsInterp;
    int i_dir;
    int nd_Jones,na_Jones,nch_Jones,nt_Jones;

    printf("len %i",LengthJonesList);
    int JonesDims[4];
    int ModeInterpolation=1;
    int *ptrModeInterpolation;

    if(LengthJonesList>0){
      DoApplyJones=1;

      npTimeMappingJonesMatrices  = (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 0), PyArray_INT32, 0, 4);
      ptrTimeMappingJonesMatrices = p_int32(npTimeMappingJonesMatrices);

      npA0 = (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 1), PyArray_INT32, 0, 4);
      ptrA0 = p_int32(npA0);
      int ifor;

      npA1= (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 2), PyArray_INT32, 0, 4);
      ptrA1=p_int32(npA1);
      
      // (nt,nd,na,1,2,2)
      npJonesMatrices = (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 3), PyArray_COMPLEX64, 0, 6);
      ptrJonesMatrices=p_complex64(npJonesMatrices);
      nt_Jones=(int)npJonesMatrices->dimensions[0];
      nd_Jones=(int)npJonesMatrices->dimensions[1];
      na_Jones=(int)npJonesMatrices->dimensions[2];
      nch_Jones=(int)npJonesMatrices->dimensions[3];
      JonesDims[0]=nt_Jones;
      JonesDims[1]=nd_Jones;
      JonesDims[2]=na_Jones;
      JonesDims[3]=nch_Jones;

      npJonesIDIR= (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 4), PyArray_INT32, 0, 4);
      ptrJonesIDIR=p_int32(npJonesIDIR);
      i_dir=ptrJonesIDIR[0];

      npCoefsInterp= (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 5), PyArray_FLOAT32, 0, 4);
      ptrCoefsInterp=p_float32(npCoefsInterp);

      npModeInterpolation= (PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LJones, 6), PyArray_INT32, 0, 4);
      ptrModeInterpolation=p_int32(npModeInterpolation);
      ModeInterpolation=ptrModeInterpolation[0];

    };
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////
    ////////////////////////////////////////////////////////////////////////////



    
    double VarTimeDeGrid=0;
    int Nop=0;

    double* ptrFacetInfos=p_float64(NpFacetInfos);
    double Cu=ptrFacetInfos[0];
    double Cv=ptrFacetInfos[1];
    double l0=ptrFacetInfos[2];
    double m0=ptrFacetInfos[3];
    double n0=sqrt(1-l0*l0-m0*m0)-1;


    //printf("npols=%i %i\n",npolsMap,PolMap[3]);

    // Get size of grid.
    double* ptrWinfo = p_float64(Winfos);
    double WaveRefWave = ptrWinfo[0];
    double wmax = ptrWinfo[1];
    double NwPlanes = ptrWinfo[2];
    int OverS=floor(ptrWinfo[3]);


    //printf("WaveRef=%f, wmax=%f \n",WaveRefWave,wmax);
    int nGridX    = grid->dimensions[3];
    int nGridY    = grid->dimensions[2];
    int nGridPol  = grid->dimensions[1];
    int nGridChan = grid->dimensions[0];
    
    // Get visibility data size.
    int nVisPol   = flags->dimensions[2];
    int nVisChan  = flags->dimensions[1];
    int nrows     = uvw->dimensions[0];
    //printf("(nrows, nVisChan, nVisPol)=(%i, %i, %i)\n",nrows,nVisChan,nVisPol);
    
    
    // Get oversampling and support size.
    int sampx = OverS;//int (cfs.sampling[0]);
    int sampy = OverS;//int (cfs.sampling[1]);
    
    double* __restrict__ sumWtPtr = p_float64(sumwt);//->data;
    double complex psfValues[4];
    psfValues[0] = psfValues[1] = psfValues[2] = psfValues[3] = 1;

    //uint inxRowWCorr(0);

    double offset_p[2],uvwScale_p[2];

    offset_p[0]=nGridX/2;//(nGridX-1)/2.;
    offset_p[1]=nGridY/2;
    float fnGridX=nGridX;
    float fnGridY=nGridY;
    double *incr=p_float64(increment);
    double *Pfreqs=p_float64(freqs);
    uvwScale_p[0]=fnGridX*incr[0];
    uvwScale_p[1]=fnGridX*incr[1];
    //printf("uvscale=(%f %f)",uvwScale_p[0],uvwScale_p[1]);
    double C=2.99792458e8;
    int inx;


    double posx,posy;


    // Loop over all visibility rows to process.
    for (inx=row0; inx<row1; ++inx) {
      int irow = inx;

      //printf("row=%i/%i \n",irow,nrows);



      double*  __restrict__ uvwPtr   = p_float64(uvw) + irow*3;
      // Loop over all channels in the visibility data.
      // Map the visibility channel to the grid channel.
      // Skip channel if data are not needed.
      int visChan;
      
      for (visChan=0; visChan<nVisChan; ++visChan) {
        int gridChan = 0;//chanMap_p[visChan];
        int CFChan = 0;//ChanCFMap[visChan];
	double recipWvl = Pfreqs[visChan] / C;
	double ThisWaveLength=C/Pfreqs[visChan];
	//printf("visChan=%i \n",visChan);
	
	//W-projection
	double wcoord=uvwPtr[2];
	
	int iwplane = floor((NwPlanes-1)*abs(wcoord)*(WaveRefWave/ThisWaveLength)/wmax+0.5);
	int skipW=0;
	if(iwplane>NwPlanes-1){skipW=1;continue;};

	//int iwplane = floor((NwPlanes-1)*abs(wcoord)/wmax);

	//printf("wcoord=%f, iw=%i \n",wcoord,iwplane);

	if(wcoord>0){
	  cfs=(PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(Lcfs, iwplane), PyArray_COMPLEX64, 0, 2);
	} else{
	  cfs=(PyArrayObject *) PyArray_ContiguousFromObject(PyList_GetItem(LcfsConj, iwplane), PyArray_COMPLEX64, 0, 2);
	}
	int nConvX = cfs->dimensions[0];
	int nConvY = cfs->dimensions[1];
	int supx = (nConvX/OverS-1)/2;
	int supy = (nConvY/OverS-1)/2;
	int SupportCF=nConvX/OverS;


	//cout<<"  chan="<<visChan<<"taking CF="<<CFChan<<endl;

	// !! dirty trick to select all channels
	//chanMap_p[visChan]=0;

        if (gridChan >= 0  &&  gridChan < nGridChan) {
          // Determine the grid position from the UV coordinates in wavelengths.

	  // Change coordinate and shift visibility to facet center
	  double complex UVNorm=2.*I*PI/ThisWaveLength;
	  double U=uvwPtr[0];
	  double V=uvwPtr[1];
	  double W=uvwPtr[2];
	  double complex corr=cexp(UVNorm*(U*l0+V*m0+W*n0));
	  U+=W*Cu;
	  V+=W*Cv;
	  //printf("uvw = (%f,%f,%f)\n",U,V,W);

	  double recipWvl = Pfreqs[visChan] / C;
	  //cout<<"vbs.freq_p[visChan]" <<vbs.freq_p[visChan] <<endl;
	  posx = uvwScale_p[0] * U * recipWvl + offset_p[0];//#-1;
	  posy = uvwScale_p[1] * V * recipWvl + offset_p[1];//-1;

          int locx = nint (posx);    // location in grid
          int locy = nint (posy);
	  //printf("locx=%i, locy=%i\n",locx,locy);
          double diffx = locx - posx;
          double diffy = locy - posy;
	  //printf("diffx=%f, diffy=%f\n",diffx,diffy);
          int offx = nint (diffx * sampx); // location in
          int offy = nint (diffy * sampy); // oversampling
	  //printf("offx=%i, offy=%i\n",offx,offy);
          offx += (nConvX-1)/2;
          offy += (nConvY-1)/2;
          // Scaling with frequency is not necessary (according to Cyril).
          double freqFact = 1;
          int fsampx = nint (sampx * freqFact);
          int fsampy = nint (sampy * freqFact);
          int fsupx  = nint (supx / freqFact);
          int fsupy  = nint (supy / freqFact);

	  //



	  /* Weights_Lin_Interp[0]=(1.-diffx)*(1.-diffy); */
	  /* Weights_Lin_Interp[1]=(1.-diffx)*diffy; */
	  /* Weights_Lin_Interp[2]=diffx*(1.-diffy); */
	  /* Weights_Lin_Interp[3]=diffx*diffy; */


          // Only use visibility point if the full support is within grid.
          if (locx-supx >= 0  &&  locx+supx < nGridX  &&
              locy-supy >= 0  &&  locy+supy < nGridY) {
            ///            cout << "in grid"<<endl;
            // Get pointer to data and flags for this channel.
            int doff = (irow * nVisChan + visChan) * nVisPol;
            float complex* __restrict__ visPtr  = p_complex64(vis)  + doff;
            bool* __restrict__ flagPtr = p_bool(flags) + doff;
	    float complex ThisVis[4]={0};

	    int ipol;

            // Handle a visibility if not flagged.
            /* for (ipol=0; ipol<nVisPol; ++ipol) { */
            /*   if (! flagPtr[ipol]) { */
	    /* 	visPtr[ipol] = Complex(0,0); */
            /*   } */
            /* } */

	    //for (Int w=0; w<4; ++w) {
	    //  Double weight_interp(Weights_Lin_Interp[w]);
            for (ipol=0; ipol<nVisPol; ++ipol) {
              if (((int)flagPtr[ipol])==0) {
                // Map to grid polarization. Only use pol if needed.
                int gridPol = PolMap[ipol];
                if (gridPol >= 0  &&  gridPol < nGridPol) {
                  /// Complex norm(0,0);
                  // Get the offset in the grid data array.

                  int goff = (gridChan*nGridPol + gridPol) * nGridX * nGridY;
                  // Loop over the scaled support.
		  int sy;
		  //initTime();

		  const float complex* __restrict__ gridPtr;
		  const float complex* __restrict__ cf0;

		  // // no jumps
		  int io=(offy - fsupy*fsampy);
		  int jo=(offx - fsupx*fsampx);
		  int cfoff = io * OverS * SupportCF*SupportCF + jo * SupportCF*SupportCF;
		  //cf0 =  __builtin_assume_aligned(p_complex64(cfs) + cfoff,8);
		  cf0 =  p_complex64(cfs) + cfoff;




                  for (sy=-fsupy; sy<=fsupy; ++sy) {
                    // Get the pointer in the grid for the first x in this y.
		    //float complex *gridPtr = p_complex64(grid) + goff + (locy+sy)*nGridX + locx-supx;
		    //gridPtr =  __builtin_assume_aligned(p_complex64(grid) + goff + (locy+sy)*nGridX + locx-supx,8);
		    gridPtr =  p_complex64(grid) + goff + (locy+sy)*nGridX + locx-supx;
		    // Fast version

                    //const float complex* __restrict__ cf[1];
                    //int cfoff = (offy + sy*fsampy)*nConvX + offx - fsupx*fsampx;

                    // Get pointers to the first element to use in the 4
                    // convolution functions for this channel,pol.

		    // fast version


 		    //cf[0] = p_complex64(cfs) + cfoff;
		    int sx;
                    for (sx=-fsupx; sx<=fsupx; ++sx) {
		      //outFile<<irow <<" "<<ipol<<" "<<posx<<" "<<posy<<" "<<(offx+ sx*fsampx-(nConvX-1.)/2.)/float(fsampx)<<" "<<(offy + sy*fsampy-(nConvX-1)/2.)/float(fsampy)
		      //<<" "<<real(*gridPtr * *cf[0])<<" "<<imag(*gridPtr * *cf[0])<<" "<<real(*gridPtr)<<" "<<imag(*gridPtr)<<endl;
		      
		      //visPtr[ipol] += *gridPtr  * *cf[0] *corr;;//* factor;
		      //ThisVis[ipol] += *gridPtr  * *cf[0];
		      ThisVis[ipol] += *gridPtr  * *cf0;
		      
		      //cf[0] += fsampx;
		      cf0 ++;
                      gridPtr++;
		      //Nop+=1;
		      //printf("(%f, %f)\n",creal(visPtr[ipol]),cimag(visPtr[ipol]));
                    }

		    // // Full version
                    // const Complex* __restrict__ cf[4];
                    // Int cfoff = (offy + sy*fsampy)*nConvX + offx - fsupx*fsampx;
                    // for (int i=0; i<4; ++i) {
                    //   cf[i] = (*cfs.vdata)[gridChan][i][ipol].data() + cfoff;
                    // }
                    // for (Int sx=-fsupx; sx<=fsupx; ++sx) {
                    //   for (Int i=0; i<nVisPol; ++i) {
                    //     visPtr[i] += *gridPtr * *cf[i];
                    //     cf[i] += fsampx;
                    //   }
                    //   gridPtr++;
                    // }

                  }
		  //VarTimeDeGrid+=AppendTimeit();
                } // end if gridPol



              } // end if !flagPtr
	      //visPtr[ipol]*=corr;
            } // end for ipol

	    if(DoApplyJones){
	      // Shape: nt,nd,na,1,2,2
	      int i_t=ptrTimeMappingJonesMatrices[irow];
	      int i_ant0=ptrA0[irow];
	      int i_ant1=ptrA1[irow];
	      
	      float complex J0[4]={0},J1[4]={0},J1H[4]={0};
	      GiveJones(ptrJonesMatrices, JonesDims, ptrCoefsInterp, i_t, i_ant0, i_dir, ModeInterpolation, J0);
	      GiveJones(ptrJonesMatrices, JonesDims, ptrCoefsInterp, i_t, i_ant1, i_dir, ModeInterpolation, J1);
	      
	      MatH(J1,J1H);
	      MatDot(J0,ThisVis,ThisVis);
	      MatDot(ThisVis,J1H,ThisVis);
	      
	    };

	    for(ipol=0; ipol<4; ipol++){
	      visPtr[ipol]+=ThisVis[ipol] *corr;
	    }

          } // end if ongrid
        } // end if gridChan
	//}
      } // end for visChan
    } // end for inx
    //assert(false);
    //printf(" timedegrid %f %i\n",VarTimeDeGrid,Nop);
  }
