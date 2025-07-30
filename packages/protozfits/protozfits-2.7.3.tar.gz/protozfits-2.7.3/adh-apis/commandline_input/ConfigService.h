#ifndef CONFIG_SERVICE_HH
#define CONFIG_SERVICE_HH

#include <string>
#include <map>
#include <vector>

#include "Config.h"


namespace ADH {
namespace Conf {


/**
 * @file ConfigService.h
 * @brief Main configuration class
 * @class ConfigService
 * @brief This is the main configuration class, derived class from Config Base Class. It reads configuration
 * variables from one std::vector<string> (generally std::vector<argv[*]>)
 *
*/
class ConfigService : public Config
{
  public:

    /**
    * @brief default constructor: 
     * Command line constructor. Defines how the arguments will be
     * parsed.
     * \param message - The message to be used in the usage
     * output.
     * \param version - The version number to be used in the
     * --version switch.
     **/
    ConfigService(const std::string& message="Not defined",
        const std::string& version = "none");
					    

    ~ConfigService() ; 

    ConfigService(const ConfigService& source) 
    :Config(source), _prog_name(source._prog_name),
		     _relative_path(source._relative_path),
                     _message(source._message),
      		     _version(source._version),
                     _help_flag(source._help_flag)  {;};

    /**
     * Parses the command line arguments.
     * \param argc - Number of arguments.
     * \param argv - Array of arguments.
     */
    bool parseArgument(int argc, const char * const * argv);

    /**
     * Parses the command line arguments.
     * \param args - A vector of strings representing the args.
     * args[0] is the program name.
     */
    bool parseArgument(std::vector<std::string>& args);

    /**
     * Return command line program name.
     */
    inline std::string getProgramName() const
    {
      return _prog_name;
    }
    /**
     * Return program name's relative path.
     */
    inline std::string getRelativePath() const
    {
      return _relative_path;
    }
    /**
     * Return version.
     */
    inline std::string getVersion() const
    {
      return _version;
    }

    /**
     * Return string represtentaion of usage.
     */
    inline std::string getMessage() const
    {
      return _message;
    }

    /**
     * Return bool for help activation
     */
    inline bool helpIsActivate() const
    {
      return _help_flag;
    }

    /**
     * Parse a file and store readed variables  
     * Return true if parse pass
     */
    bool parseFile(const std::string& full_path_name);

    /**
     * Write configuration variables to a file 
     */
    bool writeFile(const std::string& full_path_name)const ;

    /**
     *  Defines what is an acceptable argument.
     */
    void addPossibleArg(const std::string& arg);

    /**
     *  Add acceptable arg as required and defines it as first prefix-less argument
     */
    void addDefaultArg(const std::string& arg);

    /**
     *  Add acceptable arg and defines its default value
     */
    void setDefaultValue(const std::string& key, const std::string& value);


  private:
    /**
     * The name of the program.  Set to argv[0].
     */
    std::string _prog_name;

    /**
     * The relative path of the program. Set form argv[0] without program name
     */
    std::string _relative_path;

    /**
     * A message used to describe the program.  Used in the usage output.
     */
    std::string _message;

    /**
     * The version to be displayed with the --version switch.
     */
    std::string _version;

    /**
     * The flag that indicated is help is active or not
     */
    bool _help_flag;

    /**
     * List of arguments that can be passed without prefix
     */
     std::vector<std::string> _default_args;


     std::vector<std::pair<std::string, std::string>> _default_values;

     bool isArgValue(const std::string& arg);

     bool isKeyPossible(const std::string& arg);


  
    
};

    /**
     * end class ConfigService
     */

}; // end namesapce Conf
}; // end namespace ADH


#endif
