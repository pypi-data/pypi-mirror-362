#include <ios>
#include <iostream>
#include <sstream>
#include <cstdio>

#include "ProtobufIFits.h"
#include "FlatProtobufZOFits.h"
#include "R1v1.pb.h"
#include "CommonZFitsUnitTests.h"

int testHeader() {
    int failed = 0;
    std::stringstream msgs;

    // platform specific, use std::filesystem::temp_directory_path
    std::string test_file = getTemporaryFilename();

    // RAII block for the output
    {
        R1v1::Event* event = new R1v1::Event();
        event->set_event_id(1);

        FlatProtobufZOFits output(1000, 100, 1000000, "zstd2", 10, 100000);
        output.open(test_file.c_str());
        output.moveToNewTable("Events");
        output.setBool("BOOLT", true);
        output.setBool("BOOLF", false);
        output.setBool("INTEGER", 12345);
        output.setFloat("DOUBLE1", 2e-10, "A double");
        output.setFloat("DOUBLE2", 1.2345, "Another double");
        output.setFloat("DOUBLE2", 1.2345, "Another double2");
        output.setFloat("LUDBL", 9223372036854775808., "A long double");
        output.SetHierarchKeyword("CTA HIERARCH KEYWORD", "Hello World","some comment");
        output.writeMessage(event);

        output.close();
    };

    ProtobufIFits ifits(test_file.c_str(), "Events");
    auto header = ifits.GetKeys();

    {
        auto entry = header.at("DOUBLE1");
        if (entry.type != 'F') {
            failed++;
            msgs << "Key DOUBLE1: has wrong type. Expected 'F', got '" << entry.type << "'\n";
        }
        double value = entry.Get<double>();
        if (value != 2e-10) {
            failed++;
            msgs << "Key DOUBLE1: expected 2e-10 got " << value << "\n";
        }
    }

    {
        auto entry = header.at("DOUBLE2");
        if (entry.type != 'F') {
            failed++;
            msgs << "Key DOUBLE2: has wrong type. Expected 'F', got '" << entry.type << "'\n";
        }
        double value = entry.Get<double>();
        if (value != 1.2345) {
            failed++;
            msgs << "Key DOUBLE2: expected 1.2345 got " << value << "\n";
        }
    }
    
    {
        auto entry = header.at("LUDBL");
        double value = entry.Get<double>();
        if (value != 9223372036854775808ul) {
            failed++;
            msgs << "Key LUDBL: expected 9223372036854775808ul got " << value << "\n";
        } 
    }

    {    
        auto entry = header.at("HIERARCH CTA HIERARCH KEYWORD");
        if (entry.type != 'T') {
            failed++;
            msgs << "Key HIERARCH CTA HIERARCH KEYWORD: has wrong type. Expected 'T', got '" << entry.type << "'\n";
        }
        std:string value = entry.Get<std::string>();
        if (value != "Hello World") {
            failed++;
            msgs << "Key String: expected Hello World got " << value << "\n";
        }
    }

    {
        auto entry = header.at("BOOLT");
        if (entry.type != 'B') {
            failed++;
            msgs << "Key BOOLT: has wrong type. Expected 'B', got '" << entry.type << "'\n";
        }
        bool value = entry.Get<bool>();
        if (!value) {
            failed++;
            msgs << "Key BOOLT: expected true, got " << std::boolalpha << value << "\n";
        }
    }

    {
        auto entry = header.at("BOOLF");
        if (entry.type != 'B') {
            failed++;
            msgs << "Key BOOLF: has wrong type. Expected 'B', got '" << entry.type << "'\n";
        }
        bool value = entry.Get<bool>();
        if (value) {
            failed++;
            msgs << "Key BOOLF: expected false, got " << std::boolalpha << value << "\n";
        }
    }

    try {
        header.at("DOUBLE1").Get<bool>();
        failed++;
        msgs << "Trying to read key DOUBLE1 did not raise wrong_type exception\n";
    } catch (const IFits::wrong_type& e) {}

    if (failed != 0) {
        std::cerr << msgs.str() << std::endl;
    }

    return failed;
}


int main() {
    int failed = testHeader();
    if (failed != 0) {
        return -1;
    }
    return 0;
}
