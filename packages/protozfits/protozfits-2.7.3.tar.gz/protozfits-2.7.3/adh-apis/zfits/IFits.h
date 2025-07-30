/**
 *
 * @file IFits.h
 *
 * @brief Reads plain fits, possibly gzipped (i.e .fits or .fits.gz)
 *
 *  Created on: Nov 5, 2013
 *      Author: lyard-bretz
 *
 */

#ifndef _FITS_H_
#define _FITS_H_

#include <stdint.h>

#include <map>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <stdexcept>

#define GCC_VERSION (__GNUC__ * 10000  + __GNUC_MINOR__ * 100  + __GNUC_PATCHLEVEL__)

#include <unordered_map>

#include <vector>
#include <iomanip>
#include <ios>
#include <iostream>


#include "IZStream.h"
#include "Checksum.h"



class IFits : public IZStream
{
    public:
        //I know I know, you're going to yiell that this does not belong here.
        //It will belong in the global scope eventually, and it makes the coding of zfits much simpler this way.
        enum Compression_t
        {
            kCompUnknown,
            kCompCTA
        };

        /**
         * Exception raised when asking to get a the value of Entry as wrong type
         */
        class wrong_type : public std::runtime_error {
            using std::runtime_error::runtime_error;
        };

        struct Entry
        {
            char        type;
            std::string value;
            std::string comment;
            std::string fitsString;

            template<typename T>
                T Get() const
            {
                T t;

                std::istringstream str(value);
                str >> t;

                return t;
            }

        };

        struct Table
        {
            off_t offset;

            bool is_compressed;

            std::string name;
            size_t bytes_per_row;
            size_t num_rows;
            size_t num_cols;
            size_t total_bytes; // NAXIS1*NAXIS2

            struct Column
            {
                size_t offset;
                size_t num;
                size_t size;
                size_t bytes;  // num*size
                char   type;
                std::string unit;
                Compression_t comp;
            };

            typedef std::map<std::string, Entry>  Keys;
            typedef std::map<std::string, Column> Columns;
            typedef std::vector<Column> SortedColumns;

            Columns cols;
            SortedColumns sorted_cols;
            Keys    keys;

            int64_t datasum;

            std::string Trim(const std::string &str, char c=' ') const;

            bool Check(const std::string &key, char type, const std::string &value="") const;

            Keys ParseBlock(const std::vector<std::string> &vec) const;

            Table();
            Table(const std::vector<std::string> &vec, off_t off);


            void PrintKeys(bool display_all=false) const;

            void PrintColumns() const;

            operator bool() const;

            bool HasKey(const std::string &key) const;

            bool HasColumn(const std::string& col) const;

            const Columns &GetColumns() const;

            const Keys &GetKeys() const;

            // Values of keys are always signed
            template<typename T>
            T Get(const std::string &key) const
            {
                const std::map<std::string,Entry>::const_iterator it = keys.find(key);
                if (it==keys.end())
                {
                    std::ostringstream str;
                    str << "Key '" << key << "' not found.";
                    throw std::runtime_error(str.str());
                }
                return it->second.Get<T>();
            }

            // Values of keys are always signed
            template<typename T>
                T Get(const std::string &key, const T &deflt) const
            {
                const std::map<std::string,Entry>::const_iterator it = keys.find(key);
                return it==keys.end() ? deflt :it->second.Get<T>();
            }

            size_t GetN(const std::string &key) const;



            // There may be a gap between the main table and the start of the heap:
            // this computes the offset
            std::streamoff GetHeapShift() const;

            // return total number of bytes 'all inclusive'
            std::streamoff GetTotalBytes() const;
        };

        std::vector<std::string> listPastTables();

    protected:
        Table fTable;
        std::string fTableName;

        std::vector<std::string> fPreviousTables; // tables that were read already

        typedef std::pair<void*, Table::Column> Address;
        typedef std::vector<Address> Addresses;
        //map<void*, Table::Column> fAddresses;
        Addresses fAddresses;

        typedef std::unordered_map<std::string, void*> Pointers;
        Pointers fPointers;

        std::vector<std::vector<char>> fGarbage;

        std::vector<char> fBufferRow;
        std::vector<char> fBufferDat;

