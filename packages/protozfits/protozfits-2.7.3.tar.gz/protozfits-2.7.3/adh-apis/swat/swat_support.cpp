/*
 * swat_support.c
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

#include "swat_support.h"

#include "swat_api.h"
#include "swat_defs.h"
#include "swat_errors.h"

#include <errno.h>
#include <fcntl.h>
#include <math.h>
#include <netinet/tcp.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/epoll.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <unistd.h>

/*****************************************************************************/
/*  Function :     swat_io_hangup                                            */
/*                                                                           */
/*  Description:   check for hangup on socket connection                     */
/*                                                                           */
/*  Return code:   SWAT_ERR_OK - no hangup, SWAT_ERR_SOCKET_HANGUP - hangup  */
/*                                                                           */
/*  Parameter arguments:                                                     */
/*                                                                           */
/*  name        I/O     valid range      description                         */
/*                                                                           */
/*  h           input                    socket on which hangup is checked   */
/*                                                                           */
/*****************************************************************************/

int swat_io_hangup(int h) {
    struct pollfd pfd;
    char c;

    pfd.fd = h; /* we want to test whether hangup occured on socket, this is __REALLY__
                   tricky */
    pfd.events = POLLIN;
    pfd.revents = 0;

    if (poll(&pfd, 1, 0) >=
        0) /* we have to poll, if error assume nothing occured ... */
    {
        if (pfd.revents & POLLHUP) /* if POLLHUP than hangup occured, unfortunately this
                                      is usually not set */
            return (SWAT_ERR_SOCKET_HANGUP);

        if (pfd.revents & POLLIN) /* if hangup occurs usually POLLIN is set and subseq.
                                     read returns 0 bytes avail */
        {
            if (0 == read(h, &c, 1)) /* Who has designed this stuff ???? */
                return (SWAT_ERR_SOCKET_HANGUP);
        }
    }

    return (SWAT_OK);
}

/*****************************************************************************/
/*  Function :     swat_io_write                                             */
/*                                                                           */
/*  Description:   write n bytes to the socket (or any device)               */
/*                                                                           */
/*  Return code:   SWAT_ERR_OK - all data written, other - some error code   */
/*                                                                           */
/*  Parameter arguments:                                                     */
/*                                                                           */
/*  name        I/O     valid range      description                         */
/*                                                                           */
/*  h           input                    socket (writable)                   */
/*  p           input                    data pointer                        */
/*  nbytes      input/output             how many bytes to write/written     */
/*  exit_signal input                    pointer to state control variable   */
/*                                                                           */
/*****************************************************************************/

int swat_io_write(int h, void* p, int* nbytes, int* exit_signal) {
    int r, total;

    if (NULL == p) return (SWAT_ERR_NUL_PTR);
    if (NULL == nbytes) return (SWAT_ERR_NUL_PTR);

    total = *nbytes;
    for ((*nbytes) = 0; (*nbytes) < total;) {
        if (NULL != exit_signal)
            if (*exit_signal) return (SWAT_ERR_EXITING);
        r = write(h, ((char*)p) + (*nbytes), (size_t)(total - (*nbytes)));
        if (-1 == r) {
            r = errno;
            if (EINTR == r) continue; /* signal caught but we ignore it ... */
            if (EAGAIN == r)
                return (SWAT_ERR_NO_NEW_DATA); /* socket nonblocking, but waiting
                                                  condition */
            return (SWAT_ERR_WRITE_FAILED); /* something else, must be system error */
        } else
            (*nbytes) += r; /* accumulate number of bytes written so far .. */
    }

    return (SWAT_OK);
}

/*****************************************************************************/
/*  Function :     swat_io_read                                              */
/*                                                                           */
/*  Description:   read n bytes from the socket (or any device)              */
/*                                                                           */
/*  Return code:   SWAT_ERR_OK - all data read, other - some error code      */
/*                                                                           */
/*  Parameter arguments:                                                     */
/*                                                                           */
/*  name        I/O     valid range      description                         */
/*                                                                           */
/*  h           input                    socket (readable)                   */
/*  p           input                    data pointer                        */
/*  nbytes      input/output             how many bytes to read / read       */
/*  exit_signal input                    pointer to state control variable   */
/*                                                                           */
/*****************************************************************************/

