/**
 * @file ThreadedObject.cpp
 *
 * @brief Simplifies the use of threads
 *  Created on: Aug 16, 2013
 *      Author: lyard
 */

#include "ThreadedObject.h"

#include <unistd.h>
#include <stdexcept>
#include <signal.h>

#include <iostream>

using namespace std;

namespace ADH
{
namespace Core
{

/******************************************************************************
*       CONSTRUCTOR
*******************************************************************************/
ThreadedObject::ThreadedObject() : _continue(false),
                                   _running(false),
                                   _handle(0),
                                   _started(false)
{

}

/******************************************************************************
 *      DESTRUCTOR
 ******************************************************************************/
ThreadedObject::~ThreadedObject()
{
    if (_handle != 0)
        pthread_join(_handle, NULL);

    _handle=0;
}

/******************************************************************************
 *      START
 ******************************************************************************/
void ThreadedObject::start(void (*signal_handler)(int))
{

    if (_running)
        throw runtime_error("You are trying to start a thread "
                            "that is already running");

    _continue = true;
    _started = false;

    thread_init();

    register_signals(signal_handler);

    if (pthread_create(&_handle, NULL, mainLoop, this))
        throw runtime_error("Thread cannot be started...");

    while (!_started)
        usleep(1000);
}

/******************************************************************************
 *      REGISTER SIGNAL.
 ******************************************************************************/
void ThreadedObject::register_signals(void (*signal_handler)(int))
{
    if (signal_handler == NULL)
        return;

    struct sigaction action;
    action.sa_handler = signal_handler;
    action.sa_flags   = 0;
    sigemptyset(&action.sa_mask);
    sigaction(SIGINT, &action, NULL);
    sigaction(SIGTERM, &action, NULL);
}

/******************************************************************************
 *      STOP
 ******************************************************************************/
void ThreadedObject::stop()
{
    if (!_running)
        return;

    _continue = false;
    pthread_join(_handle, NULL);
    _handle=0;
}

/******************************************************************************
 *      JOIN
 ******************************************************************************/
void ThreadedObject::join()
{
    if (!_running)
        return;

    pthread_join(_handle, NULL);
    _handle=0;
}

/******************************************************************************
 *      IS RUNNING
 ******************************************************************************/
bool ThreadedObject::isRunning()
{
    return _running;
}

/******************************************************************************
 *      THREAD INIT
 ******************************************************************************/
void ThreadedObject::thread_init()
{

}

/******************************************************************************
 *      THREAD LOOP
 ******************************************************************************/
void ThreadedObject::thread_loop()
{
    sleep(1);
};

/******************************************************************************
 *      THREAD DESTROY
 ******************************************************************************/
void ThreadedObject::thread_destroy()
{

}

/******************************************************************************
 *      DUMMY SIGNAL FUNCTION
 ******************************************************************************/
int ThreadedObject::_thread_interrupted = 0;

void ThreadedObject::dummy_signal_function(int signal)
{
    cout << "The threaded object catched a signal..." << endl;
    _thread_interrupted++;
}

/******************************************************************************
 *      MAIN LOOP
 ******************************************************************************/
void* ThreadedObject::mainLoop(void* context)
{
    //get object from context
    ThreadedObject* me = static_cast<ThreadedObject*>(context);

    //we did start indeed
    me->_started = true;

    //we are running
    me->_running = true;

    //loop until instructed to do otherwise
    while (me->_continue)
        me->thread_loop();

    //call object's destruction method
    me->thread_destroy();

    //we are not running any longer
    me->_running = false;

    return NULL;
}

}; //namespace Core
}; //namespace ADH
