/*
 * UnitTestSimultaneousReadWrite.cpp
 *
 *  Created on: Jan 14, 2016
 *      Author: lyard
 */

#include "CommonZFitsUnitTests.h"


int main(int, char**)
{
    string filename = getTemporaryFilename();

    //open a new output fits file
    ProtobufZOFits output(10,      //write 10 groups of events max.
                          10,      //put 10 events per group, total 10*10=100
                          1000000, //use max. 1M kB = 1GB of mem. for compression
             ProtobufZOFits::AUTO);   //let the object delete events

    //do not compress output data
    output.setDefaultCompression("raw");

    output.open(filename.c_str());

    //write one message at a time, and see what can be read in parallel
    for (uint32 i=0; i<100; i++)
    {
        ProtoDataModel::CameraEvent* event = newDummyCameraEvent();
        output.writeMessage(event);

        //if a tile was written to disk, wait a little bit and attempt to reload it
        if (i%10 == 0 && i!=0)
        {
            output.flushCatalog();

            int32 seconds_wait_until_tile_reloaded = 0;

            while (true)
            {
                ProtobufIFits input(filename.c_str(), "DATA");

                if (input.getNumMessagesInTable() == i)
                    break;
                else
                {
                    seconds_wait_until_tile_reloaded++;
                    sleep(1);
                    output.flushCatalog();
                }

                //wait 10 seconds max.
                if (seconds_wait_until_tile_reloaded >= 10) break;
            }

            ProtobufIFits input(filename.c_str(), "DATA");

            //check if target tile was indeed reloaded
            if (input.getNumMessagesInTable() != i)
                return -1;

            //load and verify messages from the new tile
            uint32 backup_event_num = g_event_number;

            g_event_number = g_event_number - 11;

            uint32 start = g_event_number+1;

            for (uint32 j=start;j<start+10;j++)
            {
                cout << "\rReading event #" << j << endl;
                cout.flush();
                ProtoDataModel::CameraEvent* read_event = input.readTypedMessage<ProtoDataModel::CameraEvent>(j);
                verifyEventData(read_event);
                input.recycleMessage(read_event);
            }
            g_event_number = backup_event_num;
        }
    }

    output.close(false);

    //read the last 10 events
    ProtobufIFits input(filename.c_str(), "DATA");

    if (input.getNumMessagesInTable() != 100) return -1;
    g_event_number = g_event_number - 11;
    uint32 start = g_event_number+1;
    for (uint32 j=start;j<start+11;j++)
    {
        cout << "\rReading event #" << j << endl;
        cout.flush();
        ProtoDataModel::CameraEvent* read_event = input.readTypedMessage<ProtoDataModel::CameraEvent>(j);
        verifyEventData(read_event);
        input.recycleMessage(read_event);
    }
    cout << endl;

    if (remove(filename.c_str()))
    {
        cout << "Impossible to remove file " << filename << " abort." << endl;
        return -1;
    }

    return 0;
}



