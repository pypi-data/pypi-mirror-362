/*
 * swat_support.h
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

#ifndef SWAT_SUPPORT_H
#define SWAT_SUPPORT_H

#include "swat_defs.h"

#include <time.h>

#ifdef __cplusplus
extern "C" {
#endif

// 50 millisec interval
#define SWAT_SNOOZE_DURATION_USEC (50000)
#define SWAT_SNOOZE_DURATION_NSEC (1000 * SWAT_SNOOZE_DURATION_USEC)

// min length for 2nd arg to swat_ip4addr2str()
#define SWAT_IP4ADDR_STR_SIZE (50)

#ifndef CLOCK_TAI
#define CLOCK_TAI (11)
#endif

#define SWAT_CLK_CALIB_NREADOUTS (10)

typedef struct UTC_TIME_STRUCT {
    int year;  /* 1972 - 2000(+) */
    int month; /* 0 - 11 */
    int day;   /* 0 - 28/29/30/31 */
    int hour;  /* 0 - 23 */
    int min;   /* 0 - 59 */
    int sec;   /* 0 - 59/60/61 */
    int usec;  /* 0 - 999999 */
} UTC_TIME;

typedef struct SWAT_CLK_CALIB_STRUCT {
    SWAT_R1_HIGH_RES_TIMESTAMP
    offset;  // offset: TAI - kernel's CLOCK_MONOTONIC clock (includes leap seconds)
    SWAT_R1_HIGH_RES_TIMESTAMP accy;  // accuracy of offset calibration
    int clktype;   // type/id of kernel's clock (neg value - not initialized)
    int leapsecs;  // number of leap seconds (TAI-UTC offset)
    int initflag;  // 0: not initialized, non-zero: structure contains valid data
} SWAT_CLK_CALIB;

extern SWAT_CLK_CALIB swat_clk_calib;

int swat_io_hangup(int h);
int swat_io_write(int h, void* p, int* nbytes, int* exit_signal);
int swat_io_read(int h, void* p, int* nbytes, int* exit_signal);
int swat_io_setnonblock(int h);
int swat_io_setblock(int h);
int swat_io_setkeepalive(int h, int kaflag, int kacnt, int kaidle, int kaintvl,
                         int timeout_ms);

int swat_ip4addr2str(unsigned long a, char* s);
int swat_str2ip4addr(const char* s);
int swat_str2clntflags(const char* s, int* send_flag, int* recv_flag, int* sort_flag);

int swat_get_current_utc(UTC_TIME* utc);

time_t swat_gettime(void);
SWAT_R1_HIGH_RES_TIMESTAMP swat_gettimeofday(void);
int swat_sleep(int sec, int nsec);
int swat_ticks_sleep(SWAT_R1_HIGH_RES_TIMESTAMP ticks_to_sleep);
int swat_snooze(void);
double swat_poisson_delay(double poirate);
SWAT_R1_HIGH_RES_TIMESTAMP swat_get_tai_time(void);
int swat_tai_clock_valid(int* leapsecs);
int swat_calibrate_mono_clock(int clktype, int leapsecs,
                              SWAT_R1_HIGH_RES_TIMESTAMP maxjitter,
                              SWAT_R1_HIGH_RES_TIMESTAMP* calib_offset,
                              SWAT_R1_HIGH_RES_TIMESTAMP* calib_accy);
int swat_clock_calibrate(int clktype, int leapsecs,
                         SWAT_R1_HIGH_RES_TIMESTAMP maxjitter, SWAT_CLK_CALIB* calib);

#ifdef __cplusplus
}
#endif

#endif /* SWAT_SUPPORT_H */