        size_t fRow;

        Checksum fChkHeader;
        Checksum fChkData;

        bool ReadBlock(std::vector<std::string> &vec);

        std::string Compile(const std::string &key, int16_t i=-1) const;

        void Constructor(const std::string &fname, std::string fout, const std::string& tableName, bool force, int tableNumber=-1);

    public:
        IFits(const std::string &fname, const std::string& tableName="", bool force=false);

        IFits(const std::string &fname, const std::string &fout, const std::string& tableName, bool force=false);

        IFits();

        virtual ~IFits();

        virtual void StageRow(size_t row, char* dest);

        virtual void WriteRowToCopyFile(size_t row);

        void ZeroBufferForChecksum(std::vector<char>& vec, const uint64_t extraZeros=0);

        uint8_t ReadRow(size_t row);

        template<size_t N>
            void revcpy(char *dest, const char *src, const int &num)
        {
            const char *pend = src + num*N;
            for (const char *ptr = src; ptr<pend; ptr+=N, dest+=N)
                std::reverse_copy(ptr, ptr+N, dest);
        }

        virtual void MoveColumnDataToUserSpace(char *dest, const char *src, const Table::Column& c);

        virtual bool GetRow(size_t row, bool check=true);

            const Table& GetTable() const {return fTable; };

        bool GetNextRow(bool check=true);

        virtual bool SkipNextRow();

        static bool Compare(const Address &p1, const Address &p2);

        template<class T, class S>
        const T &GetAs(const std::string &name)
        {
            return *reinterpret_cast<S*>(fPointers[name]);
        }

        void *SetPtrAddress(const std::string &name);

        template<typename T>
        bool SetPtrAddress(const std::string &name, T *ptr, size_t cnt)
        {
            if (fTable.cols.count(name)==0)
            {
                std::ostringstream str;
                str << "SetPtrAddress('" << name << "') - Column not found.";

                throw std::runtime_error(str.str());
            }

            if (sizeof(T)!=fTable.cols[name].size)
            {
                std::ostringstream str;
                str << "SetPtrAddress('" << name << "') - Element size mismatch: expected "
                    << fTable.cols[name].size << " from header, got " << sizeof(T);
                throw std::runtime_error(str.str());

            }

            if (cnt!=fTable.cols[name].num)
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

        template<class T>
        bool SetRefAddress(const std::string &name, T &ptr)
        {
            return SetPtrAddress(name, &ptr, sizeof(ptr)/sizeof(T));
        }

        template<typename T>
        bool SetVecAddress(const std::string &name, std::vector<T> &vec)
        {
            return SetPtrAddress(name, vec.data(), vec.size());
        }

        template<typename T>
            T Get(const std::string &key) const
        {
            return fTable.Get<T>(key);
        }

        template<typename T>
            T Get(const std::string &key, const std::string &deflt) const
        {
            return fTable.Get<T>(key, deflt);
        }

        bool SetPtrAddress(const std::string &name, void *ptr, size_t cnt=0);

        bool  HasKey(const std::string &key)           const;
        bool  HasColumn(const std::string& col)        const;
        const Table::Columns&       GetColumns()       const;
        const Table::SortedColumns& GetSortedColumns() const;
        const Table::Keys&          GetKeys()          const;

        int64_t     GetInt(const std::string &key)   const;
        uint64_t    GetUInt(const std::string &key)  const;
        double      GetFloat(const std::string &key) const;
        std::string GetStr(const std::string &key)   const;

        size_t GetN(const std::string &key) const;

        size_t GetRow() const;

        operator bool() const;

        void PrintKeys() const;
        void PrintColumns() const;

        bool IsHeaderOk() const;
        virtual bool IsFileOk() const;

        bool IsCompressedFITS() const;

        virtual size_t GetNumRows() const;

        virtual size_t GetBytesPerRow() const;

        /**
         * Seek to the end of the current Table and check if there
         * is more data available in the file.
         */
        bool hasNextTable();

        /**
         * Go to the next table in the file.
         *
         * @param force: ignore missing header end keyword if true
         */
        void openNextTable(bool force = false);
};

template<>
std::string IFits::Entry::Get() const;

template<>
bool IFits::Entry::Get() const;

#endif
