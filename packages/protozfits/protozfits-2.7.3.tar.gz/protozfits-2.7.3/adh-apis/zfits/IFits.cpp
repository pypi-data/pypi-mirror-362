/**
 * @file IFits.cpp
 *
 * @brief Reads plain fits, possibly gzipped (i.e .fits or .fits.gz)
 *
 *  Created on: Nov 5, 2013
 *      Author: lyard-bretz
 */

#include "IFits.h"

#include <cstdint>
#include <iostream>

using namespace std;




        std::string IFits::Table::Trim(const std::string &str, char c) const
        {
            // Trim Both leading and trailing spaces
            const size_t pstart = str.find_first_not_of(c); // Find the first character position after excluding leading blank spaces
            const size_t pend   = str.find_last_not_of(c);  // Find the first character position from reverse af

            // if all spaces or empty return an empty string
            if (std::string::npos==pstart || std::string::npos==pend)
                return std::string();

            return str.substr(pstart, pend-pstart+1);
        }

        bool IFits::Table::Check(const std::string &key, char type, const std::string &value) const
        {
            const Keys::const_iterator it = keys.find(key);
            if (it==keys.end())
            {
                std::ostringstream str;
                str << "Key '" << key << "' not found.";
                throw std::runtime_error(str.str());

            }

            if (it->second.type!=type)
            {
                std::ostringstream str;
                str << "Wrong type for key '" << key << "': expected " << type << ", found " << it->second.type << ".";

                throw std::runtime_error(str.str());

            }

            if (!value.empty() && it->second.value!=value)
            {
                std::ostringstream str;
                str << "Wrong value for key '" << key << "': expected " << value << ", found " << it->second.value << ".";

                throw std::runtime_error(str.str());

            }

            return true;
        }

        IFits::Table::Keys IFits::Table::ParseBlock(const std::vector<std::string> &vec) const
        {
            std::map<std::string,Entry> rc;

            for (unsigned int i=0; i<vec.size(); i++)
            {
                const std::string key = Trim(vec[i].substr(0,8))=="HIERARCH" ? Trim(vec[i].substr(0,39)) : Trim(vec[i].substr(0,8));      
                if (vec[i].substr(8,2)!="= " && key.substr(0,8)!="HIERARCH")
                    continue;   

                char type = 0;

                std::string com;
                std::string val = Trim(vec[i].substr(10));
                
                if (key.substr(0,8)=="HIERARCH") 
                    val = Trim(vec[i].substr(40));

                if (val[0]=='\'')
                {
                    // First skip all '' in the string
                    size_t p = 1;
                    while (1)
                    {
                        const size_t pp = val.find_first_of('\'', p);
                        if (pp==std::string::npos)
                            break;

                        p = val[pp+1]=='\'' ? pp+2 : pp+1;
                    }

                    // Now find the comment
                    const size_t ppp = val.find_first_of('/', p);

                    // Set value, comment and type
                    // comments could be just spaces. take care of this.
                    if (ppp!=std::string::npos && val.size() != ppp+1)
                        com = Trim(val.substr(ppp+1));

                    val  = Trim(val.substr(1, p-2));
                    type = 'T';
                }
                else
                {
                    const size_t p = val.find_first_of('/');

                    if (val.size() != p+1)
                        com = Trim(val.substr(p+2));

                    val = Trim(val.substr(0, p));

                    if (val.empty() || val.find_first_of('T')!=std::string::npos || val.find_first_of('F')!=std::string::npos)
                        type = 'B';
                    // FIXME: actually check using a grammar or regex that it follows FITS integer format
                    else if (val.find_first_not_of("+- 0123456789") == string::npos)
                        type = 'I';
                    // FIXME: actually check using a grammar or regex that it follows FITS float format
                    else
                        type = 'F';
                }

                const Entry e = { type, val, com, vec[i] };

                rc[key] = e;
            }

            return rc;
        }

        IFits::Table::Table() : offset(0),
                               is_compressed(false),
                               bytes_per_row(0),
                               num_rows(0),
                               num_cols(0),
                               total_bytes(0),
                               datasum(0)

        {

        }

        IFits::Table::Table(const std::vector<std::string> &vec, off_t off) : offset(off),
                                                                             keys(ParseBlock(vec))
        {
            is_compressed = HasKey("ZTABLE") && Check("ZTABLE", 'B', "T");

            if (!Check("XTENSION", 'T', "BINTABLE") ||
                !Check("NAXIS",    'I', "2")        ||
                !Check("BITPIX",   'I', "8")        ||
                !Check("GCOUNT",   'I', "1")        ||
                !Check("EXTNAME",  'T')             ||
                !Check("NAXIS1",   'I')             ||
                !Check("NAXIS2",   'I')             ||
                !Check("TFIELDS",  'I'))
                return;

            if (is_compressed)
            {
                if (!Check("ZNAXIS1", 'I') ||
                    !Check("ZNAXIS2", 'I') ||
                    !Check("ZPCOUNT", 'I', "0"))
                    return;
            }
            else
            {
                if (!Check("PCOUNT", 'I', "0"))
                    return;
            }

            total_bytes   = Get<size_t>("NAXIS1")*Get<size_t>("NAXIS2");
            bytes_per_row = is_compressed ? Get<size_t>("ZNAXIS1") : Get<size_t>("NAXIS1");
            num_rows      = is_compressed ? Get<size_t>("ZNAXIS2") : Get<size_t>("NAXIS2");
            num_cols      = Get<size_t>("TFIELDS");
            datasum       = is_compressed ? Get<int64_t>("ZDATASUM", -1) : Get<int64_t>("DATASUM", -1);
//cout << "IS COMPRESSED =-========= " << is_compressed << " " << Get<size_t>("NAXIS1") << endl;
            size_t bytes = 0;

            const std::string tFormName = is_compressed ? "ZFORM" : "TFORM";
            for (long long unsigned int i=1; i<=num_cols; i++)
            {
                const std::string num(std::to_string(i));

                if (!Check("TTYPE"+num, 'T') ||
                    !Check(tFormName+num, 'T'))
                    return;

                const std::string id   = Get<std::string>("TTYPE"+num);
                const std::string fmt  = Get<std::string>(tFormName+num);
                const std::string unit = Get<std::string>("TUNIT"+num, "");
                const std::string comp = Get<std::string>("ZCTYP"+num, "");

                Compression_t compress = kCompUnknown;
                if (comp == "FACT" || comp == "CTA")
                    compress = kCompCTA;

                std::istringstream sin(fmt);
                size_t n = 0;
                sin >> n;
                if (!sin)
                    n = 1;

                char type = fmt[fmt.length()-1];

                size_t size = 0;
                switch (type)
                {
                    // We could use negative values to mark floats
                    // otheriwse we could just cast them to int64_t?
                case 'L':                  // logical
                case 'A':                  // char
                case 'B': size = 1; break; // byte
                case 'I': size = 2; break; // short
                case 'J': size = 4; break; // int
                case 'K': size = 8; break; // long long
                case 'E': size = 4; break; // float
                case 'D': size = 8; break; // double
                // case 'X': size =  n; break; // bits (n=number of bytes needed to contain all bits)
                // case 'C': size =  8; break; // complex float
                // case 'M': size = 16; break; // complex double
                // case 'P': size =  8; break; // array descriptor (32bit)
                // case 'Q': size = 16; break; // array descriptor (64bit)
                default:
                    {
                        std::ostringstream str;
                        str << "FITS format TFORM='" << fmt << "' not yet supported.";
                        throw std::runtime_error(str.str());

                    }
                }

                //check if we're reading signed/unsigned types
                double values_offset = 0;

                try {
                    values_offset = Get<double>("TZERO"+num);
                } catch (...) {}

                // used for the old, broken TZERO
                uint64_t tzero_uint = 0ull;
                try {
                    tzero_uint = Get<uint64_t>("TZERO" + num);
                } catch (...) {}

                if (values_offset == -128) {
                    if (type != 'B')
                        throw runtime_error("Unexpected type instead of bytes");
                // Value was wrong in previous versions of protozfits, we keep it 
                // so old data stays readable, at least with protozfits
                } else if (values_offset == 32768 || values_offset == 32678) {
                    if (type != 'I')
                        throw runtime_error("Unexpected type instead of Short");
                    type = 'U';
                } else if (values_offset == 2147483648) {
                    if (type != 'J')
                        throw runtime_error("Unexpected type instead of Integer");
                    type = 'V';
                // Value was wrong in previous versions of protozfits, we keep it 
                // so old data stays readable, at least with protozfits
                } else if (values_offset == 9223372036854775808ull || tzero_uint == 9223372036854775807ull) {
                    if (type != 'K')
                        throw runtime_error("Unexpected type instead of Long");
                    type = 'W';
                } else if (values_offset != 0) {
                    ostringstream str;
                    str << "ERROR: unexpected offset value: " << std::fixed << std::setprecision(30) << values_offset;
                    throw runtime_error(str.str());
                }

                const Table::Column col = { bytes, n, size, n*size, type, unit, compress};

                cols[id] = col;
                sorted_cols.push_back(col);
                bytes  += n*size;
            }

            if (bytes!=bytes_per_row)
            {
                ostringstream out;
                out << "Error: columns tell that table width is " << bytes << " bytes while header says " << bytes_per_row;
                throw std::runtime_error(out.str());
            }

            name = Get<std::string>("EXTNAME");
        }

