/**
 *  @file BasicDefs.cpp
 *
 *  @brief Top-level definitions needed for the ADH code
 *
 *  Created on: Oct 3, 2014
 *      Author: lyard
 */

#include "BasicDefs.h"
#include "CMakeDefs.h"
#include "ProtoDataModel.pb.h"
#include "ProtoR1.pb.h"
#include "Auxiliary.pb.h"
#include "R1v1.pb.h"
#include "DL0v1_Telescope.pb.h"

#include <sys/time.h>
#include <iostream>
#include <string>
#include <vector>
#include <sstream>
#include <ctime>
#include <stdexcept>

using namespace std;

namespace ADH
{
namespace Core
{
    //utility for easily getting current time
    //body of this utility is here, as this file should be linked with all components
    unsigned long long getTimeUSec()
    {
        struct timeval now;
        gettimeofday(&now, NULL);
        return ((unsigned long long) now.tv_sec*1000000)+now.tv_usec;
    };

    std::string bytesToString(uint64 bytes)
    {
        ostringstream str;
        str.precision(3);
        if (bytes < 1024)
            str << bytes << "B";
        else if (bytes < 1024*1024)
            str << (float)(bytes)/1024.f << "KB";
        else if (bytes < 1024*1024*1024)
            str << (float)(bytes)/(1024.f*1024.f) << "MB";
        else if (bytes < 1024ul*1024ul*1024ul*1024ul)
            str << (float)(bytes)/(1024.f*1024.f*1024.f) << "GB";
        else str << (float)(bytes)/(1024.f*1024.f*1024.f*1024.f) << "TB";

        return str.str();
    }

    /*******************************************************************************
     * EXTRACT MESSAGE TYPE
     *******************************************************************************/
    MessageType extractMessageType(const google::protobuf::Message& message)
    {
        //use reflection to figure out type
        const google::protobuf::Descriptor* descriptor = message.GetDescriptor();

        if (descriptor == R1v1::Event::descriptor())
        {
            return R1_EVENT;
        }
        else if (descriptor == R1v1::TelescopeDataStream::descriptor())
        {
            return TELESCOPE_DATA_STREAM;
        }
        else if (descriptor == R1v1::CameraConfiguration::descriptor())
        {
            return CAMERA_CONFIG;
        }
        else if (descriptor == DL0v1::Telescope::Event::descriptor())
        {
            return DL0_TELESCOPE_EVENT;
        }
        else if (descriptor == DL0v1::Telescope::DataStream::descriptor())
        {
            return DL0_TELESCOPE_DATA_STREAM;
        }
        else if (descriptor == DL0v1::Telescope::CameraConfiguration::descriptor())
        {
            return DL0_TELESCOPE_CAMERA_CONFIG;
        }
        else if (descriptor == ProtoR1::CameraEvent::descriptor())
        {
            return R1_CAMERA_EVENT;
        }
        else if (descriptor == ProtoR1::CameraConfiguration::descriptor())
        {
            return R1_CAMERA_CONFIG;
        }
        else if (descriptor == CTAMessage::descriptor())
        {
            return MESSAGE_WRAPPER;
        }
        else if (descriptor == ProtoDataModel::ArrayEvent::descriptor())
        {
            return ARRAY_EVENT;
        }
        else if (descriptor == ProtoDataModel::CameraEvent::descriptor())
        {
            return CAMERA_EVENT;
        }
        else if (descriptor == ProtoDataModel::CameraRunHeader::descriptor())
        {
            return CAMERA_RUN_HEADER;
        }
        else if (descriptor == ProtoDataModel::ArrayTrigger::descriptor())
        {
            return ARRAY_TRIGGER;
        }
        else if (descriptor == ProtoDataModel::CameraTrigger::descriptor())
        {
            return CAMERA_TRIGGER;
        }
        else if (descriptor == ProtoDataModel::PixelsChannel::descriptor())
        {
            return PIXELS_CHANNEL;
        }
        else if (descriptor == ProtoDataModel::IntegralData::descriptor())
        {
            return INTEGRAL_DATA;
        }
        else if (descriptor == ProtoDataModel::WaveFormData::descriptor())
        {
            return WAVEFORM_DATA;
        }
        else if (descriptor == AnyArray::descriptor())
        {
            return ANY_ARRAY;
        }
        else if (descriptor == ThroughputStats::descriptor())
        {
            return THROUGHPUT_STATS;
        }
        else if (descriptor == ServerAnnouncement::descriptor())
        {
            return SERVER_ANNOUNCEMENT;
        }
        else if (descriptor == AUX::DummyAuxData::descriptor())
        {
            return DUMMY_AUX_DATA;
        }

        throw runtime_error("ERROR: Could not figure out the type of this message: its type is missing in BasicDefs.cpp");

        //this point is never reached. This is here only to remove the compiler warnings
        return NO_TYPE;
    }

