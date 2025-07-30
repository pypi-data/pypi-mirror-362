/*
 * swat_api.h
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

#ifndef SWAT_API_H
#define SWAT_API_H

#include "swat_defs.h"
#include "swat_errors.h"
#include "swat_packet.h"
#include "swat_support.h"

#include <arpa/inet.h>
#include <pthread.h>
#include <sys/epoll.h>

#ifdef __cplusplus
extern "C" {
#endif

// single message (SWAT packet) max size in bytes
#define SWAT_API_PKT_MAXLEN (200000)
#define SWAT_API_CAMEVS_MAXLEN \
    ((int)((SWAT_API_PKT_MAXLEN / sizeof(SWAT_PACKET_R1_TRIGGER) / 4) - 5))
#define SWAT_API_ARREVS_MAXLEN \
    ((int)(2 * SWAT_API_PKT_MAXLEN / sizeof(SWAT_PACKET_R1_EVENT_REQUEST)))

// maximum number of telescopes supported
#if (0 != SWAT_32BIT_ARCH)
#define SWAT_API_MAXTELS (10)
#else
#define SWAT_API_MAXTELS (100)
#endif

#define SWAT_API_MAXTELTYPES (3)

#define SWAT_API_INVALID_HANDLE (-1)

// various time related constants
#define SWAT_API_NS_TIME_T_TICKS ((SWAT_R1_HIGH_RES_TIMESTAMP)(4L))
#define SWAT_API_US_TIME_T_TICKS \
    ((SWAT_R1_HIGH_RES_TIMESTAMP)(SWAT_API_NS_TIME_T_TICKS * 1000L))
#define SWAT_API_MS_TIME_T_TICKS \
    ((SWAT_R1_HIGH_RES_TIMESTAMP)(SWAT_API_US_TIME_T_TICKS * 1000L))
#define SWAT_API_S_TIME_T_TICKS \
    ((SWAT_R1_HIGH_RES_TIMESTAMP)(SWAT_API_MS_TIME_T_TICKS * 1000L))
#define SWAT_API_TBINSIZE (50 * SWAT_API_MS_TIME_T_TICKS)
#define SWAT_API_CONNECT_TIMEOUT (2 * SWAT_API_S_TIME_T_TICKS)
#define SWAT_API_MS_TIME_FLOAT_3(x) \
    ((((SWAT_R1_HIGH_RES_TIMESTAMP)x) / SWAT_API_MS_TIME_T_TICKS) / 1000.0)

// States of the API
// after creation
#define SWAT_API_STATE_INIT (0)
// connection is being attempted
#define SWAT_API_STATE_CONNECTING (1)
// connection is established
#define SWAT_API_STATE_ESTABLISHED (2)
// connect() timeouted/aborted
#define SWAT_API_STATE_ABORTED (3)
// socket closed by peer
#define SWAT_API_STATE_HANGUP (4)
// socket closed by the application
#define SWAT_API_STATE_CLOSED (5)
// socket connection refused by peer
#define SWAT_API_STATE_REFUSED (6)

#define SWAT_API_EVENT_NULL (0)
#define SWAT_API_EVENT_ERROR (0x1)
#define SWAT_API_EVENT_CONNECT (0x2)
#define SWAT_API_EVENT_ESTABLISHED (0x4)
#define SWAT_API_EVENT_ABORT (0x8)
#define SWAT_API_EVENT_HANGUP (0x10)
#define SWAT_API_EVENT_CLOSE (0x20)
#define SWAT_API_EVENT_REFUSED (0x40)
#define SWAT_API_EVENT_CONFIGURE (0x80)
#define SWAT_API_EVENT_UNCONFIG (0x100)
#define SWAT_API_EVENT_WRKR_START (0x200)
#define SWAT_API_EVENT_WRKR_STOP (0x400)

#define SWAT_API_STATE_NULL (0)
#define SWAT_API_STATE_PKTHDR (1)
#define SWAT_API_STATE_PKTPAYLOAD (2)
#define SWAT_API_STATE_PKTACCEPT (3)

#define SWAT_API_READER_EVENTS (EPOLLIN | EPOLLHUP | EPOLLERR | EPOLLRDHUP)
#define SWAT_API_WRITER_EVENTS (EPOLLIN | EPOLLOUT | EPOLLHUP | EPOLLERR | EPOLLRDHUP)

#define SWAT_API_MAXWRBUFITEMS (50)

// Values used to configure printed types of debugging messages
#define SWAT_API_DEBUG_ALL (0xFFFF)
#define SWAT_API_DEBUG_CAMEV (0x1)
#define SWAT_API_DEBUG_ARREV_POS (0x2)
#define SWAT_API_DEBUG_ARREV_NEG (0x4)
#define SWAT_API_DEBUG_PKTHDR (0x8)
#define SWAT_API_DEBUG_CLOCK (0x10)
#define SWAT_API_DEBUG_EVENT (0x20)
#define SWAT_API_DEBUG_EPOLL (0x40)
#define SWAT_API_DEBUG_ERRORS (0x80)
#define SWAT_API_DEBUG_TEST_DUPKTS (0x100)
#define SWAT_API_DEBUG_TEST_RECONN (0x200)
#define SWAT_API_DEBUG_TEST_STUCK (0x400)
#define SWAT_API_DEBUG_SIGNALS (0x800)
#define SWAT_API_DEBUG_READER (0x1000)
#define SWAT_API_DEBUG_DISPATCHER (0x2000)
#define SWAT_API_DEBUG_DATA_READER (0x4000)
#define SWAT_API_DEBUG_DATA_WRITER (0x8000)
#define SWAT_API_DEBUG_FINAL_REPORT (0x10000)
#define SWAT_API_DEBUG_CONTROL (0x20000)
#define SWAT_API_DEBUG_CONFIG (0x40000)
#define SWAT_API_DEBUG_DATASTREAM (0x80000)

// Logger function setup constants
#define SWAT_API_LOGGER_DISABLED ((int (*)(int, char*))0)
#define SWAT_API_LOGGER_DEFAULT ((int (*)(int, char*))1)

#define SWAT_API_LOGGER_MAX_MSG (10000)

// Logger message types
#define SWAT_API_LOG_INFO (1)
#define SWAT_API_LOG_DEBUG (10004)
#define SWAT_API_LOG_WARNING (2)
#define SWAT_API_LOG_ERROR (3)
#define SWAT_API_LOG_ALERT (4)
#define SWAT_API_LOG_NOTICE (5)

// Internal worker thread setup constants
#define SWAT_API_WORKER_THR_DISABLED ((void* (*)(void*))0)
#define SWAT_API_WORKER_THR_DEFAULT ((void* (*)(void*))1)

typedef struct SWAT_API_CLIENT_STRUCT {
    pthread_mutex_t mux;
    int debug_flag;
    int state;  // CLOSED, CONNECTING, ESTABLISHED
    int sock;   // i/o socket
    int epfd;   // epoll socket
    struct in_addr ip4addr;
    int port;
    int telnum;
    uint64_t sb_id;
    uint64_t sb_id_rx;
    uint64_t ob_id;
    uint64_t ob_id_rx;
    uint16_t subarray_id;
    int send_flag;
    int recv_flag;
    int sort_flag;
    int hw_flag;
    int* async_signal;  // may be NULL
    int read_seqnum;
    int write_seqnum;
    char wrbuf[SWAT_API_PKT_MAXLEN];
    int wrlen;
    int wrofs;
    int wrbufitems;  // number of packets in write buffer
    SWAT_PACKET_HEADER rdhdr;
    char rdbuf[SWAT_API_PKT_MAXLEN];
    int rdlen;
    int rdofs;
    int rdstate;
    SWAT_R1_HIGH_RES_TIMESTAMP
    connect_time;  // when the next connection attempt will be (i.e. after REFUSED)
    SWAT_PACKET_R1_TRIGGER camevbuf[SWAT_API_CAMEVS_MAXLEN];
    int camevlen;
    SWAT_PACKET_R1_EVENT_REQUEST
    arrevlast;  // used to filter out duplicates upon reconnect to SWAT
    SWAT_PACKET_R1_EVENT_REQUEST arrevbuf[SWAT_API_ARREVS_MAXLEN];
    int arrevlen;
    int arrevofs;
    int timeout_ms;  // zero disables
    int events;
    void* (*worker_thr)(void*);
    pthread_t worker_thr_ID;
    int worker_join_request;
    int camev_nfull;  // number of camera events dropped by API due to buffer full
    int camev_ngood;  // number of good camera events processed by API
    int camevlenmax;
    int arrev_nduplicate;
    int arrev_nfull;
    int arrev_npositive;
    int arrev_nnegative;
    int arrevlenmax;
    int (*debug_logger)(int type, char* msg);
} SWAT_API_CLIENT;

// The struct describing the state of the API
typedef struct SWAT_API_STATUS_STRUCT {
    int debug_flag;        // zero for normal operation, non-zero means extra logging
    int telnum;            // telescope channel number
    int state;             // CLOSED, CONNECTING, ESTABLISHED
    int events;            // API events registered since last call to api_worker()
    uint64_t sb_id;        // SB ID set during configuration
    uint64_t sb_id_rx;     // SB ID received from SWAT server
    uint64_t ob_id;        // OB ID set during configuration
    uint64_t ob_id_rx;     // OB ID received from SWAT server
    uint16_t subarray_id;  // subarray ID received from SWAT server
    SWAT_R1_HIGH_RES_TIMESTAMP
    connect_time;     // when the API will attempt to (re-)connect to SWAT server (i.e.
                      // after REFUSED)
    int timeout_ms;   // timeout for socket operations
    int wrbufitems;   // number of outstanding packets in API send buffer
    int camev_inbuf;  // number of outgoing camera events in API send buffer
    int camev_bufsize;  // max possible number of outgoing camera events in API send
                        // buffer (buffer limit)
    int camev_nfull;  // number of camera events dropped by API due to send buffer full
    int camev_ngood;  // number of good camera events processed by API
    int camev_inbufmax;  // max number of outgoing camera events in API send buffer
    int arrev_inbuf;     // number of incoming array events in API receive buffers
                         // (received, but not read by userapp)
    int arrev_bufsize;   // max possible number of incoming array events in API receive
                         // buffers (buffer limit)
    int arrev_nduplicate;  // number of duplicated array events
    int arrev_nfull;      // number of array events dropped by API due to receive buffer
                          // full
    int arrev_npositive;  // number of good positive array events received by API
    int arrev_nnegative;  // number of good negative array events received by API
    int arrev_inbufmax;   // max number of incoming array events in API receive buffers
                          // (received, but not read by userapp)
} SWAT_API_STATUS;

/**
 * Allocates the SWAT API structure.
 * @param    swat_api_h   the pointer to be updated with the API structure address
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_create(SWAT_API_CLIENT** swat_api_h);
/**
 * Deallocates the SWAT API structure.
 * @param  swat_api_h     the pointer to the structure to be deleted
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_destroy(SWAT_API_CLIENT** swat_api_h);
/**
 * Gets the current status of the swat_api_h instance that is pointed at
 * @param  swat_api_h     the pointer to the API structure
 * @param  status         the pointer to the status structure to be updated
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_get_status(SWAT_API_CLIENT* swat_api_h, SWAT_API_STATUS* status);
/**
 * Sets debug logging of the API instance.
 * @param swat_api_h      the pointer to the API structure to be altered
 * @param debug_flag      the selection of the message types (refer to SWAT_API_DEBUG...
 * defines and select many using bitwise OR)
 * @param debug_logger    the logging function to be used (either a value according to
 * SWAT_API_LOGGER... defines or a custom function pointer)
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_set_debug(SWAT_API_CLIENT* swat_api_h, int debug_flag,
                       int (*debug_logger)(int type, char* msg));
/**
 * Reads the next received event request from the queue
 * @param swat_api_h      the pointer to the API structure to be accessed
 * @param swatev          the pointer to the structure to be updated using the new event
 * request information
 * @return                a SWAT completion code as described in the swat_errors.h
 * header. If no data is available equal to SWAT_ERR_NO_NEW_DATA
 */
