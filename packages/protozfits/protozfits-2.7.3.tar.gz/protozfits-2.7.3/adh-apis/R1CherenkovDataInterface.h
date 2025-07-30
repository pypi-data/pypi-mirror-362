/**
    @file R1CherenkovDataInterface.h

    @brief Abstraction of the interface between ACADA and Cherenkov camera raw data
*/

#ifndef R1CHERENKOVDATAINTERFACE_H_
#define R1CHERENKOVDATAINTERFACE_H_

#include <cstdint>
#include <string>
#include "timestamp.h"

/**
    @namespace CTA
    @brief define all the structures that are to be used mostly everywhere.
*/

namespace CTA
{
namespace R1
{
    /**
        @struct AbstractCameraConfiguration
        @brief  Abstract definition of the camera configuration and telescope data stream R1 data model
        We merged TelescopeDataStream and CameraConfiguration in a single class here for simplicity
    */
    class AbstractCameraConfiguration
    {
        public:
            /**
                @brief Default constructor. Creates an empty camera configuration
            */
            AbstractCameraConfiguration() {};

            /**
                @brief Default destructor. Releases all allocated memory
            */
            virtual ~AbstractCameraConfiguration() {};

            /**
                @brief Retrieve the telescope ID, called tel_id in data model
            */
            virtual uint16_t getTelId() const = 0;

            /**
                @brief Retrieve the local run id, called local_run_id in data model
            */
            virtual uint64_t getLocalRunId() const = 0;

            /**
                @brief Retrieve the configuration time, called config_time in data model
            */
            virtual LowResTimestamp getConfigTime() const = 0;

            /**
                @brief Retrieve the camera configuration id, called camera_config_id in data model
            */
            virtual uint64_t getCameraConfigId() const = 0;

            /**
                @brief Retrieve the pixel id map, called pixel_id_map in data model. 
                Memory allocation performed on-the-fly, according to previously set field
                num_pixels. Memory is reallocated only if the number of pixels changes, and 
                upon querying this method again.
            */
            virtual uint16_t* getPixelIdMap() = 0;
            virtual const uint16_t* getPixelIdMap() const = 0;

            /**
                @brief Retrieve the module id map, called module_id_map in data model.
                Memory allocation performed on-the-fly, according to previously set field
                num_modules. Memory is reallocated only if the number of pixels changes, and 
                upon querying this method again.
            */
            virtual uint16_t* getModuleIdMap() = 0;
            virtual const uint16_t* getModuleIdMap() const = 0;

            /**
                @brief Retrieve the number of pixels, called num_pixels in data model.
            */
            virtual uint16_t getNumPixels() const = 0;

            /**
                @brief Retrieve the number of modules, called num_modules in data model
            */
            virtual uint16_t getNumModules() const = 0;

            /**
                @brief Retrieve the number of channels, called num_channels in data model
            */
            virtual uint8_t getNumChannels() const = 0;

            /**
                @brief Retrieve the data model version string, called data_model_version in data model
            */
            virtual const std::string& getDataModelVersion() const = 0;

            /**
                @brief Retrieve the calibration service id, called calibration_service_id in data model
            */
            virtual uint64_t getCalibrationServiceId() const = 0;

            /**
                @brief Retrieve the calibration algorithm id, called calibration_algorithm_id in data model
            */
            virtual uint16_t getCalibrationAlgorithmId() const = 0;

            /**
                @brief Retrieve the nominal number of samples, called num_samples_nominal in data model
            */
            virtual uint16_t getNumSamplesNominal() const = 0;

            /**
                @brief Retrieve the long number of samples, called num_samples_long in data model
            */
            virtual uint16_t getNumSamplesLong() const = 0;

            /**
                @brief Retrieve the sampling frequency, not defined in R1 data model but added for convenience
            */
            virtual uint16_t getSamplingFrequency() const = 0;

            /**
                @brief Retrieve the scheduling block id
            */
            virtual uint64_t getSchedulingBlockID() const = 0;

            /**
                @brief Retrieve the observation block id
            */
            virtual uint64_t getObservationBlockID() const = 0;

            /**
                @brief Retrieve the scheduling block id
            */
            virtual float getWaveformScale() const = 0;

            /**
                @brief Retrieve the scheduling block id
            */
            virtual float getWaveformOffset() const = 0;

            /**
                @brief Set the local run id, called local_run_id in data model
            */
            virtual void setLocalRunId(uint64_t id) = 0;

            /**
                @brief Set the telescope id, called tel_id in data model
            */
            virtual void setTelId(uint16_t id) = 0;

            /**
                @brief Set the configuration time, called config_time in data model
            */
            virtual void setConfigTime(const LowResTimestamp &ts) = 0;

