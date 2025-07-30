#ifndef OFits_H
#define OFits_H

/**
 *  @file OFits.h
 *
 *  @brief Plain FITS binary tables writer
 *
 */

#include <string>
#include <string.h>
#include <algorithm>
#include <sstream>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>
#include <algorithm>
#include <stdexcept>

#define GCC_VERSION (__GNUC__ * 10000 + __GNUC_MINOR__ * 100 + __GNUC_PATCHLEVEL__)

#include "FitsDefs.h"
#include "Checksum.h"


#include <sys/file.h>


// Sloppy:  allow / <--- left
//          allow all characters (see specs for what is possible)

// units: m kg s rad sr K A mol cd Hz J W V N Pa C Ohm S F Wb T Hlm lx

class OFits : public std::ofstream
{
public:
    struct Key
    {
        std::string key;
        bool        delim;
        std::string value;
        std::string comment;
        std::string fitsString;

        off_t offset;   // offset in file

        bool changed;   // For closing the file

        Key(const std::string &k="");

        std::string Trim(const std::string &str);

        bool FormatKey();

        bool FormatComment();

        bool check(bool trim=false);

        size_t CalcSize() const;

        std::string Compile();

        Checksum checksum;

        void Out(std::ofstream &fout);

    };

protected:
    std::vector<Key> fKeys;

    std::vector<Key>::iterator findkey(const std::string &key);

    bool Set(const std::string &key="", bool delim=false, const std::string &value="", const std::string &comment="");

protected:
    struct Table
    {
        off_t offset;

        size_t bytes_per_row;
        size_t num_rows;
        size_t num_cols;

        struct Column
        {
            std::string name;
            size_t offset;
            size_t num;
            size_t size;
            char   type;
        };

        std::vector<Column> cols;

        Table() : offset(0), bytes_per_row(0), num_rows(0), num_cols(0)
        {
        }
    };


    Table fTable;

    std::vector<char> fOutputBuffer;

    std::vector<Table::Column>::const_iterator findcol(const std::string &name);

    Checksum fDataSum;
    Checksum fHeaderSum;

    bool fCommentTrimming;
    bool fManualExtName;

    size_t fTableStart; ///< Start offset from start of file (in bytes) of the current table

public:
    OFits();
    OFits(const char *fname);
    virtual ~OFits();

    virtual void open(const char * filename, bool addEXTNAMEKey=true);

    void AllowCommentsTrimming(bool allow);
    //Etienne: required to enable 1 to 1 reconstruction of files
    bool SetKeyComment(const std::string& key, const std::string& comment);
    bool SetKeyFromFitsString(const std::string& fitsString);
    bool SetRaw(const std::string &key, const std::string &val, const std::string &comment);

    bool SetBool(const std::string &key, bool b, const std::string &comment="");

    bool AddEmpty(const std::string &key, const std::string &comment="");

    bool SetStr(const std::string &key, std::string s, const std::string &comment="");

    bool SetInt(const std::string &key, int64_t i, const std::string &comment="");
    bool SetUInt(const std::string &key, uint64_t i, const std::string &comment="");

    bool SetFloat(const std::string &key, double f, int p, const std::string &comment="");

    bool SetFloat(const std::string &key, double f, const std::string &comment="");

    bool SetHex(const std::string &key, uint64_t i, const std::string &comment="");

    bool AddComment(const std::string &comment);

    bool AddHistory(const std::string &comment);

    void End();

    std::string CommentFromType(char type);

    uint32_t SizeFromType(char type);
    //ETIENNE to be able to restore the file 1 to 1, I must restore the header keys myself
    virtual bool AddColumn(uint32_t cnt, char typechar, const std::string &name, const std::string &unit, const std::string &comment="", bool addHeaderKeys=true);

    virtual bool AddColumn(const FITS::Compression&, uint32_t cnt, char typechar, const std::string& name, const std::string& unit,  const std::string& comment="", bool addHeaderKeys=true)
    {
        return AddColumn(cnt, typechar, name, unit, comment, addHeaderKeys);
    }

    bool AddColumnShort(uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(cnt, 'I', name, unit, comment); }
    bool AddColumnInt(uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(cnt, 'J', name, unit, comment); }
    bool AddColumnLong(uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(cnt, 'K', name, unit, comment); }
    bool AddColumnFloat(uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(cnt, 'E', name, unit, comment); }
    bool AddColumnDouble(uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(cnt, 'D', name, unit, comment); }
    bool AddColumnChar(uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(cnt, 'A', name, unit, comment); }
    bool AddColumnByte(uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(cnt, 'B', name, unit, comment); }
    bool AddColumnBool(uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(cnt, 'L', name, unit, comment); }

    bool AddColumnShort(const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(1, 'I', name, unit, comment); }
    bool AddColumnInt(const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(1, 'J', name, unit, comment); }
    bool AddColumnLong(const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(1, 'K', name, unit, comment); }
    bool AddColumnFloat(const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(1, 'E', name, unit, comment); }
    bool AddColumnDouble(const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(1, 'D', name, unit, comment); }
    bool AddColumnChar(const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(1, 'A', name, unit, comment); }
    bool AddColumnByte(const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(1, 'B', name, unit, comment); }
    bool AddColumnBool(const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(1, 'L', name, unit, comment); }

