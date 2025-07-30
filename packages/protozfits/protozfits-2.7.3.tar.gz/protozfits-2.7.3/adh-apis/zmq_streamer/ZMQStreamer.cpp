/**
 * @file ZMQStreamer.cpp
 *
 * @brief ZMQ implementation of the Streamer class
 *
 *  Created on: Aug 5, 2014
 *      Author: lyard
 */

#include "ZMQStreamer.h"
#include "ProtoDataModel.pb.h"
#include "AnyArrayHelper.h"
#include "commandline_input/ConfigService.h"

#include <stdexcept>
#include <iostream>
#include <sstream>
#include <unistd.h>
#include <signal.h>

#include <CMakeDefs.h>

#include "Logger.h"

//and the handy colored output to console
using namespace ADH::ColoredOutput;
using namespace ADH::Conf;

namespace ADH
{
namespace Core
{
    // static instance of the zmq context to be shared by all objects
    // running in a single program
    zmq::context_t* ZMQStreamer::_zmq_context = NULL;
    int32           ZMQStreamer::_num_active_streamers = 0;
    std::mutex      ZMQStreamer::_zmq_context_creation_fence;
    int32           ZMQStreamer::_desired_num_zmq_threads = 1;

/******************************************************************************
 * DEFAULT CONSTRUCTOR
 ******************************************************************************/
    ZMQStreamer::ZMQStreamer(const std::string& name,
                             int32              num_threads,
                             const bool         catch_signals,
                             uint32             forward_port)
    {
        //create a zmq context if needed
        _zmq_context_creation_fence.lock();
        _num_active_streamers++;
        if (_num_active_streamers == 1)
        {
            _zmq_context = new zmq::context_t;
            if (_desired_num_zmq_threads != 1)
                setNumIoThreads(_desired_num_zmq_threads);
        }
        _zmq_context_creation_fence.unlock();

        if (num_threads != 0)
            setNumIoThreads(num_threads);

        _interrupted = 0;

        _forward_port = forward_port;

        // in order to disable the stats/command business entirely,
        // set _stats_period to 0
        _stats_period         = 0;//10000*10000; //1 second
        _evts_feedback_period = _stats_period;

        // get the generic configuration of the streamers from
        // Resources/ZMQStreamerConfig.rc
        ConfigService config;

        //build path to input configuration file.
        string binary_dir = CMAKE_BINARY_DIR;
        string relative_path = binary_dir +
                               "/../../apis/zmq_streamer/ZMQStreamerConfig.ini";

        // test if we should read from a compiled version,
        // or from an installed one
        ifstream test_input;
        test_input.open(relative_path.c_str());

        //attempt to open config file from the current directory
        if (!test_input.good())
        {
            test_input.close();
            relative_path = "./ZMQStreamerConfig.ini";
            test_input.open(relative_path.c_str());
        }

        if (!test_input.good())
        {
            test_input.close();
            relative_path = "/opt/cta/ZMQStreamerConfig.ini";
            test_input.open(relative_path.c_str());
        }

        if (!test_input.good())
        {
            test_input.close();
            relative_path = binary_dir + "/../zmq_streamer/ZMQStreamerConfig.ini";
            test_input.open(relative_path.c_str());
        }

        if (test_input.good())
        {
            ADH_info << "Loading configuration data from " << relative_path;
            ADH_info.flush();
            config.parseFile(relative_path);
        }
        else
        {
            ADH_warn << "Warning: ZMQStreamerConfig.ini could not be found. Using default values.";
            ADH_warn.flush();
        }

        test_input.close();

        if (config.has("statistics_period"))
            _stats_period = config.get<uint64>("statistics_period");

        if (config.has("events_feedback_period"))
            _evts_feedback_period = config.get<uint64>("events_feedback_period");

        if (_stats_period != 0 && !config.has("monitor_hostname"))
            throw runtime_error("Cannot configure statistics without receiver's "
                                "hostname (from Resources/ZMQStreamerConfig.ini)");

        string monitor_hostname   = "";
        string commander_hostname = "";
        if (config.has("monitor_hostname"))
        {
            monitor_hostname = config.get<string>("monitor_hostname");
            commander_hostname = monitor_hostname;
        }

        if (config.has("commander_hostname"))
            commander_hostname = config.get<string>("commander_hostname");

        string zmq_config_stats    = "tcp://"+monitor_hostname+":12800";
        string zmq_config_commands = "tcp://"+commander_hostname+":12801";

        if (_stats_period != 0)
        {
            //create the statistics/announcement stream
            _hidden_streams[STATISTICS].stream = new zmq::socket_t(*_zmq_context, ZMQ_PUB);
            _hidden_streams[COMMANDS].stream   = new zmq::socket_t(*_zmq_context, ZMQ_SUB);

            try
            {
                int max_num_messages = 10;
                _hidden_streams[STATISTICS].stream->setsockopt(ZMQ_SNDHWM, &max_num_messages, sizeof(max_num_messages));
                int forward_timeout=0;
                _hidden_streams[STATISTICS].stream->setsockopt(ZMQ_SNDTIMEO, &forward_timeout, sizeof(forward_timeout));

                _hidden_streams[STATISTICS].stream->connect(zmq_config_stats.c_str());
                _hidden_streams[COMMANDS].stream->connect(zmq_config_commands.c_str());
            }
            catch (...)
            {
                ADH_error
					<< "looks like it does not like "
						"the statistics or commands configuration" 
					<<  endl
                	<< " Error number: " << errno << endl
					<< " Statistics stream = " << zmq_config_stats << endl
					<< " Commands stream   = " << zmq_config_commands << endl;
                throw ;
            }
        }
        
        if (forward_port != 0)
        {
            _hidden_streams[FORWARD].stream = new zmq::socket_t(*_zmq_context, ZMQ_PUSH);

            try
            {
                int max_waiting_msgs = 1000;
                _hidden_streams[FORWARD].stream->setsockopt(ZMQ_SNDHWM, &max_waiting_msgs, sizeof(max_waiting_msgs));
                int forward_timeout=100;
		        _hidden_streams[FORWARD].stream->setsockopt(ZMQ_SNDTIMEO, &forward_timeout, sizeof(forward_timeout));
	            int forward_linger_duration=0;
	 	        _hidden_streams[FORWARD].stream->setsockopt(ZMQ_LINGER, &forward_linger_duration, sizeof(forward_linger_duration));
                
                ostringstream str;
                str << "tcp://*:" << forward_port;
                _hidden_streams[FORWARD].stream->bind(str.str().c_str());
            }
            catch(...)
            {
                ADH_error << "Could not bind ZMQ forward socket. Error num: " << errno << endl;
                _forward_port = 0;
                throw;
            }
        }

        _last_evt_feedback   = 0;
        _last_stats_update   = 0;
        _poll_timeout        = 1000; //1 second
        _next_id_to_poll     = 0; //start with the first connection
        _max_num_waiting_snd = 1000;
        _max_num_waiting_rcv = 1000;
        _linger_duration     = 0;
        _send_timeout        = -1; //wait indefinitely by default
        _poll_handle         = -1;

        if (config.has("poll_timeout"))
            _poll_timeout = config.get<int32>("poll_timeout");

        if (config.has("max_num_waiting_send"))
            _max_num_waiting_snd = config.get<int32>("max_num_waiting_send");

        if (config.has("max_num_waiting_receive"))
            _max_num_waiting_rcv = config.get<int32>("max_num_waiting_receive");

        if (config.has("linger_duration"))
            _linger_duration     = config.get<int32>("linger_duration");

        if (config.has("send_timeout"))
            _send_timeout        = config.get<int32>("send_timeout");

        setName(name);

        //initialize send structure
        _message_wrapper.add_payload_type(NO_TYPE);
        _message_wrapper.set_source_name(_name);

        _last_id_announcement       = 0;
        _send_event_with_statistics = false;

        //init signal handling
        if (catch_signals)
            initSignalHandler();

        _msg_data = NULL;
        _payload_start = 0;
        _msg_size = 0;
        _payload_type = 0;
    }

