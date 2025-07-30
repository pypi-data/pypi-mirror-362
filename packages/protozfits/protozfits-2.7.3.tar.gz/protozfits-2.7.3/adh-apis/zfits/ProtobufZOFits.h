/**
 * @file ProtobufZOFits.h
 *
 * @brief Protobuf to Compressed FITS Writer
 *
 *  Created on: Apr 17, 2014
 *      Author: lyard
 */

#ifndef PROTOBUFZOFITS_H_
#define PROTOBUFZOFITS_H_

#include "ProtobufToFits.h"
#include "ZOFits.h"
#include "BasicDefs.h"

#include <map>

#include "ProtoDataModel.pb.h"

namespace ADH
{
namespace IO
{
/**
 *      @class ProtobufZOFits
 *      @brief Low-level compressed FITS writer for protobufs messages.
 *
 *      The messages are split as follow: each message is written in one row, and each field of the
 *      message is in a separate column. If a message features repeated child-messages in a field, then
 *      one column is created per-child-per-field.
 *
 *      Once initialized, only a single type of message can be written to the current fits file.
 *      Various compression schemes can be used to compress the data. At the moment, the same scheme
 *      if used for all columns. The available schemes are as follow:
 *      - zlib: the usual zlib compression, default strength. Pretty slow, average compression ratio
 *      - lzo:  the realtime compression scheme. Very fast, poor compression ratios
 *      - rice: the scheme used by fpack from FTOOLS. Very fast, good ratio
 *      - zrice: high and low parts of 16 bit words are split before separately compressing with zlib
 *      - lzorice: high and low part of 16 bit words are plit before separately compressing with lzo
 *      - raw: the data is left uncompressed
 *
 *      The writing uses the concept of Tile, i.e. a bunch of data grouped together for compression.
 *      In reality, a tile is a number of rows grouped together, while each group of column entries
 *      is compressed separately. Because of the way FITS files are stored on disk, enough tiles must
 *      be declared before starting to write, as this number cannot be extended once the first row has
 *      been written (or at very high cost). In practice, it is possible to write more tiles than originally
 *      declared, however the file becomes non-fits compliant, and some of the data will be invisible to
 *      CFITSIO (but will be read-back by ProtobufIFits nontheless).
 */
class ProtobufZOFits : public ZOFits, public ProtobufToFits
{

public:

    enum MemManagementScheme
    {
        NONE    = 0,    //the given event pointers are not touched at all. E.g. suitable for pre-allocated events in memory. getANewMessage will recycle old messages anyways though
        RECYCLE = 1,    //the given events pointers can be reused once they were written to disk by calling the getANewMessage() method. Unclaimed events are deleted along with the writer object
        AUTO    = 2,    //the given events pointers are deleted as soon as they are written to disk. the getANewMessage method always return new events in this case
    };

    //! @brief default constructor
    //! @param numTiles the number of tiles to reserve space for
    //! @param rowsPerTile the number of rows to put in each tile. Hence the reserved number of writable message to remain FITS compliant is numTiles*rowsPerTile
    //! @param maxCompressionMem The maximum memory to use for compression, in KILOBYTES
    //! @param autoMemManagement whether messages given for writing should be deleted by the writer or not once the object is destructed
    ProtobufZOFits(google::protobuf::uint32 numTiles          = 1000,
                   google::protobuf::uint32 rowsPerTile       = 1,
                   google::protobuf::uint64 maxCompressionMem = 1000000,
                   MemManagementScheme      autoMemManagement = RECYCLE);

    //! @brief default destructor
    virtual ~ProtobufZOFits();

    //! @brief initializes the columns of the fits file from the message structure
    //!
    //! The message given as example should be as large as it can be in the case of
    //! children messages in fields so that appropriate columns can be created
    //! In the case of repeated base-type arrays, their maximum size is extracted
    //! from the written data: no limitation here. If this method is not called explicitely,
    //! the file's structure is created from the first written message
    //! @param message a pointer to the example message
    virtual void initColumns(const google::protobuf::Message* message);

    //! @brief write a given message to the fits file
    //! The ownership of the pointer is given to the writer.
    //! Once the structure has been written, the ownership can be regained by calling the getRecycledMessage() method
    //! @param message a pointer to the message to be written
    virtual void writeMessage(const google::protobuf::Message* message);
    int getPercentMemUsed();
    //! @brief finalizes the current table and initializes a new one.
    //! Can take some time to execute as all data being compressed is flushed to disk
    //! @param tablename the name to give to the new table. Default=DATA
    //! @param display_stats enables the display of flusing information to cout
    virtual void moveToNewTable(string tablename="DATA", bool display_stats=false, bool closing_file=false);

