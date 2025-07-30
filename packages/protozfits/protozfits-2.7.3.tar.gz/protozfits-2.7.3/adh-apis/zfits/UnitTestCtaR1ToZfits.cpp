/**////////////////////////////////////////////////////////////////////////////
//       @file UnitTestCtaR1ToZfits.cpp                                      //
//       @brief Tests whether the official CTA R1 format                     //
//              can be written/read to/from ZFITS                            //
//                                                                           //
/////////////////////////////////////////////////////////////////////////////*/

#include "CommonZFitsUnitTests.h"

#include "R1v1.pb.h"

#define INTEGER_VALUE 10
#define ARRAYS_SIZE   1000

/**////////////////////////////////////////////////////////////////////////////
//                                                                           //
//       CREATE A DUMMY R1::EVENT                                            //
//                                                                           //
/////////////////////////////////////////////////////////////////////////////*/
R1v1::Event* newR1DummyEvent()
{
    R1v1::Event* event = new R1v1::Event;

    event->set_event_id(      INTEGER_VALUE+0);
    event->set_tel_id(        INTEGER_VALUE+1);
    event->set_local_run_id(  INTEGER_VALUE+2);
    event->set_event_type(    INTEGER_VALUE+3);
    event->set_event_time_s(  INTEGER_VALUE+4);
    event->set_event_time_qns(INTEGER_VALUE+5);
    event->set_num_channels(  INTEGER_VALUE+6);
    event->set_num_samples(   INTEGER_VALUE+7);
    event->set_num_pixels(    INTEGER_VALUE+8);
    event->set_num_modules(   INTEGER_VALUE+9);

    int16* waveforms     = reallocAs<int16>(event->mutable_waveform(),                         ARRAYS_SIZE);
    uint16* pix_status    = reallocAs<uint16>(event->mutable_pixel_status(),                     ARRAYS_SIZE);
    uint32* first_cell_id = reallocAs<uint32>(event->mutable_first_cell_id(),                    ARRAYS_SIZE);
    uint64* clk_counter   = reallocAs<uint64>(event->mutable_module_hires_local_clock_counter(), ARRAYS_SIZE);
    int32* ped_intensity = reallocAs<int32>(event->mutable_pedestal_intensity(),               ARRAYS_SIZE);

    for (uint32 i=0;i<ARRAYS_SIZE;i++)
    {
        waveforms[i]     = INTEGER_VALUE+i+0;
        pix_status[i]    = INTEGER_VALUE+i+1;
        first_cell_id[i] = INTEGER_VALUE+i+2;
        clk_counter[i]   = INTEGER_VALUE+i+3;
        ped_intensity[i] = INTEGER_VALUE+i+4;
    }

    event->set_calibration_monitoring_id(INTEGER_VALUE+10);

    return event;
}

/**////////////////////////////////////////////////////////////////////////////
//                                                                           //
//       VERIFY THAT THE DUMMY R1::EVENT CONTAINS THE EXPECTED VALUES        //
//                                                                           //
/////////////////////////////////////////////////////////////////////////////*/
void verifyR1EventData(const R1v1::Event* event)
{
    if (event->event_id()       != INTEGER_VALUE+0) throw runtime_error("Wrong event_id");
    if (event->tel_id()         != INTEGER_VALUE+1) throw runtime_error("Wrong tel_id");
    if (event->local_run_id()   != INTEGER_VALUE+2) throw runtime_error("Wrong local_run_id");
    if (event->event_type()     != INTEGER_VALUE+3) throw runtime_error("Wrong event_type");
    if (event->event_time_s()   != INTEGER_VALUE+4) throw runtime_error("Wrong event_time_s");
    if (event->event_time_qns() != INTEGER_VALUE+5) throw runtime_error("Wrong event_time_qns");
    if (event->num_channels()   != INTEGER_VALUE+6) throw runtime_error("Wrong num_channels");
    if (event->num_samples()    != INTEGER_VALUE+7) throw runtime_error("Wrong num_samples");
    if (event->num_pixels()     != INTEGER_VALUE+8) throw runtime_error("Wrong num_pixels");
    if (event->num_modules()    != INTEGER_VALUE+9) throw runtime_error("Wrong num_modules");

    const int16* waveforms     = readAs<int16>(event->waveform());
    const uint16* pix_status    = readAs<uint16>(event->pixel_status());
    const uint32* first_cell_id = readAs<uint32>(event->first_cell_id());
    const uint64* clk_counter   = readAs<uint64>(event->module_hires_local_clock_counter());
    const int32* ped_intensity = readAs<int32>(event->pedestal_intensity());

    for (uint32 i=0;i<ARRAYS_SIZE;i++)
    {
        if (waveforms[i]     != INTEGER_VALUE+i+0) throw runtime_error("Wrong waveform");
        if (pix_status[i]    != (uint16)(INTEGER_VALUE+i+1)) throw runtime_error("Wrong pixel_status");
        if (first_cell_id[i] != (uint32)(INTEGER_VALUE+i+2)) throw runtime_error("Wrong first_cell_id");
        if (clk_counter[i]   != (uint64)(INTEGER_VALUE+i+3)) throw runtime_error("Wrong module_hires_local_clock_counter");
        if (ped_intensity[i] != INTEGER_VALUE+i+4) throw runtime_error("Wrong pedestal intensity");
    }

    if (event->calibration_monitoring_id() != INTEGER_VALUE+10) throw runtime_error("Wrong calibration_monitoring_id");
}

