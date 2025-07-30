#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cstdint>
#include <sstream>
#include <stdexcept>

#include "CMakeDefs.h"
#include "DL0v1_Subarray.pb.h"
#include "DL0v1_Telescope.pb.h"
#include "DL0v1_Trigger.pb.h"
#include "FlatProtobufZOFits.h"
#include "IFits.h"
#include "ProtoR1.pb.h"
#include "ProtobufIFits.h"
#include "R1v1.pb.h"
#include "ZIFits.h"

namespace py = pybind11;
using ADH::IO::FlatProtobufZOFits;
using ADH::IO::ProtobufIFits;

// It does not seem to be possible to hand over a python protobuf
// class to c++ via pybind11, we can only exchange the bytes
// however, then, we don't actually know which class we need to
// use on the C++ side, so we need to actually build a look up table
// using the descriptor names
template <typename Message>
void write_message(FlatProtobufZOFits& fits, const std::string& data) {
    auto msg = fits.getANewMessage<Message>();
    msg->ParseFromString(data);
    fits.writeMessage(msg);
}

void write_py_message(FlatProtobufZOFits& fits, py::object message) {
    // get the name of the protobuf object from the python side
    std::string name = message.attr("DESCRIPTOR").attr("full_name").cast<std::string>();
    std::string data = message.attr("SerializeToString")().cast<std::string>();

    // use it to figure out the C++ we need to use
    // CTAO R1
    if (name == "R1v1.Event") {
        write_message<R1v1::Event>(fits, data);
    } else if (name == "R1v1.CameraConfiguration") {
        write_message<R1v1::CameraConfiguration>(fits, data);
    } else if (name == "R1v1.TelescopeDataStream") {
        write_message<R1v1::TelescopeDataStream>(fits, data);
    } else if (name == "R1v1_debug.DebugEvent") {
        write_message<R1v1_debug::DebugEvent>(fits, data);
    } else if (name == "R1v1_debug.DebugCameraConfiguration") {
        write_message<R1v1_debug::DebugCameraConfiguration>(fits, data);
    }
    // CTAO DL0
    else if (name == "DL0v1.Telescope.DataStream") {
        write_message<DL0v1::Telescope::DataStream>(fits, data);
    } else if (name == "DL0v1.Telescope.CameraConfiguration") {
        write_message<DL0v1::Telescope::CameraConfiguration>(fits, data);
    } else if (name == "DL0v1.Telescope.Event") {
        write_message<DL0v1::Telescope::Event>(fits, data);
    } else if (name == "DL0v1.Subarray.DataStream") {
        write_message<DL0v1::Subarray::DataStream>(fits, data);
    } else if (name == "DL0v1.Subarray.Event") {
        write_message<DL0v1::Subarray::Event>(fits, data);
    } else if (name == "DL0v1.Trigger.DataStream") {
        write_message<DL0v1::Trigger::DataStream>(fits, data);
    } else if (name == "DL0v1.Trigger.Trigger") {
        write_message<DL0v1::Trigger::Trigger>(fits, data);
    }
    // old R1, used e.g. by LST commissioning data
    else if (name == "ProtoR1.CameraConfiguration") {
        write_message<ProtoR1::CameraConfiguration>(fits, data);
    } else if (name == "ProtoR1.CameraEvent") {
        write_message<ProtoR1::CameraEvent>(fits, data);
    } else {
        throw std::runtime_error(std::string{"Unknown protobuf class name "} + name);
    }
}

py::object header_value(const IFits::Entry& entry) {
    switch (entry.type) {
        case 'I':
            return py::cast(std::stol(entry.value));
        case 'B':
            return py::cast(entry.value == "T");
        case 'F':
            return py::cast(std::stod(entry.value));
        default:
            return py::cast(entry.value);
    }
}

void FlatProtobufZOFits_close(FlatProtobufZOFits& self) {
    self.close();
    self.flush();
}

void FlatProtobufZOFits_exit(FlatProtobufZOFits& self, py::handle, py::handle,
                             py::handle) {
    FlatProtobufZOFits_close(self);
}

