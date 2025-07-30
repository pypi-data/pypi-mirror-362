
/**
    @file DL0CherenkovDataImpl.h

    @brief ZMQ+Protocol buffers implementation of the interface between ACADA and Cherenkov camera DL0 data
*/

#include "DL0v1_Telescope.pb.h"

// for writing to files instead of network interfaces
#include <fcntl.h>
#include <unistd.h>
#include <sstream>
#include <iostream>
#include <google/protobuf/io/zero_copy_stream_impl.h>
#include <google/protobuf/io/coded_stream.h>

// For writing to network
#include "ZMQStreamer.h"

#include "DL0CherenkovDataInterface.h"

namespace CTA
{
namespace DL0
{
namespace Telescope
{
    ///////////////////////////////////////////////////////////////////////////////
    ///                                                                         ///
    ////// CAMERA CONFIGURATION AND EVENT - PROTOCOL BUFFER IMPLEMENTATION  ///////
    ///                                                                         ///
    ///////////////////////////////////////////////////////////////////////////////

    /** 
        @class CameraConfiguration 
        @brief DL0 CameraConfiguration Implementation 
    */
    class CameraConfiguration : public AbstractCameraConfiguration
    {
        public:
            CameraConfiguration();
            ~CameraConfiguration();

            uint16  getTelId() const;
            uint64  getLocalRunId() const;
            CTA::LowResTimestamp getConfigTime() const;
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
            void setConfigTime(const CTA::LowResTimestamp &ts);
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
            mutable DL0v1::Telescope::CameraConfiguration proto_object;
            mutable DL0v1::Telescope::DataStream datastream_object;
    };

    /**
        @class Event 
        @brief DL0 Event implementation
    */
    class Event : public AbstractEvent
    {
        public:
            Event(bool alloc_proto_object=true);
            virtual ~Event();

            uint64  getEventId() const;
            uint16  getTelId() const;
            uint64  getLocalRunId() const;
            uint8   getEventType() const;
            CTA::HighResTimestamp getEventTime() const;
            uint16  getNumModules() const;
            uint8   getNumChannels() const;
            uint16  getNumSamples() const;
            uint16  getNumPixelsSurvived() const;
            uint16  getNumPixels() const;
            const uint16* getWaveform() const;
            uint16* getWaveform();
            const uint8* getPixelStatus() const;
            uint8* getPixelStatus();
            const uint16* getFirstCellId() const;
            uint16* getFirstCellId();
            uint64  getCalibrationMonitoringId() const;
            uint64  getPixelId() const;
            const float*  getPedestalIntensity() const;
            float*  getPedestalIntensity();

            void setEventId(uint64 id);
            void setLocalRunId(uint64 id);
            void setTelId(uint16 tel_id);
            void setEventType(uint8 type);
            void setEventTime(const CTA::HighResTimestamp &time);
            void setNumModules(uint16 num_modules);
            void setNumChannels(uint8 num_chans);
            void setNumSamples(uint16 num_samples);
            void setNumPixelsSurvived(uint16 num_pixels_survived);
            void setNumPixels(uint16 num_pixels);
            void setCalibrationMonitoringId(uint64 id);
            void setPixelId(uint64 id);

            // !! Here proto object is a pointer to reuse the memory-allocated message without hard copying!!
            DL0v1::Telescope::Event* proto_object;

            // flag of the proto_object memory allocation
            bool _alloc_proto_object;

            // Original number of pixels. Not present in the data model,
            // though needed anyways to manipulate a stand-alone event
            uint16 _num_pixels;
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
    MessageType getMessageEnum<DL0v1::Telescope::Event>();
    template<>
    MessageType getMessageEnum<DL0v1::Telescope::CameraConfiguration>();

    ///////////////////////////////////////////////////////////////////////////////
    ///                                                                         ///
    //////       CHERENKOV DATA STREAM - ZMQ/PROTOBUF IMPLEMENTATION         //////
    ///                                                                         ///
    ///////////////////////////////////////////////////////////////////////////////
    /**
        @class DataStream 
        @brief DL0 CherenkovDataStream Implementation
    */
    template <class CONFIG_, class EVT_>
    class DataStream : public AbstractDataStream<CONFIG_, EVT_>
    {
        public:

            ///////////////////////////////////////////////////////////////////////
            //                           CONSTRUCTOR                             //
            ///////////////////////////////////////////////////////////////////////
            DataStream(const std::string& name,
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
            ~DataStream()
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
            int BeginInputStream(CONFIG_ & config)
            {
                assert(!_stream_has_begun);
                assert(_mode == 'r');

                _stream_has_begun = true;

                if (_from_file)
                    return ReadNextMessageFromFile((google::protobuf::Message*)(&(config.proto_object)));

                int bytes_read = readTypedMessageFromZMQ<Telescope::CameraConfiguration>(config);

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

                if (event._alloc_proto_object==false)
                    throw std::runtime_error("memory not allocated for protobuf object");

                if (_from_file)
                {
                    _file_ostreamer->WriteLittleEndian32(event.proto_object->ByteSize());
                    event.proto_object->SerializeToCodedStream(_file_ostreamer);
                    return event.proto_object->ByteSize()+sizeof(int32);
                }

                return _zmq_streamer.sendMessage(*(event.proto_object), _zmq_handle, ZMQ_NOBLOCK);
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
                    return ReadNextMessageFromFile((google::protobuf::Message*)(event.proto_object));

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
            template <typename M_> int RecoverUnexpectedPayload(M_& message)
            {
                // Check that we are recovering the expected type
                if (CheckIfPayloadTypeIsCorrect<M_>() < 0)
                    return CheckIfPayloadTypeIsCorrect<M_>();

                return ParsePayload(message);
            }


        private:

            // Members for incoming payloads. 
            const char* payload;
            uint32      payload_size;
            MessageType payload_type;

            // Verifies that incoming payload is the type we are trying to read
            // returns payload type or negative value if incorrect payload
            template <typename M_> int CheckIfPayloadTypeIsCorrect()
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

            template <typename M_> int ParsePayload(M_& message)
            {
                message.proto_object.ParseFromArray(payload, payload_size);
                return payload_size;
            }

            // now DL0::Telescope::Event proto_object is a pointer
            // overload the function above with non-template function
            int ParsePayload(Event& message)
            {
                message.proto_object->ParseFromArray(payload, payload_size);
                return payload_size;
            }

            ///////////////////////////////////////////////////////////////////////
            //                    READ TYPED MESSAGE FROM ZMQ                    //
            ///////////////////////////////////////////////////////////////////////
            template <typename M_> int readTypedMessageFromZMQ(M_& message)
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
    ///   TEMPLATE SPECIALIZATION THAT CREATES THE ACTUAL CTA::DL0::EventsStream  ///
    ///                                                                         ///
    ///////////////////////////////////////////////////////////////////////////////

    typedef DataStream<CameraConfiguration, Event> EventsStream;



}; //namespace Telescope
}; //namespace DL0
}; //namespace CTA
