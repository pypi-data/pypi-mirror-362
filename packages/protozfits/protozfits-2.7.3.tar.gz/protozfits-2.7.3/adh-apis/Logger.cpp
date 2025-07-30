/*
 * Logger.cpp
 *
 *  Created on: Jul 11, 2016
 *      Author: lyard
 */

#include "Logger.h"
#include <ctime>

using namespace std;

//Hook-up of ADH logging facilities to ACS.
#ifdef ACS_BUILD
#ifdef __cplusplus
extern "C" {
#endif

extern void acs_log(int type, const char* message);

#ifdef __cplusplus
}
#endif //__cplusplus
#endif //ACS_BUILD


namespace ADH
{
namespace Core
{

    string NowString()
    {
        time_t now;
        time(&now);
        char buf[sizeof "2019-01-01T01:01:01"];
        strftime(buf, sizeof buf, "%FT%T", gmtime(&now));
        return string(buf);
    }

    using namespace ColoredOutput;

    Logger::Logger(std::ostream* output) : _buffer(),
                                           _out_stream(output)
    {
    }

    Logger::~Logger()
    {
    }

    void Logger::flush()
    {
        const lock_guard<mutex> lock(_log_fence);
        (*_out_stream) << _buffer.str() << endl;
        _out_stream->flush();
        _buffer.str("");
    }


    // take in a function with the custom signature
    Logger& Logger::operator<<(Logger::LoggerManipulator manip)
    {
        // call the function, and return it's value
        return manip(*this);
    }

    // define an operator<< to take in std::endl
    Logger& Logger::operator<<(Logger::StandardEndLine manip)
    {
        flush();
        *_out_stream << std::endl;
        return *this;
    }

    //values are identical to CSP macros for unified integration to ACS
    const uint32 Logger::INFO    = 1;
    const uint32 Logger::NOTICE  = 5;
    const uint32 Logger::WARNING = 2;
    const uint32 Logger::ERROR   = 3;
    const uint32 Logger::ALERT   = 4;


    InfoLogger::InfoLogger() : Logger()
    {
    }
    InfoLogger::~InfoLogger()
    {
    }

    void InfoLogger::flush()
    {
        if (_buffer.str().size() == 0)
            return;

        const lock_guard<mutex> lock(_log_fence);
#ifdef ACS_BUILD
        acs_log(INFO, _buffer.str().c_str());
#else
        (*_out_stream) << NowString() << " - " << _buffer.str() << endl;
        _out_stream->flush();
#endif
        _buffer.str("");
    }

    NoticeLogger::NoticeLogger() : Logger()
    {
    }

    NoticeLogger::~NoticeLogger()
    {
    }


    void NoticeLogger::flush()
    {
        const lock_guard<mutex> lock(_log_fence);
#ifdef ACS_BUILD
        acs_log(NOTICE, _buffer.str().c_str());
#else

        (*_out_stream) << green << NowString() << " - " << _buffer.str() << no_color << endl;
        _out_stream->flush();
#endif
        _buffer.str("");
    }

    WarningLogger::WarningLogger() : Logger()
    {
    }
    WarningLogger::~WarningLogger()
    {
    }

    void WarningLogger::flush()
    {
        const lock_guard<mutex> lock(_log_fence);
#ifdef ACS_BUILD
        acs_log(WARNING, _buffer.str().c_str());
#else
        (*_out_stream) << yellow << NowString() << " - " << _buffer.str() << no_color << endl;
        _out_stream->flush();
#endif
        _buffer.str("");
    }


    ErrorLogger::ErrorLogger() : Logger(&std::cerr)
    {
    }
    ErrorLogger::~ErrorLogger()
    {
    }

    void ErrorLogger::flush()
    {
        const lock_guard<mutex> lock(_log_fence);
#ifdef ACS_BUILD
        acs_log(ERROR, _buffer.str().c_str());
#else
        (*_out_stream) << light_red << NowString() << " - " << _buffer.str() << no_color << endl;
        _out_stream->flush();
#endif
        _buffer.str("");
    }

    AlertLogger::AlertLogger() : Logger(&std::cerr)
    {
    }
    AlertLogger::~AlertLogger()
    {
    }

    void AlertLogger::flush()
    {
        const lock_guard<mutex> lock(_log_fence);
#ifdef ACS_BUILD
        acs_log(ALERT, _buffer.str().c_str());
#else
        (*_out_stream) << light_red << NowString() << " - " << _buffer.str() << no_color << endl;
        _out_stream->flush();
#endif
        _buffer.str("");
    }

    InfoLogger    ADH_info;
    NoticeLogger  ADH_notice;
    WarningLogger ADH_warn;
    ErrorLogger   ADH_error;
    AlertLogger   ADH_alert;
}; //namespace Core
}; //namespace ADH

