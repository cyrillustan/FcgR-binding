/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: NormalErrorCoef_initialize.c
 *
 * MATLAB Coder version            : 3.1
 * C/C++ source code generated on  : 15-Aug-2016 16:41:41
 */

/* Include Files */
#include "rt_nonfinite.h"
#include "NormalErrorCoef.h"
#include "NormalErrorCoef_initialize.h"

/* Function Definitions */

/*
 * Arguments    : void
 * Return Type  : void
 */
void NormalErrorCoef_initialize(void)
{
  rt_InitInfAndNaN(8U);
}

/*
 * File trailer for NormalErrorCoef_initialize.c
 *
 * [EOF]
 */