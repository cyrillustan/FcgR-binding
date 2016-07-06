/*
 * Academic License - for use in teaching, academic research, and meeting
 * course requirements at degree granting institutions only.  Not for
 * government, commercial, or other organizational use.
 * File: main.c
 *
 * MATLAB Coder version            : 3.0
 * C/C++ source code generated on  : 29-Jun-2016 10:10:25
 */

/*************************************************************************/
/* This automatically generated example C main file shows how to call    */
/* entry-point functions that MATLAB Coder generated. You must customize */
/* this file for your application. Do not modify this file directly.     */
/* Instead, make a copy of this file, modify it, and integrate it into   */
/* your development environment.                                         */
/*                                                                       */
/* This file initializes entry-point function arguments to a default     */
/* size and value before calling the entry-point functions. It does      */
/* not store or use any values returned from the entry-point functions.  */
/* If necessary, it does pre-allocate memory for returned values.        */
/* You can use this file as a starting point for a main function that    */
/* you can deploy in your application.                                   */
/*                                                                       */
/* After you copy the file, and before you deploy it, you must make the  */
/* following changes:                                                    */
/* * For variable-size function arguments, change the example sizes to   */
/* the sizes that your application requires.                             */
/* * Change the example values of function arguments to the values that  */
/* your application requires.                                            */
/* * If the entry-point functions return values, store these values or   */
/* otherwise use them as required by your application.                   */
/*                                                                       */
/*************************************************************************/
/* Include Files */
#include "rt_nonfinite.h"
#include "pseudoAlgorithm.h"
#include "main.h"
#include "pseudoAlgorithm_terminate.h"
#include "pseudoAlgorithm_emxAPI.h"
#include "pseudoAlgorithm_initialize.h"

/* Function Declarations */
static void argInit_24x2_real_T(double result[48]);
static void argInit_24x8_real_T(double result[192]);
static void argInit_26x26_real_T(double result[676]);
static void argInit_2x1_real_T(double result[2]);
static void argInit_6x4_real_T(double result[24]);
static void argInit_7x1_real_T(double result[7]);
static double argInit_real_T(void);
static void main_pseudoAlgorithm(void);

/* Function Definitions */

/*
 * Arguments    : double result[48]
 * Return Type  : void
 */
static void argInit_24x2_real_T(double result[48])
{
  int idx0;
  int idx1;

  /* Loop over the array to initialize each element. */
  for (idx0 = 0; idx0 < 24; idx0++) {
    for (idx1 = 0; idx1 < 2; idx1++) {
      /* Set the value of the array element.
         Change this value to the value that the application requires. */
      result[idx0 + 24 * idx1] = argInit_real_T();
    }
  }
}

/*
 * Arguments    : double result[192]
 * Return Type  : void
 */
static void argInit_24x8_real_T(double result[192])
{
  int idx0;
  int idx1;

  /* Loop over the array to initialize each element. */
  for (idx0 = 0; idx0 < 24; idx0++) {
    for (idx1 = 0; idx1 < 8; idx1++) {
      /* Set the value of the array element.
         Change this value to the value that the application requires. */
      result[idx0 + 24 * idx1] = argInit_real_T();
    }
  }
}

/*
 * Arguments    : double result[676]
 * Return Type  : void
 */
static void argInit_26x26_real_T(double result[676])
{
  int idx0;
  int idx1;

  /* Loop over the array to initialize each element. */
  for (idx0 = 0; idx0 < 26; idx0++) {
    for (idx1 = 0; idx1 < 26; idx1++) {
      /* Set the value of the array element.
         Change this value to the value that the application requires. */
      result[idx0 + 26 * idx1] = argInit_real_T();
    }
  }
}

/*
 * Arguments    : double result[2]
 * Return Type  : void
 */
static void argInit_2x1_real_T(double result[2])
{
  int idx0;

  /* Loop over the array to initialize each element. */
  for (idx0 = 0; idx0 < 2; idx0++) {
    /* Set the value of the array element.
       Change this value to the value that the application requires. */
    result[idx0] = argInit_real_T();
  }
}

/*
 * Arguments    : double result[24]
 * Return Type  : void
 */
static void argInit_6x4_real_T(double result[24])
{
  int idx0;
  int idx1;

  /* Loop over the array to initialize each element. */
  for (idx0 = 0; idx0 < 6; idx0++) {
    for (idx1 = 0; idx1 < 4; idx1++) {
      /* Set the value of the array element.
         Change this value to the value that the application requires. */
      result[idx0 + 6 * idx1] = argInit_real_T();
    }
  }
}

/*
 * Arguments    : double result[7]
 * Return Type  : void
 */
static void argInit_7x1_real_T(double result[7])
{
  int idx0;

  /* Loop over the array to initialize each element. */
  for (idx0 = 0; idx0 < 7; idx0++) {
    /* Set the value of the array element.
       Change this value to the value that the application requires. */
    result[idx0] = argInit_real_T();
  }
}

/*
 * Arguments    : void
 * Return Type  : double
 */
static double argInit_real_T(void)
{
  return 0.0;
}

/*
 * Arguments    : void
 * Return Type  : void
 */
static void main_pseudoAlgorithm(void)
{
  emxArray_real_T *good;
  emxArray_real_T *goodfit;
  emxArray_real_T *meh;
  double dv0[24];
  double dv1[2];
  double dv2[192];
  double dv3[7];
  double dv4[48];
  double dv5[48];
  double dv6[676];
  emxInitArray_real_T(&good, 3);
  emxInitArray_real_T(&goodfit, 2);
  emxInitArray_real_T(&meh, 3);

  /* Initialize function 'pseudoAlgorithm' input arguments. */
  /* Initialize function input argument 'kdBruhns'. */
  /* Initialize function input argument 'tnpbsa'. */
  /* Initialize function input argument 'mfiAdjMean'. */
  /* Initialize function input argument 'best'. */
  /* Initialize function input argument 'meanPerCond'. */
  /* Initialize function input argument 'stdPerCond'. */
  /* Initialize function input argument 'biCoefMat'. */
  /* Call the entry-point 'pseudoAlgorithm'. */
  argInit_6x4_real_T(dv0);
  argInit_2x1_real_T(dv1);
  argInit_24x8_real_T(dv2);
  argInit_7x1_real_T(dv3);
  argInit_24x2_real_T(dv4);
  argInit_24x2_real_T(dv5);
  argInit_26x26_real_T(dv6);
  pseudoAlgorithm(argInit_real_T(), argInit_real_T(), argInit_real_T(), dv0, dv1,
                  dv2, dv3, dv4, dv5, dv6, good, goodfit, meh);
  emxDestroyArray_real_T(meh);
  emxDestroyArray_real_T(goodfit);
  emxDestroyArray_real_T(good);
}

/*
 * Arguments    : int argc
 *                const char * const argv[]
 * Return Type  : int
 */
int main(int argc, const char * const argv[])
{
  (void)argc;
  (void)argv;

  /* Initialize the application.
     You do not need to do this more than one time. */
  pseudoAlgorithm_initialize();

  /* Invoke the entry-point functions.
     You can call entry-point functions multiple times. */
  main_pseudoAlgorithm();

  /* Terminate the application.
     You do not need to do this more than one time. */
  pseudoAlgorithm_terminate();
  return 0;
}

/*
 * File trailer for main.c
 *
 * [EOF]
 */