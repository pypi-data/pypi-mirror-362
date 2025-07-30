/**
 * @file ZIFits.cpp
 * @brief Base Compressed Binary FITS tables reader class
 *
 *  Created on: May 16, 2013
 *      Author: lyard-bretz
 *
 */

#include "ZIFits.h"



    // Basic constructor
    ZIFits::ZIFits(const std::string& fname, const std::string& tableName, bool force)
        : fCatalogInitialized(false), fNumTiles(0), fNumRowsPerTile(0), fCurrentRow(-1), fHeapOff(0), fTileSize(0)
    {
        open(fname.c_str());
        Constructor(fname, "", tableName, force);
    }

    // Alternative contstructor
    ZIFits::ZIFits(const std::string& fname, const std::string& fout, const std::string& tableName, bool force)
        : fCatalogInitialized(false), fNumTiles(0), fNumRowsPerTile(0), fCurrentRow(-1), fHeapOff(0), fTileSize(0)
    {
        open(fname.c_str());
        Constructor(fname, fout, tableName, force);
    }

    // Alternative contstructor
    ZIFits::ZIFits( const IFits::Table &table, std::vector<std::vector<std::pair<int64_t, int64_t>>>& catalog, bool )
		:fCatalogInitialized(true),fNumTiles(0), fNumRowsPerTile(0), fCurrentRow(-1), fHeapOff(0),fCatalog(catalog), fTileSize(0)
		{
			fTable = table;	
		}

    ZIFits::~ZIFits() {}

    //  Skip the next row
    bool ZIFits::SkipNextRow()
    {
        if (!fTable.is_compressed)
            return IFits::SkipNextRow();

        fRow++;
        return true;
    }

    bool ZIFits::IsFileOk() const
    {
        bool rawsum = true;

        if (HasKey("RAWSUM"))
        {
                std::ostringstream str;
                str << fRawsum.val();
                rawsum = (GetStr("RAWSUM") == str.str());
        }

        return IFits::IsFileOk() && rawsum;
    };

    size_t ZIFits::GetNumRows() const
    {
        if (fTable.is_compressed)
            return fTable.Get<size_t>("ZNAXIS2");
        else
            return fTable.Get<size_t>("NAXIS2");
    }
    size_t ZIFits::GetBytesPerRow() const
    {
        if (fTable.is_compressed)
            return fTable.Get<size_t>("ZNAXIS1");
        else
            return fTable.Get<size_t>("NAXIS1");
    }

    //  Stage the requested row to internal buffer
    //  Does NOT return data to users
    void ZIFits::StageRow(size_t row, char* dest)
    {
        if (!fTable.is_compressed)
        {
            IFits::StageRow(row, dest);
            return;
        }
        ReadBinaryRow(row, dest);
    }

    // Do what it takes to initialize the compressed structured
    void ZIFits::InitCompressionReading(bool allocateBuffer)
    {
        //fCatalogInitialized = true;

        if (!fTable.is_compressed)
            return;

        //The constructor may have failed
        if (!good())
            return;

        if (fTable.is_compressed)
            for (auto it=fTable.sorted_cols.cbegin(); it!= fTable.sorted_cols.cend(); it++)
            {
                if (it->comp == kCompCTA)
                    continue;

                clear(rdstate()|std::ios::badbit);
                throw std::runtime_error("Only the CTA compression scheme is handled by this reader.");
            }

        fColumnOrdering.resize(fTable.sorted_cols.size(), FITS::kOrderByRow);

        //Get compressed specific keywords
        fNumTiles       = fTable.is_compressed ? GetInt("NAXIS2") : 0;
        fNumRowsPerTile = fTable.is_compressed ? GetInt("ZTILELEN") : 0;

        //read the file's catalog
        if ( ! fCatalogInitialized )		
        {
					ReadCatalog();
					fCatalogInitialized = true;
				}

        //give it some space for uncompressing
        if (allocateBuffer)
            AllocateBuffers();

        //check that heap agrees with head
        //CheckIfFileIsConsistent();
    }

    // Copy decompressed data to location requested by user
    void ZIFits::MoveColumnDataToUserSpace(char* dest, const char* src, const Table::Column& c)
    {
        if (!fTable.is_compressed)
        {
            IFits::MoveColumnDataToUserSpace(dest, src, c);
            return;
        }

        memcpy(dest, src, c.num*c.size);
    }



    // Get buffer space
    void ZIFits::AllocateBuffers()
    {
        uint32_t buffer_size = fTable.bytes_per_row*fNumRowsPerTile;
        uint32_t compressed_buffer_size = fTable.bytes_per_row*fNumRowsPerTile +
            //use a bit more memory for block headers. 256 char coding the compression sequence max.
            fTable.num_cols*(sizeof(FITS::BlockHeader)+256) +
            //a bit more for the tile headers
            sizeof(FITS::TileHeader) +
            //and a bit more for checksuming
            8;

        if (buffer_size % 4 != 0)
            buffer_size += 4 - (buffer_size%4);

        if (compressed_buffer_size % 4 != 0)
            compressed_buffer_size += 4 - (compressed_buffer_size%4);

        fBuffer.resize(buffer_size);

        fTransposedBuffer.resize(buffer_size);
        fCompressedBuffer.resize(compressed_buffer_size);
    }

    // Read catalog data. I.e. the address of the compressed data inside the heap
    void ZIFits::ReadCatalog()
    {
        std::vector<char> readBuf(16);
        fCatalog.resize(fNumTiles);

        fChkData.reset();

        //check if the catalog has been shrinked
        uint32_t shrink_factor = 1;
        if (HasKey("ZSHRINK"))
                shrink_factor = GetInt("ZSHRINK");

        if (shrink_factor != 1)
            std::cout << "WARNING: Too many tiles were written in this file: recovering catalog data" << std::endl;

        //do the actual reading
        for (uint32_t i=0;i<fNumTiles;i++)
            for (uint32_t j=0;j<fTable.num_cols;j++)
            {
                read(readBuf.data(), 2*sizeof(int64_t));
                fChkData.add(readBuf);
                //swap the bytes
                int64_t tempValues[2] = {0,0};
                revcpy<8>(reinterpret_cast<char*>(tempValues), readBuf.data(), 2);
                if (tempValues[0] < 0 || tempValues[1] < 0)
                {
                    clear(rdstate()|std::ios::badbit);
                    std::ostringstream str;
                    str << "Negative value in the catalog at tile " << i;
                    throw std::runtime_error(str.str());
                }
                //add catalog entry
                fCatalog[i].emplace_back(tempValues[0], tempValues[1]);
            }

        //see if there is a gap before heap data
        fHeapOff = tellg()+fTable.GetHeapShift();
        fHeapFromDataStart = fNumTiles*fTable.num_cols*2*sizeof(int64_t) + fTable.GetHeapShift();

        if (shrink_factor != 1)
        {
            CheckIfFileIsConsistent(true);
            fNumTiles = fCatalog.size();
            fNumRowsPerTile /= shrink_factor;
        }

        //compute the total size of each compressed tile
        fTileSize.resize(fNumTiles);
        fTileOffsets.resize(fNumTiles);
        for (uint32_t i=0;i<fNumTiles;i++)
        {
            fTileSize[i] = 0;
            for (uint32_t j=0;j<fTable.num_cols;j++)
            {
                fTileSize[i] += fCatalog[i][j].first;
                fTileOffsets[i].emplace_back(fCatalog[i][j].second - fCatalog[i][0].second);
            }
        }
    }

    //overrides fits.h method with empty one
    //work is done in ReadBinaryRow because it requires volatile data from ReadBinaryRow
    void ZIFits::WriteRowToCopyFile(size_t row)
    {
        if (row == fRow+1)
            fRawsum.add(fBufferRow, false);
    }

    // Compressed version of the read row
    bool ZIFits::ReadBinaryRow(const size_t &rowNum, char *bufferToRead)
    {
        if (rowNum >= GetNumRows())
            return false;

        if (!fCatalogInitialized)
            InitCompressionReading();

        const uint32_t requestedTile = rowNum/fNumRowsPerTile;
        const uint32_t currentTile   = fCurrentRow/fNumRowsPerTile;

        bool addCheckSum = ((requestedTile == currentTile+1) || (fCurrentRow == -1));

        fCurrentRow = rowNum;
        //should we read yet another chunk of data ?
        if (requestedTile != currentTile)
        {
            //read yet another chunk from the file
            const int64_t sizeToRead = fTileSize[requestedTile] + sizeof(FITS::TileHeader);

            //skip to the beginning of the tile
            const int64_t tileStart =  fCatalog[requestedTile][0].second - sizeof(FITS::TileHeader);

            seekg(fHeapOff+tileStart);

            //calculate the 32 bits offset of the current tile.
            const uint32_t offset = (tileStart + fHeapFromDataStart)%4;

            //point the tile header where it should be
            //we ain't checking the header now
//            TileHeader* tHead = reinterpret_cast<TileHeader*>(fCompressedBuffer.data()+offset);

            ZeroBufferForChecksum(fCompressedBuffer, fCompressedBuffer.size()-(sizeToRead+offset+8));

            //read one tile from disk
            read(fCompressedBuffer.data()+offset, sizeToRead);

            if (addCheckSum)
                fChkData.add(fCompressedBuffer);

            const uint32_t thisRoundNumRows = (GetNumRows()<fCurrentRow + fNumRowsPerTile) ? GetNumRows()%fNumRowsPerTile : fNumRowsPerTile;

            //uncompress it
            UncompressBuffer(requestedTile, thisRoundNumRows, offset+sizeof(FITS::TileHeader));

            // pointer to column (source buffer)
            const char *src = fTransposedBuffer.data();

            uint32_t i=0;
            for (auto it=fTable.sorted_cols.cbegin(); it!=fTable.sorted_cols.cend(); it++, i++)
            {
                char *buffer = fBuffer.data() + it->offset; // pointer to column (destination buffer)

                switch (fColumnOrdering[i])
                {
                case FITS::kOrderByRow:
                    // regular, "semi-transposed" copy
                    for (char *dest=buffer; dest<buffer+thisRoundNumRows*fTable.bytes_per_row; dest+=fTable.bytes_per_row) // row-by-row
                    {
                        memcpy(dest, src, it->bytes);
                        src += it->bytes;  // next column
                    }
                    break;

                case FITS::kOrderByCol:
                    // transposed copy
                    for (char *elem=buffer; elem<buffer+it->bytes; elem+=it->size) // element-by-element (arrays)
                    {
                        for (char *dest=elem; dest<elem+thisRoundNumRows*fTable.bytes_per_row; dest+=fTable.bytes_per_row) // row-by-row
                        {
                                memcpy(dest, src, it->size);
                                src += it->size; // next element
                        }
                    }
                    break;

                default:
                    clear(rdstate()|std::ios::badbit);
                    throw std::runtime_error("Unkown column ordering scheme found");
                    break;
                };
            }
        }

        //Data loaded and uncompressed. Copy it to destination
        memcpy(bufferToRead, fBuffer.data()+fTable.bytes_per_row*(fCurrentRow%fNumRowsPerTile), fTable.bytes_per_row);
        return good();
    }

    // Read a bunch of uncompressed data
    uint32_t ZIFits::UncompressUNCOMPRESSED(char*       dest,
                                           const char* src,
                                           uint32_t    numElems,
                                           uint32_t    sizeOfElems)
    {
        memcpy(dest, src, numElems*sizeOfElems);
        return numElems*sizeOfElems;
    }

    // Read a bunch of data compressed with the Huffman algorithm
    uint32_t ZIFits::UncompressHUFFMAN16(char*       dest,
                                        const char* src,
                                        uint32_t    numChunks)
    {
        std::vector<uint16_t> uncompressed;

        //read compressed sizes (one per row)
        const uint32_t* compressedSizes = reinterpret_cast<const uint32_t*>(src);
        src += sizeof(uint32_t)*numChunks;

        //uncompress the rows, one by one
        uint32_t sizeWritten = 0;
        for (uint32_t j=0;j<numChunks;j++)
        {
            Huffman::Decode(reinterpret_cast<const unsigned char*>(src), compressedSizes[j], uncompressed);

            memcpy(dest, uncompressed.data(), uncompressed.size()*sizeof(uint16_t));

            sizeWritten += uncompressed.size()*sizeof(uint16_t);
            dest        += uncompressed.size()*sizeof(uint16_t);
            src         += compressedSizes[j];
        }
        return sizeWritten;
    }

    // Apply the inverse transform of the integer smoothing
    uint32_t ZIFits::UnApplySMOOTHING(int16_t*   data,
                                     uint32_t   numElems)
    {
        //un-do the integer smoothing
        for (uint32_t j=2;j<numElems;j++)
            data[j] = data[j] + (data[j-1]+data[j-2])/2;

        return numElems*sizeof(uint16_t);
    }

    // Data has been read from disk. Uncompress it !
    void ZIFits::UncompressBuffer(const uint32_t &catalogCurrentRow,
                                 const uint32_t &thisRoundNumRows,
                                 const uint32_t offset)
    {
        char *dest = fTransposedBuffer.data();

        //uncompress column by column
        for (uint32_t i=0; i<fTable.sorted_cols.size(); i++)
        {
            const IFits::Table::Column &col = fTable.sorted_cols[i];
            if (col.num == 0)
                continue;

            //get the compression flag
            const int64_t compressedOffset = fTileOffsets[catalogCurrentRow][i]+offset;

            const FITS::BlockHeader* head = reinterpret_cast<FITS::BlockHeader*>(&fCompressedBuffer[compressedOffset]);

            fColumnOrdering[i] = head->ordering;

            const uint32_t numRows = (head->ordering==FITS::kOrderByRow) ? thisRoundNumRows : col.num;
            const uint32_t numCols = (head->ordering==FITS::kOrderByCol) ? thisRoundNumRows : col.num;

            const char *src = fCompressedBuffer.data()+compressedOffset+sizeof(FITS::BlockHeader)+sizeof(uint16_t)*head->numProcs;

            for (int32_t j=head->numProcs-1;j >= 0; j--)
            {
                uint32_t sizeWritten=0;

                switch (head->processings[j])
                {
                case FITS::kFactRaw:
                    sizeWritten = UncompressUNCOMPRESSED(dest, src, numRows*numCols, col.size);
                    break;

                case FITS::kFactSmoothing:
                    sizeWritten = UnApplySMOOTHING(reinterpret_cast<int16_t*>(dest), numRows*numCols);
                    break;

                case FITS::kFactHuffman16:
                    sizeWritten = UncompressHUFFMAN16(dest, src, numRows);
                    break;

                default:
                    clear(rdstate()|std::ios::badbit);

                    std::ostringstream str;
                    str << "Unkown processing applied to data. Col " << i << " proc " << j << " out of " << (int)head->numProcs;
                    throw std::runtime_error(str.str());
                }
                //increment destination counter only when processing done.
                if (j==0)
                    dest+= sizeWritten;
            }
        }
    }

    void ZIFits::CheckIfFileIsConsistent(bool update_catalog)
    {
        //goto start of heap
        std::streamoff whereAreWe = tellg();
        seekg(fHeapOff);

        //init number of rows to zero
        uint64_t numRows = 0;

        //get number of columns from header
        size_t numCols = fTable.num_cols;

        std::vector<std::vector<std::pair<int64_t, int64_t> > > catalog;

        FITS::TileHeader  tileHead;
        FITS::BlockHeader columnHead;

        std::streamoff offsetInHeap = 0;
        //skip through the heap
        while (true)
        {
            read((char*)(&tileHead), sizeof(FITS::TileHeader));
            //end of file
            if (!good())
            {
//                std::cout << "Stream not good while reading a Tile header in file " << std::endl;
                break;
            }
            //padding or corrupt data
            if (memcmp(tileHead.id, "TILE", 4))
            {
                clear(rdstate()|std::ios::badbit);
                break;
            }

            //a new tile begins here
            catalog.emplace_back(std::vector<std::pair<int64_t, int64_t> >(0));
            offsetInHeap += sizeof(FITS::TileHeader);

            //skip through the columns
            for (size_t i=0;i<numCols;i++)
            {
                //zero sized column do not have headers. Skip it
//                if (fTable.sorted_cols[i].num == 0)
//                {
//                    std::cout << "Column " << i << " has size zero..." << std::endl;
//                    catalog.back().emplace_back(0,0);
//                    continue;
//                }

                //read column header
                read((char*)(&columnHead), sizeof(FITS::BlockHeader));

                //corrupted tile
                if (!good())
                {
                    std::cout << "Tile is corrupt right after column " << i << " while " << numCols << " were expected" << std::endl;
                    break;
                }
                catalog.back().emplace_back((int64_t)(columnHead.size),offsetInHeap);
                offsetInHeap += columnHead.size;
                //std::cout << "Size size seems to be " << columnHead.size << std::endl;
                seekg(fHeapOff+offsetInHeap);
            }

            //if we ain't good, this means that something went wrong inside the current tile.
            if (!good())
            {
                catalog.pop_back();
                break;
            }
            //current tile is complete. Add rows
            numRows += tileHead.numRows;
        }

        if (numRows != fTable.num_rows)
        {
            clear(rdstate()|std::ios::badbit);
            std::ostringstream str;
            str << "Heap data does not agree with header: " << numRows << " calculated vs " << fTable.num_rows << " from header.";
                    throw std::runtime_error(str.str());
        }

        if (update_catalog)
        {
            fCatalog = catalog;
            //clear the bad bit before seeking back (we hit eof)
            clear();
            seekg(whereAreWe);
            return;
        }

        if (catalog.size() != fCatalog.size())
        {
                    clear(rdstate()|std::ios::badbit);
                    throw std::runtime_error("Heap data does not agree with header.");
        }

        for (uint32_t i=0;i<catalog.size(); i++)
            for (uint32_t j=0;j<numCols;j++)
            {
                if (catalog[i][j].first  != fCatalog[i][j].first ||
                    catalog[i][j].second != fCatalog[i][j].second)
                {
                    clear(rdstate()|std::ios::badbit);
                    throw std::runtime_error("Heap data does not agree with header.");
                }
            }
        //go back to start of heap
        //clear the bad bit before seeking back (we hit eof)
        clear();
        seekg(whereAreWe);
    }
