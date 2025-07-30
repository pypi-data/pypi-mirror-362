/**
 *
 * @file ProtobufIFits.h
 *
 * @brief Compressed FITS to protobuf reader.
 *
 * protobufifits.h
 *
 *  Created on: May 7, 2014
 *      Author: lyard
 *
 *      This is the Compressed Fits Binary Table to Protocol_buffers reading class
 *      TODO: The read structures should be trimmed if they are equal to their default value
 */

#ifndef PROTOBUFIFITS_H_
#define PROTOBUFIFITS_H_

#include "ZIFits.h"
#include "BasicDefs.h"
#include <stdexcept>
#include <typeinfo>

#include <list>

namespace ADH
{
namespace IO
{

/**
 *      @class ProtobufIFits
 *      @brief Low-level compressed FITS reader for protobuf messages, probably also works on plain FITS.
 *
 *      The class retrieves the message type from the FITS header, and populates the message
 *      fields from the FITS columns. The reader is backward compatible, ie. if some fields are
 *      missing from the fits columns, then they are simply not initialized. It is not yet forward
 *      compatible, i.e. if some fields are present in the columns but not in the reading message,
 *      an error is raised. Implementing the handling of missing field would be doable if needed by
 *      the project.
 *
 *      The readout messages are allocated by the reader, and can be either deleted by the user, or
 *      recycled so that the memory is reused.
 */
class ProtobufIFits : public ZIFits
{
    public:

        //! @brief default constructor.
        //! @param filename the input file to open
        //! @param tablename request a specific table instead of the first binary table available
        //! @param descriptor explicitely specify the type of message to read. Useful in case the reader was not compiled with the message definition. Otherwise, the type is retrieved from the table header
        ProtobufIFits(const std::string& filename,
                      const std::string& tablename="",
                      const google::protobuf::Descriptor* descriptor=NULL);

        //FIXME the waiting message should be deleted by the destructor...
        virtual ~ProtobufIFits();

        //! @brief get the total number of messages stored in this table
        uint32 getNumMessagesInTable() const;

        //! @brief get the total number of tiles stored in the current table
        uint32 getNumTilesInTable() const;


        uint32 getNumHeaderKeys(bool all_keys = false) const;

        //! @brief load a tile from the disk
        //! @param the index of the tile to load, starting from 1
        //! @return the number of bytes loaded from disk
        int64 loadTile(int32 tile_number);

        //! @brief retrieve a pointer to the currently loaded tile.
        //! @return a pointer to the currently loaded tile. If no tile is loaded, return NULL
        const char* getLoadedTile();

        //! @brief retrieve the size of a given tile
        //! @param tile_number the number (starting from 1) of the tile to look for
        //! @return the size in bytes of this compressed tile
        int64 tileSize(int32 tile_number);

        //! @brief Read a message from the current table
        //!        These messages should be returned via returnBorrowedMessage
        //! @param index the message index, starting at 1. WARNING: This is the index of the message in the file: in no way the event number
        //! @return the required message, NULL if there is no such message in the file
        google::protobuf::Message* readMessage(uint32 number);

        //! @brief Read a message, serialize it and return the string
        //! @param number: the message index, starting at 1.
        //!        WARNING: This is the index of the message in the file: in no way the event number
        //! @return the required message, NULL if there is no such message in the file
        std::string readSerializedMessage(uint32 number){
            std::string exchange_string;

            //get next message, C++ style
            google::protobuf::Message* message = readMessage(number);
            if (message == NULL){ return std::string(""); }

            //serialize it to string
            message->SerializeToString(&exchange_string);

            returnBorrowedMessage(message);

            return exchange_string;
        }

        //! @brief Borrow typed message from the current table.
        //!        Borrowed messages should be returned via returnBorrowedMessage
        //! @param index the message index, starting at 1.
        //! @return the required message, NULL if no such message exist
        template <typename _T>
        const _T* borrowTypedMessage(int32 number)
        {
            google::protobuf::Message* message = readMessage(number);
            _returned_messages.erase(message);
            return dynamic_cast<const _T*>(message);
        }

        //! @brief Give a borrowed message back so that the memory can be reused
        //!        this should only be used after using the borrowTypedMessage method
        void returnBorrowedMessage(const google::protobuf::Message* message)
        {
            _returned_messages.insert(const_cast<google::protobuf::Message*>(message));
        }

