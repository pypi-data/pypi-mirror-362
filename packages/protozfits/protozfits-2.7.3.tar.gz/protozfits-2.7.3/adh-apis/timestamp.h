#ifndef TIMESTAMP_H_
#define TIMESTAMP_H_

#include <cstdint>

namespace CTA
{
    /**
        @struct HighResTimestamp 
        @brief Handling and storage of precise, CTA-style timestamps
    */
    struct HighResTimestamp
    {
        /// Default constructor. Cannot construct unitialized values. Should we ? 
        HighResTimestamp(uint32_t sec, uint32_t quarternanosec) : s{sec}, qns{quarternanosec} {}

        uint32_t s;   ///< Seconds in TAI reference. Not yet final: may become UTC after all
        uint32_t qns; ///< Quarter nano-seconds elapsed since last second
    };

    /** @brief Compares full and fractional part of the timestamps for exact equality. */
    inline bool operator==(const CTA::HighResTimestamp &lhs, const CTA::HighResTimestamp &rhs) {
        return lhs.s == rhs.s && lhs.qns == rhs.qns;
    }

    /**
        @typedef LowResTimestamp
        @brief Handling and storage of low-resolution timestamps
    */
    typedef double LowResTimestamp;
};//namespace CTA

#endif //TIMESTAMP_H_
