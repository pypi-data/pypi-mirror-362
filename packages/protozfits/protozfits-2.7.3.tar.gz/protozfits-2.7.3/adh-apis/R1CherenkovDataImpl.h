
/**
    @file RawCherenkovDataImpl.h

    @brief ZMQ+Protocol buffers implementation of the interface between ACADA and Cherenkov camera raw data
*/

#include "R1v1.pb.h"

// for writing to files instead of network interfaces
#include <fcntl.h>
#include <unistd.h>
#include <sstream>
#include <iostream>
#include <google/protobuf/io/zero_copy_stream_impl.h>
#include <google/protobuf/io/coded_stream.h>

// For writing to network
#include "ZMQStreamer.h"

// Abstract interface being implemented here.
#include "R1CherenkovDataInterface.h"

// timestamp
#include "timestamp.h"

///////////////////////////////////////////////////////////////////////////////
///                                                                         ///
////// CAMERA CONFIGURATION AND EVENT - PROTOCOL BUFFER IMPLEMENTATION  ///////
///                                                                         ///
///////////////////////////////////////////////////////////////////////////////
namespace CTA
{
namespace R1
{
    /** 
        @class CameraConfiguration 
        @brief Actual implementation of the AbstractCameraConfiguration class. 
        We could actually -not- inherit from the abstract class, as all its methods
        are abstract anyway.    
    */
    class CameraConfiguration : public AbstractCameraConfiguration
    {
        public:
            CameraConfiguration();
            ~CameraConfiguration();

            uint16  getTelId() const;
            uint64  getLocalRunId() const;
            LowResTimestamp getConfigTime() const;
            uint64  getCameraConfigId() const;
            const uint16* getPixelIdMap() const;
            uint16* getPixelIdMap();
            const uint16* getModuleIdMap() const;
            uint16* getModuleIdMap();
            uint16  getNumPixels() const;
            uint16  getNumModules() const;
            uint8   getNumChannels() const;
            const std::string& getDataModelVersion() const;
            uint64  getCalibrationServiceId() const;
            uint16  getCalibrationAlgorithmId() const;
            uint16  getNumSamplesNominal() const;
            uint16  getNumSamplesLong() const;
            uint16  getSamplingFrequency() const;

            uint64 getSchedulingBlockID() const;
            uint64 getObservationBlockID() const;
            float getWaveformScale() const;
            float getWaveformOffset() const;

            void setLocalRunId(uint64 id);
            void setTelId(uint16 id);
            void setConfigTime(const LowResTimestamp &ts);
            void setCameraConfigId(uint64 id);
            void setNumPixels(uint16 num_pixels);
            void setNumModules(uint16 num_modules);
            void setNumChannels(uint8 num_channels);
            void setDataModelVersion(const std::string& version);
            void setCalibrationServiceId(uint64 id);
            void setCalibrationAlgorithmId(uint16 id);
            void setNumSamplesNominal(uint16 num_samples_nominal);
            void setNumSamplesLong(uint16 num_samples_long);
            void setSamplingFrequency(uint16 sampling_frequency);

            void setSchedulingBlockID(uint64 scheduling_block_id);
            void setObservationBlockID(uint64 observation_block_id);
            void setWaveformScale(float waveform_scale);
            void setWaveformOffset(float waveform_offset);

        
            // FIXME make the proto object private, either via get/setters, or via friendship with the streamer class.
            mutable R1v1::CameraConfiguration proto_object;
            mutable R1v1::TelescopeDataStream datastream_object;
    };

    /**
        @class Event 
        @brief Actual implementation of the AbstractEvent class. 
        We could actually -not- inherit from the abstract class, as all its methods
        are abstract anyway.
    */
    class Event : public AbstractEvent
    {
        public:
            Event();
            virtual ~Event();

            uint64  getEventId() const;
            uint16  getTelId() const;
            uint64  getLocalRunId() const;
            uint8   getEventType() const;
            CTA::HighResTimestamp getEventTime() const;
            uint16   getNumModules() const;
            uint8   getNumChannels() const;
            uint16  getNumSamples() const;
            uint16  getNumPixels() const;
            const uint16* getWaveform() const;
            uint16* getWaveform();
            const uint8* getPixelStatus() const;
            uint8* getPixelStatus();
            const uint16* getFirstCellId() const;
            uint16* getFirstCellId();
            const uint64* getModuleHiresLocalClockCounter() const;
            uint64* getModuleHiresLocalClockCounter();
            const float*  getPedestalIntensity() const;
            float* getPedestalIntensity();
            uint64  getCalibrationMonitoringId() const;

