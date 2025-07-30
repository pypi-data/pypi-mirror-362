/*
 * swat_api.c
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
 */

#include "swat_api.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

const char* l_swat_state2str(int state) {
    switch (state) {
        case SWAT_API_STATE_INIT:
            return ("INIT");
        case SWAT_API_STATE_CONNECTING:
            return ("CONNECTING");
        case SWAT_API_STATE_ESTABLISHED:
            return ("ESTABLISHED");
        case SWAT_API_STATE_ABORTED:
            return ("ABORTED");
        case SWAT_API_STATE_HANGUP:
            return ("HANGUP");
        case SWAT_API_STATE_CLOSED:
            return ("CLOSED");
        case SWAT_API_STATE_REFUSED:
            return ("REFUSED");
        default:
            return ("UNKNOWN");
    }
}

int l_swat_is_closed(SWAT_API_CLIENT* swat_api_h) {
    if ((SWAT_API_STATE_CLOSED == swat_api_h->state) ||
        (SWAT_API_STATE_ABORTED == swat_api_h->state) ||
        (SWAT_API_STATE_REFUSED == swat_api_h->state) ||
        (SWAT_API_STATE_HANGUP == swat_api_h->state))
        return (1);
    return (0);
}

void l_swat_close_sockets(SWAT_API_CLIENT* swat_api_h, int newstate) {
    SWAT_R1_HIGH_RES_TIMESTAMP curtime, nxtime;

    if ((SWAT_API_INVALID_HANDLE != swat_api_h->epfd) &&
        (SWAT_API_INVALID_HANDLE != swat_api_h->sock)) {
        epoll_ctl(swat_api_h->epfd, EPOLL_CTL_DEL, swat_api_h->sock,
                  NULL);  // errors are ignore here, we close anyway
    }
    if (SWAT_API_INVALID_HANDLE != swat_api_h->epfd) {
        close(swat_api_h->epfd);  // errors ignored
        swat_api_h->epfd = SWAT_INVALID_HANDLE;
    }
    if (SWAT_API_INVALID_HANDLE != swat_api_h->sock) {
        close(swat_api_h->sock);  // errors ignored
        swat_api_h->sock = SWAT_INVALID_HANDLE;
    }
    swat_api_h->state = newstate;
    // if we are in CLOSED state, recompute when next connection attempt will be
    if (l_swat_is_closed(swat_api_h)) {
        if (swat_api_h->connect_time)  // if we are IDLE/STOP, do recompute connect_time
        {
            curtime = swat_get_tai_time();
            // compute time of next reconnection attempt
            nxtime = swat_api_h->connect_time +
                     // if timeouts are disabled, set reconnect period to 1s (otherwise
                     // tight loop occurs if REFUSED)
                     ((swat_api_h->timeout_ms > 0) ? swat_api_h->timeout_ms : 1000) *
                         SWAT_API_MS_TIME_T_TICKS;
            // REFUSED is usually immediate, so we should linger for a couple of seconds
            // before next attempt...
            if (curtime < nxtime) {
                swat_api_h->connect_time = nxtime;
            }
            // for all other cases (TIMEOUT, HANGUP, CLOSE) we shall reconnect without
            // any delay ...
            else {
                swat_api_h->connect_time = curtime;
            }
        }
    }

    l_swat_init_buffers(
        swat_api_h);  // make sure read/write seqnums start from zero again

    return;
}

int l_swat_is_socket_ok(SWAT_API_CLIENT* swat_api_h) {
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    if (SWAT_API_STATE_INIT == swat_api_h->state) return (SWAT_ERR_BAD_STATE);
    if (l_swat_is_closed(swat_api_h)) return (SWAT_ERR_BAD_STATE);
    if (SWAT_API_INVALID_HANDLE == swat_api_h->sock) return (SWAT_ERR_BAD_ARG);
    if (SWAT_API_INVALID_HANDLE == swat_api_h->epfd) return (SWAT_ERR_BAD_ARG);
    return (SWAT_OK);
}

int l_swat_async_socket_ok(SWAT_API_CLIENT* swat_api_h) {
    int r;

    r = l_swat_is_socket_ok(swat_api_h);
    if (SWAT_OK == r)  // first check whether async signalling is enabled
    {
        if (NULL != swat_api_h->async_signal)
            if (0 != *(swat_api_h->async_signal))
                r = SWAT_ERR_EXITING;  // signal immediate exit
    }
    return (r);
}

void l_swat_init_buffers(SWAT_API_CLIENT* swat_api_h) {
    swat_api_h->read_seqnum = 0;
    swat_api_h->write_seqnum = 0;
    swat_api_h->wrlen = 0;
    swat_api_h->wrofs = 0;
    swat_api_h->wrbufitems = 0;
    swat_api_h->rdlen = 0;
    swat_api_h->rdofs = 0;
    swat_api_h->rdstate = SWAT_API_STATE_NULL;
}

void l_swat_init_defaults(SWAT_API_CLIENT* swat_api_h, int reset_debug) {
    if (reset_debug) swat_api_h->debug_flag = 0;
    swat_api_h->state = SWAT_API_STATE_INIT;
    swat_api_h->sock = SWAT_API_INVALID_HANDLE;
    swat_api_h->epfd = SWAT_API_INVALID_HANDLE;
    swat_api_h->ip4addr.s_addr = 0;
    swat_api_h->port = 0;
    swat_api_h->telnum = -1;
    swat_api_h->sb_id = 0;
    swat_api_h->ob_id = 0;
    swat_api_h->sb_id_rx = 0;
    swat_api_h->ob_id_rx = 0;
    swat_api_h->subarray_id = 0;
    swat_api_h->send_flag = 0;
    swat_api_h->recv_flag = 0;
    swat_api_h->sort_flag = 0;
    swat_api_h->hw_flag = 0;
    swat_api_h->async_signal = NULL;
    l_swat_init_buffers(swat_api_h);
    swat_api_h->connect_time = 0;
    swat_api_h->camevlen = 0;
    swat_api_h->arrevlast.requested.trigger_time = 0;
    swat_api_h->arrevlast.requested.trigger_id = 0;
    swat_api_h->arrevlast.negative_flag = 0;
    swat_api_h->arrevlast.assigned_event_id = 0;
    swat_api_h->arrevlen = 0;
    swat_api_h->arrevofs = 0;
    swat_api_h->timeout_ms = 0;
    swat_api_h->events = SWAT_API_EVENT_NULL;
    swat_api_h->worker_thr = SWAT_API_WORKER_THR_DISABLED;
    swat_api_h->worker_thr_ID = 0;
    swat_api_h->worker_join_request = 0;
    swat_api_h->camev_nfull = 0;
    swat_api_h->camev_ngood = 0;
    swat_api_h->camevlenmax = 0;
    swat_api_h->arrev_nduplicate = 0;
    swat_api_h->arrev_nfull = 0;
    swat_api_h->arrev_npositive = 0;
    swat_api_h->arrev_nnegative = 0;
    swat_api_h->arrevlenmax = 0;
    if (reset_debug) swat_api_h->debug_logger = SWAT_API_LOGGER_DISABLED;
}

int swat_api_create(SWAT_API_CLIENT** swat_api_h) {
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    *swat_api_h = (SWAT_API_CLIENT*)malloc(sizeof(SWAT_API_CLIENT));
    if (NULL == *swat_api_h) return (SWAT_ERR_NO_MEMORY);
    if (pthread_mutex_init(&((*swat_api_h)->mux), NULL)) {
        free(*swat_api_h);
        *swat_api_h = NULL;
        return (SWAT_ERR_MUTEX_INIT_FAILED);
    }
    l_swat_init_defaults(*swat_api_h, 1);
    return (SWAT_OK);
}

int swat_api_destroy(SWAT_API_CLIENT** swat_api_h) {
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    if (NULL == *swat_api_h) return (SWAT_ERR_NUL_PTR);  // already freed ??
    l_swat_close_sockets(*swat_api_h, SWAT_API_STATE_INIT);
    pthread_mutex_destroy(&((*swat_api_h)->mux));
    free((void*)(*swat_api_h));
    *swat_api_h = NULL;
    return (SWAT_OK);
}

void l_swat_api_get_status(SWAT_API_CLIENT* swat_api_h, SWAT_API_STATUS* status) {
    status->debug_flag = swat_api_h->debug_flag;
    status->telnum = swat_api_h->telnum;
    status->state = swat_api_h->state;
    status->events = swat_api_h->events;
    status->sb_id = swat_api_h->sb_id;
    status->sb_id_rx = swat_api_h->sb_id_rx;
    status->ob_id = swat_api_h->ob_id;
    status->ob_id_rx = swat_api_h->ob_id_rx;
    status->subarray_id = swat_api_h->subarray_id;
    status->connect_time = swat_api_h->connect_time;
    status->timeout_ms = swat_api_h->timeout_ms;
    status->wrbufitems = swat_api_h->wrbufitems;
    status->camev_inbuf = swat_api_h->camevlen;
    status->camev_bufsize = SWAT_API_CAMEVS_MAXLEN;
    status->camev_nfull = swat_api_h->camev_nfull;
    status->camev_ngood = swat_api_h->camev_ngood;
    status->camev_inbufmax = swat_api_h->camevlenmax;
    status->arrev_inbuf = swat_api_h->arrevlen;
    status->arrev_bufsize = SWAT_API_ARREVS_MAXLEN;
    status->arrev_nduplicate = swat_api_h->arrev_nduplicate;
    status->arrev_nfull = swat_api_h->arrev_nfull;
    status->arrev_npositive = swat_api_h->arrev_npositive;
    status->arrev_nnegative = swat_api_h->arrev_nnegative;
    status->arrev_inbufmax = swat_api_h->arrevlenmax;
}

