#ifndef ZOFits_H
#define ZOFits_H

/*
 * zofits.h
 *
 *  FACT native compressed FITS writer
 *      Author: lyard
 */

#include "OFits.h"
#include "Huffman.h"
#include "Queue.h"
#include "MemoryManager.h"
/**
 * @file ZOFits.h
 * @brief Base Compressed Binary FITS tables writer class
 *
 *  Created on: May 16, 2013
 *      Author: lyard-bretz
 *
 */

#ifdef HAVE_BOOST_THREAD
#include <boost/thread.hpp>
#endif

class ZOFits : public OFits
{

        //catalog types
public:
        struct CatalogEntry
        {
            CatalogEntry(int64_t f=0, int64_t s=0) : first(f), second(s) { }
            int64_t first;   ///< Size of this column in the tile
            int64_t second;  ///< offset of this column in the tile, from the start of the heap area
        } __attribute__((__packed__));


        typedef std::vector<CatalogEntry> CatalogRow;
        typedef std::list<CatalogRow>     CatalogType;

        // Parameters required to write a tile to disk
        struct WriteTarget
        {
            bool operator < (const WriteTarget& other) const
            {
                return tile_num < other.tile_num;
            }

            WriteTarget() { }
            WriteTarget(const WriteTarget &t, uint32_t sz) : tile_num(t.tile_num), size(sz), data(t.data) { }

            uint32_t              tile_num; ///< Tile index of the data (to make sure that they are written in the correct order)
            uint32_t              size;     ///< Size to write
            std::shared_ptr<char> data;     ///< Memory block to write
        };


        // Parameters required to compress a tile of data
        struct CompressionTarget
        {
            CompressionTarget(CatalogRow& r) : catalog_entry(r)
            {}

            CatalogRow&           catalog_entry;   ///< Reference to the catalog entry to deal with
            std::shared_ptr<char> src;             ///< Original data
            std::shared_ptr<char> transposed_src;  ///< Transposed data
            WriteTarget           target;          ///< Compressed data
            uint32_t              num_rows;        ///< Number of rows to compress

         };

public:
        /// static setter for the default number of threads to use. -1 means all available physical cores
        static uint32_t DefaultNumThreads(const uint32_t &_n=-2)
        {
#ifdef __clang__
//#pragma message("Disabling multithreaded compression support due to clang compiler")
            if (int32_t(_n) != -2) std::cout << "WARNING: multithreaded compression disabled when compiling with CLANG. Ignoring request for " << _n << " compression threads" << std::endl;
            static uint32_t n=0;
            return n;
#else
            static uint32_t n=0;
            if (int32_t(_n) >= -1)
                n=_n;
            return n;
#endif
        }
        static uint64_t DefaultMaxMemory(const uint64_t &_n=0) { static uint64_t n=1000000; if (_n>0) n=_n; return n; }
        static uint32_t DefaultMaxNumTiles(const uint32_t &_n=0) { static uint32_t n=1000; if (_n>0) n=_n; return n; }
        static uint32_t DefaultNumRowsPerTile(const uint32_t &_n=0) { static uint32_t n=100; if (_n>0) n=_n; return n; }

        /// constructors
        /// @param numTiles how many data groups should be pre-reserved ?
        /// @param rowPerTile how many rows will be grouped together in a single tile
        /// @param maxUsableMem how many bytes of memory can be used by the compression buffers
        ZOFits(uint32_t numTiles    = DefaultMaxNumTiles(),
               uint32_t rowPerTile  = DefaultNumRowsPerTile(),
               uint64_t maxUsableMem= DefaultMaxMemory());

        /// @param fname the target filename
        /// @param numTiles how many data groups should be pre-reserved ?
        /// @param rowPerTile how many rows will be grouped together in a single tile
        /// @param maxUsableMem how many bytes of memory can be used by the compression buffers
        ZOFits(const char* fname,
               uint32_t numTiles    = DefaultMaxNumTiles(),
               uint32_t rowPerTile  = DefaultNumRowsPerTile(),
               uint64_t maxUsableMem= DefaultMaxMemory());

