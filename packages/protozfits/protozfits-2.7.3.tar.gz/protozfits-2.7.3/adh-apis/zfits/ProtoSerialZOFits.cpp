/**
 * @file ProtoSerialZOFits.cpp
 *
 * @brief Same as ProtobufZOFits.cpp but from serialized messages
 *
 * Created on January 24, 2019
 *      Author: lyard
 */


#include "ProtoSerialZOFits.h"

#include "ProtoDataModel.pb.h"
#include "ProtoR1.pb.h"


using namespace std;

namespace ADH
{
namespace IO
{

/*******************************************************************************
 * DEFAULT CONSTRUCTOR
 *******************************************************************************/
ProtoSerialZOFits::ProtoSerialZOFits() :
                        ProtobufZOFits(1000,100)
{
    // Always use zrice: good overall performances
    setDefaultCompression("zrice");

    if (DefaultNumThreads() != 0)
    {
        cout << "Warning: you are using " << DefaultNumThreads()+1 << " threads to write data to zfits." << endl;
        cout << "Use ProtoSerialZOFits::DefaultNumThreads(0) before creating the ProtoSerialZOFits objects ";
        cout << "to get back to serial writing." << endl;
    }
}

/*******************************************************************************
 *  DEFAULT DESTRUCTOR
 *******************************************************************************/
ProtoSerialZOFits::~ProtoSerialZOFits()
{
}

/*******************************************************************************
 *  MOVE TO NEW TABLE
 *******************************************************************************/
void ProtoSerialZOFits::moveToNewTable(string tablename, string message_name)
{
    ProtobufZOFits::moveToNewTable(tablename);
    if (message_name == "R1_CAMERA_CONFIG")
    {
        _message_type = R1_CAMERA_CONFIG;
        return;
    }
    if (message_name == "R1_CAMERA_EVENT")
    {
        _message_type = R1_CAMERA_EVENT;
        return;
    }
    if (message_name == "DL0_RUN_HEADER")
    {
        _message_type = DL0_RUN_HEADER;
        return;
    }
    if (message_name == "DL0_CAMERA_EVENT")
    {
        _message_type = DL0_CAMERA_EVENT;
        return;
    }
    throw runtime_error("Unknown message type requested.\n"
                "Available types are:\n"
                "     R1_CAMERA_CONFIG\n"
                "     R1_CAMERA_EVENT\n"
                "     DL0_RUN_HEADER\n"
                "     DL0_CAMERA_EVENT\n");

}

/*******************************************************************************
 *  WRITE SERIALIZED MESSAGE
 *******************************************************************************/
void ProtoSerialZOFits::writeSerializedMessage(string& serializedMessage)
{
    google::protobuf::Message* to_be_written = NULL;
    switch (_message_type)
    {
        case R1_CAMERA_CONFIG:
            to_be_written = getANewMessage<ProtoR1::CameraConfiguration>();
        break;
        case R1_CAMERA_EVENT:
            to_be_written = getANewMessage<ProtoR1::CameraEvent>();
        break;
        case DL0_RUN_HEADER:
            to_be_written = getANewMessage<ProtoDataModel::CameraRunHeader>();
        break;
        case DL0_CAMERA_EVENT:
            to_be_written = getANewMessage<ProtoDataModel::CameraEvent>();
        break;
        case UNKNOWN:
        default:
            throw runtime_error("Unknown message type to write. You must call moveToNewTable before writing anything.");
        break;
    }
    to_be_written->ParseFromString(serializedMessage);
    writeMessage(to_be_written);
}

};//namespace IO
};//namespace ADH