        //! @brief
        template <typename _T>
        _T* readTypedMessage(int32 number)
        {
            const _T* pool_message = borrowTypedMessage<_T>(number);
            if (pool_message == nullptr) {
                std::string msg = "Wrong type of Message for table " + GetTable().name;
                throw std::runtime_error(msg);
            }

            // create a copy, so user owns data
            _T* to_return = NULL;
            if (_messages_to_recycle.empty())
                to_return = new _T;
            else
            {
                to_return = reinterpret_cast<_T*>(_messages_to_recycle.front());
                _messages_to_recycle.pop_front();
            }

            to_return->CopyFrom(*pool_message);
            returnBorrowedMessage(pool_message);

            return to_return;
        }

        //! @brief recycle a message's memory
        //! @param message the message that will be recycled
        void recycleMessage(google::protobuf::Message* message)
        {
            //we const-cast them as the recycled message can now be modified
            _messages_to_recycle.push_back(message);
        }

    private:

        //Messages type related members
        const google::protobuf::Descriptor* _descriptor;  ///<descriptor of the message's type stored in the file
        std::vector<std::string>            _columns_ids; ///<the list of fields IDs associated with the columns
        std::vector<std::string>            _unknown_ids; ///<IDs in the ZFITS file unknown by the current data model

        struct UsableMessage
        {
            UsableMessage(google::protobuf::Message* mess=NULL) { message = mess; used = false;}
            google::protobuf::Message* message;
            bool used;
        };
        //Loaded data related members
        int32                                       _loaded_tile;         ///<which one is the current tile loaded into memory ?
        std::map<int32, UsableMessage>              _available_messages;  ///<a map of messages ready to be given to the user. The key is the message index
        std::set<google::protobuf::Message*>        _returned_messages;


        std::list<google::protobuf::Message*>       _messages_to_recycle; ///<a list of messages to be reused

        //! @brief verify that the message definition is compatible with the file's data
        //! @param descriptor the descriptor against which the file's structure should be verified
        void initializeMessageDesc(const google::protobuf::Descriptor* descriptor=NULL);

        //! @brief verify a specific FITS column against the message description
        //! @param id the string ID of the field's location in the message structure
        //! @param desc the top-level descriptor of the messages to read
        //! @param type the expected type in the message structure, converted from the FITS type
        //! @param isArray whether this FITS column is a scalar or an array
        //! @param multipleOccurence whether or not this field appears in several FITS columns
        //! @param foundRepeatedMessage whether or not the field is under a repeated message
        bool verifyColumnVsDescription(const std::string&                            id,
                                       const google::protobuf::Descriptor*           desc,
                                       const google::protobuf::FieldDescriptor::Type type,
                                       const bool                                    isArray);

        //! @brief once a buffer has been uncompressed, deserializes the data and fill it into the messaage's fields
        //! @param index current ID of the column being de-serialized
        void populateMessageField(int32 index);

        //! @brief decompress a rice compressed buffer
        //! @param dest where to put the decompressed data. It is assumed that it is at least of size GetBytesPerRow()*fNumRowsPerTile
        //! @param src where is the compressed data
        //! @param num_bytes how many bytes are stored in the compressed buffer
        uint64_t riceDecompress(      char*        dest,
                                const char*  const src,
                                      uint32       num_bytes);

        //! @brief decompress an lzo compressed buffer
        //! @param dest where to put the decompressed data. It is assumed that it is at least of size GetBytesPerRow()*fNumRowsPerTile
        //! @param src where is the compressed data
        //! @param num_bytes how many bytes are stored in the compressed buffer
        uint64_t lzoDecompress(      char*        dest,
                               const char*  const src,
                                     uint32       num_bytes);

        //! @brief decompress a zlib compressed buffer
        //! @param dest where to put the decompressed data. It is assumed that it is at least of size GetBytesPerRow()*fNumRowsPerTile
        //! @param src where is the compressed data
        //! @param num_bytes how many bytes are stored in the compressed buffer
        uint64_t zlibDecompress(const char*        dest,
                                const char*  const src,
                                      uint32       num_bytes);

        //! @brief merge 16bit words that were split for better compresion ratio. The merge is done in place
        //! @param buffer the buffer where the split words are located.
        //! @param num_bytes the total size of the buffer, in bytes
        void mergeHiLo16(char*  buffer,
                         uint32 num_bytes);
        void mergeHiLo32(char*  buffer,
                         uint32 num_bytes);
        //! @brief template to set a message value from a given input. Never used, only specializations are to be executed
        //! @param message the target message to populate
        //! @param field the target field in the message to populate
        //! @param reflec the associated reflection structure
        //! @param value the actual value to be set
        template <typename T_>
        void setProtobufValue(google::protobuf::Message*               message,
                              const google::protobuf::FieldDescriptor* field,
                              const google::protobuf::Reflection*      reflec,
                              const T_                                 value)
        {
            std::ostringstream str;
            std::cout << "ERROR: Unable to set value for unhandled type (" << typeid(T_).name() << "). Aborting.";
            throw std::runtime_error(str.str());
        }

