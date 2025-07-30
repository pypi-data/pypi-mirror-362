/**
 *
 * @file Huffman.cpp
 *
 * @brief 16-bits Huffman encoder
 *
 * Author: lyard-bretz
 *
 */

#include "Huffman.h"

#include <vector>

namespace Huffman
{
    unsigned long numbytes_from_numbits(unsigned long numbits)
    {
        return numbits / 8 + (numbits % 8 ? 1 : 0);
    }

    unsigned long long start_time = 0;
    unsigned long long end_time   = 0;
    unsigned long long total_time = 0;
    unsigned long long total_measures = 0;
    unsigned long long min_time = 100000000;
    unsigned long long max_time = 0;

    std::vector<unsigned long long> recorded_values;

    unsigned long long getTimeUSec()
    {
        struct timeval now;
        gettimeofday(&now, NULL);
        return ((unsigned long long) now.tv_sec*1000000)+now.tv_usec;
    }

    void startProfile()
    {
        start_time = getTimeUSec();
    }

    void endProfile()
    {
        end_time = getTimeUSec();
        unsigned long long this_time = end_time - start_time;
   //     recorded_values.push_back(this_time);

        total_time += this_time;
        total_measures++;

        if (min_time > this_time)
        {
            min_time = this_time;
        }
        if (max_time < this_time)
        {
            max_time = this_time;
        }
    }

    void printProfileStats()
    {
        if (total_time != 0)
           std::cout << "Total time being profiled: " << total_time/(1000000.f) << " secs, tot. measuers=" << total_measures << " (avg per measure=" << total_time/total_measures << "usecs)" << std::endl;
        std::cout << "Min=" << min_time << " Max=" << max_time << std::endl;

     //   std::sort(recorded_values.begin(), recorded_values.end());
     // //  cout << "Median value is approx: " << recorded_values[recorded_values.size()/2] << endl;
       // for (auto it=recorded_values.begin(); it!=recorded_values.end(); it++)
       //     cout << *it << endl;
    }


        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        TreeNode::TreeNode(uint16_t sym, size_t cnt) : parent(0), isLeaf(true)
        {
            symbol = sym;
            count  = cnt;
        }

        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        TreeNode::TreeNode(TreeNode *n0, TreeNode *n1) : parent(0), isLeaf(false)
        {
            count = n0 && n1 ?  n0->count + n1->count : 0;
            zero  = n0 && n1 ? (n0->count > n1->count ? n0 : n1) : NULL;
            one   = n0 && n1 ? (n0->count > n1->count ? n1 : n0) : NULL;

            if (n0)
                n0->parent = this;

            if (n1)
                n1->parent = this;
        }

        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        TreeNode::~TreeNode()
        {
            if (isLeaf)
                return;

            if (zero)
                delete zero;
            if (one)
                delete one;
        }

        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        bool TreeNode::operator() (const TreeNode *hn1, const TreeNode *hn2) const
        {
            return hn1->count < hn2->count;
        }

        Encoder::Encoder() {}
        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        bool Encoder::CreateEncoder(const TreeNode *n, size_t bits, uint8_t nbits)
        {
            if (n->isLeaf)
            {
                if (nbits>sizeof(size_t)*8)
                    throw std::runtime_error("Too many different symbols - this should not happen!");

                lut[n->symbol].bits    = bits;
                lut[n->symbol].numbits = nbits==0 ? 1 : nbits;
                count++;
                return true;
            }

            return
                CreateEncoder(n->zero, bits,              nbits+1) &&
                CreateEncoder(n->one,  bits | (1<<nbits), nbits+1);

        }

        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        void Encoder::WriteCodeTable(std::string &out) const
        {
            out.append((char*)&count, sizeof(size_t));

            for (uint32_t i=0; i<MAX_SYMBOLS; i++)
            {
                const Code &n = lut[i];
                if (n.numbits==0)
                    continue;

                // Write the 1 or 2 byte symbol.
                out.append((char*)&i, sizeof(uint16_t));

#ifdef SINGLE_CASE
                if (count==1)
                {
                    return;
                }
#endif
                // Write the 1 byte code bit length.
                out.append((char*)&n.numbits, sizeof(uint8_t));

                // Write the code bytes.
                uint32_t numbytes = numbytes_from_numbits(n.numbits);
                out.append((char*)&n.bits, numbytes);
            }
        }

        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        void Encoder::Encode(std::string &out, const uint16_t *bufin, size_t bufinlen) const
        {

#ifdef SINGLE_CASE
            if (count==1)
            {
                return;
            }
#endif
            uint8_t curbyte = 0;
            uint8_t curbit  = 0;

            for (uint32_t i=0; i<bufinlen; ++i)
            {
                const uint16_t &symbol = bufin[i];

                const Code *code = lut+symbol;

                uint8_t nbits = code->numbits;
                const uint8_t *bits = (uint8_t*)&code->bits;

                while (nbits>0)
                {
                    // Number of bits available in the current byte
                    const uint8_t free_bits = 8 - curbit;

                    // Write bits to current byte
                    curbyte |= *bits<<curbit;

                    // If the byte has been filled, put it into the output buffer
                    // If the bits exceed the current byte step to the next byte
                    // and fill it properly
                    if (nbits>=free_bits)
                    {
                        out += curbyte;
                        curbyte = *bits>>free_bits;

                        bits++;
                    }

                    // Adapt the number of available bits, the number of consumed bits
                    // and the bit-pointer accordingly
                    const uint8_t consumed = nbits>8 ? 8 : nbits;
                    nbits  -= consumed;
                    curbit += consumed;
                    curbit %= 8;
                }
            }

            // If the buffer-byte is half-full, also add it to the output buffer
            if (curbit>0)
                out += curbyte;
        }