            /**
                @brief Set the camera configuration id, called camera_config_id in data model
            */
            virtual void setCameraConfigId(uint64_t id) = 0;

            /**
                @brief Set the number of pixels, called num_pixels in data model
            */
            virtual void setNumPixels(uint16_t num_pixels) = 0;

            /**
                @brief Set the number of modules, called num_modules in data model
            */
            virtual void setNumModules(uint16_t num_modules) = 0;

            /**
                @brief Set the number of channels, called num_channels in data model
            */
            virtual void setNumChannels(uint8_t num_channels) = 0;

            /**
                @brief Set the data model version, called data_model_version in data model
            */
            virtual void setDataModelVersion(const std::string& version) = 0;

            /**
                @brief Set the calibration service id, called calibration_service_id in data model
            */
            virtual void setCalibrationServiceId(uint64_t id) = 0;

            /**
                @brief Set the calibration algorithm id, called calibration_algorithm_id in data model
            */
            virtual void setCalibrationAlgorithmId(uint16_t id) = 0;

            /**
                @brief Set the nominal number of samples, called num_samples_nominal in data model
            */
            virtual void setNumSamplesNominal(uint16_t num_samples_nominal) = 0;

            /**
                @brief Set the long number of samples, called num_samples_nominal in data model
            */
            virtual void setNumSamplesLong(uint16_t num_samples_long) = 0;

            /**
                @brief Set the sampling frequency, not defined in R1 data model but added for convenience
            */
            virtual void setSamplingFrequency(uint16_t sampling_frequency) = 0;

            /**
                @brief Set the scheduling block id
            */
            virtual void setSchedulingBlockID(uint64_t scheduling_block_id) = 0;

            /**
                @brief Set the observation block id
            */
            virtual void setObservationBlockID(uint64_t observation_block_id) = 0;

            /**
                @brief Set the scheduling block id
            */
            virtual void setWaveformScale(float waveform_scale) = 0;

            /**
                @brief Set the scheduling block id
            */
            virtual void setWaveformOffset(float waveform_offset) = 0;

    };

    /**
        @class AbstractEvent
        @brief Abstract definition of the R1 Event data model
    */
    class AbstractEvent
    {
        public:
            /**
                @brief Default constructor. Does nothing.
            */
            AbstractEvent() {};

            /**
                @brief Default destructor. Does nothing
            */
            virtual ~AbstractEvent() {};

            /**
                @brief Retrieve the event id. Called event_id in the data model.
            */
            virtual uint64_t getEventId() const = 0;

            /**
                @brief Retrieve the telescope id. Called tel_id in the data model.
            */
            virtual uint16_t getTelId() const = 0;

            /**
                @brief Retrieve the local run id. Called local_run_id in the data model.
            */
            virtual uint64_t getLocalRunId() const = 0;

            /**
                @brief Retrieve the event type. Called event_type in the data model
            */
            virtual uint8_t getEventType() const = 0;

            /**
                @brief Retrieve the event time. Called event_time in the data model
            */
            virtual CTA::HighResTimestamp getEventTime() const = 0;

            /**
                @brief Retrieve the number of modules, called num_modules in data model
            */
            virtual uint16_t getNumModules() const = 0;

            /**
                @brief Retrieve the number of channels. Called num_channels in the data model.
            */
            virtual uint8_t getNumChannels() const = 0;

            /**
                @brief Retrieve the number of samples. Called num_samples in the data model.
            */
            virtual uint16_t getNumSamples() const = 0;

            /**
                @brief Retrieve the number of pixels. Called num_pixels in the data model.
            */
            virtual uint16_t getNumPixels() const = 0;

            /**
                @brief Retrieve the waveforms. Called waveform in the data model.
                Memory allocation performed on-the-fly, according to previously set fields
                num_channels, num_pixels and num_samples. Memory is reallocated only if the 
                number of pixels, channels or samples changes, and upon querying this method again.
            */
            virtual uint16_t* getWaveform() = 0;
            virtual const uint16_t* getWaveform() const = 0;

            /**
                @brief Retrieve the pixels status. Called pixel_status in the data model.
                Memory allocation performed on-the-fly, according to previously set field
                num_pixels. Memory is reallocated only if the number of pixels changes, 
                and upon querying this method again.
            */
            virtual uint8_t* getPixelStatus() = 0;
            virtual const uint8_t* getPixelStatus() const = 0;

            /**
                @brief Retrieve the first cell id. Called first_cell_id in the data model.
                Memory allocation performed on-the-fly, according to previously set field
                num_modules. Memory is reallocated only if the number of modules changes, 
                and upon querying this method again.
            */
            virtual uint16_t* getFirstCellId() = 0;
            virtual const uint16_t* getFirstCellId() const = 0;

