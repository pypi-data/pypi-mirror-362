/*
 * CommonZFitsUnitTests.h
 *
 *  Basic ZFits unit testing infrastructure to be used for all related tests. Inlined from source files of unit tests
 *
 *  Created on: Jan 15, 2016
 *      Author: lyard
 */




#include "ProtobufZOFits.h"
#include "ProtobufIFits.h"

#include "AnyArrayHelper.h"

#include "ProtoDataModel.pb.h"

//to be able to use remove file
#include <cstdio>

using namespace ADH::Core;
using namespace ADH::ColoredOutput;
using namespace ADH::AnyArrayHelper;
using namespace ADH::IO;
using namespace std;

uint32 g_event_number = 0;
uint32 g_num_samples  = 30;
uint32 g_num_pixels   = 2000;

//Create a new, dummy camera event
ProtoDataModel::CameraEvent* newDummyCameraEvent()
{
    ProtoDataModel::CameraEvent* event = new ProtoDataModel::CameraEvent;

    //set header data
    event->set_telescopeid(12);
    event->set_eventtype(ProtoDataModel::EventType::PHYSICAL);
    event->set_eventnumber(g_event_number++);

    //get high-gain data pointers
    event->mutable_higain()->mutable_waveforms()->set_num_samples(g_num_samples);

    //allocate data for all relevant arrays, i.e. waveforms, waveforms ids, integral gains and integral ids
    uint32 num_waveform_pixels = g_event_number % g_num_pixels;

    if (g_event_number == 1)
        num_waveform_pixels = g_num_pixels;

    uint32 num_integral_pixels = g_num_pixels - num_waveform_pixels;
    int16* raw_waveforms = reallocAs<int16>(event->mutable_higain()->mutable_waveforms()->mutable_samples(), num_waveform_pixels*g_num_samples);
    int32* raw_integrals = reallocAs<int32>(event->mutable_higain()->mutable_integrals()->mutable_gains(), num_integral_pixels);

    uint16* waveform_ids = reallocAs<uint16>(event->mutable_higain()->mutable_waveforms()->mutable_pixelsindices(), num_waveform_pixels);
    uint16* integral_ids = reallocAs<uint16>(event->mutable_higain()->mutable_integrals()->mutable_pixelsindices(), num_integral_pixels);

    //assign dummy waveform data
    for (uint32 i=0;i<num_waveform_pixels;i++)
    {
        for (uint32 j=0;j<g_num_samples;j++)
            raw_waveforms[i*g_num_samples+j] = i*g_num_samples+j;
        waveform_ids[i] = i;
    }

    //assign dummy integral data
    for (uint32 i=0;i<num_integral_pixels;i++)
    {
        raw_integrals[i] = i;
        integral_ids[i]  = i + num_waveform_pixels;
    }

    return event;
}

//verify that the given event is as expected. The value of the global variable g_event_number drives the expectations
void verifyEventData(ProtoDataModel::CameraEvent* event)
{
    if (event->telescopeid() != 12)                  throw runtime_error("Wrong telescope id");
    if (event->eventtype()   != ProtoDataModel::EventType::PHYSICAL) throw runtime_error("Wrong event type");
    if (event->eventnumber() != g_event_number++)
    {
        cout << "Got " << event->eventnumber() << " vs " << g_event_number-1 << " expected" << endl;
        throw runtime_error("Wrong event number");
    }
    if (event->higain().waveforms().num_samples() != g_num_samples) throw runtime_error("Wrong number of samples");
    uint32 num_waveform_pixels = g_event_number % g_num_pixels;

   if (g_event_number == 1)
        num_waveform_pixels = g_num_pixels;

    uint32 num_integral_pixels = g_num_pixels - num_waveform_pixels;
    const int16* raw_waveforms = readAs<int16>(event->higain().waveforms().samples());
    const int32* raw_integrals = readAs<int32>(event->higain().integrals().gains());

    if (getNumElems(event->higain().waveforms().samples()) / g_num_samples != num_waveform_pixels) throw runtime_error("Wrong number of waveform pixels");
    if (getNumElems(event->higain().waveforms().pixelsindices()) != num_waveform_pixels)           throw runtime_error("Wrong number of waveform indices");
    if (getNumElems(event->higain().integrals().gains()) != num_integral_pixels)                   throw runtime_error("Wrong number of integral pixels");
    if (getNumElems(event->higain().integrals().pixelsindices()) != num_integral_pixels)
    {
        ostringstream str;
        str << "Wrong number of integral indices... expected " << num_integral_pixels << " got " << getNumElems(event->higain().integrals().pixelsindices());
        throw runtime_error(str.str());
    }
    const uint16* waveform_ids = readAs<uint16>(event->higain().waveforms().pixelsindices());
    const uint16* integral_ids = readAs<uint16>(event->higain().integrals().pixelsindices());

    //check that the data is as expected
    for (uint32 i=0;i<num_waveform_pixels;i++)
    {
        for (uint32 j=0;j<g_num_samples;j++)
            if (raw_waveforms[i*g_num_samples+j] != (int16)(i*g_num_samples + j)) throw runtime_error("Wrong waveform data...");
        if (waveform_ids[i] != i)                                                 throw runtime_error("Wrong waveform indices data");
    }

    for (uint32 i=0;i<num_integral_pixels;i++)
    {
        if (raw_integrals[i] != (int32)(i))              throw runtime_error("Wrong integral data");
        if (integral_ids[i]  != (uint16)(i + num_waveform_pixels)) throw runtime_error("Wrong integral indices");
    }
}

/*-----------------------------------------------------------------------------------------------------------------
 * GET TEMPORARY FILENAME
 * Generates a temporary filename based on the time of day.
 *-----------------------------------------------------------------------------------------------------------------*/
inline string getTemporaryFilename()
{
    bool fileExistsAlready = true;

    ostringstream oss;

    while (fileExistsAlready)
    {
        uint64 current_time = getTimeUSec();

        oss.str("");
        oss << "./" << current_time << ".fits.fz";

        ifstream in_file(oss.str().c_str());
        if (!in_file.good())
            fileExistsAlready = false;
        else
            usleep(100000); //sleep for 0.1sec
    }

    return oss.str();
}