int swat_api_get_status(SWAT_API_CLIENT* swat_api_h, SWAT_API_STATUS* status) {
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    if (NULL == status) return (SWAT_ERR_NUL_PTR);

    pthread_mutex_lock(&swat_api_h->mux);
    l_swat_api_get_status(swat_api_h, status);
    pthread_mutex_unlock(&swat_api_h->mux);
    return (SWAT_OK);
}

int swat_api_set_debug(SWAT_API_CLIENT* swat_api_h, int debug_flag,
                       int (*debug_logger)(int type, char* msg)) {
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    pthread_mutex_lock(&swat_api_h->mux);
    swat_api_h->debug_flag = debug_flag;
    swat_api_h->debug_logger = debug_logger;
    pthread_mutex_unlock(&swat_api_h->mux);
    return (SWAT_OK);
}

int l_swat_append_pkthdr(SWAT_API_CLIENT* swat_api_h, int pktype, int len) {
    int nsize;
    SWAT_PACKET_HEADER ph;

    // check args
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    if ((len < 0) || ((len + sizeof(SWAT_PACKET_HEADER)) > SWAT_API_PKT_MAXLEN))
        return (SWAT_ERR_BAD_ARG);
    // is there enough space in write buffer ?
    nsize = swat_api_h->wrlen + sizeof(SWAT_PACKET_HEADER) +
            len;  // len does not include pkt header !
    if (nsize > SWAT_API_PKT_MAXLEN)
        return (
            SWAT_ERR_BUFFER_FULL);  // likely SWAT server too slow, or network stuck ...
    if (swat_api_h->wrbufitems >= SWAT_API_MAXWRBUFITEMS) return (SWAT_ERR_BUFFER_FULL);
    // format packet header
    ph.magic[0] = SWAT_API_PKT_MAGIC0;
    ph.magic[1] = SWAT_API_PKT_MAGIC1;
    ph.pktype = pktype;
    ph.tel_id = swat_api_h->telnum;
    ph.bunch_id = (unsigned int)(swat_api_h->write_seqnum);
    ph.paylen = len;
    ph.num_in_bunch = (pktype == SWAT_API_PKTYPE_CAMEVS) ? swat_api_h->camevlen : 0;
    // append it to write buffer
    memcpy(&(swat_api_h->wrbuf[0]) + swat_api_h->wrlen, &(ph), sizeof(ph));
    swat_api_h->wrlen += sizeof(ph);

    (swat_api_h->wrbufitems)++;
    (swat_api_h->write_seqnum)++;

    return (SWAT_OK);
}

int l_swat_append_pkt(SWAT_API_CLIENT* swat_api_h, int pktype, int len, void* p) {
    int r;

    // do some checks, prepare and append packet headers to writebufs
    r = l_swat_append_pkthdr(swat_api_h, pktype, len);
    if (SWAT_OK != r) return (r);
    // append payload to writebufs
    if (len > 0) memcpy(&(swat_api_h->wrbuf[0]) + swat_api_h->wrlen, p, len);
    swat_api_h->wrlen += len;

    return (r);
}

// function retrieves one array event from SWAT.
// ARGS: swat_api_h - pointer to SWAT client structure, arrev - pointer to array event
// RETURN VALUE: standard error code (usually SWAT_OK or SWAT_ERR_NO_NEW_DATA)
// the function is fully __NONBLOCKING__
int swat_api_read_array_event(SWAT_API_CLIENT* swat_api_h,
                              SWAT_PACKET_R1_EVENT_REQUEST* arrev) {
    int r;

    // simple checks before mutex
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    if (NULL == arrev) return (SWAT_ERR_NUL_PTR);

    r = SWAT_OK;
    pthread_mutex_lock(&swat_api_h->mux);

    // NOTE: some events may linger in our buffers even after the close()
    // we continue to successfully read such array events from our buffers
    // Only once our buffers are empty we return SWAT_ERR_NO_NEW_DATA
    if ((swat_api_h->arrevlen > 0) &&  // are there any camevs in the buffer ?
        (0 == (swat_api_h->debug_flag &
               SWAT_API_DEBUG_TEST_STUCK)))  // and we are not simulating stuck reader
    {
        *arrev = swat_api_h->arrevbuf[swat_api_h->arrevofs];
        swat_api_h->arrevofs = (swat_api_h->arrevofs + 1) % SWAT_API_ARREVS_MAXLEN;
        (swat_api_h->arrevlen)--;
    } else {
        r = SWAT_ERR_NO_NEW_DATA;
        //       if (l_swat_is_closed(swat_api_h))  r = SWAT_ERR_EXITING;
        if (NULL != swat_api_h->async_signal) {
            if (0 != *(swat_api_h->async_signal)) r = SWAT_ERR_EXITING;
        }
    }

    pthread_mutex_unlock(&swat_api_h->mux);
    return (r);
}

