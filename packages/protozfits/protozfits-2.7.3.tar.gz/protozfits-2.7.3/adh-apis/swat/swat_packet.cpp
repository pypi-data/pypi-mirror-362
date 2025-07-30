/*
 * swat_packet.c
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

#include "swat_packet.h"

#include "swat_api.h"
#include "swat_errors.h"

int swat_pkthdr_check_common(SWAT_PACKET_HEADER* pkthdr) {
    if (NULL == pkthdr) return (SWAT_ERR_NUL_PTR);
    if (SWAT_API_PKT_MAGIC0 != pkthdr->magic[0]) return (SWAT_ERR_BAD_MAGIC0);
    if (SWAT_API_PKT_MAGIC1 != pkthdr->magic[1]) return (SWAT_ERR_BAD_MAGIC1);
    if ((pkthdr->pktype < SWAT_API_PKTYPE_MIN) ||
        (pkthdr->pktype > SWAT_API_PKTYPE_MAX))
        return (SWAT_ERR_BAD_PKTYPE);
    if (pkthdr->tel_id >= SWAT_API_MAXTELS) return (SWAT_ERR_BAD_CSID);
    if ((SWAT_API_PKTYPE_NULL == pkthdr->pktype) && (0 != pkthdr->paylen))
        return (SWAT_ERR_BAD_PAYLEN);
    if ((SWAT_API_PKTYPE_REQUEST == pkthdr->pktype) &&
        (sizeof(SWAT_PACKET_CONNECT) != pkthdr->paylen))
        return (SWAT_ERR_BAD_PAYLEN);
    if (pkthdr->paylen >= SWAT_API_PKT_MAXLEN) return (SWAT_ERR_BAD_PAYLEN);
    return (SWAT_OK);
}

int swat_pkthdr_check_send(SWAT_PACKET_HEADER* pkthdr) {
    int r;

    r = swat_pkthdr_check_common(pkthdr);
    if (SWAT_OK != r) return (r);
    if (SWAT_API_PKTYPE_ARREVS == pkthdr->pktype) return (SWAT_ERR_BAD_PKTYPE);
    if (SWAT_API_PKTYPE_ACCEPT == pkthdr->pktype) return (SWAT_ERR_BAD_PKTYPE);
    if ((SWAT_API_PKTYPE_REQUEST == pkthdr->pktype) && (0 != pkthdr->bunch_id))
        return (SWAT_ERR_BAD_ARG);
    if ((SWAT_API_PKTYPE_REQUEST != pkthdr->pktype) && (0 == pkthdr->bunch_id))
        return (SWAT_ERR_BAD_ARG);
    return (SWAT_OK);
}

int swat_pkthdr_check_recv(SWAT_PACKET_HEADER* pkthdr) {
    int r;

    r = swat_pkthdr_check_common(pkthdr);
    if (SWAT_OK != r) return (r);
    if (SWAT_API_PKTYPE_CAMEVS == pkthdr->pktype) return (SWAT_ERR_BAD_PKTYPE);
    if (SWAT_API_PKTYPE_REQUEST == pkthdr->pktype) return (SWAT_ERR_BAD_PKTYPE);
    return (SWAT_OK);
}

int swat_pkthdrtype_check_send(SWAT_PACKET_HEADER* pkthdr, int pktype) {
    int r;

    if (SWAT_OK != (r = swat_pkthdr_check_send(pkthdr))) return (r);
    if (pktype != pkthdr->pktype) return (SWAT_ERR_BAD_PKTYPE);
    return (r);
}

int swat_pkthdrtype_check_recv(SWAT_PACKET_HEADER* pkthdr, int pktype) {
    int r;

    if (SWAT_OK != (r = swat_pkthdr_check_recv(pkthdr))) return (r);
    if (pktype != pkthdr->pktype) return (SWAT_ERR_BAD_PKTYPE);
    return (r);
}

int swat_pkt_arrev_log(SWAT_PACKET_HEADER* ph) {
    //   char	 buf[SWAT_MAX_MSG_LEN];
    //   int	 nct;

    //   nct = ph->paylen / sizeof(SWAT_PACKET_R1_EVENT_REQUEST);
    //   snprintf(buf, SWAT_MAX_MSG_LEN, "PKTHDR: pktype=%d, csid=%d, bunch_id=%d,
    //   paylen=%d, NCT=%d",
    //                ph->pktype, ph->csid, ph->bunch_id, ph->paylen, nct);
    //   swat_log_info(buf);

    return (SWAT_OK);
}

uint8_t swat_r1_type_to_dl0_type(uint8_t r1_trigger_type, bool triggered) {
    switch (r1_trigger_type) {
        case SWAT_PACKET_R1_TRIGGER_TYPE::T_0_STORE_EXCLUDE:
            return SWAT_DATA_DL0_EVENT_TYPE::T_0_LOCAL_EVENT;
        case SWAT_PACKET_R1_TRIGGER_TYPE::T_1_STORE_INCLUDE:
            if (triggered) {
                return SWAT_DATA_DL0_EVENT_TYPE::T_1_SUBARRAY_EVENT;
            } else {
                return SWAT_DATA_DL0_EVENT_TYPE::T_0_LOCAL_EVENT;
            }
        case SWAT_PACKET_R1_TRIGGER_TYPE::T_2_ACADA_REQUEST:
            return SWAT_DATA_DL0_EVENT_TYPE::T_2_SWAT_REQUEST;
        case SWAT_PACKET_R1_TRIGGER_TYPE::T_3_SWAT_DECISION:
            return SWAT_DATA_DL0_EVENT_TYPE::T_1_SUBARRAY_EVENT;
        default:
            return 255;
    }
}
