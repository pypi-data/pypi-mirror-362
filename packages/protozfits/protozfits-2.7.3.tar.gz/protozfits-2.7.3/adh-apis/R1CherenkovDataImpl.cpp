#include "R1CherenkovDataImpl.h"
#include "AnyArrayHelper.h"

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///                                                                         ///
//////                 CAMERA CONFIGURATION METHODS                      //////
///                                                                         ///
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

    ///////////////////////////////////////////////////////////////////////
    //   CONSTRUCTOR                                                     //
    ///////////////////////////////////////////////////////////////////////
    CTA::R1::CameraConfiguration::CameraConfiguration()
    {

    }

    ///////////////////////////////////////////////////////////////////////
    //   DESTRUCTOR                                                      //
    ///////////////////////////////////////////////////////////////////////
    CTA::R1::CameraConfiguration::~CameraConfiguration()
    {

    }

    ///////////////////////////////////////////////////////////////////////
    //   GET TEL ID                                                      //
    ///////////////////////////////////////////////////////////////////////
    uint16  CTA::R1::CameraConfiguration::getTelId() const
    {
        return proto_object.tel_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET LOCAL RUN ID                                                //
    ///////////////////////////////////////////////////////////////////////
    uint64  CTA::R1::CameraConfiguration::getLocalRunId() const
    {
        return proto_object.local_run_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CONFIG TIME                                                 //
    ///////////////////////////////////////////////////////////////////////
    CTA::LowResTimestamp CTA::R1::CameraConfiguration::getConfigTime() const
    {
        return CTA::LowResTimestamp(proto_object.config_time_s());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CAMERA CONFIG ID                                            //
    ///////////////////////////////////////////////////////////////////////
    uint64  CTA::R1::CameraConfiguration::getCameraConfigId() const
    {
        return proto_object.camera_config_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET PIXEL ID MAP                                                //
    ///////////////////////////////////////////////////////////////////////
    const uint16* CTA::R1::CameraConfiguration::getPixelIdMap() const
    {
        assert(proto_object.num_pixels() != 0);
        return ADH::AnyArrayHelper::readAs<uint16>(proto_object.pixel_id_map());
    }

    uint16* CTA::R1::CameraConfiguration::getPixelIdMap()
    {
        assert(proto_object.num_pixels() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint16>(proto_object.mutable_pixel_id_map(), 
                                                      proto_object.num_pixels());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET MODULE ID MAP                                               //
    ///////////////////////////////////////////////////////////////////////
    const uint16* CTA::R1::CameraConfiguration::getModuleIdMap() const
    {
        assert(proto_object.num_modules() != 0);
        return ADH::AnyArrayHelper::readAs<uint16>(proto_object.module_id_map());
    }

    uint16* CTA::R1::CameraConfiguration::getModuleIdMap()
    {
        assert(proto_object.num_modules() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint16>(proto_object.mutable_module_id_map(), 
                                                      proto_object.num_modules());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM PIXELS                                                  //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA::R1::CameraConfiguration::getNumPixels() const
    {
        return proto_object.num_pixels();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM MODULES                                                 //
    ///////////////////////////////////////////////////////////////////////
    uint16  CTA::R1::CameraConfiguration::getNumModules() const
    {
        return proto_object.num_modules();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    uint8 CTA::R1::CameraConfiguration::getNumChannels() const
    {
        return proto_object.num_channels();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET DATA MODEL VERSION                                          //
    ///////////////////////////////////////////////////////////////////////
    const string& CTA::R1::CameraConfiguration::getDataModelVersion() const
    {
        return proto_object.data_model_version();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CALIBRATION SERVICE ID                                      //
    ///////////////////////////////////////////////////////////////////////
    uint64 CTA::R1::CameraConfiguration::getCalibrationServiceId() const
    {
        return proto_object.calibration_service_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CALIBRATION ALGORITHM ID                                    //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA::R1::CameraConfiguration::getCalibrationAlgorithmId() const
    {
        return proto_object.calibration_algorithm_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM SAMPLES NOMINAL                                         //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA::R1::CameraConfiguration::getNumSamplesNominal() const
    {
        return proto_object.num_samples_nominal();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM SAMPLES LONG                                            //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA::R1::CameraConfiguration::getNumSamplesLong() const
    {
        return proto_object.num_samples_long();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM SAMPLES LONG                                            //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA::R1::CameraConfiguration::getSamplingFrequency() const
    {
        return 0;
    }

    ///////////////////////////////////////////////////////////////////////
    //  GET SCHEDULING BLOCK ID                                          //
    ///////////////////////////////////////////////////////////////////////
    uint64 CTA::R1::CameraConfiguration::getSchedulingBlockID() const
    {
        return datastream_object.sb_id();
    }
    ///////////////////////////////////////////////////////////////////////
    //  GET OBSERVATION BLOCK ID                                         //
    ///////////////////////////////////////////////////////////////////////
    uint64 CTA::R1::CameraConfiguration::getObservationBlockID() const
    {
        return datastream_object.obs_id();
    }
    ///////////////////////////////////////////////////////////////////////
    //  GET WAVEFORM SCALE                                               //
    ///////////////////////////////////////////////////////////////////////
    float CTA::R1::CameraConfiguration::getWaveformScale() const
    {
        return datastream_object.waveform_scale();
    }
    ///////////////////////////////////////////////////////////////////////
    //  GET WAVEFORM OFFSET                                              //
    ///////////////////////////////////////////////////////////////////////
    float CTA::R1::CameraConfiguration::getWaveformOffset() const
    {
        return datastream_object.waveform_offset();
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET LOCAL RUN ID                                                //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setLocalRunId(uint64 id)
    {
        proto_object.set_local_run_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET TEL ID                                                      //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setTelId(uint16 id)
    {
        proto_object.set_tel_id(id);
        datastream_object.set_tel_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CONFIG TIME                                                 //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setConfigTime(const CTA::LowResTimestamp &ts)
    {
        proto_object.set_config_time_s(ts);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CAMERA CONFIG ID                                            //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setCameraConfigId(uint64 id)
    {
        proto_object.set_camera_config_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM PIXELS                                                  //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setNumPixels(uint16 num_pixels)
    {
        proto_object.set_num_pixels(num_pixels);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM MODULES                                                 //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setNumModules(uint16 num_modules)
    {
        proto_object.set_num_modules(num_modules);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setNumChannels(uint8 num_channels)
    {
        proto_object.set_num_channels(num_channels);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET DATA MODEL VERSION                                          //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setDataModelVersion(const string& version)
    {
        proto_object.set_data_model_version(version);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CALIBRATION SERVICE ID                                      //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setCalibrationServiceId(uint64 id)
    {
        proto_object.set_calibration_service_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CALIBRATION ALGORITHM ID                                    //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setCalibrationAlgorithmId(uint16 id)
    {
        proto_object.set_calibration_algorithm_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM SAMPLES NOMINAL                                         //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setNumSamplesNominal(uint16 num_samples_nominal)
    {
        proto_object.set_num_samples_nominal(num_samples_nominal);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM SAMPLES LONG                                            //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setNumSamplesLong(uint16 num_samples_long)
    {
        proto_object.set_num_samples_long(num_samples_long);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET SAMPLING FREQUENCY                                          //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setSamplingFrequency(uint16 sampling_frequency)
    {
        throw runtime_error("SAMPLING FREQUENCY IS NOT PART OF DATA MODEL AND THUS NOT IMPLEMENTED");
    }

    ///////////////////////////////////////////////////////////////////////
    //  SET SCHEDULING BLOCK ID                                          //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setSchedulingBlockID(uint64 scheduling_block_id)
    {
        datastream_object.set_sb_id(scheduling_block_id);
    }

    ///////////////////////////////////////////////////////////////////////
    //  SET OBSERVATION BLOCK ID                                         //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setObservationBlockID(uint64 observation_block_id)
    {
        datastream_object.set_obs_id(observation_block_id);
    }
    ///////////////////////////////////////////////////////////////////////
    //  SET WAVEFORM SCALE                                               //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setWaveformScale(float waveform_scale)
    {
        datastream_object.set_waveform_scale(waveform_scale);
    }

    ///////////////////////////////////////////////////////////////////////
    //  SET WAVEFORM OFFSET                                              //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::CameraConfiguration::setWaveformOffset(float waveform_offset)
    {
        datastream_object.set_waveform_offset(waveform_offset);
    }

        
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///                                                                         ///
//////            EVENTS METHODS                                         //////
///                                                                         ///
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

    ///////////////////////////////////////////////////////////////////////
    //   CONSTRUCTOR                                                     //
    ///////////////////////////////////////////////////////////////////////
    CTA::R1::Event::Event()
    {

    }

    ///////////////////////////////////////////////////////////////////////
    //   DESTRUCTOR                                                      //
    ///////////////////////////////////////////////////////////////////////
    CTA::R1::Event::~Event()
    {

    }

    ///////////////////////////////////////////////////////////////////////
    //   GET EVENT ID                                                    //
    ///////////////////////////////////////////////////////////////////////
    uint64 CTA::R1::Event::getEventId() const
    {
        return proto_object.event_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET TEL ID                                                      //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA::R1::Event::getTelId() const
    {
        return proto_object.tel_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET LOCAL RUN ID                                                //
    ///////////////////////////////////////////////////////////////////////
    uint64 CTA::R1::Event::getLocalRunId() const
    {
        return proto_object.local_run_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET EVENT TYPE                                                  //
    ///////////////////////////////////////////////////////////////////////
    uint8 CTA::R1::Event::getEventType() const
    {
        return proto_object.event_type();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET EVENT TIME                                                  //
    ///////////////////////////////////////////////////////////////////////
    CTA::HighResTimestamp CTA::R1::Event::getEventTime() const
    {
        return CTA::HighResTimestamp(proto_object.event_time_s(), proto_object.event_time_qns());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA::R1::Event::getNumModules() const
    {
        return proto_object.num_modules();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    uint8 CTA::R1::Event::getNumChannels() const
    {
        return proto_object.num_channels();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM SAMPLES                                                 //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA::R1::Event::getNumSamples() const
    {
        return proto_object.num_samples();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM PIXELS                                                  //
    ///////////////////////////////////////////////////////////////////////
    uint16 CTA::R1::Event::getNumPixels() const
    {
        return proto_object.num_pixels();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET WAVEFORM                                                    //
    ///////////////////////////////////////////////////////////////////////
    const uint16* CTA::R1::Event::getWaveform() const
    {
        assert(proto_object.num_channels() != 0);
        assert(proto_object.num_samples()  != 0);
        assert(proto_object.num_pixels()   != 0);
        return ADH::AnyArrayHelper::readAs<uint16>(proto_object.waveform());
    }

    uint16* CTA::R1::Event::getWaveform()
    {
        assert(proto_object.num_channels() != 0);
        assert(proto_object.num_samples()  != 0);
        assert(proto_object.num_pixels()   != 0);
        return ADH::AnyArrayHelper::reallocAs<uint16>(proto_object.mutable_waveform(),
                                                      proto_object.num_channels()*proto_object.num_samples()*proto_object.num_pixels());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET PIXEL STATUS                                                //
    ///////////////////////////////////////////////////////////////////////
    const uint8* CTA::R1::Event::getPixelStatus() const
    {
        assert(proto_object.num_pixels() != 0);
        return ADH::AnyArrayHelper::readAs<uint8>(proto_object.pixel_status());
    }

    uint8* CTA::R1::Event::getPixelStatus()
    {
        assert(proto_object.num_pixels() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint8>(proto_object.mutable_pixel_status(),
                                                      proto_object.num_pixels());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET FIRST CELL ID                                               //
    ///////////////////////////////////////////////////////////////////////
    const uint16* CTA::R1::Event::getFirstCellId() const
    {
        assert(proto_object.num_pixels()  != 0);
        assert(proto_object.num_modules() != 0);
        return ADH::AnyArrayHelper::readAs<uint16>(proto_object.first_cell_id());
    }

    // TODO verify that the num_pixels + num_modules also leads to 
    // the size of this array for other telescopes than LST
    uint16* CTA::R1::Event::getFirstCellId()
    {
        assert(proto_object.num_pixels()  != 0);
        assert(proto_object.num_modules() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint16>(proto_object.mutable_first_cell_id(),
                                                      proto_object.num_pixels()+proto_object.num_modules()); 
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET MODULE HIRES LOCAL CLOCK COUNTER                            //
    ///////////////////////////////////////////////////////////////////////
    const uint64* CTA::R1::Event::getModuleHiresLocalClockCounter() const
    {
        assert(proto_object.num_modules() != 0);
        return ADH::AnyArrayHelper::readAs<uint64>(proto_object.module_hires_local_clock_counter());
    }

    uint64* CTA::R1::Event::getModuleHiresLocalClockCounter()
    {
        assert(proto_object.num_modules() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint64>(proto_object.mutable_module_hires_local_clock_counter(),
                                                      proto_object.num_modules());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET PEDESTAL INTENSITY                                          //
    ///////////////////////////////////////////////////////////////////////
    const float* CTA::R1::Event::getPedestalIntensity() const
    {
        assert(proto_object.num_pixels() != 0);
        return ADH::AnyArrayHelper::readAs<float>(proto_object.pedestal_intensity());
    }

    float* CTA::R1::Event::getPedestalIntensity()
    {

        assert(proto_object.num_pixels() != 0);
        return ADH::AnyArrayHelper::reallocAs<float>(proto_object.mutable_pedestal_intensity(),
                                                     proto_object.num_pixels());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CALIBRATION MONITORING ID                                   //
    ///////////////////////////////////////////////////////////////////////
    uint64 CTA::R1::Event::getCalibrationMonitoringId() const
    {
        return proto_object.calibration_monitoring_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET EVENT ID                                                    //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::Event::setEventId(uint64 id)
    {
        proto_object.set_event_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET TEL ID                                                      //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::Event::setTelId(uint16 tel_id)
    {
        proto_object.set_tel_id(tel_id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET LOCAL RUN ID                                                //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::Event::setLocalRunId(uint64 local_run_id)
    {
        proto_object.set_local_run_id(local_run_id);
    }

    ///////////////////////////////////////////////////////////////////////
    //                           CONSTRUCTOR                             //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::Event::setEventType(uint8 type)
    {
        proto_object.set_event_type(type);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET EVENT TIME                                                  //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::Event::setEventTime(const CTA::HighResTimestamp &time)
    {
        proto_object.set_event_time_s(time.s);
        proto_object.set_event_time_qns(time.qns);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM MODULES                                                 //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::Event::setNumModules(uint16 num_modules)
    {
        proto_object.set_num_modules(num_modules);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::Event::setNumChannels(uint8 num_chans)
    {
        proto_object.set_num_channels(num_chans);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM SAMPLES                                                 //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::Event::setNumSamples(uint16 num_samples)
    {
        proto_object.set_num_samples(num_samples);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM PIXELS                                                  //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::Event::setNumPixels(uint16 num_pixels)
    {
        proto_object.set_num_pixels(num_pixels);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CALIBRATION MONITORING ID                                   //
    ///////////////////////////////////////////////////////////////////////
    void CTA::R1::Event::setCalibrationMonitoringId(uint64 id)
    {
        proto_object.set_calibration_monitoring_id(id);
    }


///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
///                                                                         ///
//////               INTERNAL HELPERS SPECIALIZATION                     //////
///                                                                         ///
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

template <>
MessageType CTA::R1::getMessageEnum<CTA::R1::Event>()
{
    return R1_EVENT;
}

template<>
MessageType CTA::R1::getMessageEnum<CTA::R1::CameraConfiguration>()
{
    return TELESCOPE_DATA_STREAM;
}

