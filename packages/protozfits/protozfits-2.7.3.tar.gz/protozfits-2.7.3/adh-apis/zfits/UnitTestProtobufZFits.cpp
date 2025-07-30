/** @file UnitTestProtobufZFits.cpp
 *  @brief Unit test of protobufofits and protobufifits classes
 *
 *  Creates a temporary file where some dummy data is written and read-back to verify its validity.
 *
 *  Created on: Jan 6, 2015
 *      Author: lyard
 *
 *
 */

#include "CommonZFitsUnitTests.h"
#include "FlatProtobufZOFits.h"
#include "ProtobufIFits.h"
#include "R1v1.pb.h"
#include <ios>
#include <stdexcept>

//do the full write / read test for a given compression scheme
bool writeAndVerifyAGivenCompression(const string& filename,
                                     const string& comp_string)
{
    //reset global counter
    g_event_number = 0;
    //get a compressed FITS writer
    ProtobufZOFits output(1000,  //write 1000*10 events max.
                           10,  //group events 10 by 10
                      1000000,  //use a max. of 1GB for compression
         ProtobufZOFits::AUTO); //let the writer erase events that are given for writing

    FlatProtobufZOFits flat_output(1000,
                                100,
                            1000000,
                        comp_string,
                                 10,
                             100000);

    output.setDefaultCompression(comp_string);
    //write e.g. 951 events
    uint32 target_num_events = 353;
    output.open(filename.c_str());
    flat_output.open(string(filename+".flat").c_str());

    flat_output.moveToNewTable("DATA");

    //for all events, create dummy event and write it to disk
    for (uint32 i=0;i<target_num_events;i++)
    {
        cout << "\rDoing event " << i;
        cout.flush();
        ProtoDataModel::CameraEvent* event = newDummyCameraEvent();
        ProtoDataModel::CameraEvent* other_event = new ProtoDataModel::CameraEvent;
        other_event->CopyFrom(*event);
        output.writeMessage(event);
        flat_output.writeMessage(other_event);
    }
    //flush and close output file
    output.close(false);
    flat_output.close(true);
    flat_output.flush();

    //now let us try to read-back the data as it was written to disk
    ProtobufIFits input(filename.c_str(), "DATA");
    ProtobufIFits other_input(string(filename+".flat").c_str(), "DATA");

    //make sure that the expected number of events has been written
    if (input.getNumMessagesInTable() != target_num_events)
    {
        cout << "Wrong number of messages: " << input.getNumMessagesInTable() << " vs " << target_num_events << endl;
        return false;
    }
    g_event_number = 0;
    //for all expected events, read them back and verify their content
    for (uint32 i=1;i<=input.getNumMessagesInTable();i++)
    {
        ProtoDataModel::CameraEvent* event = input.readTypedMessage<ProtoDataModel::CameraEvent>(i);

        if (!event)
        {
            cout << "Could not load event #" << i << ": got null instead" << endl;
            return false;
        }
        verifyEventData(event);

        input.recycleMessage(event);
    }
    g_event_number = 0;
    //for all expected events, read them back and verify their content
    for (uint32 i=1;i<=input.getNumMessagesInTable();i++)
    {
        cout << "\rVerifying event " << i;
        cout.flush();
        ProtoDataModel::CameraEvent* other_event = other_input.readTypedMessage<ProtoDataModel::CameraEvent>(i);

        if (!other_event)
        {
            cout << "Could not load other event #" << i << ": got null instead" << endl;
            return false;
        }
        verifyEventData(other_event);

        other_input.recycleMessage(other_event);
    }
    //remove the newly created file
    if (remove(filename.c_str()))
    {
        cout << "Impossible to remove file " << filename << " abort." << endl;
        return false;
    }

    if (remove(string(filename+".flat").c_str()))
    {
        cout << "Impossible to remove file " << string(filename+".flat") << " abort." << endl;
        return false;
    }

    return true;
}

