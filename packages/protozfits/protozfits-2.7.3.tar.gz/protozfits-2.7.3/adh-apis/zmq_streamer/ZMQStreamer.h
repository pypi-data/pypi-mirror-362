/**
 * @file ZMQStreamer.h
 *
 * @brief ZMQ implementation of the Streamer class
 *
 *  Created on: Aug 5, 2014
 *      Author: lyard
 */

#ifndef ZMQSTREAMER_H_
#define ZMQSTREAMER_H_

#include "BasicDefs.h"
#include "zmq++.h"
#include <mutex>

#define MAX_NUM_MSGS_IN_BUNCH (32)

namespace ADH
{
namespace Core
{
    /**************************************************************************
     *      @class ZMQStreamer
     *      @brief create and store zeroMQ sockets and simplifies their use with
     *             protocol buffers.
     **************************************************************************/
    class ZMQStreamer 
    {
        public:

        /**
         *  @brief Create a new connection
         *
         *  This creates a new zeroMQ socket, either PUSH or PULL.
         *  If the type or configuration string is not valid, a
         *  runtime_exception is raised
         *  @param type the type of connection to create:
         *         either server (ZMQ_PUSH) or client (ZMQ_PULL)
         *  @param config the zeroMQ configuration string
         *  @param filter a filter for the incoming subscribed data
         *  @return the handle corresponding to the newly created stream
         */
        int32 addConnection(int 		       type,
                            const std::string& config,
                            const std::string& filter="",
			                uint64_t           affinity=0,
                            const bool         receive_block=true);

        /**
         *  @brief Simplified addConnection for servers
         *
         *  Calls add connection with type = ZMQ_PUSH,
         *  config = tcp * output_port and no filter
         *  @param output_port the port number to use
         *         to serve data
         */
        int32 addOutputStream(const int32 output_port);


        /**
         *  @brief Stops operations, destroy streams
         */
        void interruptMe();

        /**
         *  @brief default constructor
         *
         *	@param name the name identifier for display purposes
         *  @param num_threads the number of threads to use to
         *         handle the connections.
         *  @param catch_signals if true, will catch interupts like
         *         ctrl-c and wasInterrupted will return true. Allows
         *         to exit gracefully
         *  @param forward_port if non-zero will forward events on
         *         a given port
         */
        ZMQStreamer(const std::string& name        ="no_name",
                    int32              num_threads = 0,
                    const bool         catch_signals=false,
                    uint32             forward_port= 0);

        /**
         *  @brief default destructor
         */
        virtual ~ZMQStreamer();

        /**
         *  @brief destroys all existing streams.
         *         Used in the destructor
         */
        void destroyAllStreams();

        /**
         *  @brief method that should be used to wait
         *         for incoming messages
         *
         *  This method will block until a message is
         *  available from any of the remote peers
         *  @param connection_handle the connection
         *         handle of the remote peer that sent
         *         the message
         *  @param message the data that was received
         *  @param priority_poll the stream to poll in
         *         priority
         *  @return the number of bytes read from the
         *          stream, 0 in case no message was
         *          received
         */
        virtual int32 getNextMessage(int32                      connection_handle,
                                     google::protobuf::Message& message);

        virtual int32 getNextMessage(google::protobuf::Message& message);

        /**
         *  @brief configure the number of IO threads used by
         *         zeroMQ.
         *
         *  the zeroMQ instance is shared between all objects
         *  in a program. So if one is building a pipeline that
         *  uses many objects then increasing this number might
         *  help. The rule of thumb is ~ 1 thread per 8Gbps of
         *  data sent/received so one should not have to increase
         *  this number too often
         */
        void setNumIoThreads(int32 num_threads);

        /**
         *  @brief sets the name of this messages server to be
         *         included in the messages headers
         *
         *  To be used if the name could not be set during
         *  object creation. WARNING: if a socket factory
         *  also receive messages, it will obtain its name
         *  from the first received message. This feature is
         *  enabled to allow packets to keep their original
         *  source name throughout the entire pipeline
         *  @param name the name of this messages server
         */
        void setName(const std::string& name);

        /**
         *  @brief send one message
         *
         *  The message is serialized right away, while the
         *  actual send is done asynchronously
         *  @param message the message to be sent
         *  @param stream_handle the handle of the stream to
         *         end the message to, acquired from the
         *         addConnection method. If omitted, the
         *         first added stream is used.
         *  @param message_type the enum corresponding of the
         *         type of message to be sent. If ommitted it
         *         is figured using the message's introspection.
         */
        bool sendMessage(const google::protobuf::Message& message,
                         const int32 stream_handle = 0,
                         int32  flags     = 0,
                         MessageType message_type = NO_TYPE);