        Encoder::Encoder(const uint16_t *bufin, size_t bufinlen)
        {
            initialize(bufin, bufinlen);
        }

        void Encoder::initialize(const uint16_t *bufin, size_t bufinlen)
        {
        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/

 //           std::cout << this << std::endl;
            count = 0;
            uint64_t counts[MAX_SYMBOLS];
            memset(counts, 0, sizeof(uint64_t)*MAX_SYMBOLS);

            // Count occurances
            for (const uint16_t *p=bufin; p<bufin+bufinlen; p++)
                counts[*p]++;

            // Copy all occuring symbols into a sorted list
            std::multiset<TreeNode*, TreeNode> set;
            for (int i=0; i<MAX_SYMBOLS; i++)
                if (counts[i])
                    set.insert(new TreeNode(i, counts[i]));

            // Create the tree bottom-up
            while (set.size()>1)
            {
                auto it = set.begin();

                auto it1 = it++;
                auto it2 = it;

                TreeNode *nn = new TreeNode(*it1, *it2);

                set.erase(it1, ++it2);

                set.insert(nn);
            }

            // get the root of the tree
            const TreeNode *root = *set.begin();

        //CLANG TODO Here I initialize data after it was created explicitely
            for (int i=0;i<MAX_SYMBOLS;i++)
                lut[i].numbits = 0;

            CreateEncoder(root);

            // This will delete the whole tree
            delete root;
        }

        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        Decoder::Decoder() : isLeaf(false), lut(NULL)
        {
        }

        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        Decoder::~Decoder()
        {
            if (lut)
                delete [] lut;
        }

        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        void Decoder::Set(uint16_t sym, uint8_t n, size_t bits)
        {

            //allocate data space if not existing yet
            if (!lut)
                lut = new Decoder[256];

            //if this is not the final stage, do it again for the remaining bits, and that's it
            if (n>8)
            {
                lut[bits&0xff].Set(sym, n-8, bits>>8);
                return;
            }

            //if we're here, this is a leaf of max. 8 bits (i.e. n<=8)
            const int nn = 1<<(8-n);

            //here it is set all 8-bits entries which contain the remaining code (of less than 8 bits)
            for (int i=0; i<nn; i++)
            {
                const uint8_t key = bits | (i<<n);
                lut[key].symbol = sym;
                lut[key].isLeaf = true;
                lut[key].nbits  = n;
            }
        }

        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        void Decoder::Build(const TreeNode &p, uint64_t bits, uint8_t n)
        {
            if (p.isLeaf)
            {
                Set(p.symbol, n, bits);
                return;
            }

            Build(*p.zero, bits,          n+1);
            Build(*p.one,  bits | (1<<n), n+1);
        }

        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        Decoder::Decoder(const TreeNode &p) : symbol(0), isLeaf(false), lut(NULL)
        {
            Build(p);
        }


        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        const uint8_t* Decoder::Decode(const uint8_t* in_ptr,
                              const uint8_t* in_end,
                              uint16_t*            out_ptr,
                              const uint16_t*      out_end) const
        {
            Decoder const *p = this;

            //if we have only one input symbol, fill up the output with it

#ifdef SINGLE_CASE

            if (in_ptr==in_end)
            {
                while (out_ptr < out_end)
                    *out_ptr++ = p->lut->symbol;
                return in_ptr;
            }
#endif

//start_time = getTimeUSec();
            //otherwise, until we exhaust the input bits, or fill up the output bytes
            uint8_t curbit = 0;
            while (in_ptr<in_end && out_ptr<out_end)
            {
                //look at the current input byte. Take a two-bytes word as input to make sure that we can extract a full byte
                const uint16_t *two = (uint16_t*)in_ptr;

               // if (curbit >= 8) std::cout << "curbit: " << curbit << std::endl;
                //figure out what bits we are decoding exactly
                //std::cout << "Using shift mapping: " << (int)(curbit) << " " << (int)(*two) << std::endl;
 //               if (curbit > 7) std::cout << "Curbit = " << (int)(curbit) << std::endl;
 //               if (*two > 65530) std::cout << "two = " << (int)(*two) << std::endl;

                const uint8_t curbyte =  (*two >> curbit);//shift_mapping[curbit][*two];//

                //if we end up nowhere, there is a problem with the encoding
                if (!p->lut)
                    throw std::runtime_error("Unknown bitcode in stream!");

                //otherwise, traverse the graph of symbols following the new input set of bits (curbyte)
                p = p->lut + curbyte;

                //if we are not at a leaf yet, continue to traverse
                if (!p->isLeaf)
                {
                    in_ptr++;
                    continue;
                }

                //if we've hit a leaf, assign the symbol to the output, and consume the corresponding bits
                *out_ptr++ = p->symbol;
                curbit    += p->nbits;

                //and start over from the root of the graph (this)
                p = this;

                if (curbit>=8)
                {
                    curbit %= 8;
                    in_ptr++;

                }
            }
//end_time = getTimeUSec();
//total_time += end_time - start_time;
//total_measures++;

            return curbit ? in_ptr+1 : in_ptr;
        }

