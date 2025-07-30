/**
 *  @file OFits.cpp
 *
 *  @brief Plain FITS binary tables writer
 *
 */
#include "OFits.h"
#include "CMakeDefs.h"
#include "BasicDefs.h"

#include <typeinfo>

// For ceil()
#include <cmath>

        OFits::Key::Key(const std::string &k) : key(k),
                                                delim(false),
                                                fitsString(""),
                                                offset(0),
                                                changed(true)
        {

        }


        std::string OFits::Key::Trim(const std::string &str)
        {
            // Trim Both leading and trailing spaces
            const size_t first = str.find_first_not_of(' '); // Find the first character position after excluding leading blank spaces
            const size_t last  = str.find_last_not_of(' ');  // Find the first character position from reverse af

            // if all spaces or empty return an empty string
            if (std::string::npos==first || std::string::npos==last)
                return std::string();

            return str.substr(first, last-first+1);
        }

        bool OFits::Key::FormatKey()
        {
            key = Trim(key);
            if (key.empty())
            {
                throw std::runtime_error("Key name empty.");
            }
            if (key.size()>8)
            {
                std::ostringstream sout;
                sout << "Key '" << key << "' exceeds 8 bytes.";
                throw std::runtime_error(sout.str());
            }

            //transform(key.begin(), key.end(), key.begin(), toupper);
#if GCC_VERSION < 40603
            for (std::string::const_iterator c=key.begin(); c<key.end(); c++)
#else
            for (std::string::const_iterator c=key.cbegin(); c<key.cend(); c++)
#endif
                if ((*c<'A' || *c>'Z') && (*c<'0' || *c>'9') && *c!='-' && *c!='_')
                {
                    std::ostringstream sout;
                    sout << "Invalid character '" << *c << "' found in key '" << key << "'";
                    throw std::runtime_error(sout.str());
                }

            return true;
        }


        bool OFits::Key::FormatComment()
        {
            comment = Trim(comment);

#if GCC_VERSION < 40603
            for (std::string::const_iterator c=key.begin(); c<key.end(); c++)
#else
            for (std::string::const_iterator c=key.cbegin(); c<key.cend(); c++)
#endif
                if (*c<32 || *c>126)
                {
                    std::ostringstream sout;
                    sout << "Invalid character '" << *c << "' [" << int(*c) << "] found in comment '" << comment << "'";
                    throw std::runtime_error(sout.str());
                }

            return true;
        }


        bool OFits::Key::check(bool trim)
        {
            if (!FormatKey())
                return false;

            if (!FormatComment())
                return false;

            size_t sz = CalcSize();
            if (sz<=80)
                return true;

            if (!trim)
            {
                std::ostringstream sout;
                sout << "Size " << sz << " of entry for key '" << key << "' exceeds 80 characters.";
                throw std::runtime_error(sout.str());
                return false;
            }

            //looks like something went wrong. Maybe entry is too long ?
            //try to remove the comment
            comment = "";

            sz = CalcSize();
            if (sz<=80)
            {
                return true;
            }

            std::ostringstream sout;
            sout << "Size " << sz << " of entry for key '" << key << "' exceeds 80 characters even without comment.";
            throw std::runtime_error(sout.str());
        }

        size_t OFits::Key::CalcSize() const
        {
            if (!delim)
                return 10+comment.size();

            return 10 + (value.size()<20?20:value.size()) + 3 + comment.size();
        }


        std::string OFits::Key::Compile()
        {

            if (fitsString != "")
                return fitsString;

            std::ostringstream sout;
            sout << std::left << std::setw(8) << key;

            if (!delim)
            {
                sout << "  " << comment;
                return sout.str();
            }

            sout << "= ";
            sout << (!value.empty() && value[0]=='\''?std::left:std::right);
            sout << std::setw(20) << value << std::left;

            if (!comment.empty())
                sout << " / " << comment;

            return sout.str();
        }


        void OFits::Key::Out(std::ofstream &fout)
        {
            if (!changed)
                return;

            std::string str = Compile();
            str.insert(str.end(), 80-str.size(), ' ');

            if (offset==0)
                offset = fout.tellp();

            //cout << "Write[" << offset << "]: " << key << "/" << value << endl;

            fout.seekp(offset);
            fout << str;

            checksum.reset();
            checksum.add(str.c_str(), 80);

            changed = false;
        }



        std::vector<OFits::Key>::iterator OFits::findkey(const std::string &key)
        {
            for (auto it=fKeys.begin(); it!=fKeys.end(); it++)
                if (key==it->key)
                    return it;

            return fKeys.end();
        }


        bool OFits::Set(const std::string &key, bool delim, const std::string &value, const std::string &comment)
        {
            // If no delimit add the row no matter if it alread exists
            if (delim)
            {
                // if the row already exists: update it
                auto it = findkey(key);
                if (it!=fKeys.end())
                {
                    it->value   = value;
                    it->changed = true;
                    return true;
                }
            }

            if (fTable.num_rows>0)
            {
                std::ostringstream sout;
                sout << "No new header key can be defined, rows were already written to the file... ignoring new key '" << key << "'";
                for (auto it=fKeys.begin(); it!=fKeys.end(); it++)
                    std::cout << it->key << " " << it->value << std::endl;
                throw std::runtime_error(sout.str());
            }

            Key entry;

            entry.key     = key;
            entry.delim   = delim;
            entry.value   = value;
            entry.comment = comment;
            entry.offset  = 0;
            entry.changed = true;

            if (!entry.check(fCommentTrimming))
                return false;

            fKeys.push_back(entry);
            return true;
        }


        std::vector<OFits::Table::Column>::const_iterator OFits::findcol(const std::string &name)
        {
            for (auto it=fTable.cols.cbegin(); it!=fTable.cols.cend(); it++)
                if (name==it->name)
                    return it;

            return fTable.cols.cend();
        }


        OFits::OFits() : fCommentTrimming(true),
                         fManualExtName(false)
        {
        }
        OFits::OFits(const char *fname) : std::ofstream(),
                                   fCommentTrimming(true),
                                   fManualExtName(false),
                                   fCurrentFileDescriptor(NULL)
        {
            this->open(fname);
        }
        OFits::~OFits()
        {
            if (is_open())
                close();
        }

        void OFits::open(const char * filename, bool addEXTNAMEKey)
        {
            fDataSum    = 0;
            fHeaderSum  = 0;
            fTableStart = 0;

            fTable = Table();
            fKeys.clear();

            SetStr("XTENSION", "BINTABLE", "binary table extension");
            SetInt("BITPIX",                     8, "8-bit bytes");
            SetInt("NAXIS",                      2, "2-dimensional binary table");
            SetInt("NAXIS1",                     0, "width of table in bytes");
            SetInt("NAXIS2",                     0, "number of rows in table");
            SetInt("PCOUNT",                     0, "size of special data area");
            SetInt("GCOUNT",                     1, "one data group (required keyword)");
            SetInt("TFIELDS",                    0, "number of fields in each row");
            if (addEXTNAMEKey)
                SetStr("EXTNAME", "", "name of extension table");
            else
                fManualExtName = true;
            SetStr("CHECKSUM", "0000000000000000", "Checksum for the whole HDU");
            SetStr("DATASUM",  "         0", "Checksum for the data block");

#ifndef __clang__
            //open file the posix way so that we can take a lock on it
            fCurrentFileDescriptor = fopen(filename, "w");

            //lock file
            if (fCurrentFileDescriptor != NULL && strcmp(filename, "/dev/null"))
            if (flock(fileno(fCurrentFileDescriptor), LOCK_EX | LOCK_NB))
            {
                std::cout << "Filename : " << filename << std::endl;
                throw std::runtime_error("Could not lock file. At all.");
            }
#endif
            std::ofstream::open(filename);

            if (!good())
            {
                std::ostringstream str;
                str << "Could not open file " << filename;
                throw std::runtime_error(str.str());
            }
        }

        void OFits::AllowCommentsTrimming(bool allow)
        {
            fCommentTrimming = allow;
        }
        //Etienne: required to enable 1 to 1 reconstruction of files
        bool OFits::SetKeyComment(const std::string& key, const std::string& comment)
        {
            auto it = findkey(key);
            if (it==fKeys.end())
                return false;
            it->comment = comment;
            it->changed = true;
            return true;
        }
        bool OFits::SetKeyFromFitsString(const std::string& fitsString)
        {
            if (fTable.num_rows>0)
            {
                std::ostringstream sout;
                sout << "No new header key can be defined, rows were already written to the file... ignoring new key '" << fitsString << "'";
                throw std::runtime_error(sout.str());
            }

            //extract keyword
            std::string keyword = "";
            for (int i=0;i<8;i++)
            {
                if (fitsString[i] == ' ')
                    break;
                keyword += fitsString[i];
            }

            bool found = false;
            auto entry = fKeys.begin();
            for (;entry!=fKeys.end(); entry++)
            {
                if (entry->key == keyword)
                {
                    found = true;
                    break;
                }
            }

            if (!found)
            {
                Key entry;
                entry.key = keyword;
                entry.fitsString = fitsString;
                entry.changed = true;
                fKeys.push_back(entry);
            }
            else
            {
                entry->fitsString =fitsString;
                entry->changed = true;
            }
            return true;
        }
        bool OFits::SetRaw(const std::string &key, const std::string &val, const std::string &comment)
        {
            return Set(key, true, val, comment);
        }

        bool OFits::SetBool(const std::string &key, bool b, const std::string &comment)
        {
            return Set(key, true, b?"T":"F", comment);
        }

        bool OFits::AddEmpty(const std::string &key, const std::string &comment)
        {
            return Set(key, true, "", comment);
        }

        bool OFits::SetStr(const std::string &key, std::string s, const std::string &comment)
        {
            for (uint i=0; i<s.length(); i++)
                if (s[i]=='\'')
                    s.insert(i++, "\'");

            return Set(key, true, "'"+s+"'", comment);
        }

        bool OFits::SetInt(const std::string &key, int64_t i, const std::string &comment)
        {
            std::ostringstream sout;
            sout << i;

            return Set(key, true, sout.str(), comment);
        }

        bool OFits::SetUInt(const std::string &key, uint64_t i, const std::string &comment)
        {
            std::ostringstream sout;
            sout << i;

            return Set(key, true, sout.str(), comment);
        }

        bool OFits::SetFloat(const std::string &key, double f, int p, const std::string &comment)
        {
            std::ostringstream sout;

            if (p<0)
                sout << std::setprecision(-p) << fixed;
            if (p>0)
                sout << std::setprecision(p);
            if (p==0 && ceil(f) != f)
                sout << std::setprecision(f>1e-100 && f<1e100 ? 15 : 14);
            else
                sout << std::setprecision(20); //Max num digits of long unsigned

            sout << f;

            std::string str = sout.str();

            replace(str.begin(), str.end(), 'e', 'E');

            if (str.find_first_of('E')==std::string::npos && str.find_first_of('.')==std::string::npos)
                str += ".";

            return Set(key, true, str, comment);
        }

        bool OFits::SetFloat(const std::string &key, double f, const std::string &comment)
        {
            return SetFloat(key, f, 0, comment);
        }

        bool OFits::SetHex(const std::string &key, uint64_t i, const std::string &comment)
        {
            std::ostringstream sout;
            sout << std::hex << "0x" << i;
            return SetStr(key, sout.str(), comment);
        }

        bool OFits::AddComment(const std::string &comment)
        {
            return Set("COMMENT", false, "", comment);
        }

        bool OFits::AddHistory(const std::string &comment)
        {
            return Set("HISTORY", false, "", comment);
        }

        void OFits::End()
        {
            Set("END");
            while (fKeys.size()%36!=0)
                fKeys.emplace_back();
        }

        std::string OFits::CommentFromType(char type)
        {
            std::string comment;

            switch (type)
            {
            case 'L': comment = "[1-byte BOOL]";  break;
            case 'A': comment = "[1-byte CHAR]";  break;
            case 'B': comment = "[1-byte BOOL]";  break;
            case 'I': comment = "[2-byte INT]";   break;
            case 'J': comment = "[4-byte INT]";   break;
            case 'K': comment = "[8-byte INT]";   break;
            case 'E': comment = "[4-byte FLOAT]"; break;
            case 'D': comment = "[8-byte FLOAT]"; break;
            case 'Q': comment = "[var. Length]"; break;
            case 'S': comment = "[1-byte UCHAR]"; break;
            case 'U': comment = "[2-bytes UINT]"; break;
            case 'V': comment = "[4-bytes UINT]"; break;
            case 'W': comment = "[8-bytes UINT]"; break;
            }

            return comment;
        }

        uint32_t OFits::SizeFromType(char type)
        {
            size_t size = 0;

            switch (type)
            {
            case 'L': size = 1; break;
            case 'A': size = 1; break;
            case 'B': size = 1; break;
            case 'I': size = 2; break;
            case 'J': size = 4; break;
            case 'K': size = 8; break;
            case 'E': size = 4; break;
            case 'D': size = 8; break;
            case 'Q': size = 16; break;
            //new, unsigned columns
            case 'S': size = 1; break;
            case 'U': size = 2; break;
            case 'V': size = 4; break;
            case 'W': size = 8; break;
            }

            return size;
        }
        //to be able to restore the file 1 to 1, I must restore the header keys myself
        bool OFits::AddColumn(uint32_t cnt, char typechar, const std::string &name, const std::string &unit, const std::string &comment, bool addHeaderKeys)
        {
            if (tellp()<0)
            {
                std::ostringstream sout;
                sout << "File not open... ignoring column '" << name << "'";
                throw std::runtime_error(sout.str());
            }

            if ((size_t)(tellp())>fTableStart)
            {
                std::cout << "Table start: " << fTableStart << " current location: " << tellp() << std::endl;
                std::ostringstream sout;
                sout << "Header already written, no new column can be defined... ignoring column '" << name << "'";
                throw std::runtime_error(sout.str());
            }

            if (findcol(name)!=fTable.cols.cend())
            {
                std::ostringstream sout;
                sout << "A column with the name '" << name << "' already exists.";
                throw std::runtime_error(sout.str());
            }

            typechar = toupper(typechar);

            switch (typechar)
            {
                case 'S':
                    SetFloat("TZERO"+std::to_string((long long int)(fTable.num_cols+1)), -128, "Offset for signed chars");
                    typechar = 'B';
                break;

                case 'U':
                    SetFloat("TZERO"+std::to_string((long long int)(fTable.num_cols+1)), 32768, "Offset for uint16");
                    typechar = 'I';
                    break;
                case 'V':
                    SetFloat("TZERO"+std::to_string((long long int)(fTable.num_cols+1)), 2147483648, "Offset for uint32");
                    typechar = 'J';
                break;
                case 'W':
//                    SetInt("TZERO"+std::to_string(fTable.num_cols+1), WRONG nUMBER, "Offset for uint64");
                    typechar = 'K';
                break;
                default:
                    ;
            }

            static const std::string allow("LABIJKEDQ");
    #if GCC_VERSION < 40603
            if (std::find(allow.begin(), allow.end(), typechar)==allow.end())
    #else
            if (std::find(allow.cbegin(), allow.cend(), typechar)==allow.end())
    #endif
            {
                std::ostringstream sout;
                sout << "Column type '" << typechar << "' not supported.";
                throw std::runtime_error(sout.str());
            }


            std::ostringstream type;
            type << cnt;
            if (typechar=='Q')
                type << "QB";
            else
                type << typechar;

            fTable.num_cols++;

            if (fTable.num_cols >= 1000) //we've exceeded the number of allowed columns
            {
                std::ostringstream str;
                str << "Error, you've just created more than 1000 columns, while the FITS standard limits this to 999. Current columns are:\n";
                for (auto it=fTable.cols.begin(); it!= fTable.cols.end(); it++)
                    str << it->name << "\n";

                throw std::runtime_error(str.str());
            }

            if (addHeaderKeys)
            {
    #if GCC_VERSION < 40603
                const std::string nc = std::to_string((long long int)(fTable.num_cols));
    #else
                const std::string nc = std::to_string(fTable.num_cols);
    #endif
                SetStr("TFORM"+nc, type.str(), "format of "+name+" "+CommentFromType(typechar));
                SetStr("TTYPE"+nc, name, comment);
                if (!unit.empty())
                    SetStr("TUNIT"+nc, unit, "unit of "+name);
            }
            size_t size = SizeFromType(typechar);

            Table::Column col;

            col.name   = name;
            col.type   = typechar;
            col.num    = cnt;
            col.size   = size;
            col.offset = fTable.bytes_per_row;

            fTable.cols.push_back(col);

            fTable.bytes_per_row += size*cnt;

            // Align to four bytes
            fOutputBuffer.resize(fTable.bytes_per_row + 4-fTable.bytes_per_row%4);

            return true;
        }


        Checksum OFits::WriteHeader(std::ofstream &fout)
        {
            Checksum sum;
            for (auto it=fKeys.begin(); it!=fKeys.end(); it++)
            {
                it->Out(fout);
                sum += it->checksum;
            }
            fout.flush();

            return sum;
        }

        Checksum OFits::WriteHeader()
        {
            return WriteHeader(*this);
        }

        void OFits::FlushHeader()
        {
            const off_t pos = tellp();
            WriteHeader();
            seekp(pos);
        }

        Checksum OFits::WriteFitsHeader()
        {
            OFits h;

            h.SetBool("SIMPLE", true, "file does conform to FITS standard");
            h.SetInt ("BITPIX",    8, "number of bits per data pixel");
            h.SetInt ("NAXIS",     0, "number of data axes");
            h.SetBool("EXTEND", true, "FITS dataset may contain extensions");
            h.SetStr ("CHECKSUM","0000000000000000", "Checksum for the whole HDU");
            h.SetStr ("DATASUM", "         0", "Checksum for the data block");
            h.AddComment("FITS (Flexible Image Transport System) format is defined in 'Astronomy");
            h.AddComment("and Astrophysics', volume 376, page 359; bibcode: 2001A&A...376..359H");
            h.End();

            const Checksum sum = h.WriteHeader(*this);

            h.SetStr("CHECKSUM", sum.str());

            const size_t offset = tellp();
            h.WriteHeader(*this);
            seekp(offset);

            return sum;
        }

        bool OFits::WriteDrsOffsetsTable ()
        {
            return true;
        }

        bool OFits::WriteCatalog()
        {
            return true;
        }

        bool OFits::WriteTableHeader(const char *name)
        {
            if ((size_t)(tellp())>fTableStart)
            {
                throw std::runtime_error("Table not empty anymore.");
            }

            //write basic fits header only in the case of a new file
            if (fTableStart == 0)
                fHeaderSum = WriteFitsHeader();

            WriteDrsOffsetsTable();

            if (!fManualExtName)
                SetStr("EXTNAME", name);

            SetInt("NAXIS1",  fTable.bytes_per_row);
            SetInt("TFIELDS", fTable.cols.size());

            End();

            WriteHeader();

            WriteCatalog();

            return good();
        }

        uint32_t OFits::GetBytesPerRow() const
        {
            return fTable.bytes_per_row;
        }

        bool OFits::WriteRow(const void *ptr, size_t cnt, bool byte_swap)
        {
            // FIXME: Make sure that header was already written
            //        or write header now!
            if (cnt!=fTable.bytes_per_row)
            {
                std::ostringstream sout;
                sout << "WriteRow - Size " << cnt << " does not match expected size " << fTable.bytes_per_row;
                throw std::runtime_error(sout.str());
            }

            // For the checksum we need everything to be correctly aligned
            const uint8_t offset = fTable.offset%4;

            char *buffer = fOutputBuffer.data() + offset;

            auto ib = fOutputBuffer.begin();
            auto ie = fOutputBuffer.rbegin();
            *ib++ = 0;
            *ib++ = 0;
            *ib++ = 0;
            *ib   = 0;

            *ie++ = 0;
            *ie++ = 0;
            *ie++ = 0;
            *ie   = 0;

            if (!byte_swap)
                memcpy(buffer, ptr, cnt);
            else
            {
                for (auto it=fTable.cols.cbegin(); it!=fTable.cols.cend(); it++)
                {
                    const char *src  = reinterpret_cast<const char*>(ptr) + it->offset;
                    char       *dest = buffer + it->offset;

                    // Let the compiler do some optimization by
                    // knowing the we only have 1, 2, 4 and 8
                    switch (it->size)
                    {
                    case 1: memcpy   (dest, src, it->num*it->size); break;
                    case 2: revcpy<2>(dest, src, it->num);          break;
                    case 4: revcpy<4>(dest, src, it->num);          break;
                    case 8: revcpy<8>(dest, src, it->num);          break;
                    }
                }
            }

            write(buffer, cnt);
            fDataSum.add(fOutputBuffer);

            fTable.num_rows++;
            fTable.offset += cnt;
            return good();
        }

        // Flushes the number of rows to the header on disk
        void OFits::FlushNumRows()
        {
            SetInt("NAXIS2", fTable.num_rows);
            FlushHeader();
        }

        size_t OFits::GetNumRows() const
        {
            return fTable.num_rows;
        }

        void OFits::AlignTo2880Bytes()
        {
            if (tellp()%(80*36)>0)
            {
                std::vector<char> filler(80*36-tellp()%(80*36));
                write(filler.data(), filler.size());
            }
        }

        Checksum OFits::UpdateHeaderChecksum()
        {
            std::ostringstream dataSumStr;
            dataSumStr << fDataSum.val();
            SetStr("DATASUM", dataSumStr.str());

            const Checksum sum = WriteHeader();

            //sum += headersum;

            SetStr("CHECKSUM", (sum+fDataSum).str());

            return WriteHeader();
        }

        bool OFits::close()
        {
            if (tellp()<0)
                return false;

            AlignTo2880Bytes();

            // We don't have to jump back to the end of the file
            SetInt("NAXIS2",  fTable.num_rows);

            const Checksum chk = UpdateHeaderChecksum();

            std::ofstream::close();
#ifndef __clang__
            if (fCurrentFileDescriptor != NULL)
            {
                flock(fileno(fCurrentFileDescriptor), LOCK_UN);
                fclose(fCurrentFileDescriptor);
            }

            fCurrentFileDescriptor = NULL;
#endif
            if ((chk+fDataSum).valid())
                return true;

            std::ostringstream sout;
            sout << "Checksum (" << std::hex << chk.val() << ") invalid.";
            throw std::runtime_error(sout.str());
        }

        std::pair<std::string, int> OFits::GetChecksumData()
        {
            std::string datasum;
            std::string checksum;
            //cannot directly use the Get methods, because they are only in fits.h
            for (std::vector<Key>::const_iterator it=fKeys.cbegin(); it!= fKeys.cend(); it++)
            {
                if (it->key == "CHECKSUM") checksum = it->value;
                if (it->key == "DATASUM") datasum = it->value;
            }
            if (checksum[0] == '\'')
                checksum = checksum.substr(1,checksum.size()-2);
            if (datasum[0] == '\'')
                datasum = datasum.substr(1, datasum.size()-2);
            return std::make_pair(checksum, atoi(datasum.c_str()));
        }

        void OFits::SetDefaultKeys()
        {
            SetStr("CREATOR", typeid(*this).name(), "Class that wrote this file");
            SetStr("COMPILED", ADH::Core::getIsoBuildTimestamp(), "Compile time");
            SetStr("ORIGIN", "CTA", "Institution that wrote the file");
            SetStr("WORKPKG", "ADH", "Workpackage that wrote the file");
            SetStr("TIMESYS", "UTC", "Time system");
            SetStr("ADHREV", GIT_REV_ADH, "ADH GIT hash");
            SetStr("APISREV", GIT_REV_ADH_APIS, "ADH-APIS GIT hash");
            SetInt("MAJORV", ADH_VERSION_MAJOR, "Major ADH release");
            SetInt("MINORV", ADH_VERSION_MINOR, "Minor ADH release");


            const time_t t0 = time(NULL);
            const struct tm *tmp1 = gmtime(&t0);

            std::string str(19, '\0');
            if (tmp1 && strftime(const_cast<char*>(str.data()), 20, "%Y-%m-%dT%H:%M:%S", tmp1))
                SetStr("DATE", str, "File creation date");

            SetStr("DATEEND", "", "File closing date");
        }
