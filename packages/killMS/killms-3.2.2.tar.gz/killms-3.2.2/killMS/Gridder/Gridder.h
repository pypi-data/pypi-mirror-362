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

/* Header to test of C modules for arrays for Python: C_test.c */
#include "complex.h"
#include <math.h>
#include <stdbool.h>

/* ==== Prototypes =================================== */

// .... Python callable Vector functions ..................


/* .... C vector utility functions ..................*/
//PyArrayObject *pyvector(PyObject *objin);
double *pyvector_to_Carrayptrs(PyArrayObject *arrayin);
int *pyvector_to_Carrayptrs2(PyArrayObject *arrayin);
//===========================================
double complex *GetCp(PyArrayObject *arrayin);
double complex *Complex_pyvector_to_Carrayptrs(PyArrayObject *arrayin);
int *Int_pyvector_to_Carrayptrs(PyArrayObject *arrayin);
//int  not_doublevector(PyArrayObject *vec);
int nint(double n){
  //  double x=n+0.5;
  //printf("%f+0.5= %f\n",n,x);
  return floor(n+0.5);};

/* .... Python callable Matrix functions ..................*/

int *I_ptr(PyArrayObject *arrayin)  {
	return (int *) arrayin->data;
}


int *p_int32(PyArrayObject *arrayin)  {
  return (int *) arrayin->data;  /* pointer to arrayin data as double */
}


double *p_float64(PyArrayObject *arrayin)  {
  return (double *) arrayin->data;  /* pointer to arrayin data as double */
}

float *p_float32(PyArrayObject *arrayin)  {
  return (float *) arrayin->data;  /* pointer to arrayin data as double */
}


float complex *p_complex64(PyArrayObject *arrayin)  {
  return (float complex *) arrayin->data;  /* pointer to arrayin data as double */
}

double complex *p_complex128(PyArrayObject *arrayin)  {
  return (double complex *) arrayin->data;  /* pointer to arrayin data as double */
}

bool *p_bool(PyArrayObject *arrayin)  {
  return (bool *) arrayin->data;  /* pointer to arrayin data as double */
}



static PyObject *pyTestMatrix(PyObject *self, PyObject *args);
void MatInv(float complex *A, float complex* B, int H );
void MatDot(float complex *A, float complex* B, float complex* Out );



static PyObject *pyGridderPoints(PyObject *self, PyObject *args);




static PyObject *pyGridderWPol(PyObject *self, PyObject *args);
static PyObject *pyAddArray(PyObject *self, PyObject *args);
static PyObject *pyWhereMax(PyObject *self, PyObject *args);


void gridderWPol(PyArrayObject *np_grid,
	      PyArrayObject *vis,
	      PyArrayObject *uvw,
	      PyArrayObject *flags,
	      PyArrayObject *weigths,
	      PyArrayObject *sumwt,
	      int dopsf,
	      PyObject *Lcfs,
	      PyObject *LcfsConj,
	      PyArrayObject *Winfos,
	      PyArrayObject *increment,
	      PyArrayObject *freqs,
	      PyObject *Lmaps, 
	      PyObject *LJones);

static PyObject *pyDeGridderWPol(PyObject *self, PyObject *args);

void DeGridderWPol(PyArrayObject *np_grid,
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
	      PyObject *Lmaps, 
	      PyObject *LJones);

/* .... C matrix utility functions ..................*/
//PyArrayObject *pymatrix(PyObject *objin);
//double **pymatrix_to_Carrayptrs(PyArrayObject *arrayin);
//double **ptrvector(long n);
/* void free_Carrayptrs(double **v); */
/* void free_Carrayptrs2(double *v); */
/* int  not_doublematrix(PyArrayObject *mat); */

/* .... Python callable integer 2D array functions ..................*/


//* * .... C 2D int array utility functions ..................*\/ */
/* PyArrayObject *pyint2Darray(PyObject *objin); */
/* int **pyint2Darray_to_Carrayptrs(PyArrayObject *arrayin); */
/* int **ptrintvector(long n); */
/* void free_Cint2Darrayptrs(int **v); */
/* int  not_int2Darray(PyArrayObject *mat); */