int swat_api_read_array_event(SWAT_API_CLIENT* swat_api_h,
                              SWAT_PACKET_R1_EVENT_REQUEST* swatev);
/**
 * Writes a trigger to the queue
 * @param swat_api_h      the pointer to the API structure to be accessed
 * @param camev           the pointer to the structure containing the trigger
 * information
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_write_camera_event(SWAT_API_CLIENT* swat_api_h,
                                SWAT_PACKET_R1_TRIGGER* camev);
/**
 * Configures a SWAT API instance without using a configuration file.
 * @param swat_api_h      the pointer to the API structure to be altered
 * @param ip4addr         the IP address of the host running the SWAT server to connect
 * to (host byte ordering!)
 * @param port            the TCP port number used for the communication (currently
 * 13579 is default)
 * @param telnum          the channel number as assigned in SWAT configuration
 * @param sb_id           the Scheduling Block ID of the current observation
 * @param ob_id           the Observation Block ID of the current observation
 * @param send_flag       the send flag: 0 if this client shall not send triggers; 1 if
 * it shall
 * @param recv_flag       the receive flag: 0 if this client shouldn't receive event
 * requests after coincidence detection, 1 if it should
 * @param sort_flag       the sort flag: 0 if the events sent are not guaranteed to be
 * sorted, 1 if the event stream will always be fully sorted
 * @param hw_flag         the hardware trigger flag: 1 if this client serves a hardware
 * trigger that has multiple telescopes connected, 0 otherwise
 * @param timeout_ms      the timeout for socket operations in ms (2000 is recommmended)
 * @param async_signal    the async stop signal: if the value pointed is not equal to 0,
 * the API shall stop during the next event, can be NULL
 * @param worker_thr      the pointer to the internal worker function. Can be default
 * (SWAT_API_WORKER_THR_DEFAULT), custom or disabled (SWAT_API_WORKER_THR_DISABLED).
 *                          When disabled swat_api_worker(...) needs to be called
 * periodically to process events.
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_configure(SWAT_API_CLIENT* swat_api_h, struct in_addr ip4addr, int port,
                       int telnum, uint64_t sb_id, uint64_t ob_id, int send_flag,
                       int recv_flag, int sort_flag, int hw_flag, int timeout_ms,
                       int* async_signal, void* (*worker_thr)(void*));
/**
 * Requests the start of the API. Causes a connection attempt to the SWAT server
 * @param swat_api_h      the pointer to the API structure to be altered
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_start(SWAT_API_CLIENT* swat_api_h);
/**
 * Informs the API logic that the worker thread is terminating (must be called
 * excusively from the worker thread function)
 * @param swat_api_h      the pointer to the API structure to be altered
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_clear_worker(SWAT_API_CLIENT* swat_api_h);
/**
 * Checks if the internal worker thread is still running.
 * @param swat_api_h      the pointer to the API structure to be polled
 * @return                a SWAT completion code as described in the swat_errors.h
 * header: SWAT_OK when thread has terminated: SWAT_ERR_BAR_ARG when it's still running
 */
