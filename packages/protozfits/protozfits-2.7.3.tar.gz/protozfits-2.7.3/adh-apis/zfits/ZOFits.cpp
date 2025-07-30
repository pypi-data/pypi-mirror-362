/**
 * @file ZOFits.cpp
 * @brief Base Compressed Binary FITS tables writer class
 *
 *  Created on: May 16, 2013
 *      Author: lyard-bretz
 *
 */


#include "ZOFits.h"

         ZOFits::ZOFits(uint32_t numTiles    ,
                        uint32_t rowPerTile ,
                        uint64_t maxUsableMem) : OFits(),
                                                 fMemPool(0, maxUsableMem*1000),
                                                 fWriteToDiskQueue(std::bind(&ZOFits::WriteBufferToDisk, this, std::placeholders::_1), false)
        {
            InitMemberVariables(numTiles, rowPerTile, maxUsableMem*1000);
            //ETIENNE THREADS ALWAYS SET TO 0 IN ZOFITS: EASIEST WAY TO STOP THESE THREADS WITHOUT MODIFYING THE CODE TOO MUCH FOR NOW
            SetNumThreads(0);//DefaultNumThreads());
        }

         ZOFits::ZOFits(const char* fname,
                        uint32_t numTiles   ,
                        uint32_t rowPerTile ,
                        uint64_t maxUsableMem) : OFits(fname),
                                                 fMemPool(0, maxUsableMem*1000),
                                                 fWriteToDiskQueue(std::bind(&ZOFits::WriteBufferToDisk, this, std::placeholders::_1), false)
        {
            InitMemberVariables(numTiles, rowPerTile, maxUsableMem*1000);
            //ETIENNE THREADS ALWAYS SET TO 0 IN ZOFITS: EASIEST WAY TO STOP THESE THREADS WITHOUT MODIFYING THE CODE TOO MUCH FOR NOW
            SetNumThreads(0);//DefaultNumThreads());
        }

        void ZOFits::InitMemberVariables(const uint32_t nt, const uint32_t rpt, const uint64_t maxUsableMem)
        {
            fCheckOffset = 0;
            fNumQueues   = 0;

            fNumTiles       = nt==0 ? 1 : nt;
            fNumRowsPerTile = rpt;

            fRealRowWidth     = 0;
            fCatalogOffset    = 0;
            fCatalogSize      = 0;

            fMaxUsableMem = maxUsableMem;

            fThreadsException = std::exception_ptr();

            fErrno = 0;

            fShouldAllocateBuffers = true;
        }

         bool ZOFits::WriteTableHeader(const char* name)
        {
            reallocateBuffers();

            SetInt("ZNAXIS1", fRealRowWidth);

            OFits::WriteTableHeader(name);

 //ETIENNE THREADS ALWAYS SET TO 0 IN ZOFITS: EASIEST WAY TO STOP THESE THREADS WITHOUT MODIFYING THE CODE TOO MUCH FOR NOW
 //           fCompressionQueues.front().setPromptExecution(fNumQueues==0);
 //           fWriteToDiskQueue.setPromptExecution(fNumQueues==0);
            if (false)//fNumQueues != 0)
            {
                //start the compression queues
                for (auto it=fCompressionQueues.begin(); it!= fCompressionQueues.end(); it++)
                    it->start();

                //start the disk writer
                fWriteToDiskQueue.start();
            }

            //mark that no tile has been written so far
            fLatestWrittenTile = -1;

            //no wiring error (in the writing of the data) has occured so far
            fErrno = 0;

            return good();
        }

        void ZOFits::open(const char* filename, bool addEXTNAMEKey)
        {
            OFits::open(filename, addEXTNAMEKey);

            //add compression-related header entries
            SetBool( "ZTABLE",   true,            "Table is compressed");
            SetInt(  "ZNAXIS1",  0,               "Width of uncompressed rows");
            SetInt(  "ZNAXIS2",  0,               "Number of uncompressed rows");
            SetInt(  "ZPCOUNT",  0,               "");
            SetInt(  "ZHEAPPTR", 0,               "");
            SetInt(  "ZTILELEN", fNumRowsPerTile, "Number of rows per tile");
            SetInt(  "THEAP",    0,               "");
            SetStr(  "RAWSUM",   "         0",    "Checksum of raw little endian data");
            SetFloat("ZRATIO",   0,               "Compression ratio");
            SetInt(  "ZSHRINK",  1,               "Catalog shrink factor");

            fCatalogSize   = 0;
            fRealRowWidth  = 0;
            fCatalogOffset = 0;
            fCatalogSize   = 0;
            fCheckOffset   = 0;

            fRealColumns.clear();
            fCatalog.clear();
            fCatalogSum.reset();
            fRawSum.reset();
        }

        bool ZOFits::WriteDrsOffsetsTable()
        {
            return good();
        }

        uint32_t ZOFits::GetBytesPerRow() const
        {
            return fRealRowWidth;
        }

        bool ZOFits::WriteCatalog()
        {
            const uint32_t one_catalog_row_size = fTable.num_cols*2*sizeof(uint64_t);
            const uint32_t total_catalog_size   = fNumTiles*one_catalog_row_size;

            // swap the catalog bytes before writing
            std::vector<char> swapped_catalog(total_catalog_size);

            uint32_t shift = 0;
            for (auto it=fCatalog.cbegin(); it!=fCatalog.cend(); it++)
            {
                revcpy<sizeof(uint64_t)>(swapped_catalog.data() + shift, (char*)(it->data()), fTable.num_cols*2);
                shift += one_catalog_row_size;
            }

            if (fCatalogSize < fNumTiles)
                memset(swapped_catalog.data()+shift, 0, total_catalog_size-shift);

            // first time writing ? remember where we are
            if (fCatalogOffset == 0)
                fCatalogOffset = tellp();

            // remember where we came from
            const off_t where_are_we = tellp();

            // write to disk
            seekp(fCatalogOffset);
            write(swapped_catalog.data(), total_catalog_size);

            if (where_are_we != fCatalogOffset)
                seekp(where_are_we);

            // udpate checksum
            fCatalogSum.reset();
            fCatalogSum.add(swapped_catalog.data(), total_catalog_size);

            return good();
        }

        void ZOFits::DrsOffsetCalibrate(char* )
        {

        }

        ZOFits::CatalogRow& ZOFits::AddOneCatalogRow()
        {
            // add one row to the catalog
            fCatalog.emplace_back(CatalogRow());
            fCatalog.back().resize(fTable.num_cols);
            for (auto it=fCatalog.back().begin(); it != fCatalog.back().end(); it++)
                *it = CatalogEntry(0,0);

            fCatalogSize++;

            return fCatalog.back();
        }

        bool ZOFits::WriteRow(const void* ptr, size_t cnt, bool)
        {
            if (cnt != fRealRowWidth)
            {

                throw std::runtime_error("Wrong size of row given to WriteRow");

            }

            //check if something hapenned while the compression threads were working
            //if so, re-throw the exception that was generated
            if (fThreadsException != std::exception_ptr())
                std::rethrow_exception(fThreadsException);


            //copy current row to pool or rows waiting for compression
            char* target_location = fSmartBuffer.get() + fRealRowWidth*(fTable.num_rows%fNumRowsPerTile);
            memcpy(target_location, ptr, fRealRowWidth);

            //for now, make an extra copy of the data, for RAWSUM checksuming.
            //Ideally this should be moved to the threads
            //However, because the RAWSUM must be calculated before the tile is transposed, I am not sure whether
            //one extra memcpy per row written is worse than 100 rows checksumed when the tile is full....
            const uint32_t rawOffset = (fTable.num_rows*fRealRowWidth)%4;
            char* buffer = fRawSumBuffer.data() + rawOffset;
            auto ib = fRawSumBuffer.begin();
            auto ie = fRawSumBuffer.rbegin();
            *ib++ = 0;
            *ib++ = 0;
            *ib++ = 0;
            *ib   = 0;

            *ie++ = 0;
            *ie++ = 0;
            *ie++ = 0;
            *ie   = 0;

            memcpy(buffer, ptr, fRealRowWidth);

            fRawSum.add(fRawSumBuffer, false);

            fTable.num_rows++;

            if (fTable.num_rows % fNumRowsPerTile != 0)
            {
                errno = fErrno;
                return errno==0;
            }

            // use the least occupied queue
            const auto imin = std::min_element(fCompressionQueues.begin(), fCompressionQueues.end());

            if (!imin->emplace(InitNextCompression()))
            {

                throw std::runtime_error("The compression queues are not started. Did you close the file before writing this row?");

            }

            errno = fErrno;
            return errno==0;
        }

        void ZOFits::FlushNumRows()
        {
            SetInt("NAXIS2", (fTable.num_rows + fNumRowsPerTile-1)/fNumRowsPerTile);
            SetInt("ZNAXIS2", fTable.num_rows);
            FlushHeader();
        }

        ZOFits::CompressionTarget ZOFits::InitNextCompression()
        {
            CompressionTarget target(AddOneCatalogRow());

            //fill up compression target
            target.src            = fSmartBuffer;
            target.transposed_src = fMemPool.malloc();
            target.num_rows       = fTable.num_rows;

            //fill up write to disk target
            WriteTarget &write_target = target.target;
            write_target.tile_num = (fTable.num_rows-1)/fNumRowsPerTile;
            write_target.size     = 0;
            write_target.data     = fMemPool.malloc();

            //get a new buffer to host the incoming data
            fSmartBuffer = fMemPool.malloc();

            return target;
        }

        uint32_t ZOFits::ShrinkCatalog()
        {
            //add empty row to get either the target number of rows, or a multiple of the allowed size
            for (uint32_t i=0;i<fCatalogSize%fNumTiles;i++)
                AddOneCatalogRow();

            //did we write more rows than what the catalog could host ?
            if (fCatalogSize <= fNumTiles) // nothing to do
                return 1;

            //always exact as extra rows were added just above
            const uint32_t shrink_factor = fCatalogSize / fNumTiles;

            cout << "\33[33mWARNING: you wrote more data than header allows for it: FTOOLS won't work on this file.\33[0m" << endl;

            //shrink the catalog !
            uint32_t entry_id = 1;
            auto it = fCatalog.begin();
            it++;
            for (; it != fCatalog.end(); it++)
            {
                if (entry_id >= fNumTiles)
                    break;

                const uint32_t target_id = entry_id*shrink_factor;

                auto jt = it;
                for (uint32_t i=0; i<target_id-entry_id; i++)
                    jt++;

                *it = *jt;

                entry_id++;
            }

            const uint32_t num_tiles_to_remove = fCatalogSize-fNumTiles;

            //remove the too many entries
            for (uint32_t i=0;i<num_tiles_to_remove;i++)
            {
                fCatalog.pop_back();
                fCatalogSize--;
            }

            //update header keywords
            fNumRowsPerTile *= shrink_factor;

            SetInt("ZTILELEN", fNumRowsPerTile);
            SetInt("ZSHRINK",  shrink_factor);

            return shrink_factor;
        }

        bool ZOFits::close()
        {
            // stop compression and write threads
            //for (auto it=fCompressionQueues.begin(); it != fCompressionQueues.end(); it++)
            //    it->wait();

            //fWriteToDiskQueue.wait();

            if (tellp() < 0)
                return false;

            //check if something hapenned while the compression threads were working
            //if so, re-throw the exception that was generated
            if (fThreadsException != std::exception_ptr())
                std::rethrow_exception(fThreadsException);

//FIXME: this is terrible: zofits is broken so that ctaofits can work...
            //write the last tile of data (if any)
//            if (fErrno==0 && fTable.num_rows%fNumRowsPerTile!=0)
//            {
//                fWriteToDiskQueue.enablePromptExecution();
//                fCompressionQueues.front().enablePromptExecution();
//                fCompressionQueues.front().emplace(InitNextCompression());
//            }

            AlignTo2880Bytes();

            int64_t heap_size = 0;
            int64_t compressed_offset = 0;
            for (auto it=fCatalog.begin(); it!= fCatalog.end(); it++)
            {
                compressed_offset += sizeof(FITS::TileHeader);
                heap_size         += sizeof(FITS::TileHeader);
                for (uint32_t j=0; j<it->size(); j++)
                {
                    heap_size += (*it)[j].first;
                    if ((*it)[j].first < 0) throw runtime_error("Negative block size");
                    (*it)[j].second = compressed_offset;
                    compressed_offset += (*it)[j].first;
                    if ((*it)[j].first == 0)
                        (*it)[j].second = 0;
                }
            }

            const uint32_t shrink_factor = ShrinkCatalog();

            //update header keywords
            //SetInt("ZNAXIS1", fRealRowWidth);
            SetInt("ZNAXIS2", fTable.num_rows);

            //here the catalog is the full reserved size, i.e. longer than only the rows that were utilized
            SetInt("ZHEAPPTR", fCatalogSize*fTable.num_cols*sizeof(uint64_t)*2);

            const uint32_t total_num_tiles_written = (fTable.num_rows + fNumRowsPerTile-1)/fNumRowsPerTile;
            const uint32_t total_catalog_width     = 2*sizeof(int64_t)*fTable.num_cols;

            SetInt("THEAP",  total_num_tiles_written*total_catalog_width);
            SetInt("NAXIS1", total_catalog_width);
            SetInt("NAXIS2", total_num_tiles_written);
            SetStr("RAWSUM", std::to_string((long long int)(fRawSum.val())));

            if (heap_size != 0)
            {
                const float compression_ratio = (float)(fRealRowWidth*fTable.num_rows)/(float)heap_size;
                SetFloat("ZRATIO", compression_ratio);
            }
            //add to the heap size the size of the gap between the catalog and the actual heap
            heap_size += (fCatalogSize - total_num_tiles_written)*fTable.num_cols*sizeof(uint64_t)*2;

            SetInt("PCOUNT", heap_size, "size of special data area");

            //Just for updating the fCatalogSum value
            WriteCatalog();

            fDataSum += fCatalogSum;

            const Checksum checksm = UpdateHeaderChecksum();

            std::ofstream::close();

            fSmartBuffer = std::shared_ptr<char>();

            //restore the number of rows per tile in case the catalog has been shrinked
            if (shrink_factor != 1)
                fNumRowsPerTile /= shrink_factor;

            if ((checksm+fDataSum).valid())
                return true;

            std::ostringstream sout;
            sout << "Checksum (" << std::hex << checksm.val() << ") invalid.";

            throw std::runtime_error(sout.str());

        }

        bool ZOFits::AddColumn(uint32_t cnt, char typechar, const std::string& name, const std::string& unit,
                       const std::string& comment, bool addHeaderKeys)
        {
            return AddColumn(FITS::kFactRaw, cnt, typechar, name, unit, comment, addHeaderKeys);
        }


        bool ZOFits::AddColumn(const FITS::Compression &comp, uint32_t cnt, char typechar, const std::string& name,
                       const std::string& unit, const std::string& comment, bool addHeaderKeys)
        {
            if (!OFits::AddColumn(1, 'Q', name, unit, comment, addHeaderKeys))
                return false;

            const size_t size = SizeFromType(typechar);

            Table::Column col;
            col.name   = name;
            col.type   = typechar;
            col.num    = cnt;
            col.size   = size;
            col.offset = fRealRowWidth;

            fRealRowWidth += size*cnt;

            fRealColumns.emplace_back(col, comp);

            switch (typechar)
            {
                case 'S':
                    SetFloat("TZERO"+std::to_string((long long int)(fRealColumns.size())), -128., "Offset for signed chars");
                    typechar = 'B';
                    break;

                case 'U':
                    SetFloat("TZERO"+std::to_string((long long int)(fRealColumns.size())), 32768., "Offset for uint16");
                    typechar = 'I';
                    break;
                case 'V':
                    SetFloat("TZERO"+std::to_string((long long int)(fRealColumns.size())), 2147483648., "Offset for uint32");
                    typechar = 'J';
                    break;
                case 'W':
                    SetFloat("TZERO"+std::to_string((long long int)(fRealColumns.size())), 9223372036854775808., "Offset for uint64");
                    typechar = 'K';
                    break;
                default:
                    ;
            }

            SetStr("ZFORM"+std::to_string((long long int)(fRealColumns.size())), std::to_string((long long int)(cnt))+typechar, "format of "+name+" "+CommentFromType(typechar));
            SetStr("ZCTYP"+std::to_string((long long int)(fRealColumns.size())), "CTA", "Custom CTA compression");

            return true;
        }


        int32_t ZOFits::GetNumThreads() const { return fNumQueues; }
        bool ZOFits::SetNumThreads(uint32_t num)
        {
            if (tellp()>0)
            {

                throw std::runtime_error("Number of threads cannot be changed in the middle of writing a file");

                return false;
            }

            //get number of physically available threads
#ifdef HAVE_BOOST_THREAD
            unsigned int num_available_cores = boost::thread::hardware_concurrency();
#else
            unsigned int num_available_cores = std::thread::hardware_concurrency();
#endif
            // could not detect number of available cores from system properties...
            if (num_available_cores == 0)
                num_available_cores = 1;

            // leave one core for the main thread and one for the writing
            if (num > num_available_cores)
                num = num_available_cores>2 ? num_available_cores-2 : 1;

            fCompressionQueues.resize(num<1?1:num, Queue<CompressionTarget>(std::bind(&ZOFits::CompressBuffer, this, std::placeholders::_1), false));

            fNumQueues = num;

//            cout << "Num threads set to " << num << endl;
            return true;
        }

        uint32_t ZOFits::GetNumTiles() const { return fNumTiles; }
        void ZOFits::SetNumTiles(uint32_t num) { fNumTiles=num; }


        /// Allocates the required objects.
        void ZOFits::reallocateBuffers()
        {
            if (!fShouldAllocateBuffers)
                return;

            size_t total_block_head_size = 0;
            for (auto it=fRealColumns.begin(); it!=fRealColumns.end(); it++)
                total_block_head_size += it->block_head.getSizeOnDisk();

            const size_t chunk_size = fRealRowWidth*fNumRowsPerTile + total_block_head_size + sizeof(FITS::TileHeader) + 8; //+8 for checksuming;
            fMemPool.setChunkSize(chunk_size);

            fSmartBuffer = fMemPool.malloc();
            fRawSumBuffer.resize(fRealRowWidth + 4-fRealRowWidth%4); //for checksuming
        }

        bool ZOFits::writeCompressedDataToDisk(char* src, const uint32_t sizeToWrite)
        {
            char* checkSumPointer = src+4;
            int32_t extraBytes = 0;
            uint32_t sizeToChecksum = sizeToWrite;

            //should we extend the array to the left ?
            if (fCheckOffset != 0)
            {
                sizeToChecksum  += fCheckOffset;
                checkSumPointer -= fCheckOffset;
                memset(checkSumPointer, 0, fCheckOffset);
            }

            //should we extend the array to the right ?
            if (sizeToChecksum%4 != 0)
            {
                extraBytes = 4 - (sizeToChecksum%4);
                memset(checkSumPointer+sizeToChecksum, 0, extraBytes);
                sizeToChecksum += extraBytes;
            }

            //do the checksum
            fDataSum.add(checkSumPointer, sizeToChecksum);

            fCheckOffset = (4 - extraBytes)%4;

            //write data to disk
            write(src+4, sizeToWrite);

            return good();
        }

         bool ZOFits::CompressBuffer(const CompressionTarget& target)
        {
            //Can't get this to work in the thread. Printed the adresses, and they seem to be correct.
            //Really do not understand what's wrong...
            //calibrate data if required
            const uint32_t thisRoundNumRows  = (target.num_rows%fNumRowsPerTile) ? target.num_rows%fNumRowsPerTile : fNumRowsPerTile;
            for (uint32_t i=0;i<thisRoundNumRows;i++)
            {
                char* target_location = target.src.get() + fRealRowWidth*i;
                DrsOffsetCalibrate(target_location);
            }

            try
            {

                //transpose the original data
                copyTransposeTile(target.src.get(), target.transposed_src.get(), target.num_rows);

                //compress the buffer
                const uint64_t compressed_size = compressBuffer(target.target.data.get(), target.transposed_src.get(), target.num_rows, target.catalog_entry);

                //post the result to the writing queue
                //get a copy so that it becomes non-const
                fWriteToDiskQueue.emplace(target.target, compressed_size);


            }
            catch (...)
            {
                fThreadsException = std::current_exception();
                if (fNumQueues == 0)
                    std::rethrow_exception(fThreadsException);
            }


            return true;
        }

         bool ZOFits::WriteBufferToDisk(const WriteTarget& target)
        {
            //is this the tile we're supposed to write ?
            if (target.tile_num != (uint32_t)(fLatestWrittenTile+1))
                return false;

            fLatestWrittenTile++;


            try
            {

                //could not write the data to disk
                if (!writeCompressedDataToDisk(target.data.get(), target.size))
                    fErrno = errno;

            }
            catch (...)
            {
                fThreadsException = std::current_exception();
                if (fNumQueues == 0)
                    std::rethrow_exception(fThreadsException);
            }

            return true;
        }


        uint64_t ZOFits::compressBuffer(char* dest, char* src, uint32_t num_rows, CatalogRow& catalog_row)
        {
            const uint32_t thisRoundNumRows = (num_rows%fNumRowsPerTile) ? num_rows%fNumRowsPerTile : fNumRowsPerTile;
            uint32_t       offset           = 0;

            //skip the checksum reserved area
            dest += 4;

            //skip the 'TILE' marker and tile size entry
            uint64_t compressedOffset = sizeof(FITS::TileHeader);

            //now compress each column one by one by calling compression on arrays
            for (uint32_t i=0;i<fRealColumns.size();i++)
            {
                catalog_row[i].second = compressedOffset;

                if (fRealColumns[i].col.num == 0)
                    continue;

                FITS::Compression& head = fRealColumns[i].block_head;

                //set the default byte telling if uncompressed the compressed Flag
                const uint64_t previousOffset = compressedOffset;

                //skip header data
                compressedOffset += head.getSizeOnDisk();

                for (uint32_t j=0;j<head.getNumProcs();j++)//sequence.size(); j++)
                {
                    switch (head.getProc(j))
                    {
                    case FITS::kFactRaw:
                        compressedOffset += compressUNCOMPRESSED(dest + compressedOffset, src  + offset, thisRoundNumRows*fRealColumns[i].col.size*fRealColumns[i].col.num);
                        break;

                    case FITS::kFactSmoothing:
                        applySMOOTHING(src + offset, thisRoundNumRows*fRealColumns[i].col.num);
                        break;

                    case FITS::kFactHuffman16:
                        if (head.getOrdering() == FITS::kOrderByCol)
                            compressedOffset += compressHUFFMAN16(dest + compressedOffset, src  + offset, thisRoundNumRows, fRealColumns[i].col.size, fRealColumns[i].col.num);
                        else
                            compressedOffset += compressHUFFMAN16(dest + compressedOffset, src  + offset, fRealColumns[i].col.num, fRealColumns[i].col.size, thisRoundNumRows);
                        break;

                    default:
                        std::cout << "Case not handled by switch " << endl;
                        break;

                    }
                }

                //check if compressed size is larger than uncompressed
                //if so set flag and redo it uncompressed
                if ((head.getProc(0) != FITS::kFactRaw) && (compressedOffset - previousOffset > fRealColumns[i].col.size*fRealColumns[i].col.num*thisRoundNumRows+head.getSizeOnDisk()))// && two)
                {
                    //de-smooth !
                    if (head.getProc(0) == FITS::kFactSmoothing)
                        UnApplySMOOTHING(src+offset, fRealColumns[i].col.num*thisRoundNumRows);

                    FITS::Compression he;

                    compressedOffset = previousOffset + he.getSizeOnDisk();
                    compressedOffset += compressUNCOMPRESSED(dest + compressedOffset, src + offset, thisRoundNumRows*fRealColumns[i].col.size*fRealColumns[i].col.num);

                    he.SetBlockSize(compressedOffset - previousOffset);
                    he.Memcpy(dest+previousOffset);

                    offset += thisRoundNumRows*fRealColumns[i].col.size*fRealColumns[i].col.num;

                    catalog_row[i].first = compressedOffset - catalog_row[i].second;
                    continue;
                }

                head.SetBlockSize(compressedOffset - previousOffset);
                head.Memcpy(dest + previousOffset);

                offset += thisRoundNumRows*fRealColumns[i].col.size*fRealColumns[i].col.num;
                catalog_row[i].first = compressedOffset - catalog_row[i].second;
            }

            const FITS::TileHeader tile_head(thisRoundNumRows, compressedOffset);
            memcpy(dest, &tile_head, sizeof(FITS::TileHeader));

            return compressedOffset;
        }

        void ZOFits::copyTransposeTile(const char* src, char* dest, uint32_t num_rows)
        {
            const uint32_t thisRoundNumRows = (num_rows%fNumRowsPerTile) ? num_rows%fNumRowsPerTile : fNumRowsPerTile;

            //copy the tile and transpose it
            for (uint32_t i=0;i<fRealColumns.size();i++)
            {
                switch (fRealColumns[i].block_head.getOrdering())
                {
                case FITS::kOrderByRow:
                    //regular, "semi-transposed" copy
                    for (uint32_t k=0;k<thisRoundNumRows;k++)
                    {
                        memcpy(dest, src+k*fRealRowWidth+fRealColumns[i].col.offset, fRealColumns[i].col.size*fRealColumns[i].col.num);
                        dest += fRealColumns[i].col.size*fRealColumns[i].col.num;
                    }
                    break;

                case FITS::kOrderByCol:
                    //transposed copy
                    for (uint32_t j=0;j<fRealColumns[i].col.num;j++)
                        for (uint32_t k=0;k<thisRoundNumRows;k++)
                        {
                            memcpy(dest, src+k*fRealRowWidth+fRealColumns[i].col.offset+fRealColumns[i].col.size*j, fRealColumns[i].col.size);
                            dest += fRealColumns[i].col.size;
                        }
                    break;
                };
            }
        }

         uint32_t ZOFits::compressUNCOMPRESSED(char* dest, const char* src, uint32_t size)
        {
            memcpy(dest, src, size);
            return size;
        }

        uint32_t ZOFits::compressHUFFMAN16(char* dest, const char* src, uint32_t numRows, uint32_t sizeOfElems, uint32_t numRowElems)
        {
            std::string huffmanOutput;
            uint32_t previousHuffmanSize = 0;

            if (sizeOfElems < 2 )
            {
                throw std::runtime_error("HUFMANN16 can only encode columns with 16-bit or longer types");

            }

            uint32_t huffmanOffset = 0;
            for (uint32_t j=0;j<numRowElems;j++)
            {
                Huffman::Encode(huffmanOutput,
                                reinterpret_cast<const uint16_t*>(&src[j*sizeOfElems*numRows]),
                                numRows*(sizeOfElems/2));
                reinterpret_cast<uint32_t*>(&dest[huffmanOffset])[0] = huffmanOutput.size() - previousHuffmanSize;
                huffmanOffset += sizeof(uint32_t);
                previousHuffmanSize = huffmanOutput.size();
            }

            const size_t totalSize = huffmanOutput.size() + huffmanOffset;

            //only copy if not larger than not-compressed size
            //if (totalSize < numRows*sizeOfElems*numRowElems)
            memcpy(&dest[huffmanOffset], huffmanOutput.data(), huffmanOutput.size());

            return totalSize;
        }

         uint32_t ZOFits::applySMOOTHING(char* data, uint32_t numElems)
        {
            int16_t* short_data = reinterpret_cast<int16_t*>(data);
            for (int j=numElems-1;j>1;j--)
                short_data[j] = short_data[j] - (short_data[j-1]+short_data[j-2])/2;

            return numElems*sizeof(int16_t);
        }

        uint32_t ZOFits::UnApplySMOOTHING(char* data, uint32_t numElems)
        {
            int16_t* short_data = reinterpret_cast<int16_t*>(data);
            for (uint32_t j=2;j<numElems;j++)
                short_data[j] = short_data[j] + (short_data[j-1]+short_data[j-2])/2;

            return numElems*sizeof(uint16_t);
        }