        //initialization of member variables
        /// @param nt number of tiles
        /// @param rpt number of rows per tile
        /// @param maxUsableMem max amount of RAM to be used by the compression buffers
        void InitMemberVariables(const uint32_t nt=0, const uint32_t rpt=0, const uint64_t maxUsableMem=0);

        /// write the header of the binary table
        /// @param name the name of the table to be created
        /// @return the state of the file
        virtual bool WriteTableHeader(const char* name="DATA");

        /// open a new file.
        /// @param filename the name of the file
        /// @param Whether or not the name of the extension should be added or not
        virtual void open(const char* filename, bool addEXTNAMEKey=true);

        /// Super method. does nothing as zofits does not know about DrsOffsets
        /// @return the state of the file
        virtual bool WriteDrsOffsetsTable();

        /// Returns the number of bytes per uncompressed row
        /// @return number of bytes per uncompressed row
        uint32_t GetBytesPerRow() const;

        /// Write the data catalog
        /// @return the state of the file
        bool WriteCatalog();

        /// Applies the DrsOffsets calibration to the data. Does nothing as zofits knows nothing about drsoffsets.
        void DrsOffsetCalibrate(char* );

        CatalogRow& AddOneCatalogRow();

        /// write one row of data
        /// Note, in a multi-threaded environment (NumThreads>0), the return code should be checked rather
        /// than the badbit() of the stream (it might have been set by a thread before the errno has been set)
        /// errno will then contain the correct error number of the last error which happened during writing.
        /// @param ptr the source buffer
        /// @param the number of bytes to write
        /// @return the state of the file. WARNING: with multithreading, this will most likely be the state of the file before the data is actually written
        bool WriteRow(const void* ptr, size_t cnt, bool = true);

        /// update the real number of rows
        void FlushNumRows();

        /// Setup the environment to compress yet another tile of data
        /// @param target the struct where to host the produced parameters
        virtual CompressionTarget InitNextCompression();

        /// Shrinks a catalog that is too long to fit into the reserved space at the beginning of the file.
        uint32_t ShrinkCatalog();

        /// close an open file.
        /// @return the state of the file
        virtual bool close();

        /// Overload of the ofits method. Just calls the zofits specific one with default, uncompressed options for this column
        bool AddColumn(uint32_t cnt, char typechar, const std::string& name, const std::string& unit,
                       const std::string& comment="", bool addHeaderKeys=true);

        /// Overload of the simplified compressed version
        bool AddColumn(const FITS::Compression &comp, uint32_t cnt, char typechar, const std::string& name,
                       const std::string& unit, const std::string& comment="", bool addHeaderKeys=true);

        /// Get and set the actual number of threads for this object
        int32_t GetNumThreads() const;
        virtual bool SetNumThreads(uint32_t num);

        uint32_t GetNumTiles() const;
        void SetNumTiles(uint32_t num);

protected:

        /// Allocates the required objects.
        virtual void reallocateBuffers();

        /// Actually does the writing to disk (and checksuming)
        /// @param src the buffer to write
        /// @param sizeToWrite how many bytes should be written
        /// @return the state of the file
        bool writeCompressedDataToDisk(char* src, const uint32_t sizeToWrite);

        /// Compress a given buffer based on the target. This is the method executed by the threads
        /// @param target the struct hosting the parameters of the compression
        /// @return number of bytes of the compressed data, or always 1 when used by the Queues
        bool CompressBuffer(const CompressionTarget& target);
        /// Write one compressed tile to disk. This is the method executed by the writing thread
        /// @param target the struct hosting the write parameters
        bool WriteBufferToDisk(const WriteTarget& target);

        /// Compress a given buffer based on its source and destination
        //src cannot be const, as applySMOOTHING is done in place
        /// @param dest the buffer hosting the compressed data
        /// @param src the buffer hosting the transposed data
        /// @param num_rows the number of uncompressed rows in the transposed buffer
        /// @param the number of bytes of the compressed data
        uint64_t compressBuffer(char* dest, char* src, uint32_t num_rows, CatalogRow& catalog_row);