// assuming we already hold mutex on swat_api_h, function
// calls  read() once. If read completes successfully
// reading full set of data, buffer/queue is updated
// Final step is to disable EPOLLOUT for that socket
// if the is no more pending data in buffer/queue.
// ARGS: swat_api_h - pointer to SWAT client structure
// RETURN VALUE: number of bytes read or -1 on error
// NOTES: usually we are called by EPOLLIN event ...
int l_swat_read_processor(SWAT_API_CLIENT* swat_api_h) {
    int nread, i, r, toread, nitems, effidx, erlogd /*, len, ofs, rng*/;
    char buf[SWAT_API_LOGGER_MAX_MSG];
    SWAT_PACKET_R1_EVENT_REQUEST* arrevs;
    SWAT_PACKET_ACCEPT* accept;

    if (SWAT_OK != l_swat_is_socket_ok(swat_api_h)) return (-1);
    nread = 0;  // bogus compiler warning

    switch (swat_api_h->rdstate) {
        case SWAT_API_STATE_NULL:
            swat_api_h->rdstate = SWAT_API_STATE_PKTHDR;
            swat_api_h->rdlen = sizeof(SWAT_PACKET_HEADER);
            swat_api_h->rdofs = 0;
            break;
        case SWAT_API_STATE_PKTHDR:
            if (sizeof(SWAT_PACKET_HEADER) != swat_api_h->rdlen)
                return (-1);  // internal error
            break;
        case SWAT_API_STATE_PKTPAYLOAD:
        case SWAT_API_STATE_PKTACCEPT:
            break;
        default:
            return (-1);  // internal error
    }

    toread = swat_api_h->rdlen - swat_api_h->rdofs;
    if (toread < 0) return (-1);  // internal error

    if (toread > 0)  // we should read some more data
    {
        nread = read(swat_api_h->sock, (void*)(swat_api_h->rdbuf + swat_api_h->rdofs),
                     toread);
        if (nread > 0) {
            swat_api_h->rdofs += nread;
        }
    }

    if ((toread == nread) || (0 == toread))  // we just read full item
    {  //....... HERE WE PROCESS COMPLETELY READ IN DATA CHUNK ...........
        switch (swat_api_h->rdstate) {
            case SWAT_API_STATE_PKTHDR:
                memcpy(&(swat_api_h->rdhdr), &(swat_api_h->rdbuf[0]),
                       sizeof(SWAT_PACKET_HEADER));
                if (SWAT_OK != (r = swat_pkthdr_check_recv(&(swat_api_h->rdhdr)))) {
                    return (-1);
                }  // signal pktframe error
                if (swat_api_h->rdhdr.tel_id != swat_api_h->telnum) {
                    return (-1);
                }  // packet not for us ...
                if ((SWAT_API_PKTYPE_NULL != swat_api_h->rdhdr.pktype) &&
                    (swat_api_h->rdhdr.paylen > 0)) {
                    swat_api_h->rdofs = 0;
                    swat_api_h->rdlen = swat_api_h->rdhdr.paylen;
                    if (swat_api_h->rdhdr.pktype == SWAT_API_PKTYPE_ARREVS) {
                        swat_api_h->rdstate = SWAT_API_STATE_PKTPAYLOAD;
                    } else if (swat_api_h->rdhdr.pktype == SWAT_API_PKTYPE_ACCEPT) {
                        swat_api_h->rdstate = SWAT_API_STATE_PKTACCEPT;
                    } else {
                        return (-1);
                    }
                }
                break;
            case SWAT_API_STATE_PKTPAYLOAD:
                nitems = swat_api_h->rdlen / sizeof(SWAT_PACKET_R1_EVENT_REQUEST);
                arrevs = (SWAT_PACKET_R1_EVENT_REQUEST*)(&(swat_api_h->rdbuf[0]));
                if (nitems > 0)  // display debug msgs when requested
                {
                    if (swat_api_h->debug_flag & SWAT_API_DEBUG_PKTHDR) {
                        snprintf(
                            buf, SWAT_API_LOGGER_MAX_MSG,
                            "PKTYPE_ARREVS: header:  PayloadBytes=%6d  NumArrEvs = %4d",
                            swat_api_h->rdlen, nitems);
                        l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
                    }
                    if (swat_api_h->debug_flag &
                        (SWAT_API_DEBUG_ARREV_POS | SWAT_API_DEBUG_ARREV_NEG)) {
                        SWAT_R1_HIGH_RES_TIMESTAMP ct = swat_get_tai_time();
                        for (i = 0; i < nitems; i++) {
                            if (arrevs[i].negative_flag) {
                                if (swat_api_h->debug_flag & SWAT_API_DEBUG_ARREV_NEG) {
                                    snprintf(
                                        buf, SWAT_API_LOGGER_MAX_MSG,
                                        "PKTYPE_ARREVS: record: ==NEGATIVE== camid=%lu "
                                        "tstamp=%.6f deltat=%.3f",
                                        arrevs[i].requested.trigger_id,
                                        arrevs[i].requested.trigger_time /
                                            ((double)SWAT_API_S_TIME_T_TICKS),
                                        (ct -
                                         (double)arrevs[i].requested.trigger_time) /
                                            ((double)SWAT_API_S_TIME_T_TICKS));
                                    l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG,
                                                         buf);
                                }
                            } else {
                                if (swat_api_h->debug_flag & SWAT_API_DEBUG_ARREV_POS) {
                                    snprintf(
                                        buf, SWAT_API_LOGGER_MAX_MSG,
                                        "PKTYPE_ARREVS: record: arrid=%-6d camid=%lu "
                                        "tstamp=%.6f deltat=%.3f",
                                        arrevs[i].assigned_event_id,
                                        arrevs[i].requested.trigger_id,
                                        arrevs[i].requested.trigger_time /
                                            ((double)SWAT_API_S_TIME_T_TICKS),
                                        (ct -
                                         (double)arrevs[i].requested.trigger_time) /
                                            ((double)SWAT_API_S_TIME_T_TICKS));
                                    l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG,
                                                         buf);
                                }
                            }
                        }
                    }
                }
                erlogd = 0;  // only up to 1 error msgs about duplicates per SWAT packet
                for (i = 0; i < nitems; i++) {
                    if (swat_api_h->arrevlen < SWAT_API_ARREVS_MAXLEN) {
                        if (
                            // This check protects against duplicate data from SWAT
                            // server. This is only possible upon connection drop and
                            // immediate reconnect to SWAT server For negative array
                            // triggers unfortunately we have:
                            // arrevlast.assigned_event_id==0
                            //                                   (arrevs[i].trigger_id
                            //                                   <=
                            //                                   swat_api_h->arrevlast.assigned_event_id)
                            //                                   &&
                            // we check both trigger_id and trigger_time. If either is
                            // bigger than arrevlast, we accept new event.
                            (arrevs[i].requested.trigger_id <=
                             swat_api_h->arrevlast.requested.trigger_id) &&
                            (arrevs[i].requested.trigger_time <=
                             swat_api_h->arrevlast.requested.trigger_time)) {
                            (swat_api_h->arrev_nduplicate)++;
                            if (swat_api_h->debug_flag &
                                SWAT_API_DEBUG_ERRORS) {  // upon reconnect to SWAT
                                                          // server protect against
                                                          // duplicates, and do not
                                                          // flood log system with too
                                                          // many errors ...
                                if (!erlogd) {
                                    snprintf(
                                        buf, SWAT_API_LOGGER_MAX_MSG,
                                        "duplicate/unsorted data: ignoring idx=%d "
                                        "arrevs(idx=%d+, neg=%d)... prev=%lu",
                                        i, arrevs[i].assigned_event_id,
                                        arrevs[i].negative_flag,
                                        swat_api_h->arrevlast.requested.trigger_id);
                                    l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_ERROR,
                                                         buf);
                                    erlogd = 1;
                                }
                            }
                        } else {
                            if (arrevs[i].negative_flag) {
                                (swat_api_h->arrev_nnegative)++;
                            } else {
                                (swat_api_h->arrev_npositive)++;
                            }
                            erlogd = 0;
                            effidx = (swat_api_h->arrevofs + swat_api_h->arrevlen) %
                                     SWAT_API_ARREVS_MAXLEN;
                            swat_api_h->arrevlast = swat_api_h->arrevbuf[effidx] =
                                arrevs[i];
                            (swat_api_h->arrevlen)++;
                            if (swat_api_h->arrevlen > swat_api_h->arrevlenmax)
                                swat_api_h->arrevlenmax = swat_api_h->arrevlen;
                        }
                    } else  // FIXME: internal buffers full, for the time being we
                            // ignore error silently (but should be loud)
                    {
                        (swat_api_h->arrev_nfull)++;
                        // FIXME: this should be signalled to SWAT server via epoll_ctl
                        // ... so it stops flooding us with new data ...
                        if (swat_api_h->debug_flag & SWAT_API_DEBUG_ERRORS) {
                            snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                                     "buffer full: cannot insert arrev(id=%d)",
                                     arrevs[i].assigned_event_id);
                            l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_ERROR, buf);
                        }
                        break;
                    }
                }
                swat_api_h->rdofs = 0;
                swat_api_h->rdlen = sizeof(SWAT_PACKET_HEADER);
                swat_api_h->rdstate = SWAT_API_STATE_PKTHDR;
                break;
            case SWAT_API_STATE_PKTACCEPT:
                accept = (SWAT_PACKET_ACCEPT*)(&(swat_api_h->rdbuf[0]));

                if (accept->sb_id != swat_api_h->sb_id && swat_api_h->sb_id != 0) {
                    if (swat_api_h->debug_flag & SWAT_API_DEBUG_DATASTREAM) {
                        snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                                 "sb_id mismatch: received: %llu, expected %llu",
                                 accept->sb_id, swat_api_h->sb_id);
                        l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_WARNING, buf);
                    }
                }
                if (accept->obs_id != swat_api_h->ob_id && swat_api_h->ob_id != 0) {
                    if (swat_api_h->debug_flag & SWAT_API_DEBUG_DATASTREAM) {
                        snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                                 "ob_id mismatch: received: %llu, expected %llu",
                                 accept->obs_id, swat_api_h->ob_id);
                        l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_WARNING, buf);
                    }
                }

                swat_api_h->sb_id_rx = accept->sb_id;
                swat_api_h->ob_id_rx = accept->obs_id;
                swat_api_h->subarray_id = accept->subarray_id;

                swat_api_h->rdofs = 0;
                swat_api_h->rdlen = sizeof(SWAT_PACKET_HEADER);
                swat_api_h->rdstate = SWAT_API_STATE_PKTHDR;
                break;
        }
    }
    return ((toread > 0) ? nread : 0);
}

// assuming we already hold mutex on swat_api_h, function
// calls  write() once. If write completes successfully
// writing full set of data, buffer/queue is updated
// Final step is to disable EPOLLOUT for that socket
// if the is no more pending data in buffer/queue.
// ARGS: swat_api_h - pointer to SWAT client structure
// RETURN VALUE: number of bytes written or -1 on error
// NOTES: usually we are called by EPOLLOUT event ...
int l_swat_write_processor(SWAT_API_CLIENT* swat_api_h) {
    int nwritten, r, towrite;
    struct epoll_event ctlev;

    if (SWAT_OK != l_swat_is_socket_ok(swat_api_h)) return (-1);

    nwritten = 0;  // bogus compiler warning
    towrite = swat_api_h->wrlen - swat_api_h->wrofs;
    if (towrite < 0) return (-1);
    if (towrite > 0)  // we should write some more data
    {
        nwritten = write(swat_api_h->sock,
                         (void*)(swat_api_h->wrbuf + swat_api_h->wrofs), towrite);
        if (nwritten >= 0) {
            swat_api_h->wrofs += nwritten;
        }
    }

    if ((towrite == nwritten) ||
        (0 == towrite))  // we just wrote full item, time to free space in queue
    {
        swat_api_h->wrbufitems = swat_api_h->wrlen = swat_api_h->wrofs = 0;
        // OPTIMIZATION: since wditems == 0, we can unregister EPOLLOUT for current
        // socket
        ctlev.data.fd = swat_api_h->sock;
        ctlev.events = SWAT_API_READER_EVENTS;
        r = epoll_ctl(swat_api_h->epfd, EPOLL_CTL_MOD, swat_api_h->sock, &ctlev);
        if (-1 == r)  // errors ignored ...
        {
        }
    }

    return ((towrite > 0) ? nwritten : 0);
}