int swat_io_read(int h, void* p, int* nbytes, int* exit_signal) {
    int r, total;

    if (NULL == p) return (SWAT_ERR_NUL_PTR);
    if (NULL == nbytes) return (SWAT_ERR_NUL_PTR);

    total = *nbytes;
    for ((*nbytes) = 0; (*nbytes) < total;) {
        if (NULL != exit_signal)
            if (*exit_signal) return (SWAT_ERR_EXITING);
        r = read(h, ((char*)p) + (*nbytes), (size_t)(total - (*nbytes)));
        if (0 == r) {
            if (SWAT_OK != (r = swat_io_hangup(h))) return (r);
            return (SWAT_ERR_READ_FAILED);
        }
        if (-1 == r) {
            r = errno;
            if (EINTR == r) continue; /* signal caught but we ignore it ... */
            if (EAGAIN == r)
                return (SWAT_ERR_NO_NEW_DATA); /* socket nonblocking, but waiting
                                                  condition */
            return (SWAT_ERR_READ_FAILED); /* something else, must be system error */
        } else
            (*nbytes) += r; /* accumulate number of bytes written so far .. */
    }

    return (SWAT_OK);
}

// set socket to non-blocking mode
int swat_io_setnonblock(int h) {
    int r;

    r = fcntl(h, F_GETFL);  // get socket mode
    if (r < 0) return (r);

    r = fcntl(h, F_SETFL, O_NONBLOCK | r);  // set socket non-blocking
    return (r);
}

// set socket to non-blocking mode
int swat_io_setblock(int h) {
    int r;

    r = fcntl(h, F_GETFL);  // get socket mode
    if (r < 0) return (r);

    r = fcntl(h, F_SETFL, (~O_NONBLOCK) & r);  // set socket blocking
    return (r);
}

#ifndef TCP_USER_TIMEOUT
#define TCP_USER_TIMEOUT (18)
#endif

// enable KEEPALIVE on a socket (with custom settings)
int swat_io_setkeepalive(int h, int kaflag, int kacnt, int kaidle, int kaintvl,
                         int timeout_ms) {
    int r;
    int optval, optlen;

    if (kaflag) {
        if ((kacnt < 0) || (kaidle < 0) || (kaintvl < 0)) return (SWAT_ERR_BAD_ARG);
    }
    if (timeout_ms < 0) return (SWAT_ERR_BAD_ARG);

    optval = (kaflag ? 1 : 0);  // Set the KEEPALIVE option
    optlen = sizeof(optval);
    r = setsockopt(h, SOL_SOCKET, SO_KEEPALIVE, &optval, optlen);
    if (r < 0) return (r);

    if (kaflag & (kacnt > 0)) {
        optval = kacnt;  // 5 missing probes
        optlen = sizeof(optval);
        r = setsockopt(h, SOL_TCP, TCP_KEEPCNT, &optval, optlen);
        if (r < 0) return (r);
    }

    if (kaflag & (kaidle > 0)) {
        optval = kaidle;  // interval between subsequent keepalive probes
        optlen = sizeof(optval);
        r = setsockopt(h, SOL_TCP, TCP_KEEPIDLE, &optval, optlen);
        if (r < 0) return (r);
    }

    if (kaflag & (kaintvl > 0)) {
        optval = kaintvl;  // time from the last data packet sent and 1st probe
        optlen = sizeof(optval);
        r = setsockopt(h, SOL_TCP, TCP_KEEPINTVL, &optval, optlen);
    }

    if (timeout_ms > 0) {
        optval =
            timeout_ms;  // userland max delay in millisecs (overrides keepalive params)
        optlen = sizeof(optval);
        r = setsockopt(h, SOL_TCP, TCP_USER_TIMEOUT, &optval, optlen);
    }

    return (r);
}

int swat_ip4addr2str(unsigned long a, char* s) {
    if (NULL == s) return (SWAT_ERR_NUL_PTR);
    sprintf(s, "%d.%d.%d.%d", (int)((a >> 24) & 0xFF), (int)((a >> 16) & 0xFF),
            (int)((a >> 8) & 0xFF), (int)(a & 0xFF));
    return (SWAT_OK);
}

/* convert string to IP4 address (as integer).
   Returns 0 on error
*/

int swat_str2ip4addr(const char* s) {
    int a, b, c, d;
    if (NULL == s) return (0);
    if (4 != sscanf(s, "%d.%d.%d.%d", &a, &b, &c, &d)) return (0);
    return ((a << 24) + (b << 16) + (c << 8) + d);
}

int swat_str2clntflags(const char* s, int* send_flag, int* recv_flag, int* sort_flag) {
    int snd, rcv, srt;

    snd = rcv = srt = 1;  // defaults
    if (NULL != s) {
        for (; *s; s++) {
            switch (*s) {
                case 'o':
                    srt = 0;
                    break;
                case 'O':
                    srt = 1;
                    break;
                case 'r':
                    rcv = 0;
                    break;
                case 'R':
                    rcv = 1;
                    break;
                case 's':
                    snd = 0;
                    break;
                case 'S':
                    snd = 1;
                    break;
            }
        }
    }

    if (NULL != sort_flag) *sort_flag = srt;
    if (NULL != recv_flag) *recv_flag = rcv;
    if (NULL != send_flag) *send_flag = snd;

    return (SWAT_OK);
}

