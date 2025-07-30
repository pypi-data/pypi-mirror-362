/**
 * @file ProtobufOFits.h
 *
 * @brief protobuf to plain FITS writer, NOT FINISHED YET
 * Created on: Mar 10, 2015
 *      Author: lyard
 *
 */

 #ifndef PROTOBUFOFITS_H_
 #define PROTOBUFOFITS_H_

 #include "OFits.h"
 #include "ProtobufToFits.h"
 #include "BasicDefs.h"

#include "ProtoDataModel.pb.h"

namespace ADH
{
namespace IO
{
/**
 *      @class ProtobufOFits
 *      @brief low-level plain FITS writer for protobuf messages
 *      IS NOT FULLY FINISHED YET: use it at your own risks
 *
 *      Each message is written to a row while each message field
 *      become a separate column. If a message features repeated
 *      child-messages in a field, then one column is created per-
 *      child-per-field. Unlike with compressed FITS, the width of
 *      each row must remain constant. Thus, for variable-length
 *      fields, the number of element in each field must remain constant
 */
 class ProtobufOFits : public OFits,
                       public ProtobufToFits
 {
    public:
        //! @brief default constructor
        ProtobufOFits();

        //! @brief default constructor
        virtual ~ProtobufOFits();

        //! @brief initializes the columns of the fits file from the
        //!        message structure
        //!
        //! The message given as example should be as large as it can
        //! be in the case of children messages in fields so that appropriate
        /// columns can be created. In the case of repeated base-type arrays,
        /// their maximum size is extracted from the written data: no
        /// limitation here. If this method is not called explicitely,
        //! the file's structure is created from the first written message
        //! @param message a pointer to the example message
        virtual void initColumns(const google::protobuf::Message* message);

        //! @brief write a given message to the fits file
        //! The ownership of the pointer is given to the writer.
        //! Once the structure has been written, the ownership can
        /// be regained by calling the getRecycledMessage() method
        //! @param message a pointer to the message to be written
        virtual void writeMessage(google::protobuf::Message* message);

        //! @brief close the currently open file
        //! @return whether or not the file has been successfully written.
        /// Equivalent to ofstream::good()
        virtual bool close();

    private:
        //! @brief specific FITS columns intialization in case of the custom
        ///        AnyArray message type
        //! @param message containing the cta array to use for the
        ///        initialization
        //! @param name the full name of this message
        void addAnyArrayColumn(const google::protobuf::Message& message,
                               const std::string& name,
                               const std::string& id="");

        //! @brief crawls through the input message using reflexion and
        ///        build the corresponding fits columns
        //! @param message the current message to use for the initialization
        //! @param name the full name of the current message, for naming columns
        void buildFitsColumns(const google::protobuf::Message& message,
                              const std::string&               name="",
                              const std::string&               id="");

        void writeMessageFields(const google::protobuf::Message* message,
                                int32&                           col_index,
                                const std::string&               name,
                                int32&                           size_written);

        uint32 serializeAnyArrayToFITS(char*                           target,
                              const google::protobuf::Message*         message,
                              const google::protobuf::FieldDescriptor* field,
                              const google::protobuf::Reflection*      ,
                              const int32                              col_index);

        uint32 serializeUInt32(char*                                    target,
                               const google::protobuf::Message*         message,
                               const google::protobuf::FieldDescriptor* field,
                               const google::protobuf::Reflection*      reflec,
                               const int32                              col_index);

        uint32 serializeUInt64(char*                                    target,
                             const google::protobuf::Message*         message,
                             const google::protobuf::FieldDescriptor* field,
                             const google::protobuf::Reflection*      reflec,
                             const int32                              col_index);

        uint32 serializeUInt16(char*                                    target,
                         const google::protobuf::Message*         message,
                         const google::protobuf::FieldDescriptor* field,
                         const google::protobuf::Reflection*      reflec,
                         const int32                              col_index);

        char* _one_row;
        int32 _row_size;

}; //class protobufofits

}; //namespace ADH
}; //namespace IO

#endif
