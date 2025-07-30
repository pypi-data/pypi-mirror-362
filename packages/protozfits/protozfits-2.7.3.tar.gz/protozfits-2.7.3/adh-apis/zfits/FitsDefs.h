/**
 *
 * @file FitsDefs.h
 *
 * @brief Global FITS header
 *
 * Author: lyard-bretz
 *
 */

#ifndef FitsDefs_H
#define FitsDefs_H

#include <stdint.h>

namespace FITS
{
    //Identifier of the compression schemes processes
    enum CompressionProcess_t
    {
        kFactRaw         = 0x0,
        kFactSmoothing   = 0x1,
        kFactHuffman16   = 0x2,
        eCTADiff         = 0x3,
        eCTADoubleDiff   = 0x4,
        eCTASplitHiLo16  = 0x5,
        eCTAHuffTimes4   = 0x6,
        eCTAZlib         = 0x7,
        eCTAHuffmanByRow = 0x8,
        eCTALZO          = 0x9,
        eCTARICE         = 0xa,
        eCTAHuffman8     = 0xb,
        eCTAHalfman16    = 0xc,
        eCTAHalfman8     = 0xd,
        eCTASplitHiLo32  = 0xe,
        eCTALocalDiff    = 0xf,
        eCTA128Offset    = 0x10,
        eCTASameValues   = 0x11,
        eCTALossyFloats  = 0x12,
        eCTASparseValues = 0x13,
        eCTAHalfDiff32   = 0x14,
        eCTALossyInt16   = 0x15,
        eCTALossyInt32   = 0x16,
        eCTAzstd         = 0x17
    };

    //ordering of the columns / rows
    enum RowOrdering_t
    {
        kOrderByCol = 'C',
        kOrderByRow = 'R'
    };

    //Structure helper for tiles headers
    struct TileHeader
    {
      char     id[4];
      uint32_t numRows;
      uint64_t size;

      TileHeader() {}

      TileHeader(uint32_t nRows,
                 uint64_t s) : id{'T', 'I', 'L', 'E'},
                                 numRows(nRows),
                                 size(s)
      { };
    } __attribute__((__packed__));

    //Structure helper for blocks headers and compresion schemes
    struct BlockHeader
    {
        uint64_t      size;
        char          ordering;
        unsigned char numProcs;
        uint16_t      processings[];

        BlockHeader(uint64_t      s=0,
                    char          o=kOrderByRow,
                    unsigned char n=1) : size(s),
                                         ordering(o),
                                         numProcs(n)
        {}
    } __attribute__((__packed__));


    //Helper structure to simplify the initialization and handling of compressed blocks headers
    struct Compression
    {
        std::vector<uint16_t> sequence;
        BlockHeader           header;

        Compression(const std::vector<uint16_t> &seq, const RowOrdering_t &order=kOrderByCol)
            : sequence(seq), header(0, order, seq.size())
        {

        }

        Compression(const CompressionProcess_t &compression=kFactRaw, const RowOrdering_t &order=kOrderByCol)
            : sequence(1), header(0, order, 1)
        {
            sequence[0] = compression;
        }


        RowOrdering_t getOrdering() const
        {
            return RowOrdering_t(header.ordering);
        }

        uint32_t getSizeOnDisk() const
        {
            return sizeof(BlockHeader) + sizeof(uint16_t)*header.numProcs;
        }

        CompressionProcess_t getProc(uint32_t i) const
        {
            return CompressionProcess_t(sequence[i]);
        }

        uint16_t getNumProcs() const
        {
            return header.numProcs;
        }

        void SetBlockSize(uint64_t size)
        {
            header.size = size;

        }
        void Memcpy(char *dest) const
        {
            memcpy(dest, &header, sizeof(BlockHeader));
            memcpy(dest+sizeof(BlockHeader), sequence.data(), header.numProcs*sizeof(uint16_t));
        }
    };
};

#endif //FitsDefs_H