    //Signals handling stuff
    int32 ZMQStreamer::_interrupted = 0;


/******************************************************************************
 * SIGNAL HANDLER- flag setter. For some reason, zmq does not throw an
 *   exception on the first interrupt received (because it is
 *   catched here ?). Re-raise, but only once
 ******************************************************************************/
    void ZMQStreamer::signalHandler(int signal)
    {
        bool reraise = (_interrupted %2 == 0) ? true : false;
        _interrupted ++;
        if (reraise)
            raise(signal);
    }

/******************************************************************************
 * INTERRUPT ME
 ******************************************************************************/
    void ZMQStreamer::interruptMe()
    {
        _interrupted++;
    }

/******************************************************************************
 * INIT SIGNAL HANDLER
 *      interrupts initializer. We only handle SIGINT and SIGTERM for now
 ******************************************************************************/
    void ZMQStreamer::initSignalHandler()
    {
        struct sigaction action;
        action.sa_handler = signalHandler;
        action.sa_flags = 0;
        sigemptyset(&action.sa_mask);
        sigaction(SIGINT, &action, NULL);
        sigaction(SIGTERM, &action, NULL);
    }


/*******************************************************************************
 * SET NUM IO THREADS
 *******************************************************************************/
    void ZMQStreamer::setNumIoThreads(int32 num_threads)
    {
        int rc = zmq_ctx_set(static_cast<void*>(*_zmq_context),
                             ZMQ_IO_THREADS,
                             num_threads);

        _desired_num_zmq_threads = num_threads;

        if (rc != 0)
            throw runtime_error("Cannot change the number of threads of the context");
    }

/*******************************************************************************
 * SET NAME
 *******************************************************************************/
    void ZMQStreamer::setName(const std::string& name)
    {
        char hostname[1024];
        gethostname(hostname, 1024);

        _name = name;
        _host = string(hostname);
        _message_wrapper.set_source_name(name);

        if (name != "" && _stats_period != 0)
            _hidden_streams[COMMANDS].stream->setsockopt(ZMQ_SUBSCRIBE,
                                                         name.c_str(),
                                                         name.size());
    }

/******************************************************************************
 * DESTROY ALL STREAMS
 ******************************************************************************/
    void ZMQStreamer::destroyAllStreams()
    {
        for (auto it=_servers.begin(); it!= _servers.end(); it++)
        {
            it->second.stream->close();
            delete it->second.stream;
        }
        _servers.clear();
        for (auto it=_pollers.begin(); it!= _pollers.end(); it++)
        {
            it->second.stream->close();
            delete it->second.stream;
        }
        _pollers.clear();
        for (auto it = _hidden_streams.begin(); it!= _hidden_streams.end(); it++)
        {
//            it->second.stream->setsockopt(ZMQ_TCP_KEEPALIVE, 0);

            it->second.stream->close();
            delete it->second.stream;
        }
        _hidden_streams.clear();
    }

/*******************************************************************************
 * DEFAULT DESTRUCTOR
 *******************************************************************************/
    ZMQStreamer::~ZMQStreamer()
    {
        destroyAllStreams();

        //create a zmq context if needed
        _zmq_context_creation_fence.lock();
        _num_active_streamers--;

        if (_num_active_streamers == 0)
        {
            delete _zmq_context;
            _zmq_context = NULL;
        }
        _zmq_context_creation_fence.unlock();
    }

/*******************************************************************************
 * VERIFY CONFIG STRING
 * TODO do some actual sanity checks
 *******************************************************************************/
    void ZMQStreamer::verifyConfigString(int , const string& conf)
    {
        string protocol, address, port;

        extractConfigParams(conf, protocol, address, port);

        if (protocol == "inproc")
            return;

        if (protocol != "tcp")
            throw runtime_error("Only tcp and inproc are currently supported "
                                +protocol);

        int32 int_port = atoi(port.c_str());
        if (int_port == 0)
            throw runtime_error("Port could not be converted to integer. Value="
                                +port);
    }
uint64 num_sending_failed=0;
/******************************************************************************
 * GET NEXT RAW MESSAGE
 * TODO add priority into the polling
 * ****************************************************************************/
    int32 ZMQStreamer::getNextRawMessage(int32           connection_handle,
                                         zmq::message_t& zmess)
    {

        int32 num_connections = _pollers.size();
        //create and populate poll structure
        vector<zmq::pollitem_t> items(num_connections);
        vector<map<int32, StreamData>::iterator> items_handles(num_connections);

        int32 counter=(connection_handle == -1) ?
                                    _next_id_to_poll :
                                    connection_handle-1;

        for (auto it=_pollers.begin(); it!= _pollers.end(); it++)
        {
            items[counter].socket  = static_cast<void*>(*(it->second.stream));
            items[counter].fd      = 0;
            items[counter].events  = ZMQ_POLLIN;
            items[counter].revents = 0;
            items_handles[counter] = it;
            counter = (counter + 1 )%num_connections;
        }
        _next_id_to_poll = (_next_id_to_poll+1)%num_connections;

        connection_handle = -1;

        // poll, i.e. wait until data is available
        // or until 1 second has elapsed
        zmq::poll(items.data(), items.size(), _poll_timeout);

        // if we are already interrupted, and in blocking mode,
        // throw an exception already
        if (_interrupted != 0)
            throw runtime_error("Stopping events polling");

        int32 received_bytes = 0;
        for (int32 i=0; i<(int32)(items.size()); i++)
        {
            if (items[i].revents & ZMQ_POLLIN)
            {
                //receive message
                try
                {
                    items_handles[i]->second.stream->recv(&zmess);
                }
                catch (...)
                {
                    ostringstream error_text;
                    switch (errno)
                    {
                    case EAGAIN:
                        error_text << "Non-blocking mode was requested and no "
                                      "messages are available at the moment.";
                        break;
                    case ENOTSUP:
                        error_text << "The zmq_recv() operation is not supported "
                                      "by this socket type.";
                        break;
                    case EFSM:
                        error_text << "The zmq_recv() operation cannot be "
                                      "performed on this socket at the moment "
                                      "due to the socket not being in the "
                                      "appropriate state. This error may occur "
                                      "with socket types that switch between "
                                      "several states, such as ZMQ_REP. See the "
                                      "messaging patterns section of zmq_socket(3) "
                                      "for more information.";
                        break;
                    case ETERM:
                        error_text << "The ZMQ context associated with the specified "
                                      "socket was terminated.";
                        break;
                    case ENOTSOCK:
                        error_text << "The provided socket was invalid.";
                        break;
                    case EINTR:
                        error_text << "The operation was interrupted by delivery of "
                                      "a signal before a message was available.";
                        break;
                    case EFAULT:
                        error_text << "The message passed to the function was invalid.";
                        break;
                    default:
                        error_text << "Unkown error occured while receiving message";
                        break;
                    };
                    throw runtime_error(error_text.str());
                }

                 //provide which socket fired to the user
                _poll_handle = items_handles[i]->first;

                received_bytes = zmess.size();
                items_handles[i]->second.num_bytes += received_bytes;
                items_handles[i]->second.mess_counter ++;
                break;
            }
        }

        if (received_bytes != 0 && _forward_port != 0)
        {
            _zmess_send.copy(&zmess);
            if (!sendRawMessage(_zmess_send, FORWARD, ZMQ_NOBLOCK|ZMQ_DONTWAIT))
	    {
	    //	cout << "Sending failed... " << num_sending_failed++ << endl;
	    }
        }

        //in case the stats are disabled, return here !
        if (_stats_period == 0) return received_bytes;

        //poll for a hidden command
        zmq::pollitem_t incoming_command;
        incoming_command.socket  = static_cast<void*>(*(_hidden_streams[COMMANDS].stream));
        incoming_command.fd      = 0;
        incoming_command.events  = ZMQ_POLLIN;
        incoming_command.revents = 0;

        //FIXME we lose some additional time here: include
        //      this poll with previous one
        zmq::poll(&incoming_command, 1,0);
        if (incoming_command.revents & ZMQ_POLLIN)
        {

            _hidden_streams[COMMANDS].stream->recv(&_z_hidden_mess, ZMQ_NOBLOCK|ZMQ_DONTWAIT);
            if (((char*)(_z_hidden_mess.data()))[_z_hidden_mess.size()-1] == 'Y')
                _send_event_with_statistics = true;
            else
                _send_event_with_statistics = false;

        }

        //send statistics data, if any
        uint64 this_elapsed_time = getTimeUSec() - _last_stats_update;
        if (this_elapsed_time > _stats_period)
        {
            for (auto it=_pollers.begin(); it!=_pollers.end(); it++)
            {
                ThroughputStats stats;
                stats.set_num_bytes(it->second.num_bytes);
                it->second.num_bytes = 0;
                stats.set_elapsed_us(this_elapsed_time);
                stats.set_origin(it->second.peer);
                stats.set_port(it->second.port);
                stats.set_dest(_name+":"+_host);
                sendMessage(stats, STATISTICS, ZMQ_NOBLOCK|ZMQ_DONTWAIT);
            }
            _last_stats_update = getTimeUSec();
        }

        return received_bytes;
    }

/******************************************************************************
 * GET NEXT MESSAGE
 ******************************************************************************/
    int32 ZMQStreamer::getNextMessage(google::protobuf::Message& message)
    {
        return getNextMessage(-1, message);
    }

/******************************************************************************
 * TRANSLATE CAMERA EVENT
 *******************************************************************************/
    void ZMQStreamer::translateCameraEvent(const CTAMessage& input, CTAMessage& output)
    {
        ProtoDataModel::CameraEvent event;

        output.Clear();

        output.add_payload_type(CAMERA_EVENT);
        if (input.has_source_name())
            output.set_source_name(input.source_name());

        //TODO things are somewhat serialized twice in this case:
        //     build the headers from the low-level structs on-the-fly instead
        event.SerializeToString(output.add_payload_data());
    }

/*******************************************************************************
 * GET NEXT MESSAGE
 *******************************************************************************/
    int32 ZMQStreamer::getNextMessage(int32    connection_handle,
                                      google::protobuf::Message& message)
    {
        // get the raw zmq message
        int32 received_bytes = 0;
        try {
            received_bytes = getNextRawMessage(connection_handle,
                                                _zmess_receive);
        }
        catch(exception& e)
        {
            if (!wasInterrupted())
                throw e;
        }

        // nothing to see here, return
        if (received_bytes == 0)
            return 0;
	
        message.ParseFromArray(_zmess_receive.data(),
                               _zmess_receive.size());

        // we want to keep the origin tag of the packets -> update the
        // source name if not already updated
        if (_input_source.empty())
        {
            CTAMessage* mess = dynamic_cast<CTAMessage*>(&message);
            if (mess)
            {
                _input_source = mess->source_name();
                _message_wrapper.set_source_name(mess->source_name());
            }
        }

        // check if we should send the received message to the monitoring tool
        updateMessageDisplay(message);

        return received_bytes;
    }

/*******************************************************************************
 * UPDATE MESSAGE DISPLAY
 *******************************************************************************/
    void ZMQStreamer::updateMessageDisplay(google::protobuf::Message& message)
    {

        //if the update is off, return
        if (!_send_event_with_statistics) return;

        //if the statistics are disabled, return
        if (_evts_feedback_period == 0)   return;

        uint64 this_elapsed_time = getTimeUSec() - _last_evt_feedback;

        if (this_elapsed_time > _evts_feedback_period)
        {
            //TODO Messages are always wrapped: this check can be removed I believe
            if (extractMessageType(message) == MESSAGE_WRAPPER)
                sendHeadlessMessage(message, STATISTICS, ZMQ_NOBLOCK|ZMQ_DONTWAIT);

            _last_evt_feedback = getTimeUSec();
        }
    }

/*******************************************************************************
 * ADD A NEW OUTPUT PULL STREAM
 *******************************************************************************/
    int32 ZMQStreamer::addOutputStream(const int32 output_port)
    {
        ostringstream config;
        config << "tcp://*:" << output_port;
        return addConnection(ZMQ_PUSH, config.str());
    }

/*******************************************************************************
 * ADD A NEW CONNECTION
 *******************************************************************************/
    int32 ZMQStreamer::addConnection(int           type,
				                     const string& config,
				                     const string& filter,
				                     uint64_t      affinity,
                                     const bool    receive_block)
    {
        //verify configuration validity
        verifyConfigString(type, config);

        //create a new socket
        zmq::socket_t* new_socket = new zmq::socket_t(*_zmq_context,
                                                      type);

        // split the input parameters, and populate the appropriate
        // data structures
        string protocol, address, port;

        extractConfigParams(config, protocol, address, port);

        bool is_server = false;

        //servers do accept connections
        if (address == "*")   is_server = true;

        // inproc streams are identified by their name and procID
        // (in place of the TCP port)
        if (protocol == "inproc")
        {
            if (type == ZMQ_PUSH) is_server = true;
            ostringstream ss;
            ss << getpid();
            port = ss.str();
        }

        // Unknown addresses are replaced by their true hostnames,
        // for resolution in the monitoring tool
        if (address == "*" || address == "localhost")
        {
            char hostname[1024];
            gethostname(hostname, 1024);
            address = string(hostname);
            if (address.find('.') != string::npos)
            {
                address = address.substr(0, address.find_first_of('.'));
            }
        }

        // stream handle '0' is reserved to request data from any stream.
        // So start from 1
        int32 num_connections = _servers.size() + _pollers.size() + 1;

        //store the newly created socket parameters
        StreamData details;
        details.stream       = new_socket;
        details.config       = config;
        details.mess_counter = 0;
        details.num_bytes    = 0;
        details.peer         = address;
        details.port         = atoi(port.c_str());

        // streams are added to the server/poller depending on their
        // zmq settings, not their address
        switch (type)
        {
            case ZMQ_PUSH:
            case  ZMQ_PUB:
                _servers[num_connections] = details;
            break;
            case ZMQ_PULL:
            case  ZMQ_SUB:
                _pollers[num_connections] = details;
            break;
            default:
                throw runtime_error("Unhandled connection type");
            break;
        };

        //and connect it depending on the requested type of connection
        try
        {
            int receive_timeout = 1000;
            if (!receive_block)
                new_socket->setsockopt(ZMQ_RCVTIMEO,
                                       &receive_timeout,
                                       sizeof(receive_timeout));

            new_socket->setsockopt(ZMQ_SNDHWM,
                                   &_max_num_waiting_snd,
                                   sizeof(_max_num_waiting_snd));

            new_socket->setsockopt(ZMQ_RCVHWM,
                                   &_max_num_waiting_rcv,
                                   sizeof(_max_num_waiting_rcv));

            new_socket->setsockopt(ZMQ_LINGER,
                                   &_linger_duration,
                                   sizeof(_linger_duration));

	        new_socket->setsockopt(ZMQ_AFFINITY,
	                               &affinity,
	                               sizeof(affinity));

	        new_socket->setsockopt(ZMQ_SNDTIMEO,
	                               &_send_timeout,
	                               sizeof(_send_timeout));

	        int true_bool = 1;

	        new_socket->setsockopt(ZMQ_IMMEDIATE,
	                               &true_bool,
	                               sizeof(true_bool));

            new_socket->setsockopt(ZMQ_TCP_KEEPALIVE, 1);
            new_socket->setsockopt(ZMQ_TCP_KEEPALIVE_IDLE, 10000);
            new_socket->setsockopt(ZMQ_TCP_KEEPALIVE_INTVL, 300);


            if (is_server)
            {
                new_socket->bind(config.c_str());
            }
            else
            {
                new_socket->connect(config.c_str());
            }
        }
        catch (...)
        {
            ostringstream error_text;
            switch (errno)
            {
                case EINVAL:
                    error_text << "The endpoint supplied is invalid";
                    break;
                case EPROTONOSUPPORT:
                    error_text << "The requested transport protocol is "
                                  "not supported.";
                    break;
                case ENOCOMPATPROTO:
                    error_text << "The requested transport protocol is "
                                  "not compatible with the socket type.";
                    break;
                case EADDRINUSE:
                    error_text << "The requested address is already in use.";
                    break;
                case EADDRNOTAVAIL:
                    error_text << "The requested address was not local.";
                    break;
                case ENODEV:
                    error_text << "The requested address specifies a "
                                  "nonexistent interface.";
                    break;
                case ETERM:
                    error_text << "The ZMQ context associated with the "
                                  "specified socket was terminated.";
                    break;
                case ENOTSOCK:
                    error_text << "The provided socket was invalid.";
                    break;
                case EMTHREAD:
                    error_text << "No I/O thread is available to accomplish "
                                  "the task.";
                    break;
                case ECONNREFUSED:
                    error_text << "Connexion refused. If you use zeromq < 4 "
                                  "then servers must be started before clients: "
                                  "if this is your case either re-organize "
                                  "the startup of your objects or update zeroMQ";
                    break;
                default:
                    error_text << "Unkown error. code = " << errno;
                    break;
            };
            error_text << " Config string was: \"" << config << "\"";
            throw runtime_error(error_text.str());
        }


        //in case we are subscribing, set the appropriate filter
        if (type == ZMQ_SUB)
            new_socket->setsockopt(ZMQ_SUBSCRIBE, filter.c_str(), filter.size());

        //return associated socket handle
        return num_connections;
    }

/*******************************************************************************
 * EXTRACT THE DETAILED CONFIGURATION PARAMETERS FROMM THE CONFIGURATION STRING
 *******************************************************************************/
    void ZMQStreamer::extractConfigParams(const string& config,
                                       string&       protocol,
                                       string&       address,
                                       string&       port)
    {
        //split the string in 3 parts. separators are :// and :
        size_t protocol_separator = config.find_first_of("://");
        size_t port_separator     = config.find_last_of(":");

        if (protocol_separator == string::npos)
            throw runtime_error(red+"ERROR: \"://\" could not be found "
                                    "in config string"+no_color);

        protocol = config.substr(0,
                                 protocol_separator);

        address  = config.substr(protocol_separator+3,
                                 port_separator-protocol_separator-3);

        port     = config.substr(port_separator+1,
                                 config.size()-port_separator-1);

        if (port == "//"+address)
            port = "";
    }


/*******************************************************************************
 * UPDATE IDENTITY ANNOUNCEMENT
 *******************************************************************************/
    void ZMQStreamer::updateIdentityAnnouncement()
    {

        //one update every 10 seconds
        if (getTimeUSec() - _last_id_announcement > 10000000)
        {
            if (_stats_period != 0)
                for (auto it = _servers.begin(); it!=_servers.end(); it++)
                {
                    ServerAnnouncement announce;
                    announce.set_name(_name);
                    announce.set_host(it->second.peer);
                    announce.set_port(it->second.port);
                    sendMessage(announce, STATISTICS, ZMQ_NOBLOCK|ZMQ_DONTWAIT);
                }


            //FIXME This crashes if the forward port is not zero and stats_period is zero
            if (false)//_forward_port != 0)
            {
                ServerAnnouncement announce;
                announce.set_name(_name);
                char hostname[1024];
                gethostname(hostname, 1024);
                string str_host = string(hostname);
                if (str_host.find('.') != string::npos)
                    str_host = str_host.substr(0, str_host.find_first_of('.'));
                announce.set_host(str_host);
                announce.set_port(_forward_port);
                uint32 backup_port = _forward_port;
                _forward_port = 0;
                sendMessage(announce, STATISTICS, ZMQ_NOBLOCK|ZMQ_DONTWAIT);
                _forward_port = backup_port;
            }

            _last_id_announcement = getTimeUSec();
        }
    }

