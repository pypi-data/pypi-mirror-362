# adh-apis

Contains all the code common to both ADH internally, Cherenkov Camera servers and analysis reader. This project only builds relevant libraries to be used in your own
project. To build unit tests for this code the project ACADA/Array-data-handler should be used instead. 

Note: this repository previously contained the `protozfits` python package,
providing python bindings to `libZFitsIO`. This has now been moved into its own repository:
<https://gitlab.cta-observatory.org/cta-computing/common/protozfits-python>.

## Cloning

This module relies on third party code included via git submodules.
When cloning for the first time, make sure to add `--recursive`, i.e.

```bash
$ git clone --recursive git@gitlab.cta-observatory.org:cta-computing/common/acada-array-elements/adh-apis
```

To update the submodules, or if you forgot to add the `--recursive` when cloning, do
```bash
$ git submodule update --init --recursive
```

## Build requirements

To build this project, you need a c++11 capable compiler, cmake >= 3.15 and the following dependencies:

* libprotobuf and the protoc compiler
* zeromq
* zstd

### CentOS 7

```
$ sudo yum install epel-release
$ sudo yum install -y cmake3 make gcc gcc-c++ protobuf-devel zeromq-devel libzstd-devel
```

### AlmaLinux 9

```
sudo dnf install -y 'dnf-command(config-manager)'
sudo dnf config-manager -y --set-enabled crb
sudo dnf install -y epel-release
sudo dnf install -y cmake make gcc gcc-c++ protobuf-devel protobuf-compiler zeromq-devel zstd-devel
```


### Ubuntu

```
$ sudo apt update
$ sudo apt install -y cmake build-essential libzmq3-dev libzstd-dev libprotobuf-dev protobuf-compiler
```


## Build

To build the apis to directory `BUILD`, `cmake` should be invoked from the cloned root. e.g.
```bash
$ cmake -S . -B BUILD
$ cmake --build BUILD
$ cmake --install BUILD
```

To install to a non-standard path, add `-DCMAKE_INSTALL_PREFIX` to the first `cmake` call.

On CentOS 7, use `cmake3` instead of `cmake` or install an up-to-date CMake yourself.

## Example programs

There are 4 example programs which demonstrate the usage of the ADH APIs for 
dealing with Events and Trigger data. Currently only the R1 data format is used, DL0 will be added once its data model will be agreed.

Command lines given as examples below assume that the code was built according to the directions given above. Calling the programs without
any argument prints the help.

### Sending Cherenkov events from camera servers
Two executables are provided: `events_server` and `events_consumer` along with their source code `ExecExampleEventsServer.cpp` and `ExecExampleEventsConsumer.cpp` respectively.

The server creates dummy R1 events and sends them in a loop to the consumer, which then discards them. Obviously server and consumer should use the same port number. The following command lines would generate 100 events at ~10Hz on port 1234 before exiting:

```
BUILD/bin/events_server --port 1234 --sleep 100000 --total 100
```

If running the consumer on the same host its command line should be:
```
BUILD/bin/events_consumer --input tcp://localhost:1234
```

Otherwise `localhost` should be replaced by the hostname (or IP) running the server.

The total number of consumed messages should be 102: 100 events + 2 header messages. 


### Sending software triggers and listening for events requests
An executable is provided: `swat_client` along with its source code `ExecExampleSWATClient.cpp`.

The software exhibits the basic usage of the C++-based SWAT API in order to send triggers and receive requests. It configures the `SWAT_API_CLIENT` structure using a .ini file or programmed defaults, starts the underlying processing thread and creates three threads: first is responsible for event generation and submission, second reads and prints event information to stdout (for performance reasons it's recommended to redirect to a file), third catches signals in order to stop the software gracefully.

To test, clone the main ADH repository, build the software and start the standalone SWAT server (the steps below use a docker-based environment to simplify working with ACS-dependent software):
```
git clone --recurse-submodules git@gitlab.cta-observatory.org:cta-computing/acada/adh.git
cd adh
./docker_run
./build_all.sh
cd software-array-trigger/build/swat-prototype/
./swat_server -s -L <the UTC-TAI offset; currently: 37 (accurate at least until Dec 31 2021)>
```
A SWAT server started using the procedure outline above will run until stoppped with a SIGQUIT (for instance, a ctrl+\ keystroke).

To start the API example:
```
BUILD/bin/swat_client --file <ini configuration file path; example at swat/SWAT_config.ini> \ 
                      --IP <SWAT IP; 127.0.0.1 if server is on the same machine> \
                      --channel <telescope channel; use 0 for 1st instance 1 for 2nd and so on> \
                      >./events.log
```
The client generates events indefinitely until the process is stopped by a SIGINT (ctrl+C) signal (during preliminary testing at a rate of ~30k events per second).


# Flashcam-style API
Following the first round of discussions that occured between camera teams and ACADA, the Flashcam team requested a slightly different API. Discussions are not yet finalized and not everyone agree yet. Nevertheless, as the requested API was not so far from the proposed one, we implemented a first tentative wrapper around our proposal. The reasonning being that it doesn't matter if teams use slightly different APIs to fit their needs, as long as the underlying implementation of formats and protocols is indeed the same. 

Please note that this is a work in progress, and that even though the API is fairly well defined, it's implementation isn't fully finalized yet and was not tested much (if at all). We hope that it will help the discussion go forward to reach an agreement among all the teams. 

## API definition
The tentative adaptation is given in the file [R1CherenkovDataInterface.h](./R1CherenkovDataInterface.h). So far only the camera configuration and R1 event format are defined, as the DL0 data model remains to be decided. An abstract streaming interface is also provided in the same file. Doxygen user-friendly documentation of the interface can be generated as follow:

```
( cat Doxyfile ; echo "INPUT=R1CherenkovDataInterface.h" ) | doxygen -
```

And then the user needs to open the generated html/index into his/her favourite web browswer.

The namespaces names is only tentative and should be discussed with all stakeholders. 

An implementation based on protobuf and ZMQ is available in [R1CherenkovDataImpl.h](./R1CherenkovDataImpl.h)/[cpp](R1CherenkovDataImpl.cpp), and two examples are given in [ExecExampleEventsServerFlashcamStyle.cpp](./ExecExampleEventsServerFlashcamStyle.cpp) and [ExecExampleEventReaderFlashcamStyle.cpp](./ExecExampleEventsReaderFlashcamStyle.cpp). The server will generate a predefined number of events, while the reader reads this data and verifies its content. They can be used either via a network stream, or via files. Please note that the file implementation currently has no header of any kind, which would allow to link the binary data to the code that would be able to read it back. If there is a demand for this feature beyond the occasional quick-and-dirty test, we will work to improve the situation.

## Example usage
### Network usage
Here is an example configuration to exchange data via the network:

```
./events_server_flashcam --config "tcp://*:1235" --sleep 10000 --total 1000
```
This would send 1000 dummy events from port 1235, towards any interface, at a rate of 100Hz, while:

```
./events_reader_flashcam --config tcp://localhost:1235
```
Would read these events from localhost, and verify their content.

### File-based usage
Here is an example configuration to exchanage data via files:
```
./events_server_flashcam --config "/tmp/test_output.bin" --total 1000
```
this would write 1000 events to a file, while
```
./events_reader_flashcam --config "/tmp/test_output.bin"
```
Would read these events from the same file and verify their content. 

Existing files cannot be overriden, to prevent absent-minded users from overwriting valuable data.

Currently only the network interface can be used when writing and reading data in parallel. This is because the file-based implementation lacks the required mechanism to prevent the reader to overtake the writing, leading to corrupted events data. 

