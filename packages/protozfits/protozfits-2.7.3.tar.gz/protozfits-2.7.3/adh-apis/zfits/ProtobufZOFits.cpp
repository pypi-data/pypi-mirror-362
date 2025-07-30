/**
 * @file ProtobufZOFits.cpp
 *
 * @brief Protobuf to Compressed FITS Writer
 *
 *  Created on: Apr 17, 2014
 *      Author: lyard
 */

#include "ProtobufZOFits.h"

#include <zlib.h>
#include "minilzo.h"
#include "ricecomp.h"
#include "zstd.h"

//using namespace google::protobuf;
using namespace std;
using namespace ADH::ColoredOutput;

namespace ADH
{
namespace IO
{
/*******************************************************************************
 *      DEFAULT CONSTRUCTOR
 *******************************************************************************/
ProtobufZOFits::ProtobufZOFits(uint32 numTiles,
                               uint32 rowsPerTile,
                               uint64 maxCompressionMem,
                               MemManagementScheme   autoMemManagement)

             :          ZOFits(numTiles, rowsPerTile, maxCompressionMem),
                        ProtobufToFits(),
                        _incoming_data(new vector<const google::protobuf::Message*>),
                        _compression_block_size(0),
                        _write_to_disk_queue(bind(&ProtobufZOFits::writeToDisk, this, placeholders::_1), false),
                        _next_buffer_to_write(0),
                        _auto_memory_management(autoMemManagement),
                        _current_table_name("DATA"),
                        _num_tiles_written(0),
                        _raw_heap_size(0),
                        _sparse_value(-100), //once compressed -1.f becomes -100
                        _lossy_int16_quantization(1),
                        _lossy_average_error(0),
                        _lossy_num_error_samples(0)
{

 // _incoming_data = shared_ptr<std::vector<google::protobuf::Message*>>(new vector<google::protobuf::Message*>);
 //  _compression_block_size = 0;
 //    _write_to_disk_queue = Queue<WriteToDiskTarget>(bind(&ProtobufZOFits::writeToDisk, this, placeholders::_1), false);
 //   _next_buffer_to_write = 0;
 //   _auto_memory_management = autoMemManagement;
 //   _current_table_name = string("DATA");
 //   _num_tiles_written = 0;
 //   _raw_heap_size = 0;

    uint32 num_threads_to_use = DefaultNumThreads();

    _compression_queues.resize((num_threads_to_use<1)?1:num_threads_to_use, Queue<CompressionTarget>(bind(&ProtobufZOFits::compressMessages, this, placeholders::_1), false));
    fNumQueues = num_threads_to_use;
    _compression_queues.front().setPromptExecution(fNumQueues==0);
    _write_to_disk_queue.setPromptExecution(fNumQueues==0);

    //start the queues !
    //THIS WAS DISABLED AS IT IS NOW EXECUTED FROM moveToNewTable
    if (fNumQueues != 0)
    {
        for (auto it=_compression_queues.begin(); it!= _compression_queues.end(); it++)
            it->start();

        _write_to_disk_queue.start();
    }

    setDefaultCompression("raw");

    //prevent zofits from allocating its own buffers
    fShouldAllocateBuffers = false;

    _size_written_to_disk = 0;

    _zstd_level = 0;
}


/*******************************************************************************
 * DEFAULT DESTRUCTOR
 *******************************************************************************/
ProtobufZOFits::~ProtobufZOFits()
{
    if (_auto_memory_management != NONE)
        for (auto it=_recycled_messages.begin(); it!=_recycled_messages.end(); it++)
            delete *it;

//    if (_incoming_data != NULL)
//        delete _incoming_data;
}

/*********************************************************************
 *
 * SET COMPRESSION BLOCK SIZE
 *
 *********************************************************************/
void ProtobufZOFits::setCompressionBlockSize(uint32 size)
{
    _compression_block_size = size;
}

/*******************************************************************************
 *  INIT COLUMNS
 *
 *  Initializes the FITS structure from the message structure
 *******************************************************************************/
void ProtobufZOFits::initColumns(const google::protobuf::Message* message)
{
    //Only one given message type can be writen at a given time...
    if (_descriptor != NULL)
        throw runtime_error("Looks like you are trying to initialize the columns of the tables more than once... this is NOT allowed.");

    //store the message descriptor.
    _descriptor = message->GetDescriptor();
    SetStr("PBFHEAD", std::string{_descriptor->full_name()}, "Written message name");
    SetDefaultKeys();

    _total_num_columns = 0;
    //build the fits columns from the message. Start with an empty prefix
    buildFitsColumns(*message);

    if (_compression_block_size == 0)
        _compression_block_size = 1.2*message->ByteSize()*fNumRowsPerTile; //assume that in the worst case, compressed data will end up as 1.2x the original, raw size

    if (_compression_block_size == 0)
    {
        throw runtime_error("You are initializing compression chunks with a message of size 0");
    }
    //add space for tile and block headers. block headers is assumed to have <= 10 processings
    _compression_block_size += sizeof(FITS::TileHeader) + sizeof(FITS::BlockHeader)*fTable.num_cols + 10*sizeof(uint16)*fTable.num_cols + 8; //+8 for checksuming

    //check that enough memory is allocated to the compression, compared to the requested number of compression threads
    int32 max_usable_threads = fMaxUsableMem/(3*_compression_block_size);

    //if there is not enough memory for one thread to run, throw an exception
    if (max_usable_threads == 0)
    {
        ostringstream str;
        str << "Not enough memory was allocated for the compression (" << fMaxUsableMem/(1024*1024) << "MB vs " << (3*_compression_block_size)/(1024*1024) << "MB requested per thread). ImpossibRe to continue" << endl;
        throw runtime_error(str.str());
    }

    //if not enough memory is available to allow for all requested threads to run simultaneously, display a warning
    if (fNumQueues+1 > max_usable_threads)
        cout << yellow << "WARNING: Not enough memory was allocated (" << fMaxUsableMem/(1024*1024) << "MB), hence only " << max_usable_threads << " compression threads will be used." << no_color << endl;

    //set the chunk size of the compression blocks
    fMemPool.setChunkSize(_compression_block_size);
}

/*******************************************************************************
 *  SET DEFAULT COMPRESSION
 *******************************************************************************/
void ProtobufZOFits::setDefaultCompression(const string& compression)
{
    requestExplicitCompression("default", compression);
}

/*******************************************************************************
 *  SET DEFAULT COMPRESSION
 *******************************************************************************/
void ProtobufZOFits::requestExplicitCompression(const string& field,
                                                const string& compression)
{

    vector<uint16> real_scheme;
    vector<uint16>& scheme = (field=="default") ? _default_comp : real_scheme;

        if (compression == "digicam")
    {
        requestExplicitCompression("telescopeID",                    "zrice");
        requestExplicitCompression("trigger_output_patch7",          "zlib");//
        requestExplicitCompression("trigger_output_patch19",         "zrice32");
        requestExplicitCompression("eventNumber",                    "ricefact");
        requestExplicitCompression("hiGain.waveforms.samples",       "diffman16");
        requestExplicitCompression("hiGain.waveforms.baselines",     "zrice");
        requestExplicitCompression("hiGain.waveforms.pixelsIndices", "doublediffman16");
        requestExplicitCompression("local_time_nanosec",             "zlib");
        requestExplicitCompression("local_time_sec",                 "zlib");
        requestExplicitCompression("pixels_flags",                   "zlib");
        requestExplicitCompression("event_type",                     "zrice");
        requestExplicitCompression("trigger_input_traces",           "zlib");
    }
    else if (compression == "nectarcam")
    {
        setDefaultCompression("raw");
        requestExplicitCompression("waveform", "diffman16");
        requestExplicitCompression("pixel_status", "zstd-1");
        requestExplicitCompression("nectarcam.counters", "zrice");
    }
    else if (compression == "lst")
    {
        requestExplicitCompression("configuration_id",           "zrice32");
        requestExplicitCompression("event_id",                   "zrice32");
        requestExplicitCompression("tel_event_id",               "zrice32");
        requestExplicitCompression("trigger_time_s",             "zrice32");
        requestExplicitCompression("trigger_time_qns",           "zrice32");
        requestExplicitCompression("trigger_type",               "zrice32");
        requestExplicitCompression("waveform",                   "fact");
        requestExplicitCompression("pixel_status",               "zlib");
        requestExplicitCompression("ped_id",                     "zrice32");
        requestExplicitCompression("lstcam.module_status",       "lzo");
        requestExplicitCompression("lstcam.extdevices_presence", "zrice32");
        requestExplicitCompression("lstcam.tib_data",            "zrice32");
        requestExplicitCompression("lstcam.cdts_data",           "zrice32");
        requestExplicitCompression("lstcam.swat_data",           "zrice32");
        requestExplicitCompression("lstcam.counters",            "zlib");
        requestExplicitCompression("lstcam.chips_flags",         "zrice32");
        requestExplicitCompression("lstcam.first_capacitor_id",  "doublediffman16");
        requestExplicitCompression("lstcam.drs_tag_status",      "lzo");
        requestExplicitCompression("lstcam.drs_tag",             "fact");
    }
    else if (compression == "lst-r1v1-uncalibrated") {
         requestExplicitCompression("waveform", "fact");
         requestExplicitCompression("event_id", "zrice32");
         requestExplicitCompression("tel_id", "zrice32");
         requestExplicitCompression("local_run_id", "zrice32");
         requestExplicitCompression("event_type", "zrice32");
         requestExplicitCompression("event_time_s", "zrice32");
         requestExplicitCompression("event_time_qns", "zrice32");
         requestExplicitCompression("num_channels", "zrice32");
         requestExplicitCompression("num_samples", "zrice32");
         requestExplicitCompression("num_pixels", "zrice32");
         requestExplicitCompression("num_modules", "zrice32");
         requestExplicitCompression("pixel_status", "zlib");
         requestExplicitCompression("first_cell_id", "doublediffman16");
         requestExplicitCompression("module_hires_local_clock_counter", "zlib");
         requestExplicitCompression("calibration_monitoring_id", "zrice32");
         requestExplicitCompression("debug.module_status", "lzo");
         requestExplicitCompression("debug.extdevices_presence", "zrice32");
         requestExplicitCompression("debug.tib_data", "zrice32");
         requestExplicitCompression("debug.cdts_data", "zrice32");
         requestExplicitCompression("debug.swat_data", "zrice32");
         requestExplicitCompression("debug.counters", "zlib");
         requestExplicitCompression("debug.chips_flags", "zrice32");
         requestExplicitCompression("debug.tdp_action", "zrice32");
    }
    else if (compression == "zlib")
    {
        scheme.resize(1);
        scheme[0] = FITS::eCTAZlib;
    }
    else if (compression == "fact")
    {
        scheme.resize(2);
        scheme[0] = FITS::kFactSmoothing;
        scheme[1] = FITS::kFactHuffman16;
    }
    else if (compression == "diffman16")
    {
        scheme.resize(2);
        scheme[0] = FITS::eCTADiff;
        scheme[1] = FITS::kFactHuffman16;
    }
    else if (compression == "lossyint16")
    {
        scheme.resize(3);
        scheme[0] = FITS::eCTALossyInt16;

        scheme[1] = FITS::eCTADiff;
        scheme[2] = FITS::kFactHuffman16;
    }
    else if (compression == "lossyint32")
    {
        scheme.resize(3);
        scheme[0] = FITS::eCTALossyInt32;
        scheme[1] = FITS::eCTASplitHiLo32;
        scheme[2] = FITS::eCTAHalfman16;
    }
    else if (compression == "huffman16")
    {
        scheme.resize(1);
        scheme[0] = FITS::kFactHuffman16;
    }
    //Cannot get huffman8 to always work: disabling it as compression ratios where not that great anyway...
//    else if (compression == "huffman8")
//    {
//        scheme.resize(1);
//        scheme[0] = FITS::eCTAHuffman8;
//    }
    else if (compression == "doublediffman16")
    {
        scheme.resize(4);
        scheme[0] = FITS::eCTADiff;
        scheme[1] = FITS::eCTA128Offset;
        scheme[2] = FITS::eCTASplitHiLo16;
        scheme[3] = FITS::eCTAZlib;
    }
    else if (compression == "riceman16")
    {
        scheme.resize(2);
        scheme[0] = FITS::eCTASplitHiLo32;
        scheme[1] = FITS::eCTAHalfman16;
    }
    else if (compression == "factrice")
    {
        scheme.resize(3);
        scheme[0] = FITS::kFactSmoothing;
        scheme[1] = FITS::eCTASplitHiLo16;
        scheme[2] = FITS::eCTAHalfman16;
    }
    else if (compression == "ricefact")
    {
        scheme.resize(3);
        scheme[0] = FITS::eCTASplitHiLo16;
        scheme[1] = FITS::kFactSmoothing;
        scheme[2] = FITS::eCTAHalfman16;
    }
    else if (compression == "rrice")
    {
        scheme.resize(2);
        scheme[0] = FITS::eCTASplitHiLo16;
        scheme[1] = FITS::eCTARICE;
    }
    else if (compression == "rice")
    {
        scheme.resize(1);
        scheme[0] = FITS::eCTARICE;
    }
    else if (compression == "lzo")
    {
        scheme.resize(1);
        scheme[0] = FITS::eCTALZO;

       if (lzo_init() != LZO_E_OK)
           throw runtime_error("Cannot initialize LZO");
    }
    else if (compression == "zrice")
    {
        scheme.resize(2);
        scheme[0] = FITS::eCTASplitHiLo16;
        scheme[1] = FITS::eCTAZlib;
    }
    else if (compression == "zrice32")
    {
        scheme.resize(2);
        scheme[0] = FITS::eCTASplitHiLo32;
        scheme[1] = FITS::eCTAZlib;
    }
    else if (compression == "lzorice")
    {
        scheme.resize(2);
        scheme[0] = FITS::eCTASplitHiLo16;
        scheme[1] = FITS::eCTALZO;

        if (lzo_init() != LZO_E_OK)
            throw runtime_error("Cannot initialize LZO");
    }
    else if (compression == "samevalues32")
    {
        cerr << light_yellow << "WARNING: same values comp scheme only works on very specific arrays: you might hit an exception if your data is not fit: use at your own risks" << no_color << endl;
        scheme.resize(3);
        scheme[0] = FITS::eCTASameValues;
        scheme[1] = FITS::eCTASplitHiLo32;
        scheme[2] = FITS::eCTAZlib;
    }
    else if (compression == "sparsevalues32")
    {
        cerr << light_yellow << "WARNING: sparse comp scheme only works on sparse arrays: you might hit an exception if your data is not fit: use at your own risks" << no_color << endl;
        scheme.resize(3);
        scheme[0] = FITS::eCTASparseValues;
        scheme[1] = FITS::eCTASplitHiLo32;
        scheme[2] = FITS::eCTAZlib;
    }
    else if (compression == "samelossyfloats")
    {
        cerr << light_red << "WARNING: lossy comp scheme experimental only: use at your own risks" << no_color << endl;
        scheme.resize(4);
        scheme[0] = FITS::eCTALossyFloats;
        scheme[1] = FITS::eCTASameValues;
        scheme[2] = FITS::eCTASplitHiLo32;
        scheme[3] = FITS::eCTAZlib;
    }
    else if (compression == "sparselossyfloats")
    {
        cerr << light_red << "WARNING: lossy comp scheme experimental only: use at your own risks" << no_color << endl;
        scheme.resize(4);
        scheme[0] = FITS::eCTALossyFloats;
        scheme[1] = FITS::eCTASparseValues;
        scheme[2] = FITS::eCTASplitHiLo32;
        scheme[3] = FITS::eCTAZlib;
    }
    else if (compression == "raw")
    {
        scheme.resize(1);
        scheme[0] = FITS::kFactRaw;
    }
    else if (compression.substr(0,4) == "zstd")
    {
        scheme.resize(1);
        scheme[0] = FITS::eCTAzstd;
        if (compression.size() > 4)
        {
            _zstd_level = atoi(compression.substr(4, compression.size()-4).c_str());
//            cout << "Set ZSTD compression level to " << _zstd_level << endl;
        }
    }
    else
    {
        ostringstream str;
        str << "Unkown compression scheme: " << compression << " acceptable values are:" << endl;
        str << "...........zlib: the well-known zlib," << endl;
        str << "...........fact: average difference with 2 previous samples, then huffman 16 bits," << endl;
        str << "......diffman16: difference with previous sample, then huffman 16 bits," << endl;
        str << "......huffman16: huffman encoding on 16 bits," << endl;
        str << "doublediffman16: difference with previous sample, then offset of 128, then 16-bits splitting then zlib," << endl;
        str << "......riceman16: 16-bits splitting then two huffman, one for high bits, one for low-bits," << endl;
        str << ".......factrice: average difference with 2 previous samples, then hi-lo splitting on 16 bits, then two huffmans (1 high, 1 low)," << endl;
        str << ".......ricefact: the symmetric of factrice: hi-lo splitting, then smoothing, then two huffmans ," << endl;
        str << "..........rrice: 16-bits splitting then native 16-bits RICE from cfitsio," << endl;
        str << "...........rice: native 16-bits RICE from cfitsio," << endl;
        str << "..........zrice: 16-bits splitting then zlib," << endl;
        str << "........zrice32: 32-bits splitting then zlib," << endl;
        str << "........lzorice: 16-bits splitting then lzo compression," << endl;
        str << ".sparsevalues32: 32-bits experimental algorithm," << endl;
        str << "sparselossyfloats: lossy floating point, precision 0.01" << endl;
        str << "..........zstdX: z-standard level X, with X between -1 and 22," << endl;
        str << "digicam: digicam specific compression" << endl;
        str << "nectarcam: nectarcam specific compression" << endl;
        str << "lst: lst-cam specific compression" << endl;
        str << "............raw: no compression," << endl;

        throw runtime_error(str.str());
    }

    if (field!="default")
        _explicit_comp[field] = scheme;
}

/*******************************************************************************
 *  WRITE MESSAGE
 *******************************************************************************/
void ProtobufZOFits::writeMessage(const google::protobuf::Message* message)
{
    if (_descriptor == NULL)
    {
        initColumns(message);
        WriteTableHeader(_current_table_name.c_str());
    }

    if (_descriptor != message->GetDescriptor())
    {
        throw runtime_error("Only one kind of message can be written at a given time...");
    }
    _incoming_data->push_back(message);

    fTable.num_rows++;

    if (_incoming_data->size() == fNumRowsPerTile)
    {
        launchNewCompression();
    }

    if (!good())
        throw runtime_error("Could not write to file");
}


/*******************************************************************************
 *  WRITE MESSAGE
 *******************************************************************************/
void ProtobufZOFits::moveToNewTable(string tablename, bool display_stats, bool closing_file)
{

    //launch remaining compressions for this table, if any
    if (_incoming_data->size() != 0)
        launchNewCompression();

    //wait for all compression threads to finish
    uint32 total_waiting_queues = 1;
    while (display_stats && total_waiting_queues != 0)
    {
        total_waiting_queues = 0;
        for (auto it=_compression_queues.begin(); it!=_compression_queues.end(); it++)
            total_waiting_queues+=it->size();
        if (total_waiting_queues != 0)
        {
            cout << "\r" << total_waiting_queues << " buffers awaiting compression           ";
            cout.flush();
            usleep(500000);
        }
        else
            cout << "\r0 buffers awaiting compression           " << endl;
    }

    for (auto it=_compression_queues.begin(); it!= _compression_queues.end(); it++)
        it->wait();

    //also wait for data to be flushed to disk
    total_waiting_queues = _write_to_disk_queue.size();

    while (display_stats && total_waiting_queues != 0)
    {
        cout << "\r" << total_waiting_queues << " buffers awaiting flush to disk             ";
        cout.flush();
        usleep(500000);
        total_waiting_queues = _write_to_disk_queue.size();
    if (total_waiting_queues == 0)
        cout << "\r0 buffers awaiting flush to disk               ";
    }
    _write_to_disk_queue.wait();

    //restart queues if needed
    if (!closing_file && DefaultNumThreads() != 0)
    {
        for (auto it=_compression_queues.begin(); it!=_compression_queues.end(); it++)
            it->start();
        _write_to_disk_queue.start();
    }

    //remember where the last data item finished
    off_t end_of_data = tellp();

    //update date end only if blank. Otherwise it means that it was manually set
    std::vector<Key>::iterator date_end = findkey("DATEEND");
    if (date_end != fKeys.end() && date_end->value == "''")
    {
        const time_t t0 = time(NULL);
        const struct tm *tmp1 = gmtime(&t0);
        std::string str(19, '\0');
        if (tmp1 && strftime(const_cast<char*>(str.data()), 20, "%Y-%m-%dT%H:%M:%S", tmp1))
            SetStr("DATEEND", str, "File closing date");
    }

    //reset any missing field in incoming protocol buffer messages
    _missing_fields.clear();

    // if we are still at the beginning of the table,
    // it means that nothing was written yet: assume
    // that we are starting the very first table
    if (fTableStart == (size_t)(tellp()))
    {
        _current_table_name = tablename;
            //reset quantities used to keep track of a given table's content
            fTable             = Table();
            _descriptor        = NULL;
            _total_num_columns = 0;
            _columns_sizes.clear();
            fDataSum.reset();
            fHeaderSum.reset();
            fRealRowWidth         = 0;
            fCatalogOffset        = 0;
            fCatalogSize          = 0;
            fCheckOffset          = 0;
            _next_buffer_to_write = 0;
            _num_tiles_written    = 0;
            fKeys.clear();
            fRealColumns.clear();
            fCatalog.clear();
            fCatalogSum.reset();
            fRawSum.reset();

            //add standard FITS header entries
            SetStr("XTENSION",   "BINTABLE",         "binary table extension");
            SetInt("BITPIX",     8,                  "8-bit bytes");
            SetInt("NAXIS",      2,                  "2-dimensional binary table");
            SetInt("NAXIS1",     0,                  "width of table in bytes");
            SetInt("NAXIS2",     0,                  "number of rows in table");
            SetInt("PCOUNT",     0,                  "size of special data area");
            SetInt("GCOUNT",     1,                  "one data group (required keyword)");
            SetInt("TFIELDS",    0,                  "number of fields in each row");
            SetStr("EXTNAME",    tablename,          "name of extension table");
            SetStr("CHECKSUM",   "0000000000000000", "Checksum for the whole HDU");
            SetStr("DATASUM",    "         0",       "Checksum for the data block");

            SetBool( "ZTABLE",   true,               "Table is compressed");
            SetInt(  "ZNAXIS1",  0,                  "Width of uncompressed rows");
            SetInt(  "ZNAXIS2",  0,                  "Number of uncompressed rows");
            SetInt(  "ZPCOUNT",  0,                  "");
            SetInt(  "ZHEAPPTR", 0,                  "");
            SetInt(  "ZTILELEN", fNumRowsPerTile,    "Number of rows per tile");
            SetInt(  "THEAP",    0,                  "");
            SetStr(  "RAWSUM",   "         0",       "Checksum of raw little endian data");
            SetFloat("ZRATIO",   0,                  "Compression ratio");
            SetInt(  "ZSHRINK",  1,                  "Catalog shrink factor");
        return;
    }

    //otherwise we are actually moving to a new table.

    //update FITS values
    updateHeaderKeys(true);

    if (display_stats)
    {
        cout << "Comp ratio: ";
        for (auto it=fKeys.begin(); it!=fKeys.end(); it++)
        {
            if (it->key == "ZRATIO")
                cout << it->value << endl;
        }
    }

    //write the actual catalog data
    WriteCatalog();

    fDataSum += fCatalogSum;

    const Checksum checksm = UpdateHeaderChecksum();

    if (!(checksm+fDataSum).valid()) throw runtime_error("Wrong checksum while finalizing table "+_current_table_name);

    //move back to the end of the data and finalize FITS structure
    seekp(end_of_data);

    AlignTo2880Bytes();

    //let the next table know that it does NOT start from beginning of file
    fTableStart = tellp();

    //remember the new table name
    _current_table_name = tablename;

    //free messages currently waiting to be reused as they are unlikely to be the same as the new type of messages written to the new table
    if (_auto_memory_management != NONE)
    {
        for (auto it=_recycled_messages.begin(); it!=_recycled_messages.end(); it++)
            delete *it;
        _recycled_messages.clear();
    }
    //reset quantities used to keep track of a given table's content
    fTable             = Table();
    _descriptor        = NULL;
    _total_num_columns = 0;
    _columns_sizes.clear();
    fDataSum.reset();
    fHeaderSum.reset();
    fRealRowWidth         = 0;
    fCatalogOffset        = 0;
    fCatalogSize          = 0;
    fCheckOffset          = 0;
    _next_buffer_to_write = 0;
    _num_tiles_written    = 0;
    fKeys.clear();
    fRealColumns.clear();
    fCatalog.clear();
    fCatalogSum.reset();
    fRawSum.reset();

    //add standard FITS header entries
    SetStr("XTENSION",   "BINTABLE",         "binary table extension");
    SetInt("BITPIX",     8,                  "8-bit bytes");
    SetInt("NAXIS",      2,                  "2-dimensional binary table");
    SetInt("NAXIS1",     0,                  "width of table in bytes");
    SetInt("NAXIS2",     0,                  "number of rows in table");
    SetInt("PCOUNT",     0,                  "size of special data area");
    SetInt("GCOUNT",     1,                  "one data group (required keyword)");
    SetInt("TFIELDS",    0,                  "number of fields in each row");
    SetStr("EXTNAME",    tablename,          "name of extension table");
    SetStr("CHECKSUM",   "0000000000000000", "Checksum for the whole HDU");
    SetStr("DATASUM",    "         0",       "Checksum for the data block");

    SetBool( "ZTABLE",   true,               "Table is compressed");
    SetInt(  "ZNAXIS1",  0,                  "Width of uncompressed rows");
    SetInt(  "ZNAXIS2",  0,                  "Number of uncompressed rows");
    SetInt(  "ZPCOUNT",  0,                  "");
    SetInt(  "ZHEAPPTR", 0,                  "");
    SetInt(  "ZTILELEN", fNumRowsPerTile,    "Number of rows per tile");
    SetInt(  "THEAP",    0,                  "");
    SetStr(  "RAWSUM",   "         0",       "Checksum of raw little endian data");
    SetFloat("ZRATIO",   0,                  "Compression ratio");
    SetInt(  "ZSHRINK",  1,                  "Catalog shrink factor");


}

void ProtobufZOFits::copyTableFrom(const string& filename,
                                   const string& tablename)
{
    char buffer[81];
    buffer[80] = '\0';
    ifstream input(filename.c_str());

    uint64 tablename_size = tablename.size();

    uint64 table_start = 0;
    uint64 table_end   = 0;
    bool table_found   = false;
    uint64 bytes_read = 0;

    while (!input.eof())
    {
        input.read(buffer, 80);

        string key_name (buffer, 8);

        if (key_name == "XTENSION")
        {
            if (table_found)
            {
                table_end = bytes_read;
                break;
            }

            table_start = bytes_read;
        }

        if (key_name == "EXTNAME ")
        {
            string this_tablename(buffer+11, tablename_size);
            if (this_tablename == tablename)
            {
                table_found = true;
            }
        }
        bytes_read += 80;
    }

    if (table_found && table_end == 0)
    {
        input.clear();
        table_end = bytes_read - 80;
    }

    input.seekg(table_start);

    for (uint64 i=table_start; i<table_end; i+=80)
    {
//        if (i==table_start)
//            cout << buffer << endl;
        input.read(buffer, 80);
        write(buffer, 80);
    }

    fTableStart = tellp();
}

int ProtobufZOFits::getPercentMemUsed()
{
    return (int)(100.f*((float)(fMemPool.getInUse()) / (float)(fMaxUsableMem)));
}
/*******************************************************************************
 *  LAUNCH NEW COMPRESSION
 *******************************************************************************/
void ProtobufZOFits::launchNewCompression()
{
    CompressionTarget comp_target(AddOneCatalogRow());

    //assign input messages to compression target
    comp_target.messages = _incoming_data;
    comp_target.targetId = fTable.num_rows / fNumRowsPerTile;

    //if it is the last compression round, tile might not be full...
    if (fTable.num_rows%fNumRowsPerTile != 0) comp_target.targetId++;

    //and replace incoming data slot by a new vector
    _incoming_data = shared_ptr<std::vector<const google::protobuf::Message*>>(new vector<const google::protobuf::Message*>);

    //cound how many buffers are to be written
    uint32 total_num_buffers    = 0;
    uint64 bytes_in_this_buffer = 0;
    for (auto it=comp_target.messages->begin(); it!= comp_target.messages->end(); it++)
    {
        //serial size of the current message
        uint64 this_size = (*it)->ByteSize();

        //if it does not fit in an entire block, resize blocks
        if (this_size*fNumRowsPerTile > _compression_block_size)
        {
            fMemPool.setChunkSize(this_size*fNumRowsPerTile);
            _compression_block_size = this_size*fNumRowsPerTile;
            total_num_buffers++;
            bytes_in_this_buffer = this_size;
        }
        else
        {
            //can we add it to the current block ?
            if (this_size + bytes_in_this_buffer <= _compression_block_size)
                bytes_in_this_buffer += this_size;
            else
            {
                total_num_buffers++;
                bytes_in_this_buffer = this_size;
            }
        }
    }
    //get one extra buffer, to account for the one that was not filled up entirely
    total_num_buffers++;
    //and yet another one, because if no compression is applied, the output data is a tiny bit larger than the input because of the compression markers
    total_num_buffers++;
    //and yet yet another one, to be able to serialize the input data before compression
    total_num_buffers++;

    if (total_num_buffers*fMemPool.getChunkSize() > fMemPool.getMaxMemory())
    {
        ostringstream str;
        str << yellow << "ERROR: Protobufzofits was not allocated enough memory to compress data to "
               "disk. Either increase the allocated compression memory in the constructor, "
               "or reduce the number of events per tile, also in the constructor. The current "
               "max. available memory for compression is currently set to ";
        str << fMemPool.getMaxMemory();
        str << " bytes while we would need at least ";
        str << total_num_buffers*fMemPool.getChunkSize();
        str << " bytes.";
        str << no_color;
        throw runtime_error(str.str());
    }

    for (uint32 i=0;i<total_num_buffers;i++)
        comp_target.buffers.push_back(fMemPool.malloc());

    //assign the compression job to the least used compression queue.
    const auto imin = min_element(_compression_queues.begin(), _compression_queues.end());

    imin->emplace(comp_target);
}

/*******************************************************************************
 *      WRITE TO DISK
 *******************************************************************************/
bool ProtobufZOFits::writeToDisk(const WriteToDiskTarget& target)
{
    //if the current target is not the next line in queue, wait for the next one to show up
    if (target.targetId != (uint32_t)(_next_buffer_to_write+1))
        return false;

    //MUTEX HERE
    const lock_guard<mutex> lock(_catalog_flush_fence);
    //simply crawl through the list of buffers and write their data
    _next_buffer_to_write++;
    auto it = target.buffers.begin();
    auto jt = target.num_bytes_in_buffer.begin();
    for ( ; it!= target.buffers.end(); it++, jt++)
    {
        _size_written_to_disk+=*jt;
        writeCompressedDataToDisk(it->get(), *jt);
    }
    _num_tiles_written++;

    return true;
}

/*******************************************************************************
 *  COMPRESS MESSAGES
 *******************************************************************************/
bool ProtobufZOFits::compressMessages(const CompressionTarget& comp_target)
{
    //bind only accept const arguments.
    //we need non-const for recursion -> make a copy !
    CompressionTarget nc_comp_target = comp_target;

    //get a buffer where the serial, gathered messages data can be put
    if (nc_comp_target.buffers.empty())
        throw runtime_error("ERROR: no buffer available for serialization");
    shared_ptr<char> gather = nc_comp_target.buffers.front();
    nc_comp_target.buffers.pop_front();

    //get a first target buffer, where to write the compressed data
    if (nc_comp_target.buffers.empty())
        throw runtime_error("ERROR: no buffer available for compression");
    shared_ptr<char> comp_buf = nc_comp_target.buffers.front();
    nc_comp_target.buffers.pop_front();

    //reserve space for tile header. +4 bytes are left to allow for checksum calculation
    FITS::TileHeader* tile_head = reinterpret_cast<FITS::TileHeader*>(comp_buf.get()+4);

    WriteToDiskTarget disk_target;

    //launch the recursive crawl of the message's structure
    int32 bytes_written = sizeof(FITS::TileHeader);
    int32 column_indices = 0;

    //the input list of messages is not const so that messages can be recycled.
    //make this incoming parameter const
    vector<const google::protobuf::Message*> const_messages;
    for (auto it=comp_target.messages->begin(); it!=comp_target.messages->end(); it++)
        const_messages.push_back(*it);

    compressMessageFields(const_messages, column_indices, gather.get(), comp_buf, bytes_written, nc_comp_target, disk_target);

    //add the last buffer to the disk target
    disk_target.buffers.push_back(comp_buf);
    disk_target.num_bytes_in_buffer.push_back(bytes_written);
    disk_target.targetId = nc_comp_target.targetId;

    //count the total number of compressed bytes
       uint32_t total_compressed_bytes = 0;
       for (auto it=disk_target.num_bytes_in_buffer.begin(); it!=disk_target.num_bytes_in_buffer.end(); it++)
           total_compressed_bytes += *it;

    //set the tile header properly
    tile_head->id[0] = 'T';
    tile_head->id[1] = 'I';
    tile_head->id[2] = 'L';
    tile_head->id[3] = 'E';
    tile_head->numRows = nc_comp_target.messages->size();
    tile_head->size = total_compressed_bytes - sizeof(FITS::TileHeader);

    //FIXME this was a debug check. should be disabled at runtime
    if (column_indices != (int32)(_total_num_columns))
    {
        ostringstream str;
        str << "ERROR: did not write the expected number of columns: got " << column_indices << " vs " << _total_num_columns << " expected";
        throw runtime_error(str.str());
    }

    //put the buffers to write to disk in the writing queue
    _write_to_disk_queue.emplace(disk_target);

    //if auto memory management, delete messages that were serialized already
    if (_auto_memory_management == AUTO)
    {
        for (auto it=comp_target.messages->begin(); it!=comp_target.messages->end(); it++)
            delete *it;
        return true;
    }

    if (_auto_memory_management == NONE)
        return true;

    //recycle the messages that were given as an input. We can const-cast them as protobufZOFits can indeed change them
    const lock_guard<mutex> lock(_recycle_fence);
    for (auto it=comp_target.messages->begin(); it!=comp_target.messages->end(); it++)
        _recycled_messages.push_back(const_cast<google::protobuf::Message*>(*it));

    return true;
}

/*******************************************************************************
 *      GET RECYCLED MESSAGE
 *******************************************************************************/
google::protobuf::Message* ProtobufZOFits::getRecycledMessage()
{
    const lock_guard<mutex> lock(_recycle_fence);

    if (_recycled_messages.empty())
        return NULL;

    google::protobuf::Message* to_return = _recycled_messages.front();
    _recycled_messages.pop_front();

    return to_return;
}

/*******************************************************************************
 *      COMPRESS MESSAGE FIELDS
 *      gathers similar values scattered accross several messages and compress them to disk
 *******************************************************************************/
void ProtobufZOFits::compressMessageFields(const vector<const google::protobuf::Message*>& messages,
                                                int32&                 col_index,
                                                char*                  gather_buf,
                                                shared_ptr<char>&      compres_buff,
                                                int32&                 comp_bytes_written,
                                                CompressionTarget&     comp_target,
                                                WriteToDiskTarget&     disk_target,
                                                const string&          name)
{
    //FIXME remove this check
    if (messages.size() == 0)
        throw runtime_error("No message found for compression");

    //retrieve the message metadata
    const google::protobuf::Descriptor* desc   = messages[0]->GetDescriptor();

    //Append a . to the prefix, only if it is not null
    const string prefix_name = (name=="") ? "" : name+".";

    //For all fields in this message, either gather the values
    //or call this function recursively if it contains other messages.
    for (int32 i=0;i<desc->field_count(); i++)
    {
        //build the full name and ID of this field
        const string full_name = prefix_name + std::string{desc->field(i)->name()};
        if (isVetoed(full_name))
            continue;

        int32 bytes_gathered = 0;
        switch (desc->field(i)->type())
        {
            case google::protobuf::FieldDescriptor::TYPE_DOUBLE:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += serialize<double>(gather_buf+bytes_gathered, messages[j], desc->field(i), messages[j]->GetReflection(), col_index);
                break;

            case google::protobuf::FieldDescriptor::TYPE_FLOAT:
                for (uint32 j=0;j<messages.size();j++)
                     bytes_gathered += serialize<float>(gather_buf+bytes_gathered, messages[j], desc->field(i), messages[j]->GetReflection(), col_index);
                break;

            case google::protobuf::FieldDescriptor::TYPE_INT64:
            case google::protobuf::FieldDescriptor::TYPE_SFIXED64:
            case google::protobuf::FieldDescriptor::TYPE_SINT64:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += serialize<int64>(gather_buf+bytes_gathered, messages[j], desc->field(i), messages[j]->GetReflection(), col_index);
                break;

            case google::protobuf::FieldDescriptor::TYPE_FIXED64:
            case google::protobuf::FieldDescriptor::TYPE_UINT64:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += serialize<uint64>(gather_buf+bytes_gathered, messages[j], desc->field(i), messages[j]->GetReflection(), col_index);
               break;

            case google::protobuf::FieldDescriptor::TYPE_INT32:
            case google::protobuf::FieldDescriptor::TYPE_SFIXED32:
            case google::protobuf::FieldDescriptor::TYPE_SINT32:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += serialize<int32>(gather_buf+bytes_gathered, messages[j], desc->field(i), messages[j]->GetReflection(), col_index);
                break;

            case google::protobuf::FieldDescriptor::TYPE_FIXED32:
            case google::protobuf::FieldDescriptor::TYPE_UINT32:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += serialize<uint32>(gather_buf+bytes_gathered, messages[j], desc->field(i), messages[j]->GetReflection(), col_index);
                break;

            case google::protobuf::FieldDescriptor::TYPE_BOOL:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += serialize<bool>(gather_buf+bytes_gathered, messages[j], desc->field(i), messages[j]->GetReflection(), col_index);
                break;
            case google::protobuf::FieldDescriptor::TYPE_ENUM:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += serialize<google::protobuf::EnumValueDescriptor>(gather_buf+bytes_gathered, messages[j], desc->field(i), messages[j]->GetReflection(), col_index);
                break;

            case google::protobuf::FieldDescriptor::TYPE_STRING:
            case google::protobuf::FieldDescriptor::TYPE_BYTES:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += serialize<char>(gather_buf+bytes_gathered, messages[j], desc->field(i), messages[j]->GetReflection(), col_index);
                break;
            case google::protobuf::FieldDescriptor::TYPE_GROUP:
                continue;
            break;

            case google::protobuf::FieldDescriptor::TYPE_MESSAGE:
            {
                //for messages, we must recursively call this function. If messages are repeated, empty slots are filled-in by the default value
                if (desc->field(i)->is_repeated())
                {
                    //look up the expected max. number of messages
                    if (_num_expected_child.find(col_index) == _num_expected_child.end())
                    {
                        ostringstream str;
                        str << "Mapping to number of expected children nowhere to be found for column " << col_index << " num entries: " << _num_expected_child.size();
                        throw runtime_error(str.str());
                    }

                    int32 num_children = _num_expected_child[col_index];

                    //for all the expected children
                    for (int32 k=0;k<num_children;k++)
                    {
                        vector<const google::protobuf::Message*> child_messages;
                        //for all the input messages
                        for (uint32 j=0;j<messages.size();j++)
                        {
                            //TODO find a more effective check
                            //check that no input message exceeds the max. number of expected children
                            if (messages[j]->GetReflection()->FieldSize(messages[j][0], desc->field(i)) > num_children)
                                    throw runtime_error("The number of repeated messages from the initialization message is less than for the subsequent messages");

                            if (messages[j]->GetReflection()->FieldSize(messages[j][0], desc->field(i)) > k)
                            {//stack up this message
                                child_messages.push_back(&(messages[j]->GetReflection()->GetRepeatedMessage(*(messages[j]), desc->field(i), k)));
                            }
                            else
                            {//no message available at this index. Add the default message. FIXME I am not sure at all that "message_type" does what I think it should do...
                                child_messages.push_back(google::protobuf::MessageFactory::generated_factory()->GetPrototype(desc->field(i)->message_type()));
                            }
                        }

                        if (desc->field(i)->message_type()->name() == "AnyArray")
                        {//in case of cta array, do the serialization right away
                            for (uint32 j=0;j<child_messages.size();j++)
                                bytes_gathered += serialize<AnyArray>(gather_buf+bytes_gathered, child_messages[j], desc->field(i), child_messages[j]->GetReflection(), col_index);
                            compressBuffer(gather_buf, compres_buff, bytes_gathered, comp_bytes_written, col_index, comp_target, disk_target);
                        }
                        else
                        {//otherwise, call the function with these message
                            ostringstream str;
                            str << full_name << "#" << k;
                            compressMessageFields(child_messages, col_index, gather_buf, compres_buff, comp_bytes_written, comp_target, disk_target, str.str());
                        }
                     }
                }
                else //single message fields
                {
                    vector<const google::protobuf::Message*> child_messages;
                    for (uint32 j=0;j<messages.size();j++)
                        child_messages.push_back(&(messages[j]->GetReflection()->GetMessage(*(messages[j]), desc->field(i))));
                    if (desc->field(i)->message_type()->name() == "AnyArray")
                    {
                        for (uint32 j=0;j<child_messages.size();j++)
                            bytes_gathered += serialize<AnyArray>(gather_buf+bytes_gathered, child_messages[j], desc->field(i), child_messages[j]->GetReflection(), col_index);

                        compressBuffer(gather_buf, compres_buff, bytes_gathered, comp_bytes_written, col_index, comp_target, disk_target);
                    }
                    else
                    {
                        compressMessageFields(child_messages, col_index, gather_buf, compres_buff, comp_bytes_written, comp_target, disk_target, full_name);
                    }
                }

                //in the case of messages, the compression has been done already.
                continue;
            }
            break;

            default:
                throw runtime_error("Unkown field type");
        };//switch field type

        //All values of the current field were serialize to gather_buf. the number of bytes is bytes_gathered.
        compressBuffer(gather_buf, compres_buff, bytes_gathered, comp_bytes_written, col_index, comp_target, disk_target);
    } //for all fields

    return;
}

/*******************************************************************************
 *  SPLIT HIGH LOW 16
 *******************************************************************************/
void ProtobufZOFits::splitHiLo16(char* buffer, uint32 num_bytes)
{
    if (num_bytes%2 != 0)
    {
        throw runtime_error("Number of bytes not multiple of 2");
    }
    vector<char> hi_words_store(num_bytes/2);
    vector<char> lo_words_store(num_bytes/2);
    char* hi_words = hi_words_store.data();
    char* lo_words = lo_words_store.data();
    char* input    = buffer;
    for (uint32 k=0;k<num_bytes;k+=2)
    {
        *hi_words++ = *input++;
        *lo_words++ = *input++;
    }
    memcpy(buffer,             hi_words_store.data(), num_bytes/2);
    memcpy(buffer+num_bytes/2, lo_words_store.data(), num_bytes/2);
}

void ProtobufZOFits::splitHiLo32(char* buffer, uint32 num_bytes)
{
    if (num_bytes%4 != 0)
    {
        throw runtime_error("Number of bytes not multiple of 4");
    }
    vector<char> hi_words_store(num_bytes/2);
    vector<char> lo_words_store(num_bytes/2);
    char* hi_words = hi_words_store.data();
    char* lo_words = lo_words_store.data();
    char* input    = buffer;
    for (uint32 k=0;k<num_bytes;k+=4)
    {
        *hi_words++ = *input++;
        *hi_words++ = *input++;
        *lo_words++ = *input++;
        *lo_words++ = *input++;
    }
    memcpy(buffer,             hi_words_store.data(), num_bytes/2);
    memcpy(buffer+num_bytes/2, lo_words_store.data(), num_bytes/2);
}

/*******************************************************************************
 *  ZLIB COMPRESS
 *  FIXME zlib uses uLongf, which on some architectures (AIX and probably windows) is 32 bits instead of 64 -> add a run-time check
 *******************************************************************************/
uint64_t ProtobufZOFits::zlibCompress(char* dest, const char* src, uint32 num_bytes)
{
    uint64_t compressed_size = _compression_block_size - sizeof(FITS::TileHeader) - 4 - 40;

    if (compress((Bytef*)(dest), (uLongf*)(&compressed_size), (const Bytef*)(src), num_bytes) != Z_OK)
    {
        int32 returnVal = compress((Bytef*)(dest), (uLongf*)(&compressed_size), (const Bytef*)(src), num_bytes);
        ostringstream str;
        str << "Could not compress with zlib. error code: " << returnVal << ". num_bytes=" << num_bytes;
        throw runtime_error(str.str());
    }
    return compressed_size;
}

int32 num_compressed_buffers_debug = 0;


/*******************************************************************************
 *      COMPRESS BUFFER
 *******************************************************************************/
void ProtobufZOFits::compressBuffer(char*             src,
                                   shared_ptr<char>&  dest,
                                   int32              num_bytes,
                                   int32&             bytes_in_dest,
                                   int32&             col_index,
                                   CompressionTarget& comp_target,
                                   WriteToDiskTarget& disk_target)
{
    //get the target block header. Make a copy so that several threads can work in parallel
    FITS::Compression scheme = fRealColumns[col_index].block_head;
    uint32 block_head_size = scheme.getSizeOnDisk();

    //add current gathered bytes to the total raw, uncompressed size
    _raw_heap_size += num_bytes;

    //FIXME should this stay here or not ?
    if (num_bytes%4 != 0) num_bytes += 4-(num_bytes%4);

    //verify that the target buffer has enough room to host the compressed data
    if (bytes_in_dest + num_bytes + block_head_size + 4 > _compression_block_size)
    {//get a new compressed buffer
        disk_target.num_bytes_in_buffer.push_back(bytes_in_dest);
        disk_target.buffers.push_back(dest);

        bytes_in_dest = 0;
        if (!comp_target.buffers.empty())
        {
            dest = comp_target.buffers.front();
            comp_target.buffers.pop_front();
        }
        else
        {
            cout << yellow << "WARNING: taking one extra buffer..." << no_color << endl;
            dest = fMemPool.malloc();
        }
    }

    char* compres_buff_target = dest.get() + bytes_in_dest + 4;
    //check the size to be copied. If too small, make it raw
    if (false)//num_bytes < 10)
    {
        FITS::Compression raw_scheme;
        raw_scheme.SetBlockSize(num_bytes+block_head_size);
        raw_scheme.Memcpy(compres_buff_target);
        bytes_in_dest += raw_scheme.getSizeOnDisk();
        memcpy(compres_buff_target+raw_scheme.getSizeOnDisk(), src, num_bytes);
        //remember number of compressed bytes in catalog
        comp_target.catalog[col_index].first = raw_scheme.getSizeOnDisk() + num_bytes;
        //move to next column
        col_index++;

        return;
    }

    //otherwise follow the requested compression
    char* target          = compres_buff_target + block_head_size;
    uint32 max_output_size = _compression_block_size-(bytes_in_dest+block_head_size+4);

    uint32 compressed_size = 0;

    for (uint32 i=0;i<scheme.getNumProcs();i++)
    {
        switch (scheme.getProc(i))
        {
            case FITS::eCTAZlib:
                compressed_size = zlibCompress(target, src, num_bytes);
                if (compressed_size >= max_output_size)
                    throw runtime_error("written size exceeded buffer size zlib");
                //FIXME check that it went well
                break;

            case FITS::eCTAzstd:
            {
                size_t available_bytes_in_dest = _compression_block_size - sizeof(FITS::TileHeader) - 44;

                compressed_size = ZSTD_compress(target, available_bytes_in_dest,
                                                src, num_bytes,
                                                _zstd_level);

                if (ZSTD_isError(compressed_size))
                    throw runtime_error("Something went wrong while using zstd compression");
            }
            break;

            case FITS::eCTALZO:
            {
                lzo_uint out_len;
                LZO_HEAP_ALLOC(wrkmem, LZO1X_1_MEM_COMPRESS);

                if (lzo1x_1_compress((unsigned char*)(src), num_bytes, (unsigned char*)(target), &out_len, wrkmem) != LZO_E_OK)
                    throw runtime_error("Something went wrong during LZO compression");

                compressed_size = out_len;

                if (compressed_size >= max_output_size)
                    throw runtime_error("written size exceeded buffer size lzo");

            }
                break;

            case FITS::eCTARICE:
            {
                checkArrayValueSize(num_bytes, 2, FITS::eCTARICE);
                memcpy(target, &num_bytes, sizeof(int32));
                target          += sizeof(num_bytes);
                compressed_size += sizeof(num_bytes);
                int64 size_written = fits_rcomp_short((int16*)(src), num_bytes/2, (unsigned char*)(target), max_output_size, 1);
                //FIXME the last parameter "1" is probably not correct
                if (size_written > max_output_size || size_written < 0)
                    throw runtime_error("RICE compression seems to have failed...");
                //FIXME check that it went well... better than above
                compressed_size += size_written;

                if (compressed_size >= max_output_size)
                    throw runtime_error("written size exceeded buffer size rice");
            }
                break;

            case FITS::eCTASplitHiLo16:
                checkArrayValueSize(num_bytes, 2, FITS::eCTASplitHiLo16);
                splitHiLo16(src, num_bytes);
                break;

            case FITS::eCTA128Offset:
            {
                checkArrayValueSize(num_bytes, 2, FITS::eCTA128Offset);
                int16* values = reinterpret_cast<int16*>(src);
                for (int32 i=0;i<num_bytes/2;i++)
                {
                    values[i] += 128;
                }
            }
            break;
            case FITS::eCTALocalDiff:
            {
                checkArrayValueSize(num_bytes, 2, FITS::eCTALocalDiff);
                uint16* data = reinterpret_cast<uint16*>(src);
                uint32  nitems = num_bytes/2;
                //make groups of 50
                for (uint32 i=0,j=1;i<nitems;i++,j++)
                {

                    if (j==50) {j=1; data = &data[50];}
                    data[j] -= data[0];
                }
            }
            break;
            case FITS::eCTASplitHiLo32:
                checkArrayValueSize(num_bytes, 4, FITS::eCTASplitHiLo32);
                splitHiLo32(src, num_bytes);
                break;

            case FITS::kFactRaw:
                memcpy(target, src, num_bytes);
                compressed_size = num_bytes;
                break;

            case FITS::kFactSmoothing:
                checkArrayValueSize(num_bytes, 2, FITS::kFactSmoothing);
                applySMOOTHING(src, num_bytes/2);
                break;

            case FITS::eCTADiff:
            {
                checkArrayValueSize(num_bytes, 2, FITS::eCTADiff);
                int16* src16 = reinterpret_cast<int16*>(src);
                for (uint32 i=(num_bytes/2)-1;i!=0;i--)
                    src16[i] -= src16[i-1];
            }
            break;

            case FITS::eCTAHalfDiff32:
            {
                checkArrayValueSize(num_bytes, 4, FITS::eCTAHalfDiff32);
                int32* src32 = reinterpret_cast<int32*>(src);
                for (uint32 i=(num_bytes/8)-1;i!=0;i--)
                {
                    src32[i] -= src32[i-1];
                }
            }

            case FITS::eCTADoubleDiff:
            {
                checkArrayValueSize(num_bytes, 2, FITS::eCTADoubleDiff);
                int16* src16 = reinterpret_cast<int16*>(src);
                for (uint32 i=num_bytes/2;i!=0;i--)
                    src16[i] -= src16[i-1];
                for (uint32 i=num_bytes/2;i!=0;i--)
                    src16[i] -= src16[i-1];
            }
            break;

            case FITS::kFactHuffman16:
            {
                checkArrayValueSize(num_bytes, 2, FITS::kFactHuffman16);

                string huffman_output;
                Huffman::Encode(huffman_output, reinterpret_cast<const uint16_t*>(src), num_bytes/2);
                reinterpret_cast<uint32*>(target)[0] = huffman_output.size();
                memcpy(&target[sizeof(uint32)], huffman_output.data(), huffman_output.size());
                compressed_size += huffman_output.size()+sizeof(uint32);
            }
            break;

            case FITS::eCTAHalfman16:
            {
                checkArrayValueSize(num_bytes, 4, FITS::eCTAHalfman16);
                string huffman_output;
                int32 num1 = num_bytes/4;
                int32 num2 = num_bytes/2 - num1; //if num_bytes/2 is odd

                Huffman::Encode(huffman_output, reinterpret_cast<const uint16_t*>(src), num1);
                int32 previous_size = huffman_output.size();
                reinterpret_cast<uint32*>(target)[0] = previous_size;
                Huffman::Encode(huffman_output, reinterpret_cast<const uint16_t*>(src+num1*2), num2);
                reinterpret_cast<uint32*>(target)[1] = huffman_output.size() - previous_size;
                memcpy(&target[2*sizeof(uint32)], huffman_output.data(), huffman_output.size());
                compressed_size += huffman_output.size()+2*sizeof(uint32);
            }
            break;

            case FITS::eCTASameValues:
            {
                checkArrayValueSize(num_bytes, 4, FITS::eCTASameValues);

                //this is the number of 32 bits values that must be dealt with
                uint32 total_num_values = num_bytes/sizeof(uint32);

                uint32* src32 = reinterpret_cast<uint32*>(src);
                //take an intermediate buffer twice as large as the input on, to be able to handle the worst case scenario
                uint32* buffer = new uint32[total_num_values*2 + 1];
                //reserve the first slot to remember how many values will be stored
                uint32* buf_target = buffer+1;

                //initialize variables to count number of occuring values
                uint32 this_value = 0;
                uint32 num_values = 0;
                uint32 num_pairs_of_values = 0;
                //crawl through the input array and accumulate same values
                for (uint32 i=0;i<total_num_values;)
                {
                    this_value = src32[i++];
                    num_values = 1;
                    while (i < total_num_values && src32[i] == this_value)
                    {
                        num_values++;
                        i++;
                    }
                    //we've reached a new value, store the previous one in temp buffer
                    *buf_target++ = num_values;
                    *buf_target++ = this_value;
                    num_pairs_of_values++;
                }

                //remember in the first element the number of values found
                buffer[0] = num_pairs_of_values;

                if (_compression_block_size < (num_pairs_of_values*2+1)*sizeof(uint32))
                {
                    //uint32* int32values = reinterpret_cast<uint32*>(src);
                   // for (uint32 i=0;i<num_bytes/4;i++)
                    //    cout << int32values[i] << " ";
                   // cout << endl;
                    ostringstream str;
                    str << "Exceeding size of available buffer while doing eCTASameValues pre-process " << num_bytes << " " << num_pairs_of_values << " " << _compression_block_size;
                    throw runtime_error(str.str());
                }
                num_bytes = (num_pairs_of_values*2+1)*sizeof(uint32);

                //copy the data back in place in the original buffer
                memcpy(src, buffer, num_bytes);

                delete[] buffer;
            }
            break;

            case FITS::eCTASparseValues:
            {//very similar to eCTASameValues, see above for comments
                checkArrayValueSize(num_bytes, 4, FITS::eCTASparseValues);
                uint32 total_num_values = num_bytes / sizeof(uint32);

                int32* src32 = reinterpret_cast<int32*>(src);
                int32* buffer = new int32[total_num_values*2 + 2]; //first value is hollow value, second is number of values
                int32* target = buffer+2;
                uint32 num_output_values = 0;

                for (uint32 i=0;i<total_num_values;)
                {
                    //first skip through the current "zero" values
                    uint32 this_num_hollow = 0;
                    while (src32[i] == _sparse_value)
                    {
                        this_num_hollow++;
                        i++;
                        if (i >= total_num_values)
                            break;
                    }
                    target[num_output_values++] = this_num_hollow;

                    //exit if we've reached the end of the input array
                    if (i >= total_num_values)
                        break;

                    //the add the next "real" value to the output buffer
                    target[num_output_values++] = src32[i++];
                }

                buffer[0] = _sparse_value;
                reinterpret_cast<uint32*>(&buffer[1])[0] = num_output_values;

                //cout << "Original: " << endl;
                //for (uint32 i=0;i<100;i++)
                //    cout << src32[i] << " ";
                //cout << endl << "Compressed: " << endl;
                //for (uint32 i=0;i<100;i++)
                //    cout << target[i] << " ";
                //cout << endl << endl;

                if (_compression_block_size < (num_output_values+2)*sizeof(uint32))
                    throw runtime_error("Exceeding size of available buffer while doing eCTASparseValues pre-process");

                num_bytes = (num_output_values+2)*sizeof(uint32);

                memcpy(src, buffer, num_bytes);

                delete[] buffer;
            }
            break;
/*
case FITS::eCTASparseValues:
{//very similar to eCTASameValues, see above for comments
    checkArrayValueSize(num_bytes, 4, FITS::eCTASparseValues);
    uint32 total_num_values = num_bytes / sizeof(uint32);
    uint32* src32 = reinterpret_cast<uint32*>(src);
    uint32* buffer = new uint32[total_num_values*2 + 1];
    uint32* buf_indices = buffer+1;
    uint32* buf_values  = buffer + (total_num_values + 1);
    uint32 num_pairs_of_values = 0;
    for (uint32 i=0;i<total_num_values;i++)
    {
        if (src32[i] == 0)
            continue;

        *buf_indices++ = i;
        *buf_values++ = src32[i];
        num_pairs_of_values++;
    }
    buffer[0] = num_pairs_of_values;

    if (_compression_block_size < (num_pairs_of_values*2+1)*sizeof(uint32))
        throw runtime_error("Exceeding size of available buffer while doing eCTASparseValues pre-process");

    num_bytes = (num_pairs_of_values*2+1)*sizeof(uint32);

    memcpy(src, buffer, num_pairs_of_values*sizeof(uint32) + sizeof(uint32));
    memcpy(src+((num_pairs_of_values+1)*sizeof(uint32)), buffer+ (total_num_values+1), num_pairs_of_values*sizeof(uint32));
    delete[] buffer;
}
break;
*/
            //TODO verify that the usage of this compression is limited to floating point fields
            case FITS::eCTALossyFloats:
            {
                //TODO remove this check once only floats can use this compression as their size is always 4
                checkArrayValueSize(num_bytes, 4, FITS::eCTALossyFloats);

                float precision = 0.01f; //for now, we only deal with this precision: no quantization involved
                float delta = precision / 2.f; //value to add before devision to compensate for the floor effect

                float* f_src = reinterpret_cast<float*>(src);
                int32* i_dst = reinterpret_cast<int32*>(src); //we transform the data in-place

                int32 num_consumed_bytes = 0;

                while (num_consumed_bytes < num_bytes)
                {
                    //get the number of values for this chunk
                    uint32 this_num_values = *i_dst / sizeof(float);
                    i_dst++;
                    f_src++;

                    for (uint32 i=0;i<this_num_values;i++)
                    {
                        if (*f_src >= 0)
                            *i_dst++ = (int32)((*f_src++ + delta) / precision);
                        else
                            *i_dst++ = (int32)((*f_src++ - delta) / precision);
                    }

                    num_consumed_bytes += (this_num_values+1)*sizeof(float);
                }

            }
            break;

            case FITS::eCTALossyInt16:
            {
                //We will degrade the data. But we must NOT screw up the sizes of the blocks
                //num_bytes is the total size that we must NOT exceed
                int32 bytes_consumed = 0;
                int32 this_size      = reinterpret_cast<int32*>(src)[0];
                bytes_consumed += sizeof(int32);

                while (bytes_consumed < num_bytes)
                {
                    checkArrayValueSize(this_size, 2, FITS::eCTALossyInt16);

                    uint16* isrc = reinterpret_cast<uint16*>(src+bytes_consumed);
                    float  average_error     = 0;
                    uint64 num_average_error = 0;

                    uint16 shift = _lossy_int16_quantization / 2;

                    uint16 new_value = 0;

                    for (int32 i=0;i<this_size/2;i++)
                    {
                        new_value = ((isrc[i] + shift) / _lossy_int16_quantization)*_lossy_int16_quantization;

                        average_error += abs(isrc[i] - _lossy_int16_quantization*new_value);
                        num_average_error++;

                        isrc[i] = new_value;
                    }
                    _lossy_average_error += (average_error / num_average_error);
                    _lossy_num_error_samples ++;

                    bytes_consumed += this_size;
                    this_size = reinterpret_cast<int32*>(src+bytes_consumed)[0];
                    bytes_consumed += sizeof(int32);
                }
            }
            break;

            case FITS::eCTALossyInt32:
            {
                //We will degrade the data. But we must NOT screw up the sizes of the blocks
                //num_bytes is the total size that we must NOT exceed
                int32 bytes_consumed = 0;
                int32 this_size      = reinterpret_cast<int32*>(src)[0];
                bytes_consumed += sizeof(int32);

                while (bytes_consumed < num_bytes)
                {
                    checkArrayValueSize(this_size, 4, FITS::eCTALossyInt32);

                    uint32* isrc = reinterpret_cast<uint32*>(src+bytes_consumed);
                    float  average_error     = 0;
                    uint64 num_average_error = 0;

                    uint32 shift = _lossy_int16_quantization / 2;

                    uint32 new_value = 0;

                    for (int32 i=0;i<this_size/4;i++)
                    {
                        new_value = ((isrc[i] + shift) / _lossy_int16_quantization)*_lossy_int16_quantization;

                        average_error += abs(int(isrc[i] - _lossy_int16_quantization*new_value));
                        num_average_error++;

                        isrc[i] = new_value;
                    }
                    _lossy_average_error += (average_error / num_average_error);
                    _lossy_num_error_samples ++;

                    bytes_consumed += this_size;
                    this_size = reinterpret_cast<int32*>(src+bytes_consumed)[0];
                    bytes_consumed += sizeof(int32);
                }
            }
            break;

            default:
                    throw runtime_error("Unhandled compression scheme requested");
                break;
        };//switch
    }//for all procs


    if (compressed_size+bytes_in_dest+block_head_size > (uint32)(_compression_block_size))
    {
        //FIXME this must never happen !
        ostringstream ss;
        ss << "Exceeded compression buffer size... " << compressed_size << " " << max_output_size << " " << bytes_in_dest << " " << block_head_size << " " << _compression_block_size << " " << num_bytes;
        throw runtime_error(ss.str());
    }

    if (false)//num_compressed_buffers_debug++ < 5)
    {
        ostringstream str;
        str << "/scratch/sample_data" << col_index << ".txt";
        ofstream out_samples;
        out_samples.open(str.str());
        int16* sample_data = reinterpret_cast<int16*>(src);
        for (int32 i=0;i<num_bytes/2;i++) {
            out_samples << sample_data[i] << " ";
            if (i == num_bytes/4) out_samples << endl;
            }
        out_samples << endl << endl << endl;
        out_samples.close();
        cout << "Col: " << col_index << " Bytes=(" << num_bytes << "," << compressed_size << "," << block_head_size  << ")" << red << " ratio= " << (float)(num_bytes) / (float)(compressed_size + block_head_size) << no_color << endl;
    }

    //update the header block and write it to output
    scheme.SetBlockSize(compressed_size+block_head_size);
    scheme.Memcpy(compres_buff_target);
    bytes_in_dest += block_head_size + compressed_size;

    //remember number of compressed bytes in catalog
    comp_target.catalog[col_index].first = block_head_size + compressed_size;

    //move to next column
    col_index++;
}

//flushHeader updates the fits header of the current table, with the latest columns and row width.
void ProtobufZOFits::updateHeaderKeys(bool finalUpdate)
{
    uint64 row_width = 0;
    for (uint32 i=0;i<_columns_sizes.size();i++)
    {
        ostringstream entry_name;
        entry_name << "ZFORM" << i+1;

        //get the column type
        char type = fRealColumns[i].col.type;
        switch (type)
        {
            case 'U':
                type = 'I';
                break;
            case 'V':
                type = 'J';
                break;
            case 'W':
                type = 'K';
                break;
            case 'S':
                type = 'B';
                break;
            default:
                break;
        };

        switch (type)
        {
            case 'I':
                row_width += sizeof(int16)*_columns_sizes[i];
                break;
            case 'J':
            case 'E':
                row_width += sizeof(int32)*_columns_sizes[i];
                break;

            case 'K':
            case 'D':
                row_width += sizeof(int64)*_columns_sizes[i];
                break;

            case 'B':
            case 'L':
            case 'A':
                row_width += _columns_sizes[i];
                break;
            default:
                throw runtime_error("Unexpected column type...");
                break;
        };

        //set proper size
        ostringstream correct_type;
        correct_type << _columns_sizes[i] << type;
        SetStr(entry_name.str(), correct_type.str());
    }

    SetInt("ZNAXIS1", row_width);

    fRealRowWidth = row_width;

    //updates normally done in ZOFits::close.

    if (fThreadsException != std::exception_ptr())
    std::rethrow_exception(fThreadsException);

    int64 heap_size         = 0;
    int64 compressed_offset = 0;
    int32 current_tile      = 0;
    for (auto it=fCatalog.begin(); it!= fCatalog.end(); it++)
    {
        compressed_offset += sizeof(FITS::TileHeader);
        heap_size         += sizeof(FITS::TileHeader);
        for (uint32_t j=0; j<it->size(); j++)
        {
            heap_size += (*it)[j].first;
            if ((*it)[j].first < 0) throw runtime_error("Negative block size");
            (*it)[j].second = compressed_offset;
            compressed_offset += (*it)[j].first;
            if ((*it)[j].first == 0)
                (*it)[j].second = 0;
        }

        //only deal with the tiles that were written to disk already
        current_tile ++;
        if (current_tile >= _num_tiles_written) break;
    }

//    uint32 shrink_factor = 1;

    if (finalUpdate)
    {
        //shrink_factor =
        ShrinkCatalog();
        SetInt("ZNAXIS2", fTable.num_rows);
        SetInt("ZHEAPPTR", fNumTiles*fTable.num_cols*sizeof(uint64_t)*2);
    }
    else
    {
        SetInt("ZNAXIS2",  _num_tiles_written*fNumRowsPerTile);
        SetInt("ZHEAPPTR", fNumTiles*fTable.num_cols*sizeof(uint64)*2);
   }

    const uint32_t total_num_tiles_written = (fTable.num_rows + fNumRowsPerTile-1)/fNumRowsPerTile;
    const uint32   total_catalog_width = 2*sizeof(int64)*fTable.num_cols;

    if (finalUpdate)
    {
        SetInt("THEAP",  total_num_tiles_written*total_catalog_width);
        SetInt("NAXIS1", total_catalog_width);
        SetInt("NAXIS2", total_num_tiles_written);
        SetStr("RAWSUM", std::to_string((long long int)(fRawSum.val())));
        if (heap_size != 0)
        {
            const float compression_ratio = (float)(_raw_heap_size)/(float)heap_size;
 //           cout << "heap sizes: " << _raw_heap_size << " " << heap_size << endl;
            SetFloat("ZRATIO", compression_ratio);
        }
    }
    else
    {
        SetInt("THEAP", _num_tiles_written*total_catalog_width);
        SetInt("NAXIS1", total_catalog_width);
        SetInt("NAXIS2", _num_tiles_written);
    }

    //add to the heap size the size of the gap between the catalog and the actual heap
    if ((uint32)(_num_tiles_written) < fCatalogSize)
        heap_size += (fCatalogSize - _num_tiles_written)*fTable.num_cols*sizeof(uint64_t)*2;

    SetInt("PCOUNT", heap_size, "size of special data area");
}

/*******************************************************************************
 *  CLOSE
 *******************************************************************************/
bool ProtobufZOFits::close(bool display_stats)
{
    if (!is_open()) return true;

    moveToNewTable("NO_TABLE", display_stats, true);

    std::ofstream::close();

#ifndef __clang__
            if (fCurrentFileDescriptor != NULL)
            {
                flock(fileno(fCurrentFileDescriptor), LOCK_UN);
                fclose(fCurrentFileDescriptor);
            }

            fCurrentFileDescriptor = NULL;
#endif

    return true;
}

bool ProtobufZOFits::close()
{
    return close(true);
}

void ProtobufZOFits::flushCatalog()
{
    //MUTEX HERE
    if (_num_tiles_written == 0)
        return;

    const lock_guard<mutex> lock(_catalog_flush_fence);
    updateHeaderKeys();
    FlushHeader();
    WriteCatalog();
}


/*******************************************************************************
 *  ADD ANY ARRAY COLUMN
 *******************************************************************************/
void ProtobufZOFits::addAnyArrayColumn(const google::protobuf::Message& message, const string& name, const string& )
{
    //no veto check is necessary here because either the veto was done earlier, or this is the top message, surely not to be vetoed.

    //retrieve the message descriptor
    const google::protobuf::Descriptor* desc = message.GetDescriptor();

    //retrieve the fields of interest to figure out the content of the binary array
    const google::protobuf::FieldDescriptor* type_field = desc->FindFieldByNumber(ANYARRAY_TYPE);
//    const FieldDescriptor* pack_field = desc->FindFieldByNumber(2);
//    const FieldDescriptor* comp_field = desc->FindFieldByNumber(3);//FindFieldByName("comp");
    const google::protobuf::FieldDescriptor* data_field = desc->FindFieldByNumber(ANYARRAY_DATA);//FindFieldByName("data");

    const google::protobuf::Reflection* reflection = message.GetReflection();

    //for now, we do not allow for packed message.
   // if (reflection->GetEnum(message, pack_field)->number() != AnyArray::RAW)
   //     throw runtime_error("Error: packets cannot be pre-compressed yet.... but soooon...");

    //FIXME for now, we assign always the same compression
    //FIXME why is it vector here while it is a struct in OFits.h ???? How can that even compile ???
    vector<uint16_t> comp_seq = _default_comp;

    if (_explicit_comp.find(name) != _explicit_comp.end())
    {
        comp_seq = _explicit_comp[name];
 //       cout << "Assigned " << name << " an explicit compression scheme" << endl;
    }
//    else
//        cout << name << " has default compression" << endl;

    _total_num_columns++;
    _columns_sizes.push_back(0);
    //figure out the size of the column
    int32 column_width = reflection->GetString(message, data_field).size();

    //replace the '.' by '_'. We cannot do that earlier as the distinction is needed between hierarchy (.) and indices (_)
    string column_name = name;
    for (auto it=column_name.begin(); it!=column_name.end(); it++)
        if ((*it) == '.' || (*it) == '#')
            *it = '_';

    //figure out the type of column to be initialized
    const google::protobuf::EnumValueDescriptor* type = reflection->GetEnum(message, type_field);
    switch (type->number())
    {
        case AnyArray::NONE:
            AddColumnByte(comp_seq, column_width, column_name);
//           cout << yellow << "WARNING: you are adding a cta array with no defined type (column=" << name << ")" << no_color << endl;
            break;
        case AnyArray::S8:
            AddColumnChar(comp_seq, column_width, column_name);
            break;
        case AnyArray::S16:
            AddColumnShort(comp_seq, column_width/2, column_name);
            break;
        case AnyArray::S32:
            AddColumnInt(comp_seq, column_width/4, column_name);
            break;
        case AnyArray::S64:
            AddColumnLong(comp_seq, column_width/8, column_name);
            break;
        case AnyArray::FLOAT:
            AddColumnFloat(comp_seq, column_width/4, column_name);
            break;
        case AnyArray::DOUBLE:
            AddColumnDouble(comp_seq, column_width/8, column_name);
            break;
        case AnyArray::BOOL:
            AddColumnBool(comp_seq, column_width, column_name);
            break;
        case AnyArray::U8:
            AddColumnSignedByte(comp_seq, column_width, column_name);
            break;
        case AnyArray::U16:
            AddColumnUnsignedShort(comp_seq, column_width/2, column_name);
            break;
        case AnyArray::U32:
            AddColumnUnsignedInt(comp_seq, column_width/4, column_name);
            break;
        case AnyArray::U64:
            AddColumnUnsignedLong(comp_seq, column_width/8, column_name);
            break;

        default:
            throw runtime_error("Unhandled type for cta array...");
//            cout << "Unhandled value..." << endl;
            break;
    };
}

/*******************************************************************************
 *  BUILD FITS COLUMNS
 *******************************************************************************/
void ProtobufZOFits::buildFitsColumns(const google::protobuf::Message& message, const string& name, const string& id)
{
    //retrieve the message descriptor
    const google::protobuf::Descriptor* desc = message.GetDescriptor();

    //In case of a AnyArray, call the dedicated function
    if (desc->name() == "AnyArray")
    {
        addAnyArrayColumn(message, name, id);
        //write the column indices to the header
        ostringstream str;
        str << "TPBID" << fTable.num_cols;
        SetStr(str.str(), id, "Protobuf ID");
        return;
    }
    //Append a . to the prefix, only if it is not null
    const string prefix_name = (name=="") ? "" : name+".";
    const string prefix_id   = (id  =="") ? "" : id  +".";

    //For all fields in this message, either instantiate the appropriate columns
    //or call this function recursively if it contains other messages.
    const google::protobuf::Reflection* refl = message.GetReflection();

    for (int32 i=0;i<desc->field_count(); i++)
    {
        const google::protobuf::FieldDescriptor* field = desc->field(i);
        //build the full name and ID of this field
        ostringstream full_id_str;
        full_id_str << prefix_id << field->number();
        const string full_id   = full_id_str.str();
        const string full_name = prefix_name + std::string{field->name()};

        //skip explicitely vetoed fields
        if (isVetoed(full_name))
            continue;

        //and also fields that were left empty
        if (field->is_repeated())
        {
            if (refl->FieldSize(message, field) == 0 && !isAllowed(full_name))
            {
                vetoField(full_name, true);
                continue;
            }
        }
        else
        {
            if (!refl->HasField(message, field) && !isAllowed(full_name))
            {
                vetoField(full_name, true);
                continue;
            }
        }

        vector<uint16_t> comp_seq = _default_comp;
        if (field->type() != google::protobuf::FieldDescriptor::TYPE_MESSAGE)
        {
            if (_explicit_comp.find(full_name) != _explicit_comp.end())
            {
                comp_seq = _explicit_comp[full_name];
            }
        }

        //let's make sure here that the compression type sparcelossyfloat is only applied to floats
        for (auto it=comp_seq.begin(); it!=comp_seq.end(); it++)
            if (*it == FITS::eCTALossyFloats)
            {
                if (field->type() != google::protobuf::FieldDescriptor::TYPE_FLOAT && field->type() != google::protobuf::FieldDescriptor::TYPE_MESSAGE)
                {
                    ostringstream str;
                    str << "You tried to apply a specific lossy-floats compression to a field of another type(" << field->name() << ") IMPOSIBRE! Aborting.";
                    throw runtime_error(str.str());
                }
                break;
            }

        //replace the '.' by '_'. We cannot do that earlier as the distinction is needed between hierarchy (.) and indices (_)
        string column_name = full_name;
        for (auto it=column_name.begin(); it!=column_name.end(); it++)
            if ((*it) == '.' || (*it) == '#')
                *it = '_';

        int32 num_items = field->is_repeated() ? refl->FieldSize(message,field) : 1;
        bool skipped_field = false;
        switch (field->type())
        {
            case google::protobuf::FieldDescriptor::TYPE_MESSAGE:
                if (field->is_repeated())
                {
                    _num_expected_child.insert(make_pair(_total_num_columns, num_items));
                }
                if (! field->is_repeated())
                    buildFitsColumns(refl->GetMessage(message, field), full_name, full_id);
                else
                    for (int32 j=0;j<num_items;j++)
                    {
                        ostringstream str_j;
                        str_j << j;
                        buildFitsColumns(refl->GetRepeatedMessage(message, field, j), full_name + "#" + str_j.str(), full_id+"."+str_j.str());
                    }
                continue;
            break;

            case google::protobuf::FieldDescriptor::TYPE_DOUBLE:
                AddColumnDouble(comp_seq, num_items, column_name);
                break;

            case google::protobuf::FieldDescriptor::TYPE_FLOAT:
                AddColumnFloat(comp_seq, num_items, column_name);
                break;

            case google::protobuf::FieldDescriptor::TYPE_INT64:
            case google::protobuf::FieldDescriptor::TYPE_SFIXED64:
            case google::protobuf::FieldDescriptor::TYPE_SINT64:
                AddColumnLong(comp_seq, num_items, column_name);
                break;

            case google::protobuf::FieldDescriptor::TYPE_UINT64:
            case google::protobuf::FieldDescriptor::TYPE_FIXED64:
                AddColumnUnsignedLong(comp_seq, num_items, column_name);
                break;

            case google::protobuf::FieldDescriptor::TYPE_INT32:
            case google::protobuf::FieldDescriptor::TYPE_SFIXED32:
            case google::protobuf::FieldDescriptor::TYPE_SINT32:
                AddColumnInt(comp_seq, num_items, column_name);
                break;

            case google::protobuf::FieldDescriptor::TYPE_UINT32:
            case google::protobuf::FieldDescriptor::TYPE_FIXED32:
                AddColumnUnsignedInt(comp_seq, num_items, column_name);
                break;

            case google::protobuf::FieldDescriptor::TYPE_BOOL:
                AddColumnBool(comp_seq, num_items, column_name);
                break;

            case google::protobuf::FieldDescriptor::TYPE_ENUM:
                AddColumnInt(comp_seq, num_items, column_name);
                break;

            case google::protobuf::FieldDescriptor::TYPE_STRING:
            case google::protobuf::FieldDescriptor::TYPE_BYTES:
                AddColumnChar(comp_seq, num_items, column_name);
                break;

            case google::protobuf::FieldDescriptor::TYPE_GROUP:
                cout << yellow << "WARNING: skipping field " << full_name << " because of unhandled type...." << no_color << endl;
                skipped_field = true;
            break;

            default:
                throw runtime_error("Unkown field type");
        }; //switch type()

        if (!skipped_field)
        {
            //write the column indices to the header
            ostringstream str;
            str << "TPBID" << fTable.num_cols;
            SetStr(str.str(), full_id, "Protobuf ID");

            _total_num_columns++;
            _columns_sizes.push_back(num_items);
        }
    }//for all fields
}


