#ifndef CASM_InputParser_impl
#define CASM_InputParser_impl

#include "casm/casm_io/Help.hh"
#include "casm/casm_io/Log.hh"
#include "casm/casm_io/json/InputParser.hh"
#include "casm/global/enum/json_io.hh"
#include "casm/misc/TypeInfo.hh"

namespace CASM {

/// \brief Construct parser and use `parse(*this, std::forward<Args>(args)...)`
template <typename T>
template <typename... Args>
InputParser<T>::InputParser(jsonParser const &_input, Args &&...args)
    : KwargsParser(_input, "", true) {
  parse(*this, std::forward<Args>(args)...);
}

/// \brief Construct parser and use
///     `parse(*this, std::forward<Args>(args)...)` if `_path` exists
template <typename T>
template <typename... Args>
InputParser<T>::InputParser(jsonParser const &_input, fs::path _path,
                            bool _required, Args &&...args)
    : KwargsParser(_input, _path, _required) {
  if (this->exists()) {
    parse(*this, std::forward<Args>(args)...);
  }
}

/// \brief Construct parser and use custom parse function,
///     `f_parse(*this, std::forward<Args>(args)...)`
template <typename T>
template <typename CustomParse, typename... Args>
InputParser<T>::InputParser(CustomParse f_parse, jsonParser const &_input,
                            Args &&...args)
    : KwargsParser(_input, "", true) {
  f_parse(*this, std::forward<Args>(args)...);
}

/// Construct parser and use custom parse function,
///     `f_parse(*this, std::forward<Args>(args)...)`, if `_path` exists
template <typename T>
template <typename CustomParse, typename... Args>
InputParser<T>::InputParser(CustomParse f_parse, jsonParser const &_input,
                            fs::path _path, bool _required, Args &&...args)
    : KwargsParser(_input, _path, _required) {
  if (this->exists()) {
    f_parse(*this, std::forward<Args>(args)...);
  }
}

template <typename T>
template <typename RequiredType, typename... Args>
std::unique_ptr<RequiredType> InputParser<T>::require(fs::path option,
                                                      Args &&...args) {
  auto it = self.find_at(option);
  std::unique_ptr<RequiredType> res;
  if (it == self.end()) {
    std::stringstream msg;
    msg << "Error: missing required option '" << option.string() << "'.";
    this->insert_error(option, msg.str());
    return res;
  }

  try {
    return it->template make<RequiredType>(std::forward<Args>(args)...);
  } catch (std::exception &e) {
    std::stringstream msg;
    msg << "Error: could not construct type '"
        << CASM::type_name<RequiredType>() << "' from option '"
        << option.string() << "'.";
    this->insert_error(option, msg.str());
    return res;
  }
}

template <typename T>
template <typename RequiredType, typename... Args>
void InputParser<T>::require(RequiredType &value, fs::path option,
                             Args &&...args) {
  auto it = self.find_at(option);
  std::unique_ptr<RequiredType> res;
  if (it == self.end()) {
    std::stringstream msg;
    msg << "Error: missing required option '" << option.string() << "'.";
    this->insert_error(option, msg.str());
    return;
  }

  try {
    it->template get<RequiredType>(value, std::forward<Args>(args)...);
    return;
  } catch (std::exception &e) {
    std::stringstream msg;
    msg << "Error: could not construct type '"
        << CASM::type_name<RequiredType>() << "' from option '"
        << option.string() << "'.";
    this->insert_error(option, msg.str());
    return;
  }
}

template <typename T>
template <typename RequiredType, typename... Args>
std::unique_ptr<RequiredType> InputParser<T>::optional(fs::path option,
                                                       Args &&...args) {
  jsonParser const *ptr;
  if (option.empty()) {
    ptr = &self;
  } else {
    auto it = self.find_at(option);
    if (it == self.end() || it->is_null()) {
      return std::unique_ptr<RequiredType>();
    } else {
      ptr = &(*it);
    }
  }

  try {
    return ptr->make<RequiredType>(std::forward<Args>(args)...);
  } catch (std::exception &e) {
    std::stringstream msg;
    msg << "Error: could not construct type '"
        << CASM::type_name<RequiredType>() << "' from option '"
        << option.string() << "'.";
    this->insert_error(option, msg.str());
    return std::unique_ptr<RequiredType>();
  }
}

template <typename T>
template <typename RequiredType, typename... Args>
void InputParser<T>::optional(RequiredType &value, fs::path option,
                              Args &&...args) {
  jsonParser const *ptr;
  if (option.empty()) {
    ptr = &self;
  } else {
    auto it = self.find_at(option);
    if (it == self.end() || it->is_null()) {
      return;
    } else {
      ptr = &(*it);
    }
  }

  try {
    ptr->get<RequiredType>(value, std::forward<Args>(args)...);
    return;
  } catch (std::exception &e) {
    std::stringstream msg;
    msg << "Error: could not construct type '"
        << CASM::type_name<RequiredType>() << "' from option '"
        << option.string() << "'.";
    this->insert_error(option, msg.str());
    return;
  }
}

template <typename T>
template <typename RequiredType, typename... Args>
RequiredType InputParser<T>::optional_else(fs::path option,
                                           const RequiredType &_default,
                                           Args &&...args) {
  jsonParser const *ptr;
  if (option.empty()) {
    ptr = &self;
  } else {
    auto it = self.find_at(option);
    if (it == self.end() || it->is_null()) {
      return _default;
    } else {
      ptr = &(*it);
    }
  }

  try {
    return ptr->get<RequiredType>(std::forward<Args>(args)...);
  } catch (std::exception &e) {
    std::stringstream msg;
    msg << "Error: could not construct type '"
        << CASM::type_name<RequiredType>() << "' from option '"
        << option.string() << "'.";
    this->insert_error(option, msg.str());
    return _default;
  }
}

template <typename T>
template <typename RequiredType, typename... Args>
void InputParser<T>::optional_else(RequiredType &value, fs::path option,
                                   const RequiredType &_default,
                                   Args &&...args) {
  jsonParser const *ptr;
  if (option.empty()) {
    ptr = &self;
  } else {
    auto it = self.find_at(option);
    if (it == self.end() || it->is_null()) {
      value = _default;
      return;
    } else {
      ptr = &(*it);
    }
  }

  try {
    ptr->get<RequiredType>(value, std::forward<Args>(args)...);
    return;
  } catch (std::exception &e) {
    std::stringstream msg;
    msg << "Error: could not construct type '"
        << CASM::type_name<RequiredType>() << "' from option '"
        << option.string() << "'.";
    this->insert_error(option, msg.str());
    return;
  }
}

template <typename T>
template <typename RequiredType, typename... Args>
std::shared_ptr<InputParser<RequiredType>> InputParser<T>::subparse(
    fs::path option, Args &&...args) {
  auto subparser = std::make_shared<InputParser<RequiredType>>(
      this->input, this->relpath(option), true, std::forward<Args>(args)...);
  subparser->type_name = CASM::type_name<RequiredType>();
  insert(subparser->path, subparser);
  return subparser;
}

template <typename T>
template <typename RequiredType, typename... Args>
std::shared_ptr<InputParser<RequiredType>> InputParser<T>::subparse_if(
    fs::path option, Args &&...args) {
  auto subparser = std::make_shared<InputParser<RequiredType>>(
      this->input, this->relpath(option), false, std::forward<Args>(args)...);
  subparser->type_name = CASM::type_name<RequiredType>();
  insert(subparser->path, subparser);
  return subparser;
}

template <typename T>
template <typename RequiredType, typename... Args>
std::shared_ptr<InputParser<RequiredType>> InputParser<T>::subparse_else(
    fs::path option, const RequiredType &_default, Args &&...args) {
  auto subparser =
      subparse_if<RequiredType>(option, std::forward<Args>(args)...);
  if (!subparser->exists() || subparser->self.is_null()) {
    subparser->value = notstd::make_unique<RequiredType>(_default);
  }
  return subparser;
}

template <typename T>
template <typename RequiredType, typename... Args>
std::shared_ptr<InputParser<RequiredType>> InputParser<T>::parse_as(
    Args &&...args) {
  auto subparser = std::make_shared<InputParser<RequiredType>>(
      this->input, this->path, true, std::forward<Args>(args)...);
  subparser->type_name = CASM::type_name<RequiredType>();
  insert(subparser->path, subparser);
  return subparser;
}

/// \brief Equivalent to `subparse`, but using custom parse method
template <typename T>
template <typename RequiredType, typename CustomParse, typename... Args>
std::shared_ptr<InputParser<RequiredType>> InputParser<T>::subparse_with(
    CustomParse f_parse, fs::path option, Args &&...args) {
  auto subparser = std::make_shared<InputParser<RequiredType>>(
      f_parse, this->input, this->relpath(option), true,
      std::forward<Args>(args)...);
  subparser->type_name = CASM::type_name<RequiredType>();
  insert(subparser->path, subparser);
  return subparser;
}

/// \brief Equivalent to `subparse_if`, but using custom parse method
template <typename T>
template <typename RequiredType, typename CustomParse, typename... Args>
std::shared_ptr<InputParser<RequiredType>> InputParser<T>::subparse_if_with(
    CustomParse f_parse, fs::path option, Args &&...args) {
  auto subparser = std::make_shared<InputParser<RequiredType>>(
      f_parse, this->input, this->relpath(option), false,
      std::forward<Args>(args)...);
  subparser->type_name = CASM::type_name<RequiredType>();
  insert(subparser->path, subparser);
  return subparser;
}

/// \brief Equivalent to `subparse_else`, but using custom parse method
template <typename T>
template <typename RequiredType, typename CustomParse, typename... Args>
std::shared_ptr<InputParser<RequiredType>> InputParser<T>::subparse_else_with(
    CustomParse f_parse, fs::path option, const RequiredType &_default,
    Args &&...args) {
  auto subparser = subparse_if_with<RequiredType>(f_parse, option,
                                                  std::forward<Args>(args)...);
  if (!subparser->exists() || subparser->self.is_null()) {
    subparser->value = notstd::make_unique<RequiredType>(_default);
  }
  return subparser;
}

/// Run an InputParser on the JSON file with path given by the option,
///     collecting errors and warnings
template <typename T>
template <typename RequiredType, typename... Args>
std::shared_ptr<InputParser<RequiredType>> InputParser<T>::subparse_from_file(
    fs::path option, Args &&...args) {
  std::string filepath;
  require(filepath, option);
  if (!fs::exists(filepath)) {
    insert_error(option, "Error: file does not exist.");
    jsonParser json;
    return std::make_shared<InputParser<RequiredType>>(
        json, std::forward<Args>(args)...);
  }
  jsonParser json{fs::path(filepath)};
  auto subparser = std::make_shared<InputParser<RequiredType>>(
      json, std::forward<Args>(args)...);
  subparser->type_name = CASM::type_name<RequiredType>();
  insert(this->relpath(option), subparser);
  return subparser;
}

/// \brief Equivalent to `parse_as`, but using custom parse method
template <typename T>
template <typename RequiredType, typename CustomParse, typename... Args>
std::shared_ptr<InputParser<RequiredType>> InputParser<T>::parse_as_with(
    CustomParse f_parse, Args &&...args) {
  auto subparser = std::make_shared<InputParser<RequiredType>>(
      f_parse, this->input, this->path, true, std::forward<Args>(args)...);
  subparser->type_name = CASM::type_name<RequiredType>();
  insert(subparser->path, subparser);
  return subparser;
}

/// \brief Print errors and warnings, throwing as specified if any errors exist
///     in parser (and subparsers)
///
/// See `::InputParser` for example usage.
///
/// \relates InputParser
template <typename ErrorType>
void report_and_throw_if_invalid(KwargsParser const &parser, Log &log,
                                 ErrorType error) {
  if (!parser.valid()) {
    jsonParser report = make_report(parser);
    log << std::endl;
    print_errors(parser, log, "Error Summary");
    log << std::endl;
    log.indent() << report << std::endl << std::endl;
    throw error;
  }
  if (parser.all_warnings().size()) {
    jsonParser report = make_report(parser);
    log << std::endl;
    print_warnings(parser, log, "Warning Summary");
    log << std::endl;
    log.indent() << report << std::endl << std::endl;
  }
}

/// \brief Default parse method
///
/// If `parser.exists()`, parses value using `parser.self.make<T>()`.
/// Otherwise, stores a "could not construct" error message.
///
/// \relates InputParser
template <typename T>
void parse(InputParser<T> &parser) {
  if (parser.exists()) {
    try {
      parser.value = parser.self.template make<T>();
    } catch (std::exception &e) {
      parser.error.insert(std::string("Error: could not construct type '") +
                          CASM::type_name<T>() + "'.");
    }
  }
}
}  // namespace CASM

#endif