        //! @brief send one message. Helper function to be
        //! able to ommit any of the two later parameters
        bool sendMessage(const google::protobuf::Message& message,
                         MessageType           message_type,
                         const int32                      stream_handle = 0)
        {
            return sendMessage(message, stream_handle, 0, message_type);
        }

        bool sendMessages( google::protobuf::Message** messages,
                          const uint32 num_messages,
                          const int32  stream_handle = 0,
                                int32  zmq_flags = 0);

        /** @brief send one already serialized message
         *
         *  the actual send is done asynchronously
         *  @param message the message to be sent
         *  @param stream_handle the handle of the stream
         *         to send the message to, acquired from
         *         the addConnection method. If omitted,
         *         the first added stream is used.
         *  @param message_type the enum corresponding of
         *         the type of message to be sent. If
         *         ommitted it is figured using the message's
         *         introspection.
         */
        void sendHeadlessMessage(const google::protobuf::Message& message_wrapper,
                                 const int32                      stream_handle = 0,
                                       int32                      zmq_flags = 0);

        /** @brief send a raw zmq message. You're on your own with this one.
         *
         */
        bool sendRawMessage(zmq::message_t& message,
                            const int32     stream_handle=0,
                            int32           zmq_flags=0);

        /// @brief tells the downstream pipeline that the stream ended
        bool sendEOS(const int32 stream_handle=0, const bool blocking = true);

        bool sendNonBlockingEOS();

        //! @brief returns the current zmq context
        static const zmq::context_t& getContext() { return *_zmq_context;}

        /**
         * @brief  set the timeout durection of the receive methods
         *         (getNextMessage and getNextRawMessage)
         *
         *  default value is 1 second. Providing a negative value
         *  makes the receive block indefinitly
         *  @param milliseconds the duration of the timeout, in
         *  microseconds. negative value means wait indefinitly.
         */
        void setReceiveTimeoutMilliSec(int32 milliseconds)
        {
            if (milliseconds <= -1)
                _poll_timeout = -1;
            else
                _poll_timeout = milliseconds;
        }

        static bool wasInterrupted() { return (_interrupted!=0);}

    protected:

        //! @brief helper function to get the returned message and stream
        //! ID from member variables rather than parameters
        int32 getNextMessage() { return getNextMessage(-1, _message);}

        //! @brief helper function to get the next message, considering
        //! a given stream in priority
        int32 getNextMessage(int32 stream_handle) { return getNextMessage(stream_handle, _message);}

        /** @brief send a message to the monitoring.
         *
         *  Used internally by the socket factory, it can be called by
         *  the user in case specific data has to be reviewed. Please
         *  note that it will actually update the display if at least
         *  1 second has passed since the last update. If this is not
         *  good for you, well we can certainly implement some fine-tuned
         *  behavior control: let me know !
         *  @param message the data to be sent to the monitoring tool
         */
        void updateMessageDisplay(google::protobuf::Message& message);

        /** @brief obtain the next incoming raw zeroMQ message
         *
         *  Bypasses all the protocol buffer and monitoring stuff: you
         *  are on your own
         *  @param connection_handle ID of the stream that produced data
         *  @param zmess the zeroMQ message structure that will receive
         *         the data
         *  @return the number of bytes received, 0 in case no message
         *          was received
         */
        int32 getNextRawMessage(int32           connection_handle,
                                zmq::message_t& zmess);

        struct StreamData
        {
            /// the real zmq socket
            zmq::socket_t* stream;

            /// the configuration string
            std::string    config;

            /// the number of messages sent TODO cannot remember if
            /// received messages are counted too
            int32          mess_counter;

            /// the number of bytes sent/received
            int64          num_bytes;

            /// the distant peer. for servers always localhost
            std::string    peer;

            /// the connection port
            int32          port;
        };

        //! @brief a list of hidden streams, used for homekeeping information
        enum HiddenStreams
        {
            /// statistics channel
            STATISTICS    = -1,
            /// announcement channel is the same as statistic
            ANNOUNCEMENTS = -1,

            /// commands channel. Currently only used to enable/disable the
            /// sending of events data
            COMMANDS      = -2,

            /// forward channel, for QLA
            FORWARD       = -3
        };