int swat_api_check_worker(SWAT_API_CLIENT* swat_api_h);
/**
 * Blocks the calling thread until the worker thread is stopped
 * @param swat_api_h      the pointer to the API structure to be polled
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_wait_worker_cleared(SWAT_API_CLIENT* swat_api_h);
/**
 * Stops the API by closing all sockets and, if applicable, signalling the worker thread
 * @param swat_api_h      the pointer to the API structure to be altered
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_stop(SWAT_API_CLIENT* swat_api_h);
/**
 * Stop the API the same way as swat_api_stop(...) and clears the configuration
 * @param swat_api_h      the pointer to the API structure to be altered
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_reset(SWAT_API_CLIENT* swat_api_h);
/**
 * The function called by the internal worker thread to process queued events that must
 * be called manually if the thread has been disabled
 * @param swat_api_h      the pointer to the API structure to be altered
 * @param timeout_ms      a maximum time the function will wait for new events and block
 * the calling thread
 * @param status          the pointer to the status struct to be updated with the effect
 * of the processing. May be NULL
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_worker(SWAT_API_CLIENT* swat_api_h, int timeout_ms,
                    SWAT_API_STATUS* status);
/**
 * The default implementation of the worker thread with a signature compatible with
 * pthread_create(...)
 * @param arg             the pointer to the SWAT_API_CLIENT to be served
 * @return                always NULL
 */