// assuming we already hold mutex on swat_api_h, function
// submits one packet of specified pktype, len, and payload.
// Final step is to (optionally) re-enable EPOLLOUT for that socket.
// ARGS: swat_api_h - pointer to SWAT client structure
// RETURN VALUE: standard error code
int l_swat_submit_processor(SWAT_API_CLIENT* swat_api_h, int pktype, void* payload,
                            int len) {
    int er, r;
    struct epoll_event ctlev;

    // check whether client is connected (or at least connecting) ...
    if (SWAT_OK != (r = l_swat_is_socket_ok(swat_api_h))) return (r);
    // do the transfer and update buffer/queue state
    if (SWAT_OK != (r = l_swat_append_pkt(swat_api_h, pktype, len, payload)))
        return (r);
    // if this is the first item in buffer/queue, than we have to (re)enable EPOLLOUT
    if (1 == swat_api_h->wrbufitems) {
        ctlev.data.fd = swat_api_h->sock;
        ctlev.events = SWAT_API_WRITER_EVENTS;
        er = epoll_ctl(swat_api_h->epfd, EPOLL_CTL_MOD, swat_api_h->sock, &ctlev);
        if (er < 0) r = SWAT_ERR_EPOLL_CTL_FAILED;
    }
    return (r);
}

// assuming we already hold mutex on swat_api_h, function
// submits one packet of specified pktype, len, and payload.
// Final step is to (optionally) re-enable EPOLLOUT for that socket.
// ARGS: swat_api_h - pointer to SWAT client structure
// RETURN VALUE: standard error code
int l_swat_submit_request(SWAT_API_CLIENT* swat_api_h) {
    SWAT_PACKET_CONNECT reqpld;

    // check whether this is the very first packet send by SWAT client
    if (0 != swat_api_h->write_seqnum) return (SWAT_ERR_BAD_WR_SEQNUM);

    reqpld.tel_id = swat_api_h->telnum;
    reqpld.send_flag = swat_api_h->send_flag;
    reqpld.recv_flag = swat_api_h->recv_flag;
    reqpld.sort_flag = swat_api_h->sort_flag;
    reqpld.hw_flag = swat_api_h->hw_flag;
    reqpld.sb_id = swat_api_h->sb_id;
    reqpld.obs_id = swat_api_h->ob_id;

    return (l_swat_submit_processor(swat_api_h, SWAT_API_PKTYPE_REQUEST,
                                    (void*)&(reqpld), sizeof(reqpld)));
}

int l_swat_flush_events(SWAT_API_CLIENT* swat_api_h) {
    int r, i;
    char buf[SWAT_API_LOGGER_MAX_MSG];

    if (0 == swat_api_h->camevlen) return (SWAT_OK);
    // ok, so we will be creating a new packet. Errors (like SWAT_ERR_BUFFER_FULL) to be
    // handled by submit_processor()
    r = l_swat_submit_processor(swat_api_h, SWAT_API_PKTYPE_CAMEVS,
                                (void*)&(swat_api_h->camevbuf[0]),
                                swat_api_h->camevlen * sizeof(SWAT_PACKET_R1_TRIGGER));
    if (SWAT_OK == r) {
        if (swat_api_h->debug_flag & SWAT_API_DEBUG_PKTHDR) {
            snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                     "PKTYPE_CAMEVS: header:  PayloadBytes %6d  NumCamEvs = %4d",
                     (int)(swat_api_h->camevlen * sizeof(SWAT_PACKET_R1_TRIGGER)),
                     (int)(swat_api_h->camevlen));
            l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        }
        if (swat_api_h->debug_flag & SWAT_API_DEBUG_CAMEV) {
            SWAT_R1_HIGH_RES_TIMESTAMP ct = swat_get_tai_time();
            for (i = 0; i < swat_api_h->camevlen; i++) {
                snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                         "PKTYPE_CAMEVS: record[%d]: camid=%lu tstamp=%.6f deltat=%.3f",
                         i, swat_api_h->camevbuf[i].trigger_id,
                         swat_api_h->camevbuf[i].trigger_time /
                             ((double)SWAT_API_S_TIME_T_TICKS),
                         (ct - (double)swat_api_h->camevbuf[i].trigger_time) /
                             ((double)SWAT_API_S_TIME_T_TICKS));
                l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
            }
        }
        if (SWAT_API_DEBUG_TEST_DUPKTS & swat_api_h->debug_flag)
            r = l_swat_submit_processor(
                swat_api_h, SWAT_API_PKTYPE_CAMEVS, (void*)&(swat_api_h->camevbuf[0]),
                swat_api_h->camevlen * sizeof(SWAT_PACKET_R1_TRIGGER));
        if (SWAT_OK == r)
            swat_api_h->camevlen = 0;  // packet generated ok, so mark camevbuf as empty
    }
    return (r);
}

// function submits one camera event for writing to SWAT.
// ARGS: swat_api_h - pointer to SWAT client structure, requested - pointer to camera
// event RETURN VALUE: standard error code (usually SWAT_OK or SWAT_ERR_BUF_FULL) the
// function is fully __NONBLOCKING__
int swat_api_write_camera_event(SWAT_API_CLIENT* swat_api_h,
                                SWAT_PACKET_R1_TRIGGER* camev) {
    int r;

    // simple checks before mutex
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    if (NULL == camev) return (SWAT_ERR_NUL_PTR);

    pthread_mutex_lock(&swat_api_h->mux);

    camev->bunch_id = swat_api_h->write_seqnum;

    //   r = l_swat_is_socket_ok(swat_api_h);
    r = SWAT_OK;
    if (SWAT_OK == r) {
        if (swat_api_h->camevlen > 0)  // are there any camevs in the buffer ?
        {
            if ((camev->trigger_time >=
                 (swat_api_h->camevbuf[0].trigger_time +
                  SWAT_API_TBINSIZE))  // did we crosss timebin boundary ?
                || (swat_api_h->camevlen >=
                    SWAT_API_CAMEVS_MAXLEN))  // or maybe simply too many events ?
            {
                r = l_swat_flush_events(swat_api_h);
            }
        }
        if (swat_api_h->camevlen < SWAT_API_CAMEVS_MAXLEN) {
            swat_api_h->camevbuf[swat_api_h->camevlen] = *camev;
            (swat_api_h->camevlen)++;
            if (swat_api_h->camevlen > swat_api_h->camevlenmax)
                swat_api_h->camevlenmax = swat_api_h->camevlen;

            (swat_api_h->camev_ngood)++;  // update stats : number of good camera events
                                          // ingested
        } else {
            (swat_api_h->camev_nfull)++;  // update stats : number of rejected camera
                                          // events due to API buffer full
        }
    }

    pthread_mutex_unlock(&swat_api_h->mux);
    return (r);
}

// assuming we already hold mutex on swat_api_h, function
// processes one epoll event. It performs reads & writes
// detects hangups (and closes sockets in this case)
// ARGS: swat_api_h - pointer to SWAT client structure, ev : pointer to epoll event
// RETURN VALUE: standard error code
int l_swat_epoll_process_event(SWAT_API_CLIENT* swat_api_h, struct epoll_event* ev) {
    int r, nread, nwritten, ok2close, readflag;
    int rv = -1;
    socklen_t rvlen = sizeof(rv);
    char buf[SWAT_API_LOGGER_MAX_MSG];

    // simple checks ...
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    if (NULL == ev) return (SWAT_ERR_NUL_PTR);
    if (SWAT_API_STATE_CLOSED == swat_api_h->state) return (SWAT_ERR_BAD_STATE);
    // init state variables
    r = SWAT_OK;
    readflag = 0;  // initially signal not an I/O read event
    ok2close = 0;  // initially signal cannot close
    nread = 0;     // bogus compiler warning
    // event: we can write some data
    if (ev->events & EPOLLOUT) {  // but first we check, whether initial connect()
                                  // completed (and without errors) ...
        if (swat_api_h->debug_flag & SWAT_API_DEBUG_EPOLL) {
            snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "EPOLL: EPOLLOUT, state=%d",
                     swat_api_h->state);
            l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        }
        if (SWAT_API_STATE_CONNECTING == swat_api_h->state) {
            if (getsockopt(swat_api_h->sock, SOL_SOCKET, SO_ERROR, &rv, &rvlen) < 0) {
                r = SWAT_ERR_CONNECT_FAILED;  // getsockopt() failed, unlikely (unless
                                              // bad args)
                l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_ERROR);
            } else {
                if (0 != rv)  // ERROR: connect did not "go through" - likely SWAT
                              // server not running
                {
                    r = SWAT_ERR_CONNECT_FAILED;
                    l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_REFUSED);
                } else {
                    swat_api_h->state = SWAT_API_STATE_ESTABLISHED;  // signal success -
                                                                     // we are connected
                    l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_ESTABLISHED);
                    // REQUEST packet already submitted (waiting in API buffer)
                    //                   r = l_swat_submit_request(swat_api_h);   // so
                    //                   it is time to send REQUEST packet
                }
            }
        }
        if (SWAT_API_STATE_ESTABLISHED == swat_api_h->state) {
            nwritten =
                l_swat_write_processor(swat_api_h);  // "standard" write procedure ...
            if (nwritten)                            // bogus compiler warning
            {
            }
        }
    }
    // we can read some data
    if (ev->events & EPOLLIN) {
        if (swat_api_h->debug_flag & SWAT_API_DEBUG_EPOLL) {
            snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "EPOLL: EPOLLIN, state=%d",
                     swat_api_h->state);
            l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        }
        if (0 == (SWAT_API_DEBUG_TEST_STUCK & swat_api_h->debug_flag)) {
            readflag = 1;
            nread = l_swat_read_processor(swat_api_h);  // standard read procedure
            if (nread < 0) ok2close = 1;  // force close due to error condition
        } else {
        }
    }
    // is event related to hangup and/or error condition ?
    if (ev->events & (EPOLLHUP | EPOLLERR | EPOLLRDHUP)) {
        if ((1 == readflag) && (0 == nread))
            ok2close = 1;                 // hangup on socket and data read
        if (0 == readflag) ok2close = 1;  // hangup and no data at all
        if (swat_api_h->debug_flag & SWAT_API_DEBUG_EPOLL) {
            snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                     "EPOLL: POLLHUP/ERR/RDHUP, state=%d, readflag=%d, nread=%d, "
                     "ok2close=%d",
                     swat_api_h->state, readflag, nread, ok2close);
            l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        }
    }
    // i/o errors are fatal and we close sockets
    if (ok2close) {
        l_swat_close_sockets(swat_api_h,
                             (SWAT_ERR_CONNECT_FAILED == r)
                                 ? SWAT_API_STATE_REFUSED
                                 : SWAT_API_STATE_HANGUP);  // errors ignored ...
        if (SWAT_ERR_CONNECT_FAILED != r) {
            r = SWAT_ERR_SOCKET_HANGUP;
            l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_HANGUP);
        }
    }
    return (r);
}

