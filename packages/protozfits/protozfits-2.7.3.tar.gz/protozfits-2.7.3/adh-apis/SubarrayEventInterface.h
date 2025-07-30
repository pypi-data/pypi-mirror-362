/**
 * @file SubarrayEventIterface.h
 * 
 * @brief Abstraction of the interface between the Software Array Trigger and Science Alert Generator 
 */

#include <cstddef>
#include <vector>
#include <cstdint>

/**
 * @namespace CTA
 * 
 * @brief top level namespace in CTA
*/
namespace CTA{
    /**
     * @namespace CTA_DL0
     * 
     * @brief Contains everything specific to DL0 data model
     */
    namespace CTA_DL0
    {
        /**
         * @class AbstractSubarrayEvent
         * 
         * @brief Abstract definition of DL0/Event/Subarray data structure
         * 
         * Needs to facilitate sharing messages containing the following data:
         * - a uint64_t event ID assigned by the Subarray Trigger
         * - a list of uint16_t IDs of Telescopes that paricipate in the Subarray Event
         * - a list of uint64_t IDs of Triggers that form the Subarray Event
         */
        class AbstractSubarrayEvent
        {
        public:
            /**
             * @brief Default constructor
             */
            AbstractSubarrayEvent() {};
            /**
             * @brief Copy constructor
             */
            AbstractSubarrayEvent(const AbstractSubarrayEvent& ){};
            /**
             * @brief Destructor
             */
            virtual ~AbstractSubarrayEvent() {};
            /**
             * @brief Copy assignment operator
             */
            virtual AbstractSubarrayEvent & operator=(const AbstractSubarrayEvent& ) = 0;
            
            /**
             * @brief Getter: the event ID assigned by the Subarray Trigger
             */            
            virtual uint64_t & getEventId() = 0;
            /**
             * @brief Getter: the list of IDs of all Telescopes that have triggers associated with the Subarray Event
             */  
            virtual std::vector<uint16_t>& getTelIdWithTriggerVector() = 0;
            /**
             * @brief Getter: the list of IDs of Telescopes that have event data associated with the Subarray Event
             */
            virtual std::vector<uint16_t>& getTelIdWithDataVector() = 0;
            /**
             * @brief Getter: the list of IDs of Triggers that form the Subarray Event
             */  
            virtual std::vector<uint64_t>& getTriggerIdVector() = 0;

            /**
             * @brief Getter (const): the event ID assigned by the Subarray Trigger
             */
            virtual uint64_t getEventId() const = 0;
            /**
             * @brief Getter (const): the list of IDs of all Telescopes that have triggers associated with the Subarray Event
             */
            virtual const std::vector<uint16_t>& getTelIdWithTriggerVector() const = 0;
            /**
             * @brief Getter (const): the list of IDs of Telescopes that have event data associated with the Subarray Event
             */
            virtual const std::vector<uint16_t>& getTelIdWithDataVector() const = 0;
            /**
             * @brief Getter (const): the list of IDs of Triggers that form the Subarray Event
             */
            virtual const std::vector<uint64_t>& getTriggerIdVector() const = 0;

            /**
             * @brief Setter: the event ID assigned by the subarray trigger
             */
            virtual void setEventId(uint64_t id) = 0;
            /**
             * @brief Setter: the list of IDs of all Telescopes that have triggers associated with the Subarray Event
             */
            virtual void setTelIdWithTriggerVector(const std::vector<uint16_t>& tel_ids) = 0;
            /**
             * @brief Setter: the list of IDs of Telescopes that have event data associated with the Subarray Event
             */
            virtual void setTelIdWithDataVector(const std::vector<uint16_t>& tel_ids) = 0;
            /**
             * @brief Setter: the list of IDs of Triggers that form the Subarray Event
             */
            virtual void setTriggerIdVector(const std::vector<uint64_t>& trigger_ids) = 0;

            /**
             * @brief Parse a buffer & populate values stored in the object
             * 
             * @param message The buffer to be parsed
             * @param message_size Size of the buffer
             * 
             * @return The length of the data parsed if successful; 0 if parsing failed
             */
            virtual size_t fromMessage(const char * message, size_t message_size) = 0;
            /**
             * @brief Serialize the message stored in the object into a buffer
             * 
             * @param message The buffer to write to
             * @param message_size Size of the buffer
             * 
             * @return The length of the data written if successful; 0 if serialization failed
             */
            virtual size_t toMessage(char * message, size_t buffer_size) const = 0;
            /**
             * @brief Get the size of the message that contains the currently stored data
             */
            virtual size_t getSize() const = 0;
        };
    }

    /**
     * Communication & session management is expected to be implemented using
     * the AbstractCherenkovDataStream interface (R1CherenkovDataInterface.h:350)
     * or an analogous approach, if unexpected implementation issues arise.
     */
}
