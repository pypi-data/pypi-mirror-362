/**
 * @file AnyArrayHelper.h
 *
 * @brief Bundle of helper function to access AnyArray objects conveniently (including the AnyArrayStreamer class)
 *
 *  Created on: Sep 3, 2014
 *      Author: lyard
 */

#ifndef ANY_ARRAY_HELPER_H_
#define ANY_ARRAY_HELPER_H_

#include "CoreMessages.pb.h"
#include <stdexcept>
#include <iostream>
#include <sstream>
#include <typeinfo>

using namespace std;

namespace ADH
{
/** @namespace ADH::AnyArrayHelper
 *  @brief A collection of global helper functions and classes to access AnyArray objects conveniently
 *
 */
namespace AnyArrayHelper
{
    /**
     *  @brief retrieves the CTAType enumeration corresponding to a fundamental type
     *  @tparam _T fundamental type for which the CTA enum should be retrieved, e.g. int16 gives AnyArray::S16
     *  @return the AnyArray enum corresponding to this fundamental type
     *  @throw runtime_error if the given template type is not known by the object
     *  @todo The idea to use template was to specialize the function. Right now it is using typeid and a collection of ifs... Oh boy this is ugly
     */
    template<typename _T>
    AnyArray::ItemType getItemType()
    {
          if (typeid(_T) == typeid(void))
        return AnyArray::NONE;
          else if (typeid(_T) == typeid(char))
        return AnyArray::S8;
          else if (typeid(_T) == typeid(unsigned char))
        return AnyArray::U8;
          else if (typeid(_T) == typeid(google::protobuf::int8))
        return AnyArray::S8;
          else if (typeid(_T) == typeid(google::protobuf::uint8))
        return AnyArray::U8;
          else if (typeid(_T) == typeid(google::protobuf::int16))
        return AnyArray::S16;
          else if (typeid(_T) == typeid(google::protobuf::uint16))
        return AnyArray::U16;
          else if (typeid(_T) == typeid(google::protobuf::int32))
        return AnyArray::S32;
          else if (typeid(_T) == typeid(google::protobuf::uint32))
        return AnyArray::U32;
          else if (typeid(_T) == typeid(google::protobuf::int64))
        return AnyArray::S64;
          else if (typeid(_T) == typeid(google::protobuf::uint64))
        return AnyArray::U64;
          else if (typeid(_T) == typeid(float))
        return AnyArray::FLOAT;
          else if (typeid(_T) == typeid(double))
        return AnyArray::DOUBLE;
          else if (typeid(_T) == typeid(bool))
        return AnyArray::BOOL;
          else
        {
            throw std::runtime_error("Unhandled typeid case while checking a cta array. Maybe you requested a pointer type ?? if so, the * should be dropped form the template parameter");
        }
      return AnyArray::NONE;
    }

    /**
     *  @brief Get the array as a pointer to a mutable C-array of the desired size
     *  @tparam _T the type of the array elements to retrieve the pointer for
     *  @return a pointer to a mutable C-array of the desired type
     *  @param input A pointer to the AnyArray that must be transformed
     *  @param num_items the number of elements that the array must be able to store. The AnyArray is resized accordingly
     */
    template<typename _T>
    _T* reallocAs(AnyArray* input, google::protobuf::uint32 num_items)
    {
        //FIXME do this only in Debug mode, i.e. add macro guards
        if (input->has_type() &&
            input->type() != getItemType<_T>())
        {
            std::ostringstream str;
            str << "It sounds quite dangerous to modify the type of an existing anyarray so we currently throw an exception. ";
            str << " current type: " << input->type() << " being set: " << getItemType<_T>();
            throw std::runtime_error(str.str());
        }

        input->set_type(getItemType<_T>());

        std::string* data = input->mutable_data();

        if (data->size() != num_items*sizeof(_T))
            data->resize(num_items*sizeof(_T));

        return reinterpret_cast<_T*>(&((*(data))[0]));
    }

    template<typename _T>
    void copyArrayAs(AnyArray* output, _T* input, google::protobuf::uint32 num_items)
    {
        _T* target = reallocAs<_T>(output, num_items);
        memcpy(target, input, num_items*sizeof(_T));
    }

    std::string toString(const AnyArray&);

    std::string CTATypeString(const AnyArray::ItemType& type);

    /**
     *  @brief Get the array as a pointer to a constant C-array.
     *
     *  This function verifies that the type of the template matches the type of the AnyArray
     *  @tparam _T The type  of data the the user believes is in the array
     *  @param input A reference to the AnyArray that must be accessed
     *  @return a const pointer to a mutable C-array of the desired type
     *  @throw runtime_error if the AnyArray type does not match the template type
     *  @todo Put IFDEFs to make the data type check only active in DEBUG configuration
     */
    template<typename _T>
    const _T* readAs(const AnyArray& input)
    {
	if (input.data().size() == 0)
		return NULL;
        //TODO add some debug checks for the contained type
        if (input.type() != getItemType<_T>())
        {
            if (!input.type() && input.data().size() != 0)
	{
		ostringstream str;
str << "Size of the data: " << input.data().size() << " desired type: " << CTATypeString(getItemType<_T>());
                throw std::runtime_error(str.str());
}
            std::ostringstream str;
            str << "You accessed an AnyArray using the wrong type: " << CTATypeString(getItemType<_T>()) << " while the array is of type " << CTATypeString(input.type());
            throw std::runtime_error(str.str());
        }
        return reinterpret_cast<const _T*>(input.data().data());
    }

