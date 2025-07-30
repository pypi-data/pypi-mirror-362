/*
 * swat_packet.h
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

#ifndef SWAT_PACKET_H
#define SWAT_PACKET_H

#include "swat_defs.h"

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

#define SWAT_API_PKT_MAGIC0 (0x41)
#define SWAT_API_PKT_MAGIC1 (0x54)

#define SWAT_API_PKTYPE_NULL (0)
#define SWAT_API_PKTYPE_REQUEST (1)
#define SWAT_API_PKTYPE_ACCEPT (2)
#define SWAT_API_PKTYPE_CAMEVS (3)
#define SWAT_API_PKTYPE_ARREVS (4)

#define SWAT_API_PKTYPE_MIN (SWAT_API_PKTYPE_NULL)
#define SWAT_API_PKTYPE_MAX (SWAT_API_PKTYPE_ARREVS)

/*
Basic chunk of data exchanged between SWAT and CSP/CDTS is packet.
Packet format is :

   packet header    (SWAT_PACKET_HEADER - 12 bytes)
   packet payload   (variable number of bytes - lenght specified in packet header)

Types of packets :

SWAT_API_PKTYPE_NULL	- no payload  (0 bytes - SWAT accepts and ignores NULL packets
anytime, excepting very first packet which should be of type SWAT_API_PKTYPE_REQUEST)
SWAT_API_PKTYPE_REQUEST	- payload is SWAT_PKT_REQUEST - very first packet during
session. Accepted only once.
SWAT_API_PKTYPE_ACCEPT	- reply sent back to CSP/CDTS once connection is accepted by
SWAT. If connection is rejected no packet is sent and close() is called
SWAT_API_PKTYPE_CAMEVS	- payload: SWAT_API_PKT_CAMEVHDR + n * SWAT_PACKET_R1_TRIGGER.
                          Sent periodically by CSP/CDTS to SWAT
SWAT_API_PKTYPE_ARREVS	- payload: n * SWAT_PACKET_R1_EVENT_REQUEST. Sent periodically
by SWAT to CSP.

Packet sequencing :

CSP/CDTS -> SWAT :

packet(SWAT_API_PKTYPE_REQUEST, seqnum=0)
packet(SWAT_API_PKTYPE_CAMEVS, seqnum=1)
packet(SWAT_API_PKTYPE_CAMEVS, seqnum=2)
packet(SWAT_API_PKTYPE_CAMEVS, seqnum=3)
[...]

SWAT -> CSP :

packet(SWAT_API_PKTYPE_ACCEPT, seqnum=0)
packet(SWAT_API_PKTYPE_ARREVS, seqnum=1)
packet(SWAT_API_PKTYPE_ARREVS, seqnum=2)
packet(SWAT_API_PKTYPE_ARREVS, seqnum=3)

*/

typedef struct SWAT_PACKET_HEADER_STRUCT {
    // Fields related to technical implementation of SWAT protocol
    unsigned char magic[2];
    unsigned char pktype;
    unsigned int paylen;

    // R1/Event/Telescope/TriggerBunch and R1/Event/Subarray/EventRequestBunch fields
    uint16_t tel_id;
    uint64_t bunch_id;      // bunch_id for TriggerBunch,
                            // event_request_bunch_id for EventRequestBunch
    uint64_t num_in_bunch;  // num_triggers_in_bunch for TriggerBunch,
                            // num_requests_in_bunch for EventRequestBunch

} SWAT_PACKET_HEADER;

typedef struct SWAT_PACKET_CONNECT_STRUCT {
    // Fields related to technical implementation of SWAT protocol
    unsigned char send_flag;  // CSP or CDTS --> SWAT
    unsigned char recv_flag;  // SWAT --> CSP
    unsigned char sort_flag;  // CSP/CDTS always sends its trigger strictly sorted
    unsigned char hw_flag;    // client provides camera triggers from another H/W based
                              // array trigger

    // R1/Event/Telescope/DataStream fields
    uint16_t tel_id;
    uint64_t sb_id;
    uint64_t obs_id;
    // waveform_scale, waveform_offset not relevant to SWAT communication
    // see data_model directory for implementation of structures used for Camera <-> SDH
    // communication

} SWAT_PACKET_CONNECT;

typedef struct SWAT_PACKET_ACCEPT_STRUCT {
    uint16_t subarray_id;
    uint64_t sb_id;
    uint64_t obs_id;
} SWAT_PACKET_ACCEPT;

enum SWAT_PACKET_R1_TRIGGER_TYPE : uint8_t {
    T_0_STORE_EXCLUDE = 0,
    T_1_STORE_INCLUDE = 1,
    T_2_ACADA_REQUEST = 2,
    T_3_SWAT_DECISION = 3
};

namespace SWAT_PACKET_R1_TRIGGER_MASK {
const uint16_t B_0_MONO = 1;
const uint16_t B_1_STEREO = 1 << 1;
const uint16_t B_2_CALIBRATION = 1 << 2;
const uint16_t B_3_PHOTO_ELECTRON = 1 << 3;
const uint16_t B_4_SOFTWARE = 1 << 4;
const uint16_t B_5_PEDESTAL = 1 << 5;
const uint16_t B_6_SLOW_CONTROL = 1 << 6;
const uint16_t B_8_NEIGHBOUR_1 = 1 << 8;
const uint16_t B_9_NEIGHBOUR_2 = 1 << 9;
const uint16_t B_10_NEIGHBOUR_3 = 1 << 10;
const uint16_t B_11_NEIGHBOUR_4 = 1 << 11;
const uint16_t B_12_NEIGHBOUR_5 = 1 << 12;
const uint16_t B_13_NEIGHBOUR_6 = 1 << 13;
const uint16_t B_14_NEIGHBOUR_7 = 1 << 14;
}  // namespace SWAT_PACKET_R1_TRIGGER_MASK

typedef struct SWAT_PACKET_R1_TRIGGER_STRUCT {
    uint64_t trigger_id;
    uint64_t bunch_id;
    uint8_t trigger_type;
    SWAT_R1_HIGH_RES_TIMESTAMP trigger_time;
    bool readout_requested;
    bool data_available;
    uint16_t hardware_stereo_trigger_mask;

} SWAT_PACKET_R1_TRIGGER;

typedef struct SWAT_PACKET_R1_EVENT_REQUEST_STRUCT {
    uint64_t assigned_event_id;
    uint64_t event_request_bunch_id;
    SWAT_PACKET_R1_TRIGGER requested;
    bool negative_flag;

} SWAT_PACKET_R1_EVENT_REQUEST;

enum SWAT_DATA_DL0_EVENT_TYPE : uint8_t {
    T_0_LOCAL_EVENT = 0,
    T_1_SUBARRAY_EVENT = 1,
    T_2_SWAT_REQUEST = 2
};

int swat_pkthdr_check_common(SWAT_PACKET_HEADER* pkthdr);
int swat_pkthdr_check_send(SWAT_PACKET_HEADER* pkthdr);
int swat_pkthdr_check_recv(SWAT_PACKET_HEADER* pkthdr);
int swat_pkthdrtype_check_send(SWAT_PACKET_HEADER* pkthdr, int pktype);
int swat_pkthdrtype_check_recv(SWAT_PACKET_HEADER* pkthdr, int pktype);
int swat_pkt_arrev_log(SWAT_PACKET_HEADER* ph);
uint8_t swat_r1_type_to_dl0_type(uint8_t r1_trigger_type, bool triggered);

#ifdef __cplusplus
}
#endif

#endif /* SWAT_PACKET_H */
