/**
 * @file MemoryManager.cpp
 *
 * @brief Fast and controlled memory allocation by allocating always the same block size and keeping track of them ourselves
 *
 * @author bretz-lyard
 */

#include "MemoryManager.h"
#include <stdexcept>
#include <iostream>
    /************************************************************************************
     *
     ************************************************************************************/
    MemoryStock::MemoryStock(size_t chunk, size_t max) : fChunkSize(chunk), fMaxMemory(max<chunk?chunk:max),
        fInUse(0), fAllocated(0), fMaxInUse(0)
    {
    }

bool exceeded_memory = false;

    /************************************************************************************
     *
     ************************************************************************************/
    std::shared_ptr<char> MemoryStock::pop(bool block)
    {
        if (block)
        {
            // No free slot available, next alloc would exceed max memory:
            // block until a slot is available
            std::unique_lock<std::mutex> lock(fMutexCond);
            while (fMemoryStock.empty() && fAllocated+fChunkSize>fMaxMemory)
            {
                fCond.wait(lock);
            }
        }
        else
        {
            // No free slot available, next alloc would exceed max memory
            // return an empty pointer
            if (fMemoryStock.empty() && fAllocated+fChunkSize>fMaxMemory)
            {
                std::cout << "Returning an empty pointer..." << std::endl;
                return std::shared_ptr<char>();
            }
        }

        // Get the next free slot from the stack and return it
        const std::lock_guard<std::mutex> lock(fMutexMem);

        // We will return this amount of memory
        // This is not 100% thread safe, but it is not a super accurate measure anyway
        if (fInUse>fMaxInUse)
               fMaxInUse = fInUse;

        fInUse += fChunkSize;

#ifdef AUTO_BLOCK_SIZE
        fAllocated += fChunkSize;
        return std::shared_ptr<char>(new char[fChunkSize], std::default_delete<char[]>());
#else
        if (fMemoryStock.empty())
        {
            // No free slot available, allocate a new one
            fAllocated += fChunkSize;
            return std::shared_ptr<char>(new char[fChunkSize], std::default_delete<char[]>());
        }

        const auto mem = fMemoryStock.front();
        fMemoryStock.pop_front();

        return mem;
#endif

    };

    /************************************************************************************
     *
     ************************************************************************************/
    void MemoryStock::push(const std::shared_ptr<char> &mem)
    {
        if (!mem)
            return;

//in automatic allocation mode, always free a slot !
#ifdef AUTO_BLOCK_SIZE
        const std::lock_guard<std::mutex> lock(fMutexMem);
        //in this case fInUse == fAllocated is always true
        //and it may go below zero if the size of chunks was increase on-the-fly
        if (fInUse >= fChunkSize)
        {
            fInUse     -= fChunkSize;
            fAllocated -= fChunkSize;
        }
        else
        {
            fAllocated = 0;
            fInUse     = 0;
        }
        fCond.notify_one();
        return;
#endif
        // If the maximum memory has changed, we might be over the limit.
        // In this case: free a slot
        if (fAllocated>fMaxMemory)
        {
            const std::lock_guard<std::mutex> lock(fMutexMem);
            // Decrease the amont of memory in use accordingly
            fInUse -= fChunkSize;

            fAllocated -= fChunkSize;
            return;
        }
        else
        {
            const std::lock_guard<std::mutex> lock(fMutexMem);
            fMemoryStock.emplace_front(mem);

            // Decrease the amont of memory in use accordingly
            fInUse -= fChunkSize;
        }

        {
            const std::lock_guard<std::mutex> lock(fMutexCond);
            fCond.notify_one();
        }
    }

    /************************************************************************************
     *
     ************************************************************************************/
    MemoryChunk::MemoryChunk(const std::shared_ptr<MemoryStock> &mem, bool block)
        : fMemoryStock(mem)
    {
        fPointer = fMemoryStock->pop(block);
    }

    /************************************************************************************
     *
     ************************************************************************************/
    MemoryChunk::~MemoryChunk()
    {
        fMemoryStock->push(fPointer);
    }

    /************************************************************************************
     *
     ************************************************************************************/
    MemoryManager::MemoryManager(size_t chunk, size_t max) : fMemoryStock(std::make_shared<MemoryStock>(chunk, max))
    {
    }

    /************************************************************************************
     *
     ************************************************************************************/
    std::shared_ptr<char> MemoryManager::malloc(bool block)
    {
        const std::shared_ptr<MemoryChunk> chunk(new MemoryChunk(fMemoryStock, block));
        return std::shared_ptr<char>(chunk, chunk->fPointer.get());
    }

    /************************************************************************************
     *
     ************************************************************************************/
    size_t MemoryManager::getChunkSize() const
    {
        return fMemoryStock->fChunkSize;
    }

    /************************************************************************************
     *
     ************************************************************************************/
    bool   MemoryManager::setChunkSize(const size_t size)
    {
#ifndef AUTO_BLOCK_SIZE
    if (getInUse())
    {
            ostringstream str;
            str << yellow << "Compression blocks size is too small: " << fMemoryStock->fChunkSize << " Bytes vs " << size << " Bytes requested.\n";
            str << "Please use the method ProtobufZOFits::setCompressionBlockSize(uint32 size) to allocate more memory at startup (or appropriate option if used through ZFitsWriter\n";
            str << "Or even better:  enable the AUTO_BLOCK_SIZE option to let the software handle this.\n" << no_color;
            throw runtime_error(str.str());
    }
#endif
    if (getMaxMemory()<size)
            throw std::runtime_error("Chunk size ("+std::to_string((long long int)(size))+") larger than allowed memory ("+std::to_string((long long int)(getMaxMemory()))+")");

        fMemoryStock->fChunkSize = size;
        return true;
    }

    /************************************************************************************
     *
     ************************************************************************************/
    size_t MemoryManager::getMaxMemory() const
    {
        return fMemoryStock->fMaxMemory;
    }

    /************************************************************************************
     *
     ************************************************************************************/
    size_t MemoryManager::getInUse() const
    {
        return fMemoryStock->fInUse;
    }

    /************************************************************************************
     *
     ************************************************************************************/
    size_t MemoryManager::getAllocated() const
    {
        return fMemoryStock->fAllocated;
    }

    /************************************************************************************
     *
     ************************************************************************************/
    size_t MemoryManager::getMaxInUse() const
    {
        return fMemoryStock->fMaxInUse;
    }


    bool MemoryManager::freeAllMemory()
    {
        if (getInUse() != 0)
            return false;

        fMemoryStock->fMemoryStock.clear();
        fMemoryStock->fAllocated = 0;
        return true;
    }
