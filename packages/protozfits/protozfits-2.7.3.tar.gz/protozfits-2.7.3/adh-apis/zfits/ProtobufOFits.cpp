/**
 * @file ProtobufOFits.cpp
 *
 * @brief protobuf to plain FITS writer, NOT FINISHED YET
 * Created on: Mar 10, 2015
 *      Author: lyard
 *
 */

 #include "ProtobufOFits.h"

 using namespace std;
 using namespace google::protobuf;
 using namespace ADH::ColoredOutput;

 namespace ADH
 {
 namespace IO
 {

/************************************************
 *  DEFAULT CONSTRUCTOR
 ************************************************/
ProtobufOFits::ProtobufOFits() : OFits(),
                                 ProtobufToFits()
{
}

/************************************************
 *  DEFAULT DESTRUCTOR
 ************************************************/
ProtobufOFits::~ProtobufOFits()
{
    if (is_open())
        if (!close())
            throw runtime_error("Impossible to close file");
}

/************************************************
 *  INIT COLUMNS
 ************************************************/
void ProtobufOFits::initColumns(const Message* message)
{
    //Only one given message type can be writen at a given time...
    if (_descriptor != NULL)
        throw runtime_error("Looks like you are trying to initialize "
                            "the columns of the tables more than once... "
                            "this is NOT allowed.");

    //store the message descriptor.
    _descriptor = message->GetDescriptor();

    SetStr("PBFHEAD", std::string{_descriptor->full_name()}, "Written message name");

    _total_num_columns = 0;
    //build the fits columns from the message. Start with an empty prefix
    buildFitsColumns(*message);

    _row_size = 0;
    for (auto it=_columns_sizes.begin(); it!=_columns_sizes.end(); it++)
        _row_size += *it;

    _one_row = new char[_row_size];
}

/************************************************
 *  WRITE MESSAGE
 ************************************************/
void ProtobufOFits::writeMessage(Message* message)
{
    if (_descriptor == NULL)
    {
        initColumns(message);
        WriteTableHeader();
    }

    if (_descriptor != message->GetDescriptor())
        throw runtime_error("Only one kind of message can be written at a "
                            "given time...");

    google::protobuf::int32 column_index = 0;
    google::protobuf::int32 size_written = 0;
    writeMessageFields(message, column_index, "", size_written);

    WriteRow(_one_row, _row_size);
}

/*******************************************************************************
 *  SERIALIZE DataModel::Any ARRAY
 *******************************************************************************/
google::protobuf::uint32 ProtobufOFits::serializeAnyArrayToFITS(char*                  target,
                                              const Message*         message,
                                              const FieldDescriptor* field,
                                              const Reflection*      ,
                                              const google::protobuf::int32            col_index)
{
    google::protobuf::uint32 num_bytes_written = 0;
    const google::protobuf::Descriptor* desc = field->message_type();
    const google::protobuf::Reflection* refl = message->GetReflection();

    const string& data = refl->GetString(*message, desc->FindFieldByNumber(ANYARRAY_DATA));

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

    memcpy(target+num_bytes_written, &data[0], data.size());

    switch (refl->GetEnum(*message, desc->FindFieldByNumber(ANYARRAY_TYPE))->number())
    {
        case AnyArray::U16:
        {
            google::protobuf::int16*  signed_pointer   =
                reinterpret_cast<google::protobuf::int16*>(target+num_bytes_written);
            google::protobuf::uint16* unsigned_pointer =
                reinterpret_cast<google::protobuf::uint16*>(target+num_bytes_written);
            for (google::protobuf::uint32 i=0;i<num_items;i++)
                signed_pointer[i] = unsigned_pointer[i] - 32768;
        }
        break;
        case AnyArray::U32:
        {
            google::protobuf::int32*  signed_pointer   =
                reinterpret_cast<google::protobuf::int32*>(target+num_bytes_written);
            google::protobuf::uint32* unsigned_pointer =
                reinterpret_cast<google::protobuf::uint32*>(target+num_bytes_written);
            for (google::protobuf::uint32 i=0;i<num_items;i++)
                signed_pointer[i] = unsigned_pointer[i] - 2147483648;
        }
        break;
        case AnyArray::U8:
        {
            char*  signed_pointer   =
                reinterpret_cast<char*>(target+num_bytes_written);
            unsigned char* unsigned_pointer =
                reinterpret_cast<unsigned char*>(target+num_bytes_written);
            for (google::protobuf::uint32 i=0;i<num_items;i++)
            {
                signed_pointer[i] = (google::protobuf::int32)(unsigned_pointer[i]) - 128;
            }
        }
        break;

//        case AnyArray::U64:
//        {
//            int64*  signed_pointer   = reinterpret_cast<int64*>(target+num_bytes_written);
//            uint64* unsigned_pointer = reinterpret_cast<uint64*>(target+num_bytes_written);
//            for (uint32 i=0;i<num_items;i++)
//                signed_pointer[i] = unsigned_pointer[i] - 9223372036854775807;
//        }
        break;

        default:
        break;
    };

    num_bytes_written += data.size();

    return num_bytes_written;
}


/*******************************************************************************
 *  SERIALIZE UNSIGNED INT 32 BITS
 *******************************************************************************/
google::protobuf::uint32 ProtobufOFits::serializeUInt32(char*                  target,
                                      const Message*         message,
                                      const FieldDescriptor* field,
                                      const Reflection*      reflec,
                                      const google::protobuf::int32            col_index)
{
    google::protobuf::uint32 num_bytes_written = 0;

    if (field->is_repeated())
    {
        google::protobuf::int32 field_size = reflec->FieldSize(*message, field);

        for (google::protobuf::int32 i=0; i<field_size; i++)
        {
            reinterpret_cast<google::protobuf::int32*>(target+num_bytes_written)[0] =
    getProtobufRepeatedValue<google::protobuf::uint32>(*message, field, reflec, i) - 2147483648;
            num_bytes_written += sizeof(google::protobuf::uint32);
        }
    }
    else
    {
        reinterpret_cast<google::protobuf::int32*>(target)[0] =
            getProtobufValue<google::protobuf::uint32>(*message, field, reflec) - 2147483648;
        num_bytes_written += sizeof(google::protobuf::uint32);
    }

    return num_bytes_written;
}


/*******************************************************************************
 *  SERIALIZE UNSIGNED INT 64 BITS
 *******************************************************************************/
google::protobuf::uint32 ProtobufOFits::serializeUInt64(char*                  target,
                                      const Message*         message,
                                      const FieldDescriptor* field,
                                      const Reflection*      reflec,
                                      const google::protobuf::int32            col_index)
{
    google::protobuf::uint32 num_bytes_written = 0;

    if (field->is_repeated())
    {
        google::protobuf::int32 field_size = reflec->FieldSize(*message, field);

        for (google::protobuf::int32 i=0; i<field_size; i++)
        {
//            reinterpret_cast<int64*>(target+num_bytes_written)[0] = getProtobufRepeatedValue<uint64>(*message, field, reflec, i) - 9223372036854775807;
            reinterpret_cast<google::protobuf::int64*>(target+num_bytes_written)[0] =
            getProtobufRepeatedValue<google::protobuf::uint64>(*message, field, reflec, i);// - 9223372036854775807;
            num_bytes_written += sizeof(google::protobuf::uint64);
        }
    }
    else
    {
//        uint64 value = getProtobufValue<uint64>(*message, field, reflec) ;
//        cout << "Value: " << value << endl;
//        int64 svalue = value - 9223372036854775807;
//        cout << "Signed value: " << svalue << endl;
//        value = svalue + 9223372036854775807;
//        cout << "Recovered value: " << value << endl << endl;
  //      reinterpret_cast<int64*>(target)[0] = getProtobufValue<uint64>(*message, field, reflec) - 9223372036854775800;
        reinterpret_cast<google::protobuf::int64*>(target)[0] =
        getProtobufValue<google::protobuf::uint64>(*message, field, reflec);
        num_bytes_written += sizeof(google::protobuf::uint64);
    }

    return num_bytes_written;
}

google::protobuf::uint32 ProtobufOFits::serializeUInt16(char*                  target,
                                      const Message*         message,
                                      const FieldDescriptor* field,
                                      const Reflection*      reflec,
                                      const google::protobuf::int32            col_index)
{
    google::protobuf::uint32 num_bytes_written = 0;

    if (field->is_repeated())
    {
        google::protobuf::int32 field_size = reflec->FieldSize(*message, field);

        for (google::protobuf::int32 i=0; i<field_size; i++)
        {
            reinterpret_cast<google::protobuf::int16*>(target+num_bytes_written)[0] =
            getProtobufRepeatedValue<google::protobuf::uint16>(*message, field, reflec, i) - 32768;
            num_bytes_written += sizeof(google::protobuf::uint16);
        }
    }
    else
    {
        reinterpret_cast<google::protobuf::int16*>(target)[0] =
        getProtobufValue<google::protobuf::uint16>(*message, field, reflec) - 32768;
        num_bytes_written += sizeof(google::protobuf::uint16);
    }

    return num_bytes_written;
}

void ProtobufOFits::writeMessageFields(const Message* message,
                                       google::protobuf::int32&         col_index,
                                       const          string& name,
                                       google::protobuf::int32&         size_written)
{
    const Descriptor* desc = message->GetDescriptor();
    const Reflection*  refl = message->GetReflection();

    const string prefix_name = (name=="") ? "" : name+".";

    for (google::protobuf::int32 i=0;i<desc->field_count();i++)
    {
        const FieldDescriptor* field = desc->field(i);
        const string full_name = prefix_name + std::string{field->name()};

        if (isVetoed(full_name))
            continue;

        switch (field->type())
        {
            case FieldDescriptor::TYPE_DOUBLE:
                size_written +=
    serialize<double>(_one_row+size_written, message, field, refl, col_index);
            break;

            case FieldDescriptor:: TYPE_FLOAT:
                size_written +=
    serialize<float>(_one_row+size_written, message, field, refl, col_index);
            break;

            case FieldDescriptor:: TYPE_INT64:
            case FieldDescriptor:: TYPE_SFIXED64:
            case FieldDescriptor:: TYPE_SINT64:
                size_written +=
    serialize<google::protobuf::int64>(_one_row+size_written, message, field, refl, col_index);
            break;

            case FieldDescriptor:: TYPE_FIXED64:
            case FieldDescriptor:: TYPE_UINT64:
                size_written +=
    serializeUInt64(_one_row+size_written, message, field, refl, col_index);
            break;

            case FieldDescriptor:: TYPE_INT32:
            case FieldDescriptor:: TYPE_SFIXED32:
            case FieldDescriptor:: TYPE_SINT32:
                size_written +=
    serialize<google::protobuf::int32>(_one_row+size_written, message, field, refl, col_index);
            break;

            case FieldDescriptor:: TYPE_FIXED32:
            case FieldDescriptor:: TYPE_UINT32:
                size_written +=
    serializeUInt32(_one_row+size_written, message, field, refl, col_index);
            break;

            case FieldDescriptor:: TYPE_BOOL:
                size_written +=
    serialize<bool>(_one_row+size_written, message, field, refl, col_index);
            break;

            case FieldDescriptor:: TYPE_ENUM:
                size_written +=
    serialize<EnumValueDescriptor>(_one_row+size_written, message, field, refl, col_index);
            break;

            case FieldDescriptor:: TYPE_STRING:
            case FieldDescriptor:: TYPE_BYTES:
                continue;
            break;

            case FieldDescriptor:: TYPE_GROUP:
                continue;
            break;

            case FieldDescriptor:: TYPE_MESSAGE:

                if (field->is_repeated())
                    throw runtime_error("repeated messages are not yet handled");

                const Message* child_message =
                &(refl->GetMessage(*message, field));

                if (field->message_type()->name() == "AnyArray")
                    size_written += serializeAnyArrayToFITS(_one_row+size_written,
                                                            child_message,
                                                            field,
                                                            child_message->GetReflection(),
                                                            col_index);
                else
                    writeMessageFields(child_message,
                                       col_index,
                                       full_name,
                                       size_written);
            break;
        }
        col_index++;
    }

}

/************************************************
 *  CLOSE
 ************************************************/
bool ProtobufOFits::close()
{
    if (!is_open()) return true;

    return OFits::close();
}


/*******************************************************************************
 *  ADD ANY ARRAY COLUMN
 *******************************************************************************/
void ProtobufOFits::addAnyArrayColumn(const Message& message,
                                      const string&  name,
                                      const string& )
{
    //retrieve the message descriptor
    const Descriptor* desc = message.GetDescriptor();

    //retrieve the fields of interest to figure out the content of the binary array
    const FieldDescriptor* type_field = desc->FindFieldByNumber(ANYARRAY_TYPE);
    const FieldDescriptor* data_field = desc->FindFieldByNumber(ANYARRAY_DATA);//FindFieldByName("data");

    const Reflection* reflection = message.GetReflection();

    //FIXME for now, we assign always the same compression
    //FIXME why is it vector here while it is a struct in OFits.h ???? How can that even compile ???
    vector<uint16_t> comp_seq;

    _total_num_columns++;
    //figure out the size of the column
    google::protobuf::int32 column_width = reflection->GetString(message, data_field).size();
    _columns_sizes.push_back(column_width);

    //replace the '.' by '_'. We cannot do that earlier as the distinction is needed between hierarchy (.) and indices (_)
    string column_name = name;
    for (auto it=column_name.begin(); it!=column_name.end(); it++)
        if ((*it) == '.' || (*it) == '#')
            *it = '_';

    //figure out the type of column to be initialized
    const EnumValueDescriptor* type = reflection->GetEnum(message, type_field);
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
        break;
    };

}

/*******************************************************************************
 *  BUILD FITS COLUMNS
 *******************************************************************************/
void ProtobufOFits::buildFitsColumns(const Message& message,
                                     const string&  name,
                                     const string&  id)
{
    // retrieve the message descriptor
    const google::protobuf::Descriptor* desc = message.GetDescriptor();

    // In case of a AnyArray, call the dedicated function
    if (desc->name() == "AnyArray")
    {
        addAnyArrayColumn(message, name, id);
        //write the column indices to the header
        ostringstream str;
        str << "TPBID" << fTable.num_cols;
        SetStr(str.str(), id, "Protobuf ID");
        return;
    }

    // Append a . to the prefix, only if it is not null
    const string prefix_name = (name=="") ? "" : name+".";
    const string prefix_id   = (id  =="") ? "" : id  +".";

    // For all fields in this message, either instantiate the appropriate
    // columns
    // or call this function recursively if it contains other messages.
    const google::protobuf::Reflection* refl = message.GetReflection();

    for (google::protobuf::int32 i=0;i<desc->field_count(); i++)
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

        vector<uint16_t> comp_seq;

        //replace the '.' by '_'. We cannot do that earlier as the distinction is needed between hierarchy (.) and indices (_)
        string column_name = full_name;
        for (auto it=column_name.begin(); it!=column_name.end(); it++)
            if ((*it) == '.' || (*it) == '#')
                *it = '_';

        google::protobuf::int32 num_items = field->is_repeated() ?
                refl->FieldSize(message,field) :
                1;

        switch (field->type())
        {
            case google::protobuf::FieldDescriptor::TYPE_MESSAGE:

                if (field->is_repeated())
                    throw runtime_error("Repeated fields are not handled yet");

                buildFitsColumns(refl->GetMessage(message, field),
                                 full_name,
                                 full_id);
                continue;
            break;

            case google::protobuf::FieldDescriptor::TYPE_DOUBLE:
                AddColumnDouble(comp_seq, num_items, column_name);
                num_items *= sizeof(double);
                break;

            case google::protobuf::FieldDescriptor::TYPE_FLOAT:
                AddColumnFloat(comp_seq, num_items, column_name);
                num_items *= sizeof(float);
                break;

            case google::protobuf::FieldDescriptor::TYPE_INT64:
            case google::protobuf::FieldDescriptor::TYPE_SFIXED64:
            case google::protobuf::FieldDescriptor::TYPE_SINT64:
                AddColumnLong(comp_seq, num_items, column_name);
                num_items *= sizeof(google::protobuf::int64);
                break;

            case google::protobuf::FieldDescriptor::TYPE_UINT64:
            case google::protobuf::FieldDescriptor::TYPE_FIXED64:
                AddColumnUnsignedLong(comp_seq, num_items, column_name);
                num_items *= sizeof(google::protobuf::uint64);
                break;

            case google::protobuf::FieldDescriptor::TYPE_INT32:
            case google::protobuf::FieldDescriptor::TYPE_SFIXED32:
            case google::protobuf::FieldDescriptor::TYPE_SINT32:
                AddColumnInt(comp_seq, num_items, column_name);
                num_items *= sizeof(google::protobuf::int32);
                break;

            case google::protobuf::FieldDescriptor::TYPE_UINT32:
            case google::protobuf::FieldDescriptor::TYPE_FIXED32:
//            cout << "Adding unsigned int for " << column_name << endl;
                AddColumnUnsignedInt(comp_seq, num_items, column_name);
                num_items *= sizeof(google::protobuf::uint32);
                break;

            case google::protobuf::FieldDescriptor::TYPE_BOOL:
                AddColumnBool(comp_seq, num_items, column_name);
                num_items *= sizeof(bool);
                break;

            case google::protobuf::FieldDescriptor::TYPE_ENUM:
                AddColumnInt(comp_seq, num_items, column_name);
                num_items *= sizeof(google::protobuf::int32);
                break;

            case google::protobuf::FieldDescriptor::TYPE_STRING:
            case google::protobuf::FieldDescriptor::TYPE_BYTES:
                cout << "WARNING: Ignoring unhandled column type for ";
                cout << full_name << endl;
                vetoField(full_name, true);
                continue;
            break;

            case google::protobuf::FieldDescriptor::TYPE_GROUP:
                cout << yellow << "WARNING: skipping field ";
                cout << full_name << " because of unhandled type....";
                cout << no_color << endl;
                vetoField(full_name, true);
                continue;
            break;

            default:
                throw runtime_error("Unkown field type");
        }; //switch type()

        //write the column indices to the header
        ostringstream str;
        str << "TPBID" << fTable.num_cols;
        SetStr(str.str(), full_id, "Protobuf ID");

        _total_num_columns++;
        _columns_sizes.push_back(num_items);

    }//for all fields
}


}; //namespace IO
}; //namespace ADH
