#include "swat_api_config.h"

#include <arpa/inet.h>
#include <string.h>
#include "../commandline_input/ConfigService.h"

int swat_api_configure_from_file(SWAT_API_CLIENT* swat_api_h, const char* IP_address,
                                 int telnum, const char* config_filename,
                                 uint64_t sb_id, uint64_t ob_id, bool disable_worker) {
    if (swat_api_h == NULL || IP_address == NULL || config_filename == NULL) {
        return SWAT_ERR_BAD_ARG;
    }

    struct in_addr addr;
    if (inet_pton(AF_INET, IP_address, &addr) != 1) {
        return SWAT_ERR_BAD_CMDLINE;
    }
    addr.s_addr = ntohl(addr.s_addr);

    ADH::Conf::ConfigService config;
    if (strcmp(config_filename, "")) {
        if (!config.parseFile(std::string(config_filename))) {
            return SWAT_ERR_READ_FAILED;
        }
    }

    // config.printAll();
    // Calibrate the SWAT clock functionality
    swat_api_calibrate_tai(
        // The API struct (can be NULL, but this disables logging)
        swat_api_h,
        // Source clock type 0 for CLOCK_REALTIME (always available),
        // 11 for CLOCK_TAI (the kernel needs to be configured)
        CLOCK_TAI,
        // Number of leapsecs (TAI-UTC offset);
        // unused if CLOCK_TAI is selected
        config.has("SWAT", "TAI_offset") ? config.get<int>("SWAT", "TAI_offset") : 37);

    // If CLOCK_REALTIME is selected and there is no leapsecond config,
    // time calibration has failed.
    if (swat_clk_calib.clktype == CLOCK_REALTIME && swat_clk_calib.leapsecs == 0) {
        return SWAT_ERR_CANNOT_CALIBRATE;
    }

    // Configure the SWAT API struct
    return swat_api_configure(
        // The API struct
        swat_api_h,
        // The IP address as Linux in_addr struct (host byte ordering !)
        addr,
        // The TCP port number used for the communication (currently 13579 is default)
        config.has("SWAT", "Port") ? config.get<int>("SWAT", "Port") : 13579,
        // The channel number as assigned in SWAT configuration
        telnum,
        // The Scheduling Block ID of the current observation
        sb_id,
        // The Observation Block ID of the current observation
        ob_id,
        // The send flag: 0 if this client won't send triggers; 1 if it will
        config.has("SWAT", "Send_flag") ? config.get<int>("SWAT", "Send_flag") : 1,
        // The receive flag: 0 if this client shouldn't receive event requests
        // after coincidence detection, 1 if it should
        config.has("SWAT", "Receive_flag") ? config.get<int>("SWAT", "Receive_flag")
                                           : 1,
        // This flag informs SWAT the the trigger timestamps may not be fully sorted
        // when being sent (value 0) or are fully sorted by time (value 1)
        config.has("SWAT", "Sort_flag") ? config.get<int>("SWAT", "Sort_flag") : 1,
        // HW flag: 1 if the timpstamps are supplied by a hardware array trigger
        // that has multiple telescopes connected, 0 otherwise
        config.has("SWAT", "Hardware_trigger_flag")
            ? config.get<int>("SWAT", "Hardware_trigger_flag")
            : 0,
        // Timeout value in milliseconds for socket operations
        config.has("SWAT", "Net_timeout_ms") ? config.get<int>("SWAT", "Net_timeout_ms")
                                             : 2000,
        // Pointer to an integer to be used as the async stop signal;
        // if non zero will stop the api during the next operation.
        // May be NULL to disable that functionality
        NULL,
        // Pointer to the function used internally by SWAT to create a processing
        // thread for event sending and readout. Can be disabled by using
        // SWAT_API_WORKER_THR_DISABLED to preserve a single-threaded
        // environment, but in that case the function swat_api_worker(...)
        // must be called periodically to process outgoing and incoming events
        disable_worker == false ? SWAT_API_WORKER_THR_DEFAULT
                                : SWAT_API_WORKER_THR_DISABLED);

    /*
    TAI_offset              37
    Port                    13579
    Send_flag               1
    Receive_flag            1
    Sort_flag               1
    Hardware_trigger_flag   0
    Net_timeout_ms          2000
    */
}