/**
 * @file ProtoSerialZOFits.h
 *
 * @brief Same as ProtobufZOFits, but from serialized messages instead
 *
 * Created on January 24, 2019
 *      Author: lyard
 */


#ifndef PROTOSERIALZOFITS_H_
#define PROTOSERIALZOFITS_H_

#include "ProtobufZOFits.h"

namespace ADH
{
namespace IO
{

/**
 *      @class ProtoSerialZOFits
 *      @brief writes serialized protocol buffer messages to ZFITS
 *
 */
class ProtoSerialZOFits : public ProtobufZOFits
{

    public:
    //default constructor
    ProtoSerialZOFits();

    //default destructor
    ~ProtoSerialZOFits();

    //Record of the message type beging written
    enum MessageType
    {
        UNKNOWN          = 0,
        R1_CAMERA_CONFIG = 1,
        R1_CAMERA_EVENT  = 2,
        DL0_RUN_HEADER   = 3,
        DL0_CAMERA_EVENT = 4
    };

    //move to a new table and expect a given, serialized message type
    void moveToNewTable(string tablename, string message_name);

    //write a message from its serialized version instead of structured
    void writeSerializedMessage(string& serializedMessage);

    protected:
        MessageType _message_type;
}; //class ProtoSerialZOFits

} //namespace IO
} //namespace ADH

#endif //PROTOSERIALZOFITS_H_
