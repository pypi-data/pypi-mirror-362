#ifndef _MEMORY_MANAGER_H_
#define _MEMORY_MANAGER_H_
/**
 * @file MemoryManager.h
 *
 * @brief Fast and controlled memory allocation by allocating always the same block size and keeping track of them ourselves
 *
 * @author bretz-lyard
 */

#include <forward_list>
#include <condition_variable>


//If defined, allows modification of memory block sizes
//side effects include:
// ** May exceed max. allowed memory for a short while
// ** Slower than static, fixed-size allocation
#define AUTO_BLOCK_SIZE

class MemoryStock
{
    friend class MemoryChunk;
    friend class MemoryManager;

    size_t fChunkSize;
    size_t fMaxMemory;

    size_t fInUse;
    size_t fAllocated;

    size_t fMaxInUse;

    std::mutex fMutexMem;
    std::mutex fMutexCond;
    std::condition_variable fCond;

    std::forward_list<std::shared_ptr<char>> fMemoryStock;

public:
    MemoryStock(size_t chunk, size_t max);

private:
    std::shared_ptr<char> pop(bool block);

    void push(const std::shared_ptr<char> &mem);
};

class MemoryChunk
{
    friend class MemoryManager;

    std::shared_ptr<MemoryStock> fMemoryStock;
    std::shared_ptr<char>        fPointer;

    MemoryChunk(const std::shared_ptr<MemoryStock> &mem, bool block);

public:
    ~MemoryChunk();
};

class MemoryManager
{
    std::shared_ptr<MemoryStock> fMemoryStock;

public:
    MemoryManager(size_t chunk=1024, size_t max=10240);
    std::shared_ptr<char> malloc(bool block=true);

    size_t getChunkSize() const;
    bool   setChunkSize(const size_t size);

    size_t getMaxMemory() const;
    size_t getInUse() const;
    size_t getAllocated() const;
    size_t getMaxInUse() const;
    bool   freeAllMemory();
};

#endif