        /// ZeroMQ context used for the communications.
        // Static as there should only be one context per instance
        // Pointer because it must be destroyed if all streams are destroyed
        static zmq::context_t* _zmq_context;
        static int32           _num_active_streamers;
        static std::mutex      _zmq_context_creation_fence;
        static int32           _desired_num_zmq_threads;

        /// List of hidden streams. the key is the stream handle allocated
        /// at creation time
        std::map<int32, StreamData> _hidden_streams;

        /// List of pusher streams. The name sucks as it only means that
        /// they are pushing data forward
        std::map<int32, StreamData> _servers;

        /// List of poller streams.
        std::map<int32, StreamData> _pollers;

        /// Name of this component
        std::string _name;

        /// hostname onto which this component is running
        std::string _host;

        /// message wrapper used to send the data
        CTAMessage _message_wrapper;

        /// pointer to the payload string
        std::string* _payload;

        /// time when the last ID of this node was announced through
        /// hidden stream
        uint64 _last_id_announcement;

        /// duration in microseconds between two updates of the statistics
        uint64 _stats_period;

        /// duration in microseconds between two updates of the events display
        uint64 _evts_feedback_period;

        /// Internal variable to store the last time when the event was updated
        uint64 _last_evt_feedback;

        /// Time when the statistics where last updated
        uint64 _last_stats_update;

        /// flag telling to send events data to the central monitor or not
        bool _send_event_with_statistics;

        /// Port where events should be forwarded
        uint32 _forward_port;

        /// ZMQ message structure reused for sending messages
        zmq::message_t _zmess_send;

        /// ZMQ message structure reused for receiving messages
        zmq::message_t _zmess_receive;

        /// ZMQ message structure reused for doing the hidden
        /// communication stuff
        zmq::message_t _z_hidden_mess;

        /// Name of the messages source
        std::string _input_source;

        /// All clients need this. TODO remove the local defs from
        /// clients and the parameter from getNextMessage
        int32 _poll_handle;

        /// index of the last connection that was read first, to
        /// balance the reading from all inputs
        int32 _next_id_to_poll;

        /// Almost All clients need this. TODO remove the local
        /// defs from clients and the parameter from getNextMessage
        CTAMessage _message;

        /// timeout duration while getting incoming messages
        int32 _poll_timeout;

        /// Max number of messages waiting in the ZMQ queue to be sent
        int32 _max_num_waiting_snd;

        ///Max number of messages waiting in the ZMQ queue to be received
        int32 _max_num_waiting_rcv;

        /// Duration between the disconnect order and actual disconnection
        int32 _linger_duration;

        /// Timeout after which a send is considered a failure
        int32 _send_timeout;

        //Signals handling stuff
        static int32 _interrupted;
        static void  signalHandler(int signal);
        void         initSignalHandler();

        static int32 _connected_stream_count;

        /**
         * @brief Checks (poorly) if the provided string is a valid configuration
         *
         *  @param type the zmq type of connection desired
         *  @param value the configuration string used to create the stream
         */
        virtual void verifyConfigString(int type, const std::string& value);

        /**
         * @brief basic extraction of parameters from configuration string
         *
         *  Leaves the port empty if no port was provided
         *  @param config the input configuration string
         *  @param protocol where to store the extracted protocol value
         *  @param address  where to store the extracted address  value
         *  @param port     where to store the extracted port value
         */
        virtual void extractConfigParams(const std::string& config,
                                               std::string& protocol,
                                               std::string& address,
                                               std::string& port);

        /** @brief broadcast the identify of this node through hidden stream.
         *
         * Used to let the monitor know what is the real name of the nodes
         * instead of just e.g. localhost:12345
         *
         */
        void updateIdentityAnnouncement();

        /**
         * @brief moves a message forward, without over-riding its header metadata
         */
        void translateRawCameraMessage(const std::string& buffer, google::protobuf::Message& target);
        void translateCameraEvent(const CTAMessage& input, CTAMessage& target);

    public:
        /**
         *  Optimization for R1 API
         */
        bool GetNextPayload(const char*& payload,
                            uint32&      payload_size,
                            MessageType& payload_type,
                            int32        handle);

    protected:
        // pointer to the start of the message
        char* _msg_data;

        // Where we are in the message
        uint32  _payload_start;

        // Total size of the message
        uint32 _msg_size;

        int32 _payload_type;

    };  //class Streamer

}; //namespace Core
}; //namespace ADH

#endif /* SOCKETS_FACTORY_H_ */
