/**
 * @file FlatProtobufZOFits.h
 *
 * Created on: Apr 16 2019
 *  Author: lyard
 */

 #ifndef FLATPROTOBUFZOFITS_H_
 #define FLATPROTOBUFZOFITS_H_

 #include <fstream>
 #include <iostream>
 #include <sstream>
 #include <set>

 #include "BasicDefs.h"
 #include "MemoryManager.h"
 #include "Queue.h"
 #include "FitsDefs.h"
 #include "Checksum.h"

 #include <google/protobuf/message.h>

 namespace ADH
 {

 namespace IO
 {

///////////////////////////////////////////////////////////////////////////////
//  FLAT PROTOBUF ZOFITS                                          
//////////////////////////////////////////////////////////////////////////////
//  New, optimized version of ProtobufZOFits                          
//  Flattened, i.e. classes hierarchy was merged into a single class            
//  Asynchronous, i.e. all operations to disk happen asynchronously             
//  Memory is allocated only once accross multiple files                        
//  Threads are started only once accross multiple files                        
//  V1.0 - questions: Etienne.Lyard@unige.ch                                    
//  Note: not much doc here: look at ProtobufZOFits.h/.cpp instead              
//////////////////////////////////////////////////////////////////////////////
 class FlatProtobufZOFits
 {
    public:

        FlatProtobufZOFits(uint32 num_tiles           = 1000,
                           uint32 rows_per_tile       = 100,
                           uint64 max_comp_mem        = 1000000,
                           const string default_comp  = "raw",
                           uint32 num_comp_threads    = 0,
                           uint32 comp_block_size_kb  = 0);

        virtual ~FlatProtobufZOFits();

        ///////////////////////////////////////////////////////////////////////
        //                          PUBLIC API                                    
        ///////////////////////////////////////////////////////////////////////

        void open(const char* filename);

        bool isOpen();

        bool close(bool display_stats=true);

        void flush();

        void writeTableHeader();

        void setCompressionBlockSize(uint32 size);

        int getPercentMemUsed();

        void vetoField(const std::string& name);

        void writeMessage(const google::protobuf::Message* message);

        void setDefaultCompression(const string& compression);
        void requestExplicitCompression(const string& field,
                                        const string& compression);


        void moveToNewTable(string tablename    ="DATA",
                            bool   display_stats=false,
                            bool   closing_file =false);

        uint64 getSizeWrittenToDisk();

        void SetHierarchKeyword(const string& longkey,
                                        string s,
                                        string comment);
        
        void SetDefaultHierarchKeywords();

        void   setStr(const std::string& key,
                      std::string        s,
                      const std::string& comment="");

        void   setInt(const std::string& key,
                      int64 value,
                      const std::string& comment="");

        void SetUInt(const std::string& key, 
                     uint64 value, 
                     const std::string& comment="");

        void   setFloat(const std::string& key,
                        double value,
                        const std::string& comment="");

        void   setBool(const std::string& key,
                       bool value,
                       const std::string& comment="");

        template <typename _T>
        _T* getANewMessage()
        {
            //let's try to recycle a message first
            google::protobuf::Message* to_return = getRecycledMessage();

            if (to_return != NULL)
            {
                if (dynamic_cast<_T*>(to_return) != NULL)
                    return dynamic_cast<_T*>(to_return);
                else
                {   //type of message has changed: discard current and get new, correct one
                    delete to_return;
                    return new _T();
                }
            }
            else
                return new _T();
        }

        uint64 _bytes_written;

        ///////////////////////////////////////////////////////////////////////
        //                     FITS TABLES                                               
        ///////////////////////////////////////////////////////////////////////
        //          All structures needed to write a FITS table                          
        ///////////////////////////////////////////////////////////////////////
        struct Key
        {
            std::string key;
            std::string value;
            std::string comment;
            std::string longkeyword;
            off_t       offset;
            bool        delim;   //used to handle also comments
            bool        changed;
            Checksum    checksum;

            Key(const std::string &k="");

            std::string Trim(const std::string &str);
            bool        FormatKey();
            bool        FormatComment();
            bool        check();
            size_t      CalcSize() const;
            std::string Compile();
            void        Out(std::ofstream &fout);
        };

        ///////////////////////////////////////////////////////////////////////
        ///////////////////////////////////////////////////////////////////////
        struct Table
        {
           struct Column
            {
                std::string name;
                size_t      offset;
                size_t      num;
                size_t      size;
                char        type;
            };

            off_t               offset;
            size_t              bytes_per_row;
            size_t              num_rows;
            size_t              num_cols;
            std::vector<Column> cols;

            Table();
        };

        ///////////////////////////////////////////////////////////////////////
        ///////////////////////////////////////////////////////////////////////
        struct CatalogEntry
        {
            CatalogEntry(int64 f=0,
                         int64 s=0);
            int64 first;   ///< Size of this column in the tile
            int64 second;  ///< offset of this column in the tile, from the start of the heap area
        } __attribute__((__packed__));


        ///////////////////////////////////////////////////////////////////////
        ///////////////////////////////////////////////////////////////////////
        typedef std::vector<CatalogEntry> CatalogRow;
        typedef std::list<CatalogRow>     CatalogType;

        ///////////////////////////////////////////////////////////////////////
        ///////////////////////////////////////////////////////////////////////
        struct CompressedColumn
        {
            CompressedColumn(const Table::Column& c,
                             const FITS::Compression& h);

            Table::Column col;             ///< the regular column entry
            FITS::Compression block_head;  ///< the compression data associated with that column
        };

        ///////////////////////////////////////////////////////////////////////
        //                       ZFITS OUTPUT                                                      
        ///////////////////////////////////////////////////////////////////////
        // Structure, or rather subclass used to write zfits asyncronously               
        ///////////////////////////////////////////////////////////////////////
        struct ZFitsOutput
        {
            ZFitsOutput(uint64 file_id, FlatProtobufZOFits& caller_param) : 
                                          table_start(0),          checksum_offset(0),
                                          real_row_width(0),       catalog_offset(0),
                                          catalog_size(0),         raw_heap_size(0),
                                          num_tiles_written(0),    total_num_columns(0),
                                          size_written_to_disk(0), file_descriptor(NULL),
                                          output_file(NULL),       descriptor(NULL),
                                          file_index(file_id),     caller(caller_param)
            {
            }

            std::vector<Key>    keys;
            Table               table;
            size_t              table_start;
            Checksum            datasum;
            Checksum            catalogsum;
            Checksum            headersum;
            int32               checksum_offset;
            uint32              real_row_width;
            CatalogType         catalog;
            int64               catalog_offset;
            uint64              catalog_size;
            uint64              raw_heap_size;
            uint64              num_tiles_written;
            uint32              total_num_columns;
            std::vector<uint32> columns_sizes;
            uint64              size_written_to_disk;
            std::string         table_name;
            std::string         file_name;
            FILE*               file_descriptor;
            std::ofstream*      output_file;
            std::vector<CompressedColumn>       real_columns;
            const google::protobuf::Descriptor* descriptor;
            uint64              file_index;
            std::map<int, int>  num_expected_child;

            std::set<std::string> _missing_fields;

            std::mutex          _catalog_fence;

            void vetoField(const std::string& name);
            bool isVetoed(const std::string& name);


            ///////////////////////////////////////////////////////////////////
            // REFERENCE TO CALLER TO USE ITS MEMBERS
            ///////////////////////////////////////////////////////////////////
            FlatProtobufZOFits& caller; 

            ///////////////////////////////////////////////////////////////////
            //     OUTPUT OPERATIONS                             
            ///////////////////////////////////////////////////////////////////
            void open();
            bool close(bool display_stats);
            void moveToNewTable();

            ///////////////////////////////////////////////////////////////////
            //     HEADER KEYS OPERATIONS                             
            ///////////////////////////////////////////////////////////////////
            bool Set(const std::string& key    ="",
                     bool               delim  =false,
                     const std::string& value  ="",
                     const std::string& comment="",
                     const std::string& longkeyword="");
            bool SetStr(  const std::string &key   , std::string s, const std::string &comment="");
            bool SetHierarchStr(std::string s, const std::string &comment="",const std::string &longkeyword="");
            bool SetInt(  const std::string &key   , int64       i, const std::string &comment="");
            bool SetUInt( const std::string &key   , uint64      i, const std::string &comment="");
            bool SetFloat(const std::string &key   , double      f, const std::string &comment="");
            bool SetBool( const std::string &key   , bool        b, const std::string &comment="");

            void SetDefaultKeys();

            std::string CommentFromType(char type);
            uint32      SizeFromType(char type);

            std::vector<Key>::iterator findkey(const std::string &key);
            std::vector<Key>::iterator findlongkey(const std::string &longkeyword);

            ///////////////////////////////////////////////////////////////////
            //                          COLUMNS OPERATIONS                               
            ///////////////////////////////////////////////////////////////////
            void initColumns(const google::protobuf::Message* message,
                                   uint64                     compression_block_size,
                                   uint64                     max_usable_mem,
                                   int32                      num_queues,
                                   FlatProtobufZOFits*        parent);


            void buildFitsColumns(const google::protobuf::Message& message,
                                  FlatProtobufZOFits* parent,
                                  const std::string& name="",
                                  const std::string& id="");

            std::vector<Table::Column>::const_iterator findcol(const std::string &name);

            bool AddColumn(uint32             cnt,
                           char               typechar,
                           const std::string& name,
                           const std::string& unit,
                           const std::string& comment      ="",
                           bool               addHeaderKeys=true);

            bool AddColumn(const FITS::Compression& comp,
                           uint32                   cnt,
                           char                     typechar,
                           const std::string&       name,
                           const std::string&       unit,
                           const std::string&       comment      ="",
                           bool                     addHeaderKeys=true);

            bool AddColumnByte(         const FITS::Compression& comp, uint32 cnt, const std::string& name, const std::string& unit="", const std::string& comment="");
            bool AddColumnChar(         const FITS::Compression& comp, uint32 cnt, const std::string& name, const std::string& unit="", const std::string& comment="");
            bool AddColumnShort(        const FITS::Compression& comp, uint32 cnt, const std::string& name, const std::string& unit="", const std::string& comment="");
            bool AddColumnInt(          const FITS::Compression& comp, uint32 cnt, const std::string& name, const std::string& unit="", const std::string& comment="");
            bool AddColumnLong(         const FITS::Compression& comp, uint32 cnt, const std::string& name, const std::string& unit="", const std::string& comment="");
            bool AddColumnFloat(        const FITS::Compression& comp, uint32 cnt, const std::string& name, const std::string& unit="", const std::string& comment="");
            bool AddColumnDouble(       const FITS::Compression& comp, uint32 cnt, const std::string& name, const std::string& unit="", const std::string& comment="");
            bool AddColumnBool(         const FITS::Compression& comp, uint32 cnt, const std::string& name, const std::string& unit="", const std::string& comment="");
            bool AddColumnSignedByte(   const FITS::Compression& comp, uint32 cnt, const std::string& name, const std::string& unit="", const std::string& comment="");
            bool AddColumnUnsignedShort(const FITS::Compression& comp, uint32 cnt, const std::string& name, const std::string& unit="", const std::string& comment="");
            bool AddColumnUnsignedInt(  const FITS::Compression& comp, uint32 cnt, const std::string& name, const std::string& unit="", const std::string& comment="");
            bool AddColumnUnsignedLong( const FITS::Compression& comp, uint32 cnt, const std::string& name, const std::string& unit="", const std::string& comment="");

            void addAnyArrayColumn(const google::protobuf::Message& message, const std::string& name);

            ///////////////////////////////////////////////////////////////////
            //            HEADER/FOOTER/CATALOG FORMATING OPERATIONS                     
            ///////////////////////////////////////////////////////////////////
            bool     WriteTableHeader();
            Checksum WriteFitsHeader();
            bool     WriteCatalog();
            Checksum WriteHeader();
            Checksum WriteHeader(ofstream &fout);
            void     AlignTo2880Bytes();
            Checksum UpdateHeaderChecksum();
            bool     AddComment(const std::string &comment);
            void     updateHeaderKeys(bool finalUpdate = false);
            void     End();

            uint32 ShrinkCatalog();
            CatalogRow& AddOneCatalogRow();

        
            ///////////////////////////////////////////////////////////////////
            //        PREPARE INPUT DATA FOR COMPRESSION                         
            ///////////////////////////////////////////////////////////////////
        
            template <typename T_>
            uint32 serialize(char*                                    target,
                             const google::protobuf::Message*         message,
                             const google::protobuf::FieldDescriptor* field,
                             const google::protobuf::Reflection*      reflec,
                             const int32                              col_index)
            {
                uint32 num_bytes_written = 0;

                if (field->is_repeated())
                {
                    int32 field_size = reflec->FieldSize(*message, field);
                    reinterpret_cast<uint32*>(target)[0] = field_size;
                    num_bytes_written += sizeof(uint32);

                    for (int32 i=0; i<field_size; i++)
                    {
                        reinterpret_cast<T_*>(target+num_bytes_written)[0] =
                            getProtobufRepeatedValue<T_>(*message, field, reflec, i);
                        num_bytes_written += sizeof(T_);
                    }

                    if ((uint32)(field_size) > columns_sizes[col_index])
                        columns_sizes[col_index] = field_size;
                }
                else
                {
                    reinterpret_cast<T_*>(target)[0] =
                        getProtobufValue<T_>(*message, field, reflec);
                    num_bytes_written += sizeof(T_);
                }

                return num_bytes_written;
            }

            template <typename T_>
            T_ getProtobufValue(const google::protobuf::Message& message,
                                const google::protobuf::FieldDescriptor* field,
                                const google::protobuf::Reflection* reflec)
            {
                std::ostringstream str;
                std::cout << "Unhandled type (" << typeid(T_).name();
                std::cout << ") in getProtobufValue... specialization is missing";
                throw std::runtime_error(str.str());
                return T_();
            }

            template <typename T_>
            T_ getProtobufRepeatedValue(const google::protobuf::Message& message,
                                        const google::protobuf::FieldDescriptor* field,
                                        const google::protobuf::Reflection* reflec,
                                        int32 index)
            {
                std::ostringstream str;
                std::cout << "Unhandled type (" << typeid(T_).name();
                std::cout << ") in getProtobufRepeatedValue... specialization ";
                std::cout << "is missing";
                throw std::runtime_error(str.str());
                return T_();
            }

        }; //ZFitsOutput

        ///////////////////////////////////////////////////////////////////////
        // WE FLATPROTOBUFZOFITS HAS TO BE FRIEND WITH ZFITSOUTPUT
        // So that it can access its members that used to be global variables
        /////////////////////////////////////////////////////////////////////// 
        friend class ZFitsOutput;

    protected:

        ///////////////////////////////////////////////////////////////////////
        // THREADS INPUTS
        ///////////////////////////////////////////////////////////////////////                                                                                                  
        // Structure, given as input to the threads (compression and output to disk)                                                                                                      
        ///////////////////////////////////////////////////////////////////////
        struct TableOperation
        {
            bool        move_to_new_table;
            bool        open_file;
            bool        close_file;
            bool        display_stats;
            bool        write_table_header;

            TableOperation();
            bool IsSet() const;
        };

        struct CompressionTarget
        {
            CompressionTarget(CatalogRow&  row,
                              ZFitsOutput* this_output,
                              uint64       f_index);

            CatalogRow&                         catalog;
            uint32                              targetId;
            std::shared_ptr<vector<const google::protobuf::Message*>> messages;
            std::list<std::shared_ptr<char>>    buffers;

            ZFitsOutput*                        output;
            uint64                              file_index;
            TableOperation                      table_operation;
        };

        struct WriteToDiskTarget
        {
            WriteToDiskTarget(ZFitsOutput* this_output);
            bool operator < (const WriteToDiskTarget& other) const;
            uint64                      targetId;            ///< Tile number, for sorting inputs before writing to disk
            list<uint32>                num_bytes_in_buffer; ///< Number of bytes to write per input buffer
            list<uint32>                num_bytes_originally;
            list<std::shared_ptr<char>> buffers;             ///< Actual data to be written
            ZFitsOutput*                output;
            uint64                      file_index;
            TableOperation              table_operation;
        };

        ///////////////////////////////////////////////////////////////////////
        // CLASS MEMBERS
        ///////////////////////////////////////////////////////////////////////
        // Data used internally by Flat protobuf ZOFits                       
        ///////////////////////////////////////////////////////////////////////
        vector<uint64> _comp_target_counter;
        uint64         _compression_block_size;
        vector<uint64> _next_buffer_to_write;
        uint64         _current_file_index;
        int32          _num_queues;
        int32          _num_writer_threads;
        uint64         _max_usable_mem;
        ZFitsOutput*   _current_table;
        std::mutex     _recycle_fence;
        MemoryManager  _memory_pool;
        int32          _zstd_level;

        uint32 _num_tiles;
        uint32 _num_rows_per_tile;
    public:
        uint64 _size_written_to_disk;
        uint64 _size_uncompressed_to_disk;
        uint64 _previous_size_written_to_disk;
        uint64 _previous_size_uncompressed_to_disk;

    protected:
        std::set<std::string> _vetoed_fields;
        std::set<std::string> _allowed_fields;
        std::vector<uint16>                        _default_comp;
        std::map<std::string, std::vector<uint16>> _explicit_comp;

        std::vector<Queue<CompressionTarget>>                 _compression_queues;
        std::vector<Queue<WriteToDiskTarget, QueueMin<WriteToDiskTarget>>> _write_to_disk_queue;

        std::shared_ptr<std::vector<const google::protobuf::Message*>> _incoming_data;
        std::map<const google::protobuf::Descriptor*, std::list<google::protobuf::Message*> > _recycled_messages;

        ///////////////////////////////////////////////////////////////////////
        // MEMBERS USED BY ZFITSOUTPUT TO PASS FILES PARAMETERS ASYNCHRONOUSLY
        ///////////////////////////////////////////////////////////////////////
        size_t*    global_table_start     = NULL;
        ofstream** global_output_file     = NULL;
        FILE**     global_file_descriptor = NULL;

        ///////////////////////////////////////////////////////////////////////
        // CLASS METHODS
        ///////////////////////////////////////////////////////////////////////
        // Methods used internally by Flat protobuf ZOFits                 
        ///////////////////////////////////////////////////////////////////////
        google::protobuf::Message* getRecycledMessage();

        ///////////////////////////////////////////////////////////////////////
        // HEADER KEYS OPERATIONS             
        ///////////////////////////////////////////////////////////////////////
        bool isVetoed(const std::string& name);
        bool isAllowed(const std::string& name);

        ///////////////////////////////////////////////////////////////////////
        // WRITE TO DISK OPERATIONS                           
        ///////////////////////////////////////////////////////////////////////
        bool writeToDisk(const WriteToDiskTarget& target);

        bool writeCompressedDataToDisk(char*        src,
                                       const uint32 sizeToWrite,
                                       ZFitsOutput* output);

        ///////////////////////////////////////////////////////////////////////
        // COMPRESSION OPERATIONS                          
        ///////////////////////////////////////////////////////////////////////
        void launchNewCompression();

        bool compressMessages(const CompressionTarget& comp_target);

        void compressMessageFields(const vector<const google::protobuf::Message*>& messages,
                                    int32&                 col_index,
                                    char*                  gather_buf,
                                    shared_ptr<char>&      compres_buff,
                                    int32&                 comp_bytes_written,
                                    int32&                 comp_bytes_read,
                                    CompressionTarget&     comp_target,
                                    WriteToDiskTarget&     disk_target,
                                    const string&          name="");

        void compressBuffer(char*              src,
                            shared_ptr<char>&  dest,
                            int32              num_bytes,
                            int32&             bytes_in_dest,
                            int32&             col_index,
                            CompressionTarget& comp_target);

        void checkArrayValueSize(int32 num_bytes,
                                 int32 multiple,
                                 FITS::CompressionProcess_t ongoing_process);

        void splitHiLo16(char* buffer, uint32 num_bytes);
        void splitHiLo32(char* buffer, uint32 num_bytes);
        uint32 applySMOOTHING(char* data, uint32 numElems);


 }; //FlatProtobufZOFits

///////////////////////////////////////////////////////////////////////
// TEMPLATES SPECIALIZATION
///////////////////////////////////////////////////////////////////////
 template <> uint32 FlatProtobufZOFits::ZFitsOutput::serialize<AnyArray>(char* target, const google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const int32 col_index);
 template <> uint32 FlatProtobufZOFits::ZFitsOutput::serialize<google::protobuf::EnumValueDescriptor>(char* target, const google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const int32 col_index);
 template <> uint32 FlatProtobufZOFits::ZFitsOutput::serialize<char>(char* target, const google::protobuf::Message* message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, const int32 col_index);

 template <> uint32 FlatProtobufZOFits::ZFitsOutput::getProtobufValue<uint32>(const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);
 template <> int32  FlatProtobufZOFits::ZFitsOutput::getProtobufValue<int32> (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);
 template <> uint64 FlatProtobufZOFits::ZFitsOutput::getProtobufValue<uint64>(const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);
 template <> int64  FlatProtobufZOFits::ZFitsOutput::getProtobufValue<int64> (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);
 template <> double FlatProtobufZOFits::ZFitsOutput::getProtobufValue<double>(const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);
 template <> float  FlatProtobufZOFits::ZFitsOutput::getProtobufValue<float> (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);
 template <> bool   FlatProtobufZOFits::ZFitsOutput::getProtobufValue<bool>  (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec);

 template <> uint32 FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<uint32>(const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);
 template <> int32  FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<int32> (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);
 template <> uint64 FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<uint64>(const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);
 template <> int64  FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<int64> (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);
 template <> double FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<double>(const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);
 template <> float  FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<float> (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);
 template <> bool   FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<bool>  (const google::protobuf::Message& message, const google::protobuf::FieldDescriptor* field, const google::protobuf::Reflection* reflec, int32 index);

 }; //namespace IO
 }; //namespace ADH
 #endif //FLATPROTOBUFZOFITS_H_
