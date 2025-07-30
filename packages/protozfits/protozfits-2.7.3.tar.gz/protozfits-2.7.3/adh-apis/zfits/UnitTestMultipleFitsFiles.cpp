/**
 * @file UnitTestMultipleFitsTables.cpp
 * @brief Unit test of protobufofits capability to write more than one table in a single file
 *
 * Creates a temporary file where two tables are created and read-back to verify its validity
 *
 *  Created on: Jan 14, 2016
 *      Author: lyard
 */

#include "CommonZFitsUnitTests.h"

#include "ProtoSerialZOFits.h"

#include "FlatProtobufZOFits.h"

uint32 target_num_events = 100;

bool verify_file_content(string filename, ProtoDataModel::CameraRunHeader* head)
{
    cout << "Verifying from " << filename << endl;
    ProtobufIFits runhead(filename.c_str(), "RunHeader");

    runhead.CheckIfFileIsConsistent(false);


    if (runhead.getNumMessagesInTable() != 1)
    {
        cout << "Wrong number of messages in table RunHeader: expected 1 while got " << runhead.getNumMessagesInTable() << endl;
        return false;
    }

    head = runhead.readTypedMessage<ProtoDataModel::CameraRunHeader>(1);

    if (head->telescopeid() != 12)
    {
        cout << "Wrong telescope id: expectd 12 while got " << head->telescopeid() << endl;
        return false;
    }

    runhead.recycleMessage(head);

    ProtobufIFits events(filename.c_str(), "Events");

    events.CheckIfFileIsConsistent(false);

    if (events.getNumMessagesInTable() != target_num_events)
    {
        cout << "Wrong number of events in table Events: expected " << target_num_events << " got " << events.getNumMessagesInTable() << endl;
        return false;
    }
    g_event_number = 0;
    for (uint32 i=1;i<=target_num_events;i++)
    {
        ProtoDataModel::CameraEvent* event = events.readTypedMessage<ProtoDataModel::CameraEvent>(i);
        if (!event)
        {
            cout << "Could not load event #" << i << ": got null instead" << endl;
            return false;
        }
        verifyEventData(event);

        events.recycleMessage(event);
    }
    return true;

}

int main(int, char**)
{
    //get a temporary filename to output and verify data
    string filename = getTemporaryFilename();

    FlatProtobufZOFits flat_output(1000,
                                     10,
                                1000000,
                                  "raw",
                                      5,
                                   1500);


    FlatProtobufZOFits flat_output2(1000,
                                     10,
                                1000000,
                                  "raw",
                                      5,
                                   1500);

    flat_output.open((filename+".flat1").c_str());
    flat_output2.open((filename+".flat2").c_str());

    flat_output.moveToNewTable("RunHeader");
    flat_output2.moveToNewTable("RunHeader");

    ProtoDataModel::CameraRunHeader* head  = new ProtoDataModel::CameraRunHeader();
    ProtoDataModel::CameraRunHeader* hebd = new ProtoDataModel::CameraRunHeader();
    head->set_telescopeid(12);
    hebd->set_telescopeid(12);
    head->set_runnumber(1);
    hebd->set_runnumber(1);
    int32 unix_date = (int32)(getTimeUSec());
    head->set_datemjd(unix_date);
    hebd->set_datemjd(unix_date);

    head->set_imgreducmode(ProtoDataModel::INTEGRATION);
    hebd->set_imgreducmode(ProtoDataModel::INTEGRATION);
    head->set_evtsreducmode(ProtoDataModel::NO_EVT_REDUC);
    hebd->set_evtsreducmode(ProtoDataModel::NO_EVT_REDUC);
    head->set_numtraces(50);
    hebd->set_numtraces(50);
    head->set_numgainchannels(1);
    hebd->set_numgainchannels(1);
    head->set_integwindowsize(50);
    hebd->set_integwindowsize(50);

    flat_output.writeMessage(hebd);
    flat_output2.writeMessage(head);

    flat_output.moveToNewTable("Events");
    flat_output2.moveToNewTable("Events");

    for (uint32 i=0;i<target_num_events;i++)
    {
        cout << "\rDoing event " << i;
        cout.flush();
        ProtoDataModel::CameraEvent* event = newDummyCameraEvent();
        ProtoDataModel::CameraEvent* other_event = new ProtoDataModel::CameraEvent;
        other_event->CopyFrom(*event);
        flat_output.writeMessage(event);
        flat_output2.writeMessage(other_event);
    }
    cout << endl;

    flat_output.close(false);
    flat_output2.close(false);

    flat_output.flush();
    flat_output2.flush();

    cout << "Verifying flat output: " << endl;
    if (!verify_file_content(filename+".flat1", head)) return -1;
    if (!verify_file_content(filename+".flat2", hebd)) return -1;

    if (remove((filename+".flat1").c_str()) || remove((filename+".flat2").c_str()))
    {
        cout << "Impossible to remove file " << filename << ".flat. abort." << endl;
        return -1;
    }

    return 0;

}

