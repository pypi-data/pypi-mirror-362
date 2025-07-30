
// Use implementation of abstract interface
#include "R1CherenkovDataImpl.h"

// Parse user input
#include "ConfigService.h"

// Standard library
using namespace std;
// ADH configuration parser 
using namespace ADH::Conf;
// Print help with color
using namespace ADH::ColoredOutput;

// Constants used in the program
#define SLEEP_USEC_DURATION (100000)
#define NUM_PIXELS          (1000)
#define NUM_CHANNELS        (1)
#define NUM_SAMPLES_SHORT   (20)
#define NUM_SAMPLES_LONG    (100)

int main(int argc, char** argv)
{

    // Parse input parameters
    ConfigService config_service(
        "|------------------------------------------------------------------------------|\n"
        "|---------------------------EXAMPLE EVENTS SERVER------------------------------|\n"
        "|------------A dummy camera server that can be used as data source-------------|\n"
        "|------------------------------------------------------------------------------|\n"
        "Required parameter: \n"+
        green+"--config"+no_color+" stream configuration. Either ZMQ stream, e.g. tcp://*:1234, or a filename.\n\n"
        "Optional parameters: \n"+
        green+"--sleep"+no_color+"  Duration in usec to sleep between two events. Default= 0.\n"+
        green+"--total"+no_color+"  Number of events to send before exiting. Default= infinite\n"
        );

    config_service.addDefaultArg("config");
    config_service.setDefaultValue("sleep", "0");
    config_service.setDefaultValue("total", "0");
    if (!config_service.parseArgument(argc, argv)) return -1;
    string str_cfg    = config_service.get<string>("config");
    uint32 sleep      = config_service.get<uint32>("sleep");
    uint64 total_evts = config_service.get<uint64>("total");

    // Get a writing stream of Cherenkov events
    CTA::R1::EventsStream stream("test_stream", 'w');

    // Assign its endpoint according to the command line
    stream.SetEndpoint(str_cfg);

    // Create a configuration and a short event
    CTA::R1::CameraConfiguration config;
    config.setNumPixels(NUM_PIXELS);
    config.setSchedulingBlockID(12345);
    config.setObservationBlockID(67890);
    config.setWaveformScale(1.1f);
    config.setWaveformOffset(10.1f);

    CTA::R1::Event event;
    event.setNumPixels(NUM_PIXELS);
    event.setNumChannels(NUM_CHANNELS);
    event.setNumSamples(NUM_SAMPLES_SHORT);
    uint16* waveform = event.getWaveform();
    for (uint32 i=0;i<NUM_CHANNELS*NUM_PIXELS*NUM_SAMPLES_SHORT;i++)
        waveform[i] = i;

    // Wait until an input configuration becomes available
    while (!stream.BeginOutputStream(config))
    {
        cout << "\r Waiting for peer to become available";
        cout.flush();
        usleep(SLEEP_USEC_DURATION);
    }
    cout << endl;

    // Write one short event
    stream.WriteEvent(event);

    // Transform the event into a long one and populate its waveform
    // Note that because of uint16, waveform values are overflowing
    event.setNumSamples(NUM_SAMPLES_LONG);
    uint16* waveform2 = event.getWaveform();
    for (uint32 i=0;i<NUM_CHANNELS*NUM_PIXELS*NUM_SAMPLES_LONG;i++)
        waveform2[i] = i;

    // Send long events either until the target number is reached, or forever
    uint32 evt_counter = 1;
    while (evt_counter!=total_evts)
    {
        event.setEventId(evt_counter);
        int bytes_written = stream.WriteEvent(event);
        if (bytes_written != 0)
        {
            if (sleep != 0)
                usleep(sleep);
            evt_counter++;
        }
    }

    // Wait 1 second for events to flush before we destroy the streams
    usleep(1000000);

    // Release objects from streamer, e.g. threads, handles...
    stream.EndEventStream();

}
