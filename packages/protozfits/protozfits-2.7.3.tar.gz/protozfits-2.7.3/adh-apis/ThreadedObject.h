/**
 * @file ThreadedObject.h
 *
 * @brief Simplifies the use of threads
 *  Created on: Aug 16, 2013
 *      Author: lyard
 */

#ifndef THREADED_OBJECT_H_
#define THREADED_OBJECT_H_

#include <pthread.h>

namespace ADH
{
namespace Core
{
    /*
     *      @class ThreadedObject
     *      @brief base class to easily use a separate thread
     *
     *      This class simplify the startup and control of threads. It handles
     *      everything, all that one should do is derive the thread_ methods.
     *      Warning: no sleep is called between calls to thread_loop. So sleep
     *      time should be implemented by the derived class
     *
     */
    class ThreadedObject
    {
        public:
            //! @brief default constructor
            ThreadedObject();

            //! @brief default destructor
            virtual ~ThreadedObject();

            //! @brief start the thread. If a signal handler is given,
            //! it will handle SIGINT and SIGTERM by default. the function
            //! register_signals can be be overriden if needed. Enabling
            //! this signal handling will disable the one implemented by ZMQ
            virtual void start(void (*signal_handler)(int) = NULL);

            //! @brief stop the thread
            virtual void stop();

            //! @brief whether the thread is running or not
            bool isRunning();

            //! @brief wait for the thread to finish naturally
            virtual void join();

        protected:
            //! @brief initializes the class before starting the thread.
            //! Must be implemented by the derived class
            virtual void thread_init();

            //! @brief Main thread loop. This method is called over and
            //! over while the thread is running. Must be implemented by
            //! the derived class
            virtual void thread_loop();

            //! @brief actions to be taken after the thread stops running.
            //! Must be implemented by the derived class

            virtual void thread_destroy();
            //! @brief setup of the signals handling by the thread. Called
            //! by the start() method, only if the signal_handler parameter
            // is not null
            virtual void register_signals(void (*signal_handler)(int));

            //! @brief a dummy signal handler, just prints a text on the
            //! screen and increment the member variable _interrupted
            static void dummy_signal_function(int signal);

            /// Should the thread be running or not
            bool       _continue;

            /// Is the thread currently running or not
            bool       _running;

            /// Low-level handle of the thread
            pthread_t  _handle;

            /// Interger to register that the threaded object was interrupted
            static int _thread_interrupted;

            /// Boolean to let the start() method know that it can return
            bool       _started;

        private:

            //! @brief this is the actual method that gets called.
            //! It then calls the other, derived-class implemented
            //! thread_ methods
            static void* mainLoop(void* context);
    };
}; //namespace Core
}; //namespace ADH

#endif /* THREADED_OBJECT_H_ */
