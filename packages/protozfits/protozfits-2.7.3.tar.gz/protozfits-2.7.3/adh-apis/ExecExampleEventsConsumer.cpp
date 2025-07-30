/******************************************************************************
 *  @file ExecExampleEventsConsumer.cpp
 *
 *  @brief Example code to illustrate the usage of ADH APIs
 *             Receives event sent from ExecExampleEventsServer.cpp
 *             Does nothing with them.
 *
 *        To get support please write to Etienne.Lyard@unige.ch
 ******************************************************************************/

// Use ZMQ/protobuf wrapping
#include "ZMQStreamer.h"
// Use configuration service
#include "ConfigService.h"

// Use standard library
using namespace std;
// Use ADH configuration parser
using namespace ADH::Conf;
// Use ADH API
using namespace ADH::Core;
// Print help with color
using namespace ADH::ColoredOutput;

int main(int argc, char** argv)
{
    // Parse input parameters
    ConfigService config(
        "|------------------------------------------------------------------------------|\n"
        "|-------------------------------EVENTS CONSUMER--------------------------------|\n"
        "|---------------A Poller of events that discards all of them-------------------|\n"
        "|------------------------------------------------------------------------------|\n"
        "Required parameter:\n"+
        green + "--input" + no_color + " the zmq input streams config(s)\n"
        );

    config.addDefaultArg("input");

    if (!config.parseArgument(argc, argv)) return -1;

    vector<string> inputs = config.getVector<string>("input");

    // Create the ZMQ streamer
    ZMQStreamer consumer("Consumer", 0, true);

    // Streamers can receive messages from more than one source
    for (auto it=inputs.begin(); it!= inputs.end(); it++)
        consumer.addConnection(ZMQ_PULL, *it);

    // Get a top-level message to receive the data.
    CTAMessage message;

    // Get variables for statistics
    uint64  num_consumed = 0;
    uint64  previous_num = 0;
    uint64 start_t      = getTimeUSec();

    // Get messages forever
    while (true)
    {
        uint64 c_t = getTimeUSec();
        if (c_t - start_t > 1000000)
        {
            // Print statistics
            cout << "\rConsumed " << num_consumed << " messages";
            cout << " (" << 1000000*(num_consumed - previous_num)/(c_t-start_t) << "evts/s)" << "          ";
            previous_num = num_consumed;
            cout.flush();
            start_t = c_t;
        }

        // Stop if a signal was received
        if (consumer.wasInterrupted())
            break;

        // Do nothing if no new message was received
        if (!consumer.getNextMessage(message))
            continue;

        // Stop if end-of-stream is received
        // end-of-streams are always send as a single payload
        if (message.payload_type(0) == END_OF_STREAM)
        {
            consumer.interruptMe();
            break;
        }

        num_consumed++;
    }

    uint64 c_t = getTimeUSec();
    cout << "\rConsumed " << num_consumed << " messages";
    cout << " (" << 1000000*(num_consumed - previous_num)/(c_t-start_t) << "evts/s)" << "          ";
    cout.flush();

    cout << endl;
}