            void setEventId(uint64 id);
            void setTelId(uint16 tel_id);
            void setLocalRunId(uint64 local_run_id);
            void setEventType(uint8 type);
            void setEventTime(const CTA::HighResTimestamp &time);
            void setNumModules(uint16 num_modules);
            void setNumChannels(uint8 num_chans);
            void setNumSamples(uint16 num_samples);
            void setNumPixels(uint16 num_pixels);
            void setCalibrationMonitoringId(uint64 id);

            // FIXME make the proto object private, either via get/setters, or via friendship with the streamer class.
            mutable R1v1::Event proto_object;
    };

    ///////////////////////////////////////////////////////////////////////////////
    ///                                                                         ///
    //////                      HELPER FUNCTIONS                             //////
    ///                                                                         ///
    ///////////////////////////////////////////////////////////////////////////////
    template <typename M_>
    MessageType getMessageEnum()
    {
        throw std::runtime_error("Error: you are trying to read a message type that is not supported");
    }
    template <>
    MessageType getMessageEnum<CTA::R1::Event>();
    template<>
    MessageType getMessageEnum<CTA::R1::CameraConfiguration>();

    ///////////////////////////////////////////////////////////////////////////////
    ///                                                                         ///
    //////       CHERENKOV DATA STREAM - ZMQ/PROTOBUF IMPLEMENTATION         //////
    ///                                                                         ///
    ///////////////////////////////////////////////////////////////////////////////
    /**
        @class CherenkovDataStream 
        @brief Actual implementation of the AbstractCherenkovDataStream class. 
        We could actually -not- inherit from the abstract class, as all its methods
        are abstract anyway.
    */
    template <class CONFIG_, class EVT_>
    class CherenkovDataStream : public AbstractCherenkovDataStream<CONFIG_, EVT_>
    {
        public:

            ///////////////////////////////////////////////////////////////////////
            //                           CONSTRUCTOR                             //
            ///////////////////////////////////////////////////////////////////////
            CherenkovDataStream(const std::string& name, 
                                const char mode,
                                const int forward_port=0) : _file_handle(0),
                                                    _file_ostream(NULL),
                                                    _file_istream(NULL),
                                                    _file_ostreamer(NULL),
                                                    _file_istreamer(NULL),
                                                    _zmq_streamer(name, 0, false, forward_port),
                                                    _zmq_handle(0),
                                                    _mode(mode),
                                                    _stream_has_begun(false),
                                                    _from_file(true)
            {
                if (_mode != 'w' && _mode != 'r' )
                    throw std::runtime_error("Wrong mode given in stream constructor. Only r or w accepted");
            }

            ///////////////////////////////////////////////////////////////////////
            //                            DESTRUCTOR                             //
            ///////////////////////////////////////////////////////////////////////
            virtual ~CherenkovDataStream()
            {
                if (_stream_has_begun) 
                    EndEventStream();
            }

            ///////////////////////////////////////////////////////////////////////
            //                          SET ENDPOINT                             //
            ///////////////////////////////////////////////////////////////////////
            void SetEndpoint(const std::string& endpoint_config)
            {
                // Should we create a network connection ? 
                if (endpoint_config.substr(0,3) == "tcp")
                {
                    _from_file = false;
                    int push_or_pull = ZMQ_PUSH;
                    if (_mode == 'r') 
                        push_or_pull = ZMQ_PULL;
                    _zmq_handle = _zmq_streamer.addConnection(push_or_pull, endpoint_config, "", 0, false);
                    return;
                }

                // Create read/write to a file
                mode_t mode = O_WRONLY | O_CREAT | O_EXCL; // Don't override existing files. Should we anyway ?
                if (_mode == 'r')
                    mode = O_RDONLY;
                _file_handle = open(endpoint_config.c_str(), mode);

                if (_file_handle == -1)
                    throw std::runtime_error("Couldn't open file stream from config " + endpoint_config);
                if (_mode == 'w')
                {
                    _file_ostream  = new google::protobuf::io::FileOutputStream(_file_handle);
                    _file_ostreamer = new google::protobuf::io::CodedOutputStream(_file_ostream);
                }
                else
                {
                    _file_istream  = new google::protobuf::io::FileInputStream(_file_handle);
                    _file_istreamer = new google::protobuf::io::CodedInputStream(_file_istream);
    
                }
            }

