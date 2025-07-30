/**
 *
 * @file IZStream.h
 *
 * @brief overload of ifstream to also handle gzipped streams
 *
 * author: bretz
 *
 */

#ifndef IZStream_H
#define IZStream_H

#include <string.h>

#include <istream>
#include <streambuf>

#include <zlib.h>

class IZStream : public std::streambuf,
                 public std::istream
{
    private:
        static const int fgBufferSize = 2048*1024*2;

        gzFile fFile;   // file handle for compressed file
        char  *fBuffer; // data buffer

        int underflow();

    public:
        IZStream();
        IZStream(const char *name);
        virtual ~IZStream();

        int is_open();

        // --------------------------------------------------------------------------
        //
        // Open a file by name. Test if it is open like for an ifstream
        // It doesn't matter whether the file is gzip compressed or not.
        //
        void open(const char* name);

        // --------------------------------------------------------------------------
        //
        // Close an open file.
        //
        void close();

        std::streambuf::pos_type seekoff(std::streambuf::off_type offset, std::ios_base::seekdir dir,
                                         std::ios_base::openmode = std::ios_base::in);

        std::streambuf::pos_type seekpos(std::streambuf::pos_type pos,
                                         std::ios_base::openmode = std::ios_base::in);
};

#endif //IZStream_H
