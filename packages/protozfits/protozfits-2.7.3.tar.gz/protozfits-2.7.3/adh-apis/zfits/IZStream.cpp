/**
 * @file IZStream.cpp
 *
 * @brief overload of ifstream to also handle gzipped streams
 *
 * author: bretz
 *
 */
#include "IZStream.h"


    int IZStream::underflow()
    {
        if (gptr() && gptr()<egptr())
            return * reinterpret_cast<unsigned char *>(gptr());

        if (!is_open())
            return EOF;

        // gptr()-eback(): if more than four bytes are already flushed
        const int iputback = gptr()-eback()>4 ? 4 : gptr()-eback();

        // Copy the last four bytes flushed into the putback area
        memcpy(fBuffer+(4-iputback), gptr()-iputback, iputback);

        // Fill the buffer starting at the current file position and reset buffer
        // pointers by calling setg
        const int num = gzread(fFile, fBuffer+4, fgBufferSize-4);
        if (num <= 0) // ERROR or EOF
            return EOF;

        // reset buffer pointers
        setg(fBuffer+(4-iputback), fBuffer+4, fBuffer+4+num);

        // return next character
        return *reinterpret_cast<unsigned char *>(gptr());
    }


    IZStream::IZStream() : std::istream(this), fFile(0)
    {
        fBuffer = new char[fgBufferSize];
        setg(fBuffer+4, fBuffer+4, fBuffer+4);
    }
    IZStream::IZStream(const char *name) : std::istream(this), fFile(0)
    {
        fBuffer = new char[fgBufferSize];
        setg(fBuffer+4, fBuffer+4, fBuffer+4);
        open(name);
    }
    IZStream::~IZStream() { IZStream::close(); delete [] fBuffer; }

    int IZStream::is_open() { return fFile!=0; }

    // --------------------------------------------------------------------------
    //
    // Open a file by name. Test if it is open like for an ifstream
    // It doesn't matter whether the file is gzip compressed or not.
    //
    void IZStream::open(const char* name)
    {
        if (is_open())
        {
            clear(rdstate()|std::ios::failbit);
            return;
        }

        fFile = gzopen(name, "rb");
        if (fFile == 0)
        {
            clear(rdstate()|std::ios::failbit);
            return;
        }
    }
    // --------------------------------------------------------------------------
    //
    // Close an open file.
    //
    void IZStream::close()
    {
        if (!is_open())
            return;

        if (gzclose(fFile) != Z_OK)
            clear(rdstate()|std::ios::failbit);

        fFile = 0;
    }

    std::streambuf::pos_type IZStream::seekoff(std::streambuf::off_type offset, std::ios_base::seekdir dir,
                                     std::ios_base::openmode)
    {
        // Using a switch instead results in:
        //  In member function `virtual std::streampos izstream::seekoff(long int, std::_Ios_Seekdir, std::_Ios_Openmode)':
        //  warning: enumeration value `_M_ios_seekdir_end' not handled in switch
        //  warning: case value `0' not in enumerated type `_Ios_Seekdir'
        //  warning: case value `1' not in enumerated type `_Ios_Seekdir'
        //  warning: case value `2' not in enumerated type `_Ios_Seekdir'

        if (dir==std::ios::end)
        {
            clear(rdstate()|std::ios::failbit);
            return EOF;
        }

        // We only do relative seeking to avoid unnecessary decompression
        // of the whole file
        if (dir==std::ios::beg)
            offset -= tellg();

        // Calculate future position in streambuffer
        const char *ptr = gptr()+offset;

        // This is the number of bytes still available in the buffer
        const size_t sbuf = egptr()-gptr();

        // Check if the new position will still be in the buffer
        // In this case the target data was already decompressed.
        if (ptr>=eback() && ptr<egptr())
        {
            // Absolute position in z-stream
            const z_off_t zpos = gztell(fFile)-sbuf; //gzseek(fFile, 0, SEEK_CUR);

            gbump(offset);

            return zpos+offset;
        }

        const std::streampos pos = gzseek(fFile, offset-sbuf, SEEK_CUR);

        // Buffer is empty - force refilling
        setg(fBuffer+4, fBuffer+4, fBuffer+4);

        return pos<0 ? std::streampos(EOF) : pos;

        return EOF;
    }

    std::streambuf::pos_type IZStream::seekpos(std::streambuf::pos_type pos,
                                     std::ios_base::openmode)
    {
        return seekoff(pos, std::ios::beg);
    }

