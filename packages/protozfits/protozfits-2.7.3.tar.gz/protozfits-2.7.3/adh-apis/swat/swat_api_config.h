#include "swat_api.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Configures the SWAT API using a .ini configuration file at a given path (an example
 * file SWAT_config.ini is available as a part of the repository). Internally calls
 * swat_api_calibrate_TAI(...) and swat_api_configure(...).
 * @param swat_api_h      the pointer to the API structure to be altered
 * @param IP_address      the IP address of the SWAT server to connect to
 * @param telnum          the SWAT channel number reserved for the telescope
 * @param config_fliename the path of the configuration file. Can be an empty string
 * (i.e "") to use default, programmed values
 * @param sb_id           the Scheduling Block ID of the current observation
 * @param ob_id           the Observation Block ID of the current observation
 * @param disable_worker  if true the API worker thread is disabled and the user needs
 * to periodically invoke swat_api_worker(...) to process events
 * @return                a SWAT completion code as described in the swat_errors.h
 * header
 */
int swat_api_configure_from_file(SWAT_API_CLIENT* swat_api_h, const char* IP_address,
                                 int telnum, const char* config_filename,
                                 uint64_t sb_id = 0, uint64_t ob_id = 0,
                                 bool disable_worker = false);

#ifdef __cplusplus
}
#endif