            ///////////////////////////////////////////////////////////////////////
            //                          BEGIN OUTPUT STREAM                      //
            ///////////////////////////////////////////////////////////////////////
            int BeginOutputStream(const CONFIG_& config)
            {
                assert(!_stream_has_begun);
                assert(_mode == 'w');

                _stream_has_begun = true;
                if (_from_file)
                {
                    _file_ostreamer->WriteLittleEndian32(config.datastream_object.ByteSize());
                    config.datastream_object.SerializeToCodedStream(_file_ostreamer);
                    _file_ostreamer->WriteLittleEndian32(config.proto_object.ByteSize());
                    config.proto_object.SerializeToCodedStream(_file_ostreamer);
                    return config.datastream_object.ByteSize() + sizeof(int32) + config.proto_object.ByteSize() + sizeof(int32);
                }

                int bytes_written = _zmq_streamer.sendMessage(config.datastream_object, _zmq_handle, ZMQ_NOBLOCK);
            
                if (!bytes_written)
                    _stream_has_begun = false;
                
                int bytes_written_2 = _zmq_streamer.sendMessage(config.proto_object, _zmq_handle, ZMQ_NOBLOCK);
            
                if (!bytes_written_2)
                    _stream_has_begun = false;
                
                return bytes_written+bytes_written_2;
            }

            ///////////////////////////////////////////////////////////////////////
            //                          BEGIN INPUT STREAM                       //
            ///////////////////////////////////////////////////////////////////////
            int BeginInputStream(CONFIG_& config)
            {
                assert(!_stream_has_begun);
                assert(_mode == 'r');

                _stream_has_begun = true;

                if (_from_file)
                {
                    int32 size_1 = ReadNextMessageFromFile((google::protobuf::Message*)(&(config.datastream_object)));
                    int32 size_2 = ReadNextMessageFromFile((google::protobuf::Message*)(&(config.proto_object)));
                    return size_1+size_2;
                }
                
                int bytes_read = readTypedMessageFromZMQ<CTA::R1::CameraConfiguration>(config);

                if (bytes_read == 0)
                    _stream_has_begun = false;
                
                return bytes_read;
            }

            ///////////////////////////////////////////////////////////////////////
            //                            WRITE EVENT                            //
            ///////////////////////////////////////////////////////////////////////
            int WriteEvent(const EVT_& event)
            {
                assert(_stream_has_begun);
                assert(_mode=='w');

                if (_from_file)
                {
                    _file_ostreamer->WriteLittleEndian32(event.proto_object.ByteSize());
                    event.proto_object.SerializeToCodedStream(_file_ostreamer);
                    return event.proto_object.ByteSize()+sizeof(int32);
                }

                return _zmq_streamer.sendMessage(event.proto_object, _zmq_handle, ZMQ_NOBLOCK);
            }

            ///////////////////////////////////////////////////////////////////////
            //                            READ EVENT                             //
            //      Returns the number of bytes read                             //
            //          0 if nothing was read                                    //
            //          a negative error code if the wrong event type was read   //
            ///////////////////////////////////////////////////////////////////////
            int ReadEvent(EVT_& event)
            {
                assert(_stream_has_begun);
                assert(_mode == 'r');
                
                if (_from_file)
                    return ReadNextMessageFromFile((google::protobuf::Message*)(&(event.proto_object)));

                return readTypedMessageFromZMQ<EVT_>(event);
            }

            ///////////////////////////////////////////////////////////////////////
            //                          END EVENT STREAM                         //
            ///////////////////////////////////////////////////////////////////////
            void EndEventStream()
            {
                assert(_stream_has_begun);

                _stream_has_begun = false;

                if (_from_file)
                {
                    if (_file_ostreamer != NULL)
                    {
                        delete _file_ostreamer;
                        delete _file_ostream;
                        _file_ostreamer = NULL;
                        _file_ostream  = NULL;
                    }
                    if (_file_istreamer != NULL)
                    {
                        delete _file_istreamer;
                        delete _file_istream;
                        _file_istreamer = NULL;
                        _file_istream  = NULL;
                    }
                    if (_file_handle > 0)
                    {
                        close(_file_handle);
                        _file_handle = 0;
                    }
                    return;
                }

                if (_mode == 'w')
                    _zmq_streamer.sendNonBlockingEOS();
                    //sleep 1/10 of a second to let the EOS be sent before destroying streams
                    usleep(100000);

                _zmq_streamer.destroyAllStreams();
            }

            ///////////////////////////////////////////////////////////////////////
            //                   RECOVER UNEXPECTED PAYLOAD                      //
            ///////////////////////////////////////////////////////////////////////        
            template <typename M_>
            int RecoverUnexpectedPayload(M_& message)
            {
                // Check that we are recovering the expected type
                if (CheckIfPayloadTypeIsCorrect<M_>() < 0)
                    return CheckIfPayloadTypeIsCorrect<M_>();

                return ParsePayload(message);
            }

