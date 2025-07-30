#ifndef CONFIG_HH
#define CONFIG_HH

#include <map>
#include <unordered_map>
#include <vector>
#include <list>
#include <set>
#include <string>
#include <memory>
#include <iostream>
#include <typeinfo>
#include <iomanip>
#include <stdexcept>
#include <sstream>
#include <type_traits>

//#include "BasicDefs.h"
#include "ColoredOutput.h"

using namespace ADH::ColoredOutput;

/** @file Config.h
 *  @brief Base configuration class
 *
 * @namespace ADH::Conf
 * @brief r/w configuration service from/to file/db ...
*/

namespace ADH {
namespace Conf {

struct Param {
    Param() = delete;
    Param(std::string value, std::string comment="")
    :_value(value), _comment(comment) {};
    std::string _value ;
    std::string _comment;
};

/* Insertion operator for std::list of fundamental type*/
std::ostream& operator << (std::ostream& out,std::list<std::string> l);
std::ostream& operator << (std::ostream& out,std::list<char> l) ;
std::ostream& operator << (std::ostream& out,std::list<char16_t> l) ;
std::ostream& operator << (std::ostream& out,std::list<char32_t> l) ;
std::ostream& operator << (std::ostream& out,std::list<wchar_t> l) ;
std::ostream& operator << (std::ostream& out,std::list<signed short int> l) ;
std::ostream& operator << (std::ostream& out,std::list<signed int> l) ;
std::ostream& operator << (std::ostream& out,std::list<signed long int> l) ;
std::ostream& operator <<(std::ostream& out,std::list<signed long long int>l) ;
std::ostream& operator << (std::ostream& out,std::list<unsigned short int> l) ;
std::ostream& operator << (std::ostream& out,std::list<unsigned int> l) ;
std::ostream& operator << (std::ostream& out,std::list<unsigned long int> l) ;
std::ostream& operator<<(std::ostream& out,std::list<unsigned long long int>l) ;
std::ostream& operator << (std::ostream& out,std::list<float> l) ;
std::ostream& operator << (std::ostream& out,std::list<double> l) ;
std::ostream& operator << (std::ostream& out,std::list<long double> l) ;
std::ostream& operator << (std::ostream& out,std::list<bool> l) ;

/* Insertion operator for std::vector of fundamental type*/
std::ostream& operator << (std::ostream& out,std::vector<std::string> l);
std::ostream& operator << (std::ostream& out,std::vector<char> l) ;
std::ostream& operator << (std::ostream& out,std::vector<char16_t> l) ;
std::ostream& operator << (std::ostream& out,std::vector<char32_t> l) ;
std::ostream& operator << (std::ostream& out,std::vector<wchar_t> l) ;
std::ostream& operator << (std::ostream& out,std::vector<signed short int> l) ;
std::ostream& operator << (std::ostream& out,std::vector<signed int> l) ;
std::ostream& operator << (std::ostream& out,std::vector<signed long int> l) ;
std::ostream& operator <<(std::ostream& out,std::vector<signed long long int>l) ;
std::ostream& operator << (std::ostream& out,std::vector<unsigned short int> l) ;
std::ostream& operator << (std::ostream& out,std::vector<unsigned int> l) ;
std::ostream& operator << (std::ostream& out,std::vector<unsigned long int> l) ;
std::ostream& operator<<(std::ostream& out,std::vector<unsigned long long int>l) ;
std::ostream& operator << (std::ostream& out,std::vector<float> l) ;
std::ostream& operator << (std::ostream& out,std::vector<double> l) ;
std::ostream& operator << (std::ostream& out,std::vector<long double> l) ;


#define DEFAULT_SECTION "DEFAULT_SECTION"
/*
 * @class Config
 * @brief Base class that holds configuration variables.
 * This class is abstract, therefore it cannot be instantiated. User code
 * has to instantiate one of its derived classes.
 *
 * Configuration variables are stored in a double level key-value dictionary:
 * - 1st key: configuration variable section
 * - 2nd key: configuration variable name
 * - value  : configuration variable value
 * 
*/
class Config
{
  public:

    /**
    * @brief default constructor: 
    * */ 
    Config() { ; } ;
    Config(const Config& source) :_required(source._required)
    { 
//gcc4.1
    for (auto eelem=source._entries.begin(); eelem!=source._entries.end();eelem++)
    {
        const auto& elem = *eelem;
//    for ( const auto& elem : source._entries)
//        {
          std::string section = elem.first;
          _entries[section] = elem.second;//std::copy_unique(elem.second);
        } 
    } ;
    virtual ~Config() ; 
 /**
 *       */
  class CastException : public std::runtime_error {
  public:
    CastException(std::string where, std::string what)
      : runtime_error((where+" --> "+what).c_str()){ ; }
  };

/*! 
 * add a configuration variable value <T> to a corresponding section/key
 * */
template< typename T>
    bool add(const std::string& section, const std::string& key ,T& value ) 
    {
      std::ostringstream converter; 
      converter << value;
      return this->add(section,key,converter.str());
    }

/*! 
 * add a configuration variable value <T> to the default section and 
 * corresponding key
 * */
template< typename T>
    bool add(const std::string& key ,T& value ) 
    {
      std::ostringstream converter; 
      converter << value;
      return this->add(DEFAULT_SECTION,key,converter.str());
    }
/*! 
 * add a configuration variable std::string value to a corresponding section/key
 * */
    bool add(const std::string& section,const  std::string& key,const std::string& value, std::string comment="" ) ;

/*
 * return true if Config contains a variable for this SECTION/KEY
 * Otherwise return false;
 */
  bool has(const std::string& section,const std::string& key) const
  {
    try {
      this->get<std::string>(section,key); 
      return true;
    }catch (const std::runtime_error& e ) { return false;}

    return true;
  }
/*
 * add a configuration variable for DEFAULT_SECTION/KEY to the required list
 * parseArguments  method will return false if this configuration variable
 * is missing
 */
  void addRequired(const std::string& key) 
  {
    this->addRequired(DEFAULT_SECTION,key);
  }

/*
 * add a configuration variable for section/KEY to the required list
 * parseArguments  method will return false if this configuration variable
 * is missing
 */
  void addRequired(const std::string& section,const std::string& key) 
  {
    _possible_args.push_back(key);
    _required.push_back({section,key});
  }

/*
 * Verify that all configuration variables present in _required map (added via addRequired)
 * are prensent in _entries map
 *
 */
  bool checkRequiredParams()
  {
    bool result = true;
    //gcc4.1
    for (auto rrequired=_required.begin(); rrequired!=_required.end(); rrequired++)
    {
        auto required = *rrequired;
//    for ( auto required : _required )
//    {
      if (! this->has(required.first,required.second)) 
      { 
        std::cout << red << "Configuration variable " ;
        if (required.first != "DEFAULT_SECTION")
            std::cout << required.first << " / ";
        std::cout << "\"" << required.second << "\""
                  << " is missing." << no_color << std::endl;
        result = false; 
      }
    } 
    return result;
  }

/*
 * return true if Config contains a variable for this DEFAULT_SECTION/KEY
 * Otherwise return false;
 */
  bool has(const std::string& key) const
  {
    return this->has(DEFAULT_SECTION,key);
  }

/*! 
 * get a configuration variable from its name to a corresponding section map
 * This is a template method. You need to specify type of returning value.
 * If you specify a wrong type an exception will be throw
 * Example:
 *  - int val_int_test = conf.get<int>("reader", "value_integer");
 * */
  template< typename T>
  T get(const std::string& section, const std::string& key ) const
  { 
      std::string val_str = this->getInternal(section,key);
      T result;
      if (std::is_fundamental<T>::value)
        { convert<T>(result, val_str); }

      else 
        { convert(result,val_str); }

      return result;
  }

/*
 * get configuration variable on the DEFAULT_SECTION section
 */
  template< typename T>
  T get(const std::string& key )  const
  {
    const std::string section(DEFAULT_SECTION);
    return this->get<T>(section,key);
  }
/*
 * getVector same as get but for std::vector
 * */
  template< typename T>
  std::vector<T> getVector(const std::string& section,
                           const std::string& key ) const
  {
    std::vector<T> result;
    std::string val_str = this->getInternal(section,key);
    // convert our framework list format to std::vector
    std::list<std::string> str_list = this->getListFromString(val_str);
//gcc4.1
    for (auto eelem=str_list.begin();eelem!=str_list.end();eelem++)
    {
        std::string elem = *eelem;
//    for(std::string elem : str_list)
//    {
      T val;
      if (std::is_fundamental<T>::value)
        { convert<T>(val, elem); }
      else 
        { convert(val,elem); }

      result.push_back(val);
    }
    return result;
  }
  
/*
 * get vector of configuration variable on the DEFAULT_SECTION section
 */
  template< typename T>
  std::vector<T> getVector(const std::string& key ) const
  {
    const std::string def = DEFAULT_SECTION;
    return  getVector<T>(def,key);
  }
/*
 * getList same as get but for std::list
 * */
  template< typename T>
  std::list<T> getList(const std::string& section,const std::string& key ) const
  {
    std::list<T> result;
    std::string val_str = this->getInternal(section,key);
    // convert our framework list format to std::list
    std::list<std::string> str_list = this->getListFromString(val_str);
    //gcc4.1
    for (auto eelem=str_list.begin(); eelem!=str_list.end(); eelem++)
    {
        std::string elem = *eelem;
//    for(std::string elem : str_list)
//    {
      T val;
      if (std::is_fundamental<T>::value)
        { convert<T>(val, elem); }
      else 
        { convert(val,elem); }
      result.push_back(val);
    }
    return result;
  }

/*
 * get list of configuration variable on the DEFAULT_SECTION section
 */
  template< typename T>
  std::list<T> getList(const std::string& key ) const
  {
    return getList<T>(DEFAULT_SECTION,key);;
  }