int swat_get_current_utc(UTC_TIME* utc) /* days from 01.Jan.1958 plus millisec of day */
{
    struct timeval mytv;
    struct tm tm;
    time_t sec;

    if (NULL == utc) return (SWAT_ERR_NUL_PTR);

    if (gettimeofday(&mytv, NULL)) return (SWAT_ERR_BAD_ARG);
    sec = mytv.tv_sec;
    if (NULL == (gmtime_r(&sec, &tm))) return (SWAT_ERR_BAD_ARG);
    utc->year = tm.tm_year + 1900;
    utc->month = tm.tm_mon;     // range  : 0 -- 11 (0 - January, 11 - December)
    utc->day = tm.tm_mday - 1;  // range  : 0 -- 30 (30 means its 31th of i.e. May)
    utc->hour = tm.tm_hour;     // range  : 0 -- 23
    utc->min = tm.tm_min;       // range  : 0 -- 59
    utc->sec = tm.tm_sec;
    utc->usec = mytv.tv_usec;
    return (SWAT_OK);
}

/* get seconds since epoch */

time_t swat_gettime(void) { return (time(NULL)); }

/* get ticks since epoch, resolution as per posix is 1 microsec, actual may be less
   Returns:
     0 - on error (really unlikely ...)
*/

SWAT_R1_HIGH_RES_TIMESTAMP swat_gettimeofday(void) {
    struct timeval tv;

    if (0 != gettimeofday(&tv, NULL)) return ((SWAT_R1_HIGH_RES_TIMESTAMP)0);
    return ((SWAT_R1_HIGH_RES_TIMESTAMP)(tv.tv_sec * SWAT_API_S_TIME_T_TICKS +
                                         tv.tv_usec * SWAT_API_US_TIME_T_TICKS));
}

int swat_sleep(int sec, int nsec) {
    struct timespec rqtp;

    rqtp.tv_sec = sec;
    rqtp.tv_nsec = nsec;
    return (nanosleep(&rqtp, NULL));
}

int swat_ticks_sleep(SWAT_R1_HIGH_RES_TIMESTAMP ticks_to_sleep) {
    struct timespec rqtp;

    rqtp.tv_sec = (time_t)(ticks_to_sleep / SWAT_API_S_TIME_T_TICKS);
    rqtp.tv_nsec =
        (long)((ticks_to_sleep % SWAT_API_S_TIME_T_TICKS) / SWAT_API_NS_TIME_T_TICKS);
    return (nanosleep(&rqtp, NULL));
}

int swat_snooze(void) { return (swat_sleep(0, SWAT_SNOOZE_DURATION_NSEC)); }

double swat_poisson_delay(double poirate) { return (-log(drand48()) / poirate); }

SWAT_CLK_CALIB swat_clk_calib;

/*****************************************************************************/
/*  Function :     swat_get_tai_time                                         */
/*                                                                           */
/*  Description:   compute current TAI time                                  */
/*                                                                           */
/*  Return code:   current TAI time (in SWAT_R1_HIGH_RES_TIMESTAMP units), on error
 * ZERO.   */
/*                                                                           */
/*  Parameter arguments:                                                     */
/*                                                                           */
/*  name        I/O     valid range      description                         */
/*                                                                           */
/*****************************************************************************/

SWAT_R1_HIGH_RES_TIMESTAMP swat_get_tai_time(void) {
    struct timespec ts;

    if (0 == swat_clk_calib.initflag)
        return ((SWAT_R1_HIGH_RES_TIMESTAMP)0);  // not intialized (yet)
    if (0 != clock_gettime(CLOCK_MONOTONIC, &ts))
        return ((SWAT_R1_HIGH_RES_TIMESTAMP)0);  // return zero on error

    return ((SWAT_R1_HIGH_RES_TIMESTAMP)(
        SWAT_API_S_TIME_T_TICKS * ts.tv_sec      // monotonic clock seconds
        + SWAT_API_NS_TIME_T_TICKS * ts.tv_nsec  // nanoseconds
        + swat_clk_calib.offset));  // add offset (computed by calibrate_mono_clock())
}

