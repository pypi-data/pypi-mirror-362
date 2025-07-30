/**
 * @file ProtobufToFits.h
 *
 * @brief base class for both ProtobufOFits and ProtobufZOFits
 * Created on: Mar 10, 2015
 *      Author: lyard
 */

 #ifndef PROTOBUFTOFITS_H_
 #define PROTOBUFTOFITS_H_

 #include "BasicDefs.h"
 #include "ProtoDataModel.pb.h"

 #include "FitsDefs.h"

 #include <iostream>
 #include <sstream>
 #include <set>
 #include <string>
 #include <stdexcept>

 namespace ADH
 {
 namespace IO
 {
/**
 *      @class ProtobufToFits
 *      @brief Base class for the common stuff between ProtobufOFits
 *             and ProtobufZOFits
 */
 class ProtobufToFits
 {
    public:

        ProtobufToFits();

        virtual ~ProtobufToFits();

        //! @brief prevents a given message's item to be written.
        //!
        //! The name should be the name as declared in the .proto file,
        //! with children structures being separated by '.'
        //! Note that the name of the fields should be used rather than
        //! the name of the message's classes
        //! Note also that the name of the top-level message is omitted
        //! @param name the string describing the field to be ignored
        void vetoField(const std::string& name, bool missing_field = false);

        void allowField(const std::string& name);

    protected:

        /// Simply counts the number of columns that were
        /// created from the message
        int32 _total_num_columns;

        /// the max. size of each column, to be able to
        /// update the columns description upon closing the file.
        std::vector<uint32> _columns_sizes;

        /// descriptor of the current messages
        /// being written to the fits file.
        const google::protobuf::Descriptor* _descriptor;

        /// A list of fields that should not be
        /// written to the data table
        std::set<std::string> _vetoed_fields;
        std::set<std::string> _missing_fields;
        std::set<std::string> _allowed_fields;

        //! @brief tells whether a given message's field name
        /// has been vetoed or not
        //! @param name the name of a given column to check for
        //! @return whether or not the given name has been vetoed
        bool isVetoed(const std::string& name);
        bool isAllowed(const std::string& name);

        /// tells how many children are to be expected,
        /// based on the initialization
        std::map<int, int> _num_expected_child;


    public:
        //! @brief get the value described by a given FieldDescriptor
        ///        from a given message
        //! @param message the message from which the field's value
        ///        must be retrieved
        //! @param field the descriptor of the field to retrieve
        //! @param reflec the reflection associated with the input message
        template <typename T_>
        T_ getProtobufValue(const google::protobuf::Message& message,
                            const google::protobuf::FieldDescriptor* field,
                            const google::protobuf::Reflection* reflec)
        {
            std::ostringstream str;
            std::cout << "Unhandled type (" << typeid(T_).name();
            std::cout << ") in getProtobufValue... specialization is missing";
            throw std::runtime_error(str.str());
            return T_();
        }

        int32 getProtobufEnumValue(const google::protobuf::Message& message,
                                   const google::protobuf::FieldDescriptor* field,
                                   const google::protobuf::Reflection* reflec);

    protected:


        //! @brief get the value at the given index of a repeated field
        //! @param message the message from which the repeated field's
        ///        value must be retrieved
        //! @param field the descriptor of the field to retrieve
        //! @param reflec the reflection associated with the input message
        //! @param index the index of the value to be retrieved in the
        ///        repeated array
        template <typename T_>
        T_ getProtobufRepeatedValue(const google::protobuf::Message& message,
                                    const google::protobuf::FieldDescriptor* field,
                                    const google::protobuf::Reflection* reflec,
                                    int32 index)
        {
            std::ostringstream str;
            std::cout << "Unhandled type (" << typeid(T_).name();
            std::cout << ") in getProtobufRepeatedValue... specialization ";
            std::cout << "is missing";
            throw std::runtime_error(str.str());
            return T_();
        }

        //! @brief serialize a given field inside a protobuf message
        //! @param target the buffer where to write the data. It must
        ///        always be large enough to contain the serialization
        ///        (from initialization)
        //! @param message the message containing the field to be serialized
        //! @param field the descriptor of the field to retrieve
        //! @param reflec the reflection associated with the input message
        //! @return the number of bytes written to the buffer
        template <typename T_>
        uint32 serialize(char*                                    target,
                         const google::protobuf::Message*         message,
                         const google::protobuf::FieldDescriptor* field,
                         const google::protobuf::Reflection*      reflec,
                         const int32                              col_index)
        {
            uint32 num_bytes_written = 0;

            if (field->is_repeated())
            {
                int32 field_size = reflec->FieldSize(*message, field);
                reinterpret_cast<uint32*>(target)[0] = field_size;
                num_bytes_written += sizeof(uint32);

                for (int32 i=0; i<field_size; i++)
                {
                    reinterpret_cast<T_*>(target+num_bytes_written)[0] =
                        getProtobufRepeatedValue<T_>(*message, field, reflec, i);
                    num_bytes_written += sizeof(T_);
                }

                if ((uint32)(field_size) > _columns_sizes[col_index])
                    _columns_sizes[col_index] = field_size;
            }
            else
            {
                reinterpret_cast<T_*>(target)[0] =
                    getProtobufValue<T_>(*message, field, reflec);
                num_bytes_written += sizeof(T_);
            }

            return num_bytes_written;
        }

 }; //class protobuftofits

 /*************************************
 *TEMPLATES SPECIALIZATIONS
 ************************************/
template <> uint32 ProtobufToFits::serialize<AnyArray>(char* target, const google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const int32 col_index);
template <> uint32 ProtobufToFits::serialize<google::protobuf::EnumValueDescriptor>(char* target, const google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const int32 col_index);
template <> uint32 ProtobufToFits::serialize<char>(char* target, const google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const int32 col_index);

template <> uint32 ProtobufToFits::getProtobufValue<uint32>(const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);
template <> int32  ProtobufToFits::getProtobufValue<int32> (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);
template <> uint64 ProtobufToFits::getProtobufValue<uint64>(const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);
template <> int64  ProtobufToFits::getProtobufValue<int64> (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);
template <> double ProtobufToFits::getProtobufValue<double>(const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);
template <> float  ProtobufToFits::getProtobufValue<float> (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);
template <> bool   ProtobufToFits::getProtobufValue<bool>  (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);

template <> uint32 ProtobufToFits::getProtobufRepeatedValue<uint32>(const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);
template <> int32  ProtobufToFits::getProtobufRepeatedValue<int32> (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);
template <> uint64 ProtobufToFits::getProtobufRepeatedValue<uint64>(const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);
template <> int64  ProtobufToFits::getProtobufRepeatedValue<int64> (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);
template <> double ProtobufToFits::getProtobufRepeatedValue<double>(const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);
template <> float  ProtobufToFits::getProtobufRepeatedValue<float> (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);
template <> bool   ProtobufToFits::getProtobufRepeatedValue<bool>  (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);


 }; //namespace IO
 }; //namespace ADH

 #endif //PROTOBUFTOFITS_H_
