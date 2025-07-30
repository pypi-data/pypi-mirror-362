/**
 *  @file FlatProtobufZOFits.cpp
 *
 *  Created on: Apr 17, 2019
 *      Author: lyard
 */

 #include "FlatProtobufZOFits.h"
 #include "CMakeDefs.h"
 #include "Logger.h"

 #include <zlib.h>
 #include "minilzo.h"
 #include "Huffman.h"
 #include "zstd.h"

 #include <sys/file.h>
 #include <iomanip>
 
 // For min_element on old compilers
 #include <algorithm>

// For ceil()
 #include <cmath>

 using namespace std;
 using namespace ADH::ColoredOutput;
 using namespace ADH::Core;
 using namespace google::protobuf;

 namespace ADH
 {

 namespace IO
 {

    ///////////////////////////////////////////////////////////////////////////
    // STATIC STUFF
    ///////////////////////////////////////////////////////////////////////////
    //a dummy catalog row to initialize queued structures
    //for disk operations
    FlatProtobufZOFits::CatalogRow dummy_catalog_row;

 //////////////////////////////////////////////////////////////////////////////
 // CONSTRUCTOR
 //////////////////////////////////////////////////////////////////////////////
 FlatProtobufZOFits::FlatProtobufZOFits(uint32 num_tiles,
                                        uint32 rows_per_tile,
                                        uint64 max_comp_mem,
                                        const string default_comp,
                                        uint32 num_comp_threads,
                                        uint32 comp_block_size_kb)
 {

    _size_written_to_disk               = 0;
    _size_uncompressed_to_disk          = 0;
    _previous_size_written_to_disk      = 0;
    _previous_size_uncompressed_to_disk = 0;
    _num_tiles                          = 0;
    _num_rows_per_tile                  = 0;

    _current_table      = NULL;
    _max_usable_mem     = max_comp_mem*1000;
    _memory_pool        = MemoryManager(0, max_comp_mem*1000);
    _incoming_data      = shared_ptr<vector<const Message*>>(new vector<const Message*>);
    _current_file_index = 0;
    _num_writer_threads = 1;
    _num_tiles          = num_tiles==0 ? 1 : num_tiles;
    _num_rows_per_tile  = rows_per_tile;

    _compression_block_size = comp_block_size_kb*1024;
    _memory_pool.setChunkSize(_compression_block_size);

    _zstd_level = 0;

#ifdef __clang__
    if (num_comp_threads != 0)
    {
        ADH_info << "Overriding number of desired threads because of clang";
        ADH_info.flush();
        num_comp_threads = 0;
    }
#endif

     // Set compression threads -1 for write to disk queue
     if (num_comp_threads == 0)
     {
        _num_queues = 0;
        ADH_info << "Will compress data sequentially";
     }
     else
     {
        _num_queues = num_comp_threads - 1;

        if (_num_queues == 0 && num_comp_threads == 1)
        {
            _num_queues = 1;
            ADH_warn << "WARNING: took one extra thread for writing to disk.";
            ADH_warn.flush();
        }

        if (_num_queues > 10)
        {
            _num_queues--;
            _num_writer_threads++;
        }

        ADH_info << "Will use " << _num_queues << " thread(s) to compress data + " << _num_writer_threads << " to write to disk";
     }

     ADH_info.flush();

    _compression_queues.resize((_num_queues<1)?1:_num_queues, Queue<CompressionTarget>(
                    bind(&FlatProtobufZOFits::compressMessages, this, placeholders::_1), false));
    _write_to_disk_queue.resize(_num_writer_threads, Queue<WriteToDiskTarget, QueueMin<WriteToDiskTarget>>(
                    bind(&FlatProtobufZOFits::writeToDisk,this,placeholders::_1), false));

    _next_buffer_to_write.resize(_write_to_disk_queue.size());
    _comp_target_counter.resize(_write_to_disk_queue.size());

    for (auto it=_next_buffer_to_write.begin(); it!=_next_buffer_to_write.end(); it++)
        *it = 0;
    for (auto it=_comp_target_counter.begin(); it!=_comp_target_counter.end();it++)
        *it = 0;

    _compression_queues.front().setPromptExecution(_num_queues==0);
    _write_to_disk_queue.front().setPromptExecution(_num_queues==0);

    if (_num_queues != 0)
    {
        for (auto it=_compression_queues.begin(); it!= _compression_queues.end(); it++)
            it->start();

        for (auto it=_write_to_disk_queue.begin(); it!=_write_to_disk_queue.end();it++)
            it->start();
    }

    setDefaultCompression("raw");
    setDefaultCompression(default_comp);

   //if (global_table_start != NULL)
   //     throw runtime_error("Only one object of type FlatProtobufZOFits can be created at once... sorry.");

    global_table_start     = new size_t[_num_writer_threads];
    global_output_file     = new ofstream*[_num_writer_threads];
    global_file_descriptor = new FILE*[_num_writer_threads];

    for (int32 i=0;i<_num_writer_threads;i++)
        global_table_start[i] = 0;
 }

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
 FlatProtobufZOFits::~FlatProtobufZOFits()
 {
    flush();

    for (auto it=_recycled_messages.begin(); it!=_recycled_messages.end(); it++)
    {
        for (auto jt=it->second.begin(); jt!=it->second.end(); jt++)
            delete *jt;
    }

    delete [] global_table_start;
    delete [] global_output_file;
    delete [] global_file_descriptor;
    global_table_start = NULL;
    global_output_file = NULL;
    global_file_descriptor = NULL;
 }

///////////////////////////////////////////////////////////////////////////////
// PUBLIC API
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::open(const char* filename)
{
    if (_current_table != NULL)
        throw runtime_error("Better close current table before opening a new one...");

    _current_table = new ZFitsOutput(_current_file_index, *this);

    _current_table->datasum     = 0;
    _current_table->headersum   = 0;
    _current_table->table_start = 0;
    _current_table->file_name   = string(filename);

    _current_table->table = Table();
    _current_table->keys.clear();

    _current_table->SetStr( "XTENSION", "BINTABLE", "binary table extension");
    _current_table->SetInt( "BITPIX",            8, "8-bit bytes");
    _current_table->SetInt( "NAXIS",             2, "2-dimensional binary table");
    _current_table->SetInt( "NAXIS1",            0, "width of table in bytes");
    _current_table->SetInt( "NAXIS2",            0, "number of rows in table");
    _current_table->SetInt( "PCOUNT",            0, "size of special data area");
    _current_table->SetInt( "GCOUNT",            1, "one data group (required keyword)");
    _current_table->SetInt( "TFIELDS",           0, "number of fields in each row");
    _current_table->SetStr( "EXTNAME",          "", "name of extension table");
    _current_table->SetStr( "CHECKSUM", "0000000000000000", "Checksum for the whole HDU");
    _current_table->SetStr( "DATASUM",  "       0", "Checksum for the data block");
    _current_table->SetBool("ZTABLE",         true, "Table is compressed");
    _current_table->SetInt( "ZNAXIS1",           0, "Width of uncompressed rows");
    _current_table->SetInt( "ZNAXIS2",           0, "Number of uncompressed rows");
    _current_table->SetInt( "ZPCOUNT",           0, "");
    _current_table->SetInt( "ZHEAPPTR",          0, "");
    _current_table->SetInt( "ZTILELEN", _num_rows_per_tile, "Number of rows per tile");
    _current_table->SetInt( "THEAP",             0, "");
    _current_table->SetStr( "RAWSUM", "         0", "Checksum of raw little endian data");
    _current_table->SetFloat("ZRATIO",           0, "Compression ratio");
    _current_table->SetInt( "ZSHRINK",           1, "Catalog shrink factor");

    _current_table->catalog_size    = 0;
    _current_table->real_row_width  = 0;
    _current_table->catalog_offset  = 0;
    _current_table->catalog_size    = 0;
    _current_table->checksum_offset = 0;
    _current_table->real_columns.clear();
    _current_table->catalog.clear();
    _current_table->catalogsum.reset();

    _current_table->output_file = new ofstream();

    //launch a special compression, aka open me
    CompressionTarget comp_target(dummy_catalog_row,
                                  _current_table,
                                  _current_file_index);
    comp_target.table_operation.open_file = true;

    comp_target.targetId = ++(_comp_target_counter[_current_file_index]);

    const auto imin = min_element(_compression_queues.begin(),
                                  _compression_queues.end());

    imin->emplace(comp_target);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::isOpen()
{
    return (_current_table != NULL);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::close(bool display_stats)
{

    if (!isOpen())
        return false;

    //flush any data waiting to be written
    if (_incoming_data->size() != 0)
        launchNewCompression();

    //launch a special compression, aka close me
    CompressionTarget comp_target(dummy_catalog_row,
                                  _current_table,
                                  _current_file_index);

    comp_target.table_operation.move_to_new_table = true;
    comp_target.table_operation.close_file        = true;
    comp_target.table_operation.display_stats     = display_stats;

    comp_target.targetId = ++(_comp_target_counter[_current_file_index]);

    const auto imin = min_element(_compression_queues.begin(),
                                  _compression_queues.end());

    _current_file_index = (_current_file_index+1)%_num_writer_threads;

    imin->emplace(comp_target);

    _current_table = NULL;

    return true;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::flush()
{
    if (_current_table != NULL)
        close(true);

    //wait for all compression threads to finish
    for (auto it=_compression_queues.begin(); it!= _compression_queues.end(); it++)
        it->wait();

    //also wait for data to be flushed to disk
    for (auto it=_write_to_disk_queue.begin(); it!= _write_to_disk_queue.end();it++)
        it->wait();
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::writeTableHeader()
{
    //launch a special compression, aka close me
    CompressionTarget comp_target(dummy_catalog_row,
                                  _current_table,
                                  _current_file_index);

    comp_target.table_operation.write_table_header = true;

    comp_target.targetId = ++(_comp_target_counter[_current_file_index]);

    const auto imin = min_element(_compression_queues.begin(),
                                  _compression_queues.end());

    imin->emplace(comp_target);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::setCompressionBlockSize(uint32 size)
{
    _compression_block_size = size;
    _memory_pool.setChunkSize(_compression_block_size);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
int FlatProtobufZOFits::getPercentMemUsed()
{
    return (int)(100.f*((float)(_memory_pool.getInUse()) / (float)(_memory_pool.getMaxMemory())));
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::vetoField(const string& name)
{
        _vetoed_fields.insert(name);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::ZFitsOutput::vetoField(const string& name)
{
        _missing_fields.insert(name);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::writeMessage(const Message* message)
{
    if (_current_table->descriptor == NULL)
    {
        _current_table->initColumns(message,
                                    _compression_block_size,
                                    _max_usable_mem,
                                    _num_queues,
                                    this);
        writeTableHeader();
    }

    if (_current_table->descriptor != message->GetDescriptor())
        throw runtime_error("Only one kind of message can be written at a given time...");

    _incoming_data->push_back(message);

    _current_table->table.num_rows++;

    if (_incoming_data->size() == _num_rows_per_tile)
    {
        launchNewCompression();
    }
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::setDefaultCompression(const string& compression)
{
    requestExplicitCompression("default", compression);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::moveToNewTable(string tablename,
                                        bool   display_stats,
                                        bool   closing_file)
{
    if (_incoming_data->size() != 0)
        launchNewCompression();

    //launch a special compression, aka close me
    CompressionTarget comp_target(dummy_catalog_row,
                                  _current_table,
                                  _current_file_index);

    comp_target.table_operation.move_to_new_table = true;
    comp_target.table_operation.close_file        = closing_file;
    comp_target.table_operation.display_stats     = display_stats;

    comp_target.targetId = ++(_comp_target_counter[_current_file_index]);

    const auto imin = min_element(_compression_queues.begin(),
                                  _compression_queues.end());

    if (closing_file)
    {
        imin->emplace(comp_target);
        return;
    }

    ZFitsOutput* previous_table = _current_table;

    _current_table = new ZFitsOutput(_current_file_index, *this);

    _current_table->output_file     = previous_table->output_file;
    _current_table->file_name       = previous_table->file_name;

    //We can go ahead and erase the previous _current_table in the writing thread
    imin->emplace(comp_target);

    //let the next table know that it does NOT start from beginning of file.
    //NO ! we don't do it here any longer as everything is asynchronous now.
    _current_table->table_start = 0;

    //remember the new table name
    _current_table->table_name = tablename;

    //reset quantities used to keep track of a given table's content
    _current_table->table             = Table();
    _current_table->descriptor        = NULL;
    _current_table->total_num_columns = 0;
    _current_table->columns_sizes.clear();
    _current_table->datasum.reset();
    _current_table->headersum.reset();
    _current_table->real_row_width    = 0;
    _current_table->catalog_offset    = 0;
    _current_table->catalog_size      = 0;
    _current_table->checksum_offset   = 0;
    _current_table->num_tiles_written = 0;
    _current_table->keys.clear();
    _current_table->real_columns.clear();
    _current_table->catalog.clear();
    _current_table->catalogsum.reset();

    //add standard FITS header entries
    _current_table->SetStr("XTENSION",   "BINTABLE",         "binary table extension");
    _current_table->SetInt("BITPIX",     8,                  "8-bit bytes");
    _current_table->SetInt("NAXIS",      2,                  "2-dimensional binary table");
    _current_table->SetInt("NAXIS1",     0,                  "width of table in bytes");
    _current_table->SetInt("NAXIS2",     0,                  "number of rows in table");
    _current_table->SetInt("PCOUNT",     0,                  "size of special data area");
    _current_table->SetInt("GCOUNT",     1,                  "one data group (required keyword)");
    _current_table->SetInt("TFIELDS",    0,                  "number of fields in each row");
    _current_table->SetStr("EXTNAME",    tablename,          "name of extension table");
    _current_table->SetStr("CHECKSUM",   "0000000000000000", "Checksum for the whole HDU");
    _current_table->SetStr("DATASUM",    "         0",       "Checksum for the data block");

    _current_table->SetBool( "ZTABLE",   true,               "Table is compressed");
    _current_table->SetInt(  "ZNAXIS1",  0,                  "Width of uncompressed rows");
    _current_table->SetInt(  "ZNAXIS2",  0,                  "Number of uncompressed rows");
    _current_table->SetInt(  "ZPCOUNT",  0,                  "");
    _current_table->SetInt(  "ZHEAPPTR", 0,                  "");
    _current_table->SetInt(  "ZTILELEN", _num_rows_per_tile,    "Number of rows per tile");
    _current_table->SetInt(  "THEAP",    0,                  "");
    _current_table->SetStr(  "RAWSUM",   "         0",       "Checksum of raw little endian data");
    _current_table->SetFloat("ZRATIO",   0,                  "Compression ratio");
    _current_table->SetInt(  "ZSHRINK",  1,                  "Catalog shrink factor");

    _current_table->SetStr("ADHREV", GIT_REV_ADH, "ADH GIT hash");
    _current_table->SetStr("APISREV", GIT_REV_ADH_APIS, "ADH-APIS GIT hash");
    _current_table->SetInt("ADHMAJ", ADH_VERSION_MAJOR, "Major version of ADH package");
    _current_table->SetInt("ADHMIN", ADH_VERSION_MINOR, "Minor version of ADH package");
}
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::SetHierarchKeyword(const string& longkey,
                                        string s,
                                        string comment)
{
    if (_current_table == NULL) throw runtime_error("No open table right now...");
    
    _current_table->SetHierarchStr(s, comment,longkey);
}
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::SetDefaultHierarchKeywords()
{
    if (_current_table == NULL) throw runtime_error("No open table right now...");
        
    _current_table->SetHierarchStr("Array Data Handler", "", "CTA ACTIVITY NAME");
    _current_table->SetHierarchStr("Software", "", "CTA ACTIVITY TYPE");
    _current_table->SetHierarchStr("ADH", "", "CTA ACTIVITY SOFTWARE NAME");
    _current_table->SetHierarchStr(to_string(ADH_VERSION_MAJOR), "", "CTA ACTIVITY SOFTWARE VERSION");
    const time_t t1 = time(NULL);
    const struct tm *tmp1 = gmtime(&t1);
    string str(19, '\0');
    if (tmp1 && strftime(const_cast<char*>(str.data()), 20, "%Y-%m-%dT%H:%M:%S", tmp1))
        _current_table->SetHierarchStr( str, "","CTA ACTIVITY START");
    _current_table->SetHierarchStr("", "","CTA ACTIVITY END");
}
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
uint64 FlatProtobufZOFits::getSizeWrittenToDisk()
{
    return _size_written_to_disk;
};


///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::setStr(const string &key, string s, const string &comment)
{
    if (_current_table == NULL) throw runtime_error("No open table right now...");
    if (!_current_table->SetStr(key, s, comment)) {
        throw runtime_error("Failed setting key:" + key);
    };
};

void FlatProtobufZOFits::setInt(const string &key, int64 value, const string &comment)
{
    if (_current_table == NULL) throw runtime_error("No open table right now...");
    if (!_current_table->SetInt(key, value, comment)) {
        throw runtime_error("Failed setting key: " + key);
    };
};

void FlatProtobufZOFits::SetUInt(const string& key, uint64 value, const string& comment)
{
    if (_current_table == NULL) throw runtime_error("No open table right now...");
    if (!_current_table->SetUInt(key, value, comment)) {
        throw runtime_error("Failed setting key: " + key);
    };
};

void FlatProtobufZOFits::setFloat(const string &key, double value, const string &comment)
{
    if (_current_table == NULL) throw runtime_error("No open table right now...");
    if (!_current_table->SetFloat(key, value, comment)) {
        throw runtime_error("Failed setting key: " + key);
    };
};

void FlatProtobufZOFits::setBool(const string &key, bool value, const string &comment)
{
    if (_current_table == NULL) throw runtime_error("No open table right now...");
    if (!_current_table->SetBool(key, value, comment)) {
        throw runtime_error("Failed setting key: " + key);
    };
};

///////////////////////////////////////////////////////////////////////////////
//  FITS TABLES
///////////////////////////////////////////////////////////////////////////////
FlatProtobufZOFits::
Key::Key(const string &k) : key(k),
                            offset(0),
                            delim(false),
                            changed(true)
{
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
string FlatProtobufZOFits::
       Key::Trim(const string &str)
{
    const size_t first = str.find_first_not_of(' ');
    const size_t last  = str.find_last_not_of(' ');

    if (string::npos==first || string::npos==last)
        return string();

    return str.substr(first, last-first+1);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     Key::FormatKey()
{
    key = Trim(key);
    if (key.empty())
    {
        throw runtime_error("Key name empty.");
    }
    if (key.size()>8)
    {
        ostringstream sout;
        sout << "Key '" << key << "' exceeds 8 bytes.";
        throw runtime_error(sout.str());
    }

    for (string::const_iterator c=key.cbegin(); c<key.cend(); c++)
        if ((*c<'A' || *c>'Z') && (*c<'0' || *c>'9') && *c!='-' && *c!='_')
        {
            ostringstream sout;
            sout << "Invalid character '" << *c
                 << "' found in key '" << key << "'";
            throw runtime_error(sout.str());
        }

    return true;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     Key::FormatComment()
{
    comment = Trim(comment);

    for (string::const_iterator c=key.cbegin(); c<key.cend(); c++)
        if (*c<32 || *c>126)
        {
            ostringstream sout;
            sout << "Invalid character '" << *c
                 << "' [" << int(*c) << "] found in comment '"
                 << comment << "'";
            throw runtime_error(sout.str());
        }

    return true;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     Key::check()
{
    if (!FormatKey())
        return false;

    if (!FormatComment())
        return false;

    size_t sz = CalcSize();
    if (sz<=80)
        return true;

    comment = "";

    sz = CalcSize();
    if (sz<=80)
    {
        return true;
    }

    ostringstream sout;
    sout << "Size " << sz << " of entry for key '"
         << key << "' exceeds 80 characters even without comment.";
    throw runtime_error(sout.str());
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
size_t FlatProtobufZOFits::
       Key::CalcSize() const
{
    if (!delim)
        return 10+comment.size();
    if (longkeyword!="")
        return 41 + (value.size()<20?20:value.size())+ 3 + comment.size();
    return 10 + (value.size()<20?20:value.size()) + 3 + comment.size();
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
string FlatProtobufZOFits::
       Key::Compile()
{
    ostringstream sout;

    if (delim && key=="HIERARCH")
    {
        sout << left << setw(39) << key+" "+longkeyword;
        sout << "= ";
        sout << (!value.empty() && value[0]=='\''?left:right);
        sout << setw(20) << value << left;
        if (!comment.empty())
            sout << " / " << comment;
        return sout.str();
    }

    sout << left << setw(8) << key;

    if (!delim)
    {
        sout << "  " << comment;
        return sout.str();
    }

    sout << "= ";
    sout << (!value.empty() && value[0]=='\''?left:right);
    sout << setw(20) << value << left;

    if (!comment.empty())
        sout << " / " << comment;

    return sout.str();
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::
     Key::Out(ofstream &fout)
{
    if (!changed)
        return;

    string str = Compile();
    str.insert(str.end(), 80-str.size(), ' ');

    if (offset==0)
        offset = fout.tellp();

    fout.seekp(offset);
    fout << str;

    checksum.reset();
    checksum.add(str.c_str(), 80);

    changed = false;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
FlatProtobufZOFits::
Table::Table(): offset(0),
                bytes_per_row(0),
                num_rows(0),
                num_cols(0)
{
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
FlatProtobufZOFits::
CatalogEntry::CatalogEntry(int64 f,
                           int64 s) : first(f),
                                      second(s)
{
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
FlatProtobufZOFits::
CompressedColumn::CompressedColumn(const Table::Column&     c,
                                   const FITS::Compression& h) : col(c),
                                                                 block_head(h)
{
}

///////////////////////////////////////////////////////////////////////////////
//  ZFITS OUTPUT
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::
     ZFitsOutput::open()
{

#ifndef __clang__
    //open file the posix way so that we can take a lock on it
    file_descriptor = fopen(file_name.c_str(), "w");

    //lock file
    if (file_descriptor != NULL && strcmp(file_name.c_str(), "/dev/null"))
        if (flock(fileno(file_descriptor), LOCK_EX | LOCK_NB))
        {
            cout << "Filename : " << file_name << endl;
            throw runtime_error("Could not lock file.");
        }
#endif

    output_file->open(file_name);

    if (!output_file->good())
    {
        ostringstream str;
        str << "Could not open file " << file_name;
        throw runtime_error(str.str());
    }
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::close(bool display_stats)
{
    if (output_file == NULL || !output_file->is_open())
        return true;

    moveToNewTable();

    output_file->close();

    caller.global_table_start[file_index] = 0;
    caller.global_output_file[file_index] = NULL;
    caller.global_file_descriptor[file_index] = NULL;

#ifndef __clang__
    if (file_descriptor != NULL)
    {
        flock(fileno(file_descriptor), LOCK_UN);
        fclose(file_descriptor);
    }
    file_descriptor = NULL;
#endif

    delete output_file;

    if (display_stats)
    {
        ADH_info << "Closed  " << file_name;
        ADH_info.flush();
    }

    return true;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::
     ZFitsOutput::moveToNewTable()
{
    //remember where the last data item finished
    off_t end_of_data = output_file->tellp();

    //update date end only if blank. Otherwise it means that it was manually set
    vector<Key>::iterator date_end = findkey("DATEEND");
    if (date_end != keys.end() && date_end->value == "''")
    {
        const time_t t0 = time(NULL);
        const struct tm *tmp1 = gmtime(&t0);
        string str(19, '\0');
        if (tmp1 && strftime(const_cast<char*>(str.data()), 20, "%Y-%m-%dT%H:%M:%S", tmp1))
            SetStr("DATEEND", str, "File closing date");
    }

    caller.global_output_file[file_index]     = output_file;
    caller.global_file_descriptor[file_index] = file_descriptor;

    // if we are still at the beginning of the table,
    // it means that nothing was written yet: assume
    // that we are starting the very first table
    if (table_start == (size_t)(output_file->tellp()))
    {
        return;
    }

    //otherwise we are actually moving to a new table.

    //update FITS values
    updateHeaderKeys(true);

    //write the actual catalog data
    WriteCatalog();

    datasum += catalogsum;

    const Checksum checksm = UpdateHeaderChecksum();

    if (!(checksm+datasum).valid())
        throw runtime_error("Wrong checksum while finalizing table "+table_name);

    //move back to the end of the data and finalize FITS structure
    output_file->seekp(end_of_data);

    AlignTo2880Bytes();

    caller.global_table_start[file_index] = output_file->tellp();
}

///////////////////////////////////////////////////////////////////////////////
//  HEADER KEYS OPERATIONS
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::Set(const string& key,
                            bool    delim,
                      const string& value,
                      const string& comment,
                      const string& longkeyword)
{
    // If no delimit add the row no matter if it alread exists
    if (delim && longkeyword=="")
    {
        // if the row already exists: update it
        auto it = findkey(key);
        if (it!=keys.end())
        {
            it->value   = value;
            it->changed = true;
            return true;
        }
    }
    if (delim && longkeyword!="")
    {
        // if the row already exists: update it
        auto it = findlongkey(longkeyword);
        if (it!=keys.end())
        {
            it->value   = value;
            it->changed = true;
            return true;
        }
    }

    Key entry;
    entry.key     = key;
    entry.delim   = delim;
    entry.value   = value;
    entry.comment = comment;
    entry.offset  = 0;
    entry.changed = true;
    entry.longkeyword=longkeyword;

    if (!entry.check())
        return false;

    keys.push_back(entry);
    return true;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::SetStr(const string& key,
                               string  s,
                         const string& comment)
{
    for (uint i=0; i<s.length(); i++)
        if (s[i]=='\'')
            s.insert(i++, "\'");

    return Set(key, true, "'"+s+"'", comment);
}
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::SetHierarchStr(string  s,
                         const string& comment,
                         const string& longkeyword)
{
    for (uint i=0; i<s.length(); i++)
        if (s[i]=='\'')
            s.insert(i++, "\'");

    return Set("HIERARCH", true, "'"+s+"'", comment, longkeyword);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::SetInt(const string& key,
                               int64   i,
                         const string& comment)
{
    ostringstream sout;
    sout << i;

    return Set(key, true, sout.str(), comment);
}

bool FlatProtobufZOFits::
     ZFitsOutput::SetUInt(const string& key, 
                                uint64  i,
                          const string& comment)
{
    ostringstream sout;
    sout << i;

    return Set(key, true, sout.str(), comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::SetFloat(const string& key,
                                  double f,
                           const string& comment)
{
    ostringstream sout;

    if (ceil(f) != f)
        sout << setprecision(f>1e-100 && f<1e100 ? 15 : 14);
    else
        sout << setprecision(20); //Max num digits of long unsigned

    sout << f;

    string str = sout.str();

    replace(str.begin(), str.end(), 'e', 'E');

    if (str.find_first_of('E')==string::npos && str.find_first_of('.')==string::npos)
        str += ".";

    return Set(key, true, str, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::SetBool(const string& key,
                                   bool b,
                          const string& comment)
{
    return Set(key, true, b?"T":"F", comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::
     ZFitsOutput::SetDefaultKeys()
{
    SetStr("CREATOR",  typeid(*this).name(),   "Class that wrote this file");
    SetStr("COMPILED", getIsoBuildTimestamp(), "Compile time");
    SetStr("ORIGIN",   "CTA",                  "Institution that wrote the file");
    SetStr("WORKPKG",  "ADH",                  "Workpackage that wrote the file");
    SetStr("TIMESYS",  "UTC",                  "Time system");
    SetStr("ADHREV",   GIT_REV_ADH,            "ADH GIT hash");
    SetStr("APISREV",  GIT_REV_ADH_APIS,       "ADH-APIS GIT hash");
    SetInt("MAJORV",   ADH_VERSION_MAJOR,      "Major ADH release");
    SetInt("MINORV",   ADH_VERSION_MINOR,      "Minor ADH release");

    const time_t t0 = time(NULL);
    const struct tm *tmp1 = gmtime(&t0);

    string str(19, '\0');
    if (tmp1 && strftime(const_cast<char*>(str.data()), 20, "%Y-%m-%dT%H:%M:%S", tmp1))
        SetStr("DATE", str, "File creation date");

    SetStr("DATEEND", "", "File closing date");
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
string FlatProtobufZOFits::
       ZFitsOutput::CommentFromType(char type)
{
    string comment;

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

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
uint32 FlatProtobufZOFits::
       ZFitsOutput::SizeFromType(char type)
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

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
vector<FlatProtobufZOFits::Key>::iterator FlatProtobufZOFits::
                                          ZFitsOutput::findkey(const string &key)
{
    for (auto it=keys.begin(); it!=keys.end(); it++)
        if (key==it->key)
            return it;

    return keys.end();
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
vector<FlatProtobufZOFits::Key>::iterator FlatProtobufZOFits::
                                          ZFitsOutput::findlongkey(const string &longkeyword)
{
    for (auto it=keys.begin(); it!=keys.end(); it++)
        if (longkeyword==it->longkeyword)
            return it;

    return keys.end();
}

///////////////////////////////////////////////////////////////////////////////
//  COLUMNS OPERATIONS
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::
     ZFitsOutput::initColumns(const Message*      message,
                              uint64              compression_block_size,
                              uint64              max_usable_mem,
                              int32               num_queues,
                              FlatProtobufZOFits* parent)
{
    //Only one given message type can be writen at a given time...
    if (descriptor != NULL)
        throw runtime_error("Looks like you are trying to initialize the "
                            "columns of the tables more than once... "
                            "This is NOT allowed.");

    //store the message descriptor.
    descriptor = message->GetDescriptor();

    SetStr("PBFHEAD", std::string{descriptor->full_name()}, "Written message name");
    SetDefaultKeys();

    total_num_columns = 0;
    //build the fits columns from the message. Start with an empty prefix
    buildFitsColumns(*message, parent);

    uint64 needed_block_size = 1.1*message->ByteSize()*caller._num_rows_per_tile;

    //add space for tile and block headers. block headers
    //is assumed to have <= 10 processings
    needed_block_size += sizeof(FITS::TileHeader)
                         + sizeof(FITS::BlockHeader)*table.num_cols
                         + 10*sizeof(uint16)*table.num_cols
                         + 8; //+8 for checksuming

    if (compression_block_size < needed_block_size)
    {
        ostringstream str;
        str << "ERROR: You didn't allocate large enough "
               "compression blocks. They must be > ";
        str << needed_block_size << " bytes, while they are only "
            << compression_block_size << " bytes.";
        throw runtime_error(str.str());
    }

    //check that enough memory is allocated to the compression,
    //compared to the requested number of compression threads
    int32 max_usable_threads = max_usable_mem/(3*compression_block_size);

    //if there is not enough memory for one thread to run, throw an exception
    if (max_usable_threads == 0)
    {
        ostringstream str;
        str << "Not enough memory was allocated for the compression ("
            << max_usable_mem/(1024*1024) << "MB vs "
            << (3*compression_block_size)/(1024*1024)
            << "MB requested per thread). ImpossibRe to continue" << endl;
        throw runtime_error(str.str());
    }

    //if not enough memory is available to allow for all requested
    //threads to run simultaneously, display a warning
    if (num_queues+1 > max_usable_threads)
    {
        ADH_warn << "WARNING: Not enough memory was allocated ("
                  << max_usable_mem/(1024*1024) << "MB), hence only "
                  << max_usable_threads << " compression threads will be used.";
        ADH_warn.flush();
    }

}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::
     ZFitsOutput::buildFitsColumns(const Message&      message,
                                   FlatProtobufZOFits* parent,
                                   const string&       name,
                                   const string&       id)
{
    //retrieve the message descriptor
    const Descriptor* desc = message.GetDescriptor();

    //In case of a AnyArray, call the dedicated function
    if (desc->name() == "AnyArray")
    {
        addAnyArrayColumn(message, name);
        //write the column indices to the header
        ostringstream str;
        str << "TPBID" << table.num_cols;
        SetStr(str.str(), id, "Protobuf ID");
        return;
    }
    //Append a . to the prefix, only if it is not null
    const string prefix_name = (name=="") ? "" : name+".";
    const string prefix_id   = (id  =="") ? "" : id  +".";

    //For all fields in this message, either instantiate the appropriate columns
    //or call this function recursively if it contains other messages.
    const Reflection* refl = message.GetReflection();

    for (int32 i=0;i<desc->field_count(); i++)
    {
        const FieldDescriptor* field = desc->field(i);
        //build the full name and ID of this field
        ostringstream full_id_str;
        full_id_str << prefix_id << field->number();
        const string full_id   = full_id_str.str();
        const string full_name = prefix_name + std::string{field->name()};

        //skip explicitely vetoed fields
        if (parent->isVetoed(full_name))
        {
            vetoField(full_name);
            continue;
        }

        //and also fields that were left empty
        if (field->is_repeated())
        {
            if (refl->FieldSize(message, field) == 0 && !parent->isAllowed(full_name))
            {
                vetoField(full_name);
                continue;
            }
        }
        else
        {
            if (!refl->HasField(message, field) && !parent->isAllowed(full_name))
            {
                vetoField(full_name);
                continue;
            }
        }

        vector<uint16> comp_seq = caller._default_comp;
        if (field->type() != FieldDescriptor::TYPE_MESSAGE)
        {
            if (caller._explicit_comp.find(full_name) != caller._explicit_comp.end())
            {
                comp_seq = caller._explicit_comp[full_name];
            }
        }

        //replace the '.' by '_'. We cannot do that earlier as the distinction
        //is needed between hierarchy (.) and indices (_)
        string column_name = full_name;
        for (auto it=column_name.begin(); it!=column_name.end(); it++)
            if ((*it) == '.' || (*it) == '#')
                *it = '_';

        int32 num_items = field->is_repeated() ? refl->FieldSize(message,field) : 1;
        bool skipped_field = false;
        switch (field->type())
        {
            case FieldDescriptor::TYPE_MESSAGE:
                if (field->is_repeated())
                {
                    num_expected_child.insert(make_pair(total_num_columns, num_items));
                }
                if (! field->is_repeated())
                    buildFitsColumns(refl->GetMessage(message, field),
                                     parent,
                                     full_name,
                                     full_id);
                else
                    for (int32 j=0;j<num_items;j++)
                    {
                        ostringstream str_j;
                        str_j << j;
                        buildFitsColumns(refl->GetRepeatedMessage(message, field, j),
                                         parent,
                                         full_name + "#" + str_j.str(),
                                         full_id+"."+str_j.str());
                    }
                continue;
            break;

            case FieldDescriptor::TYPE_DOUBLE:
                AddColumnDouble(comp_seq, num_items, column_name);
            break;

            case FieldDescriptor::TYPE_FLOAT:
                AddColumnFloat(comp_seq, num_items, column_name);
            break;

            case FieldDescriptor::TYPE_INT64:
            case FieldDescriptor::TYPE_SFIXED64:
            case FieldDescriptor::TYPE_SINT64:
                AddColumnLong(comp_seq, num_items, column_name);
            break;

            case FieldDescriptor::TYPE_UINT64:
            case FieldDescriptor::TYPE_FIXED64:
                AddColumnUnsignedLong(comp_seq, num_items, column_name);
            break;

            case FieldDescriptor::TYPE_INT32:
            case FieldDescriptor::TYPE_SFIXED32:
            case FieldDescriptor::TYPE_SINT32:
                AddColumnInt(comp_seq, num_items, column_name);
            break;

            case FieldDescriptor::TYPE_UINT32:
            case FieldDescriptor::TYPE_FIXED32:
                AddColumnUnsignedInt(comp_seq, num_items, column_name);
            break;

            case FieldDescriptor::TYPE_BOOL:
                AddColumnBool(comp_seq, num_items, column_name);
            break;

            case FieldDescriptor::TYPE_ENUM:
                AddColumnInt(comp_seq, num_items, column_name);
            break;

            case FieldDescriptor::TYPE_STRING:
            case FieldDescriptor::TYPE_BYTES:
                AddColumnChar(comp_seq, num_items, column_name);
            break;

            case FieldDescriptor::TYPE_GROUP:
                ADH_warn << "WARNING: skipping field " << full_name
                          << " because of unhandled type....";
                ADH_warn.flush();
                skipped_field = true;
            break;

            default:
                throw runtime_error("Unkown field type");
        }; //switch type()

        if (!skipped_field)
        {
            //write the column indices to the header
            ostringstream str;
            str << "TPBID" << table.num_cols;
            SetStr(str.str(), full_id, "Protobuf ID");

            total_num_columns++;
            columns_sizes.push_back(num_items);
        }
    }//for all fields
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
vector<FlatProtobufZOFits::Table::Column>::const_iterator FlatProtobufZOFits::
                                                          ZFitsOutput::findcol(const string &name)
{
    for (auto it=table.cols.cbegin(); it!=table.cols.cend(); it++)
        if (name==it->name)
            return it;

    return table.cols.cend();
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumn(uint32        cnt,
                            char          typechar,
                            const string& name,
                            const string& unit,
                            const string& comment,
                            bool          addHeaderKeys)
{
    if (findcol(name)!= table.cols.cend())
    {
        ostringstream sout;
        sout << "A column with the name '" << name << "' already exists.";
        throw runtime_error(sout.str());
    }

    typechar = toupper(typechar);

    switch (typechar)
    {
        case 'S':
            SetFloat("TZERO"+to_string((long long int)(table.num_cols+1)),
                   -128,
                   "Offset for signed chars");
            typechar = 'B';
        break;

        case 'U':
            SetFloat("TZERO"+to_string((long long int)(table.num_cols+1)),
                   32768,
                   "Offset for uint16");
            typechar = 'I';
            break;
        case 'V':
            SetFloat("TZERO"+to_string((long long int)(table.num_cols+1)),
                   2147483648,
                   "Offset for uint32");
            typechar = 'J';
        break;
        case 'W':
            typechar = 'K';
        break;
        default:
            ;
    }

    static const string allow("LABIJKEDQ");

    if (find(allow.cbegin(), allow.cend(), typechar)==allow.end())
    {
        ostringstream sout;
        sout << "Column type '" << typechar << "' not supported.";
        throw runtime_error(sout.str());
    }


    ostringstream type;
    type << cnt;
    if (typechar=='Q')
        type << "QB";
    else
        type << typechar;

    table.num_cols++;

    if (table.num_cols >= 1000)
    {
        ostringstream str;
        str << "Error, you've just created more than 1000 columns, "
               "while the FITS standard limits this to 999. "
               "Current columns are:\n";
        for (auto it=table.cols.begin(); it!= table.cols.end(); it++)
            str << it->name << "\n";

        throw runtime_error(str.str());
    }

    if (addHeaderKeys)
    {

        const string nc = to_string(table.num_cols);
        SetStr("TFORM"+nc,
               type.str(),
               "format of "+name+" "+CommentFromType(typechar));
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
    col.offset = table.bytes_per_row;

    table.cols.push_back(col);

    table.bytes_per_row += size*cnt;

    return true;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumn(const FITS::Compression& comp,
                            uint32                   cnt,
                            char                     typechar,
                            const string&            name,
                            const string&            unit,
                            const string&            comment,
                            bool                     addHeaderKeys)
{
    if (!AddColumn(1, 'Q', name, unit, comment, addHeaderKeys))
        return false;

    const size_t size = SizeFromType(typechar);

    Table::Column col;
    col.name   = name;
    col.type   = typechar;
    col.num    = cnt;
    col.size   = size;
    col.offset = real_row_width;

    real_row_width += size*cnt;

    real_columns.emplace_back(col, comp);

    switch (typechar)
    {
        case 'S':
            SetFloat("TZERO"+to_string((long long int)(real_columns.size())),
                   -128.,
                   "Offset for signed chars");
            typechar = 'B';
            break;

        case 'U':
            SetFloat("TZERO"+to_string((long long int)(real_columns.size())),
                   32768.,
                   "Offset for uint16");
            typechar = 'I';
            break;
        case 'V':
            SetFloat("TZERO"+to_string((long long int)(real_columns.size())),
                   2147483648.,
                   "Offset for uint32");
            typechar = 'J';
            break;
        case 'W':
            SetFloat("TZERO"+to_string((long long int)(real_columns.size())),
                   9223372036854775808.,
                   "Offset for uint64");
            typechar = 'K';
            break;
        default:
            ;
    }

    SetStr("ZFORM"+to_string((long long int)(real_columns.size())),
           to_string((long long int)(cnt))+typechar,
           "format of "+name+" "+CommentFromType(typechar));
    SetStr("ZCTYP"+to_string((long long int)(real_columns.size())),
           "CTA",
           "Custom CTA compression");

    return true;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumnByte(const FITS::Compression& comp,
                                uint32                   cnt,
                                const string&            name,
                                const string&            unit,
                                const string&            comment)
{
    return AddColumn(comp, cnt, 'B', name, unit, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumnChar(const FITS::Compression& comp,
                                uint32                   cnt,
                                const string&            name,
                                const string&            unit,
                                const string&            comment)
{
    return AddColumn(comp, cnt, 'A', name, unit, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumnShort(const FITS::Compression& comp,
                                 uint32                   cnt,
                                 const string&            name,
                                 const string&            unit,
                                 const string&            comment)
{
    return AddColumn(comp, cnt, 'I', name, unit, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumnInt(const FITS::Compression& comp,
                               uint32                   cnt,
                               const string&            name,
                               const string&            unit,
                               const string&            comment)
{
    return AddColumn(comp, cnt, 'J', name, unit, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumnLong(const FITS::Compression& comp,
                                uint32                   cnt,
                                const string&            name,
                                const string&            unit,
                                const string&            comment)
{
    return AddColumn(comp, cnt, 'K', name, unit, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumnFloat(const FITS::Compression& comp,
                                 uint32                   cnt,
                                 const string&            name,
                                 const string&            unit,
                                 const string&            comment)
{
    return AddColumn(comp, cnt, 'E', name, unit, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumnDouble(const FITS::Compression& comp,
                                  uint32                   cnt,
                                  const string&            name,
                                  const string&            unit,
                                  const string&            comment)
{
    return AddColumn(comp, cnt, 'D', name, unit, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumnBool(const FITS::Compression& comp,
                                uint32                   cnt,
                                const string&            name,
                                const string&            unit,
                                const string&            comment)
{
    return AddColumn(comp, cnt, 'L', name, unit, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumnSignedByte(const FITS::Compression& comp,
                                      uint32                   cnt,
                                      const string&            name,
                                      const string&            unit,
                                      const string&            comment)
{
    return AddColumn(comp, cnt, 'S', name, unit, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumnUnsignedShort(const FITS::Compression& comp,
                                         uint32                   cnt,
                                         const string&            name,
                                         const string&            unit,
                                         const string&            comment)
{
    return AddColumn(comp, cnt, 'U', name, unit, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumnUnsignedInt(const FITS::Compression& comp,
                                       uint32                   cnt,
                                       const string&            name,
                                       const string&            unit,
                                       const string&            comment)
{
    return AddColumn(comp, cnt, 'V', name, unit, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddColumnUnsignedLong(const FITS::Compression& comp,
                                        uint32                   cnt,
                                        const string&            name,
                                        const string&            unit,
                                        const string&            comment)
{
    return AddColumn(comp, cnt, 'W', name, unit, comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::
     ZFitsOutput::addAnyArrayColumn(const Message& message,
                                    const string&  name)
{
    //no veto check is necessary here because either the veto was done earlier, or this is the top message, surely not to be vetoed.

    const AnyArray& array = static_cast<const AnyArray&>(message);

    vector<uint16_t> comp_seq = caller._default_comp;

    if (caller._explicit_comp.find(name) != caller._explicit_comp.end())
        comp_seq = caller._explicit_comp[name];


    //figure out the size of the column
    int32 column_width = array.data().size();

    total_num_columns++;
    //cout << "ADDING COLUMN WIDTH OF " << column_width << endl;
    columns_sizes.push_back(0); //column_width);

    //replace the '.' by '_'. We cannot do that earlier as the distinction is needed between hierarchy (.) and indices (_)
    string column_name = name;
    for (auto it=column_name.begin(); it!=column_name.end(); it++)
        if ((*it) == '.' || (*it) == '#')
            *it = '_';

    //figure out the type of column to be initialized
    switch (array.type())
    {
        case AnyArray::NONE:
            AddColumnByte(comp_seq, column_width, column_name);
            break;
        case AnyArray::S8:
            AddColumnChar(comp_seq, column_width, column_name);
            break;
        case AnyArray::S16:
            AddColumnShort(comp_seq, column_width/2, column_name);
            break;
        case AnyArray::S32:
            AddColumnInt(comp_seq, column_width/4, column_name);
            break;
        case AnyArray::S64:
            AddColumnLong(comp_seq, column_width/8, column_name);
            break;
        case AnyArray::FLOAT:
            AddColumnFloat(comp_seq, column_width/4, column_name);
            break;
        case AnyArray::DOUBLE:
            AddColumnDouble(comp_seq, column_width/8, column_name);
            break;
        case AnyArray::BOOL:
            AddColumnBool(comp_seq, column_width, column_name);
            break;
        case AnyArray::U8:
            AddColumnSignedByte(comp_seq, column_width, column_name);
            break;
        case AnyArray::U16:
            AddColumnUnsignedShort(comp_seq, column_width/2, column_name);
            break;
        case AnyArray::U32:
            AddColumnUnsignedInt(comp_seq, column_width/4, column_name);
            break;
        case AnyArray::U64:
            AddColumnUnsignedLong(comp_seq, column_width/8, column_name);
            break;

        default:
            throw runtime_error("Unhandled type for cta array...");
            break;
    };
}

///////////////////////////////////////////////////////////////////////////////
//  HEADER/FOOTER/CATALOG FORMATING OPERATIONS
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::WriteTableHeader()
{
    //WE NEED TO USE THESE GLOBAL VARIABLES BECAUSE THE WRITING IS DONE ASYNCHRONOUSLY
    //ALL IS NEEDED IS THAT WRITETABLEHEADER IS ALWAYS CALLED RIGHT AFTER MOVETONEWTABLE
    table_start     = caller.global_table_start[file_index];
    file_descriptor = caller.global_file_descriptor[file_index];
    output_file     = caller.global_output_file[file_index];

    SetInt("ZNAXIS1", real_row_width);

    if ((size_t)(output_file->tellp())>table_start)
    {
        throw runtime_error("Table not empty anymore.");
    }

    //write basic fits header only in the case of a new file
    if (table_start == 0)
        headersum = WriteFitsHeader();

    SetStr("EXTNAME", table_name);
    SetInt("NAXIS1",  table.bytes_per_row);
    SetInt("TFIELDS", table.cols.size());

    End();

    WriteHeader();

    WriteCatalog();

    return output_file->good();
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
Checksum FlatProtobufZOFits::
         ZFitsOutput::WriteFitsHeader()
{
    ZFitsOutput h(file_index, caller);

    h.SetBool("SIMPLE", true, "file does conform to FITS standard");
    h.SetInt ("BITPIX",    8, "number of bits per data pixel");
    h.SetInt ("NAXIS",     0, "number of data axes");
    h.SetBool("EXTEND", true, "FITS dataset may contain extensions");
    h.SetStr ("CHECKSUM","0000000000000000", "Checksum for the whole HDU");
    h.SetStr ("DATASUM", "         0", "Checksum for the data block");
    h.AddComment("FITS (Flexible Image Transport System) format is defined in 'Astronomy");
    h.AddComment("and Astrophysics', volume 376, page 359; bibcode: 2001A&A...376..359H");
    h.End();

    const Checksum sum = h.WriteHeader(*output_file);

    h.SetStr("CHECKSUM", sum.str());

    const size_t offset = output_file->tellp();
    h.WriteHeader(*output_file);
    output_file->seekp(offset);

    return sum;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::WriteCatalog()
{
    const uint32 one_catalog_row_size = table.num_cols*2*sizeof(uint64);
    const uint32 total_catalog_size   = caller._num_tiles*one_catalog_row_size;

    // swap the catalog bytes before writing
    vector<char> swapped_catalog(total_catalog_size);

    const lock_guard<mutex> lock(_catalog_fence);

    uint32 shift = 0;
    for (auto it=catalog.cbegin(); it!=catalog.cend(); it++)
    {
        char*       dest = swapped_catalog.data() + shift;
        char*        src = (char*)(it->data());
        uint32       num = table.num_cols*2;
        const char *pend = src + num*sizeof(uint64);

        for (const char *ptr = src; ptr<pend; ptr+=sizeof(uint64), dest+=sizeof(uint64))
            reverse_copy(ptr, ptr+sizeof(uint64), dest);

        shift += one_catalog_row_size;
    }

    if (catalog_size < caller._num_tiles)
        memset(swapped_catalog.data()+shift, 0, total_catalog_size-shift);

    // first time writing ? remember where we are
    if (catalog_offset == 0)
        catalog_offset = output_file->tellp();

    // remember where we came from
    const off_t where_are_we = output_file->tellp();

    // write to disk
    output_file->seekp(catalog_offset);
    output_file->write(swapped_catalog.data(), total_catalog_size);

    if (where_are_we != catalog_offset)
        output_file->seekp(where_are_we);

    // udpate checksum
    catalogsum.reset();
    catalogsum.add(swapped_catalog.data(), total_catalog_size);

    return output_file->good();
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
Checksum FlatProtobufZOFits::
         ZFitsOutput::WriteHeader()
{
    return WriteHeader(*output_file);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
Checksum FlatProtobufZOFits::
         ZFitsOutput::WriteHeader(ofstream &fout)
{
    Checksum sum;
    for (auto it=keys.begin(); it!=keys.end(); it++)
    {
        it->Out(fout);
        sum += it->checksum;
    }
    fout.flush();

    return sum;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::
     ZFitsOutput::AlignTo2880Bytes()
{
    if (output_file->tellp()%(80*36)>0)
    {
        vector<char> filler(80*36-output_file->tellp()%(80*36));
        output_file->write(filler.data(), filler.size());
    }
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
Checksum FlatProtobufZOFits::
         ZFitsOutput::UpdateHeaderChecksum()
{
    ostringstream datasum_str;
    datasum_str << datasum.val();
    SetStr("DATASUM", datasum_str.str());

    const Checksum sum = WriteHeader();

    //sum += headersum;

    SetStr("CHECKSUM", (sum+datasum).str());

    return WriteHeader();
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     ZFitsOutput::AddComment(const string &comment)
{
    return Set("COMMENT", false, "", comment);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::
     ZFitsOutput::updateHeaderKeys(bool finalUpdate)
{
    vector<Key>::iterator hdate_end = findlongkey("CTA ACTIVITY END");
    if (hdate_end != keys.end() && hdate_end->value == "''")
    {
        const time_t t0 = time(NULL);
        const struct tm *tmp1 = gmtime(&t0);
        string str(19, '\0');
        if (tmp1 && strftime(const_cast<char*>(str.data()), 20, "%Y-%m-%dT%H:%M:%S", tmp1))
            SetHierarchStr(str, "","CTA ACTIVITY END");
    }

    uint64 row_width = 0;
    for (uint32 i=0;i<columns_sizes.size();i++)
    {
        ostringstream entry_name;
        entry_name << "ZFORM" << i+1;

        //get the column type
        char type = real_columns[i].col.type;
        switch (type)
        {
            case 'U':
                type = 'I';
                break;
            case 'V':
                type = 'J';
                break;
            case 'W':
                type = 'K';
                break;
            case 'S':
                type = 'B';
                break;
            default:
                break;
        };

        switch (type)
        {
            case 'I':
                row_width += sizeof(int16)*columns_sizes[i];
                break;
            case 'J':
            case 'E':
                row_width += sizeof(int32)*columns_sizes[i];
                break;

            case 'K':
            case 'D':
                row_width += sizeof(int64)*columns_sizes[i];
                break;

            case 'B':
            case 'L':
            case 'A':
                row_width += columns_sizes[i];
                break;
            default:
                throw runtime_error("Unexpected column type...");
                break;
        };

        //set proper size
        ostringstream correct_type;
        correct_type << columns_sizes[i] << type;
        SetStr(entry_name.str(), correct_type.str());
    }

    SetInt("ZNAXIS1", row_width);

    real_row_width = row_width;

    int64 heap_size         = 0;
    int64 compressed_offset = 0;
    uint64 current_tile     = 0;

    _catalog_fence.lock();

    for (auto it=catalog.begin(); it!=catalog.end(); it++)
    {
        compressed_offset += sizeof(FITS::TileHeader);
        heap_size         += sizeof(FITS::TileHeader);
        for (uint32 j=0; j<it->size(); j++)
        {
            heap_size += (*it)[j].first;

            if ((*it)[j].first < 0)
                throw runtime_error("Negative block size");

            (*it)[j].second = compressed_offset;
            compressed_offset += (*it)[j].first;

            if ((*it)[j].first == 0)
                (*it)[j].second = 0;
        }

        //only deal with the tiles that were written to disk already
        current_tile ++;
        if (current_tile >= num_tiles_written) break;
    }

    _catalog_fence.unlock();

    if (finalUpdate)
    {
        ShrinkCatalog();
        SetInt("ZNAXIS2", table.num_rows);
        SetInt("ZHEAPPTR", caller._num_tiles*table.num_cols*sizeof(uint64)*2);
    }
    else
    {
        SetInt("ZNAXIS2",  num_tiles_written*caller._num_rows_per_tile);
        SetInt("ZHEAPPTR", caller._num_tiles*table.num_cols*sizeof(uint64)*2);
   }

    const uint32 total_num_tiles_written = (table.num_rows + caller._num_rows_per_tile-1)/caller._num_rows_per_tile;
    const uint32 total_catalog_width = 2*sizeof(int64)*table.num_cols;

    if (finalUpdate)
    {
        SetInt("THEAP",  total_num_tiles_written*total_catalog_width);
        SetInt("NAXIS1", total_catalog_width);
        SetInt("NAXIS2", total_num_tiles_written);
        if (heap_size != 0)
        {
            const float compression_ratio = (float)(raw_heap_size)/(float)heap_size;
            SetFloat("ZRATIO", compression_ratio);
        }
    }
    else
    {
        SetInt("THEAP", num_tiles_written*total_catalog_width);
        SetInt("NAXIS1", total_catalog_width);
        SetInt("NAXIS2", num_tiles_written);
    }

    //add to the heap size the size of the gap between the catalog and the actual heap
    if (num_tiles_written < catalog_size)
        heap_size += (catalog_size - num_tiles_written)*table.num_cols*sizeof(uint64)*2;

    SetInt("PCOUNT", heap_size, "size of special data area");

}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::
     ZFitsOutput::End()
{
    Set("END");
    while (keys.size()%36!=0)
        keys.emplace_back();
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
uint32 FlatProtobufZOFits::
       ZFitsOutput::ShrinkCatalog()
{
    //add empty row to get either the target number of rows, or a multiple of the allowed size
    for (uint32 i=0;i<catalog_size%caller._num_tiles;i++)
        AddOneCatalogRow();

    const lock_guard<mutex> lock(_catalog_fence);

    //did we write more rows than what the catalog could host ?
    if (catalog_size <= caller._num_tiles) // nothing to do
        return 1;

    //always exact as extra rows were added just above
    const uint32 shrink_factor = catalog_size / caller._num_tiles;

    ADH_warn << "\33[33mWARNING: you wrote more data than header "
                 "allows for it: FTOOLS won't work on this file.\33[0m";
    ADH_warn.flush();

    //shrink the catalog !
    uint32 entry_id = 1;
    auto it = catalog.begin();
    it++;
    for (; it != catalog.end(); it++)
    {
        if (entry_id >= caller._num_tiles)
            break;

        const uint32 target_id = entry_id*shrink_factor;

        auto jt = it;
        for (uint32 i=0; i<target_id-entry_id; i++)
            jt++;

        *it = *jt;

        entry_id++;
    }

    const uint32 num_tiles_to_remove = catalog_size - caller._num_tiles;

    //remove the too many entries
    for (uint32 i=0;i<num_tiles_to_remove;i++)
    {
        catalog.pop_back();
        catalog_size--;
    }

    //update header keywords
    uint32 num_rows_per_tile = caller._num_rows_per_tile;
    num_rows_per_tile *= shrink_factor;

    SetInt("ZTILELEN", num_rows_per_tile);
    SetInt("ZSHRINK",  shrink_factor);

    return shrink_factor;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
FlatProtobufZOFits::CatalogRow& FlatProtobufZOFits::
                                ZFitsOutput::AddOneCatalogRow()
{
    const lock_guard<mutex> lock(_catalog_fence);

    // add one row to the catalog
    catalog.emplace_back(CatalogRow());
    catalog.back().resize(table.num_cols);
    for (auto it=catalog.back().begin(); it != catalog.back().end(); it++)
        *it = CatalogEntry(0,0);

    catalog_size++;

    return catalog.back();
}

///////////////////////////////////////////////////////////////////////////////
//  THREADS INPUTS
///////////////////////////////////////////////////////////////////////////////
FlatProtobufZOFits::
TableOperation::TableOperation() : move_to_new_table(false),
                                   open_file(false),
                                   close_file(false),
                                   display_stats(false),
                                   write_table_header(false)
{
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     TableOperation::IsSet() const
{
    return (open_file || move_to_new_table || write_table_header);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
FlatProtobufZOFits::
CompressionTarget::CompressionTarget(CatalogRow&  row,
                                     ZFitsOutput* this_output,
                                     uint64       f_index) : catalog(row),
                                                             targetId(0),
                                                             output(this_output),
                                                             file_index(f_index)
{
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
FlatProtobufZOFits::
WriteToDiskTarget::WriteToDiskTarget(ZFitsOutput* this_output) : targetId(0),
                                                                 num_bytes_in_buffer(0),
                                                                 num_bytes_originally(0),
                                                                 buffers(0),
                                                                 output(this_output),
                                                                 file_index(0)
{
}
///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
bool FlatProtobufZOFits::
     WriteToDiskTarget::operator < (const WriteToDiskTarget& other) const
{
    return targetId < other.targetId;
}

///////////////////////////////////////////////////////////////////////////////
//  CLASS METHODS
///////////////////////////////////////////////////////////////////////////////
Message* FlatProtobufZOFits::getRecycledMessage()
{

    if (_current_table == NULL)
        return NULL;

    const lock_guard<mutex> lock(_recycle_fence);

    const Descriptor* descriptor = _current_table->descriptor;

    if (_recycled_messages[descriptor].empty())
        return NULL;

    Message* to_return = _recycled_messages[descriptor].front();
    _recycled_messages[descriptor].pop_front();

    return to_return;
}


///////////////////////////////////////////////////////////////////////////////
//  HEADER KEYS OPERATIONS
///////////////////////////////////////////////////////////////////////////////
  string removePounds(const string& name)
  {
      string name_no_index = name;
    //remove any index inserted into the name
    //FIXME this collides with _ inserted in fields names
    while (name_no_index.find('#') !=  string::npos)
    {
        //get the first underscore
        size_t underscore_index = name_no_index.find_first_of('#');
        ostringstream str;
        size_t end_index = name_no_index.find_first_of('.', underscore_index);

        //concatenate up to the first underscore
        str << name_no_index.substr(0, underscore_index);

        //add the trailing chars, if any
        if (end_index != string::npos) str << name_no_index.substr(end_index);

        name_no_index = str.str();
    }
        return name_no_index;
  }

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
 bool FlatProtobufZOFits::isVetoed(const string& name)
 {
    return (_vetoed_fields.find(removePounds(name)) != _vetoed_fields.end());
 }

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
 bool FlatProtobufZOFits::ZFitsOutput::isVetoed(const string& name)
 {
    return (_missing_fields.find(removePounds(name)) != _missing_fields.end());
 }

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
 bool FlatProtobufZOFits::isAllowed(const string& name)
 {
    return (_allowed_fields.find(name) != _allowed_fields.end());
 }

///////////////////////////////////////////////////////////////////////////////
//  WRITE TO DISK OPERATIONS
///////////////////////////////////////////////////////////////////////////////
 bool FlatProtobufZOFits::writeToDisk(const WriteToDiskTarget& target)
 {
    //if the current target is not the next line in queue,
    //wait for the next one to show up
    if (target.targetId != (_next_buffer_to_write[target.file_index]+1))
        return false;

    _next_buffer_to_write[target.file_index]++;

    //If table operation, just forward it to the write to disk thread
    if (target.table_operation.IsSet())
    {
        if (target.table_operation.open_file)
        {
            target.output->open();
            return true;
        }

        if (target.table_operation.close_file)
        {
            target.output->close(target.table_operation.display_stats);
            delete target.output;
            return true;
        }

        if (target.table_operation.move_to_new_table)
        {
            target.output->moveToNewTable();
            delete target.output;
            return true;
        }

        if (target.table_operation.write_table_header)
        {
            target.output->WriteTableHeader();
            return true;
        }
    }

    //simply crawl through the list of buffers and write their data
    auto it = target.buffers.begin();
    auto jt = target.num_bytes_in_buffer.begin();
    auto kt = target.num_bytes_originally.begin();
    for ( ; it!= target.buffers.end(); it++, jt++, kt++)
    {
        FlatProtobufZOFits::_size_written_to_disk+=*jt;
        FlatProtobufZOFits::_size_uncompressed_to_disk+=*kt;

        writeCompressedDataToDisk(it->get(), *jt, target.output);
    }
    target.output->num_tiles_written++;

    return true;
 }


///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
 bool FlatProtobufZOFits::writeCompressedDataToDisk(char*        src,
                                                    const uint32 sizeToWrite,
                                                    ZFitsOutput* output)
 {
    char* checkSumPointer = src+4;
    int32 extraBytes = 0;
    uint32 sizeToChecksum = sizeToWrite;

    //should we extend the array to the left ?
    if (output->checksum_offset != 0)
    {
        sizeToChecksum  += output->checksum_offset;
        checkSumPointer -= output->checksum_offset;
        memset(checkSumPointer, 0, output->checksum_offset);
    }

    //should we extend the array to the right ?
    if (sizeToChecksum%4 != 0)
    {
        extraBytes = 4 - (sizeToChecksum%4);
        memset(checkSumPointer+sizeToChecksum, 0, extraBytes);
        sizeToChecksum += extraBytes;
    }

    //do the checksum
    output->datasum.add(checkSumPointer, sizeToChecksum);

    output->checksum_offset = (4 - extraBytes)%4;

    //write data to disk
    output->output_file->write(src+4, sizeToWrite);

    return output->output_file->good();
 }

///////////////////////////////////////////////////////////////////////////////
//  COMPRESSION OPERATIONS
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::launchNewCompression()
{
    CompressionTarget comp_target(_current_table->AddOneCatalogRow(),
                                  _current_table,
                                  _current_file_index);

    //assign input messages to compression target
    comp_target.messages   = _incoming_data;
    comp_target.targetId   = ++(_comp_target_counter[_current_file_index]);

    //and replace incoming data slot by a new vector
    _incoming_data = shared_ptr<vector<const Message*>>(new vector<const Message*>);

    // Instead of the mess above, just use 2 buffers: one to serialize, one to compress...
    uint32 total_num_buffers = 2;

    if (total_num_buffers*_memory_pool.getChunkSize() > _memory_pool.getMaxMemory())
    {
        ostringstream str;
        str << yellow << "ERROR: Protobufzofits was not allocated enough "
                         "memory to compress data to disk. Either increase "
                         "the allocated compression memory in the constructor, "
                         "or reduce the number of events per tile, also in "
                         "the constructor. The current max. available memory "
                         "for compression is currently set to ";
        str << _memory_pool.getMaxMemory();
        str << " bytes while we would need at least ";
        str << total_num_buffers*_memory_pool.getChunkSize();
        str << " bytes.";
        str << no_color;
        throw runtime_error(str.str());
    }

    for (uint32 i=0;i<total_num_buffers;i++)
        comp_target.buffers.push_back(_memory_pool.malloc());

    //assign the compression job to the least used compression queue.
    const auto imin = min_element(_compression_queues.begin(), _compression_queues.end());

    imin->emplace(comp_target);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
 bool FlatProtobufZOFits::compressMessages(const CompressionTarget& comp_target)
 {

    //bind only accept const arguments.
    //we need non-const for recursion -> make a copy !
    CompressionTarget nc_comp_target = comp_target;

    WriteToDiskTarget disk_target(nc_comp_target.output);
    disk_target.targetId   = nc_comp_target.targetId;
    disk_target.file_index = nc_comp_target.file_index;

    //If table operation, just forward it to the write to disk thread
    if (comp_target.table_operation.IsSet())
    {
        disk_target.table_operation = comp_target.table_operation;
        _write_to_disk_queue[disk_target.file_index].emplace(disk_target);
        return true;
    }

    //get a buffer where the serial, gathered messages data can be put
    if (nc_comp_target.buffers.empty())
        throw runtime_error("ERROR: no buffer available for serialization");
    shared_ptr<char> gather = nc_comp_target.buffers.front();
    nc_comp_target.buffers.pop_front();

    //get a first target buffer, where to write the compressed data
    if (nc_comp_target.buffers.empty())
        throw runtime_error("ERROR: no buffer available for compression");
    shared_ptr<char> comp_buf = nc_comp_target.buffers.front();
    nc_comp_target.buffers.pop_front();

    //reserve space for tile header. +4 bytes are left to allow for checksum calculation
    FITS::TileHeader* tile_head = reinterpret_cast<FITS::TileHeader*>(comp_buf.get()+4);

    //launch the recursive crawl of the message's structure
    int32 bytes_written = sizeof(FITS::TileHeader);
    int32 bytes_read    = 0;
    int32 column_indices = 0;

    //the input list of messages is not const so that messages can be recycled.
    //make this incoming parameter const
    vector<const Message*> const_messages;
    for (auto it=comp_target.messages->begin(); it!=comp_target.messages->end(); it++)
        const_messages.push_back(*it);


    compressMessageFields(const_messages,
                          column_indices,
                          gather.get(),
                          comp_buf,
                          bytes_written,
                          bytes_read,
                          nc_comp_target,
                          disk_target);

//    bytes_written = 0;//35606756;

    //add the last buffer to the disk target
    disk_target.buffers.push_back(comp_buf);
    disk_target.num_bytes_in_buffer.push_back(bytes_written);
    disk_target.num_bytes_originally.push_back(bytes_read);

    //count the total number of compressed bytes
    uint32 total_compressed_bytes = 0;
    for (auto it=disk_target.num_bytes_in_buffer.begin(); it!=disk_target.num_bytes_in_buffer.end(); it++)
         total_compressed_bytes += *it;

    //set the tile header properly
    tile_head->id[0] = 'T';
    tile_head->id[1] = 'I';
    tile_head->id[2] = 'L';
    tile_head->id[3] = 'E';
    tile_head->numRows = nc_comp_target.messages->size();
    tile_head->size = total_compressed_bytes - sizeof(FITS::TileHeader);

    //put the buffers to write to disk in the writing queue
    _write_to_disk_queue[disk_target.file_index].emplace(disk_target);

    //recycle the messages that were given as an input. We can const-cast them as protobufZOFits can indeed change them
    const lock_guard<mutex> lock(_recycle_fence);
    list<Message*>& this_recycle_bin = _recycled_messages[nc_comp_target.output->descriptor];
    for (auto it=comp_target.messages->begin(); it!=comp_target.messages->end(); it++)
        this_recycle_bin.push_back(const_cast<Message*>(*it));

    return true;

 }

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::compressMessageFields(const vector<const Message*>& messages,
                                                     int32&                  col_index,
                                                     char*                   gather_buf,
                                                     shared_ptr<char>&       compres_buff,
                                                     int32&                  comp_bytes_written,
                                                     int32&                  comp_bytes_read,
                                                     CompressionTarget&      comp_target,
                                                     WriteToDiskTarget&      disk_target,
                                               const string&                 name)
{
    //FIXME remove this check
    if (messages.size() == 0)
        throw runtime_error("No message found for compression");

    ZFitsOutput* this_output = comp_target.output;

    //retrieve the message metadata
    const Descriptor* desc   = messages[0]->GetDescriptor();

    //Append a . to the prefix, only if it is not null
    const string prefix_name = (name=="") ? "" : name+".";

    //For all fields in this message, either gather the values
    //or call this function recursively if it contains other messages.
    for (int32 i=0;i<desc->field_count(); i++)
    {
        //build the full name and ID of this field
        const string full_name = prefix_name + std::string{desc->field(i)->name()};
        if (this_output->isVetoed(full_name))
            continue;

        int32 bytes_gathered = 0;
        switch (desc->field(i)->type())
        {
            case FieldDescriptor::TYPE_DOUBLE:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += this_output->serialize<double>(gather_buf+bytes_gathered,
                                                        messages[j],
                                                        desc->field(i),
                                                        messages[j]->GetReflection(),
                                                        col_index);
                break;

            case FieldDescriptor::TYPE_FLOAT:
                for (uint32 j=0;j<messages.size();j++)
                     bytes_gathered += this_output->serialize<float>(gather_buf+bytes_gathered,
                                                        messages[j],
                                                        desc->field(i),
                                                        messages[j]->GetReflection(),
                                                        col_index);
                break;

            case FieldDescriptor::TYPE_INT64:
            case FieldDescriptor::TYPE_SFIXED64:
            case FieldDescriptor::TYPE_SINT64:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += this_output->serialize<int64>(gather_buf+bytes_gathered,
                                                       messages[j],
                                                       desc->field(i),
                                                       messages[j]->GetReflection(),
                                                       col_index);
                break;

            case FieldDescriptor::TYPE_FIXED64:
            case FieldDescriptor::TYPE_UINT64:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += this_output->serialize<uint64>(gather_buf+bytes_gathered,
                                                        messages[j],
                                                        desc->field(i),
                                                        messages[j]->GetReflection(),
                                                        col_index);
               break;

            case FieldDescriptor::TYPE_INT32:
            case FieldDescriptor::TYPE_SFIXED32:
            case FieldDescriptor::TYPE_SINT32:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += this_output->serialize<int32>(gather_buf+bytes_gathered,
                                                       messages[j],
                                                       desc->field(i),
                                                       messages[j]->GetReflection(),
                                                       col_index);
                break;

            case FieldDescriptor::TYPE_FIXED32:
            case FieldDescriptor::TYPE_UINT32:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += this_output->serialize<uint32>(gather_buf+bytes_gathered,
                                                        messages[j],
                                                        desc->field(i),
                                                        messages[j]->GetReflection(),
                                                        col_index);
                break;

            case FieldDescriptor::TYPE_BOOL:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += this_output->serialize<bool>(gather_buf+bytes_gathered,
                                                      messages[j],
                                                      desc->field(i),
                                                      messages[j]->GetReflection(),
                                                      col_index);
                break;
            case FieldDescriptor::TYPE_ENUM:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += this_output->serialize<EnumValueDescriptor>(gather_buf+bytes_gathered,
                                                                     messages[j],
                                                                     desc->field(i),
                                                                     messages[j]->GetReflection(),
                                                                     col_index);
                break;

            case FieldDescriptor::TYPE_STRING:
            case FieldDescriptor::TYPE_BYTES:
                for (uint32 j=0;j<messages.size();j++)
                    bytes_gathered += this_output->serialize<char>(gather_buf+bytes_gathered,
                                                      messages[j],
                                                      desc->field(i),
                                                      messages[j]->GetReflection(),
                                                      col_index);
                break;
            case FieldDescriptor::TYPE_GROUP:
                continue;
            break;

            case FieldDescriptor::TYPE_MESSAGE:
            {
                //for messages, we must recursively call this function.
                //If messages are repeated, empty slots are filled-in by the default value
                if (desc->field(i)->is_repeated())
                {
                    //look up the expected max. number of messages
                    if (this_output->num_expected_child.find(col_index) ==
                        this_output->num_expected_child.end())
                    {
                        ostringstream str;
                        str << "Mapping to number of expected children "
                               "nowhere to be found for column "
                            << col_index << " num entries: "
                            << this_output->num_expected_child.size();
                        throw runtime_error(str.str());
                    }

                    int32 num_children = this_output->num_expected_child[col_index];

                    //for all the expected children
                    for (int32 k=0;k<num_children;k++)
                    {
                        vector<const Message*> child_messages;
                        //for all the input messages
                        for (uint32 j=0;j<messages.size();j++)
                        {
                            //TODO find a more effective check
                            //check that no input message exceeds the max. number of expected children
                            if (messages[j]->GetReflection()->FieldSize(messages[j][0], desc->field(i)) > num_children)
                                    throw runtime_error("The number of repeated messages from the "
                                                        "initialization message is less than for "
                                                        "the subsequent messages");

                            if (messages[j]->GetReflection()->FieldSize(messages[j][0], desc->field(i)) > k)
                            {//stack up this message
                                child_messages.push_back(&(messages[j]->GetReflection()->GetRepeatedMessage(*(messages[j]), desc->field(i), k)));
                            }
                            else
                            {//no message available at this index. Add the default message.
                            //FIXME I am not sure at all that "message_type" does what I think it should do...
                                child_messages.push_back(MessageFactory::generated_factory()->GetPrototype(desc->field(i)->message_type()));
                            }
                        }

                        if (desc->field(i)->message_type()->name() == "AnyArray")
                        {//in case of cta array, do the serialization right away
                            for (uint32 j=0;j<child_messages.size();j++)
                                bytes_gathered += this_output->serialize<AnyArray>(gather_buf+bytes_gathered,
                                                                      child_messages[j],
                                                                      desc->field(i),
                                                                      child_messages[j]->GetReflection(),
                                                                      col_index);
                            compressBuffer(gather_buf,
                                           compres_buff,
                                           bytes_gathered,
                                           comp_bytes_written,
                                           col_index,
                                           comp_target);
                            comp_bytes_read += bytes_gathered;
                        }
                        else
                        {//otherwise, call the function with these message
                            ostringstream str;
                            str << full_name << "#" << k;
                            compressMessageFields(child_messages,
                                                  col_index,
                                                  gather_buf,
                                                  compres_buff,
                                                  comp_bytes_written,
                                                  comp_bytes_read,
                                                  comp_target,
                                                  disk_target,
                                                  str.str());
                        }
                     }
                }
                else //single message fields
                {
                    vector<const Message*> child_messages;
                    for (uint32 j=0;j<messages.size();j++)
                        child_messages.push_back(&(messages[j]->GetReflection()->GetMessage(*(messages[j]), desc->field(i))));

                    if (desc->field(i)->message_type()->name() == "AnyArray")
                    {
                        for (uint32 j=0;j<child_messages.size();j++)
                            bytes_gathered += this_output->serialize<AnyArray>(gather_buf+bytes_gathered,
                                                                  child_messages[j],
                                                                  desc->field(i),
                                                                  child_messages[j]->GetReflection(),
                                                                  col_index);

                        compressBuffer(gather_buf,
                                       compres_buff,
                                       bytes_gathered,
                                       comp_bytes_written,
                                       col_index,
                                       comp_target);
                        comp_bytes_read += bytes_gathered;
                    }
                    else
                    {
                        compressMessageFields(child_messages,
                                              col_index,
                                              gather_buf,
                                              compres_buff,
                                              comp_bytes_written,
                                              comp_bytes_read,
                                              comp_target,
                                              disk_target,
                                              full_name);
                    }
                }

                //in the case of messages, the compression has been done already.
                continue;
            }
            break;

            default:
                throw runtime_error("Unkown field type");
        };//switch field type

        //All values of the current field were serialize
        //to gather_buf. the number of bytes is bytes_gathered.
        compressBuffer(gather_buf,
                       compres_buff,
                       bytes_gathered,
                       comp_bytes_written,
                       col_index,
                       comp_target);
        comp_bytes_read += bytes_gathered;
    } //for all fields

    return;
 }

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
 void FlatProtobufZOFits::compressBuffer(char*              src,
                                         shared_ptr<char>&  dest,
                                         int32              num_bytes,
                                         int32&             bytes_in_dest,
                                         int32&             col_index,
                                         CompressionTarget& comp_target)
 {
    ZFitsOutput* this_output = comp_target.output;
    //get the target block header. Make a copy so
    //that several threads can work in parallel
    FITS::Compression scheme = this_output->real_columns[col_index].block_head;
    uint32 block_head_size = scheme.getSizeOnDisk();

    //add current gathered bytes to the total raw, uncompressed size
    //FIXME THAT IS A BUG AS THERE IS CONCURRENT ACCESS TO THIS VARIABLE BUT NO MUTEX
//    this_output->raw_heap_size += num_bytes;

    //FIXME should this stay here or not ?
    if (num_bytes%4 != 0) num_bytes += 4-(num_bytes%4);

    char* compres_buff_target = dest.get() + bytes_in_dest + 4;

    //otherwise follow the requested compression
    char* target          = compres_buff_target + block_head_size;
    uint32 max_output_size = _compression_block_size-(bytes_in_dest+block_head_size+4);

    uint32 compressed_size = 0;

    for (uint32 i=0;i<scheme.getNumProcs();i++)
    {
        switch (scheme.getProc(i))
        {
            case FITS::eCTAZlib:
            {
                uint64 long_compressed_size = _compression_block_size - sizeof(FITS::TileHeader) - 4 - 40;

                int32 returnVal = compress((Bytef*)(target),
                                           (uLongf*)(&long_compressed_size),
                                           (const Bytef*)(src),
                                           num_bytes);
                if (returnVal != Z_OK)
                {
                    ostringstream str;
                    str << "Could not compress with zlib. error code: "
                        << returnVal << ". num_bytes=" << num_bytes << " compressed_size=" << compressed_size;
                    throw runtime_error(str.str());
                }
                compressed_size = long_compressed_size;

                if (compressed_size >= max_output_size)
                    throw runtime_error("written size exceeded buffer size zlib");
            }
            break;

            case FITS::eCTAzstd:
            {
                size_t available_bytes_in_dest = _compression_block_size - sizeof(FITS::TileHeader) - 44;

                compressed_size = ZSTD_compress(target, available_bytes_in_dest,
                                                src, num_bytes,
                                                _zstd_level);

                if (ZSTD_isError(compressed_size))
                    throw runtime_error("Something went wrong while using zstd compression");
            }
            break;

            case FITS::eCTALZO:
            {
                lzo_uint out_len;
                LZO_HEAP_ALLOC(wrkmem, LZO1X_1_MEM_COMPRESS);

                if (lzo1x_1_compress((unsigned char*)(src),
                                     num_bytes,
                                     (unsigned char*)(target),
                                     &out_len,
                                     wrkmem) != LZO_E_OK)
                    throw runtime_error("Something went wrong during LZO compression");

                compressed_size = out_len;
            }
            break;

            case FITS::eCTASplitHiLo16:
            {
                checkArrayValueSize(num_bytes, 2, FITS::eCTASplitHiLo16);
                splitHiLo16(src, num_bytes);
            }
            break;

            case FITS::eCTA128Offset:
            {
                checkArrayValueSize(num_bytes, 2, FITS::eCTA128Offset);
                int16* values = reinterpret_cast<int16*>(src);
                for (int32 i=0;i<num_bytes/2;i++)
                    values[i] += 128;
            }
            break;

            case FITS::eCTASplitHiLo32:
            {
                checkArrayValueSize(num_bytes, 4, FITS::eCTASplitHiLo32);
                splitHiLo32(src, num_bytes);
            }
            break;

            case FITS::kFactRaw:
            {
                memcpy(target, src, num_bytes);
                compressed_size = num_bytes;
            }
            break;

            case FITS::kFactSmoothing:
            {
                checkArrayValueSize(num_bytes, 2, FITS::kFactSmoothing);
                applySMOOTHING(src, num_bytes/2);
            }
            break;

            case FITS::eCTADiff:
            {
                checkArrayValueSize(num_bytes, 2, FITS::eCTADiff);
                int16* src16 = reinterpret_cast<int16*>(src);
                for (uint32 i=(num_bytes/2)-1;i!=0;i--)
                    src16[i] -= src16[i-1];
            }
            break;

            case FITS::kFactHuffman16:
            {
                checkArrayValueSize(num_bytes, 2, FITS::kFactHuffman16);
                string huffman_output;

                Huffman::Encode(huffman_output,
                                reinterpret_cast<const uint16_t*>(src),
                                num_bytes/2);

                reinterpret_cast<uint32*>(target)[0] = huffman_output.size();
                memcpy(&target[sizeof(uint32)], huffman_output.data(), huffman_output.size());
                compressed_size += huffman_output.size()+sizeof(uint32);
            }
            break;

            case FITS::eCTAHalfman16:
            {
                checkArrayValueSize(num_bytes, 4, FITS::eCTAHalfman16);
                string huffman_output;
                int32 num1 = num_bytes/4;
                int32 num2 = num_bytes/2 - num1; //if num_bytes/2 is odd

                Huffman::Encode(huffman_output,
                                reinterpret_cast<const uint16_t*>(src),
                                num1);

                int32 previous_size = huffman_output.size();
                reinterpret_cast<uint32*>(target)[0] = previous_size;

                Huffman::Encode(huffman_output,
                                reinterpret_cast<const uint16_t*>(src+num1*2),
                                num2);

                reinterpret_cast<uint32*>(target)[1] = huffman_output.size() - previous_size;
                memcpy(&target[2*sizeof(uint32)], huffman_output.data(), huffman_output.size());
                compressed_size += huffman_output.size()+2*sizeof(uint32);
            }
            break;

            default:
                    throw runtime_error("Unhandled compression scheme requested");
                break;
        };//switch
    }//for all procs

    //update the header block and write it to output
    scheme.SetBlockSize(compressed_size+block_head_size);
    scheme.Memcpy(compres_buff_target);
    bytes_in_dest += block_head_size + compressed_size;

    //remember number of compressed bytes in catalog
    comp_target.catalog[col_index].first = block_head_size + compressed_size;

    //move to next column
    col_index++;
 }


///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
 void FlatProtobufZOFits::checkArrayValueSize(int32                      num_bytes,
                                              int32                      multiple,
                                              FITS::CompressionProcess_t ongoing_process)
 {
    if (num_bytes % multiple == 0) return;

    const char* compressionProcessesNames[] =
    {
        "kFactRaw",
        "kFactSmoothing",
        "kFactHuffman16",
        "eCTADiff"      ,
        "eCTADoubleDiff",
        "eCTASplitHiLo16",
        "eCTAHuffTimes4",
        "eCTAZlib"      ,
        "eCTAHuffmanByRow",
        "eCTALZO"         ,
        "eCTARICE"        ,
        "eCTAHuffman8"    ,
        "eCTAHalfman16"   ,
        "eCTAHalfman8"    ,
        "eCTASplitHiLo32" ,
        "eCTALocalDiff"   ,
        "eCTA128Offset"   ,
        "eCTASameValues"  ,
        "eCTALossyFloats" ,
        "eCTASparseValues",
        "eCTAHalfDiff32"  ,
        "eCTALossyInt16"  ,
        "eCTALossyInt32"  ,
        "eCTAzstd"
    };
    ostringstream str;
    str << red << "ERROR: array values' size is not a multiple of "
        << multiple << " bytes as expected while doing process ";
    str << compressionProcessesNames[ongoing_process];

    throw runtime_error(str.str());
 }

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
 void FlatProtobufZOFits::splitHiLo16(char* buffer, uint32 num_bytes)
 {
    if (num_bytes%2 != 0)
    {
        throw runtime_error("Number of bytes not multiple of 2");
    }
    vector<char> hi_words_store(num_bytes/2);
    vector<char> lo_words_store(num_bytes/2);
    char* hi_words = hi_words_store.data();
    char* lo_words = lo_words_store.data();
    char* input    = buffer;
    for (uint32 k=0;k<num_bytes;k+=2)
    {
        *hi_words++ = *input++;
        *lo_words++ = *input++;
    }
    memcpy(buffer,             hi_words_store.data(), num_bytes/2);
    memcpy(buffer+num_bytes/2, lo_words_store.data(), num_bytes/2);
 }

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
 void FlatProtobufZOFits::splitHiLo32(char* buffer, uint32 num_bytes)
 {
    if (num_bytes%4 != 0)
    {
        throw runtime_error("Number of bytes not multiple of 4");
    }
    vector<char> hi_words_store(num_bytes/2);
    vector<char> lo_words_store(num_bytes/2);
    char* hi_words = hi_words_store.data();
    char* lo_words = lo_words_store.data();
    char* input    = buffer;
    for (uint32 k=0;k<num_bytes;k+=4)
    {
        *hi_words++ = *input++;
        *hi_words++ = *input++;
        *lo_words++ = *input++;
        *lo_words++ = *input++;
    }
    memcpy(buffer,             hi_words_store.data(), num_bytes/2);
    memcpy(buffer+num_bytes/2, lo_words_store.data(), num_bytes/2);
 }


///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
 uint32 FlatProtobufZOFits::applySMOOTHING(char* data, uint32 numElems)
 {
    int16* short_data = reinterpret_cast<int16*>(data);
    for (int j=numElems-1;j>1;j--)
        short_data[j] = short_data[j] - (short_data[j-1]+short_data[j-2])/2;
    return numElems*sizeof(int16);
 }

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
void FlatProtobufZOFits::requestExplicitCompression(const string& field,
                                                    const string& compression)
{

    vector<uint16> real_scheme;
    vector<uint16>& scheme = (field=="default") ? _default_comp : real_scheme;


    if (compression == "nectarcam")
    {
        requestExplicitCompression("eventNumber",                  "ricefact");
        requestExplicitCompression("hiGain.waveforms.samples",     "diffman16");
        requestExplicitCompression("hiGain.waveforms.num_samples", "zlib");
        requestExplicitCompression("hiGain.integrals.gains",       "zrice");
        requestExplicitCompression("loGain.waveforms.samples",     "doublediffman16");
        requestExplicitCompression("loGain.waveforms.num_samples", "zlib");
        requestExplicitCompression("event_type",                   "zlib");
        requestExplicitCompression("loGain.integrals.gains",       "zlib");
        requestExplicitCompression("cameraCounters.counters",      "zrice32");
        requestExplicitCompression("moduleStatus.status",          "zlib");
        requestExplicitCompression("pixelPresence.presence",       "zlib");
        requestExplicitCompression("acquisitionMode",              "zlib");
        requestExplicitCompression("uctsDataPresence",             "zlib");
        requestExplicitCompression("uctsData.data",                "zlib");
        requestExplicitCompression("tibDataPresence",              "zlib");
        requestExplicitCompression("tibData.data",                 "zrice32");
        requestExplicitCompression("swatDataPresence",             "zlib");
        requestExplicitCompression("swatData.data",                "zlib");
    }
    else if (compression == "lst")
    {
        requestExplicitCompression("configuration_id",           "zrice32");
        requestExplicitCompression("event_id",                   "zrice32");
        requestExplicitCompression("tel_event_id",               "zrice32");
        requestExplicitCompression("trigger_time_s",             "zrice32");
        requestExplicitCompression("trigger_time_qns",           "zrice32");
        requestExplicitCompression("trigger_type",               "zrice32");
        requestExplicitCompression("waveform",                   "fact");
        requestExplicitCompression("pixel_status",               "zlib");
        requestExplicitCompression("ped_id",                     "zrice32");
        requestExplicitCompression("lstcam.module_status",       "lzo");
        requestExplicitCompression("lstcam.extdevices_presence", "zrice32");
        requestExplicitCompression("lstcam.tib_data",            "zrice32");
        requestExplicitCompression("lstcam.cdts_data",           "zrice32");
        requestExplicitCompression("lstcam.swat_data",           "zrice32");
        requestExplicitCompression("lstcam.counters",            "zlib");
        requestExplicitCompression("lstcam.chips_flags",         "zrice32");
        requestExplicitCompression("lstcam.first_capacitor_id",  "doublediffman16");
        requestExplicitCompression("lstcam.drs_tag_status",      "lzo");
        requestExplicitCompression("lstcam.drs_tag",             "fact");
    }
    else if (compression == "lst-r1v1-uncalibrated") {
         requestExplicitCompression("waveform", "fact");
         requestExplicitCompression("event_id", "zrice32");
         requestExplicitCompression("tel_id", "zrice32");
         requestExplicitCompression("local_run_id", "zrice32");
         requestExplicitCompression("event_type", "zrice32");
         requestExplicitCompression("event_time_s", "zrice32");
         requestExplicitCompression("event_time_qns", "zrice32");
         requestExplicitCompression("num_channels", "zrice32");
         requestExplicitCompression("num_samples", "zrice32");
         requestExplicitCompression("num_pixels", "zrice32");
         requestExplicitCompression("num_modules", "zrice32");
         requestExplicitCompression("pixel_status", "zlib");
         requestExplicitCompression("first_cell_id", "doublediffman16");
         requestExplicitCompression("module_hires_local_clock_counter", "zlib");
         requestExplicitCompression("calibration_monitoring_id", "zrice32");
         requestExplicitCompression("debug.module_status", "lzo");
         requestExplicitCompression("debug.extdevices_presence", "zrice32");
         requestExplicitCompression("debug.tib_data", "zrice32");
         requestExplicitCompression("debug.cdts_data", "zrice32");
         requestExplicitCompression("debug.swat_data", "zrice32");
         requestExplicitCompression("debug.counters", "zlib");
         requestExplicitCompression("debug.chips_flags", "zrice32");
         requestExplicitCompression("debug.tdp_action", "zrice32");
    }
    else if (compression == "zlib")
    {
        scheme.resize(1);
        scheme[0] = FITS::eCTAZlib;
    }
    else if (compression == "fact")
    {
        scheme.resize(2);
        scheme[0] = FITS::kFactSmoothing;
        scheme[1] = FITS::kFactHuffman16;
    }
    else if (compression == "diffman16")
    {
        scheme.resize(2);
        scheme[0] = FITS::eCTADiff;
        scheme[1] = FITS::kFactHuffman16;
    }
    else if (compression == "doublediffman16")
    {
        scheme.resize(4);
        scheme[0] = FITS::eCTADiff;
        scheme[1] = FITS::eCTA128Offset;
        scheme[2] = FITS::eCTASplitHiLo16;
        scheme[3] = FITS::eCTAZlib;
    }
    else if (compression == "ricefact")
    {
        scheme.resize(3);
        scheme[0] = FITS::eCTASplitHiLo16;
        scheme[1] = FITS::kFactSmoothing;
        scheme[2] = FITS::eCTAHalfman16;
    }
    else if (compression == "lzo")
    {
        scheme.resize(1);
        scheme[0] = FITS::eCTALZO;

       if (lzo_init() != LZO_E_OK)
           throw runtime_error("Cannot initialize LZO");
    }
    else if (compression == "zrice")
    {
        scheme.resize(2);
        scheme[0] = FITS::eCTASplitHiLo16;
        scheme[1] = FITS::eCTAZlib;
    }
    else if (compression == "zrice32")
    {
        scheme.resize(2);
        scheme[0] = FITS::eCTASplitHiLo32;
        scheme[1] = FITS::eCTAZlib;
    }
    else if (compression == "raw")
    {
        scheme.resize(1);
        scheme[0] = FITS::kFactRaw;
    }
    else if (compression.substr(0,4) == "zstd")
    {
        scheme.resize(1);
        scheme[0] = FITS::eCTAzstd;
        if (compression.size() > 4)
        {
            _zstd_level = atoi(compression.substr(4, compression.size()-4).c_str());
            ADH_info << "Set ZSTD compression level to " << _zstd_level << endl;
        }
    }
    else
    {
        ostringstream str;
        str << "Unkown compression scheme: " << compression;
        str << " acceptable values are:" << endl;
        str << "...........zlib: the well-known zlib," << endl;
        str << "...........fact: average difference with 2 previous "
               "samples, then huffman 16 bits," << endl;
        str << "......diffman16: difference with previous sample, "
               "then huffman 16 bits," << endl;
        str << "doublediffman16: difference with previous sample, "
               "then offset of 128, then 16-bits splitting then zlib," << endl;
        str << ".......ricefact: the symmetric of factrice: hi-lo splitting, "
               "then smoothing, then two huffmans ," << endl;
        str << "..........zrice: 16-bits splitting then zlib," << endl;
        str << "........zrice32: 32-bits splitting then zlib," << endl;
        str << "........lzorice: 16-bits splitting then lzo compression," << endl;
        str << "..........zstdX: z-standard level X, with X between -1 and 22," << endl;
        str << "nectarcam: nectarcam specific compression" << endl;
        str << "lst: lst-cam specific compression" << endl;
        str << "............raw: no compression," << endl;

        throw runtime_error(str.str());
    }

    if (field!="default")
        _explicit_comp[field] = scheme;
}

///////////////////////////////////////////////////////////////////////////////
//  TEMPLATES SPECIALIZATION
///////////////////////////////////////////////////////////////////////////////
template <>
uint32 FlatProtobufZOFits::ZFitsOutput::serialize<AnyArray>(char*                  target,
                                                            const Message*         message,
                                                            const FieldDescriptor* field,
                                                            const Reflection*      ,
                                                            const int32            col_index)
{
    uint32 num_bytes_written = 0;

    const AnyArray* array = static_cast<const AnyArray*>(message);
    const string& data = array->data();

    //FIXME make sure that the size is small enough to fit into a signed int32
    reinterpret_cast<int32*>(target)[0] = (int32)(data.size());
    num_bytes_written = sizeof(int32);

    //update the max size of the column, if required
    uint32 num_items = data.size();

    switch (array->type())
    {
        case AnyArray::U8:
        case AnyArray::S8:
        case AnyArray::BOOL:
            break;
        case AnyArray::U16:
        case AnyArray::S16:
            num_items /= 2;
            break;
        case AnyArray::U32:
        case AnyArray::S32:
        case AnyArray::FLOAT:
            num_items /= 4;
            break;
        case AnyArray::U64:
        case AnyArray::S64:
        case AnyArray::DOUBLE:
            num_items /= 8;
            break;
        default:
            cout << "Couldn't find AnyArray element size this many bytes: " << num_items << endl;
            break;
    }

    if (num_items > columns_sizes[col_index]) 
        columns_sizes[col_index] = num_items;

    memcpy(target+num_bytes_written, &data[0], data.size());
    num_bytes_written += data.size();

    return num_bytes_written;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
uint32 FlatProtobufZOFits::ZFitsOutput::serialize<char>(char*                  target,
                                                        const Message*         message,
                                                        const FieldDescriptor* field,
                                                        const Reflection*      ,
                                                        const int32            col_index)
{
    if (field->is_repeated())
        throw runtime_error("Repeated string / bytes fields not handled "
                            "yet in zfits... sorry !");

    uint32 num_bytes_written = 0;

    const Reflection* refl = message->GetReflection();

    const string& data = refl->GetString(*message, field);
    //FIXME make sure that the size is small enough to fit into a signed int32
    reinterpret_cast<int32*>(target)[0] = (int32)(data.size());
    num_bytes_written = sizeof(int32);

    if (data.size() > columns_sizes[col_index])
        columns_sizes[col_index] = data.size();

    memcpy(target+num_bytes_written, &data[0], data.size());
    num_bytes_written += data.size();

    return num_bytes_written;
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
uint32 FlatProtobufZOFits::ZFitsOutput::serialize<EnumValueDescriptor>(char*                  target,
                                                                       const Message*         message,
                                                                       const FieldDescriptor* field,
                                                                       const Reflection*      reflec,
                                                                       const int32            col_index)
{
    uint32 num_bytes_written = 0;

    if (field->is_repeated())
    {
        int32 field_size = reflec->FieldSize(*message, field);
        reinterpret_cast<uint32*>(target)[0] = field_size;
        num_bytes_written += sizeof(uint32);

        for (int32 i=0; i<field_size; i++)
        {
            reinterpret_cast<int32*>(target+num_bytes_written)[0] =
                reflec->GetRepeatedEnum(*message, field, i)->number();
            num_bytes_written += sizeof(int32);
        }
        if ((uint32)(field_size) > columns_sizes[col_index])
            columns_sizes[col_index] = field_size;
    }
    else
    {
        reinterpret_cast<int32*>(target)[0] =
            reflec->GetEnum(*message, field)->number();
        num_bytes_written += sizeof(int32);
    }

    return num_bytes_written;
}


///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
uint32 FlatProtobufZOFits::ZFitsOutput::getProtobufValue<uint32>(const Message&         message,
                                                                 const FieldDescriptor* field,
                                                                 const Reflection*      reflec)
{
    return reflec->GetUInt32(message, field);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
int32 FlatProtobufZOFits::ZFitsOutput::getProtobufValue<int32>(const Message&         message,
                                                               const FieldDescriptor* field,
                                                               const Reflection*      reflec)
{
    return reflec->GetInt32(message, field);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
uint64 FlatProtobufZOFits::ZFitsOutput::getProtobufValue<uint64>(const Message&         message,
                                                                 const FieldDescriptor* field,
                                                                 const Reflection*      reflec)
{
    return reflec->GetUInt64(message, field);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
int64 FlatProtobufZOFits::ZFitsOutput::getProtobufValue<int64>(const Message&         message,
                                                               const FieldDescriptor* field,
                                                               const Reflection*      reflec)
{
    return reflec->GetInt64(message, field);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
double FlatProtobufZOFits::ZFitsOutput::getProtobufValue<double>(const Message&         message,
                                                                 const FieldDescriptor* field,
                                                                 const Reflection*      reflec)
{
    return reflec->GetDouble(message, field);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
float FlatProtobufZOFits::ZFitsOutput::getProtobufValue<float>(const Message&         message,
                                                               const FieldDescriptor* field,
                                                               const Reflection*      reflec)
{
    return reflec->GetFloat(message, field);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
bool FlatProtobufZOFits::ZFitsOutput::getProtobufValue<bool>(const Message&         message,
                                                             const FieldDescriptor* field,
                                                             const Reflection*      reflec)
{
    return reflec->GetBool(message, field);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
uint32 FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<uint32>(const Message&         message,
                                                                         const FieldDescriptor* field,
                                                                         const Reflection*      reflec,
                                                                         int32                  index)
{
    return reflec->GetRepeatedUInt32(message, field, index);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
int32 FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<int32>(const Message&         message,
                                                                       const FieldDescriptor* field,
                                                                       const Reflection*      reflec,
                                                                       int32                  index)
{
    return reflec->GetRepeatedInt32(message, field, index);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
uint64 FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<uint64>(const Message&         message,
                                                                         const FieldDescriptor* field,
                                                                         const Reflection*      reflec,
                                                                         int32                  index)
{
    return reflec->GetRepeatedUInt64(message, field, index);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
int64 FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<int64>(const Message&         message,
                                                                       const FieldDescriptor* field,
                                                                       const Reflection*      reflec,
                                                                       int32                  index)
{
    return reflec->GetRepeatedInt64(message, field, index);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
double FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<double>(const Message&         message,
                                                                         const FieldDescriptor* field,
                                                                         const Reflection*      reflec,
                                                                         int32                  index)
{
    return reflec->GetRepeatedDouble(message, field, index);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
float FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<float>(const Message&         message,
                                                                       const FieldDescriptor* field,
                                                                       const Reflection*      reflec,
                                                                       int32                  index)
{
    return reflec->GetRepeatedFloat(message, field, index);
}

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
template <>
bool FlatProtobufZOFits::ZFitsOutput::getProtobufRepeatedValue<bool>(const Message&         message,
                                                                     const FieldDescriptor* field,
                                                                     const Reflection*      reflec,
                                                                     int32                  index)
{
    return reflec->GetRepeatedBool(message, field, index);
}

 }; //namespace ADH

 }; //namespace IO