        /// Transpose a tile to a new buffer
        /// @param src buffer hosting the regular, row-ordered data
        /// @param dest the target buffer that will receive the transposed data
        void copyTransposeTile(const char* src, char* dest, uint32_t num_rows);

        /// Specific compression functions
        /// @param dest the target buffer
        /// @param src the source buffer
        /// @param size number of bytes to copy
        /// @return number of bytes written
        uint32_t compressUNCOMPRESSED(char* dest, const char* src, uint32_t size);

        /// Do huffman encoding
        /// @param dest the buffer that will receive the compressed data
        /// @param src the buffer hosting the transposed data
        /// @param numRows number of rows of data in the transposed buffer
        /// @param sizeOfElems size in bytes of one data elements
        /// @param numRowElems number of elements on each row
        /// @return number of bytes written
        uint32_t compressHUFFMAN16(char* dest, const char* src, uint32_t numRows, uint32_t sizeOfElems, uint32_t numRowElems);

        /// Applies Thomas' DRS4 smoothing
        /// @param data where to apply it
        /// @param numElems how many elements of type int16_t are stored in the buffer
        /// @return number of bytes modified
        uint32_t applySMOOTHING(char* data, uint32_t numElems);

        /// Apply the inverse transform of the integer smoothing
        /// @param data where to apply it
        /// @param numElems how many elements of type int16_t are stored in the buffer
        /// @return number of bytes modified
        uint32_t UnApplySMOOTHING(char* data, uint32_t numElems);

        //thread related stuff
        MemoryManager   fMemPool;           ///< Actual memory manager, providing memory for the compression buffers
        int32_t         fNumQueues;         ///< Current number of threads that will be used by this object
        uint64_t        fMaxUsableMem;      ///< Maximum number of bytes that can be allocated by the memory manager
        int32_t         fLatestWrittenTile; ///< Index of the last tile written to disk (for correct ordering while using several threads)

        std::vector<Queue<CompressionTarget>>     fCompressionQueues;  ///< Processing queues (=threads)
        Queue<WriteTarget, QueueMin<WriteTarget>> fWriteToDiskQueue;   ///< Writing queue (=thread)

        // catalog related stuff
        CatalogType fCatalog;               ///< Catalog for this file
        uint32_t    fCatalogSize;           ///< Actual catalog size (.size() is slow on large lists)
        uint32_t    fNumTiles;              ///< Number of pre-reserved tiles
        uint32_t    fNumRowsPerTile;        ///< Number of rows per tile
        off_t       fCatalogOffset;         ///< Offset of the catalog from the beginning of the file

        // checksum related stuff
        Checksum fCatalogSum;    ///< Checksum of the catalog
        Checksum fRawSum;        ///< Raw sum (specific to FACT/CTA)
        int32_t  fCheckOffset;   ///< offset to the data pointer to calculate the checksum

        // data layout related stuff
        // Regular columns augmented with compression informations
        struct CompressedColumn
        {
            CompressedColumn(const Table::Column& c, const FITS::Compression& h) : col(c),
                block_head(h)
            {}

            Table::Column col;             ///< the regular column entry
            FITS::Compression block_head;  ///< the compression data associated with that column
        };
        std::vector<CompressedColumn> fRealColumns;     ///< Vector hosting the columns of the file
        uint32_t                      fRealRowWidth;    ///< Width in bytes of one uncompressed row
        std::shared_ptr<char>         fSmartBuffer;     ///< Smart pointer to the buffer where the incoming rows are written
        std::vector<char>             fRawSumBuffer;    ///< buffer used for checksuming the incoming data, before compression

        std::exception_ptr fThreadsException; ///< exception pointer to store exceptions coming from the threads

        int                fErrno;            ///< propagate errno to main thread

        bool               fShouldAllocateBuffers; ///< If used as a parent class, allows to disable buffers allocation.
};

#endif //ZOFits_H