int swat_api_configure(SWAT_API_CLIENT* swat_api_h, struct in_addr ip4addr, int port,
                       int telnum, uint64_t sb_id, uint64_t ob_id, int send_flag,
                       int recv_flag, int sort_flag, int hw_flag, int timeout_ms,
                       int* async_signal, void* (*worker_thr)(void*)) {
    int r;

    // simple checks before mutex
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    if ((telnum < 0) || (telnum >= SWAT_API_MAXTELS)) return (SWAT_ERR_BAD_ARG);
    if (port <= 0) return (SWAT_ERR_BAD_ARG);
    if (0 == ip4addr.s_addr) return (SWAT_ERR_BAD_ARG);
    if (timeout_ms < 0) return (SWAT_ERR_BAD_ARG);

    pthread_mutex_lock(&swat_api_h->mux);

    if (SWAT_API_STATE_INIT != swat_api_h->state) {
        r = SWAT_ERR_ALREADY_SETUP;
    } else {
        l_swat_init_defaults(swat_api_h, 0);

        swat_api_h->ip4addr = ip4addr;
        swat_api_h->sb_id = sb_id;
        swat_api_h->ob_id = ob_id;
        swat_api_h->port = port;
        swat_api_h->telnum = telnum;
        swat_api_h->send_flag = send_flag;
        swat_api_h->recv_flag = recv_flag;
        swat_api_h->sort_flag = sort_flag;
        swat_api_h->hw_flag = hw_flag;
        swat_api_h->async_signal = async_signal;
        swat_api_h->timeout_ms = timeout_ms;
        swat_api_h->state = SWAT_API_STATE_CLOSED;
        l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_CONFIGURE);
        swat_api_h->worker_thr = worker_thr;
        r = SWAT_OK;
    }

    pthread_mutex_unlock(&swat_api_h->mux);
    return (r);
}

#define L_SWAT_API_MAX_EVENTS (10)

int l_swat_api_wait_event(SWAT_API_CLIENT* swat_api_h, int timeout_ms) {
    int i, numev, r;
    struct epoll_event evlist[L_SWAT_API_MAX_EVENTS];

    // process those events (make sure epfd is a valid socket and not -1)
    if (SWAT_INVALID_HANDLE == swat_api_h->epfd) return (SWAT_ERR_BAD_HANDLE);

    r = SWAT_OK;
    numev =
        epoll_wait(swat_api_h->epfd, &(evlist[0]), L_SWAT_API_MAX_EVENTS, timeout_ms);
    if (numev < 0) {
        if (NULL != swat_api_h->async_signal)
            if (swat_api_h->async_signal) r = SWAT_ERR_EXITING;
        if (SWAT_OK == r)
            if (EINTR != errno) r = SWAT_ERR_EPOLL_WAIT_FAILED;
    }
    // let's process all the events received, one by one, ignore any errors
    else {
        for (i = 0; i < numev; i++) l_swat_epoll_process_event(swat_api_h, evlist + i);
        if (0 == numev) r = SWAT_ERR_NO_NEW_DATA;
    }

    return (r);
}

int l_swat_api_connect(SWAT_API_CLIENT* swat_api_h) {
    struct sockaddr_in sin;
    struct epoll_event epev;
    int optval, r;

    // simple checks before mutex
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);

    // create nonblocking i/o socket
    swat_api_h->sock = socket(PF_INET, SOCK_STREAM | SOCK_NONBLOCK, 0);
    if (swat_api_h->sock < 0) {
        swat_api_h->sock = SWAT_INVALID_HANDLE;
        r = SWAT_ERR_SOCKET_FAILED;
        goto EEX0;
    }
    // set some options
    optval = 1;
    if (-1 ==
        setsockopt(swat_api_h->sock, SOL_SOCKET, SO_REUSEADDR, (void*)&optval,
                   sizeof(optval))) {  // we currently ignore SO_REUSEADDR failure ...
                                       // swat_log_warn("setsockopt(SO_REUSEADDR)
                                       // failed. Fast server restart impossible");
    }
    // notabene : TCP_USER_TIMEOUT works in synchronized state only (ESTABLISHED, etc
    // ...)
    r = swat_io_setkeepalive(swat_api_h->sock, 1, 0, 0, 0, swat_api_h->timeout_ms);
    if (SWAT_OK != r) goto EEX0;

    // create epoll socket
    swat_api_h->epfd = epoll_create(1);
    if (-1 == swat_api_h->epfd) {
        r = SWAT_ERR_EPOLL_CTL_FAILED;
        goto EEX0;
    }
    // attach i/o socket to epoll socket
    epev.data.fd = swat_api_h->sock;
    epev.events = EPOLLIN | EPOLLOUT | EPOLLHUP | EPOLLERR | EPOLLRDHUP;
    r = epoll_ctl(swat_api_h->epfd, EPOLL_CTL_ADD, swat_api_h->sock, &epev);
    if (r < 0) {
        r = SWAT_ERR_EPOLL_CTL_FAILED;
        goto EEX0;
    }
    // prepare for connect
    memset(&sin, 0, sizeof(sin));
    sin.sin_family = PF_INET;
    sin.sin_addr.s_addr = htonl(swat_api_h->ip4addr.s_addr);
    sin.sin_port = htons(swat_api_h->port);
    // finally let's do this connect() stuff ...
    r = connect(swat_api_h->sock, (struct sockaddr*)&sin, sizeof(sin));
    if (0 == r)  // connect succeeded right away (impossible on Linux though ...)
    {
        swat_api_h->state = SWAT_API_STATE_ESTABLISHED;
        l_swat_api_flag_events(swat_api_h,
                               SWAT_API_EVENT_CONNECT | SWAT_API_EVENT_ESTABLISHED);
        r = l_swat_submit_request(swat_api_h);  // so it is time to send REQUEST packet
    } else if (errno == EINPROGRESS)            // standard answer on Linux
    {
        swat_api_h->state = SWAT_API_STATE_CONNECTING;
        l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_CONNECT);
        r = l_swat_submit_request(swat_api_h);  // so it is time to send REQUEST packet
                                                //       r = SWAT_OK;
    } else  // general error with connect (out of memory/handles ??)
    {
        r = SWAT_ERR_CONNECT_FAILED;
    }
EEX0:
    if (SWAT_OK != r) {
        l_swat_close_sockets(swat_api_h, SWAT_API_STATE_ABORTED);
        l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_ERROR);
    }
    return (r);
}

int swat_api_start(SWAT_API_CLIENT* swat_api_h) {
    int r;

    // simple checks before mutex
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);

    r = SWAT_ERR_BAD_STATE;

    pthread_mutex_lock(&swat_api_h->mux);

    if (l_swat_is_closed(swat_api_h)) {
        if (0 == swat_api_h->connect_time) {
            swat_api_h->connect_time = swat_get_tai_time();
            r = SWAT_OK;
        }
    }

    if (SWAT_API_WORKER_THR_DISABLED != swat_api_h->worker_thr) {
        swat_api_h->worker_thr_ID = 0;
        if (pthread_create(&(swat_api_h->worker_thr_ID), NULL,
                           ((SWAT_API_WORKER_THR_DEFAULT == swat_api_h->worker_thr)
                                ? swat_api_worker_thr
                                : swat_api_h->worker_thr),
                           (void*)swat_api_h)) {
            swat_api_h->worker_thr_ID = 0;
            if (SWAT_OK == r) r = SWAT_ERR_PTHREAD_CREATE_FAILED;
        } else {
            l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_WRKR_START);
        }
    }

    pthread_mutex_unlock(&swat_api_h->mux);

    return (r);
}