    bool AddColumnShort(const FITS::Compression &comp, uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, cnt, 'I', name, unit, comment); }
    bool AddColumnInt(const FITS::Compression &comp, uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, cnt, 'J', name, unit, comment); }
    bool AddColumnLong(const FITS::Compression &comp, uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, cnt, 'K', name, unit, comment); }
    bool AddColumnFloat(const FITS::Compression &comp, uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, cnt, 'E', name, unit, comment); }
    bool AddColumnDouble(const FITS::Compression &comp, uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, cnt, 'D', name, unit, comment); }
    bool AddColumnChar(const FITS::Compression &comp, uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, cnt, 'A', name, unit, comment); }
    bool AddColumnByte(const FITS::Compression &comp, uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, cnt, 'B', name, unit, comment); }
    bool AddColumnBool(const FITS::Compression &comp, uint32_t cnt, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, cnt, 'L', name, unit, comment); }

    bool AddColumnSignedByte(const FITS::Compression& comp, uint32_t cnt, const std::string& name, const std::string& unit="", const std::string& comment="")
    { return AddColumn(comp, cnt, 'S', name, unit, comment); }
    bool AddColumnUnsignedShort(const FITS::Compression& comp, uint32_t cnt, const std::string& name, const std::string& unit="", const std::string& comment="")
    { return AddColumn(comp, cnt, 'U', name, unit, comment); }
    bool AddColumnUnsignedInt(const FITS::Compression& comp, uint32_t cnt, const std::string& name, const std::string& unit="", const std::string& comment="")
    { return AddColumn(comp, cnt, 'V', name, unit, comment); }
    bool AddColumnUnsignedLong(const FITS::Compression& comp, uint32_t cnt, const std::string& name, const std::string& unit="", const std::string& comment="")
    { return AddColumn(comp, cnt, 'W', name, unit, comment); }

    bool AddColumnShort(const FITS::Compression &comp, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, 1, 'I', name, unit, comment); }
    bool AddColumnInt(const FITS::Compression &comp, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, 1, 'J', name, unit, comment); }
    bool AddColumnLong(const FITS::Compression &comp, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, 1, 'K', name, unit, comment); }
    bool AddColumnFloat(const FITS::Compression &comp, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, 1, 'E', name, unit, comment); }
    bool AddColumnDouble(const FITS::Compression &comp, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, 1, 'D', name, unit, comment); }
    bool AddColumnChar(const FITS::Compression &comp, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, 1, 'A', name, unit, comment); }
    bool AddColumnByte(const FITS::Compression &comp, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, 1, 'B', name, unit, comment); }
    bool AddColumnBool(const FITS::Compression &comp, const std::string &name, const std::string &unit="", const std::string &comment="")
    { return AddColumn(comp, 1, 'L', name, unit, comment); }

    bool AddColumnSignedByte(const FITS::Compression& comp, const std::string& name, const std::string& unit="", const std::string& comment="")
    { return AddColumn(comp, 1, 'S', name, unit, comment); }
    bool AddColumnUnsignedShort(const FITS::Compression& comp, const std::string& name, const std::string& unit="", const std::string& comment="")
    { return AddColumn(comp, 1, 'U', name, unit, comment); }
    bool AddColumnUnsignedInt(const FITS::Compression& comp, const std::string& name, const std::string& unit="", const std::string& comment="")
    { return AddColumn(comp, 1, 'V', name, unit, comment); }
    bool AddColumnUnsignedLong(const FITS::Compression& comp, const std::string& name, const std::string& unit="", const std::string& comment="")
    { return AddColumn(comp, 1, 'W', name, unit, comment); }

    Checksum WriteHeader(std::ofstream &fout);

    Checksum WriteHeader();

    void FlushHeader();

    Checksum WriteFitsHeader();

    virtual bool WriteDrsOffsetsTable ();

    virtual bool WriteCatalog();

    virtual bool WriteTableHeader(const char *name="DATA");

    template<size_t N>
        void revcpy(char *dest, const char *src, int num)
    {
        const char *pend = src + num*N;
        for (const char *ptr = src; ptr<pend; ptr+=N, dest+=N)
            std::reverse_copy(ptr, ptr+N, dest);
    }

    virtual uint32_t GetBytesPerRow() const;

    virtual bool WriteRow(const void *ptr, size_t cnt, bool byte_swap=true);

    template<typename N>
    bool WriteRow(const std::vector<N> &vec)
    {
        return WriteRow(vec.data(), vec.size()*sizeof(N));
    }

    // Flushes the number of rows to the header on disk
    virtual void FlushNumRows();

    size_t GetNumRows() const;

    void AlignTo2880Bytes();

    Checksum UpdateHeaderChecksum();
    virtual bool close();

    std::pair<std::string, int> GetChecksumData();

    void SetDefaultKeys();

    FILE* fCurrentFileDescriptor;
};

#endif //OFits_H
