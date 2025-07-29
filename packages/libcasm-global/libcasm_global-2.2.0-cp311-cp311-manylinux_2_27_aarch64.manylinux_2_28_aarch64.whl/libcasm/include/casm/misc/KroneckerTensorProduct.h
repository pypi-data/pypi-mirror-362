#include <casm/external/Eigen/Core>

// This file is part of Eigen, a lightweight C++ template library
// for linear algebra.
//
// Copyright (C) 2011 Kolja Brix <brix@igpm.rwth-aachen.de>
// Copyright (C) 2011 Andreas Platen <andiplaten@gmx.de>
//
// This Source Code Form is subject to the terms of the Mozilla
// Public License v. 2.0. If a copy of the MPL was not distributed
// with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
//
// Note from JGG:
// A newer implementation of this file exists, but I've kept this one
// because the interface is different. We might want to go with the
// newer version though.
 
 
#ifndef KRONECKER_TENSOR_PRODUCT_H
#define KRONECKER_TENSOR_PRODUCT_H
 
 
namespace Eigen {
 
  namespace internal {
 
    template<typename Derived_A, typename Derived_B, typename Derived_AB>
      void kroneckerProduct_full(const Derived_A& A, const Derived_B& B, Derived_AB & AB)
    {
      const unsigned int Ar = A.rows(),
	Ac = A.cols(),
	Br = B.rows(),
	Bc = B.cols();
      for (unsigned int i=0; i<Ar; ++i)
	for (unsigned int j=0; j<Ac; ++j)
	  AB.block(i*Br,j*Bc,Br,Bc) = A(i,j)*B;
    }
 
 
    template<typename Derived_A, typename Derived_B, typename Derived_AB>
      void kroneckerProduct_sparse(const Derived_A &A, const Derived_B &B, Derived_AB &AB)
    {
      const unsigned int Ar = A.rows(),
	Ac = A.cols(),
	Br = B.rows(),
	Bc = B.cols();
      AB.resize(Ar*Br,Ac*Bc);
      AB.resizeNonZeros(0);
      AB.reserve(A.nonZeros()*B.nonZeros());
 
      for (int kA=0; kA<A.outerSize(); ++kA)
	{
	  for (int kB=0; kB<B.outerSize(); ++kB)
	    {
	      for (typename Derived_A::InnerIterator itA(A,kA); itA; ++itA)
		{
		  for (typename Derived_B::InnerIterator itB(B,kB); itB; ++itB)
		    {
		      const unsigned int iA = itA.row(),
			jA = itA.col(),
			iB = itB.row(),
			jB = itB.col(),
			i = iA*Br + iB,
			j = jA*Bc + jB;
		      AB.insert(i,j) = itA.value() * itB.value();
		    }
		}
	    }
	}
    }
 
  } // end namespace internal
 
 
 
  template<typename A,typename B,typename CScalar,int CRows,int CCols, int COptions, int CMaxRows, int CMaxCols>
    void kroneckerProduct(const MatrixBase<A>& a, const MatrixBase<B>& b, Matrix<CScalar,CRows,CCols,COptions,CMaxRows,CMaxCols>& c)
  {
    c.resize(a.rows()*b.rows(),a.cols()*b.cols());
    internal::kroneckerProduct_full(a.derived(), b.derived(), c);
  }
 
  template<typename A,typename B,typename C>
    void kroneckerProduct(const MatrixBase<A>& a, const MatrixBase<B>& b, MatrixBase<C> const & c_)
  {
    MatrixBase<C>& c = const_cast<MatrixBase<C>& >(c_);
    internal::kroneckerProduct_full(a.derived(), b.derived(), c.derived());
  }
 
} // end namespace Eigen
 
#endif // KRONECKER_TENSOR_PRODUCT_H