        private:
        ///////////////////////////////////////////////////////////////////////////
        //                         PRIVATE HELPER FUNCTIONS                      //
        ///////////////////////////////////////////////////////////////////////////

            // Members for incoming payloads. 
            const char* payload;
            uint32      payload_size;
            MessageType payload_type;

            // Verifies that incoming payload is the type we are trying to read
            // returns payload type or negative value if incorrect payload
            template <typename M_>
            int CheckIfPayloadTypeIsCorrect()
            {
                if (payload_type != getMessageEnum<M_>())
                {
                    // If we got end-of-stream, return it
                    if (payload_type == END_OF_STREAM)
                        return -1;
                    
                    // otherwise just say that we got a wrong type and encode what type we really got
                    return WRONG_TYPE - payload_type;
                }
                return payload_type;
            }

            int ParsePayload(CTA::R1::Event& message)
            {
                message.proto_object.ParseFromArray(payload, payload_size);
                return payload_size;
            }

            int ParsePayload(CTA::R1::CameraConfiguration& message)
            {
                std::cout << "Parsing CameraConfiguration now" << std::endl;
                message.datastream_object.ParseFromArray(payload, payload_size);
                uint32 first_size = payload_size;
                
                // retry GetNextPayload up to 10 times until payload is received
                uint32 Ntry = 10;
                for (uint32 i=0; i<Ntry;i++) {
                    if (_zmq_streamer.wasInterrupted())
                        throw std::runtime_error("ZMQ streamer interrupted");
                    if (_zmq_streamer.GetNextPayload(payload, payload_size, payload_type, _zmq_handle) != 0)
                        break;
                    if (i == Ntry-1)
                        return 0;
                }

                if (payload_type != CAMERA_CONFIG)
                    return WRONG_TYPE - payload_type;
                message.proto_object.ParseFromArray(payload, payload_size);

                return first_size + payload_size;
            }

            ///////////////////////////////////////////////////////////////////////
            //                    READ TYPED MESSAGE FROM ZMQ                    //
            ///////////////////////////////////////////////////////////////////////
            template <typename M_>
            int readTypedMessageFromZMQ(M_& message)
            {
                if (!_zmq_streamer.GetNextPayload(payload, payload_size, payload_type, _zmq_handle))
                    return 0;
        
                // Check that we are reading the expected type
                if (CheckIfPayloadTypeIsCorrect<M_>() < 0)
                    return CheckIfPayloadTypeIsCorrect<M_>();

                return ParsePayload(message);
            }

            ///////////////////////////////////////////////////////////////////////
            //                   READ NEXT MESSAGE FROM FILE                     //
            ///////////////////////////////////////////////////////////////////////
            int ReadNextMessageFromFile(google::protobuf::Message *msg) 
            {
                // FIXME There is a problem with _file_istreamer, which goes crazy after some number of events. 
                // I should investigate why. In the meantime, this just works...
                delete _file_istreamer;
                _file_istreamer = new google::protobuf::io::CodedInputStream(_file_istream);
                uint32 size_read;
                bool has_next = _file_istreamer->ReadLittleEndian32(&size_read);
                if(!has_next) 
                    return -1;
                else 
                {
                    google::protobuf::io::CodedInputStream::Limit msgLimit = _file_istreamer->PushLimit(size_read);
                    if (!msg->ParseFromCodedStream(_file_istreamer)) 
                        throw std::runtime_error("A message couldn't be parsed form the file stream");

                    _file_istreamer->PopLimit(msgLimit);

                    return size_read+sizeof(int32);
                }
            }

            ///////////////////////////////////////////////////////////////////////
            //                          MEMBER VARIABLES                         //
            ///////////////////////////////////////////////////////////////////////
            // Read/Write to files
            int                _file_handle;
            google::protobuf::io::FileOutputStream*  _file_ostream;
            google::protobuf::io::FileInputStream*   _file_istream;
            google::protobuf::io::CodedOutputStream* _file_ostreamer;
            google::protobuf::io::CodedInputStream*  _file_istreamer;

            // Read/Write to network
            ADH::Core::ZMQStreamer _zmq_streamer;
            int         _zmq_handle;
            const char  _mode;
            bool        _stream_has_begun;

            // Figure out between files and network streams
            bool        _from_file;
    };

    ///////////////////////////////////////////////////////////////////////////////
    ///                                                                         ///
    ///   TEMPLATE SPECIALIZATION THAT CREATES THE ACTUAL CTA::R1::EventsStream  ///
    ///                                                                         ///
    ///////////////////////////////////////////////////////////////////////////////

    typedef CherenkovDataStream<CTA::R1::CameraConfiguration, CTA::R1::Event> EventsStream;

}; //namespace R1
}; //namespace CTA