    void ProtobufZOFits::checkArrayValueSize(int32 num_bytes,
                                             int32 multiple,
                                             FITS::CompressionProcess_t ongoing_process)
    {
        if (num_bytes % multiple == 0) return;


        const char* compressionProcessesNames[] =
        {
            "kFactRaw"        ,
            "kFactSmoothing"  ,
            "kFactHuffman16"  ,
            "eCTADiff"        ,
            "eCTADoubleDiff"  ,
            "eCTASplitHiLo16" ,
            "eCTAHuffTimes4"  ,
            "eCTAZlib"        ,
            "eCTAHuffmanByRow",
            "eCTALZO"         ,
            "eCTARICE"        ,
            "eCTAHuffman8"    ,
            "eCTAHalfman16"   ,
            "eCTAHalfman8"    ,
            "eCTASplitHiLo32" ,
            "eCTALocalDiff"   ,
            "eCTA128Offset"   ,
            "eCTASameValues"  ,
            "eCTALossyFloats" ,
            "eCTASparseValues",
            "eCTAHalfDiff32",
            "eCTALossyInt16",
            "eCTALossyInt32",
            "eCTAzstd"
        };
        ostringstream str;
        str << red << "ERROR: array values' size is not a multiple of " << multiple << " bytes as expected while doing process ";
        str << compressionProcessesNames[ongoing_process];

        throw runtime_error(str.str());
    }




};//namespace IO
};//namespace ADH