  /*
  * print all configuration key/value pair
  */
  void printAll() const ;

  private:
/*! 
 * convert
 * Convert std::string to typename T
 * There is special action for bool
 * */
  template< typename T>
  void convert(T& dest, const std::string& entry )const
  {
    // For string we return entry
    // For bool, we accept the following values:
    //  - 0
    //  - 1
    //  - true (with any letter case)
    //  - false (with any letter case)
    //  - yes (with any letter case)
    //  - no (with any letter case)
    //  but istringstream operator >> convert string to bool only if
    //  input is "0" and "1".
    //  So we need to detect and change entry value when needed

    std::string value = entry;
    if ( typeid(dest) == typeid(bool) )
    {
      // convert to lower case
      for (std::string::iterator p = value.begin();
        p != value.end(); ++p) {
           *p = tolower(*p); // tolower is for char
      }
      std::set<std::string> true_list = { "true","yes","1" } ;
      std::set<std::string> false_list = { "false","no","0" } ;
      if ( true_list.find(value) != true_list.end())  { value = "1";  } 
      if ( false_list.find(value) != false_list.end())  { value = "0";  } 
    }

    std::istringstream is(value);
    while ( is.good() ) {
      if ( is.peek() != EOF )
      is >> std::setbase(0) >> dest;
      else
        break;
    }

  }
  void convert(std::string& dest, const std::string& entry )const
  {
    // Remove double quote if first AND last character are double quote
    std::string local = entry; 
    size_t len = local.size();
    if ( local[0] == '\"' && local[len-1] == '\"' )
    local = local.substr(1, len-2);

    dest=local;
  }

  protected:

    std::map<
      std::string , std::map<std::string,Param >
        > _entries;

    std::list<std::pair<std::string ,std::string>> _required;

     /**
      * List of possible arguments
      */
     std::vector<std::string> _possible_args;
  
  protected:
    std::string trimKey(const std::string &entry)const ;
    std::string &ltrim(std::string &s)const ;
    std::string &rtrim(std::string &s)const ;
    std::string &trim(std::string &s)const ;


  private:
  const std::string& getInternal(const std::string& section
    ,const std::string& key) const;
  std::list<std::string> getListFromString(const std::string& entry) const;
};
/**
* end class Config
*/

}; // end namesapce Conf
}; // end namespace ADH


#endif
