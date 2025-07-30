/**
 * @file AnyArrayHelper.cpp
 *
 * @brief Bundle of helper function to access AnyArray objects conveniently (including the AnyArrayStreamer class)
 *
 *  Created on: Sep 3, 2014
 *      Author: lyard
 */
#include "AnyArrayHelper.h"

#include <stdexcept>

using namespace google::protobuf;
namespace ADH
{
namespace AnyArrayHelper
{

    google::protobuf::uint32 getNumElems(const AnyArray& input)
    {
        switch (input.type())
        {
            case AnyArray::S16:
            case AnyArray::U16:
                return input.data().size()/2;
                break;

            case AnyArray::S32:
            case AnyArray::U32:
            case AnyArray::FLOAT:
                return input.data().size()/4;
                break;

            case AnyArray::S64:
            case AnyArray::U64:
            case AnyArray::DOUBLE:
                return input.data().size()/8;
                break;

	        case AnyArray::S8:
            case AnyArray::U8:
            case AnyArray::NONE:
            case AnyArray::BOOL:
                return input.data().size();
                break;

            default:
                throw std::runtime_error("Unhandled data type for getting the size of a cta array");
        };
    }

    template <typename _T>
    void printToSStream(const _T* data, uint32 num_elems, ostringstream& output)
    {
          for (uint32 i=0;i<num_elems;i++)
          {
                output << data[i];
                if (i != num_elems)
                    output << ", ";
          }
    }

    std::string toString(const AnyArray& array)
    {
        ostringstream output;
        output << "[";
        switch (array.type())
        {
            case AnyArray::S16:
              printToSStream(readAs<int16>(array), getNumElems(array), output);
            break;
            case AnyArray::U16:
                printToSStream(readAs<uint16>(array), getNumElems(array), output);
            break;

            case AnyArray::S32:
                printToSStream(readAs<int32>(array), getNumElems(array), output);
            break;

            case AnyArray::U32:
                printToSStream(readAs<uint32>(array), getNumElems(array), output);
            break;

            case AnyArray::FLOAT:
                printToSStream(readAs<float>(array), getNumElems(array), output);
            break;

            case AnyArray::S64:
                printToSStream(readAs<int64>(array), getNumElems(array), output);
            break;

            case AnyArray::U64:
                printToSStream(readAs<uint64>(array), getNumElems(array), output);
            break;

            case AnyArray::DOUBLE:
                printToSStream(readAs<double>(array), getNumElems(array), output);
            break;

            case AnyArray::S8:
                printToSStream(readAs<int8>(array), getNumElems(array), output);
            break;

            case AnyArray::U8:
                printToSStream(readAs<uint8>(array), getNumElems(array), output);
            break;

            case AnyArray::NONE:
            case AnyArray::BOOL:
            default:
                throw std::runtime_error("Unhandled data type for getting the string of a cta array");

        };

        output << "]";
        return output.str();
    }

    google::protobuf::uint32 getNumBytes(const AnyArray& input)
    {
        return input.data().size();
    }

    google::protobuf::uint32 getNumElems(const AnyArray* input)
    {
        return getNumElems(*input);
    }

    google::protobuf::uint32 getNumBytes(const AnyArray* input)
    {
        return getNumBytes(*input);
    }

    std::string CTATypeString(const AnyArray::ItemType& type)
    {
        switch (type)
        {
            case AnyArray::NONE:
                return "no_type";
            case AnyArray::S8:
                return "S8";
            case AnyArray::U8:
                return "U8";
            case AnyArray::S16:
                return "S16";
            case AnyArray::U16:
                return "U16";
            case AnyArray::S32:
                return "S32";
            case AnyArray::U32:
                return "U32";
            case AnyArray::S64:
                return "S64";
            case AnyArray::U64:
                return "U64";
            case AnyArray::FLOAT:
                return "FLOAT";
            case AnyArray::DOUBLE:
                return "DOUBLE";
            case AnyArray::BOOL:
                return "BOOL";
            default:
                return "unknown_type";
        };
        return "unknown_type";
    }

    void printToScreen(const AnyArray& which)
    {
        if (which.type() == AnyArray::NONE) return;
        if (which.type() == AnyArray::S8)
        {
            const char* data = readAs<char>(which);
            for (unsigned int i=0;i<getNumElems(which);i++) cout << data[i] << " ";
            return;
        }
        if (which.type() == AnyArray::U8)
        {
            const unsigned char* data = readAs<unsigned char>(which);
            for (unsigned int i=0;i<getNumElems(which);i++) cout << (uint32)(data[i]) << " ";
            return;
        }
        if (which.type() == AnyArray::S16)
        {
            const int16* data = readAs<int16>(which);
            for (unsigned int i=0;i<getNumElems(which);i++) cout << data[i] << " ";
            return;
        }
        if (which.type() == AnyArray::U16)
        {
            const uint16* data = readAs<uint16>(which);
            for (unsigned int i=0;i<getNumElems(which);i++) cout << data[i] << " ";
            return;
        }
        if (which.type() == AnyArray::S32)
        {
            const int32* data = readAs<int32>(which);
            for (unsigned int i=0;i<getNumElems(which);i++) cout << data[i] << " ";
            return;
        }
        if (which.type() == AnyArray::U32)
        {
            const uint32* data = readAs<uint32>(which);
            for (unsigned int i=0;i<getNumElems(which);i++) cout << data[i] << " ";
            return;
        }
        if (which.type() == AnyArray::S64)
        {
            const int64* data = readAs<int64>(which);
            for (unsigned int i=0;i<getNumElems(which);i++) cout << data[i] << " ";
            return;
        }
        if (which.type() == AnyArray::U64)
        {
            const uint64* data = readAs<uint64>(which);
            for (unsigned int i=0;i<getNumElems(which);i++) cout << data[i] << " ";
            return;
        }
        if (which.type() == AnyArray::FLOAT)
        {
            const float* data = readAs<float>(which);
            for (unsigned int i=0;i<getNumElems(which);i++) cout << data[i] << " ";
            return;
        }
        if (which.type() == AnyArray::DOUBLE)
        {
            const double* data = readAs<double>(which);
            for (unsigned int i=0;i<getNumElems(which);i++) cout << data[i] << " ";
            return;
        }
        if (which.type() == AnyArray::BOOL)
        {
            const bool* data = readAs<bool>(which);
            for (unsigned int i=0;i<getNumElems(which);i++) cout << data[i] << " ";
            return;
        }

        throw std::runtime_error("Unkown type for printing to cout");
    }

}; //namespace AnyArrayHelper
}; //namespace ADH
