#include "DL0CherenkovDataImpl.h"
#include "AnyArrayHelper.h"

namespace CTA
{
namespace DL0
{
    ///////////////////////////////////////////////////////////////////////
    //   CONSTRUCTOR                                                     //
    ///////////////////////////////////////////////////////////////////////
    Telescope::CameraConfiguration::CameraConfiguration()
    {

    }

    ///////////////////////////////////////////////////////////////////////
    //   DESTRUCTOR                                                      //
    ///////////////////////////////////////////////////////////////////////
    Telescope::CameraConfiguration::~CameraConfiguration()
    {

    }

    ///////////////////////////////////////////////////////////////////////
    //   GET TEL ID                                                      //
    ///////////////////////////////////////////////////////////////////////
    uint16  Telescope::CameraConfiguration::getTelId() const
    {
        return proto_object.tel_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET LOCAL RUN ID                                                //
    ///////////////////////////////////////////////////////////////////////
    uint64  Telescope::CameraConfiguration::getLocalRunId() const
    {
        return proto_object.local_run_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CONFIG TIME                                                 //
    ///////////////////////////////////////////////////////////////////////
    CTA::LowResTimestamp Telescope::CameraConfiguration::getConfigTime() const
    {
        return CTA::LowResTimestamp(proto_object.config_time_s());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CAMERA CONFIG ID                                            //
    ///////////////////////////////////////////////////////////////////////
    uint64  Telescope::CameraConfiguration::getCameraConfigId() const
    {
        return proto_object.camera_config_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET PIXEL ID MAP                                                //
    ///////////////////////////////////////////////////////////////////////
    const uint16* Telescope::CameraConfiguration::getPixelIdMap() const
    {
        assert(proto_object.num_pixels() != 0);
        return ADH::AnyArrayHelper::readAs<uint16>(proto_object.pixel_id_map());
    }

    uint16* Telescope::CameraConfiguration::getPixelIdMap()
    {
        assert(proto_object.num_pixels() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint16>(proto_object.mutable_pixel_id_map(), 
                                                      proto_object.num_pixels());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET MODULE ID MAP                                               //
    ///////////////////////////////////////////////////////////////////////
    const uint16* Telescope::CameraConfiguration::getModuleIdMap() const
    {
        assert(proto_object.num_modules() != 0);
        return ADH::AnyArrayHelper::readAs<uint16>(proto_object.module_id_map());
    }

    uint16* Telescope::CameraConfiguration::getModuleIdMap()
    {
        assert(proto_object.num_modules() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint16>(proto_object.mutable_module_id_map(), 
                                                      proto_object.num_modules());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM PIXELS                                                  //
    ///////////////////////////////////////////////////////////////////////
    uint16  Telescope::CameraConfiguration::getNumPixels() const
    {
        return proto_object.num_pixels();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM MODULES                                                 //
    ///////////////////////////////////////////////////////////////////////
    uint16  Telescope::CameraConfiguration::getNumModules() const
    {
        return proto_object.num_modules();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    uint8 Telescope::CameraConfiguration::getNumChannels() const
    {
        return proto_object.num_channels();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET DATA MODEL VERSION                                          //
    ///////////////////////////////////////////////////////////////////////
    const string& Telescope::CameraConfiguration::getDataModelVersion() const
    {
        return proto_object.data_model_version();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CALIBRATION SERVICE ID                                      //
    ///////////////////////////////////////////////////////////////////////
    uint64 Telescope::CameraConfiguration::getCalibrationServiceId() const
    {
        return proto_object.calibration_service_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CALIBRATION ALGORITHM ID                                    //
    ///////////////////////////////////////////////////////////////////////
    uint16 Telescope::CameraConfiguration::getCalibrationAlgorithmId() const
    {
        return proto_object.calibration_algorithm_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM SAMPLES NOMINAL                                         //
    ///////////////////////////////////////////////////////////////////////
    uint16 Telescope::CameraConfiguration::getNumSamplesNominal() const
    {
        return proto_object.num_samples_nominal();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM SAMPLES LONG                                            //
    ///////////////////////////////////////////////////////////////////////
    uint16 Telescope::CameraConfiguration::getNumSamplesLong() const
    {
        return proto_object.num_samples_long();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET SAMPLING FREQUENCY                                          //
    ///////////////////////////////////////////////////////////////////////
    uint16 Telescope::CameraConfiguration::getSamplingFrequency() const
    {
        return proto_object.sampling_frequency();
    }

    ///////////////////////////////////////////////////////////////////////
    //  GET SCHEDULING BLOCK ID                                          //
    ///////////////////////////////////////////////////////////////////////
    uint64 Telescope::CameraConfiguration::getSchedulingBlockID() const
    {
        return datastream_object.sb_id();
    }
    ///////////////////////////////////////////////////////////////////////
    //  GET OBSERVATION BLOCK ID                                         //
    ///////////////////////////////////////////////////////////////////////
    uint64 Telescope::CameraConfiguration::getObservationBlockID() const
    {
        return datastream_object.obs_id();
    }
    ///////////////////////////////////////////////////////////////////////
    //  GET WAVEFORM SCALE                                               //
    ///////////////////////////////////////////////////////////////////////
    float Telescope::CameraConfiguration::getWaveformScale() const
    {
        return datastream_object.waveform_scale();
    }
    ///////////////////////////////////////////////////////////////////////
    //  GET WAVEFORM OFFSET                                              //
    ///////////////////////////////////////////////////////////////////////
    float Telescope::CameraConfiguration::getWaveformOffset() const
    {
        return datastream_object.waveform_offset();
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET LOCAL RUN ID                                                //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setLocalRunId(uint64 id)
    {
        proto_object.set_local_run_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET TEL ID                                                      //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setTelId(uint16 id)
    {
        proto_object.set_tel_id(id);
        datastream_object.set_tel_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CONFIG TIME                                                 //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setConfigTime(const CTA::LowResTimestamp &ts)
    {
        proto_object.set_config_time_s(ts);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CAMERA CONFIG ID                                            //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setCameraConfigId(uint64 id)
    {
        proto_object.set_camera_config_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM PIXELS                                                  //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setNumPixels(uint16 num_pixels)
    {
        proto_object.set_num_pixels(num_pixels);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM MODULES                                                 //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setNumModules(uint16 num_modules)
    {
        proto_object.set_num_modules(num_modules);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setNumChannels(uint8 num_channels)
    {
        proto_object.set_num_channels(num_channels);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET DATA MODEL VERSION                                          //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setDataModelVersion(const string& version)
    {
        proto_object.set_data_model_version(version);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CALIBRATION SERVICE ID                                      //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setCalibrationServiceId(uint64 id)
    {
        proto_object.set_calibration_service_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CALIBRATION ALGORITHM ID                                    //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setCalibrationAlgorithmId(uint16 id)
    {
        proto_object.set_calibration_algorithm_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM SAMPLES NOMINAL                                         //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setNumSamplesNominal(uint16 num_samples_nominal)
    {
        proto_object.set_num_samples_nominal(num_samples_nominal);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM SAMPLES LONG                                            //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setNumSamplesLong(uint16 num_samples_long)
    {
        proto_object.set_num_samples_long(num_samples_long);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET SAMPLING FREQUENCY                                          //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setSamplingFrequency(uint16 sampling_frequency)
    {
        proto_object.set_sampling_frequency(sampling_frequency);
    }

    ///////////////////////////////////////////////////////////////////////
    //  SET SCHEDULING BLOCK ID                                          //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setSchedulingBlockID(uint64 scheduling_block_id)
    {
        datastream_object.set_sb_id(scheduling_block_id);
    }

    ///////////////////////////////////////////////////////////////////////
    //  SET OBSERVATION BLOCK ID                                         //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setObservationBlockID(uint64 observation_block_id)
    {
        datastream_object.set_obs_id(observation_block_id);
    }
    ///////////////////////////////////////////////////////////////////////
    //  SET WAVEFORM SCALE                                               //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setWaveformScale(float waveform_scale)
    {
        datastream_object.set_waveform_scale(waveform_scale);
    }

    ///////////////////////////////////////////////////////////////////////
    //  SET WAVEFORM OFFSET                                              //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::CameraConfiguration::setWaveformOffset(float waveform_offset)
    {
        datastream_object.set_waveform_offset(waveform_offset);
    }

    ///////////////////////////////////////////////////////////////////////
    //   CONSTRUCTOR                                                     //
    ///////////////////////////////////////////////////////////////////////
    Telescope::Event::Event(bool alloc_proto_obj) : proto_object(NULL), 
                                                    _alloc_proto_object(alloc_proto_obj),
                                                    _num_pixels(0)
    {
        if (_alloc_proto_object==true)
            proto_object = new DL0v1::Telescope::Event;
    }

    ///////////////////////////////////////////////////////////////////////
    //   DESTRUCTOR                                                      //
    ///////////////////////////////////////////////////////////////////////
    Telescope::Event::~Event()
    {
        if (_alloc_proto_object==true)
            delete proto_object;
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET EVENT ID                                                    //
    ///////////////////////////////////////////////////////////////////////
    uint64 Telescope::Event::getEventId() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        return proto_object->event_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET LOCAL RUN ID                                                //
    ///////////////////////////////////////////////////////////////////////
    uint64 Telescope::Event::getLocalRunId() const
    {
        // no local_run_id in DL0 model! Nothing here!
        return 0;
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET TEL ID                                                      //
    ///////////////////////////////////////////////////////////////////////
    uint16 Telescope::Event::getTelId() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        return proto_object->tel_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET EVENT TYPE                                                  //
    ///////////////////////////////////////////////////////////////////////
    uint8 Telescope::Event::getEventType() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        return proto_object->event_type();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET EVENT TIME                                                  //
    ///////////////////////////////////////////////////////////////////////
    CTA::HighResTimestamp Telescope::Event::getEventTime() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        return CTA::HighResTimestamp(proto_object->event_time_s(), proto_object->event_time_qns());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM MODULES                                                 //
    ///////////////////////////////////////////////////////////////////////
    uint16 Telescope::Event::getNumModules() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        return proto_object->num_modules();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    uint8 Telescope::Event::getNumChannels() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        return proto_object->num_channels();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM SAMPLES                                                 //
    ///////////////////////////////////////////////////////////////////////
    uint16 Telescope::Event::getNumSamples() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        return proto_object->num_samples();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM PIXELS SURVIVED                                         //
    ///////////////////////////////////////////////////////////////////////
    uint16 Telescope::Event::getNumPixelsSurvived() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        return proto_object->num_pixels_survived();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET NUM PIXELS                                                  //
    ///////////////////////////////////////////////////////////////////////
    uint16 Telescope::Event::getNumPixels() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        return _num_pixels;
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET WAVEFORM                                                    //
    ///////////////////////////////////////////////////////////////////////
    const uint16* Telescope::Event::getWaveform() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        assert(proto_object->num_channels()        != 0);
        assert(proto_object->num_samples()         != 0);
        assert(proto_object->num_pixels_survived() != 0);
        return ADH::AnyArrayHelper::readAs<uint16>(proto_object->waveform());
    }

    uint16* Telescope::Event::getWaveform()
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        assert(proto_object->num_channels()        != 0);
        assert(proto_object->num_samples()         != 0);
        assert(proto_object->num_pixels_survived() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint16>(proto_object->mutable_waveform(),
                                                      proto_object->num_channels()*proto_object->num_samples()*proto_object->num_pixels_survived());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET PIXEL STATUS                                                //
    ///////////////////////////////////////////////////////////////////////
    const uint8* Telescope::Event::getPixelStatus() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        assert(_num_pixels != 0);
        return ADH::AnyArrayHelper::readAs<uint8>(proto_object->pixel_status());
    }

    uint8* Telescope::Event::getPixelStatus()
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        assert(_num_pixels != 0);
        return ADH::AnyArrayHelper::reallocAs<uint8>(proto_object->mutable_pixel_status(),
                                                     _num_pixels);
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET FIRST CELL ID                                               //
    ///////////////////////////////////////////////////////////////////////
    const uint16* Telescope::Event::getFirstCellId() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        assert(proto_object->num_pixels_survived() != 0);
        assert(proto_object->num_modules() != 0);
        return ADH::AnyArrayHelper::readAs<uint16>(proto_object->first_cell_id());
    }

    uint16* Telescope::Event::getFirstCellId()
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        assert(proto_object->num_pixels_survived() != 0);
        assert(proto_object->num_modules() != 0);
        return ADH::AnyArrayHelper::reallocAs<uint16>(proto_object->mutable_first_cell_id(),
                                                      proto_object->num_pixels_survived()+proto_object->num_modules());
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET CALIBRATION MONITORING ID                                   //
    ///////////////////////////////////////////////////////////////////////
    uint64 Telescope::Event::getCalibrationMonitoringId() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        return proto_object->calibration_monitoring_id();
    }

    ///////////////////////////////////////////////////////////////////////
    //   GET PEDESTAL INTENSITY                                          //
    ///////////////////////////////////////////////////////////////////////
    const float* Telescope::Event::getPedestalIntensity() const
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        assert(proto_object->num_pixels_survived() != 0);
        return ADH::AnyArrayHelper::readAs<float>(proto_object->pedestal_intensity());
    }

    float* Telescope::Event::getPedestalIntensity()
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        assert(proto_object->num_pixels_survived() != 0);
        return ADH::AnyArrayHelper::reallocAs<float>(proto_object->mutable_pedestal_intensity(),
                                                     proto_object->num_pixels_survived());
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET EVENT ID                                                    //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::Event::setEventId(uint64 id)
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        proto_object->set_event_id(id);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET LOCAL RUN ID                                                //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::Event::setLocalRunId(uint64 id)
    {
        // no local_run_id in DL0 model! Nothing here!
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET TEL ID                                                      //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::Event::setTelId(uint16 tel_id)
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        proto_object->set_tel_id(tel_id);
    }

    ///////////////////////////////////////////////////////////////////////
    //                           CONSTRUCTOR                             //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::Event::setEventType(uint8 type)
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        proto_object->set_event_type(type);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET EVENT TIME                                                  //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::Event::setEventTime(const CTA::HighResTimestamp &time)
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        proto_object->set_event_time_s(time.s);
        proto_object->set_event_time_qns(time.qns);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM MODULES                                                 //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::Event::setNumModules(uint16 num_modules)
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        proto_object->set_num_modules(num_modules);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM CHANNELS                                                //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::Event::setNumChannels(uint8 num_chans)
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        proto_object->set_num_channels(num_chans);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM SAMPLES                                                 //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::Event::setNumSamples(uint16 num_samples)
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        proto_object->set_num_samples(num_samples);
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET NUM PIXELS SURVIVED                                         //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::Event::setNumPixelsSurvived(uint16 num_pixels_survived)
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        proto_object->set_num_pixels_survived(num_pixels_survived);
    }

    ///////////////////////////////////////////////////////////////////////
    //  SET NUM PIXELS                                                   //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::Event::setNumPixels(uint16 num_pixels)
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        _num_pixels = num_pixels;
    }

    ///////////////////////////////////////////////////////////////////////
    //   SET CALIBRATION MONITORING ID                                   //
    ///////////////////////////////////////////////////////////////////////
    void Telescope::Event::setCalibrationMonitoringId(uint64 id)
    {
        if (_alloc_proto_object==false)
            throw std::runtime_error("memory not allocated for protobuf object");
        proto_object->set_calibration_monitoring_id(id);
    }

    ///////////////////////////////////////////////////////////////////////////////
    //////               INTERNAL HELPERS SPECIALIZATION                     //////
    ///////////////////////////////////////////////////////////////////////////////
    template <>
    MessageType Telescope::getMessageEnum<DL0v1::Telescope::Event>()
    {
        return DL0_TELESCOPE_EVENT;
    }

    template<>
    MessageType Telescope::getMessageEnum<DL0v1::Telescope::CameraConfiguration>()
    {
        return DL0_TELESCOPE_CAMERA_CONFIG;
    }

};// namespace DL0
};// namespace CTA