template<>
std::string IFits::Entry::Get() const
{
    return value;
}

template<>
bool IFits::Entry::Get() const {
    if (type != 'B') {
        std::stringstream msg;
        msg << "value is not a bool, has type: '" << type << "'";
        throw wrong_type(msg.str());
    }
    return value == "T";
}

        void IFits::Table::PrintKeys(bool display_all) const
        {
            for (Keys::const_iterator it=keys.cbegin(); it!=keys.cend(); it++)
            {
                if (!display_all &&
                    (it->first.substr(0, 6)=="TTYPE" ||
                     it->first.substr(0, 6)=="TFORM" ||
                     it->first.substr(0, 6)=="TUNIT" ||
                     it->first=="TFIELDS"  ||
                     it->first=="XTENSION" ||
                     it->first=="NAXIS"    ||
                     it->first=="BITPIX"   ||
                     it->first=="PCOUNT"   ||
                     it->first=="GCOUNT")
                   )
                    continue;

                cout << std::setw(2) << it->second.type << '|' << it->first << '=' << it->second.value << '/' << it->second.comment << '|' << std::endl;
            }
        }

        void IFits::Table::PrintColumns() const
        {
            typedef std::map<std::pair<size_t, std::string>, Column> Sorted;

            Sorted sorted;

            for (Columns::const_iterator it=cols.cbegin(); it!=cols.cend(); it++)
                sorted[std::make_pair(it->second.offset, it->first)] = it->second;

            for (Sorted::const_iterator it=sorted.cbegin(); it!=sorted.cend(); it++)
            {
                cout<< std::setw(6) << it->second.offset << "| ";
                cout << it->second.num << 'x';
                switch (it->second.type)
                {
                case 'A': cout << "char(8)";    break;
                case 'L': cout << "bool(8)";    break;
                case 'B': cout << "byte(8)";    break;
                case 'I': cout << "short(16)";  break;
                case 'J': cout << "int(32)";    break;
                case 'K': cout << "int(64)";    break;
                case 'E': cout << "float(32)";  break;
                case 'D': cout << "double(64)"; break;
                }
                cout << ": " << it->first.second << " [" << it->second.unit << "]" << std::endl;
            }
        }

        IFits::Table::operator bool() const
        {
            return !name.empty();
        }

        bool IFits::Table::HasKey(const std::string &key) const
        {
            return keys.find(key)!=keys.end();
        }

        bool IFits::Table::HasColumn(const std::string& col) const
        {
            return cols.find(col)!=cols.end();
        }

        const IFits::Table::Columns& IFits::Table::GetColumns() const
        {
            return cols;
        }

        const IFits::Table::Keys& IFits::Table::GetKeys() const
        {
            return keys;
        }

        size_t IFits::Table::GetN(const std::string &key) const
        {
            const Columns::const_iterator it = cols.find(key);
            return it==cols.end() ? 0 : it->second.num;
        }



        // There may be a gap between the main table and the start of the heap:
        // this computes the offset
        streamoff IFits::Table::GetHeapShift() const
        {
            if (!HasKey("ZHEAPPTR"))
                return 0;

            const size_t shift = Get<size_t>("ZHEAPPTR");
            return shift <= total_bytes ? 0 : shift - total_bytes;
        }

        // return total number of bytes 'all inclusive'
        streamoff IFits::Table::GetTotalBytes() const
        {
            //and special data area size
            const streamoff size  = HasKey("PCOUNT") ? Get<streamoff>("PCOUNT") : 0;
            //const streamoff offset = HasKey("ZHEAPPTR") ? Get<streamoff>("ZHEAPPTR") : 0;
            //ETIENNE
            //cout << Get<streamoff>("PCOUNT") << endl;
            // Get the total size
            const streamoff total = total_bytes + size;

            // check for padding
            if (total%2880==0)
                return total;

            // padding necessary
            return total + (2880 - (total%2880));
        }




    bool IFits::ReadBlock(std::vector<std::string> &vec)
    {
        int endtag = 0;
        for (int i=0; i<36; i++)
        {
            char c[81];
            c[80] = 0;
            read(c, 80);
            if (!good())
                break;

            fChkHeader.add(c, 80);

            std::string str(c);

            if (endtag==2 || str=="END                                                                             ")
            {
                endtag = 2; // valid END tag found
                continue;
            }

            if (endtag==1 || str=="                                                                                ")
            {
                endtag = 1; // end tag not found, but expected to be there
                continue;
            }

            vec.push_back(str);
        }

        // Make sure that no empty vector is returned
        if (endtag && vec.size()%36==0)
            vec.emplace_back("END     = '' / ");

        return endtag==2;
    }

    std::string IFits::Compile(const std::string &key, int16_t i) const
    {
#if GCC_VERSION < 40603
        return i<0 ? key : key+std::to_string((long long int)(i));
#else
        return i<0 ? key : key+std::to_string(i);
#endif
    }

    void IFits::Constructor(const std::string &fname, std::string fout, const std::string& tableName, bool force, int tableNumber)
    {
        fPreviousTables.clear();
        fTableName = tableName;

        char simple[10];
        read(simple, 10);
        if (!good()) {
            throw std::runtime_error("ERROR: CANNOT READ FROM INPUT FILE " + fname + ".ABORTING");
        }
        int current_table = 0;

        if (memcmp(simple, "SIMPLE  = ", 10))
        {
            clear(rdstate()|std::ios::badbit);
            throw std::runtime_error("File is not a FITS file.");
        }

        seekg(0);
 
        while (hasNextTable()) {
            openNextTable();
            if (tableName.empty() || tableName == fTable.name) {
                break;
            }
        }

        if (!tableName.empty() && tableName != fTable.name) {
            throw runtime_error("Table "+tableName+" could not be found in input file. Aborting.");
        }

        if (fout.empty())
            return;

        if (*fout.rbegin()=='/')
        {
            const size_t p = fname.find_last_of('/');
            fout.append(fname.substr(p+1));
        }

        const streampos p = tellg();
        seekg(0);

        std::vector<char> buf(p);
        read(buf.data(), p);
    }

    vector<string> IFits::listPastTables()
    {
        return fPreviousTables;
    }

    IFits::IFits(const std::string &fname, const std::string& tableName, bool force) : IZStream(fname.c_str())
    {
        Constructor(fname, "", tableName, force);
        if ((fTable.is_compressed && !force) ||
            (fTable.name == "ZDrsCellOffsets" && !force))
        {
            throw std::runtime_error("You are trying to read a compressed fits with the base fits class. Please use factfits instead.");
            clear(rdstate()|std::ios::badbit);
        }
    }

    IFits::IFits(const std::string &fname, const std::string &fout, const std::string& tableName, bool force) : IZStream(fname.c_str())
    {
        Constructor(fname, fout, tableName, force);
        if ((fTable.is_compressed && !force) ||
            (fTable.name == "ZDrsCellOffsets" && !force))
        {
            throw std::runtime_error("You are trying to read a compressed fits with the base fits class. Please use factfits instead.");
            clear(rdstate()|std::ios::badbit);
        }
    }

    IFits::IFits() : IZStream()
    {

    }

    IFits::~IFits()
    {

    }

    void IFits::StageRow(size_t row, char* dest)
    {
        // if (row!=fRow+1) // Fast seeking is ensured by izstream
        seekg(fTable.offset+row*fTable.bytes_per_row);
        read(dest, fTable.bytes_per_row);
        //fin.clear(fin.rdstate()&~ios::eofbit);
    }

    void IFits::WriteRowToCopyFile(size_t row)
    {
        if (row==fRow+1)
        {
            fChkData.add(fBufferRow);
        }
    }

    void IFits::ZeroBufferForChecksum(std::vector<char>& vec, const uint64_t extraZeros)
    {
        auto ib = vec.begin();
        auto ie = vec.end();

        *ib++ = 0;
        *ib++ = 0;
        *ib++ = 0;
        *ib   = 0;

        for (uint64_t i=0;i<extraZeros+8;i++)
            *--ie = 0;
    }

    uint8_t IFits::ReadRow(size_t row) {
        // For the checksum we need everything to be correctly aligned
        const uint8_t offset = (row*fTable.bytes_per_row)%4;

        ZeroBufferForChecksum(fBufferRow);

        StageRow(row, fBufferRow.data()+offset);

        WriteRowToCopyFile(row);

        fRow = row;

        return offset;
    }

    void IFits::MoveColumnDataToUserSpace(char *dest, const char *src, const Table::Column& c)
    {
        // Let the compiler do some optimization by
        // knowing that we only have 1, 2, 4 and 8
        switch (c.size)
        {
        case 1: memcpy   (dest, src, c.bytes); break;
        case 2: revcpy<2>(dest, src, c.num);   break;
        case 4: revcpy<4>(dest, src, c.num);   break;
        case 8: revcpy<8>(dest, src, c.num);   break;
        }
    }

    bool IFits::GetRow(size_t row, bool check)
    {
        if (check && row>=fTable.num_rows)
            return false;

        const uint8_t offset = ReadRow(row);
        if (!good())
            return good();

        const char *ptr = fBufferRow.data() + offset;

        for (Addresses::const_iterator it=fAddresses.cbegin(); it!=fAddresses.cend(); it++)
        {
            const Table::Column &c = it->second;

            const char *src = ptr + c.offset;
            char *dest = reinterpret_cast<char*>(it->first);

            MoveColumnDataToUserSpace(dest, src, c);
        }

        return good();
    }

    bool IFits::GetNextRow(bool check)
    {
        return GetRow(fRow+1, check);
    }

    bool IFits::SkipNextRow()
    {
        seekg(fTable.offset+(++fRow)*fTable.bytes_per_row);
        return good();
    }

     bool IFits::Compare(const Address &p1, const Address &p2)
    {
        return p1.first>p2.first;
    }


    void* IFits::SetPtrAddress(const std::string &name)
    {
        if (fTable.cols.count(name)==0)
        {
            std::ostringstream str;
            str << "SetPtrAddress('" << name << "') - Column not found.";
            throw std::runtime_error(str.str());
        }

        Pointers::const_iterator it = fPointers.find(name);
        if (it!=fPointers.end())
            return it->second;

        fGarbage.emplace_back(fTable.cols[name].bytes);

        void *ptr = fGarbage.back().data();

        fPointers[name] = ptr;
        fAddresses.emplace_back(ptr, fTable.cols[name]);
        sort(fAddresses.begin(), fAddresses.end(), Compare);
        return ptr;
    }


    bool IFits::SetPtrAddress(const std::string &name, void *ptr, size_t cnt)
    {
        if (fTable.cols.count(name)==0)
        {
            std::ostringstream str;
            str <<"SetPtrAddress('" << name << "') - Column not found.";
            throw std::runtime_error(str.str());

        }

        if (cnt && cnt!=fTable.cols[name].num)
        {
            std::ostringstream str;
            str << "SetPtrAddress('" << name << "') - Element count mismatch: expected "
                << fTable.cols[name].num << " from header, got " << cnt;
            throw std::runtime_error(str.str());

        }

        //fAddresses[ptr] = fTable.cols[name];
        fPointers[name] = ptr;
        fAddresses.emplace_back(ptr, fTable.cols[name]);
        sort(fAddresses.begin(), fAddresses.end(), Compare);
        return true;
    }

    bool     IFits::HasKey(const std::string &key) const { return fTable.HasKey(key); }
    bool     IFits::HasColumn(const std::string& col) const { return fTable.HasColumn(col);}
    const IFits::Table::Columns& IFits::GetColumns() const { return fTable.GetColumns();}
    const IFits::Table::SortedColumns& IFits::GetSortedColumns() const { return fTable.sorted_cols;}
    const IFits::Table::Keys& IFits::GetKeys() const { return fTable.GetKeys();}

    int64_t     IFits::GetInt(const std::string &key) const { return fTable.Get<int64_t>(key); }
    uint64_t    IFits::GetUInt(const std::string &key) const { return fTable.Get<uint64_t>(key); }
    double      IFits::GetFloat(const std::string &key) const { return fTable.Get<double>(key); }
    std::string IFits::GetStr(const std::string &key) const { return fTable.Get<std::string>(key); }

    size_t IFits::GetN(const std::string &key) const
    {
        return fTable.GetN(key);
    }

