/*
 * Logger.h
 *
 *  Created on: Jul 11, 2016
 *      Author: lyard
 */

#ifndef CORE_LOGGER_H_
#define CORE_LOGGER_H_

#include <iostream>
#include <fstream>
#include <sstream>

#include <mutex>

#include "BasicDefs.h"

namespace ADH
{
namespace Core
{
    class Logger
    {

    public:
        Logger(std::ostream* output = &std::cout);

        virtual ~Logger();

        template <typename T_>
        Logger& operator <<(const T_& value)
        {
            std::lock_guard<std::mutex> lock(_log_fence);
            _buffer << value;
           return *this;
        }

        virtual void flush();

        //Functors for handling std::endl properly
        // function that takes a custom stream, and returns it
        typedef Logger& (*LoggerManipulator)(Logger&);

        // take in a function with the custom signature
        Logger& operator<<(LoggerManipulator manip);

        // this is the type of std::cout
        typedef std::basic_ostream<char, std::char_traits<char> > CoutType;

        // this is the function signature of std::endl
        typedef CoutType& (*StandardEndLine)(CoutType&);

        // define an operator<< to take in std::endl
        Logger& operator<<(StandardEndLine manip);

        //values are identical to ACS enums defined in loggingBaseLog.h, to ease translation (saves on case-switch)
        static const uint32 INFO;
        static const uint32 NOTICE;
        static const uint32 WARNING;
        static const uint32 ERROR;
        static const uint32 ALERT;

    protected:
        std::mutex         _log_fence;
        std::ostringstream _buffer;
        std::ostream*      _out_stream;
    };

    class InfoLogger : public Logger
    {
        public:
                    InfoLogger();
            virtual ~InfoLogger();
            void    flush();
    };

    class NoticeLogger : public Logger
    {
        public:
                    NoticeLogger();
            virtual ~NoticeLogger();
            void    flush();
    };

    class WarningLogger : public Logger
    {
        public:
                    WarningLogger();
            virtual ~WarningLogger();
            void    flush();
    };

    class ErrorLogger : public Logger
    {
        public:
                    ErrorLogger();
            virtual ~ErrorLogger();
            void    flush();
    };

    class AlertLogger : public Logger
    {
        public:
                AlertLogger();
            virtual ~AlertLogger();
            void    flush();
    };

    extern InfoLogger    ADH_info;
    extern NoticeLogger  ADH_notice;
    extern WarningLogger ADH_warn;
    extern ErrorLogger   ADH_error;
    extern AlertLogger   ADH_alert;

}; //namespace Core
}; //namespace ADH



#endif /* CORE_LOGGER_H_ */