/**////////////////////////////////////////////////////////////////////////////
//                                                                           //
//       CREATE A DUMMY R1::CAMERACONFIGURATION                              //                                           //
//                                                                           //
/////////////////////////////////////////////////////////////////////////////*/
R1v1::CameraConfiguration* newCameraConfiguration()
{
    R1v1::CameraConfiguration* config = new R1v1::CameraConfiguration;

    config->set_tel_id(          INTEGER_VALUE+0);
    config->set_local_run_id(    INTEGER_VALUE+1);
    config->set_config_time_s(   INTEGER_VALUE+2);
    config->set_camera_config_id(INTEGER_VALUE+4);
    
    uint16* pix_id_map = reallocAs<uint16>(config->mutable_pixel_id_map(),  ARRAYS_SIZE);
    uint16* mod_id_map = reallocAs<uint16>(config->mutable_module_id_map(), ARRAYS_SIZE);

    for (uint32 i=0;i<ARRAYS_SIZE;i++)
    {
        pix_id_map[i] = INTEGER_VALUE+i+0;
        mod_id_map[i] = INTEGER_VALUE+i+1;
    }

    config->set_num_modules(             INTEGER_VALUE+5);
    config->set_num_pixels(              INTEGER_VALUE+6);
    config->set_num_channels(            INTEGER_VALUE+7);
    config->set_data_model_version(      "TEST_VERSION");
    config->set_calibration_service_id(  INTEGER_VALUE+9);
    config->set_calibration_algorithm_id(INTEGER_VALUE+10);
    config->set_num_samples_nominal(     INTEGER_VALUE+11);
    config->set_num_samples_long(        INTEGER_VALUE+12);

    return config;
}

/**////////////////////////////////////////////////////////////////////////////
//                                                                           //
//      VERIFY THAT THE DUMMY R1::EVENT CONTAINS THE EXPECTED VALUES         //                                           //
//                                                                           //
/////////////////////////////////////////////////////////////////////////////*/
void verifyR1CameraConfiguration(const R1v1::CameraConfiguration* config)
{
    if (config->tel_id()           != INTEGER_VALUE+0) throw runtime_error("Wrong tel_id");
    if (config->local_run_id()     != INTEGER_VALUE+1) throw runtime_error("Wrong local_run_id");
    if (config->config_time_s()    != INTEGER_VALUE+2) throw runtime_error("Wrong config_time_s");
    if (config->camera_config_id() != INTEGER_VALUE+4) throw runtime_error("Wrong camera config id");
    
    const uint16* pix_id_map = readAs<uint16>(config->pixel_id_map());
    const uint16* mod_id_map = readAs<uint16>(config->module_id_map());

    for (uint32 i=0;i<ARRAYS_SIZE;i++)
    {
        if (pix_id_map[i] != INTEGER_VALUE+i+0) throw runtime_error("Wrong pix_id_map");
        if (mod_id_map[i] != INTEGER_VALUE+i+1) throw runtime_error("Wrong mod_id_map");
    }

    if (config->num_modules()              != INTEGER_VALUE+5)  throw runtime_error("Wrong num_modules");
    if (config->num_pixels()               != INTEGER_VALUE+6)  throw runtime_error("Wrong num_pixels");
    if (config->num_channels()             != INTEGER_VALUE+7)  throw runtime_error("Wrong num_channels");
    if (config->data_model_version()       != "TEST_VERSION")   throw runtime_error("Wrong data_model_version");
    if (config->calibration_service_id()   != INTEGER_VALUE+9)  throw runtime_error("Wrong calibration_service_id");
    if (config->calibration_algorithm_id() != INTEGER_VALUE+10) throw runtime_error("Wrong calibration_algorithm_id");
    if (config->num_samples_nominal()      != INTEGER_VALUE+11) throw runtime_error("Wrong num_samples_nominal");
    if (config->num_samples_long()         != INTEGER_VALUE+12) throw runtime_error("Wrong num_samples_long");
}

int main(int argc, char** argv)
{
    string filename = getTemporaryFilename();

    ProtobufZOFits::DefaultNumThreads(10);

    ProtobufZOFits output(10, 10, 1000000, ProtobufZOFits::AUTO);

    uint32 target_num_events = 100;
    output.open(filename.c_str());
    
    output.moveToNewTable("CameraConfiguration");
    output.writeMessage(newCameraConfiguration());
    output.moveToNewTable("Events");
    for (uint32 i=0;i<target_num_events;i++)
        output.writeMessage(newR1DummyEvent());
    
    output.close(false);

    ProtobufIFits input(filename.c_str(), "CameraConfiguration");

    if (input.getNumMessagesInTable() != 1)
        throw runtime_error("Header should only contain one message");

    R1v1::CameraConfiguration* config = input.readTypedMessage<R1v1::CameraConfiguration>(1);

    verifyR1CameraConfiguration(config);

    cout << "Header ok." << endl;

    input.close();
    ProtobufIFits input2(filename.c_str(), "Events");

    if (input2.getNumMessagesInTable() != target_num_events)
        throw runtime_error("DATA table contains a wrong number of events.");
    
    for (uint32 i=1;i<=input2.getNumMessagesInTable();i++)
    {
        cout << "\rVerifying event " << i;
        cout.flush();

        R1v1::Event* event = input2.readTypedMessage<R1v1::Event>(i);

        verifyR1EventData(event);
    }

    input2.close();

    cout << "\rVerified " << target_num_events << " events        " << endl;

    if (remove(filename.c_str()))
       throw runtime_error(string("Impossible to remove ")+filename);
}