            /**
                @brief Retrieve the module high resolution clock counters. Called module_hires_local_clock_counter in the data model.
                Memory allocation performed on-the-fly, according to previously set field
                num_modules. Memory is reallocated only if the number of modules changes, 
                and upon querying this method again.
            */
            virtual uint64_t* getModuleHiresLocalClockCounter() = 0;
            virtual const uint64_t* getModuleHiresLocalClockCounter() const = 0;

            /**
                @brief  Retrieve the pedestal intensity. Called pedestal_intensity in the data model.
                Memory allocation performed on-the-fly, according to previously set field
                num_pixels. Memory is reallocated only if the number of pixels changes, 
                and upon querying this method again.
            */
            virtual float* getPedestalIntensity() = 0;
            virtual const float* getPedestalIntensity() const = 0;

            /**
                @brief Retrieve the calibration monitoring id. Called calibration_monitoring_id in the data model.
            */
            virtual uint64_t getCalibrationMonitoringId() const = 0;

            /**
                @brief Set the event id. Called event_id in the data model.
            */
            virtual void setEventId(uint64_t id) = 0;

            /**
                @brief Set the telescope id. Called tel_id in the data model.
            */
            virtual void setTelId(uint16_t tel_id) = 0;

            /**
                @brief Set the local run id. Called local_run_id in the data model.
            */
            virtual void setLocalRunId(uint64_t local_run_id) = 0;

            /**
                @brief Set the event type. Called event_type in the data model.
            */
            virtual void setEventType(uint8_t type) = 0;

            /**
                @brief Set the event time. Called event_time in the data model.
            */
            virtual void setEventTime(const CTA::HighResTimestamp &time) = 0;

            /**
                @brief Set the number of modules, called num_modules in data model
            */
            virtual void setNumModules(uint16_t num_modules) = 0;

            /**
                @brief Set the number of channels. Called num_channels in the data model.
            */
            virtual void setNumChannels(uint8_t num_chans) = 0;

            /**
                @brief Set the number of samples. Called num_samples in the data model.
            */
            virtual void setNumSamples(uint16_t num_samples) = 0;

            /**
                @brief Set the number of pixels. Called num_pixels in the data model.
            */
            virtual void setNumPixels(uint16_t num_pixels) = 0;

            /**
                @brief Set the calibration moniroting id. Called calibration_monitoring_id in the data model.
            */
            virtual void setCalibrationMonitoringId(uint64_t id) = 0;
    };

    /**
        @class AbstractCherenkovDataStream
        @brief Abstract definition of a generic Cherenkov events streamer
        @tparam CONFIG_ the actual object used to handle Cherenkov camera configuration
        @tparam EVT_ the actual object used to handle Cherenkov camera events
    */
    template <class CONFIG_, class EVT_>
    class AbstractCherenkovDataStream  
    {
        public:
            /**
                @brief Default constructor.
            */
            AbstractCherenkovDataStream() {};

            /**
                @brief Default destructor. Frees all objects used and closes any endpoint
            */
            virtual ~AbstractCherenkovDataStream() {};

            /**
                @brief Define where the stream should go. Please refer to the implementation for the meaning of endpoint_config and potential exceptions that may be thrown.
            */
            virtual void SetEndpoint(const std::string& endpoint_config) = 0;

            /**
                @brief Initializes streaming by sending a Cherenkov camera configuration 
                @return the number of bytes written. 0 means that there is not yet a connected peer
            */
            virtual int BeginOutputStream(const CONFIG_& config) = 0;

            /**
                @brief Initializes streaming by reading a Cherenkov camera configuration
                @return the number of bytes read. 0 means that there is not yet a connected peer. -1 means that the stream was terminated
            */
            virtual int BeginInputStream(CONFIG_& config) = 0;

            /**
                @brief Write a Cherenkov event.
                @return the number of bytes written. 0 means that the event couldn't be written e.g. because
                output queues are full, but that otherwise all is well. 
            */
            virtual int WriteEvent(const EVT_& event) = 0;

            /**
                @brief Read a Cherenkov event.
                @return the number of bytes read. 0 means that the event couldn't be read, e.g. because of empty input queues. -1 means that the stream was terminated.
            */
            virtual int ReadEvent(EVT_& event) = 0;

            /**
                @brief End the stream of events.
                In case of a ZMQ streamer, the end-of-stream message is sent out. In all cases this 
                frees the memory allocated by the streamer itself. 
            */
            virtual void EndEventStream() = 0;
    };

};//namespace R1
};//namespace CTA

#endif // R1CHERENKOVDATAINTERFACE_H_