    bool ZMQStreamer::sendMessages(google::protobuf::Message** messages,
                                   const uint32 num_messages,
                                   const int32 stream_handle,
                                         int32 zmq_flags)
   {
        if (num_messages > MAX_NUM_MSGS_IN_BUNCH)
            throw runtime_error("You cannot send so many messages at once in sendMessages."
                                "The max number at once is defined in MAX_NUM_MSGS_IN_BUNCH");

        //we assume that all messages are of the same type
        MessageType message_type = extractMessageType(*(messages[0]));
        _message_wrapper.set_payload_type(0, message_type);

        //calculate sizes of everyone
        char all_payload_heads[MAX_NUM_MSGS_IN_BUNCH][8];
        uint32     these_chars[MAX_NUM_MSGS_IN_BUNCH];
        uint32  messages_sizes[MAX_NUM_MSGS_IN_BUNCH];
        uint32 total_num_bytes = 0;

        for (uint32 i=0;i<num_messages;i++)
        {
            char* payload_head = all_payload_heads[i];
            memset(payload_head, 0, 8);
            payload_head[0] = 0x22;
            uint32& this_char = these_chars[i];
            uint32& message_size = messages_sizes[i];

            this_char    = 1;
            message_size = messages[i]->ByteSize();

            uint32 encoded_payload_size = message_size;

            while (encoded_payload_size)
            {
                payload_head[this_char]  = 0x80;
                payload_head[this_char] |= encoded_payload_size & 0x7f;
                encoded_payload_size     = encoded_payload_size >> 7;
                this_char++;
            }
            if (this_char != 1)
                payload_head[--this_char] &= 0x7f;
            this_char++;

            total_num_bytes += this_char + message_size;
        }

        uint32 wrapper_size = _message_wrapper.ByteSize();
        total_num_bytes += wrapper_size;

        _zmess_send.rebuild(total_num_bytes);

        _message_wrapper.SerializeToArray(_zmess_send.data(), wrapper_size);

        uint32 offset = wrapper_size;
        for (uint32 i=0;i<num_messages;i++)
        {
            memcpy((char*)(_zmess_send.data())+offset, all_payload_heads[i], these_chars[i]);
            offset += these_chars[i];
            messages[i]->SerializeToArray((char*)(_zmess_send.data())+offset, messages_sizes[i]);
            offset += messages_sizes[i];
        }

        return sendRawMessage(_zmess_send, stream_handle, zmq_flags);
    }

/*******************************************************************************
 * SEND A MESSAGE
 *******************************************************************************/
    bool ZMQStreamer::sendMessage(const google::protobuf::Message& message,
                                                       const int32 stream_handle,
                                                             int32 zmq_flags,
                                                       MessageType message_type)
    {
        // in case the type of message to send was not specified,
        // figure it out from introspection
        if (message_type == NO_TYPE)
            message_type = extractMessageType(message);

        //increment the outbound message counter
        if (stream_handle == 0) //default stream
        {
            if (_servers.size() > 0)
            {
                _message_wrapper.set_message_count(_servers.begin()->second.mess_counter++);
            }
        }
        else if (stream_handle > 0) //regular user-defined stream
            _message_wrapper.set_message_count(_servers[stream_handle].mess_counter++);
        else // hidden statistic and control streams
            _message_wrapper.set_message_count(_hidden_streams[stream_handle].mess_counter++);

        // set the payload type
        _message_wrapper.set_payload_type(0, message_type);

        // build the payload header Manually to avoid one copy of the data
        // this only defines the payload header, not the message header
        // which is still serialized "the usual way"
        // This payload header basically says "I'm a payload (0x22)" then
        // contains the number of bytes of the payload encoded as a varint.
        // 0x22 comes from "field number << 3 | field_type".
        // Here the field number is 4=0x100, and field type is 2=0x10
        // which gives 00100010=0x22
        // TODO look if there would not be a faster way to calculate the
        // varint encoding. A small lookup table maybe ?
        char payload_head[8] = {0x22, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0};
        uint32 this_char     = 1;
        uint32 encoded_payload_size = message.ByteSize();
        while (encoded_payload_size)
        {
            payload_head[this_char]  = 0x80;
            payload_head[this_char] |= encoded_payload_size & 0x7f;
            encoded_payload_size     = encoded_payload_size >> 7;
            this_char++;
        }
        if (this_char != 1)
            payload_head[--this_char] &= 0x7f;
        this_char++;

        //serialize first message header, then payload header, then payload
        uint32 wrapper_size = _message_wrapper.ByteSize();
        uint32 total_num_bytes = message.ByteSize() + wrapper_size + this_char;

        _zmess_send.rebuild(total_num_bytes);

        _message_wrapper.SerializeToArray(_zmess_send.data(), wrapper_size);

        memcpy((char*)(_zmess_send.data())+wrapper_size, payload_head, this_char);

        message.SerializeToArray((char*)(_zmess_send.data())+wrapper_size+this_char,
                                 message.ByteSize());

        return sendRawMessage(_zmess_send, stream_handle, zmq_flags);
    }

/*******************************************************************************
 *  SEND END-OF-STREAM
 *******************************************************************************/
    bool ZMQStreamer::sendEOS(const int32 stream_handle, const bool blocking)
    {
        //FIXME as many messages as connected peers should be sent in the case of the PUSH pattern
        //FIXME appropriate messages should be sent in the case of ZMQ_PUB
        int32 zmq_flags = (blocking) ? 0 : (ZMQ_NOBLOCK|ZMQ_DONTWAIT);
        CTAMessage message;
        return sendMessage(message, stream_handle, zmq_flags, END_OF_STREAM);
    }

/*******************************************************************************
 * SEND NON-BLOCK END-OF-STREAM
 *******************************************************************************/
    bool ZMQStreamer::sendNonBlockingEOS()
    {
        return sendEOS(0, false);
    }

/*******************************************************************************
 *  SEND RAW MESSAGE
 *******************************************************************************/
    bool ZMQStreamer::sendRawMessage(zmq::message_t& message,
                                         const int32 stream_handle,
                                         const int32 zmq_flags)
    {
        if (stream_handle == 0 && _servers.size() == 0)
            throw runtime_error("ERROR: trying to send a message but no "
                                "server stream was created");

        if (stream_handle > 0 && (_servers.find(stream_handle) == _servers.end()))
            throw runtime_error("Requested stream cannot be found in servers");

        if (stream_handle < 0)
            if (_hidden_streams.find(stream_handle) == _hidden_streams.end())
                throw runtime_error("Requested stream cannot be "
                                    "found in hidden streams");

        StreamData* data = NULL;

        if (stream_handle == 0)
            data = &(_servers.begin()->second);
        else if (stream_handle > 0)
            data = &(_servers[stream_handle]);
        else if (stream_handle < 0)
            data = &(_hidden_streams[stream_handle]);

        data->num_bytes += message.size();

        bool success_send = false;

        try
        {
            while (!success_send && _interrupted == 0)
            {
                try {
                    success_send = data->stream->send(message, zmq_flags);
                }
                catch(exception& e)
                { 
                    if (!wasInterrupted())
                        throw e;
                }
                if (((zmq_flags&ZMQ_NOBLOCK)  != 0) ||
		    (       (zmq_flags&ZMQ_DONTWAIT) != 0)) //== ZMQ_NOBLOCK)
                    break;
            }
        }
        catch (...)
        {
            ostringstream error_text;
            switch (errno)
            {
                case EAGAIN:
                    error_text << "Non-blocking mode was requested and "
                                  "the message cannot be sent at the moment.";
                    break;
                case ENOTSUP:
                    error_text << "The zmq_send() operation is not "
                                  "supported by this socket type.";
                    break;
                case EFSM:
                    error_text << "The zmq_send() operation cannot be "
                                  "performed on this socket at the moment "
                                  "due to the socket not being in the "
                                  "appropriate state. This error may occur "
                                  "with socket types that switch between "
                                  "several states, such as ZMQ_REP. See the "
                                  "messaging patterns section of zmq_socket(3) "
                                  "for more information.";
                    break;
                case ETERM:
                    error_text << "The ZMQ context associated with the "
                                  "specified socket was terminated.";
                    break;
                case ENOTSOCK:
                    error_text << "The provided socket was invalid.";
                    break;
                case EINTR:
                    error_text << "The operation was interrupted by delivery "
                                  "of a signal before the message was sent.";
                    break;
                case EFAULT:
                    error_text << "Invalid message.";
                    break;
                default:
                    error_text << "Unkown error while sending message...";
                    break;
            };

            // we did catch a signal. Not sure what to do here: probably
            // nothing as an exception is raised and to be taken care of
            // by the application using the streamer
            if (_interrupted != 0)
            {

            }

            throw runtime_error(error_text.str());
        }

        // if we are already interrupted, and in blocking mode,
        // throw an exception already
        //if (_interrupted != 0 && zmq_flags != ZMQ_NOBLOCK)
        //    throw runtime_error("Send was interrupted");

        if ((stream_handle >= 0) || (_forward_port != 0))
            updateIdentityAnnouncement();

        return success_send;
    }

/*******************************************************************************
 * SEND COMPLETE MESSAGE
 *******************************************************************************/
    void ZMQStreamer::sendHeadlessMessage(const google::protobuf::Message& message_wrapper,
                                          const int32                      stream_handle,
                                                int32                      zmq_flags)
    {
        //get a zeroMQ message to send out
        //serialize full message, i.e. header + payload to zeroMQ structure
        _zmess_send.rebuild(message_wrapper.ByteSize());
	    message_wrapper.SerializeToArray(_zmess_send.data(), message_wrapper.ByteSize());

        sendRawMessage(_zmess_send, stream_handle, zmq_flags);
    }