/*****************************************************************************/
/*  Function :     swat_tai_clock_valid                                      */
/*                                                                           */
/*  Description:   verify kernel's CLOCK_TAI is fully calibrated             */
/*                                                                           */
/*  Return code:   SWAT_OK - calibrated, otherwise - some error code         */
/*                                                                           */
/*  Parameter arguments:                                                     */
/*                                                                           */
/*  name        I/O     valid range      description                         */
/*                                                                           */
/*  leapseconds output                   *int holding TAI-UTC (leap seconds) */
/*                                                                           */
/*****************************************************************************/

/* the function checks whether :
 *     1) CLOCK_TAI is supported by kernel (3.10+) and glibc
 *     2) kernel's TAI clock is __properly calibrated (i.e. by NTP)
 *        if CLOCK_TAI readout is the same as CLOCK_REALTIME
 *        then clock TAI is NOT valid/supported !
 *  the function returns current number of leap seconds (TAI-UTC)
 *  valid at the time the function terminates.
 *  the function carefully avoids leap second period (it sleeps up to 4s)
 *
 *  In order to properly calibrate CLOCK_TAI kernel clock it is necessary to :
 *
 *     *) run 3.10+ Linux kernel (i.e. Centos 7, SL7)
 *     *) add to /etc/ntp.conf line: leapfile VALID_LEAPSEC_FILE
 *     *) have at least half-decent version of ntpd (4.2.8+) running all the time
 *     *) regularly update VALID_LEAPSEC_FILE (i.e. cron job)
 *
 *  For more information see :
 *
 *     https://stackoverflow.com/questions/29361964/how-to-add-a-leap-second-file-table-in-an-ntp-server
 *     https://askubuntu.com/questions/675622/why-clock-tai-and-clock-realtime-returns-the-same-value
 *
 */

int swat_tai_clock_valid(int* leapsecs) {
    time_t ttai, tprev, tnext;
    UTC_TIME utc;
    struct timespec ts;
    int r, ls;

    r = clock_gettime(CLOCK_REALTIME, &ts);
    if (r) return (SWAT_ERR_GETTIME_FAILED);
    tprev = ts.tv_sec;
    //
    for (;; tnext = tprev) {
        if (SWAT_OK != (r = swat_get_current_utc(&utc))) return (r);
        if (((5 == utc.month) && (29 == utc.day))       // Jun 30th
            || ((11 == utc.month) && (30 == utc.day)))  // Dec 31th
        {
            if ((23 == utc.hour) && (59 == utc.min) &&
                (utc.sec >= 58))  // we are <=2s before leap second
            {
                swat_sleep(62 - utc.sec, 0);  // we sleep until at least 1s after end of
                                              // leap second (up to 4s max)
                continue;  // have to repeat (in case a signal was delivered)
            }
        }  // if we have slept ==> tprev != tnext, so next iteration is assured
        r = clock_gettime(CLOCK_TAI, &ts);
        if (r) return (SWAT_ERR_GETTIME_FAILED);
        ttai = ts.tv_sec;

        // we call REALTIME clock twice (in case we crossed second boundary by chance
        // and/or slept)
        r = clock_gettime(CLOCK_REALTIME, &ts);
        if (r) return (SWAT_ERR_GETTIME_FAILED);
        tnext = ts.tv_sec;
        if (tprev == tnext) break;  // didn't cross second's bndry, so we'are done
    }

    // if ttai equals either tprev or tnext the kernel's TAI clock is not properly
    // calibrated if ((tprev == ttai) || (ttai == tnext))
    // return(SWAT_ERR_TAI_NOT_VALID); compute time distance between TAI and UTC
    ls = (int)(ttai - tprev);
    // during runtime we may accrue new leapsecond (at most every 6 month),
    // so any value of : -1, 0, 1 means TAI clock is __NOT__ properly
    // calibrated by Linux kernel (the code requires that machine is rebooted
    // before 2nd leap second since its boottime)
    if ((ls >= -1) && (ls <= 1)) return (SWAT_ERR_TAI_NOT_VALID);
    if (NULL != leapsecs) *leapsecs = ls;
    return (SWAT_OK);
}

/*****************************************************************************/
/*  Function :     swat_calibrate_mono_clock                                 */
/*                                                                           */
/*  Description:   calibrate kernel's MONOTONIC clock calibrated             */
/*                 The function computes offset between given clock type     */
/*                 (CLOCK_TAI/CLOCK_REALTIME) and CLOCK_MONOTONIC            */
/*                 Calibration information is stored in static struct        */
/*                 SWAT_CLK_CALIB swat_clk_calib (only if retcode==SWAT_OK)  */
/*                 DEPRECATED FUNCTION - use swat_clock_calibrate() instead  */
/*                                                                           */
/*  Return code:   SWAT_OK - calibrated, otherwise - some error code         */
/*                                                                           */
/*  Parameter arguments:                                                     */
/*                                                                           */
/*  name         I/O     valid range   description                           */
/*                                                                           */
/*  clktype      input   0 -- 11       type of reference clock               */
/*  leapsecs     input                 adjust computed offset by this leaps  */
/*  maxjitter    input                 max allowable jitter                  */
/*  calib_offset output                computed calibration value, NULL OK   */
/*  calib_accy   output                accuracy of calibration, NULL is OK   */
/*                                                                           */
/*****************************************************************************/