//    size_t GetNumRows() const { return fTable.num_rows; }
    size_t IFits::GetRow() const { return fRow==(size_t)-1 ? 0 : fRow; }

    IFits::operator bool() const { return fTable && fTable.offset!=0; }

    void IFits::PrintKeys() const { fTable.PrintKeys(); }
    void IFits::PrintColumns() const { fTable.PrintColumns(); }

    bool IFits::IsHeaderOk() const { return fTable.datasum<0?false:(fChkHeader+Checksum(fTable.datasum)).valid(); }
     bool IFits::IsFileOk() const { return (fChkHeader+fChkData).valid(); }

    bool IFits::IsCompressedFITS() const { return fTable.is_compressed;}

    size_t IFits::GetNumRows() const
    {
        return fTable.Get<size_t>("NAXIS2");
    }

    size_t IFits::GetBytesPerRow() const
    {
        return fTable.Get<size_t>("NAXIS1");
    }

bool IFits::hasNextTable() {
    // fTable.offset is zero initialized, so this also works
    // if no table has yet been read
    seekg(fTable.offset + fTable.GetTotalBytes());
    peek();
    return good();
}

void IFits::openNextTable(bool force) {
    seekg(fTable.offset + fTable.GetTotalBytes());

    while (good())
    {
        std::vector<std::string> block;
        while(true) {
            peek();

            if (eof() || bad()) {
                throw runtime_error("No table left in file");
            }

            // FIXME: Set limit on memory consumption
            const bool end_found = ReadBlock(block);
            if (end_found) {
                break;
            }

            if (!good()) {
                clear(rdstate()|std::ios::badbit);
                throw std::runtime_error("FITS file corrupted: reached end-of-file before end of header");
            }

            if (block.size() % 36) {
                if (!end_found && !force) {
                    clear(rdstate()|std::ios::badbit);
                    throw std::runtime_error("END keyword missing in FITS header.");
                }
                break;
            }
        }

        if (block.empty())
            break;

        if (block[0].substr(0, 9)=="SIMPLE  =")
        {
            fChkHeader.reset();
            continue;
        }

        if (block[0].substr(0, 9)=="XTENSION=")
        {
            fTable = Table(block, tellg());
            fRow   = (size_t)-1;

            if (!fTable)
            {
                clear(rdstate()|std::ios::badbit);
                throw std::runtime_error("Could not read table");
            }

            fPreviousTables.push_back(fTable.name);

            fBufferRow.resize(fTable.bytes_per_row + 8-fTable.bytes_per_row%4);
            fBufferDat.resize(fTable.bytes_per_row);

            break;
        }
    }
}
