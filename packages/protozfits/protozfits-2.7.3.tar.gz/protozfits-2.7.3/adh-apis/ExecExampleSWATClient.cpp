/**
 *  @file ExecExampleSWATClient.c
 *
 *  @brief An example, minimal implementation for a SWAT client that utilizes the
 * C-based API in order to send camera triggers and receive event requests
 *
 *  Created on: Jan 27, 2020
 *      Author: Muraczewski
 */

#include <commandline_input/ConfigService.h>
#include <swat/swat_api_config.h>

#include <memory.h>
#include <atomic>
#include <iostream>
#include <mutex>
#include <thread>

#include <signal.h>
#include <unistd.h>

SWAT_API_CLIENT* swat_client_h;
std::mutex cerr_mutex;
std::atomic_bool quit{false};

void writer_loop() {
    SWAT_PACKET_R1_TRIGGER camev;
    int r;
    for (unsigned int i = 0; !quit; i++) {
        // Wait until next camera trigger is available, then clear
        // the memory and copy camera trigger data to camev and send it to SWAT
        memset(&camev, 0, sizeof(camev));
        // Timestamp is provided as per the R1 high resolution standard
        // i.e. seconds (struct field: s) in TAI time scale since UNIX
        // epoch and nanosecond qurarter reminder (struct field: qns).
        // Can also be provided as plain qns since UNIX epoch in TAI
        // time scale (if assigned/constructed using an unsigned long
        // value). As an example, the current time is used.
        camev.trigger_time = swat_get_tai_time();
        // Monotonically increasing trigger ID as unsingned int
        camev.trigger_id = i;
        // Information whether data is available for readout. If set to false
        // (for instance for busy triggers) associated event request is skipped
        // regardless of detection result
        camev.data_available = true;
        // Information on the type of the trigger; affects how the trigger is
        // processed by SWAT. 4 trigger types are available:
        // * SWAT_PACKET_R1_TRIGGER_TYPE::T_0_STORE_EXCLUDE: store the event and
        //      exclude it from the detection (Flat Field, Single PE, Pedestal)
        // * SWAT_PACKET_R1_TRIGGER_TYPE::T_1_STORE_INCLUDE: include the trigger
        //      in the detection, but store the event regardless of the result
        //      (Muon candidate, LST hardware trigger)
        // * SWAT_PACKET_R1_TRIGGER_TYPE::T_2_ACADA_REQUEST: ACADA requests that
        //      the event is stored; functionally the same as type 1 (e.g. central
        //      illuminator)
        // * SWAT_PACKET_R1_TRIGGER_TYPE::T_3_SWAT_DECISION: perform a normal detection,
        //      store if coincidence is detected (shower candidate events)
        camev.trigger_type = SWAT_PACKET_R1_TRIGGER_TYPE::T_3_SWAT_DECISION;
        // Write the event structure to the API buffer
        r = swat_api_write_camera_event(swat_client_h, &camev);
        if (SWAT_OK != r) {
            std::lock_guard<std::mutex> lock(cerr_mutex);
            // Handle errors such as SWAT_ERR_BUFFER_FULL:
            // print error code & exit
            std::cerr << "Writer error: " << r << "!\n";
            quit = true;
            break;
        }

        // In the synthetic example a short wait is introduced in order
        // to not to starve the worker thread because of a mutex lock.
        // This setup generated ~30k events per second during tesitng
        if (i % 80 == 0) {
            usleep(1000);
        }
    }
    return;
}

void reader_loop() {
    SWAT_PACKET_R1_EVENT_REQUEST arrev;
    int r;
    while (!quit) {
        // Try to read the next incoming event from the API's internal buffer
        r = swat_api_read_array_event(swat_client_h, &arrev);
        if (SWAT_ERR_NO_NEW_DATA == r) {
            // No new data available; wait 50 millisec to avoid unnecessary loops
            swat_snooze();
            continue;
        } else if (SWAT_OK != r) {
            // Handle other errors: print code & exit
            std::lock_guard<std::mutex> lock(cerr_mutex);
            std::cerr << "Reader error: " << r << "!\n";
            quit = true;
            break;
        }

        // Handle each received array trigger
        if (arrev.negative_flag) {
            // Check if the trigger is negative. If true it means that triggers
            // with IDs <= arrev.requested.trigger_id or with timestamps <=
            // arrev.requested.trigger_time can be safely discarded
            // as they do not count towards an array event
            std::cout << "NEGATIVE: "
                      << "event ID: " << arrev.requested.trigger_id << ' '
                      << "timestamp: " << arrev.requested.trigger_time.s << 's' << " + "
                      << arrev.requested.trigger_time.qns << "qns" << '\n';
        } else {
            // Process an array trigger (print as an example):
            // array event ID (assigned by SWAT) in arrev.assigned_event_id
            // trigger ID in arrev.requested.trigger_id,
            // timestamp in  arrev.requested.trigger_time
            std::cout << "array event ID: " << arrev.assigned_event_id << ' '
                      << "event ID: " << arrev.requested.trigger_id << ' '
                      << "timestamp: " << arrev.requested.trigger_time.s << 's' << " + "
                      << arrev.requested.trigger_time.qns << "qns" << '\n';
        }
    }
    return;
}