/* clktype should be :
 *      preferred  --> CLOCK_TAI (11) if kernel supports and NTP calibrates
 *      compatible --> CLOCK_REALTIME (0) (because CLOCK_TAI is __NOT__ supported by SL6
 * !)
 *
 * WARNING: CLOCK_REALTIME requires that the number of leap seconds is known
 *          from some other source (config file or ACS's CDB).
 *          The good news is that SWAT properly works __during__ leap second interval.
 * NOTE:    when using CLOCK_TAI, number of leap seconds passed as arg should be ZERO
 */

int swat_calibrate_mono_clock(int clktype, int leapsecs,
                              SWAT_R1_HIGH_RES_TIMESTAMP maxjitter,
                              SWAT_R1_HIGH_RES_TIMESTAMP* calib_offset,
                              SWAT_R1_HIGH_RES_TIMESTAMP* calib_accy) {
    SWAT_R1_HIGH_RES_TIMESTAMP rdout_rt[SWAT_CLK_CALIB_NREADOUTS],
        rdout_mono[SWAT_CLK_CALIB_NREADOUTS];
    SWAT_R1_HIGH_RES_TIMESTAMP maxdt_rt, maxdt_mono, my_accy, my_offset;
    struct timespec ts;
    int i, r;

    for (i = 0; i < SWAT_CLK_CALIB_NREADOUTS;
         i++) {  // perform precise time measurements required number of times
        r = clock_gettime(clktype, &ts);
        if (r) return (SWAT_ERR_GETTIME_FAILED);
        rdout_rt[i] =
            SWAT_API_S_TIME_T_TICKS * ts.tv_sec + SWAT_API_NS_TIME_T_TICKS * ts.tv_nsec;

        r = clock_gettime(CLOCK_MONOTONIC, &ts);
        if (r) return (SWAT_ERR_GETTIME_FAILED);
        rdout_mono[i] =
            SWAT_API_S_TIME_T_TICKS * ts.tv_sec + SWAT_API_NS_TIME_T_TICKS * ts.tv_nsec;
    }
    // check whether sampling jitter is too high (usually it is below 1 microsec for
    // precise clocks)
    maxdt_rt = maxdt_mono = 0;
    for (i = 1; i < SWAT_CLK_CALIB_NREADOUTS; i++) {
        if ((rdout_rt[i] - rdout_rt[i - 1]) > maxdt_rt)
            maxdt_rt = rdout_rt[i] - rdout_rt[i - 1];
        if ((rdout_mono[i] - rdout_mono[i - 1]) > maxdt_mono)
            maxdt_mono = rdout_mono[i] - rdout_mono[i - 1];
    }
    my_accy = maxdt_rt + maxdt_mono;
    if (my_accy > maxjitter) return (SWAT_ERR_CANNOT_CALIBRATE);

    // finally compute precise time calibration (it is off by 1/2 of sampling period but
    // who cares ...)
    my_offset = 0;
    for (i = 0; i < SWAT_CLK_CALIB_NREADOUTS; i++)
        my_offset += (rdout_rt[i] - rdout_mono[i]) / SWAT_CLK_CALIB_NREADOUTS;
    my_offset += leapsecs * SWAT_API_S_TIME_T_TICKS;
    swat_clk_calib.offset = my_offset;
    if (NULL != calib_offset) *calib_offset = my_offset;
    swat_clk_calib.accy = my_accy;
    if (NULL != calib_accy) *calib_accy = my_accy;
    swat_clk_calib.clktype = clktype;
    swat_clk_calib.leapsecs = leapsecs;
    swat_clk_calib.initflag = 1;  // signal that valid data is available

    return (SWAT_OK);
}

int swat_clock_calibrate(int clktype, int leapsecs,
                         SWAT_R1_HIGH_RES_TIMESTAMP maxjitter, SWAT_CLK_CALIB* calib) {
    int r;

    r = swat_calibrate_mono_clock(clktype, leapsecs, maxjitter, NULL, NULL);
    if (SWAT_OK == r)
        if (NULL != calib) *calib = swat_clk_calib;
    return (r);
}
