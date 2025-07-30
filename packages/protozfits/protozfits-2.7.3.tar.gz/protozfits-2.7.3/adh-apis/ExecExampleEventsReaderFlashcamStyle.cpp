
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
        green+"--config"+no_color+" stream configuration. Either ZMQ stream, e.g. tcp://localhost:1234, or a filename.\n\n"
        );

    config_service.addDefaultArg("config");
    if (!config_service.parseArgument(argc, argv)) return -1;
    string str_cfg    = config_service.get<string>("config");

    // Get a reading stream of Cherenkov events
    CTA::R1::EventsStream stream("test_stream", 'r');

    // Assign its endpoint according to the command line
    stream.SetEndpoint(str_cfg);

    // Wait until an input configuration becomes available
    CTA::R1::CameraConfiguration config;
    while (!stream.BeginInputStream(config))
    {
        cout << "\rWaiting for peer to connect...";
        cout.flush();
        usleep(SLEEP_USEC_DURATION);
    }
    cout << endl;

    // Verify that the expected configuration was received
    if (config.getNumPixels() != NUM_PIXELS)
        throw runtime_error("Wrong number of pixels...");

    cout << "Got new stream with params: " << endl;
    cout << "SB ID:           " << config.getSchedulingBlockID() << endl;
    cout << "OB ID:           " << config.getObservationBlockID() << endl;
    cout << "Waveform scale:  " << config.getWaveformScale() << endl;
    cout << "Waveform offset: " << config.getWaveformOffset() << endl;

    // Read the first event of the stream (a short one)
    CTA::R1::Event event;
    stream.ReadEvent(event);

    // Verify that short event data is as expected
    if (event.getNumPixels() != NUM_PIXELS)
        throw runtime_error("Wrong event num pixels");
    if (event.getNumChannels() != NUM_CHANNELS)
        throw runtime_error("Wrong event num channels");
    if (event.getNumSamples() != NUM_SAMPLES_SHORT)
        throw runtime_error("Wrong event num samples");
    
    // Also verify the waveform data
    uint16* waveform = event.getWaveform();
    for (uint32 i=0;i<NUM_CHANNELS*NUM_PIXELS*NUM_SAMPLES_SHORT;i++)
        if (waveform[i] != i)
            throw runtime_error("Wrong sample value");

    // Look forever until end-of-stream is received or input file ends
    uint32 evt_counter = 1;   
    while (true)
    {
        cout << "\r" << "Reading evt #" << evt_counter;
        cout.flush();

        int bytes_read = stream.ReadEvent(event);

        // stop upon stream ending
        if (bytes_read == -1)
            break;

        // continue if no new data is available
        if (bytes_read == 0)
        {
            usleep(SLEEP_USEC_DURATION);
            continue;
        }

        if (event.getEventId() != evt_counter)
            throw runtime_error("Wrong event id");
        // subsequent events should be long ones. Check their waveforms
        waveform = event.getWaveform();
        for (uint32 i=0;i<NUM_CHANNELS*NUM_PIXELS*NUM_SAMPLES_LONG;i++)
            if (waveform[i] != (uint16)(i)) 
            {
                cout << endl << "we're at i=" << i << " and value is: " << waveform[i] << endl;
                throw runtime_error("Wrong later sample value");
            }

        evt_counter++;
    }

    cout << endl;

    // Release objects from streamer, e.g. threads, handles...
    stream.EndEventStream();
}
