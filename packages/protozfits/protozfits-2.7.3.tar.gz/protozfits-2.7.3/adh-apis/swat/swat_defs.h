/*
 * swat_defs.h
 *
 * Copyright 2019 Jerzy Borkowski/CAMK <jubork@ncac.torun.pl>
 *
 * The 3-Clause BSD License
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1.  Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 *
 * 2.  Redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution.
 *
 * 3.  Neither the name of the copyright holder nor the names of its
 * contributors may be used to endorse or promote products derived from this
 * software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef SWAT_DEFS_H
#define SWAT_DEFS_H

#include <stdint.h>

/* varia - from other files - probably to rename / move somewhere else */

/* early definitions needed for proper namespace bootstrap */

#define SWAT_INVALID_HANDLE (-1)

// typedef unsigned char		byte;                           /* fundamental
// data type */

/* unit is 1/4 ns. */
/*
#if ( 0 != SWAT_32BIT_ARCH )
typedef unsigned long long              SWAT_R1_HIGH_RES_TIMESTAMP;
#else
typedef unsigned long			SWAT_R1_HIGH_RES_TIMESTAMP;
#endif
*/
struct SWAT_R1_HIGH_RES_TIMESTAMP {
    uint32_t s = 0;
    uint32_t qns = 0;

    SWAT_R1_HIGH_RES_TIMESTAMP() = default;
    SWAT_R1_HIGH_RES_TIMESTAMP(unsigned long time)
        : s(time / 4000000000), qns(time % 4000000000) {}
    operator long int() const { return s * 4000000000 + qns; }
    SWAT_R1_HIGH_RES_TIMESTAMP& operator+=(const SWAT_R1_HIGH_RES_TIMESTAMP& right) {
        *this = static_cast<unsigned long>(*this) + static_cast<unsigned long>(right);
        return *this;
    }
};

/* raw readout value from PMTs */
typedef unsigned short swat_pmtval_t;

#endif /* SWAT_DEFS_H */