void signal_loop(sigset_t sigset) {
    timespec second{1, 0};
    int sig;
    while (!quit) {
        // Watch for signals and inform other threads if SIGTERM or SIGINT is caught
        // using the quit variable
        sig = sigtimedwait(&sigset, NULL, &second);
        if (sig != -1) {
            std::lock_guard<std::mutex> lock(cerr_mutex);
            std::cerr << "Signal caught: " << sig << ".\n";
            quit = true;
            break;
        }
    }
}

int swat_client_main(std::string IP, int channel, std::string config_path) {
    int r;
    sigset_t sigset;

    // Mask signals so that masking is inherited by spawned threads
    sigemptyset(&sigset);
    sigaddset(&sigset, SIGINT);
    sigaddset(&sigset, SIGTERM);
    if (pthread_sigmask(SIG_BLOCK, &sigset, NULL) != 0) {
        swat_api_destroy(&swat_client_h);
        return (-1);
    }

    // Create and allocate the SWAT API struct
    r = swat_api_create(&swat_client_h);
    // Check the return code for errors
    if (SWAT_OK != r) {
        return (r);
    }

    // Configure the API struct using provided parameters and the config file
    r = swat_api_configure_from_file(swat_client_h, IP.c_str(), channel,
                                     config_path.c_str());
    if (SWAT_OK != r) {
        swat_api_destroy(&swat_client_h);
        return (r);
    }

    std::cerr << "Starting threads...";

    // Connect to the SWAT (start worker thread)
    r = swat_api_start(swat_client_h);
    if (SWAT_OK != r) {
        swat_api_destroy(&swat_client_h);
        return (r);
    }

    // Start reader thread
    std::thread reader_thread(reader_loop);

    // Start writer thread
    std::thread writer_thread(writer_loop);

    // Start signal watching thread
    std::thread signal_thread(signal_loop, sigset);

    {
        std::lock_guard<std::mutex> lock(cerr_mutex);
        std::cerr << " started.\n";
    }

    // There are now 5 threads executing in parallel;
    // wait until other threads which use swat_client_h terminate
    reader_thread.join();
    writer_thread.join();
    signal_thread.join();

    // terminate worker thread, unconfigure API
    r = swat_api_stop(swat_client_h);
    if (SWAT_OK != r) {
        swat_api_destroy(&swat_client_h);
        return (r);
    }

    std::cerr << "All threads joined.\n";

    // Deallocate buffers/structures
    r = swat_api_destroy(&swat_client_h);
    return (r);
}

int main(int argc, char* argv[]) {
    // This is a C++ class used to read command line parameters; the same can be
    // acheived manually or by using Linux getopt
    ADH::Conf::ConfigService config(
        "|-----------------------------------------------------------------------------"
        "|\n"
        "|--------------------------EXAMPLE SWAT API "
        "CLIENT----------------------------|\n"
        "|A dummy camera server that can be used as a trigger source and request "
        "reader|\n"
        "|-----------------------------------------------------------------------------"
        "|\n"
        "Required parameters: \n" +
        green + "--IP" + no_color +
        " IP address of the machune running the SWAT server.\n" + green + "--channel" +
        no_color +
        " The number of the SWAT channel reserved for the telescope.\n"
        "Optional parameter: \n" +
        green + "--file" + no_color +
        " Path of the SWAT API .ini configuration file.\n");
    config.setDefaultValue("file", "");
    config.addDefaultArg("IP");
    config.addDefaultArg("channel");

    try {
        if (!config.parseArgument(argc, argv)) {
            return -1;
        }
    } catch (const std::exception& e) {
        std::cerr << "Parameters' parsing exception: " << e.what() << '\n';
        return -1;
    }

    return (swat_client_main(config.getVector<std::string>("IP").front(),
                             config.get<int>("channel"),
                             config.getVector<std::string>("file").front()));
}