    void copyTableFrom(const string& filename,
                       const string& tablename);

    //! @brief updates header information to disk
    void updateHeaderKeys(bool finalUpdate = false);

    //! @brief close the currently open file
    //! @return whether or not the file has been successfully written. Equivalent to ofstream::good()
    virtual bool close(bool display_stats);
    bool close();

    //! @brief flushes the header and catalog data so that data currently on disk can be read
    void flushCatalog();

    //! @brief set the compression scheme to be applied to all columns
    //! @param compression the compression name, either 'zlib', 'lzo', 'rice', 'zrice', 'lzorice', 'raw'
    virtual void setDefaultCompression(const string& compression);
    void requestExplicitCompression(const string& field,        ///< @brief full hierarchical name of the field to set
                                    const string& compression);  ///< @brief which compression scheme should be assigned

    void setCompressionBlockSize(google::protobuf::uint32 size);

    //! @brief free the allocated compression memory
    //!
    //! Will throw a runtime error if some of the memory blocks are currently in use, i.e. compression is ongoing.
    void freeCompressionMemory()
    {
        if (!fMemPool.freeAllMemory())
            throw runtime_error("Could not free compression memory");
    }

    //! @brief get a pointer to a message structure that can be reused. The ownership of the memory is given back to the user
    //! @return a message structure that can be reused, NULL if none is currently available
    google::protobuf::Message* getRecycledMessage();

    //! @brief type-specific creation method recycles messages if possible. Only meant to deliver the type of messages being written. The behavior is undefined otherwise
    //! @return always returns a type-specific message: creates a new one if needed
    template <typename _T>
    _T* getANewMessage()
    {
        //let's try to recycle a message first
        google::protobuf::Message* to_return = getRecycledMessage();

        if (to_return != NULL)
        {
            if (dynamic_cast<_T*>(to_return) != NULL)
                return dynamic_cast<_T*>(to_return);
            else
            {   //type of message has changed: discard current and get new, correct one
                delete to_return;
                return new _T();
            }
        }
        else
            return new _T();
    }

    uint64 getSizeWrittenToDisk() { return _size_written_to_disk;}

private:

    //! @brief compression pre-processing. Separates the high and low bytes forming the 16 bits word
    //! @param buffer the memory where the values to be split are located
    //! @param num_bytes the total number of bytes used by the values (i.e. num_values = num_bytes/2)
    void splitHiLo16(char* buffer, uint32 num_bytes);
    void splitHiLo32(char* buffer, uint32 num_bytes);
    //! @brief gzip compression. Throws a WriteTest Error in case the destination buffer is not large enough
    //! @param destination buffer, at least num_bytes of free space must be available
    //! @param src source buffer containing num_bytes of data to be compressed
    //! @param num_bytes the number of bytes of data to be compressed
    //! @return the number of bytes written to dest
    uint64_t zlibCompress(char* dest, const char* src, uint32 num_bytes);

    std::shared_ptr<std::vector<const google::protobuf::Message*>> _incoming_data;         ///< incoming messages

    //! @brief specific FITS columns intialization in case of the custom AnyArray message type
    //! @param message containing the cta array to use for the initialization
    //! @param name the full name of this message
    void addAnyArrayColumn(const google::protobuf::Message& message, const std::string& name, const std::string& id="");

    //! @brief crawls through the input message using reflexion and build the corresponding fits columns
    //! @param message the current message to use for the initialization
    //! @param name the full name of the current message, for naming columns
    void buildFitsColumns(const google::protobuf::Message& message, const std::string& name="", const std::string& id="");

    std::vector<uint16>                           _default_comp; ///< @brief default compression to be assigned to every column
    std::map<std::string, std::vector<uint16>>              _explicit_comp; ///< @brief specific, per-column compressions

//protected so that nullWriter can use these
protected:
    std::list<google::protobuf::Message*>    _recycled_messages;     ///< list of messages that can be reused
    std::mutex                               _recycle_fence;         ///< fence to add recycled message in a multi-threaded environment
    std::mutex                               _catalog_flush_fence;

private:
    uint64                                   _compression_block_size;///< size in bytes of the compression memory blocks

    uint64                                   _size_written_to_disk;

    int32                                    _zstd_level;

    //! @brief struct used to pass compression target to threads
    struct CompressionTarget
    {
        CompressionTarget(CatalogRow& row) : catalog(row),
                                             targetId(0)
        {}