void* swat_api_worker_thr(void* arg);
/**
 * Translates the numeric representation of the logger message type to its textual
 * counterpart
 * @param type            the numeric message type
 * @return                the textual counterpart (always 5 characters)
 */
const char* swat_api_log_type2str(int type);
/**
 * Logs the provided message (in the standalone, non-ACS version: formats and prints to
 * stderr)
 * @param type            the numeric message type
 * @param msg             the message text
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_log(int type, char* msg);
/**
 * Logs a message of type DEBUG using the swat_api_log(...) function
 * @param msg             the message text
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_log_debug(char* msg);
/**
 * Logs a message of type INFO using the swat_api_log(...) function
 * @param msg             the message text
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_log_info(char* msg);
/**
 * Logs a message of type WARNING using the swat_api_log(...) function
 * @param msg             the message text
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_log_warn(char* msg);
/**
 * Logs a message of type ERROR using the swat_api_log(...) function
 * @param msg             the message text
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_log_error(char* msg);
/**
 * Logs a message of type ALERT using the swat_api_log(...) function
 * @param msg             the message text
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_log_alert(char* msg);
/**
 * Calibrates the internal timekeeping functions to operate based on either CLOCK_TAI or
 * CLOCK_REALTIME. If there is no valid CLOCK_TAI configuration, an automatic fallback
 * to CLOCK_REALTIME occurs.
 * @param swat_api_h      a SWAT_API_CLIENT intance to inherit logging and debug
 * settings from. Can be NULL
 * @param tai_flag        the clock source to be used: either CLOCK_TAI or
 * CLOCK_REALTIME
 * @param leap_secs       the UTC-TAI difference to be used together with
 * CLOCK_REALTIME; current value valid at least until 31 Dec 2021 is 37
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_calibrate_tai(SWAT_API_CLIENT* swat_api_h, int tai_flag, int leap_secs);

// DEPRECATED FUNCTIONS
int swat_api_get_state(SWAT_API_CLIENT* swat_api_h, int* state);
int swat_api_close(SWAT_API_CLIENT* swat_api_h);
int swat_api_setup(SWAT_API_CLIENT* swat_api_h, struct in_addr ip4addr, int port,
                   int telnum, int send_flag, int recv_flag, int sort_flag, int hw_flag,
                   int timeout_ms, int* async_signal);
int swat_api_get_wrbufitems(SWAT_API_CLIENT* swat_api_h, int* wrbufitems);
int swat_api_get_arrev_stats(SWAT_API_CLIENT* swat_api_h, int* ndups, int* nfull,
                             int* ngood);
int swat_api_wait_event(SWAT_API_CLIENT* swat_api_h, int timeout_millisec,
                        int* read_array_events, int* write_camera_events);

// INTERNALLY-USED FUNCTIONS
const char* l_swat_state2str(int state);
int l_swat_is_closed(SWAT_API_CLIENT* swat_api_h);
void l_swat_close_sockets(SWAT_API_CLIENT* swat_api_h, int newstate);
int l_swat_is_socket_ok(SWAT_API_CLIENT* swat_api_h);
int l_swat_async_socket_ok(SWAT_API_CLIENT* swat_api_h);
void l_swat_init_buffers(SWAT_API_CLIENT* swat_api_h);
void l_swat_init_defaults(SWAT_API_CLIENT* swat_api_h, int reset_debug);

void l_swat_api_get_status(SWAT_API_CLIENT* swat_api_h, SWAT_API_STATUS* status);

int l_swat_append_pkthdr(SWAT_API_CLIENT* swat_api_h, int pktype, int len);
int l_swat_append_pkt(SWAT_API_CLIENT* swat_api_h, int pktype, int len, void* p);

int l_swat_read_processor(SWAT_API_CLIENT* swat_api_h);

int l_swat_write_processor(SWAT_API_CLIENT* swat_api_h);
int l_swat_submit_processor(SWAT_API_CLIENT* swat_api_h, int pktype, void* payload,
                            int len);
int l_swat_submit_request(SWAT_API_CLIENT* swat_api_h);

int l_swat_epoll_process_event(SWAT_API_CLIENT* swat_api_h, struct epoll_event* ev);

int l_swat_api_wait_event(SWAT_API_CLIENT* swat_api_h, int timeout_ms);
int l_swat_api_connect(SWAT_API_CLIENT* swat_api_h);
int l_swat_api_signal_worker(SWAT_API_CLIENT* swat_api_h);
int l_swat_api_debug_msg(SWAT_API_CLIENT* swat_api_h, int type, char* msg);
int l_swat_api_mutex_debug_msg(SWAT_API_CLIENT* swat_api_h, int type, char* msg);
int l_swat_api_flag_events(SWAT_API_CLIENT* swat_api_h, int myevents);
const char* l_swat_api_clktype2str(int clktype);
int l_swat_api_final_report(SWAT_API_CLIENT* swat_api_h);

#ifdef __cplusplus
}
#endif

#endif /* SWAT_API_H */
