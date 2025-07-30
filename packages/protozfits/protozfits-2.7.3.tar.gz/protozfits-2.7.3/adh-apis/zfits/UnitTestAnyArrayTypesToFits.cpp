/*
 *  UnitTestAnyArrayTypes.cpp
 *
 *  tries out to set and readback various AnyArray types using the UnitTestAtomicTypes message
 *
 */

#include "CommonZFitsUnitTests.h"

uint32 size_of_arrays = 132;
uint32 num_iterations = 1;

template <typename _T>
_T getNextValue(_T value)
{
    return value + 1;
//    return (_T)(((float)(value)*1000.f) + size_of_arrays);
}

template <typename _T>
void fillInArray(_T seed, AnyArray* any_array)
{
    _T* array     = reallocAs<_T>(any_array, size_of_arrays);
    _T base_value = getNextValue(seed);

    for (uint32 i=0;i<size_of_arrays;i++)
    {
        array[i] = base_value;
        base_value = getNextValue(base_value);
    }
}

template <typename _T>
void verifyArray(_T seed, const AnyArray& any_array)
{
    const _T* array = readAs<_T>(any_array);

    _T base_value = getNextValue(seed);

    for (uint32 i=0;i<size_of_arrays;i++)
    {
        if (array[i] != base_value)
        {
            ostringstream ss;
            ss << "Array value (" << (int)(array[i]) << ") ";
            ss << "does not match expected one (" << (int)(base_value) << ")";
            ss << " for type " << typeid(_T).name() << " at iteration " << (int)(seed);
            throw runtime_error(ss.str());
        }
        base_value =  getNextValue(base_value);
    }
}

 int main(int, char**)
 {
    //get the basic message type
    UnitTestAtomicTypes* test_message;

    string filename = getTemporaryFilename();

    ProtobufZOFits output(num_iterations, 1, 1000000, ProtobufZOFits::RECYCLE);

    output.setDefaultCompression("raw");
    output.open(filename.c_str());

    for (uint32 i=1;i<=num_iterations;i++)
    {
        test_message = output.getANewMessage<UnitTestAtomicTypes>();

        fillInArray(  (int8)(i), test_message->mutable_int8_array());
        fillInArray( (uint8)(i), test_message->mutable_uint8_array());
        fillInArray( (int16)(i), test_message->mutable_int16_array());
        fillInArray((uint16)(i), test_message->mutable_uint16_array());
        fillInArray( (int32)(i), test_message->mutable_int32_array());
        fillInArray((uint32)(i), test_message->mutable_uint32_array());
        fillInArray( (int64)(i), test_message->mutable_int64_array());
        fillInArray((uint64)(i), test_message->mutable_uint64_array());
        fillInArray( (float)(i), test_message->mutable_float_array());
        fillInArray((double)(i), test_message->mutable_double_array());

        test_message->set_string_value("This is indeed a string value");

        output.writeMessage(test_message);
    }

    output.close();

    ProtobufIFits input(filename.c_str(), "DATA");

    for (uint32 i=1;i<=num_iterations;i++)
    {
        UnitTestAtomicTypes* test_input = input.readTypedMessage<UnitTestAtomicTypes>(i);
        verifyArray<int8>(    (int8)(i), test_input->int8_array());
        verifyArray<uint8>(  (uint8)(i), test_input->uint8_array());
        verifyArray<int16>(  (int16)(i), test_input->int16_array());
        verifyArray<uint16>((uint16)(i), test_input->uint16_array());
        verifyArray<int32>(  (int32)(i), test_input->int32_array());
        verifyArray<uint32>((uint32)(i), test_input->uint32_array());
        verifyArray<int64>(  (int64)(i), test_input->int64_array());
        verifyArray<uint64>((uint64)(i), test_input->uint64_array());
        verifyArray<float>(  (float)(i), test_input->float_array());
        verifyArray<double>((double)(i), test_input->double_array());

        const string& string_value = test_input->string_value();
        if (string_value != "This is indeed a string value")
        {
            ostringstream str;
            str << "ERROR: String value not properly written. Got: \"" << string_value << "\"";
            throw runtime_error(str.str());
        }

        input.recycleMessage(test_input);
    }

    if (remove(filename.c_str()))
    {
        cout << "Impossible to remove file " << filename << " abort." << endl;
        return -1;
    }

    return 0;
 }