        /*---------------------------------------------------
         *---------------------------------------------------
         *--------------------------------------------------*/
        Decoder::Decoder(const uint8_t* bufin, int64_t &pindex) : isLeaf(false), lut(NULL)
        {
            // FIXME: Sanity check for size missing....

            // Read the number of entries.
            size_t count=0;
            memcpy(&count, bufin + pindex, sizeof(count));
            pindex += sizeof(count);

            // Read the entries.
            for (size_t i=0; i<count; i++)
            {
                uint16_t sym;
                memcpy(&sym, bufin + pindex, sizeof(uint16_t));
                pindex += sizeof(uint16_t);

//THIS HAS BEEN COMMENTED
#ifdef SINGLE_CASE
                if (count==1)
                {
                    Set(sym);
                    break;
                }
#endif
                uint8_t numbits;
                memcpy(&numbits, bufin + pindex, sizeof(uint8_t));
                pindex += sizeof(uint8_t);

                const uint8_t numbytes = numbytes_from_numbits(numbits);

                if (numbytes>sizeof(size_t))
                    throw std::runtime_error("Number of bytes for a single symbol exceeds maximum.");

                size_t bits=0;
                memcpy(&bits, bufin+pindex, numbytes);
                pindex += numbytes;

                Set(sym, numbits, bits);
            }
        }

/********************************************************************************
 ********************************************************************************
 ********************************************************************************/
    bool Encode(std::string &bufout, const uint16_t *bufin, size_t bufinlen)
    {
        Encoder encoder;//(bufin, bufinlen);
        encoder.initialize(bufin, bufinlen);
        bufout.append((char*)&bufinlen, sizeof(size_t));
        encoder.WriteCodeTable(bufout);
        encoder.Encode(bufout, bufin, bufinlen);

        return true;
    }

/********************************************************************************
 ********************************************************************************
 ********************************************************************************/
    int64_t Decode(const uint8_t *bufin,
                   size_t         bufinlen,
                   std::vector<uint16_t> &pbufout)
    {
        int64_t i = 0;

        // Read the number of data bytes this encoding represents.
        size_t data_count = 0;
        memcpy(&data_count, bufin, sizeof(size_t));
        i += sizeof(size_t);

        pbufout.resize(data_count);

        const Decoder decoder(bufin, i);

        const uint8_t *in_ptr =
            decoder.Decode(bufin+i, bufin+bufinlen,
                           pbufout.data(), pbufout.data()+data_count);

        return in_ptr-bufin;
    }
};
