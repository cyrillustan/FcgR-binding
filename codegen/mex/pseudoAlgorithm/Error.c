/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 *
 * Error.c
 *
 * Code generation for function 'Error'
 *
 */

/* Include files */
#include "rt_nonfinite.h"
#include "pseudoAlgorithm.h"
#include "Error.h"
#include "StoneSolver.h"
#include "pseudoAlgorithm_data.h"

/* Variable Definitions */
static emlrtRSInfo p_emlrtRSI = { 16, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtRSInfo q_emlrtRSI = { 18, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtRSInfo r_emlrtRSI = { 45, "Error",
  "C:\\Users\\ryan\\Documents\\GitHub\\recepnum1\\Error.m" };

static emlrtRSInfo eb_emlrtRSI = { 7, "nansum",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\stats\\eml\\nansum.m" };

static emlrtBCInfo vb_emlrtBCI = { 1, 8, 128, 13, "", "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m",
  0 };

static emlrtBCInfo wb_emlrtBCI = { 1, 192, 113, 27, "", "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m",
  0 };

static emlrtBCInfo xb_emlrtBCI = { 1, 192, 100, 23, "", "nan_sum_or_mean",
  "C:\\Program Files\\MATLAB\\R2015b\\toolbox\\stats\\eml\\private\\nan_sum_or_mean.m",
  0 };

/* Function Definitions */
void Error(const emlrtStack *sp, real_T Rtot[9], const real_T Kd[24], const
           real_T mfiAdjMean[192], const real_T v[2], const real_T biCoefMat[676],
           const real_T tnpbsa[2], real_T *J, real_T mfiExp_data[], int32_T
           mfiExp_size[2], real_T mfiExpPre[48])
{
  real_T y[9];
  int32_T k;
  real_T Kx;
  real_T mfiExpPrePre[48];
  int32_T j;
  int32_T ixstart;
  int32_T ix;
  boolean_T varargin_1[48];
  boolean_T maxval[8];
  int32_T i;
  boolean_T mtmp;
  real_T a[192];
  real_T b_varargin_1[192];
  real_T b_y[8];
  int32_T iy;
  real_T s;
  emlrtStack st;
  emlrtStack b_st;
  st.prev = sp;
  st.tls = sp->tls;
  b_st.prev = &st;
  b_st.tls = st.tls;

  /*  If error is called with Rtot being a single value, assume we want to */
  /*  have constant expression across all the receptors */
  /* Convert from log scale */
  memcpy(&y[0], &Rtot[0], 9U * sizeof(real_T));
  for (k = 0; k < 9; k++) {
    Rtot[k] = muDoubleScalarPower(10.0, y[k]);
  }

  Kx = Rtot[6];

  /* Get expected value of MFIs (before conversion factors) from Equation 7 */
  /* from Stone */
  memset(&mfiExpPrePre[0], 0, 48U * sizeof(real_T));
  j = 0;
  while (j < 6) {
    k = 0;
    while (k < 4) {
      st.site = &p_emlrtRSI;
      mfiExpPrePre[j + 6 * k] = StoneSolver(&st, Rtot[j], Kx, v[0], Kd[j + 6 * k],
        tnpbsa[0], biCoefMat);
      st.site = &q_emlrtRSI;
      mfiExpPrePre[j + 6 * (4 + k)] = StoneSolver(&st, Rtot[j], Kx, v[1], Kd[j +
        6 * k], tnpbsa[1], biCoefMat);
      k++;
      if (*emlrtBreakCheckR2012bFlagVar != 0) {
        emlrtBreakCheckR2012b(sp);
      }
    }

    j++;
    if (*emlrtBreakCheckR2012bFlagVar != 0) {
      emlrtBreakCheckR2012b(sp);
    }
  }

  /* Multiply by conversion factors */
  for (ixstart = 0; ixstart < 48; ixstart++) {
    mfiExpPre[ixstart] = Rtot[7] * mfiExpPrePre[ixstart];
  }

  for (ixstart = 0; ixstart < 4; ixstart++) {
    for (ix = 0; ix < 6; ix++) {
      mfiExpPre[ix + 6 * (4 + ixstart)] = Rtot[8] * mfiExpPrePre[ix + 6 * (4 +
        ixstart)];
    }
  }

  /* Check for undefined values (errors from ReqFuncSolver) */
  for (ixstart = 0; ixstart < 48; ixstart++) {
    varargin_1[ixstart] = (mfiExpPre[ixstart] == -1.0);
  }

  for (j = 0; j < 8; j++) {
    maxval[j] = varargin_1[6 * j];
    for (i = 0; i < 5; i++) {
      mtmp = maxval[j];
      if ((int32_T)varargin_1[(i + 6 * j) + 1] > (int32_T)maxval[j]) {
        mtmp = varargin_1[(i + 6 * j) + 1];
      }

      maxval[j] = mtmp;
    }
  }

  mtmp = maxval[0];
  for (ix = 0; ix < 7; ix++) {
    if ((int32_T)maxval[ix + 1] > (int32_T)mtmp) {
      mtmp = maxval[ix + 1];
    }
  }

  if (mtmp) {
    *J = 1.0E+8;
    mfiExp_size[0] = 6;
    mfiExp_size[1] = 8;
    for (ixstart = 0; ixstart < 48; ixstart++) {
      mfiExpPre[ixstart] = -1.0;
      mfiExp_data[ixstart] = -1.0;
    }
  } else {
    /* Create array of expected values to calculate residuals */
    mfiExp_size[0] = 24;
    mfiExp_size[1] = 8;
    memset(&mfiExp_data[0], 0, 192U * sizeof(real_T));
    j = 0;
    while (j < 6) {
      k = 0;
      while (k < 4) {
        ixstart = (j << 2) + k;
        for (ix = 0; ix < 4; ix++) {
          mfiExp_data[ixstart + 24 * ix] = mfiExpPre[j + 6 * k];
        }

        ixstart = (j << 2) + k;
        for (ix = 0; ix < 4; ix++) {
          mfiExp_data[ixstart + 24 * (4 + ix)] = mfiExpPre[j + 6 * (4 + k)];
        }

        k++;
        if (*emlrtBreakCheckR2012bFlagVar != 0) {
          emlrtBreakCheckR2012b(sp);
        }
      }

      j++;
      if (*emlrtBreakCheckR2012bFlagVar != 0) {
        emlrtBreakCheckR2012b(sp);
      }
    }

    /* Error */
    st.site = &r_emlrtRSI;
    for (ixstart = 0; ixstart < 192; ixstart++) {
      a[ixstart] = mfiExp_data[ixstart] - mfiAdjMean[ixstart];
    }

    b_st.site = &ab_emlrtRSI;
    for (k = 0; k < 192; k++) {
      b_varargin_1[k] = muDoubleScalarPower(a[k], 2.0);
    }

    st.site = &r_emlrtRSI;
    b_st.site = &eb_emlrtRSI;
    ix = 0;
    iy = 0;
    for (i = 0; i < 8; i++) {
      ixstart = ix;
      ix++;
      if (!((ixstart + 1 >= 1) && (ixstart + 1 <= 192))) {
        emlrtDynamicBoundsCheckR2012b(ixstart + 1, 1, 192, &xb_emlrtBCI, &b_st);
      }

      if (!muDoubleScalarIsNaN(b_varargin_1[ixstart])) {
        s = b_varargin_1[ixstart];
      } else {
        s = 0.0;
      }

      for (k = 0; k < 23; k++) {
        ix++;
        if (!((ix >= 1) && (ix <= 192))) {
          emlrtDynamicBoundsCheckR2012b(ix, 1, 192, &wb_emlrtBCI, &b_st);
        }

        if (!muDoubleScalarIsNaN(b_varargin_1[ix - 1])) {
          s += b_varargin_1[ix - 1];
        }
      }

      iy++;
      if (!((iy >= 1) && (iy <= 8))) {
        emlrtDynamicBoundsCheckR2012b(iy, 1, 8, &vb_emlrtBCI, &b_st);
      }

      b_y[iy - 1] = s;
    }

    *J = 0.0;
    for (k = 0; k < 8; k++) {
      if (!muDoubleScalarIsNaN(b_y[k])) {
        *J += b_y[k];
      }
    }
  }
}

/* End of code generation (Error.c) */