bool testHeaderKeys(const string& filename) {
    // RAII block for writing the test file
    {
        FlatProtobufZOFits output(1000, 100, 1000000, "zstd2", 10, 100000);
        output.open(filename.c_str());
        output.moveToNewTable("Events");

        output.setStr("MYSTR1", "Hello World");

        output.setBool("MYBOOL1", true);
        output.setBool("MYBOOL2", false);

        output.setInt("MYINT1", -1234);
        output.setInt("MYINT2", 1234567891011);

        output.setFloat("MYFLOAT1", 2.718);
        output.setFloat("MYFLOAT2", 3.14159);
        output.setFloat("MYFLOAT3", 6.626e-34);
        output.SetHierarchKeyword("CTA HIERARCH KEYWORD", "Hello World","some comment");

        // FIXME: seems we don't write valid fits files in case of empty table
        ProtoDataModel::CameraEvent* event = newDummyCameraEvent();
        output.writeMessage(event);
    }

    ProtobufIFits ifits(filename, "Events");
    if (auto result = ifits.Get<std::string>("MYSTR1") != "Hello World") {
        cout << "Error for key MYSTR1, expected 'Hello World' got '" << result << "'" << std::endl;
        return false;
    }

    if (!ifits.Get<bool>("MYBOOL1")) {
        cout << "Error for key MYBOOL1, expected true got false" << std::endl;
        return false;
    }

    if (ifits.Get<bool>("MYBOOL2")) {
        cout << "Error for key MYBOOL2, expected false got true" << std::endl;
        return false;
    }

    if (auto result = ifits.Get<int64>("MYINT1") != -1234) {
        cout << "Error for key MYINT1, expected -1234 got " << result << std::endl;
        return false;
    }

    if (auto result = ifits.Get<int64>("MYINT2") != 1234567891011) {
        cout << "Error for key MYINT1, expected 1234567891011 got " << result << std::endl;
        return false;
    }

    if (auto result = ifits.Get<double>("MYFLOAT1") != 2.718) {
        cout << "Error for key MYFLOAT1, expected 2.718 got " << result << std::endl;
        return false;
    }

    if (auto result = ifits.Get<double>("MYFLOAT2") != 3.14159) {
        cout << "Error for key MYFLOAT2, expected 3.14159 got " << result << std::endl;
        return false;
    }

    if (auto result = ifits.Get<double>("MYFLOAT3") != 6.626e-34) {
        cout << "Error for key MYFLOAT3, expected 6.626e-34 got " << result << std::endl;
        return false;
    }
    if (auto result = ifits.Get<std::string>("HIERARCH CTA HIERARCH KEYWORD") != "Hello World") {
        cout << "Error for key HIERARCH CTA HIERARCH KEYWORD, expected Hello World got " << result << std::endl;
        return false;
    }

    // Check reading back in works
    return true;
}

bool testMessageInvalidType(const string& filename) {
    // RAII block for writing the test file
    {
        FlatProtobufZOFits output(1000, 100, 1000000, "zstd2", 10, 100000);
        output.open(filename.c_str());
        output.moveToNewTable("Events");
        auto event = output.getANewMessage<R1v1::Event>();
        event->set_event_id(1);
        event->set_tel_id(1);
        output.writeMessage(event);
    }

    ProtobufIFits ifits{filename, "Events"};
    try {
        // try reading with wrong message type, should give a good error
        ifits.readTypedMessage<R1v1::CameraConfiguration>(1);
    } catch (std::runtime_error e) {
        std::string msg = e.what();
        std::string expected = "Wrong type of Message for table Events";
        if (msg != expected) {
            std::cerr << "Expected exception with message '" << expected << "', got: '" << msg << "'\n";
            return false;
        }
        return true;
    }

    std::cerr << "Expected std::runtime_error" << std::endl;
    return false;
}

int main(int , char**)
{
    //get a temporary filename to output and verify data
    string filename = getTemporaryFilename();

    //we will be using 10 compression threads, just to make things messy
    ProtobufZOFits::DefaultNumThreads(10);

    if (!testHeaderKeys(filename)) throw std::runtime_error("Header tests failed");

    if (!testMessageInvalidType(filename)) throw std::runtime_error("InvalidType test failed");

    if (!writeAndVerifyAGivenCompression(filename, "raw"))             throw runtime_error("raw compression failed");
    cout << "raw" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "fact"))            throw runtime_error("fact compression failed");
    cout << "fact" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "diffman16"))       throw runtime_error("diffman16 compression failed");
    cout << "diffman16" << endl;
//    if (!writeAndVerifyAGivenCompression(filename, "huffman16"))       throw runtime_error("huffman16 compression failed");
//    cout << "huffman16" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "doublediffman16")) throw runtime_error("doublediffman16 compression failed");
    cout << "doublediffman16" << endl;
//    if (!writeAndVerifyAGivenCompression(filename, "riceman16"))       throw runtime_error("riceman16 compression failed");
//    cout << "riceman16" << endl;
//    if (!writeAndVerifyAGivenCompression(filename, "factrice"))        throw runtime_error("factrice compression failed");
//    cout << "factrice" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "ricefact"))        throw runtime_error("ricefact compression failed");
    cout << "ricefact" << endl;
//    if (!writeAndVerifyAGivenCompression(filename, "rrice"))           throw runtime_error("rrice compression failed");
//    cout << "rrice" << endl;
//    if (!writeAndVerifyAGivenCompression(filename, "rice"))            throw runtime_error("rice compression failed");
//    cout << "rice" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "lzo"))             throw runtime_error("lzo compression failed");
    cout << "lzo" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "zrice"))           throw runtime_error("zrice compression failed");
    cout << "zrice" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "zrice32"))         throw runtime_error("zrice32 compression failed");
    cout << "zrice32" << endl;
    if (!writeAndVerifyAGivenCompression(filename, "zstd2"))         throw runtime_error("zstd compression failed");
    cout << "zstd" << endl;

 //   if (!writeAndVerifyAGivenCompression(filename, "lzorice"))         throw runtime_error("lzorice compression failed");
 //   cout << "lzorice" << endl;
//    if (!writeAndVerifyAGivenCompression(filename, "sparselossyfloats")) throw runtime_error("sparselossyfloats compression failed");
//    cout << "sparselossyfloats" << endl;

    return 0;
}