PYBIND11_MODULE(rawzfits, m) {
    m.doc() = "Python bindings for protobuf zfits";
    m.attr("ADH_VERSION_MAJOR") = ADH_VERSION_MAJOR;
    m.attr("ADH_VERSION_MINOR") = ADH_VERSION_MINOR;
    m.attr("ADH_VERSION_PATCH") = ADH_VERSION_PATCH;

    py::class_<IFits::Table>(m, "Table", "A FITS binary table.")
        .def_readonly("name", &IFits::Table::name);

    py::class_<IFits>(m, "IFits", "Reader for standard FITS files.")
        .def(py::init<const std::string&, const std::string&>(), py::arg("file_path"),
             py::arg("table_name") = "")
        .def_property_readonly("header",
                               [](const IFits& self) { return self.GetTable().keys; })
        // the lambda enables ignoring self passed if the static method is called on an
        // instance and not the class
        .def_property_readonly("seen_tables", &IFits::listPastTables)
        .def_property_readonly("table", &IFits::GetTable)
        .def("has_next_table", &IFits::hasNextTable,
             "Returns True if there is another table after the current one")
        .def("open_next_table", &IFits::openNextTable, py::arg("force") = false,
             "Open the next table after the current one")
        .def("close", &IFits::close)
        .def("__enter__", [](IFits& self) { return py::cast(self); })
        .def("__exit__",
             [](IFits& self, py::handle, py::handle, py::handle) { self.close(); });

    py::class_<IFits::Entry>(m, "HeaderEntry", "A FITS header entry.")
        .def_readonly("type", &IFits::Entry::type)
        .def_property_readonly("value", header_value)
        .def_readonly("comment", &IFits::Entry::comment)
        .def_readonly("fits_string", &IFits::Entry::fitsString)
        .def("__repr__", [](const IFits::Entry& self) {
            return "HeaderEntry(value='" + self.value + "', comment='" + self.comment
                   + "')";
        });

    py::class_<ZIFits, IFits>(m, "ZIFits", "Reader for cta-compressed fits files.");

    py::class_<ProtobufIFits, ZIFits>(
        m, "ProtobufIFits", "Reader for cta-compressed fits files using protobuf.")
        .def(py::init<const std::string&, const std::string&>(), py::arg("file_path"),
             py::arg("table_name") = "")
        .def("check_if_file_is_consistent", &ProtobufIFits::CheckIfFileIsConsistent,
             py::arg("update_catalog") = false,
             "Check the file for defects. Raises an exception on found problems.")
        .def("__len__", &ProtobufIFits::getNumMessagesInTable,
             "Number of rows in the current table.")
        .def(
            "read_serialized_message",
            [](ProtobufIFits& fits, uint32 number) {
                if (number > fits.getNumMessagesInTable()) {
                    std::stringstream ss{};
                    ss << "Index " << number << " is out of bounds for table "
                       << "with length " << fits.getNumMessagesInTable();
                    throw std::out_of_range(ss.str());
                }
                return py::bytes(fits.readSerializedMessage(number));
            },
            py::arg("message_number"),
            "Read the specified message from the table.  ``message_number`` starts at "
            "1.");

    py::class_<FlatProtobufZOFits>(m, "ProtobufZOFits")
        .def(

            py::init<uint32_t, uint32_t, uint64_t, std::string, uint32_t, uint32_t>(),
            py::arg("n_tiles") = 1000, py::arg("rows_per_tile") = 100,  // NOLINT
            py::arg("max_compression_memory") = 1000000,                // NOLINT
            py::arg("default_compression") = "raw",
            py::arg("n_compression_threads") = 0,
            py::arg("compression_block_size_kb") = 1024)  // NOLINT
        .def("open", &FlatProtobufZOFits::open, py::arg("path"))
        .def("close", &FlatProtobufZOFits_close)
        .def("__enter__", [](FlatProtobufZOFits& self) { return py::cast(self); })
        .def("__exit__", &FlatProtobufZOFits_exit)
        .def("move_to_new_table", &FlatProtobufZOFits::moveToNewTable,
             py::arg("table_name") = "DATA", py::arg("display_stats") = false,
             py::arg("closing_file") = false)
        .def("write_message", &write_py_message, py::arg("message"))
        .def("set_default_compression", &FlatProtobufZOFits::setDefaultCompression,
             py::arg("compression"))
        .def("request_explicit_compression",
             &FlatProtobufZOFits::requestExplicitCompression, py::arg("field"),
             py::arg("compression"))
        .def("set_string", &FlatProtobufZOFits::setStr)
        .def("set_int", &FlatProtobufZOFits::setInt)
        .def("set_float", &FlatProtobufZOFits::setFloat)
        .def("set_bool", &FlatProtobufZOFits::setBool);
}