int swat_api_clear_worker(SWAT_API_CLIENT* swat_api_h) {
    int r;

    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);

    pthread_mutex_lock(&swat_api_h->mux);

    if (0 == swat_api_h->worker_thr_ID) {
        r = SWAT_ERR_BAD_ARG;
    } else {
        r = SWAT_OK;
        swat_api_h->worker_thr_ID = 0;
        swat_api_h->worker_join_request = 0;
        l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_WRKR_STOP);
    }

    pthread_mutex_unlock(&swat_api_h->mux);

    return (r);
}

int l_swat_api_signal_worker(SWAT_API_CLIENT* swat_api_h) {
    int r;

    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);

    if (0 == swat_api_h->worker_thr_ID) {
        r = SWAT_ERR_BAD_ARG;
    } else {
        r = SWAT_OK;
        swat_api_h->worker_join_request = 1;
    }

    return (r);
}

int swat_api_check_worker(SWAT_API_CLIENT* swat_api_h) {
    int r;

    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);

    pthread_mutex_lock(&swat_api_h->mux);

    if (0 == swat_api_h->worker_thr_ID) {
        r = SWAT_OK;
    } else {
        r = SWAT_ERR_BAD_ARG;
    }

    pthread_mutex_unlock(&swat_api_h->mux);

    return (r);
}

int swat_api_wait_worker_cleared(SWAT_API_CLIENT* swat_api_h) {
    int r;

    for (;;) {
        // printf("joinreq = %d\n", swat_api_h->worker_join_request);
        r = swat_api_check_worker(swat_api_h);
        if (SWAT_ERR_BAD_ARG != r) break;
        swat_snooze();
    }
    return (r);
}

int swat_api_stop(SWAT_API_CLIENT* swat_api_h) {
    int r, sw;

    // simple checks before mutex
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);

    r = SWAT_ERR_BAD_STATE;
    sw = 0;

    l_swat_api_final_report(swat_api_h);
    pthread_mutex_lock(&swat_api_h->mux);

    switch (swat_api_h->state) {
        case SWAT_API_STATE_CONNECTING:
        case SWAT_API_STATE_ESTABLISHED:
            l_swat_close_sockets(swat_api_h, SWAT_API_STATE_CLOSED);
            l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_CLOSE);
        case SWAT_API_STATE_CLOSED:
        case SWAT_API_STATE_ABORTED:
        case SWAT_API_STATE_REFUSED:
        case SWAT_API_STATE_HANGUP:
            if (SWAT_OK == l_swat_api_signal_worker(swat_api_h)) sw = 1;
            if (swat_api_h->connect_time) {
                swat_api_h->connect_time = 0;
                r = SWAT_OK;
            }
            break;
    }

    pthread_mutex_unlock(&swat_api_h->mux);

    if (sw) swat_api_wait_worker_cleared(swat_api_h);

    return (r);
}

int swat_api_reset(SWAT_API_CLIENT* swat_api_h) {
    int r, sw;

    // simple checks before mutex
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    sw = 0;

    l_swat_api_final_report(swat_api_h);
    pthread_mutex_lock(&swat_api_h->mux);

    switch (swat_api_h->state) {
        case SWAT_API_STATE_CONNECTING:
        case SWAT_API_STATE_ESTABLISHED:
            l_swat_close_sockets(swat_api_h, SWAT_API_STATE_CLOSED);
            l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_CLOSE);
            if (SWAT_OK == l_swat_api_signal_worker(swat_api_h)) sw = 1;
        case SWAT_API_STATE_CLOSED:
        case SWAT_API_STATE_ABORTED:
        case SWAT_API_STATE_REFUSED:
        case SWAT_API_STATE_HANGUP:
            l_swat_init_defaults(swat_api_h, 0);
            l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_UNCONFIG);
        case SWAT_API_STATE_INIT:
            r = SWAT_OK;  // already in init/reset state
            break;
        default:
            r = SWAT_ERR_BAD_STATE;
            break;
    }

    pthread_mutex_unlock(&swat_api_h->mux);

    if (sw) swat_api_wait_worker_cleared(swat_api_h);

    return (r);
}

int swat_api_worker(SWAT_API_CLIENT* swat_api_h, int timeout_ms,
                    SWAT_API_STATUS* status) {
    int r, r2;
    SWAT_R1_HIGH_RES_TIMESTAMP curtime;

    // simple checks before mutex
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);

    curtime = swat_get_tai_time();
    r = SWAT_OK;

    pthread_mutex_lock(&swat_api_h->mux);

    switch (swat_api_h->state) {
        case SWAT_API_STATE_CLOSED:
        case SWAT_API_STATE_ABORTED:
        case SWAT_API_STATE_REFUSED:
        case SWAT_API_STATE_HANGUP:
            if (0 == swat_api_h->connect_time) {
                r = SWAT_ERR_TOO_EARLY;
                break;  // we are in idle mode
            }
            if (curtime < swat_api_h->connect_time) {
                r = SWAT_ERR_TOO_EARLY;
                break;  // too early for next connection attempt
            }
            r = l_swat_api_connect(swat_api_h);  // connect/reconnect
            break;

        case SWAT_API_STATE_CONNECTING:
            r = l_swat_async_socket_ok(swat_api_h);
            if (SWAT_OK != r) break;  // this is fatal error (handles also EXITING)
            // check if it's time to abort ongoing connection request
            if (swat_api_h->timeout_ms > 0)  // are timeouts enabled ?
            {
                if (curtime >= (swat_api_h->connect_time +
                                swat_api_h->timeout_ms * SWAT_API_MS_TIME_T_TICKS)) {
                    l_swat_close_sockets(swat_api_h, SWAT_API_STATE_ABORTED);
                    l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_ABORT);
                }
            }
            // process events, handles disconnects (if any)
            r = l_swat_api_wait_event(swat_api_h, timeout_ms);
            break;

        case SWAT_API_STATE_ESTABLISHED:
            r = l_swat_async_socket_ok(swat_api_h);
            if (SWAT_OK != r) break;  // this is fatal error (handles also EXITING)
            if (swat_api_h->debug_flag & SWAT_API_DEBUG_TEST_RECONN) {
                if (curtime >= (swat_api_h->connect_time +
                                swat_api_h->timeout_ms * SWAT_API_MS_TIME_T_TICKS)) {
                    l_swat_close_sockets(swat_api_h, SWAT_API_STATE_ABORTED);
                    l_swat_api_flag_events(swat_api_h, SWAT_API_EVENT_ABORT);
                    r = l_swat_api_connect(swat_api_h);  // immediate connect/reconnect
                }
            }
            r2 = SWAT_OK;
            if (swat_api_h->camevlen >
                0)  // then check if it's time to send out outstanding triggers
            // ok, so we will be creating new packet. Errors (like SWAT_ERR_BUFFER_FULL)
            // handled by submit_processor
            {
                if (curtime >=
                    (swat_api_h->camevbuf[0].trigger_time + SWAT_API_TBINSIZE)) {
                    r2 = l_swat_flush_events(swat_api_h);
                }  // likely buffer full errors only
            }
            // process events, handles disconnects (if any)
            r = l_swat_api_wait_event(swat_api_h, timeout_ms);
            if (SWAT_OK == r) r = r2;
            break;

        case SWAT_API_STATE_INIT:  // we can't do anything if not configured
            break;
        default:
            r = SWAT_ERR_BAD_STATE;  // internal error
            break;
    }
    // store current API stats
    if (NULL != status) l_swat_api_get_status(swat_api_h, status);

    swat_api_h->events = SWAT_API_EVENT_NULL;

    if ((SWAT_OK == r) || (SWAT_ERR_NO_NEW_DATA == r) || (SWAT_ERR_BAD_STATE == r) ||
        (SWAT_ERR_TOO_EARLY == r))
        if (NULL != swat_api_h->async_signal)
            if (0 != *(swat_api_h->async_signal)) r = SWAT_ERR_EXITING;

    if ((SWAT_OK == r) || (SWAT_ERR_NO_NEW_DATA == r) || (SWAT_ERR_BAD_STATE == r) ||
        (SWAT_ERR_TOO_EARLY == r))
        if (swat_api_h->worker_join_request) r = SWAT_ERR_EXITING;

    pthread_mutex_unlock(&swat_api_h->mux);

    return (r);
}

void* swat_api_worker_thr(void* arg) {
    SWAT_API_CLIENT* swat_api_h;
    int r;

    swat_api_h = (SWAT_API_CLIENT*)arg;
    if (NULL == swat_api_h) return (NULL);

    for (;;) {
        r = swat_api_worker(swat_api_h, 0, NULL);
        if (SWAT_OK == r) continue;
        if (SWAT_ERR_EXITING == r) break;
        swat_snooze();
    }

    swat_api_clear_worker(swat_api_h);
    return (NULL);
}