    //! @brief Retrieve the number of elements stored in a AnyArray
    //! @param input the AnyArray to look for the number of elements
    //! @param the number of elements stored in input
    google::protobuf::uint32 getNumElems(const AnyArray& input);

    //! @brief same as getNumElems except number of bytes is returns instead of number of elements
    google::protobuf::uint32 getNumBytes(const AnyArray& input);

    //! @brief Same as the other getNumElems function, only for pointer parameter
    google::protobuf::uint32 getNumElems(const AnyArray* input);

    //! @brief Same as the other getNumBytes function, only for pointer parameter
    google::protobuf::uint32 getNumBytes(const AnyArray* input);

    template<typename _T>
    _T* modifyAs(AnyArray* input)
    {
        if (input->type() != getItemType<_T>())
        {
            if (!input->type())
                throw std::runtime_error("You tried to modify an AnyArray that was not properly set: the type of its elements is missing");

            std::ostringstream str;
            str << "You tried to modify an AnyArray using the wrong type: " << CTATypeString(getItemType<_T>()) << " while the array is of type " << CTATypeString(input->type());
            throw std::runtime_error(str.str());
        }

        return reinterpret_cast<_T*>(&input->mutable_data()->front());
    }


    /**
     *  @brief Copy the values of a C-style array to a AnyArray
     *
     *  @tparam _T The type of the elements of the input array
     *  @param output A reference to the AnyArray that must be filled in with the values from input
     *  @param input A const pointer to the values that must be copied to the AnyArray
     *  @param num_elems the number of elements of type _T stored in input
     */
    template<typename _T>
    void assignTo(AnyArray& output, const _T* input, google::protobuf::uint32 num_elems)
    {
        if (output.mutable_data()->size() < num_elems*sizeof(_T))
            output.mutable_data()->resize(num_elems*sizeof(_T));

        _T* raw_array = reallocAs<_T>(&output, num_elems);

        memcpy((char*)(raw_array), input, num_elems*sizeof(_T));
    }

    /**
     *  @brief Same as the other set function, only with a pointer to the AnyArray
     */
    template<typename _T>
    void assignTo(AnyArray* output, const _T* input, google::protobuf::uint32 num_elems)
    {
      return assignTo(*output, input, num_elems);
    }

    template<typename _T>
    void assignTo(AnyArray* output, const char* input, google::protobuf::uint32 num_elems)
    {
        return assignTo<_T>(output, reinterpret_cast<const _T*>(input), num_elems);
    }


    /**
     *  @brief A Streamer class to create AnyArray efficiently when the final array size is unkown
     *
     *  This streamer class works both for unitary elements, or with arrays of elements, depending on the size
     *  given to the constructor. If the size is != 1, then using the << operator taking a reference as R-value
     *  would raise an exception.
     *  @tparam _T The type of the elements that the array will be filled in with
     */
    template <typename _T>
    class AnyArrayStreamer
    {
        public:
            /**
             *  @brief Default constructor
             *  @param arraysize The number of elements that will be written by each << operation. If values > 1 are passed, then Only the * << operator can be used
             */
            AnyArrayStreamer(google::protobuf::int32 arraysize = 1) : _data("", std::ostream::binary),
                                                                      _array_size(arraysize) {};

            //! @brief empty the content of the streamer
            void make_empty() {_data.str("");}

            /**
             *  @brief assign the content of the streamer to a AnyArray. This operation empties the streamer
             *  @param target the AnyArray that must be filled in with the values
             */
            void assignTo (AnyArray& target)
            {
                target.set_type(getItemType<_T>());
                *(target.mutable_data()) = _data.str();
                make_empty();
            }

            //! @brief same as the other assign, only with a ponter instead of a reference
            //! @todo call the other function instead of copying the code
            void assignTo (AnyArray* target)
            {
                target->set_type(getItemType<_T>());
                *(target->mutable_data()) = _data.str();
                make_empty();
            }

            //! @brief Write operation for a single element
            //! @param input A reference to the element to write
            AnyArrayStreamer& operator << (const _T& input)
            {
                if (_array_size != 1)
                    throw std::runtime_error("Using atomic put operation in AnyArrayStreamer with an object that is not atomic");

                _data.write((char*)(&input), sizeof(_T));
                return *this;
            }

            //! @brief Write operation for single or multiple elements
            //! @param input A pointer to the element(s) to write
            AnyArrayStreamer& operator << (const _T* input)
            {
                _data.write((char*)(input), sizeof(_T)*_array_size);
                return *this;
            }

            size_t getNumElems() const { return _data.str().size() / sizeof(_T);}
            size_t getNumBytes() const { return _data.str().size();}
        private:
            std::ostringstream      _data;
            google::protobuf::int32 _array_size;
    };

    void printToScreen(const AnyArray& array);

} //namespace AnyArrayHelper
} //namespace ADH

#endif /* ANY_ARRAY_HELPER_H_ */
