#ifndef _RICE_COMP_H_
#define _RICE_COMP_H_


/**
 * @file ricecomp.h
 * @brief Actual RICE compression code from cfitsio
 */


#ifdef __cplusplus
extern "C" {
#endif

int fits_rcomp_short(
      short a[],        /* input array          */
      int nx,       /* number of input pixels   */
      unsigned char *c, /* output buffer        */
      int clen,     /* max length of output     */
      int nblock);       /* coding block size        */


int fits_rdecomp_short (unsigned char *c,       /* input buffer         */
         int clen,          /* length of input      */
         unsigned short array[],    /* output array         */
         int nx,            /* number of output pixels  */
         int nblock);        /* coding block size        */


#ifdef __cplusplus
}; //extern C
#endif

#endif
