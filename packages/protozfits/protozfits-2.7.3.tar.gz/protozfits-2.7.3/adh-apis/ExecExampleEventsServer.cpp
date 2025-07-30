/******************************************************************************
 * @file ExecExampleEventsServer.cpp
 *
 * @brief Example code to illustrate the usage of ADH APIs
 *            Create dummy R1 events and send them to ADH
 *            This is the code to be used by the camera servers
 *
 *        To get support please write to Etienne.Lyard@unige.ch
 *****************************************************************************/

// ZMQ/protobuf wrapping
#include "ZMQStreamer.h"
// R1 data model
#include "R1v1.pb.h"
// Optimized low-level arrays in protobuf messages
#include "AnyArrayHelper.h"
// Basic ADH definitions, e.g. explicit types like int16
#include "BasicDefs.h"
// Configuration service
#include "ConfigService.h"
// usleep
#include <unistd.h>

// ADH API
using namespace ADH::Core;
// Standard library
using namespace std;
// ADH configuration parser 
using namespace ADH::Conf;
// Print help with color
using namespace ADH::ColoredOutput;

// Assume 100 pre-allocated events slots in memory and a random camera 
#define NUM_PREALLOCATED_EVENTS  (100)
#define NUM_PIXELS              (2021)
#define NUM_WAVEFORM_SAMPLES      (40)

// We need pointers to keep track of pre-allocated protobufs' memory.
// The memory will be released by the protobuf themselves
R1v1::Event* events_data[NUM_PREALLOCATED_EVENTS];
uint16*    waveforms_data[NUM_PREALLOCATED_EVENTS];

int main(int argc, char** argv)
{
    // Parse input parameters
    ConfigService config(
        "|------------------------------------------------------------------------------|\n"
        "|---------------------------EXAMPLE EVENTS SERVER------------------------------|\n"
        "|------------A dummy camera server that can be used as data source-------------|\n"
        "|------------------------------------------------------------------------------|\n"
        "Required parameter: \n"+
        green+"--port"+no_color+" port number to bind to.\n\n"
        "Optional parameters: \n"+
        green+"--sleep"+no_color+"  Duration in usec to sleep between two events. Default= 0.\n"+
        green+"--total"+no_color+"  Number of events to send before exiting. Default= infinite\n"
        );

    config.addDefaultArg("port");
    config.setDefaultValue("sleep", "0");
    config.setDefaultValue("total", "0");

    if (!config.parseArgument(argc, argv)) return -1;

    uint32 port       = config.get<uint32>("port");
    uint32 sleep      = config.get<uint32>("sleep");
    uint64 total_evts = config.get<uint64>("total");

    // Create a ZMQ streamer that:
    //      - is named
    //      - has 0 extra sender threads
    //      - will stop upon receiving an interrupt signal
    //      - does not forward the events it receives (it will send, not receive anyway) 
    ZMQStreamer streamer("EventsProducer", 0, true);

    // Bind to the output port
    streamer.addOutputStream(port);

    // Allocate source events memory
    // Waveform pointers must be acquired from the protobuf itself, not the other way around
    for (uint32 i=0;i<NUM_PREALLOCATED_EVENTS;i++)
    {
        events_data[i]    = new R1v1::Event;
        waveforms_data[i] = ADH::AnyArrayHelper::reallocAs<uint16>(events_data[i]->mutable_waveform(), NUM_PIXELS*NUM_WAVEFORM_SAMPLES);
    }

    // Populate events data that will remain static
    for (uint32 i=0;i<NUM_PREALLOCATED_EVENTS;i++)
    {
        events_data[i]->set_tel_id(12);
        events_data[i]->set_num_channels(1);
        events_data[i]->set_num_samples(NUM_WAVEFORM_SAMPLES);
        events_data[i]->set_num_pixels(NUM_PIXELS);
    }

    // Also create messages for homekeeping
    R1v1::TelescopeDataStream stream_metadata;
    R1v1::CameraConfiguration camera_config;

    // Populate homekeeping messages. 
    // Note: not all fields are used in this example
    stream_metadata.set_tel_id(23);
    stream_metadata.set_sb_id(12345678);
    stream_metadata.set_obs_id(87654321);

    camera_config.set_tel_id(23);
    camera_config.set_local_run_id(12345);

    // Send metadata
    streamer.sendMessage(stream_metadata);
    streamer.sendMessage(camera_config);

    //sleep 1 second for the user to see the metadata arrive
    usleep(1000000);

    // Make event number grow with time
    int32 event_number = 0;
    // Remember which pre-allocated event we will use next
    int32 event_slot   = 0;
    // Pointers to the event being sent
    R1v1::Event* this_evt      = NULL;
    uint16*    this_waveform = NULL;

    // Execute main sender loop
    for (uint32 nevt=0;nevt<total_evts || total_evts==0;nevt++)
    {
        // Get pointers to current event being dealt with
        this_evt      = events_data[event_slot];
        this_waveform = waveforms_data[event_slot];
        
        // Increment event slot
        event_slot = (event_slot+1)%NUM_PREALLOCATED_EVENTS;

        // Assign dummy data to current event
        // This is most likely done asynchronously in the camera server
        this_evt->set_event_id(event_number++);
        for (uint32 pix=0;pix<NUM_PIXELS;pix++)
            for (uint32 wave=0;wave<NUM_WAVEFORM_SAMPLES;wave++)
                this_waveform[pix*NUM_WAVEFORM_SAMPLES+wave] = (event_number+pix+wave)%4096;

        // Send the event
        streamer.sendMessage(*this_evt);

        // Sleep if needed
        if (sleep != 0)
            usleep(sleep);

        // Stop if a signal was received
        if (streamer.wasInterrupted())
            break;
    }

    // Let the receiving end know that this stream has ended
    streamer.sendEOS();

    // Free allocated memory
    for (uint32 i=0;i<NUM_PREALLOCATED_EVENTS;i++)
        delete events_data[i];

    cout << endl;
}