    ///////////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////////
    uint32 DecodeVarInt(const char* data,
                        uint32&     offset)
    {
        uint32 value = 0;
        uint32 bit_shift = 0;
        while (data[offset] & 0x80)
        {
            value |= ((data[offset] & 0x7f) << bit_shift);
            bit_shift += 7;
            offset++;
        }
        value |= (data[offset] << bit_shift);
        offset++;
        return value;
    }

    ///////////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////////
   bool ZMQStreamer::GetNextPayload(const char*& payload,
                                     uint32&      payload_size,
                                     MessageType& payload_type,
                                     int32        handle)
    {
        //member variable name too long -> take a shorter reference to it
        uint32& here = _payload_start;

        //if we consumed all of the current message, get a new one
        if (here == _msg_size)
        {
            _payload_start = 0;

            try {
                _msg_size = getNextRawMessage(handle, _zmess_receive);
            }
            catch(...) {
                _interrupted = true;
            }

            if (_msg_size == 0)
                return false;

            _msg_data = (char*)(_zmess_receive.data());

            //Skip through the message until the first payload is found.
            while (_msg_data[here] != 0x22)
            {
                char field_id = _msg_data[here];

                here++;

                switch (field_id)
                {
                    // Payload type / varint / (1<<3 | 0)
                    case 0x8:
                        _payload_type = (MessageType)(DecodeVarInt(_msg_data, here));
                    break;

                    // Source name / length-delimited / (2<<3 | 2)
                    case 0x12:
                        here += DecodeVarInt(_msg_data, here);
                    break;

                    // Message counter / fixed32 / (3<<3 | 5)
                    case 0x1d:
                        here += 4;
                    break;

                    default:
                    {
                        ostringstream str;
                        str << "Unexpected field header: " << (int)(_msg_data[here]);
                        throw runtime_error(str.str());
                    }
                    break;
                };
            }
        }

        // now we are at the payload: skip 0x22 and decode its length
        here++;
        payload_size = DecodeVarInt(_msg_data, here);

        payload = _msg_data + here;

        payload_type = (MessageType)_payload_type;

        here += payload_size;

        return true;
    }


}; //namespace Core
}; //namespace ADH
