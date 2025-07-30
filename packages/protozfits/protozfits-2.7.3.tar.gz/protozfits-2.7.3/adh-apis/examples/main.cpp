#include <memory>
#include <FlatProtobufZOFits.h>
#include <DL0v1_Telescope.pb.h>

using DL0v1::Telescope::Event;


int main() {
    ADH::IO::FlatProtobufZOFits f{10, 100, 10000000, "raw", 2, 1000000};
    f.open("test.fits.fz");
    f.moveToNewTable("EVENTS");

    // c++11, in c++14 use make_unique instead
    auto event = std::unique_ptr<Event>(new Event());
    event->set_event_id(1);
    event->set_tel_id(1);

    // FlatProtobufZOFits takes ownership of event!
    f.writeMessage(event.release());
    return 0;
}