const char* swat_api_log_type2str(int type) {
    switch (type) {
        case SWAT_API_LOG_DEBUG:
            return ("DEBUG");
        case SWAT_API_LOG_INFO:
            return ("INFO ");
        case SWAT_API_LOG_WARNING:
            return ("WARN ");
        case SWAT_API_LOG_ERROR:
            return ("ERROR");
        case SWAT_API_LOG_ALERT:
            return ("ALERT");
    }
    return ("UKNWN");
}

int swat_api_log(int type, char* msg) {
    time_t curtime;
    struct tm curgmtime;

    curtime = time(NULL);
    gmtime_r(&curtime, &curgmtime);
    fprintf(stderr, "%5.5s %04d-%02d-%02dT%02d:%02d:%02d [%u:%08X] %s\n",
            swat_api_log_type2str(type), curgmtime.tm_year + 1900, curgmtime.tm_mon + 1,
            curgmtime.tm_mday, curgmtime.tm_hour, curgmtime.tm_min, curgmtime.tm_sec,
            (unsigned)getpid(), (unsigned)pthread_self(), (msg ? msg : ""));
    return (SWAT_OK);
}

int swat_api_log_debug(char* msg) { return (swat_api_log(SWAT_API_LOG_DEBUG, msg)); }

int swat_api_log_info(char* msg) { return (swat_api_log(SWAT_API_LOG_INFO, msg)); }

int swat_api_log_warn(char* msg) { return (swat_api_log(SWAT_API_LOG_WARNING, msg)); }

int swat_api_log_error(char* msg) { return (swat_api_log(SWAT_API_LOG_ERROR, msg)); }

int swat_api_log_alert(char* msg) { return (swat_api_log(SWAT_API_LOG_ALERT, msg)); }

int l_swat_api_debug_msg(SWAT_API_CLIENT* swat_api_h, int type, char* msg) {
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);

    if (SWAT_API_LOGGER_DISABLED == swat_api_h->debug_logger) return (SWAT_OK);
    if (SWAT_API_LOGGER_DEFAULT == swat_api_h->debug_logger)
        return (swat_api_log(type, msg));
    return ((swat_api_h->debug_logger)(type, msg));
}

int l_swat_api_mutex_debug_msg(SWAT_API_CLIENT* swat_api_h, int type, char* msg) {
    int r;

    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);

    pthread_mutex_lock(&swat_api_h->mux);

    if (SWAT_API_LOGGER_DISABLED == swat_api_h->debug_logger) {
        r = SWAT_OK;
        pthread_mutex_unlock(&swat_api_h->mux);
    } else if (SWAT_API_LOGGER_DEFAULT == swat_api_h->debug_logger) {
        pthread_mutex_unlock(
            &swat_api_h->mux);  // default_logger does not use swat_api_h ...
        r = swat_api_log(type, msg);
    } else {
        r = (swat_api_h->debug_logger)(type, msg);
        pthread_mutex_unlock(&swat_api_h->mux);
    }
    return (r);
}

int l_swat_api_flag_events(SWAT_API_CLIENT* swat_api_h, int myevents) {
    char buf[SWAT_API_LOGGER_MAX_MSG];

    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);

    swat_api_h->events |= myevents;

    if (0 == (swat_api_h->debug_flag & SWAT_API_DEBUG_EVENT)) return (SWAT_OK);
    if (SWAT_API_EVENT_NULL == myevents) return (SWAT_OK);

    snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "EVENT: %s%s%s%s%s%s%s%s%s%s%s",
             ((myevents & SWAT_API_EVENT_ERROR) ? "ERROR " : ""),
             ((myevents & SWAT_API_EVENT_CONNECT) ? "CONNECTING " : ""),
             ((myevents & SWAT_API_EVENT_ESTABLISHED) ? "ESTABLISHED " : ""),
             ((myevents & SWAT_API_EVENT_ABORT) ? "ABORTED " : ""),
             ((myevents & SWAT_API_EVENT_HANGUP) ? "HANGUP " : ""),
             ((myevents & SWAT_API_EVENT_CLOSE) ? "CLOSED " : ""),
             ((myevents & SWAT_API_EVENT_REFUSED) ? "REFUSED " : ""),
             ((myevents & SWAT_API_EVENT_CONFIGURE) ? "CONFIGURE " : ""),
             ((myevents & SWAT_API_EVENT_UNCONFIG) ? "UNCONFIG " : ""),
             ((myevents & SWAT_API_EVENT_WRKR_START) ? "WRKR_START " : ""),
             ((myevents & SWAT_API_EVENT_WRKR_STOP) ? "WRKR_STOP " : ""));
    return (l_swat_api_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf));
}

const char* l_swat_api_clktype2str(int clktype) {
    switch (clktype) {
        case CLOCK_TAI:
            return ("CLOCK_TAI");
        case CLOCK_REALTIME:
            return ("CLOCK_REALTIME");
    }
    return ("CLOCK_UNKNOWN");
}

// the function calibrates system clock and TAI time.
// if tai_flag is set, the function attempts to use CLOCK_TAI
// if not supported or unusable, the function falls back to
// CLOCK_REALTIME and uses leap_secs to compensate for leap
// seconds difference between UTC and TAI.
// result is stored in global structure swat_clock_calib

int swat_api_calibrate_tai(SWAT_API_CLIENT* swat_api_h, int tai_flag, int leap_secs) {
    char buf[SWAT_API_LOGGER_MAX_MSG];
    int r, eff_ls, eff_clktype;
    SWAT_CLK_CALIB calib;

    eff_clktype = CLOCK_REALTIME;
    eff_ls = leap_secs;
    if (tai_flag) {
        r = swat_tai_clock_valid(&eff_ls);
        if (SWAT_OK == r) {
            if (NULL != swat_api_h) {
                if (swat_api_h->debug_flag & SWAT_API_DEBUG_CLOCK) {
                    snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                             "CLOCK: kernel's CLOCK_TAI is OK (leaps=%d)", eff_ls);
                    l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
                }
            }
            eff_clktype = CLOCK_TAI;
            eff_ls = 0;  // since kernel's TAI clock already includes leaps seconds, we
                         // set leaps=0
        } else {
            if (NULL != swat_api_h) {
                if (swat_api_h->debug_flag & SWAT_API_DEBUG_CLOCK) {
                    snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                             "CLOCK: requested CLOCK_TAI unusable (err=%d)", r);
                    l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_WARNING, buf);
                    snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                             "CLOCK: retrying with: CLOCK_REALTIME(leaps=%d). YMMV ...",
                             eff_ls);
                    l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
                }
            }
        }
    }
    // require accuracy of at least 1millisec (usually is ~ 200ns)
    r = swat_clock_calibrate(eff_clktype, eff_ls, SWAT_API_MS_TIME_T_TICKS, &calib);
    if (NULL != swat_api_h) {
        if (SWAT_OK != r) {
            if (swat_api_h->debug_flag & SWAT_API_DEBUG_CLOCK) {
                snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                         "CLOCK: unable to calibrate kernel clock (err=%d)", r);
                l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_ERROR, buf);
            }
        } else {
            if (swat_api_h->debug_flag & SWAT_API_DEBUG_CLOCK) {
                snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                         "CLOCK: calibrated: clktype=%s (%d), leap_seconds=%d",
                         l_swat_api_clktype2str(calib.clktype), calib.clktype,
                         calib.leapsecs);
                l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
                snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                         "CLOCK: calibrated: accy=%lu [nsec], offset=%lu [nsec]",
                         calib.accy / SWAT_API_NS_TIME_T_TICKS,
                         calib.offset / SWAT_API_NS_TIME_T_TICKS);
                l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
            }
            if ((CLOCK_REALTIME == calib.clktype) && (0 == calib.leapsecs)) {
                if (swat_api_h->debug_flag & SWAT_API_DEBUG_CLOCK) {
                    snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                             "CLOCK: CLOCK_REALTIME + ZERO leap secs. Did you forget: "
                             "-T -L 37 \?\?\?");
                    l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_WARNING, buf);
                    snprintf(buf, SWAT_API_LOGGER_MAX_MSG,
                             "CLOCK: with ZERO leap secs TAI readouts will be wrong (= "
                             "UTC). YOU HAVE BEEN WARNED !");
                    l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_WARNING, buf);
                }
            }
        }
    }
    return (r);
}

