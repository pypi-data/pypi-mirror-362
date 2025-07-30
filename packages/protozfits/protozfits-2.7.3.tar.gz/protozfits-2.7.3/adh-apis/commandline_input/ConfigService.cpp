#include "ConfigService.h" 
#include <stdexcept>

#include <stdexcept>  
#include <fstream>
#include <algorithm>
#include <vector>
#include <chrono>
#include <ctime>
#include <iostream>
#include <string>
#include <cctype>
#include <cwctype>
#include <stdexcept>

using namespace std;

namespace ADH
{
namespace Conf 
{


/**
 * @file ConfigService.cpp
 * @brief Main configuration class
 *
*/

/*---------------------------------------------------------------------------*/
ConfigService::ConfigService(const std::string& m,
                        const std::string& v) 
   : _prog_name("none"), _message(m), _version(v), _help_flag(false) 
{
//	INFO << "VERSION:"  << _version <<std::endl; ;
}

/*---------------------------------------------------------------------------*/
ConfigService::~ConfigService() 
{
}

/*---------------------------------------------------------------------------*/
/* Parse config file and store entries to Config
 * return:
 *   -true if args are parsed without error
 *   -false in other cases
 *   example:
 *  prompt#> pipe --key value
 */
bool ConfigService::parseArgument(int argc, const char * const * argv)
{
   // this step is necessary so that we have easy access to
    // mutable strings.
    std::vector<std::string> args;
    for (int i = 0; i < argc; i++)
      args.push_back(argv[i]);

    if ( args.size() > 0 ) return parseArgument(args);
    return false;
}

//tells whether the string starts with - or --
bool ConfigService::isArgValue(const std::string& arg)
{

    if (arg.find("-") == 0) return false;
    return true;
}

void ConfigService::addPossibleArg(const std::string& arg)
{
    _possible_args.push_back(arg);
}

void ConfigService::addDefaultArg(const std::string& arg)
{
    addRequired(arg);
    _possible_args.push_back(arg);
    _default_args.push_back(arg);
}

void ConfigService::setDefaultValue(const std::string& key, const std::string& value)
{
    _possible_args.push_back(key);
    _default_values.push_back(std::make_pair(key, value));
}

bool ConfigService::isKeyPossible(const std::string& key)
{
    if (_possible_args.size() == 0)
    {
        cout << "Warning: impossible to verify that parameter "+key+" is expected as possible arguments were not defined" << endl;
        return true;
    }


    for (auto it=_possible_args.begin(); it!= _possible_args.end(); it++)
        if (*it == key)
            return true;

    cout << "ERROR: Unknown parameter: " << key << endl << "Possible args are: ";
    for (auto it=_possible_args.begin(); it!= _possible_args.end();it++)
        cout << *it << ",";
    cout << endl;

    return false;
}

/*---------------------------------------------------------------------------*/
/* Parse config file and store entries to Config
 * return:
 *   -true if args are parsed without error
 *   -false in other cases
 *  Format:
 *  1/ key/value paira:  prompt#> pipe --key value
 *  2/ boleean. true if flag present:  prompt#> pipe --split (or -s)
 *
 */
bool ConfigService::parseArgument(std::vector<std::string>& args)
{
  if ( args.size() <= 1 )
  {
//    std::cout << yellow << "ConfigService: no argument to parse." << no_color << std::endl;
    std::cout << this->getMessage() << std::endl;
 //   return true;
//    exit(0);
  }
  _prog_name = args.front();
  size_t last_slash_pos = _prog_name.find_last_of("/");
  if (last_slash_pos !=  std::string::npos)
    { _relative_path = _prog_name.substr(0,last_slash_pos); }

  args.erase(args.begin()); 

  //now insert default arguments values if head-less arguments were passed
  std::vector<std::string> upgraded_args;
  unsigned int ii=0;
  for (; ii<args.size();ii++)
  {
    //stop as soon as we find a real argument header
    if (!isArgValue(args[ii]))
        break;

    //stop if no more default arguments were provided
    if (_default_args.size() <= ii)
        break;

    upgraded_args.push_back("--"+_default_args[ii]);
    upgraded_args.push_back(args[ii]);
  }

  for (unsigned int j=ii;j<args.size();j++)
    upgraded_args.push_back(args[j]);


  args = upgraded_args;

//  for (int i=0;i<args.size(); i++)
//  cout << args[i] << " ";
//  cout << endl;

  for (int i = 0; static_cast<unsigned int>(i) < args.size(); i++)
  {
    std::string entry;
    std::string key;
    std::string value;
    std::string next_entry;

    try 
    { 
      entry = args.at(i);
      if ( entry.find("--") == std::string::npos 
        && entry.find("-")  == 0)//std::string::npos  )
      {
        if (entry.size() > 2) 
          throw std::runtime_error("flag after a single  minus must be a letter, not a word");
      }

      if ( entry.find("--") == std::string::npos
       &&  entry.find("-")==std::string::npos)
      { // we expect a '--' or '-' caracters
        throw std::runtime_error("ConfingArgs: missing minus character \"-\" or \"--\" before flag") ;
        continue;
      }

        if (static_cast<unsigned int>(i)+1 >= args.size())
        {// No value for this key. So current key is a boolean flag
          key=trimKey(entry);
          if (!isKeyPossible(key)) return false;
          value = "1";
          this->add(DEFAULT_SECTION,key,value);
          continue;
        }
        else 
        { 
          next_entry = args.at(i+1);
          if ( next_entry.find("--")== 0//std::string::npos
            || next_entry.find("-")== 0)//std::string::npos)
          {  // next entry is a key not a value. So current is a boolean flag
            key=trimKey(entry);
            if (!isKeyPossible(key)) return false;
            value = "1";
            this->add(DEFAULT_SECTION,key,value);
            continue;
          }
          else
          { // next entry is a value. So current is key/value pair
            key=trimKey(entry);
            if (!isKeyPossible(key)) return false;
            value = next_entry;
            i++; // Do not process value at next loop
            this->add(DEFAULT_SECTION,key,value);
          }
        }
    }
    catch (const std::out_of_range& oor) 
    {
    }
  }
  // set _help_flag
  if ( this->has("h")== true ) {  _help_flag = true; } 
  if ( this->has("help")== true ) {  _help_flag = true; } 

  if ( _help_flag == true ) 
  {
    std::cout << this->getMessage() << std::endl;
    exit(0);
  }

  if ( this->has("v") == true ) 
    { std::cout << green << this->getProgramName() << " version "
      << this->getVersion() << no_color << std::endl;
      exit(0); }

  std::string required = "";

  if ( this->has("c")== true ) 
  { 
    required = this->get<std::string>("c");
  }
  if ( this->has("check_version")== true ) 
  { 
    required = this->get<std::string>("check_version");
  }

  if ( required.size() > 0 )
  {
    if (required.compare(this->getVersion()) != 0) 
    {
      std::cout << yellow << "Current version: " << this->getVersion() << " differ from required one:"
            << required << "." << no_color << std::endl;
      return false;
    } 
      
  }

//set default values if not already set
for (auto it=_default_values.begin(); it!=_default_values.end(); it++)
{
    if (!has(it->first))
        add(it->first, it->second);
}

return checkRequiredParams();
//return true;
}

/*---------------------------------------------------------------------------*/
/* Parse config file and store entries
 * return:
 *   -true if config file is correctly parsed
 *   -false in other cases
 */
bool ConfigService::parseFile(const std::string& full_path_name)
{
  std::ifstream file(full_path_name.c_str())   ;
  if ( (file.rdstate() & std::ifstream::failbit ) != 0 )
  {
    std::cout << yellow << "Error opening configuration file [" << full_path_name << "]"
         << no_color << std::endl;
    return false;
  }

  std::string line;
  std::string name;
  std::string inSection;
  int posEqual;
   while (std::getline(file,line)) {
    // Do not process blank line without any character
    if (! line.length()) continue;

    // Do not process line if first non space character is a hash key
    if (trim(line)[0] == '#') continue;

    // If first non space character is a open square bracket
    if (trim(line)[0] == '[') {
      line = trim(line);
      std::string section_to_trim = line.substr(1,line.find(']')-1);
      inSection=trim(section_to_trim);
      continue;
    }
    // Do no process line if line does not contain equal character
    if (line.find("=") == std::string::npos) continue;

    posEqual=line.find('=');
    std::string name_to_trim = line.substr(0,posEqual);
    name  = trim(name_to_trim);
    std::string readed_value_to_trim = line.substr(posEqual+1);
    std::string readed_value = trim(readed_value_to_trim);
    std::string comment="";

    // Do not take in account character after dash (#)
    size_t dash_pos = readed_value.find("#");
    if (dash_pos != std::string::npos )
    {
      comment = readed_value.substr(dash_pos+1);
      readed_value = readed_value.substr(0,dash_pos);
    }
    if ( readed_value.size() == 0 ) {
      std::cout << yellow << inSection << ", " << name
        << " value is blank. Cannot add it to Conf" << no_color << std::endl;
      continue ;
    }
    this->add(inSection,name,readed_value,comment);
  } //end while
//  std::cout << yellow << "Reading configuration " << full_path_name <<" was successful."     << no_color << std::endl;
return true;
}

/*---------------------------------------------------------------------------*/
/* Write entries to config file 
 * return:
 *   -true if config file is correctly writed
 *   -false in other cases
 */
bool ConfigService::writeFile(const std::string& full_path_name)const
{
  std::filebuf fb;
//gcc4.1
  if (fb.open (full_path_name,std::ios::out) != NULL)
  //nullptr)
  {
    std::ostream os(&fb);
    std::time_t end_time
       = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());

    os << "# This file was automatically generated by ADH Framework "
        <<std::endl;
    os << "# "<< std::ctime(&end_time) <<std::endl;
//gcc4.1
    for (auto eentry=_entries.begin(); eentry!=_entries.end(); eentry++)
    {
        auto& entry = *eentry;
//    for ( auto& entry : _entries)
//    {
        os << "[" << entry.first << "]" << std::endl ;
        const std::map<std::string , Param>& perSectionMap
            = entry.second;
//gcc4.1
        for (auto pperSectionEntry=perSectionMap.begin(); pperSectionEntry!=perSectionMap.end(); pperSectionEntry++)
        {
            auto perSectionEntry = *pperSectionEntry;
//        for ( auto  perSectionEntry : perSectionMap)
//        {
            try {
            std::string value = perSectionEntry.second._value;
            std::string comment = perSectionEntry.second._comment;
            os <<   perSectionEntry.first << " = " << value ;
            if ( comment.size()>0) os << "#" << comment ;
            os <<  std::endl;
            }
            catch (...)
            {
                std::cout << yellow << "Cold not write section["<< entry.first << "], key["
                     << perSectionEntry.first 
                     << "] because it cannot be convert to std::String" 
                     << no_color << std::endl;
            }
        }
    }
    fb.close();
    std::cout << green << "Writing onfiguration " << full_path_name <<" was successful."
         << no_color << std::endl;
    return true;
  }
  else {
      std::cout << yellow << "ConfigService: Cound not open file for writting: "
      <<  full_path_name << no_color << std::endl;
  }
  return false;
}


}; // end namespace Conf
}; // end namespace ADH
