#ifndef _CHECKSUM_H_
#define _CHECKSUM_H_

/**
 * @file Checksum.h
 *
 *  @brief computes the FITS checksum from a stream of bytes
 *  Created on: Nov 5, 2013
 *      Author: lyard-bretz
 */

#include <arpa/inet.h>
#include <stdint.h>
#include <vector>
#include <string>

class Checksum
{
public:
    uint64_t buffer;

    void reset();
    Checksum();
    Checksum(const Checksum &sum);
    Checksum(uint64_t v);

    uint32_t val() const;
    bool     valid() const;
    void    HandleCarryBits();

    Checksum& operator=(const Checksum&) = default;
    Checksum &operator+=(const Checksum &sum);
    Checksum operator+(Checksum sum) const;

    bool add(const char *buf, size_t len, bool big_endian = true);
    void addLoopSwapping(const uint16_t *sbuf, const uint16_t *end, uint32_t* hilo);
    void addLoop(const uint16_t *sbuf, const uint16_t *end, uint32_t* hilo);
    bool add(const std::vector<char> &v, bool big_endian = true);
    std::string str(bool complm=true) const;
};

#endif
