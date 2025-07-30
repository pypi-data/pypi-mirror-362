/**
 * @file ZIFits.h
 * @brief Base Compressed Binary FITS tables reader class
 *
 *  Created on: May 16, 2013
 *      Author: lyard-bretz
 *
 */

#ifndef ZFits_H
#define ZFits_H

#include "IFits.h"
#include "Huffman.h"

#include "FitsDefs.h"

class ZIFits : public IFits
{
    public:

        // Basic constructor
        ZIFits(const std::string& fname,
              const std::string& tableName="",
              bool               force    =false);

        // Alternative contstructor
        ZIFits(const std::string& fname,
              const std::string& fout,
              const std::string& tableName,
              bool               force=false);

        // Alternative contstructor with existing table and catalog
        ZIFits( const IFits::Table& table,
               std::vector<std::vector<std::pair<int64_t, int64_t>>>& catalog,
               bool force=false);

        virtual ~ZIFits();

        //  Skip the next row
        bool SkipNextRow();

        virtual bool IsFileOk() const;

            std::vector<std::vector<std::pair<int64_t, int64_t>>>& GetCatalog()  { return fCatalog; }  ;
        size_t GetNumRows() const;
        size_t GetBytesPerRow() const;

    protected:

        //  Stage the requested row to internal buffer
        //  Does NOT return data to users
        virtual void StageRow(size_t row, char* dest);

    protected:

        // Do what it takes to initialize the compressed structured
        void InitCompressionReading(bool allocateBuffer=true);

        // Copy decompressed data to location requested by user
        void MoveColumnDataToUserSpace(char* dest, const char* src, const Table::Column& c);

        bool  fCatalogInitialized;

        std::vector<char> fBuffer;           ///<store the uncompressed rows
        std::vector<char> fTransposedBuffer; ///<intermediate buffer to transpose the rows
        std::vector<char> fCompressedBuffer; ///<compressed rows
        std::vector<char> fColumnOrdering;   ///< ordering of the column's rows. Can change from tile to tile.

        size_t fNumTiles;       ///< Total number of tiles
        size_t fNumRowsPerTile; ///< Number of rows per compressed tile
        int64_t fCurrentRow;    ///< current row in memory signed because we need -1

        std::streamoff fHeapOff;           ///< offset from the beginning of the file of the binary data
        std::streamoff fHeapFromDataStart; ///< offset from the beginning of the data table

        std::vector<std::vector<std::pair<int64_t, int64_t>>> fCatalog;     ///< Catalog, i.e. the main table that points to the compressed data.
        std::vector<size_t>                                   fTileSize;    ///< size in bytes of each compressed tile
        std::vector<std::vector<size_t>>                      fTileOffsets; ///< offset from start of tile of a given compressed column

        Checksum fRawsum;   ///< Checksum of the uncompressed, raw data

        // Get buffer space
        void AllocateBuffers();

        // Read catalog data. I.e. the address of the compressed data inside the heap
        void ReadCatalog();

        //overrides fits.h method with empty one
        //work is done in ReadBinaryRow because it requires volatile data from ReadBinaryRow
        virtual void WriteRowToCopyFile(size_t row);

        // Compressed version of the read row
        bool ReadBinaryRow(const size_t &rowNum, char *bufferToRead);
        // Read a bunch of uncompressed data
        uint32_t UncompressUNCOMPRESSED(char*       dest,
                                        const char* src,
                                        uint32_t    numElems,
                                        uint32_t    sizeOfElems);
        // Read a bunch of data compressed with the Huffman algorithm
        uint32_t UncompressHUFFMAN16(char*       dest,
                                     const char* src,
                                     uint32_t    numChunks);

        // Apply the inverse transform of the integer smoothing
        uint32_t UnApplySMOOTHING(int16_t*   data,
                                  uint32_t   numElems);

        // Data has been read from disk. Uncompress it !
        void UncompressBuffer(const uint32_t &catalogCurrentRow,
                              const uint32_t &thisRoundNumRows,
                              const uint32_t offset);

        public:
        void CheckIfFileIsConsistent(bool update_catalog=false);

};//class zfits

#endif  //ZFits_H