        //! @brief template to set a message repeated value from a given input. Never used, only specializations are to be executed
        //! @param message the target message to populate
        //! @param field the target field in the message to populate
        //! @param reflec the associated reflection structure
        //! @param value the actual pointer to values to be set
        //! @param num_values the number of items to set
        template <typename T_>
        void setProtobufRepeatedValue(google::protobuf::Message*               message,
                                      const google::protobuf::FieldDescriptor* field,
                                      const google::protobuf::Reflection*      reflec,
                                      const T_*                                values,
                                      const uint32                             num_values)
        {
            std::ostringstream str;
            std::cout << "ERROR: Unable to set repeated value for unhandled type (" << typeid(T_).name() << "). Aborting.";
            throw std::runtime_error(str.str());
        }

        //! @brief reads a raw buffer, and populate the designated field in an array of messages
        //! @param src a pointer to the input memory
        //! @param message a vector of messages to be filled in from the input memory
        //! @param field the target field that should be populated
        //! @param reflec the associated reflection structure
        template <typename T_>
        uint32 deserialize(char*                                          src,
                           const std::vector<google::protobuf::Message*>& messages,
                           const google::protobuf::FieldDescriptor*       field,
                           const google::protobuf::Reflection*            reflec)
        {
            char* orig_src = src;
            if (field->is_repeated())
            {
                for (auto it=messages.begin(); it!= messages.end(); it++)
                {
                    uint32 num_items = reinterpret_cast<uint32*>(src)[0];
                    src += sizeof(uint32);
                    T_* t_data = reinterpret_cast<T_*>(src);
                    setProtobufRepeatedValue<T_>(*it, field, reflec, t_data, num_items);
                    src = reinterpret_cast<char*>(t_data + num_items);
                }
            }
            else
            {
                T_* t_data = reinterpret_cast<T_*>(src);
                for (auto it=messages.begin(); it!= messages.end(); it++)
                {
                    setProtobufValue<T_>(*it, field, reflec, t_data[0]);
                    t_data++;
                }
                src = reinterpret_cast<char*>(t_data);
            }
            return (uint32)(src - orig_src);
        }

        //! @brief for Any arrays, we need a specific deserialize because it required to know which column is being deserialized
        uint32 deserializeAnyArray(char* src, const std::vector<google::protobuf::Message*>& messages, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const int32 column_index);
        uint32 deserialize_chars(char*                                          src,
                           const std::vector<google::protobuf::Message*>& messages,
                           const google::protobuf::FieldDescriptor*       field,
                           const google::protobuf::Reflection*            reflec);
};

/*************************************
 *TEMPLATES SPECIALIZATIONS
 ************************************/
template<> uint32 ProtobufIFits::deserialize<google::protobuf::EnumValueDescriptor>(char* src, const std::vector<google::protobuf::Message*>& messages, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);

template <> void ProtobufIFits::setProtobufValue<uint32>(google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const uint32 value);
template <> void ProtobufIFits::setProtobufValue<int32> (google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const int32  value);
template <> void ProtobufIFits::setProtobufValue<uint64>(google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const uint64 value);
template <> void ProtobufIFits::setProtobufValue<int64> (google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const int64  value);
template <> void ProtobufIFits::setProtobufValue<double>(google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const double value);
template <> void ProtobufIFits::setProtobufValue<float> (google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const float  value);
template <> void ProtobufIFits::setProtobufValue<bool>  (google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const bool   value);

template <> void ProtobufIFits::setProtobufRepeatedValue<uint32>(google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const uint32* values, const uint32 num_values);
template <> void ProtobufIFits::setProtobufRepeatedValue<int32> (google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const int32*  values, const uint32 num_values);
template <> void ProtobufIFits::setProtobufRepeatedValue<uint64>(google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const uint64* values, const uint32 num_values);
template <> void ProtobufIFits::setProtobufRepeatedValue<int64> (google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const int64*  values, const uint32 num_values);
template <> void ProtobufIFits::setProtobufRepeatedValue<double>(google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const double* values, const uint32 num_values);
template <> void ProtobufIFits::setProtobufRepeatedValue<float> (google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const float*  values, const uint32 num_values);
template <> void ProtobufIFits::setProtobufRepeatedValue<bool>  (google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const bool*   values,const  uint32 num_values);

}//namespace IO
}//namespace ADH

#endif /* PROTOBUFIFITS_H_ */