        CatalogRow&                         catalog;  ///< Catalog row to fill in
        uint32                              targetId; ///< Tile number, to be able to sort out the tiles when writing to disk
        std::shared_ptr<vector<const google::protobuf::Message*>> messages; ///< actual data to be written
        std::list<std::shared_ptr<char>>    buffers;  ///< Pointers to memory where to write the compressed data

        friend std::ostream& operator<< (std::ostream& os, const CompressionTarget& t)
        {
            os << "Catalog entry missing << operator "   << std::endl;
            os << "targetID: " <<  t.targetId            << std::endl;
            os << "Num messages: " << t.messages->size() << std::endl;
            os << "Buffers: "                            << std::endl;
            for (auto it=t.buffers.cbegin(); it!=t.buffers.cend(); it++)
                os << (void*)(it->get()) << std::endl;
            os << "Done." << std::endl;
            return os;
        }
    };

    //! @brief struct used to pass compressed data to the disk writers
    struct WriteToDiskTarget
    {
        bool operator < (const WriteToDiskTarget& other) const
        {
            return targetId < other.targetId;
        }
        uint32                      targetId;            ///< Tile number, for sorting inputs before writing to disk
        list<uint32>                num_bytes_in_buffer; ///< Number of bytes to write per input buffer
        list<std::shared_ptr<char>> buffers;             ///< Actual data to be written
    };

    //Thread related stuff
    std::vector<Queue<CompressionTarget>>                 _compression_queues;   ///< List of available compression threads
    Queue<WriteToDiskTarget, QueueMin<WriteToDiskTarget>> _write_to_disk_queue;  ///< Single thread writing to disk
    uint32                                                _next_buffer_to_write; ///< index of the next expected buffer to be written to disk

    MemManagementScheme   _auto_memory_management; ///< boolean to let the writer delete the messages that were given to it (or not)

    std::string _current_table_name;
    int32       _num_tiles_written;

    uint64      _raw_heap_size;

    int32       _sparse_value; //the value to be removed by the sparsevalue algorithm



    //! @brief pass the currently waiting messages to the compression processing
    void launchNewCompression();

    //! @brief actual write a given bunch of compressed data to disk
    bool writeToDisk(const WriteToDiskTarget& target);

    //! @brief Compress a bunch of serialized data. Retrieve compression scheme from file initialization and col_index
    //! @param src buffer containing the input data
    //! @param dest buffer where to write to
    //! @param num_bytes number of bytes from the src buffer to compress
    //! @param bytes_in_dest number of compressed bytes already sitting in the dest buffer
    //! @param col_index index of the current column being written (to be able to retrieve the associated compression scheme)
    //! @param comp_target original compression target, to be able to get a new buffer in case the current one goes full
    //! @disk_target write to disk target, to be able to enqueue a new buffer in case the current one goes full
    void compressBuffer(char*              src,
                        shared_ptr<char>&  dest,
                        int32              num_bytes,
                        int32&             bytes_in_dest,
                        int32&             col_index,
                        CompressionTarget& comp_target,
                        WriteToDiskTarget& disk_target);

    //! @brief compress a whole set of input messages
    bool compressMessages(const CompressionTarget& comp_target);

    //! @brief recursive function that crawls through the messages fields and writes them sequentially.
    //! @param messages The list of messages to be compressed
    //! @param col_index the index of the current column being written. IO for recursion
    //! @param gather_buf buffer where to write the serialized fields to. Is large enough from initialization
    //! @param compres_buff buffer where to write the compressed data to.
    //! @param comp_bytes_written number of compressed bytes already sitting in the compres_buff
    //! @param comp_target original compression target, to be able to get new buffers in case the commpres_buff goes full
    //! @param disk_target write to disk target, to be able to enqueue new compres_buff in case it goes full
    void compressMessageFields(const std::vector<const google::protobuf::Message*>& messages,
                                 int32&                                       col_index,
                                 char*                                        gather_buf,
                                 std::shared_ptr<char>&                       compres_buff,
                                 int32&                                       comp_bytes_written,
                                 CompressionTarget&                           comp_target,
                                 WriteToDiskTarget&                           disk_target,
                                 const string&                                name="");


    //! @brief verifies that a number is indeed a multiple of a given value, throws an exception otherwise
    void checkArrayValueSize(int32 num_bytes, int32 multiple, FITS::CompressionProcess_t ongoing_process);

    //hack to test lossy integers compression
    public:
        uint16 _lossy_int16_quantization;
        float  _lossy_average_error;
        uint64 _lossy_num_error_samples;

};


};//namespace IO
};//namespace ADH

//FIXME I must specialize for the other data types.
#endif /* PROTOBUFOFITS_H_ */
