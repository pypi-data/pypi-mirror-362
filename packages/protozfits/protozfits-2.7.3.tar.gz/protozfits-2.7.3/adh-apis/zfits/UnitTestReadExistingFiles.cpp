#include "ProtobufIFits.h"
#include "ProtoR1.pb.h"
#include <cstdlib>
#include <exception>
#include <google/protobuf/message.h>
#include <iostream>
#include <memory>
#include <stdexcept>

using ADH::IO::ProtobufIFits;
using ProtoR1::CameraConfiguration;
using ProtoR1::CameraEvent;

const std::string lst_protor1_file = "LST-1.1.Run02008.0000_first50.fits.fz";

/**
 * Get the path to the test data.
 * Tries the env variable ZFITS_TEST_DATA first, if not uses
 * the path that will work in the adh-apis repo when running from
 * a build directory in base of the repository.
 */
std::string test_data_directory() {

    const char* dir = std::getenv("ZFITS_TEST_DATA");
    return dir ? dir : "../../zfits/test_files";
}

int testLSTProtoR1() {
    std::string dir = test_data_directory();
    std::string path = dir + "/" + lst_protor1_file;

    // RAII block for IFits / CameraConfig
    {
        ProtobufIFits ifits{path, "CameraConfig"};
        if (int n_rows = ifits.GetNumRows() != 1) {
            std::cerr << "Expected 1 row in table CameraConfig, got " << n_rows << std::endl;
            return 1;
        }

        auto msg = std::unique_ptr<CameraConfiguration>(ifits.readTypedMessage<CameraConfiguration>(1));


        if (int tel_id = msg->telescope_id() != 1) {
            std::cerr << "Expected telescope_id = 1, got " << tel_id << std::endl;
            return 1;
        }

        if (int configuration_id = msg->configuration_id() != 2008) {
            std::cerr << "Expected configuration_id = 2008, got " << configuration_id << std::endl;
            return 1;
        }

        if (int run_id = msg->lstcam().run_id() != 2008) {
            std::cerr << "Expected lstcam.run_id = 2008, got " << run_id << std::endl;
            return 1;
        }

        if (int num_pixels = msg->num_pixels() != 1855) {
            std::cerr << "Expected num_pixels = 1855, got " << num_pixels << std::endl;
            return 1;
        }

        if (int num_samples = msg->num_samples() != 40) {
            std::cerr << "Expected num_samples = 40, got " << num_samples << std::endl;
            return 1;
        }
    }
    
    // RAII block for IFits / Events
    {
        ProtobufIFits ifits{path, "Events"};
        int n_rows = ifits.GetNumRows();
        if (n_rows != 50) {
            std::cerr << "Expected 50 rows in table Events, got " << n_rows << std::endl;
            return 1;
        }
        for (int number=1; number <= n_rows; number++) {
            auto msg = std::unique_ptr<CameraEvent>(ifits.readTypedMessage<CameraEvent>(number));
            // four parallel streams, so we only get every fourth event. First is event_id 3
            int expected_event_id = 4 * (number - 1) + 3;
            if (msg->event_id() != expected_event_id) {
                std::cerr << "Expected event_id " << expected_event_id << " , got " << msg->event_id() << std::endl;
                return 1;
            }
        } 
    }

    return 0;
}


int testNonexistentTableThrows() {
    std::string dir = test_data_directory();
    std::string path = dir + "/" + lst_protor1_file;
    std::string expected_error = "Table ThisTableDoesNotExist could not be found in input file. Aborting.";

    // we expect this to throw an exception
    try {
        ProtobufIFits ifits{path, "ThisTableDoesNotExist"};
    } catch(std::runtime_error& e) {
        if (e.what() != expected_error) {
            std::cerr << "Error message does not match expectation. Got: '" << e.what() << "', expected '" << expected_error << "'\n";
        }
        return 0;
    }
    std::cerr << "ProtobufIFits did not throw on non-existent table" << std::endl;
    return 1;
}


int main() {
    int n_failed = 0;

    n_failed += testLSTProtoR1();
    n_failed += testNonexistentTableThrows();

    return n_failed;
}