int l_swat_api_final_report(SWAT_API_CLIENT* swat_api_h) {
    SWAT_API_STATUS mystatus;
    char buf[SWAT_API_LOGGER_MAX_MSG];
    int r;

    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    r = swat_api_get_status(swat_api_h, &mystatus);
    if ((SWAT_OK == r) && (mystatus.debug_flag & SWAT_API_DEBUG_FINAL_REPORT)) {
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG,
                                   "REPORT: ========= SWAT_API final report =========");
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: debug_flag      = 0x%04x",
                 mystatus.debug_flag);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: telnum          = %d",
                 mystatus.telnum);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: state           = %d (%s)",
                 mystatus.state, l_swat_state2str(mystatus.state));
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: events          = 0x%04x",
                 mystatus.events);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: connnect_time   = %lu",
                 static_cast<unsigned long>(mystatus.connect_time));
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: timeout_ms      = %d",
                 mystatus.timeout_ms);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: wrbufitems      = %d",
                 mystatus.wrbufitems);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: camev_inbuf     = %d",
                 mystatus.camev_inbuf);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: camev_bufsize   = %d",
                 mystatus.camev_bufsize);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: camev_nfull     = %d",
                 mystatus.camev_nfull);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: camev_ngood     = %d",
                 mystatus.camev_ngood);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: camev_inbufmax  = %d",
                 mystatus.camev_inbufmax);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: arrev_inbuf     = %d",
                 mystatus.arrev_inbuf);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: arrev_bufsize   = %d",
                 mystatus.arrev_bufsize);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: arrev_nduplic   = %d",
                 mystatus.arrev_nduplicate);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: arrev_nfull     = %d",
                 mystatus.arrev_nfull);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: arrev_npositive = %d",
                 mystatus.arrev_npositive);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: arrev_nnegative = %d",
                 mystatus.arrev_nnegative);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        snprintf(buf, SWAT_API_LOGGER_MAX_MSG, "REPORT: arrev_inbufmax  = %d",
                 mystatus.arrev_inbufmax);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG, buf);
        l_swat_api_mutex_debug_msg(swat_api_h, SWAT_API_LOG_DEBUG,
                                   "REPORT: =========================================");
    }
    return (r);
}

// DEPRECATED FUNCTIONS

int swat_api_get_state(SWAT_API_CLIENT* swat_api_h, int* state) {
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    if (NULL == state) return (SWAT_ERR_NUL_PTR);  // already freed ??

    pthread_mutex_lock(&swat_api_h->mux);
    *state = swat_api_h->state;
    pthread_mutex_unlock(&swat_api_h->mux);
    return (SWAT_OK);
}

int swat_api_close(SWAT_API_CLIENT* swat_api_h) {
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    l_swat_api_final_report(swat_api_h);
    pthread_mutex_lock(&swat_api_h->mux);
    l_swat_close_sockets(swat_api_h, SWAT_API_STATE_CLOSED);
    pthread_mutex_unlock(&swat_api_h->mux);
    return (SWAT_OK);
}

int swat_api_setup(SWAT_API_CLIENT* swat_api_h, struct in_addr ip4addr, int port,
                   int telnum, int send_flag, int recv_flag, int sort_flag, int hw_flag,
                   int timeout_ms, int* async_signal) {
    int r;

    // simple checks before mutex
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    if ((telnum < 0) || (telnum >= SWAT_API_MAXTELS)) return (SWAT_ERR_BAD_ARG);
    if (port <= 0) return (SWAT_ERR_BAD_ARG);
    if (0 == ip4addr.s_addr) return (SWAT_ERR_BAD_ARG);
    if (timeout_ms < 0) return (SWAT_ERR_BAD_ARG);

    pthread_mutex_lock(&swat_api_h->mux);

    if (SWAT_API_STATE_INIT != swat_api_h->state) {
        r = SWAT_ERR_ALREADY_SETUP;
    } else {
        l_swat_init_defaults(swat_api_h, 0);

        swat_api_h->ip4addr = ip4addr;
        swat_api_h->port = port;
        swat_api_h->telnum = telnum;
        swat_api_h->send_flag = send_flag;
        swat_api_h->recv_flag = recv_flag;
        swat_api_h->sort_flag = sort_flag;
        swat_api_h->hw_flag = hw_flag;
        swat_api_h->async_signal = async_signal;
        swat_api_h->timeout_ms = timeout_ms;
        swat_api_h->state = SWAT_API_STATE_CLOSED;

        swat_api_h->connect_time = swat_get_tai_time();

        r = l_swat_api_connect(swat_api_h);
    }

    if (SWAT_OK != r) l_swat_close_sockets(swat_api_h, SWAT_API_STATE_ABORTED);
    pthread_mutex_unlock(&swat_api_h->mux);
    return (r);
}

int swat_api_get_wrbufitems(SWAT_API_CLIENT* swat_api_h, int* wrbufitems) {
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);
    if (NULL == wrbufitems) return (SWAT_ERR_NUL_PTR);  // already freed ??

    pthread_mutex_lock(&swat_api_h->mux);
    *wrbufitems = ((swat_api_h->wrbufitems || swat_api_h->camevlen) ? 1 : 0);
    pthread_mutex_unlock(&swat_api_h->mux);
    return (SWAT_OK);
}

int swat_api_get_arrev_stats(SWAT_API_CLIENT* swat_api_h, int* ndups, int* nfull,
                             int* ngood) {
    //  simple checks before mutex
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);

    pthread_mutex_lock(&swat_api_h->mux);

    if (NULL != ndups) *ndups = swat_api_h->arrev_nduplicate;
    if (NULL != nfull) *nfull = swat_api_h->arrev_nfull;
    if (NULL != ngood)
        *ngood = swat_api_h->arrev_npositive + swat_api_h->arrev_nnegative;

    pthread_mutex_unlock(&swat_api_h->mux);

    return (SWAT_OK);
}

// function waits for the next epoll event on i/o socket
// ARGS: swat_api_h - pointer to SWAT client structure
// RETURN VALUE: standard error code (usually SWAT_OK or SWAT_ERR_EXITING)
// NOTE: due to Linux's pthread_mutex implementation, do not execute
// swat_api_wait_event in a tight loop (without sleep/yield from time to time)
// as this may block other threads from acquiring the mutex.
// function returns some statistics about its internal buffers
// Specifically, application is guaranteed to successfully call
// swat_api_read_array_event() up to read_array_events times (and each
// call will return new array trigger record) and without error.
// ditto for swat_api_write_camera_event() : it may be called up to
// write_camera_events times, without worrying about buffers overflows, etc ...
int swat_api_wait_event(SWAT_API_CLIENT* swat_api_h, int timeout_millisec,
                        int* read_array_events, int* write_camera_events) {
    int i, numev, r;
    struct epoll_event evlist[10];
    SWAT_R1_HIGH_RES_TIMESTAMP curtime;

    // simple checks before mutex
    if (NULL == swat_api_h) return (SWAT_ERR_NUL_PTR);

    pthread_mutex_lock(&swat_api_h->mux);

    r = l_swat_is_socket_ok(swat_api_h);
    if (SWAT_OK == r)  // first check async signalling
    {
        if (NULL != swat_api_h->async_signal)
            if (0 != *(swat_api_h->async_signal))
                r = SWAT_ERR_EXITING;  // signal immediate exit
    }
    if (SWAT_OK == r) {
        curtime = swat_get_tai_time();
        if (swat_api_h->camevlen >
            0)  // then check if it's time to send out outstanding triggers
        {  // ok, so we will be creating new packet. Errors (like SWAT_ERR_BUFFER_FULL)
           // handled by submit_processor
            if (curtime >= (swat_api_h->camevbuf[0].trigger_time + SWAT_API_TBINSIZE)) {
                r = l_swat_flush_events(swat_api_h);
            }  // likely buffer full errors only
        }
    }
    if (SWAT_OK == r)  // let's do some basic housekeeping ...
    {
        if (SWAT_API_STATE_CONNECTING ==
            swat_api_h->state)  // first if we are still connect()-ing
        {                       // check if it's time to abort
            if (curtime >= (swat_api_h->connect_time +
                            swat_api_h->timeout_ms * SWAT_API_MS_TIME_T_TICKS)) {
                l_swat_close_sockets(swat_api_h, SWAT_API_STATE_ABORTED);
            }
        }

        if (l_swat_is_closed(swat_api_h))  // connection has been shutdown
        {
            if ((0 == swat_api_h->wrbufitems)    // no more writes
                && (0 == swat_api_h->camevlen)   // all the camevs have been written
                && (0 == swat_api_h->arrevlen))  // all the arrevs have been read
            {
                r = SWAT_ERR_EXITING;
            }
        }
    }
    // finally process those events (make sure epfd is a valid socket and not -1
    if ((SWAT_OK == r) && (SWAT_INVALID_HANDLE != swat_api_h->epfd)) {
        numev = epoll_wait(swat_api_h->epfd, &(evlist[0]), 10, timeout_millisec);
        if (numev < 0) {
            if (NULL != swat_api_h->async_signal)
                if (swat_api_h->async_signal) r = SWAT_ERR_EXITING;
            r = errno;
            if (EINTR != r) r = SWAT_ERR_EPOLL_WAIT_FAILED;
        }
        // let's process all the events received, one by one, ignore any errors
        else {
            for (i = 0; i < numev; i++)
                l_swat_epoll_process_event(swat_api_h, evlist + i);
            if (0 == numev) r = SWAT_ERR_NO_NEW_DATA;
        }
    }
    // return how many array events are available for reading
    if (NULL != read_array_events) *read_array_events = swat_api_h->arrevlen;
    // return how many camera events can be written to internal buffers
    if (NULL != write_camera_events)
        *write_camera_events = (SWAT_API_CAMEVS_MAXLEN - swat_api_h->camevlen);

    pthread_mutex_unlock(&swat_api_h->mux);

    return (r);
}
