/**
 * @file ProtobufToFits.cpp
 *
 * @brief base class for both ProtobufOFits and ProtobufZOFits
 * Created on: Mar 10, 2015
 *      Author: lyard
 */

 #include "ProtobufToFits.h"


 using namespace google::protobuf;
 using namespace std;
 using namespace ADH::ColoredOutput;

 namespace ADH
 {
 namespace IO
 {
    ProtobufToFits::ProtobufToFits() : _total_num_columns(0),
                                       _columns_sizes(0),
                                       _descriptor(NULL)
                                       {}
    ProtobufToFits::~ProtobufToFits(){}

/*******************************************************************************
 * VETO FIELD
 *******************************************************************************/
void ProtobufToFits::vetoField(const string& name, bool missing_field)
{
    //make sure that the columns are not initialized yet
    if (!missing_field && _descriptor != NULL)
        throw runtime_error("The columns seem to be already initialized... "
                            "A bit late to ignore new fields");

    if (missing_field)
        _missing_fields.insert(name);
    else
        _vetoed_fields.insert(name);
}

/*******************************************************************************
 * ALLOW FIELD
 *******************************************************************************/
void ProtobufToFits::allowField(const string& name)
{
    _allowed_fields.insert(name);
}

/*******************************************************************************
 * IS VETOED
 *******************************************************************************/
bool ProtobufToFits::isVetoed(const string& name)
{
    string name_no_index = name;
    //remove any index inserted into the name
    //FIXME this collides with _ inserted in fields names
    while (name_no_index.find('#') !=  string::npos)
    {
        //get the first underscore
        size_t underscore_index = name_no_index.find_first_of('#');
        ostringstream str;
        size_t end_index = name_no_index.find_first_of('.', underscore_index);

        //concatenate up to the first underscore
        str << name_no_index.substr(0, underscore_index);

        //add the trailing chars, if any
        if (end_index != string::npos) str << name_no_index.substr(end_index);

        name_no_index = str.str();
    }

    return ((_vetoed_fields.find(name_no_index) != _vetoed_fields.end()) ||
            (_missing_fields.find(name_no_index) != _missing_fields.end()))
            ;
}

/*******************************************************************************
 * IS ALLOWED
 *******************************************************************************/
bool ProtobufToFits::isAllowed(const string& name)
{
    return (_allowed_fields.find(name) != _allowed_fields.end());
}


/********************************************************************************
 ********************************************************************************
 * TEMPLATES SPECIALIZATION.
 * No, they should not be in the header files and this is because they are
 * specialization, not definitions (their defs are in the header though).
 ********************************************************************************
 ********************************************************************************/

/*******************************************************************************
 *  SERIALIZE DataModel::Any ARRAY
 *******************************************************************************/
template <>
google::protobuf::uint32 ProtobufToFits::serialize<AnyArray>(char*                  target,
                                           const Message*         message,
                                           const FieldDescriptor* field,
                                           const Reflection*      ,
                                           const google::protobuf::int32            col_index)
{
    google::protobuf::uint32 num_bytes_written = 0;
    const google::protobuf::Descriptor* desc = field->message_type();
    const google::protobuf::Reflection* refl = message->GetReflection();

    const string& data = refl->GetString(*message, desc->FindFieldByNumber(ANYARRAY_DATA));

    //FIXME make sure that the size is small enough to fit into a signed int32
    reinterpret_cast<google::protobuf::int32*>(target)[0] = (google::protobuf::int32)(data.size());
    num_bytes_written = sizeof(google::protobuf::int32);

    //update the max size of the column, if required
    google::protobuf::uint32 num_items = data.size();
    switch (refl->GetEnum(*message, desc->FindFieldByNumber(ANYARRAY_TYPE))->number())
    {
        case AnyArray::U16:
        case AnyArray::S16:
            num_items /= 2;
            break;
        case AnyArray::U32:
        case AnyArray::S32:
        case AnyArray::FLOAT:
            num_items /= 4;
            break;
        case AnyArray::U64:
        case AnyArray::S64:
        case AnyArray::DOUBLE:
            num_items /= 8;
            break;
        default:
            break;
    }

    if (num_items > _columns_sizes[col_index])
        _columns_sizes[col_index] = num_items;

    memcpy(target+num_bytes_written, &data[0], data.size());
    num_bytes_written += data.size();

    return num_bytes_written;
}

/*******************************************************************************
 *  SERIALIZE DataModel::char, i.e. strings or bytes
 *******************************************************************************/
template <>
google::protobuf::uint32 ProtobufToFits::serialize<char>(char*                  target,
                                       const Message*         message,
                                       const FieldDescriptor* field,
                                       const Reflection*      ,
                                       const google::protobuf::int32            col_index)
{
    if (field->is_repeated())
        throw runtime_error("Repeated string / bytes fields not handled "
                            "yet in zfits... sorry !");

    google::protobuf::uint32 num_bytes_written = 0;

    const google::protobuf::Reflection* refl = message->GetReflection();

    const string& data = refl->GetString(*message, field);
    //FIXME make sure that the size is small enough to fit into a signed int32
    reinterpret_cast<google::protobuf::int32*>(target)[0] = (google::protobuf::int32)(data.size());
    num_bytes_written = sizeof(google::protobuf::int32);

    //update the max size of the column, if required
    google::protobuf::uint32 num_items = data.size();

    if (num_items > _columns_sizes[col_index])
        _columns_sizes[col_index] = num_items;

    memcpy(target+num_bytes_written, &data[0], data.size());
    num_bytes_written += data.size();

    return num_bytes_written;
}


/*******************************************************************************
 *  SERIALIZE ENUM
 *******************************************************************************/
template <>
google::protobuf::uint32 ProtobufToFits::serialize<EnumValueDescriptor>(char*                  target,
                                                      const Message*         message,
                                                      const FieldDescriptor* field,
                                                      const Reflection*      reflec,
                                                      const google::protobuf::int32            col_index)
{
    google::protobuf::uint32 num_bytes_written = 0;

    if (field->is_repeated())
    {
        google::protobuf::int32 field_size = reflec->FieldSize(*message, field);
        reinterpret_cast<google::protobuf::uint32*>(target)[0] = field_size;
        num_bytes_written += sizeof(google::protobuf::uint32);

        for (google::protobuf::int32 i=0; i<field_size; i++)
        {
            reinterpret_cast<google::protobuf::int32*>(target+num_bytes_written)[0] =
                reflec->GetRepeatedEnum(*message, field, i)->number();
            num_bytes_written += sizeof(google::protobuf::int32);
        }
        if ((google::protobuf::uint32)(field_size) > _columns_sizes[col_index])
            _columns_sizes[col_index] = field_size;
    }
    else
    {
        reinterpret_cast<google::protobuf::int32*>(target)[0] =
            reflec->GetEnum(*message, field)->number();
        num_bytes_written += sizeof(google::protobuf::int32);
    }

    return num_bytes_written;
}

/*******************************************************************************
 *  GET ENUM VALUE
 *******************************************************************************/
google::protobuf::int32 ProtobufToFits::getProtobufEnumValue(const Message& message,
                                           const FieldDescriptor* field,
                                           const Reflection* reflec)
{
    return reflec->GetEnum(message, field)->number();
}

/*******************************************************************************
 *  GET PROTOBUF VALUE UINT32
 *******************************************************************************/
template <>
google::protobuf::uint32 ProtobufToFits::getProtobufValue<google::protobuf::uint32>(const Message& message,
                                                const FieldDescriptor* field,
                                                const Reflection* reflec)
{
    return reflec->GetUInt32(message, field);
}

/*******************************************************************************
 *  GET PROTOBUF VALUE INT32
 *******************************************************************************/
template <>
google::protobuf::int32 ProtobufToFits::getProtobufValue<google::protobuf::int32>(const Message& message,
                                              const FieldDescriptor* field,
                                              const Reflection* reflec)
{
    return reflec->GetInt32(message, field);
}

/*******************************************************************************
 *  GET PROTOBUF VALUE UINT64
 *******************************************************************************/
template <>
google::protobuf::uint64 ProtobufToFits::getProtobufValue<google::protobuf::uint64>(const Message& message,
                                                const FieldDescriptor* field,
                                                const Reflection* reflec)
{
    return reflec->GetUInt64(message, field);
}

/*******************************************************************************
 *  GET PROTOBUF VALUE INT64
 *******************************************************************************/
template <>
google::protobuf::int64 ProtobufToFits::getProtobufValue<google::protobuf::int64>(const Message& message,
                                              const FieldDescriptor* field,
                                              const Reflection* reflec)
{
    return reflec->GetInt64(message, field);
}

/*******************************************************************************
 *  GET PROTOBUF VALUE DOUBLE
 *******************************************************************************/
template <>
double ProtobufToFits::getProtobufValue<double>(const Message& message,
                                                const FieldDescriptor* field,
                                                const Reflection* reflec)
{
    return reflec->GetDouble(message, field);
}

/*******************************************************************************
 *  GET PROTOBUF VALUE FLOAT
 *******************************************************************************/
template <>
float ProtobufToFits::getProtobufValue<float>(const Message& message,
                                              const FieldDescriptor* field,
                                              const Reflection* reflec)
{
    return reflec->GetFloat(message, field);
}

/*******************************************************************************
 *  GET PROTOBUF VALUE BOOL
 *******************************************************************************/
template <>
bool ProtobufToFits::getProtobufValue<bool>(const Message& message,
                                            const FieldDescriptor* field,
                                            const Reflection* reflec)
{
    return reflec->GetBool(message, field);
}

/*******************************************************************************
 *  GET PROTOBUF REPEATED VALUE UINT32
 *******************************************************************************/
template <>
google::protobuf::uint32 ProtobufToFits::getProtobufRepeatedValue<google::protobuf::uint32>(const Message& message,
                                                        const FieldDescriptor* field,
                                                        const Reflection* reflec,
                                                        google::protobuf::int32 index)
{
    return reflec->GetRepeatedUInt32(message, field, index);
}

/*******************************************************************************
 *  GET PROTOBUF REPEATED VALUE INT32
 *******************************************************************************/
template <>
google::protobuf::int32 ProtobufToFits::getProtobufRepeatedValue<google::protobuf::int32>(const Message& message,
                                                      const FieldDescriptor* field,
                                                      const Reflection* reflec,
                                                      google::protobuf::int32 index)
{
    return reflec->GetRepeatedInt32(message, field, index);
}

/*******************************************************************************
 *  GET PROTOBUF REPEATED VALUE UINT64
 *******************************************************************************/
template <>
google::protobuf::uint64 ProtobufToFits::getProtobufRepeatedValue<google::protobuf::uint64>(const Message& message,
                                                        const FieldDescriptor* field,
                                                        const Reflection* reflec,
                                                        google::protobuf::int32 index)
{
    return reflec->GetRepeatedUInt64(message, field, index);
}

/*******************************************************************************
 *  GET PROTOBUF REPEATED VALUE INT64
 *******************************************************************************/
template <>
google::protobuf::int64 ProtobufToFits::getProtobufRepeatedValue<google::protobuf::int64>(const Message& message,
                                                      const FieldDescriptor* field,
                                                      const Reflection* reflec,
                                                      google::protobuf::int32 index)
{
    return reflec->GetRepeatedInt64(message, field, index);
}

/*******************************************************************************
 *  GET PROTOBUF REPEATED VALUE DOUBLE
 *******************************************************************************/
template <>
double ProtobufToFits::getProtobufRepeatedValue<double>(const Message& message,
                                                        const FieldDescriptor* field,
                                                        const Reflection* reflec,
                                                        google::protobuf::int32 index)
{
    return reflec->GetRepeatedDouble(message, field, index);
}

/*******************************************************************************
 *  GET PROTOBUF REPEATED VALUE FLOAT
 *******************************************************************************/
template <>
float ProtobufToFits::getProtobufRepeatedValue<float>(const Message& message,
                                                      const FieldDescriptor* field,
                                                      const Reflection* reflec,
                                                      google::protobuf::int32 index)
{
    return reflec->GetRepeatedFloat(message, field, index);
}

/*******************************************************************************
 *  GET PROTOBUF REPEATED VALUE BOOL
 *******************************************************************************/
template <> bool ProtobufToFits::getProtobufRepeatedValue<bool>(const Message& message,
                                                                const FieldDescriptor* field,
                                                                const Reflection* reflec,
                                                                google::protobuf::int32 index)
{
    return reflec->GetRepeatedBool(message, field, index);
}


 }; //namespace IO
 }; //namespace ADH