    /*******************************************************************************
     * EXTRACT MESSAGE TYPE
     *******************************************************************************/
    google::protobuf::Message* newMessageFromType(MessageType type)
    {
        switch (type)
        {
            case END_OF_STREAM:
                throw runtime_error("END_OF_STREAM is not (yet) a message type");
            break;
            case NO_TYPE:
                throw runtime_error("NO_TYPE is not a message type");
            break;
            case ANY_ARRAY:
                return new AnyArray();
            break;
            case TELESCOPE_DATA_STREAM:
                return new R1v1::TelescopeDataStream;
            break;
            case CAMERA_CONFIG:
                return new R1v1::CameraConfiguration;
            break;
            case R1_EVENT:
                return new R1v1::Event;
            break;
            case WAVEFORM_DATA:
                return new ProtoDataModel::WaveFormData();
            case INTEGRAL_DATA:
                return new ProtoDataModel::IntegralData();
            case PIXELS_CHANNEL:
                return new ProtoDataModel::PixelsChannel();
            case CAMERA_TRIGGER:
                return new ProtoDataModel::CameraTrigger();
            case ARRAY_TRIGGER:
                return new ProtoDataModel::ArrayTrigger();
            case CAMERA_RUN_HEADER:
                return new ProtoDataModel::CameraRunHeader();
            case CAMERA_EVENT:
                return new ProtoDataModel::CameraEvent();
            case ARRAY_EVENT:
                return new ProtoDataModel::ArrayEvent();
            case THROUGHPUT_STATS:
                return new ThroughputStats();
            case SERVER_ANNOUNCEMENT:
                return new ServerAnnouncement();
            case MESSAGE_WRAPPER:
                return new CTAMessage();
            default:
                throw runtime_error("A new message type was probably introduced: please update the BasicDefs.cpp");
        }
    }


    /*******************************************************************************
     * CONVERT TO STRING
     *******************************************************************************/
    std::string convert_to_string(MessageType type)
    {
        switch (type)
        {
            case END_OF_STREAM:
            return "END_OF_STREAM";
            break;
            case NO_TYPE:
                return "NO_TYPE";
            break;
            case ANY_ARRAY:
                return "ANY_ARRAY";
            break;
            case WAVEFORM_DATA:
                return "WAVEFORM_DATA";
            break;
            case INTEGRAL_DATA:
                return "INTEGRAL_DATA";
            break;
            case PIXELS_CHANNEL:
                return "PIXELS_CHANNEL";
            break;
            case CAMERA_TRIGGER:
                return "CAMERA_TRIGGER";
            break;
            case ARRAY_TRIGGER:
                return "ARRAY_TRIGGER";
            break;
            case CAMERA_RUN_HEADER:
                return "CAMERA_RUN_HEADER";
            break;
            case CAMERA_EVENT:
                return "CAMERA_EVENT";
            break;
            case ARRAY_EVENT:
                return "ARRAY_EVENT";
            break;
            case THROUGHPUT_STATS:
                return "THROUGHPUT_STATS";
            break;
            case SERVER_ANNOUNCEMENT:
                return "SERVER_ANNOUCEMENT";
            break;
            case MESSAGE_WRAPPER:
                return "MESSAGE_WRAPPER";
            break;
            case RAW_CAMERA_DATA:
                return "RAW_CAMERA_DATA";
            break;
            default:
                return "TYPE NOT FOUND";
                break;
        }
    }

    /*******************************************************************************
     * GET ISO BUILD TIMESTAMP
     * __DATE__ is in the form Mon d y
     *******************************************************************************/
    std::string getIsoBuildTimestamp()
    {
        if ((std::string(__DATE__).size() != 11) ||
            (std::string(__TIME__).size() != 8))
            return std::string("0000-00-00T00:00:00");

        std::string iso_timestamp="";
        
        iso_timestamp += __DATE__[7];
        iso_timestamp += __DATE__[8];
        iso_timestamp += __DATE__[9];
        iso_timestamp += __DATE__[10];
        iso_timestamp += "-";
        std::string month = "   ";
        month[0] = __DATE__[0];
        month[1] = __DATE__[1];
        month[2] = __DATE__[2];

        if (month == "Jan") iso_timestamp += "01";
        if (month == "Feb") iso_timestamp += "02";
        if (month == "Mar") iso_timestamp += "03";
        if (month == "Apr") iso_timestamp += "04";
        if (month == "May") iso_timestamp += "05";
        if (month == "Jun") iso_timestamp += "06";
        if (month == "Jul") iso_timestamp += "07";
        if (month == "Aug") iso_timestamp += "08";
        if (month == "Sep") iso_timestamp += "09";
        if (month == "Oct") iso_timestamp += "10";
        if (month == "Nov") iso_timestamp += "11";
        if (month == "Dec") iso_timestamp += "12";
        iso_timestamp += "-";
        iso_timestamp += __DATE__[4];
        iso_timestamp += __DATE__[5];
        
        iso_timestamp += "T";
        iso_timestamp += std::string(__TIME__);

        return iso_timestamp;
    }

}; //namespace Core
}; //namespace ADH
