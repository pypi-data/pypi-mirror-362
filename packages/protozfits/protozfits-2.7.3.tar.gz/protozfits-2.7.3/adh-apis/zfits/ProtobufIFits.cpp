/**
 *
 * @file ProtobufIFits.cpp
 *
 * @brief Compressed FITS to protobuf reader.
 *
 * Created on: May 7, 2014
 *     Author: lyard
 */


#include "ProtobufIFits.h"

//compression stuff
#include <zlib.h>
#include "minilzo.h"
#include "ricecomp.h"
#include "zstd.h"

#include "DL0v1_Subarray.pb.h"
#include "DL0v1_Telescope.pb.h"
#include "DL0v1_Trigger.pb.h"
#include "ProtoDataModel.pb.h"
#include "ProtoR1.pb.h"
#include "R1v1.pb.h"
#include "Auxiliary.pb.h"

using namespace std;

namespace ADH
{
namespace IO
{

/*******************************************************************************
 * DEFAULT CONSTRUCTOR
 *******************************************************************************/
ProtobufIFits::ProtobufIFits(const string&     filename,
                             const string&     tablename,
                             const google::protobuf::Descriptor* descriptor) : ZIFits(filename, tablename)
{
    //Initialize zfits structures without allocating buffers memory
    InitCompressionReading(false);

    _loaded_tile = -1;
    _messages_to_recycle.clear();

    _messages_to_recycle.clear();

    //get the written message's name
    initializeMessageDesc(descriptor);

    if (lzo_init() != LZO_E_OK)
        throw runtime_error("Cannot initialize LZO");
}

/*******************************************************************************
 * DEFAULT DESTRUCTOR
 *******************************************************************************/
ProtobufIFits::~ProtobufIFits()
{
    for (auto it=_messages_to_recycle.begin(); it!= _messages_to_recycle.end(); it++)
    {
        delete *it;
    }

    for (auto it=_returned_messages.begin(); it!= _returned_messages.end(); it++)
    {
        delete *it;
    }

    for (auto it=_available_messages.begin(); it!= _available_messages.end(); it++)
    {
        if (!it->second.used)
        {
            delete it->second.message;
        }
    }
}

/*******************************************************************************
 * INITIALIZE MESSAGE DESCRIPTOR
 *******************************************************************************/
void ProtobufIFits::initializeMessageDesc(const google::protobuf::Descriptor* descriptor)
{
    string message_name = GetStr("PBFHEAD");

    if (descriptor != NULL)
        _descriptor = descriptor;
    else
    {
        // get it from the name set in the fits header
        // As the data model was renamed for the release of the official R1, we have two versions of the name possible
        if (message_name ==           "CTAMessage" ||
            message_name == "DataModel.CTAMessage")
        {
            CTAMessage message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "DL0v1.Telescope.DataStream")
        {
            DL0v1::Telescope::DataStream message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "DL0v1.Telescope.CameraConfiguration")
        {
            DL0v1::Telescope::CameraConfiguration message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "DL0v1.Telescope.DataStream")
        {
            DL0v1::Telescope::DataStream message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "DL0v1.Telescope.Event")
        {
            DL0v1::Telescope::Event message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "DL0v1.Trigger.Trigger")
        {
            DL0v1::Trigger::Trigger message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "DL0v1.Trigger.DataStream")
        {
            DL0v1::Trigger::DataStream message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "R1v1.CameraConfiguration"
                || message_name == "CTAR1.CameraConfiguration")
        {
            R1v1::CameraConfiguration message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "R1v1.TelescopeDataStream")
        {
            R1v1::TelescopeDataStream message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "R1v1.Event" || message_name == "CTAR1.Event")
        {
            R1v1::Event message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "R1.Event")
        {
            R1v1::Event message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "ProtoDataModel.ArrayEvent" ||
                 message_name ==      "DataModel.ArrayEvent")
        {
            ProtoDataModel::ArrayEvent message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "ProtoDataModel.CameraEvent" ||
                 message_name ==      "DataModel.CameraEvent")
        {
            ProtoDataModel::CameraEvent message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "ProtoDataModel.DigicamConfig" ||
                 message_name ==      "DataModel.DigicamConfig")
        {
            ProtoDataModel::DigicamConfig message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "ProtoR1.CameraEvent" ||
                 message_name ==      "R1.CameraEvent")
        {
            ProtoR1::CameraEvent message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "ProtoDataModel.CameraRunHeader" ||
                 message_name ==      "DataModel.CameraRunHeader")
        {
            ProtoDataModel::CameraRunHeader message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "DL0v1.Subarray.Event")
        {
            DL0v1::Subarray::Event message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "DL0v1.Subarray.DataStream")
        {
            DL0v1::Subarray::DataStream message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "ProtoR1.CameraConfiguration" ||
                 message_name ==      "R1.CameraConfiguration")
        {
            ProtoR1::CameraConfiguration message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "UnitTestAtomicTypes" ||
                 message_name == "DataModel.UnitTestAtomicTypes")
        {
            UnitTestAtomicTypes message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "ProtoDataModel.MCCalibration" ||
                 message_name ==      "DataModel.MCCalibration")
        {
            ProtoDataModel::MCCalibration message;
            _descriptor = message.GetDescriptor();
        }
        else if (message_name == "AUX.DummyAuxData")
        {
            AUX::DummyAuxData message;
            _descriptor = message.GetDescriptor();
        }
        else
        {
            ostringstream str;
            str << "Cannot load data of type " << message_name << ". The reason is: ProtobufIFits must be updated to handle this type of data. This is very easy to do but must unfortunatelly be done manually. Write an email to etienne and he will do it (hopefully)";
            throw runtime_error(str.str());
        }
    }

    //are we reading the expected type of message ?
    const std::string full_name{_descriptor->full_name()};

    if (message_name == "CTAR1.CameraConfiguration")
        message_name = "R1v1.CameraConfiguration";
    else if (message_name == "CTAR1.Event")
        message_name = "R1v1.Event";

    if ((full_name != message_name) && (full_name != "Proto" + message_name)) {
        ostringstream str;
        str << "The file contains messages of type " << message_name << " while you are trying to read " << full_name;
        throw runtime_error(str.str());
    }

    //let's look at the FITS columns, and see if they correspond to the message's structure
    int32 i=1;
    for (auto it=fTable.sorted_cols.cbegin(); it!=fTable.sorted_cols.cend(); it++)
    {
        ostringstream str;
        str << "TTYPE" << i;

        str.str("");
        //get the indices of the current column
        str << "TPBID" << i++;
        string column_id = GetStr(str.str());
        _columns_ids.push_back(column_id);

        google::protobuf::FieldDescriptor::Type type = google::protobuf::FieldDescriptor::MAX_TYPE;
        switch (it->type)
        {
            case 'L' : type = google::protobuf::FieldDescriptor::TYPE_BOOL;
            break;

            case 'I' :
            case 'J' : type = google::protobuf::FieldDescriptor::TYPE_INT32;
            break;

            case 'U' :
            case 'V' : type = google::protobuf::FieldDescriptor::TYPE_UINT32;
            break;

            case 'K' : type = google::protobuf::FieldDescriptor::TYPE_INT64;
            break;

            case 'W' : type = google::protobuf::FieldDescriptor::TYPE_UINT64;
            break;

            case 'E' : type = google::protobuf::FieldDescriptor::TYPE_FLOAT;
            break;

            case 'D' : type = google::protobuf::FieldDescriptor::TYPE_DOUBLE;
            break;

            case 'A' :
            case 'S' :
            case 'B' : type = google::protobuf::FieldDescriptor::TYPE_BYTES;

            break;

            default:
            {
                ostringstream str_error;
                str_error << "ERROR: unhandled FITS type: |" << it->type << "| for column " << i;
                throw runtime_error(str_error.str());
            }
        };

        bool is_array = (it->num!=1);
        if (type == google::protobuf::FieldDescriptor::TYPE_BYTES)
            is_array = false;

        if (!verifyColumnVsDescription(column_id, _descriptor, type, is_array))
        {
            cout << "This column (" << column_id << ") is not in the available message description. You are probably using an outdated version of the zfits reader..." << endl;
            _unknown_ids.push_back(column_id);
        }
    }
}


uint32 ProtobufIFits::getNumHeaderKeys(bool all_keys) const
{
    const Table::Keys& keys = GetKeys();

    if (all_keys)
        return keys.size();

    int num_keys = 0;
    for (auto it=keys.begin(); it!=keys.end(); it++)
    {
        cout << "key " << ++num_keys << ": " << it->first << " | " << it->second.value << endl;
    }
    return num_keys;
}
/*******************************************************************************
 * VERIFY COLUMNS AGAINST DESCRIPTION
 *******************************************************************************/
bool ProtobufIFits::verifyColumnVsDescription(const string&               id,
                                              const google::protobuf::Descriptor*           desc,
                                              const google::protobuf::FieldDescriptor::Type type,
                                              const bool                  isArray)
{
    //get the first ID
    size_t first_dot = id.find_first_of('.');
    string this_id = (first_dot != string::npos) ? id.substr(0,first_dot) : id;

    int32 int_id = atoi(this_id.c_str());
    //get the associated field in the message
    const google::protobuf::FieldDescriptor* field = desc->FindFieldByNumber(int_id);

    if (field == NULL)
        return false; //this field is not here. looks like we are using an outdated version of the messages description

    //if this is a message, either we hit a cta array, or we continue recursively
    if (field->type() == google::protobuf::FieldDescriptor::TYPE_MESSAGE)
    {
        if (field->message_type()->name() == "AnyArray")
            return true;

        //get the remainder of the ID string
        if (first_dot == string::npos)
            throw runtime_error("ERROR: expected a message, found a basic type");
        string remainder_id = id.substr(first_dot+1, id.length()-first_dot-1);

        if (field->is_repeated())
        {//consume the message's index from the ID
            first_dot = remainder_id.find_first_of('.');

            if (first_dot == string::npos)
                throw runtime_error("ERROR: expected a message index, found a basic type");

            remainder_id = remainder_id.substr(first_dot+1, remainder_id.length()-first_dot-1);
        }

        return verifyColumnVsDescription(remainder_id, field->message_type(), type, isArray);
    }

    if (field->type() != type)
    {//the FITS type might not be exactly the same as the protobuffer type...
        bool problem = false;
        switch (field->type())
        {
            case google::protobuf::FieldDescriptor::TYPE_STRING:
                if (type != google::protobuf::FieldDescriptor::TYPE_BYTES) problem = true;
            break;

            case google::protobuf::FieldDescriptor::TYPE_BOOL:
            case google::protobuf::FieldDescriptor::TYPE_FLOAT:
            case google::protobuf::FieldDescriptor::TYPE_BYTES:
            case google::protobuf::FieldDescriptor::TYPE_GROUP:
            case google::protobuf::FieldDescriptor::TYPE_DOUBLE:
            case google::protobuf::FieldDescriptor::TYPE_MESSAGE:
                problem = true;
            break;

            case google::protobuf::FieldDescriptor::TYPE_INT64:
            case google::protobuf::FieldDescriptor::TYPE_SINT64:
            case google::protobuf::FieldDescriptor::TYPE_SFIXED64:
                if (type != google::protobuf::FieldDescriptor::TYPE_INT64) problem = true;
            break;

            case google::protobuf::FieldDescriptor::TYPE_FIXED64:
            case google::protobuf::FieldDescriptor::TYPE_UINT64:
                if (type != google::protobuf::FieldDescriptor::TYPE_UINT64) problem = true;
            break;

            case google::protobuf::FieldDescriptor::TYPE_INT32:
            case google::protobuf::FieldDescriptor::TYPE_SINT32:
            case google::protobuf::FieldDescriptor::TYPE_SFIXED32:
            case google::protobuf::FieldDescriptor::TYPE_ENUM:
                if (type != google::protobuf::FieldDescriptor::TYPE_INT32) problem = true;
            break;

            case google::protobuf::FieldDescriptor::TYPE_FIXED32:
            case google::protobuf::FieldDescriptor::TYPE_UINT32:
                if (type != google::protobuf::FieldDescriptor::TYPE_UINT32) problem = true;
            break;

            default:
                problem = true;
        };

        if (problem)
        {
            ostringstream str;
            str << "ERROR: type mismatch. Expected " << type << " found " << field->type() << " for " << field->name();
            throw runtime_error(str.str());
        }
    }

    if (field->is_repeated() != isArray)
    {
        ostringstream str;
        str << "ERROR: Expected ";
        if (isArray)
            str << " a vector, found a scalar";
        else
            str << " a scalar, found a vector";
        throw runtime_error(str.str());
    }

    return true;
}

/*******************************************************************************
 *  READ
 *******************************************************************************/
google::protobuf::Message* ProtobufIFits::readMessage(uint32 number)
{
    if (number < 1 || number > getNumMessagesInTable())
    {
        cout << "Event number should be between 1 and " << getNumMessagesInTable() << " while you requested event " << number << endl;

        return NULL;
    }
    auto it = _available_messages.find(number-1);
    //do we have available messages ?
    if (it == _available_messages.end())
    {
        int32 size_loaded = loadTile(((number-1)/fNumRowsPerTile)+1);
        if (! size_loaded && GetBytesPerRow() == 0)
        {
            cout << ADH::ColoredOutput::red << "Only empty messages were written. Nothing to load, sorry." << endl;
            exit(-5);
        }
        it = _available_messages.find(number-1);
    }

    if (it == _available_messages.end())
        throw runtime_error("Looks like I am not loading the correct tile or something.");

    google::protobuf::Message* to_return = it->second.message;
    it->second.used = true;

    return to_return;
}

/*******************************************************************************
 * GET NUM MESSAGES IN TABLE
 *******************************************************************************/
uint32 ProtobufIFits::getNumMessagesInTable() const
{
    return fTable.Get<uint32>("ZNAXIS2");
}

/*******************************************************************************
 * GET NUM TILES IN TABLE
 *******************************************************************************/
uint32 ProtobufIFits::getNumTilesInTable() const
{
    return fNumTiles;//fTable.Get<int32>("NAXIS2");
}

/*******************************************************************************
 *  NEXT TILE SIZE
 *******************************************************************************/
int64 ProtobufIFits::tileSize(int32 tile_number)
{
    int32 num_tiles = getNumTilesInTable();
    if (num_tiles   < 1 ||
        tile_number < 1 ||
        tile_number > num_tiles )
    {
        ostringstream str;
        str << "ERROR: requested tile (" << tile_number << ") does not exist in table.";
        if (num_tiles < 1)
            str << " Actually, the table seems to be empty...";
        else
            str << " Min=1, max=" << num_tiles;
        throw runtime_error(str.str());
    }

    return fTileSize[tile_number-1] + sizeof(FITS::TileHeader);
}

/*******************************************************************************
 * READ NEXT TILE
 *******************************************************************************/
int64 ProtobufIFits::loadTile(int32 tile_number)
{
    //how many bytes should we read ?
    const int64 size_to_read = tileSize(tile_number);
    if (size_to_read == sizeof(FITS::TileHeader))
        return 0;
    const int64 tile_start   = fCatalog[tile_number-1][0].second - sizeof(FITS::TileHeader);

    _loaded_tile = tile_number-1;

    seekg(fHeapOff+tile_start);

    //TODO I should compute the checksum
    if (fCompressedBuffer.size() != uint64(size_to_read))
        fCompressedBuffer.resize(size_to_read);

    read(fCompressedBuffer.data(), size_to_read);

    //move any remaining message to the recycle pool
    for (auto it=_available_messages.begin(); it!= _available_messages.end(); it++)
    {
        if (!it->second.used)
            _messages_to_recycle.push_back(it->second.message);
    }
    _available_messages.clear();

    //move any "returned-borrowed" message to the pool to recycle
    for (auto it=_returned_messages.begin(); it!=_returned_messages.end(); it++)
    {
        _messages_to_recycle.push_back(*it);
    }

    _returned_messages.clear();

    //get messages structures to hold the decompressed data
    const uint32 num_messages = reinterpret_cast<FITS::TileHeader*>(fCompressedBuffer.data())->numRows;
    const uint32 start_index  = _loaded_tile*fNumRowsPerTile;

    for (uint32 i=0; i<num_messages; i++)
    {
        if (_messages_to_recycle.empty())
        {//nothing to be recycled ? Get a new instance !
            _available_messages[start_index+i] = UsableMessage(google::protobuf::MessageFactory::generated_factory()->GetPrototype(_descriptor)->New());
        }
        else
        {//recycle already allocated messages
            _available_messages[start_index+i] = UsableMessage(_messages_to_recycle.front());
            _messages_to_recycle.pop_front();
        }
    }

    //get a decompression buffer that is large enough to host a decompressed block
    const uint32 tile_max_size = GetBytesPerRow()*fNumRowsPerTile;
    if (fBuffer.size() < tile_max_size)
        fBuffer.resize(tile_max_size);

    const char* compressed_data = fCompressedBuffer.data() + sizeof(FITS::TileHeader);
    //decompress the blocks one by one, and fill in the messages structures
    int32 i=0;
    for (auto it=fTable.sorted_cols.cbegin(); it!=fTable.sorted_cols.cend(); it++)
    {
        //get compression parameters
        const FITS::BlockHeader* head = reinterpret_cast<const FITS::BlockHeader*>(compressed_data);

        //move to the compressed binary
        uint32 this_head_size = sizeof(FITS::BlockHeader) + head->numProcs*sizeof(uint16);
        compressed_data += this_head_size;

        //if there is no data stored, move past this block
        if (head->size == this_head_size)
        {
            cout << "No data was written to this block" << endl;
            continue;
        }
        int32 this_compressed_size = head->size - this_head_size;
        uint32 uncompressed_size   = 0;
try
{
        //decompress to temporary buffer
        for (int32 j=(int32)(head->numProcs-1); j>=0; j--)
        {
            switch (head->processings[j])
            {
                case FITS::eCTAZlib:
                    uncompressed_size = zlibDecompress(fBuffer.data(), compressed_data, this_compressed_size);
                    break;
                case FITS::eCTAzstd:
                    uncompressed_size = ZSTD_decompress(fBuffer.data(), fBuffer.size(), compressed_data, this_compressed_size);
                    if (ZSTD_isError(uncompressed_size))
                        throw runtime_error("Something wrong happenned while decompressing ZSTD data");
                    break;
                case FITS::eCTALZO:
                    uncompressed_size = lzoDecompress(fBuffer.data(), compressed_data, this_compressed_size);
                    break;

                case FITS::eCTARICE:
                    uncompressed_size = riceDecompress(fBuffer.data(), compressed_data, this_compressed_size);
                    break;

                case FITS::eCTASplitHiLo16:
                    mergeHiLo16(fBuffer.data(), uncompressed_size);
                    break;
                case FITS::eCTASplitHiLo32:
                    mergeHiLo32(fBuffer.data(), uncompressed_size);
                    break;
                case FITS::eCTA128Offset:
                {
                    int16* values = reinterpret_cast<int16*>(fBuffer.data());
                    for (uint32 i=0;i<uncompressed_size/2;i++)
                        values[i] -= 128;
                }
                break;
                case FITS::kFactRaw:
                    memcpy(fBuffer.data(), compressed_data, this_compressed_size);
                    uncompressed_size = this_compressed_size;
                    break;
                case FITS::kFactSmoothing:
                    UnApplySMOOTHING(reinterpret_cast<int16*>(fBuffer.data()), uncompressed_size/2);
                    break;
                case FITS::eCTADiff:
                {
                    int16* dest16 = reinterpret_cast<int16*>(fBuffer.data());
                    for (uint32 i=1;i<uncompressed_size/2;i++)
                        dest16[i] += dest16[i-1];
                }
                break;
                case FITS::eCTADoubleDiff:
                {
                    int16* dest16 = reinterpret_cast<int16*>(fBuffer.data());
                    for (uint32 i=1;i<uncompressed_size/2;i++)
                        dest16[i] += dest16[i-1];
                    for (uint32 i=1;i<uncompressed_size/2;i++)
                        dest16[i] += dest16[i-1];
                }
                break;
                case FITS::kFactHuffman16:
                {
                    vector<uint16> uncompressed;
                    Huffman::Decode(&reinterpret_cast<const unsigned char*>(compressed_data)[sizeof(uint32)], reinterpret_cast<const uint32*>(compressed_data)[0], uncompressed);
                    memcpy(fBuffer.data(), uncompressed.data(), uncompressed.size()*sizeof(uint16));
                    uncompressed_size = uncompressed.size()*sizeof(uint16);
                }
                break;
                case FITS::eCTAHalfman16:
                {
                    vector<uint16> uncompressed;
                    const unsigned char* usrc = reinterpret_cast<const unsigned char*>(compressed_data + 2*sizeof(uint32));
                    const uint32*        src_sizes = reinterpret_cast<const uint32*>(compressed_data);
                    Huffman::Decode(usrc, src_sizes[0], uncompressed);
                    const uint32 raw_size = uncompressed.size()*sizeof(uint16);
                    memcpy(fBuffer.data(), uncompressed.data(),raw_size);
                    Huffman::Decode(usrc+src_sizes[0], src_sizes[1], uncompressed);
                    memcpy(fBuffer.data()+raw_size, uncompressed.data(), uncompressed.size()*sizeof(uint16));
                    uncompressed_size = uncompressed.size()*sizeof(uint16) + raw_size;
                }
                break;

                case FITS::eCTASameValues:
                {
                    //read the input data as uint32
                    uint32* src32 = reinterpret_cast<uint32*>(fBuffer.data());
                    //read how many bunches were stored
                    uint32 num_bunches = *src32++;

//                    cout << "Reading " << num_bunches << " pairs (" << uncompressed_size << ")Bytes" << endl;
                    //check that the correct size was decompressed
                    if ((num_bunches*2 + 1)*sizeof(uint32) != uncompressed_size)
                    {
                        ostringstream str;
                        str << "Wrong sizes in same values algo: " << num_bunches << " " << (num_bunches*2+1)*sizeof(uint32) << " " << uncompressed_size;
                        throw runtime_error(str.str());
                    }

                    //take one intermediate buffer
                    uint32* inter32 = new uint32[fBuffer.size()/sizeof(uint32)];
                    uint32 target_index = 0;

                    //crawl all bunches and restore their data
                    for (uint32 i=0;i<num_bunches;i++)
                    {
                        uint32 num_values = src32[i*2];
                        uint32 value = src32[i*2 + 1];

                        //TODO use a memset for this instead
                        for (uint32 j=0;j<num_values;j++)
                            inter32[target_index++] = value;
                    }

                    uncompressed_size = target_index*sizeof(uint32);
//                    cout << "Uncompressed size is: " << uncompressed_size << endl;
                    //move the restored data back into fBuffer
                    memcpy(fBuffer.data(), inter32, uncompressed_size);

                    delete[] inter32;

                }
                break;

                case FITS::eCTASparseValues:
                {
                    //read the input data as int32
                    int32* src32 = reinterpret_cast<int32*>(fBuffer.data());
                    //get header data
                    int32 sparse_value = src32[0];
                    uint32 num_values  = reinterpret_cast<uint32*>(src32)[1];

                    //skip header
                    src32 += 2;

                    //restore values
                    if ((num_values + 2)*sizeof(uint32) != uncompressed_size)
                    {
                        ostringstream str;
                        str << "Wrong sizes in same values aglo: " << num_values << " " << uncompressed_size;
                        throw runtime_error(str.str());
                    }

                    //take one intermediate buffer
                    int32* inter32 = new int32[fBuffer.size()/sizeof(int32)];
                    uint32 target_index = 0;

                    for (uint32 i=0;i<num_values;)
                    {
                        //restore default values
                        for (int32 j=0;j<src32[i];j++)
                            inter32[target_index++] = sparse_value;

                        if (++i >= num_values) break;

                        inter32[target_index++] = src32[i++];
                    }

                    uncompressed_size = target_index*sizeof(int32);

                    memcpy(fBuffer.data(), inter32, uncompressed_size);

                    delete[] inter32;
                }
                break;

                case FITS::eCTALossyFloats:
                {
                    float* f_dst = reinterpret_cast<float*>(fBuffer.data());
                    int32* i_src = reinterpret_cast<int32*>(fBuffer.data());

                    float precision = 0.01f;

                    uint32 num_restored_bytes = 0;
                    while (num_restored_bytes < uncompressed_size)
                    {
                        uint32 this_num_values = *i_src / sizeof(float);
                        i_src++;
                        f_dst++;

                        for (uint32 i=0;i<this_num_values;i++)
                            *f_dst++ = (float)(*i_src++) * precision;

                        num_restored_bytes += (this_num_values+1)*sizeof(float);
                    }
                }
                break;

                case FITS::eCTALossyInt16:
                case FITS::eCTALossyInt32:
                break;
//                case FITS::eCTAHuffman8:
//                {
//                    vector<uint8> uncompressed;
//                    Huffman::Decode(&reinterpret_cast<const unsigned char*>(compressed_data)[sizeof(uint32)], reinterpret_cast<const uint32*>(compressed_data)[0], uncompressed);
//                    memcpy(fBuffer.data(), uncompressed.data(), uncompressed.size()*sizeof(uint32));
//                    uncompressed_size = uncompressed.size()*sizeof(uint32);
//                }
//                break;
//                case FITS::eCTAHalfman8:
//                {
//                    vector<uint8> uncompressed;
//                    const unsigned char* usrc = reinterpret_cast<const unsigned char*>(compressed_data + 2*sizeof(uint32));
//                    const uint32*        src_sizes = reinterpret_cast<const uint32*>(compressed_data);
//                    Huffman::Decode(usrc, src_sizes[0], uncompressed);
//                    const uint32 raw_size = uncompressed.size()*sizeof(uint8);
//                    memcpy(fBuffer.data(), uncompressed.data(),raw_size);
//                    Huffman::Decode(usrc+src_sizes[0], src_sizes[1], uncompressed);
//                    memcpy(fBuffer.data()+raw_size, uncompressed.data(), uncompressed.size()*sizeof(uint8));
//                    uncompressed_size = uncompressed.size()*sizeof(uint8) + raw_size;
//                }
//                break;

                default:
                {
                    ostringstream str;
                    str << endl;
                    str << "Unhandled compression processing: " << head->processings[j] << endl;
                    str << "Heap offset=" << fHeapOff << endl;
                    for (int32 i=0;i<tile_number;i++)
                    str << " Tile start = " << fCatalog[i][0].second << endl;
                    throw runtime_error(str.str());
                }
            }; //switch proc
        } //for all proc
} catch (runtime_error& e)
{
                    cout << e.what() << endl;
                    ostringstream str;
                    str << "Heap offset=" << fHeapOff << endl;
                    for (uint32 i=0;i<fNumTiles;i++)
                    str << " Tile start = " << fCatalog[i][0].second << endl;
                    throw runtime_error(str.str());
}
        //move past this compressed block
        compressed_data += this_compressed_size;

        //fill in the decompressed data to the messages structure
        populateMessageField(i);

        i++;
    }//for all columns

    //TODO post processing: trim messages that only contain default information

    return size_to_read;
}

/*******************************************************************************
 *  GET LOADED TILE
 *******************************************************************************/
const char* ProtobufIFits::getLoadedTile()
{
    if (_loaded_tile < 0)
        return NULL;

    return fCompressedBuffer.data();
}


/*******************************************************************************
 * LZO DECOMPRESS
 *******************************************************************************/
uint64_t ProtobufIFits::riceDecompress(      char*       dest,
                                       const char* const src,
                                             uint32      num_bytes)
{
    int32 out_len;
    memcpy(&out_len, src, sizeof(int32));

    fits_rdecomp_short((unsigned char*)(src+sizeof(int32)), num_bytes-sizeof(int32), (unsigned short*)(dest), out_len/2, 1);

    return out_len;
}

/*******************************************************************************
 * LZO DECOMPRESS
 *******************************************************************************/
uint64_t ProtobufIFits::lzoDecompress(      char*       dest,
                                      const char* const src,
                                            uint32      num_bytes)
{
    lzo_uint out_len = GetBytesPerRow()*fNumRowsPerTile;
    lzo_uint in_len  = num_bytes;

    if (lzo1x_decompress((const unsigned char*)(src), in_len, (unsigned char*)(dest), &out_len, NULL) != LZO_E_OK)
        throw runtime_error("Could not decompress LZO");

    return out_len;
}

/*******************************************************************************
 * ZLIB DECOMPRESS
 *  FIXME zlib uses uLongf, which on some architectures (AIX and probably windows) is 32 bits instead of 64 -> add a run-time check
 *******************************************************************************/
uint64_t ProtobufIFits::zlibDecompress(const char*       dest,
                                       const char* const src,
                                             uint32      num_bytes)
{
    uint64_t uncompressed_size = GetBytesPerRow()*fNumRowsPerTile;

    if (uncompress((Bytef*)(dest), (uLongf*)(&uncompressed_size), (const Bytef*)(src), num_bytes) != Z_OK)
    {
        ostringstream str;
        str << "zlibDecompress did not work... " << num_bytes << " " << uncompressed_size;
        throw runtime_error(str.str());
    }
    return uncompressed_size;
}

/*******************************************************************************
 * MERGE HIGH / LOW - 16 BITS
 *******************************************************************************/
void ProtobufIFits::mergeHiLo16(char*  buffer,
                                uint32 num_bytes)
{
    if (num_bytes%2 != 0)
        throw runtime_error("Number of bytes not multiple of 2");

    vector<char> full_words_store(num_bytes);
    char* full_words = full_words_store.data();
    char* input      = buffer;

    for (uint32 k=0;k<num_bytes;k+=2)
        full_words[k] = *input++;

    for (uint32 k=1;k<num_bytes;k+=2)
        full_words[k] = *input++;

    memcpy(buffer, full_words_store.data(), num_bytes);
}

void ProtobufIFits::mergeHiLo32(char*  buffer,
                                uint32 num_bytes)
{
    if (num_bytes%4 != 0)
        throw runtime_error("Number of bytes not multiple of 4");

    vector<char> full_words_store(num_bytes);
    char* full_words = full_words_store.data();
    char* input      = buffer;

    for (uint32 k=0;k<num_bytes;k+=4)
    {
        full_words[k]   = *input++;
        full_words[k+1] = *input++;
    }
    for (uint32 k=2;k<num_bytes;k+=4)
    {
        full_words[k]   = *input++;
        full_words[k+1] = *input++;
    }
    memcpy(buffer, full_words_store.data(), num_bytes);
}

/*******************************************************************************
 * POPULATE MESSAGE FIELD
 *******************************************************************************/
void ProtobufIFits::populateMessageField(int32 index)
{
    //get the ID for this field
    //TODO make the IDs perform faster
    string id = _columns_ids[index];

    for (auto it=_unknown_ids.begin(); it!=_unknown_ids.end(); it++)
        if (*it == id)
            return;

    //get / create target fields
    vector<google::protobuf::Message*> target_fields;

    for (auto it=_available_messages.begin(); it!=_available_messages.end(); it++)
        target_fields.push_back(it->second.message);

    //get the correct target field.
    size_t first_dot = id.find_first_of('.');

    while (first_dot != string::npos)
    {
        //get the current index and skip it in the id string
        int32 int_id = atoi(id.substr(0,first_dot).c_str());
              id     = id.substr(first_dot+1, id.length()-first_dot-1);

        const google::protobuf::Descriptor* desc = target_fields[0]->GetDescriptor();

        if (desc->FindFieldByNumber(int_id)->is_repeated())
        {
            //consume the current index of the message array
                  first_dot     = id.find_first_of('.');

            //in the case of repeated ctaArrays (very unlikely, but still), there are no more first_dots to be found
            int32 message_index = (first_dot == string::npos) ? atoi(id.c_str()) : atoi(id.substr(0, first_dot).c_str());
                  id            = (first_dot == string::npos) ? ""               : id.substr(first_dot+1, id.length()-first_dot-1);

            //create the corresponding array entry if not already there
            if (target_fields[0]->GetReflection()->FieldSize(target_fields[0][0], desc->FindFieldByNumber(int_id)) < message_index+1)
                for (auto it=target_fields.begin(); it!=target_fields.end(); it++)
                    (*it)->GetReflection()->AddMessage(*it, desc->FindFieldByNumber(int_id));

            //and replace the target with the newly created message
            for (auto it=target_fields.begin(); it!=target_fields.end(); it++)
                (*it) = (*it)->GetReflection()->MutableRepeatedMessage(*it, desc->FindFieldByNumber(int_id), message_index);
        }
        else
        {
            //only replace the targets with the current message field
            for (auto it=target_fields.begin(); it!=target_fields.end(); it++)
                (*it) = (*it)->GetReflection()->MutableMessage(*it, desc->FindFieldByNumber(int_id));
        }

        //skip past the current dot
        first_dot = id.find_first_of('.');
    }

    //Now in the targets, there is the final message before the requested field.
    //populate the requested field with the data from the uncompressed buffer
          int32       int_id = atoi(id.c_str());
    const google::protobuf::Descriptor* desc   = target_fields[0]->GetDescriptor();
    const google::protobuf::Reflection* reflec = target_fields[0]->GetReflection();

    char* input_data = fBuffer.data();

    switch(desc->FindFieldByNumber(int_id)->type())
    {
        case google::protobuf::FieldDescriptor::TYPE_DOUBLE:
            deserialize<double>(input_data, target_fields, desc->FindFieldByNumber(int_id), reflec);
            break;

        case google::protobuf::FieldDescriptor::TYPE_BOOL:
            deserialize<bool>(input_data, target_fields, desc->FindFieldByNumber(int_id), reflec);
            break;

        case google::protobuf::FieldDescriptor::TYPE_FLOAT:
            deserialize<float>(input_data, target_fields, desc->FindFieldByNumber(int_id), reflec);
            break;

        case google::protobuf::FieldDescriptor::TYPE_MESSAGE:
        {
            const google::protobuf::FieldDescriptor* field = desc->FindFieldByNumber(int_id);
            //in the case of cta arrays, the field is the message that we want to de serialize -> move it to the messages structures
            //if the field is repeated, the move was already be done earlier
            if (!field->is_repeated())
            {
                for (auto it=target_fields.begin(); it!=target_fields.end(); it++)
                    (*it) = reflec->MutableMessage(*it, field);
            }

            deserializeAnyArray(input_data, target_fields, field, reflec, index);
            break;
        }

        case google::protobuf::FieldDescriptor::TYPE_UINT64:
        case google::protobuf::FieldDescriptor::TYPE_FIXED64:
            deserialize<uint64>(input_data, target_fields, desc->FindFieldByNumber(int_id), reflec);
            break;

        case google::protobuf::FieldDescriptor::TYPE_INT64:
        case google::protobuf::FieldDescriptor::TYPE_SINT64:
        case google::protobuf::FieldDescriptor::TYPE_SFIXED64:
            deserialize<int64>(input_data, target_fields, desc->FindFieldByNumber(int_id), reflec);
        break;

        case google::protobuf::FieldDescriptor::TYPE_UINT32:
        case google::protobuf::FieldDescriptor::TYPE_FIXED32:
            deserialize<uint32>(input_data, target_fields, desc->FindFieldByNumber(int_id), reflec);
        break;

        case google::protobuf::FieldDescriptor::TYPE_INT32:
        case google::protobuf::FieldDescriptor::TYPE_SINT32:
        case google::protobuf::FieldDescriptor::TYPE_SFIXED32:
            deserialize<int32>(input_data, target_fields, desc->FindFieldByNumber(int_id), reflec);
        break;

        case google::protobuf::FieldDescriptor::TYPE_ENUM:
            deserialize<google::protobuf::EnumValueDescriptor>(input_data, target_fields, desc->FindFieldByNumber(int_id), reflec);
        break;

        case google::protobuf::FieldDescriptor::TYPE_STRING:
        case google::protobuf::FieldDescriptor::TYPE_BYTES:
            deserialize_chars(input_data, target_fields, desc->FindFieldByNumber(int_id), reflec);
        break;
        case google::protobuf::FieldDescriptor::TYPE_GROUP:
        default:
            throw runtime_error("ERROR: unhandled type while populating message fields");
    };
}

/*******************************************************************************
 * DE-SERIALIZE - ANY ARRAY SPECIALIZATION
 *******************************************************************************/
uint32 ProtobufIFits::deserializeAnyArray(char*                   src,
                                          const vector<google::protobuf::Message*>& messages,
                                          const google::protobuf::FieldDescriptor*  field,
                                          const google::protobuf::Reflection*       ,
                                          const int32             column_index)
{
    char* orig_src = src;

    const google::protobuf::Descriptor* desc = field->message_type();

    if (desc->name() != "AnyArray")
    {
        ostringstream str;
        str << "ERROR: Expected cta array, got " << desc->name();
        throw runtime_error(str.str());
        //FIXME after debug is complete, remove this useless check
    }

    for (auto it=messages.begin(); it!=messages.end(); it++)
    {
        AnyArray* array_message = dynamic_cast<AnyArray*>(*it);

        //get the number of bytes written for this message
        int32 num_bytes = reinterpret_cast<int32*>(src)[0];
        src += sizeof(int32);

        if (num_bytes < 0)
        {//the message was packed already
            //array_message->set_packed(true);

            num_bytes = -num_bytes;
            //FIXME I should write the pack method somewhere after the number of bytes
            //FIXME nope, this should be retrieved from the header.
            //FIXME Take care of the removal of the packed flag
        }

        array_message->clear_data();
        array_message->set_data(src, num_bytes);

 //       cout << "Dealing with anyarray of type " << fTable.sorted_cols[column_index].type << endl;

        switch (fTable.sorted_cols[column_index].type)
        {
            case 'I':
                array_message->set_type(AnyArray::S16);
                break;
            case 'U':
                array_message->set_type(AnyArray::U16);
                break;
            case 'J':
                array_message->set_type(AnyArray::S32);
                break;
            case 'V':
                array_message->set_type(AnyArray::U32);
                break;
            case 'K':
                array_message->set_type(AnyArray::S64);
                break;
            case 'W':
                array_message->set_type(AnyArray::U64);
                break;
            case 'E':
                array_message->set_type(AnyArray::FLOAT);
                break;
            case 'D':
                array_message->set_type(AnyArray::DOUBLE);
                break;
            case 'L':
                array_message->set_type(AnyArray::BOOL);
                break;
            case 'B':
                array_message->set_type(AnyArray::U8);
                break;
            case 'A':
                array_message->set_type(AnyArray::S8);
                break;
            case 'S':
                array_message->set_type(AnyArray::NONE);
                break;

            default:
                array_message->set_type(AnyArray::NONE);
                cout << "Warning: column type for column " << column_index << " could not be figured out" <<endl;
                break;

        }

        src += num_bytes;
    }

    return src - orig_src;
}


/*******************************************************************************
 * DE-SERIALIZE - ANY ARRAY SPECIALIZATION
 *******************************************************************************/
uint32 ProtobufIFits::deserialize_chars(char*                                          src,
                                        const std::vector<google::protobuf::Message*>& messages,
                                        const google::protobuf::FieldDescriptor*       field,
                                        const google::protobuf::Reflection*            reflec)
{
    char* orig_src = src;
    if (field->is_repeated())
    {
        throw runtime_error("You should have been prevented by the writer from doing this, i.e. use repeated strings / bytes fields");
    }
    else
    {
        for (auto it=messages.begin(); it!= messages.end(); it++)
        {
            //get the number of bytes written for this string
            int32 num_bytes = reinterpret_cast<int32*>(src)[0];
            src += sizeof(int32);

            //quite very inefficient...
            string temp_string;
            temp_string.resize(num_bytes);
            memcpy(&temp_string[0], src, num_bytes);
            reflec->SetString(*it, field, temp_string);

            src += num_bytes;
        }
    }
    return (uint32)(src - orig_src);
}

template<>
uint32 ProtobufIFits::deserialize<google::protobuf::EnumValueDescriptor>(char*                        src,
                                                       const std::vector<google::protobuf::Message*>& messages,
                                                       const google::protobuf::FieldDescriptor*       field,
                                                       const google::protobuf::Reflection*            reflec)
{
    char* orig_src = src;
    //get the ENUM descriptor
    const google::protobuf::EnumDescriptor* enum_desc = field->enum_type();
    if (field->is_repeated())
    {
        for (auto it=messages.begin(); it!= messages.end(); it++)
        {
            uint32 num_items = reinterpret_cast<uint32*>(src)[0];
            src += sizeof(uint32);
            int32* t_data = reinterpret_cast<int32*>(src);
            for (uint32 i=0;i<num_items;i++)
                reflec->AddEnum(*it, field, enum_desc->FindValueByNumber(t_data[i]));
            src = reinterpret_cast<char*>(t_data + num_items);
        }
    }
    else
    {
        int32* t_data = reinterpret_cast<int32*>(src);
        for (auto it=messages.begin(); it!= messages.end(); it++)
        {
            reflec->SetEnum(*it, field, enum_desc->FindValueByNumber(t_data[0]));
            t_data++;
        }
        src = reinterpret_cast<char*>(t_data);
    }
    return src - orig_src;

}

/*******************************************************************************
 * SET PROTOBUF VALUE UNSIGNED INT 32
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufValue<uint32>(      google::protobuf::Message*         message,
                                             const google::protobuf::FieldDescriptor* field,
                                             const google::protobuf::Reflection*      reflec,
                                                   uint32           value)
{
    reflec->SetUInt32(message, field, value);
}

/*******************************************************************************
 * SET PROTOBUF VALUE SIGNED INT 32
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufValue<int32> (      google::protobuf::Message*         message,
                                             const google::protobuf::FieldDescriptor* field,
                                             const google::protobuf::Reflection*      reflec,
                                                   int32            value)
{
    reflec->SetInt32(message, field, value);
}

/*******************************************************************************
 * SET PROTOBUF VALUE UNSIGNED INT 64
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufValue<uint64>(      google::protobuf::Message*         message,
                                             const google::protobuf::FieldDescriptor* field,
                                             const google::protobuf::Reflection*      reflec,
                                                   uint64           value)
{
    reflec->SetUInt64(message, field, value);
}

/*******************************************************************************
 * SET PROTOBUF VALUE SIGNED INT 64
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufValue<int64> (      google::protobuf::Message*         message,
                                             const google::protobuf::FieldDescriptor* field,
                                             const google::protobuf::Reflection*      reflec,
                                                   int64            value)
{
    reflec->SetInt64(message, field, value);
}

/*******************************************************************************
 * SET PROTOBUF VALUE DOUBLE
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufValue<double>(      google::protobuf::Message*         message,
                                             const google::protobuf::FieldDescriptor* field,
                                             const google::protobuf::Reflection*      reflec,
                                                   double           value)
{
    reflec->SetDouble(message, field, value);
}

/*******************************************************************************
 * SET PROTOBUF VALUE FLOAT
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufValue<float> (      google::protobuf::Message*         message,
                                             const google::protobuf::FieldDescriptor* field,
                                             const google::protobuf::Reflection*      reflec,
                                                   float            value)
{
    reflec->SetFloat(message, field, value);
}

/*******************************************************************************
 * SET PROTOBUF VALUE BOOL
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufValue<bool>  (      google::protobuf::Message*         message,
                                             const google::protobuf::FieldDescriptor* field,
                                             const google::protobuf::Reflection*      reflec,
                                                   bool             value)
{
    reflec->SetBool(message, field, value);
}

/*******************************************************************************
 * SET PROTOBUF REPEATED VALUE UNSIGNED INT 32
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufRepeatedValue<uint32>(      google::protobuf::Message*         message,
                                                     const google::protobuf::FieldDescriptor* field,
                                                     const google::protobuf::Reflection*      reflec,
                                                     const uint32*          values,
                                                           uint32           num_values)
{
    for (uint32 i=0;i<num_values;i++)
        reflec->AddUInt32(message, field, values[i]);
}

/*******************************************************************************
 * SET PROTOBUF REPEATED VALUE SIGNED INT 32
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufRepeatedValue<int32> (      google::protobuf::Message*         message,
                                                     const google::protobuf::FieldDescriptor* field,
                                                     const google::protobuf::Reflection*      reflec,
                                                     const int32*           values,
                                                           uint32           num_values)
{
    for (uint32 i=0;i<num_values;i++)
        reflec->AddInt32(message, field, values[i]);
}

/*******************************************************************************
 * SET PROTOBUF REPEATED VALUE UNSIGNED INT 64
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufRepeatedValue<uint64>(      google::protobuf::Message*         message,
                                                     const google::protobuf::FieldDescriptor* field,
                                                     const google::protobuf::Reflection*      reflec,
                                                     const uint64*          values,
                                                           uint32           num_values)
{
    for (uint32 i=0;i<num_values;i++)
        reflec->AddUInt64(message, field, values[i]);
}

/*******************************************************************************
 * SET PROTOBUF REPEATED VALUE SIGNED INT 64
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufRepeatedValue<int64> (      google::protobuf::Message*         message,
                                                     const google::protobuf::FieldDescriptor* field,
                                                     const google::protobuf::Reflection*      reflec,
                                                     const int64*           values,
                                                           uint32           num_values)
{
    for (uint32 i=0;i<num_values;i++)
        reflec->AddInt64(message, field, values[i]);
}

/*******************************************************************************
 * SET PROTOBUF REPEATED VALUE DOUBLE
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufRepeatedValue<double>(      google::protobuf::Message*         message,
                                                     const google::protobuf::FieldDescriptor* field,
                                                     const google::protobuf::Reflection*      reflec,
                                                     const double*          values,
                                                           uint32           num_values)
{
    for (uint32 i=0;i<num_values;i++)
        reflec->AddDouble(message, field, values[i]);
}

/*******************************************************************************
 * SET PROTOBUF REPEATED VALUE FLOAT
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufRepeatedValue<float>(      google::protobuf::Message*         message,
                                                    const google::protobuf::FieldDescriptor* field,
                                                    const google::protobuf::Reflection*      reflec,
                                                    const float*           values,
                                                          uint32           num_values)
{
    for (uint32 i=0;i<num_values;i++)
        reflec->AddFloat(message, field, values[i]);
}

/*******************************************************************************
 * SET PROTOBUF REPEATED VALUE BOOL
 *******************************************************************************/
template <>
void ProtobufIFits::setProtobufRepeatedValue<bool>(      google::protobuf::Message*         message,
                                                   const google::protobuf::FieldDescriptor* field,
                                                   const google::protobuf::Reflection*      reflec,
                                                   const bool*            values,
                                                         uint32           num_values)
{
    for (uint32 i=0;i<num_values;i++)
        reflec->AddBool(message, field, values[i]);
}

};//namespace IO
}; //namespace ADH
