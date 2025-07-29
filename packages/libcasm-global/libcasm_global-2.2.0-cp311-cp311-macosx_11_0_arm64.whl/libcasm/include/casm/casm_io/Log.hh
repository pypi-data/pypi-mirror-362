#ifndef CASM_Log
#define CASM_Log

#include <chrono>
#include <iostream>
#include <sstream>
#include <vector>

#include "casm/misc/cloneable_ptr.hh"

namespace CASM {

/**
 * \defgroup LogGroup Log
 *
 * \brief Classes and functions for logging.
 *
 * \ingroup casmIO
 *
 */

class Log;
struct LogText;
struct LogParagraph;
struct LogVerbatim;

/// \brief Paragraph justification for `Log::paragraph`
///
/// \ingroup LogGroup
enum class JustificationType { Left, Right, Center, Full };

/// \brief Formatted logging
class Log {
 public:
  static const int none = 0;
  static const int quiet = 5;
  static const int standard = 10;
  static const int verbose = 20;
  static const int debug = 100;

  /// \brief Construct a Log
  Log(std::ostream &_ostream = std::cout, int _verbosity = standard,
      bool _show_clock = false, int _indent_space = 2);

  // --- List of section types ---
  // Each adds a header, ends the previous section, and begins a new section
  // Each section is associated with a verbosity level which must be met or
  //   exceded in order for the section to be printed to the stream

  template <int _required_verbosity = standard>
  void calculate(const std::string &what) {
    _add<_required_verbosity>("Calculate", what);
  }

  template <int _required_verbosity = standard>
  void construct(const std::string &what) {
    _add<_required_verbosity>("Construct", what);
  }

  template <int _required_verbosity = standard>
  void generate(const std::string &what) {
    _add<_required_verbosity>("Generate", what);
  }

  template <int _required_verbosity = standard>
  void set(const std::string &what) {
    _add<_required_verbosity>("Set", what);
  }

  template <int _required_verbosity = standard>
  void check(const std::string &what) {
    _add<_required_verbosity>("Check", what);
  }

  template <int _required_verbosity = standard>
  void results(const std::string &what) {
    _add<_required_verbosity>("Results", what);
  }

  template <int _required_verbosity = standard>
  void read(const std::string &what) {
    _add<_required_verbosity>("Read", what);
  }

  template <int _required_verbosity = standard>
  void write(const std::string &what) {
    _add<_required_verbosity>("Write", what);
  }

  template <int _required_verbosity = standard>
  void begin(const std::string &what) {
    _add<_required_verbosity>("Begin", what);
  }

  template <int _required_verbosity = standard>
  void end(const std::string &what) {
    _add<_required_verbosity>("End", what);
  }

  template <int _required_verbosity = standard>
  void warning(const std::string &what) {
    _add<_required_verbosity>("Warning", what);
  }

  template <int _required_verbosity = standard>
  void error(const std::string &what) {
    _add<_required_verbosity>("Error", what);
  }

  template <int _required_verbosity = standard>
  void compiling(const std::string &what) {
    _add<_required_verbosity>("Compiling", what);
  }

  template <int _required_verbosity = standard>
  void custom(const std::string &what) {
    static_assert(_required_verbosity >= none && _required_verbosity <= debug,
                  "CASM::Log _required_verbosity must be <= 100");
    end_section();
    begin_section<_required_verbosity>();
    if (_print()) {
      ostream() << indent_str() << "-- " << what << " -- ";
      _add_time();
      ostream() << std::endl;
    }
  }

  template <int _required_verbosity = standard>
  void custom(const std::string &type, const std::string &what) {
    _add<_required_verbosity>(type, what);
  }

  /// \brief Begin a section, without header
  template <int _required_verbosity = standard>
  void begin_section() {
    m_required_verbosity.push_back(_required_verbosity);
    m_print = (m_verbosity >= m_required_verbosity.back());
  }

  /// \brief Create a subsection
  ///
  /// - Note creates a subsection, but remembers the previous section, so that
  ///   when 'end_section' is called the previous section's verbosity level
  ///   becomes active again.
  ///
  /// Example:
  /// \code
  /// log.begin("Section A");
  /// log << stuff << std::endl;
  /// log << std::endl;
  ///
  /// log.increase_indent();
  /// log.subsection().begin("Section A.1");
  /// log << indent_str() << subsection_stuff << std::endl;
  /// log << std::endl;
  /// log.end_section();
  /// log.decrease_indent();
  ///
  /// log << "continue in section A" << std::endl;
  /// log << std::endl;
  /// \endcode
  ///
  Log &subsection() {
    begin_section<none>();
    return *this;
  }

  /// \brief End a section
  void end_section() {
    if (m_required_verbosity.size()) {
      m_required_verbosity.pop_back();
    }
    m_print = (m_verbosity >= m_required_verbosity.back());
  }

  // --- Timing ---
  // Enables timing by section

  void restart_clock();

  void show_clock();

  void hide_clock();

  double time_s() const;

  void begin_lap();

  double lap_time() const;

  // --- Verbosity ---

  /// \brief Get current verbosity level
  int verbosity() const;

  /// \brief Set current verbosity level
  void set_verbosity(int _verbosity);

  template <int _required_verbosity>
  Log &require() {
    static_assert(_required_verbosity >= none && _required_verbosity <= debug,
                  "CASM::Log _required_verbosity must be <= 100");
    m_print = (m_verbosity >= _required_verbosity);
    return *this;
  }

  /// \brief Reset underlying stream
  void reset(std::ostream &_ostream = std::cout);

  // --- Paragraph printing ---

  /// \brief Set width used for following paragraphs
  void set_width(int width) { m_paragraph_width = width; }

  /// \brief Set width used for following paragraphs
  int width() const { return m_paragraph_width; }

  /// \brief Set justification type used for following paragraphs
  void set_justification(JustificationType justification) {
    m_justification = justification;
  }

  /// \brief Get current justification type
  JustificationType justification() { return m_justification; }

  /// \brief Print indented, justified, paragraph with line wrapping
  Log &paragraph(std::string text);

  /// \brief Print verbatim, but with indentation (optional on first line)
  Log &verbatim(std::string text, bool indent_first_line = true);

  // --- List printing

  /// \brief Print a list
  template <typename OutputIterator>
  Log &verbatim_list(OutputIterator begin, OutputIterator end,
                     std::string sep = "- ");

  // --- Stream operations ---

  template <typename T>
  friend Log &operator<<(Log &log, const T &msg_details);

  friend Log &operator<<(Log &log, std::ostream &(*fptr)(std::ostream &));

  /// \brief Return reference to underlying stream
  operator std::ostream &();

  /// \brief Return reference to underlying stream
  std::ostream &ostream() { return *m_ostream; }

  /// \brief If true, indicates the current verbosity level is greater than or
  ///     equal to the current required verbosity
  bool print() const;

  /// \brief If true, indicates the current verbosity level is greater than or
  ///     equal to the current required verbosity
  explicit operator bool() { return m_print; }

  // --- Indentation ---
  // Indentation is not coupled to sectioning

  /// \brief Number of spaces per indent level
  int indent_space() const { return m_indent_space; }

  /// \brief Set number of spaces per indent level
  void set_indent_space(int _indent_space) { m_indent_space = _indent_space; }

  /// \brief Indent level
  int indent_level() const { return m_indent_level; }

  /// \brief Set indent level
  void set_indent_level(int _indent_level) { m_indent_level = _indent_level; }

  /// \brief Number of initial spaces to indent
  int initial_indent_space() const { return m_indent_spaces; }

  /// \brief Set number of initial spaces to indent
  void set_initial_indent_space(int _indent_spaces) {
    m_indent_spaces = _indent_spaces;
  }
  /// \brief String of spaces used for indentation
  ///
  /// Equivalent to:
  /// \code
  /// std::string(this->indent_space() * this->indent_level()
  ///             + this->initial_indent_space(), ' ');
  /// \code
  std::string indent_str() const {
    return std::string(m_indent_space * m_indent_level + m_indent_spaces, ' ');
  }

  /// \brief Increase the current indent level by 1
  void increase_indent() { m_indent_level++; }

  /// \brief Decrease the current indent level by 1
  void decrease_indent() {
    if (m_indent_level > 0) {
      m_indent_level--;
    }
  }

  /// \brief Increase, by n, the number of initial spaces to indent
  void increase_indent_spaces(int n) { m_indent_spaces += n; }

  /// \brief Decrease, by n, the number of initial spaces to indent
  void decrease_indent_spaces(int n) { m_indent_spaces -= n; }

  /// \brief Write spaces for the current indent level
  ///
  /// Equivalent to `(*this) << indent_str(); return *this`.
  ///
  /// Usage:
  /// \code
  /// Log log;
  /// // ... use of log.increase_indent() and log.decrease_indent()
  /// //     to set the current indent level ...
  /// log.indent() << "text that should be indented..." << std::endl;
  /// log << "text that should not be indented..." << std::endl;
  /// \endcode
  ///
  Log &indent() {
    (*this) << indent_str();
    return *this;
  }

  /// Same as verbatim, but uses stringstream to convert to string first
  template <typename T>
  Log &indent(const T &t) {
    std::stringstream ss;
    ss << t;
    return verbatim(ss.str());
  }

  static std::string invalid_verbosity_msg(std::string s);

  /// \brief Read verbosity level from a string
  static std::pair<bool, int> verbosity_level(std::string s);

 private:
  template <int _required_verbosity = standard>
  void _add(const std::string &type, const std::string &what) {
    static_assert(_required_verbosity >= none && _required_verbosity <= debug,
                  "CASM::Log _required_verbosity must be <= 100");
    end_section();
    begin_section<_required_verbosity>();
    if (_print()) {
      ostream() << indent_str() << "-- " << type << ": " << what << " -- ";
      _add_time();
      ostream() << std::endl;
    }
  }

  void _print_justified_line(std::vector<std::string> &line, int curr_width);
  void _print_left_justified_line(std::vector<std::string> &line,
                                  int curr_width);
  void _print_right_justified_line(std::vector<std::string> &line,
                                   int curr_width);
  void _print_center_justified_line(std::vector<std::string> &line,
                                    int curr_width);
  void _print_full_justified_line(std::vector<std::string> &line,
                                  int curr_width);

  void _add_time();

  bool _print() const;

  std::vector<int> m_required_verbosity;

  /// If m_verbosity >= required verbosity, then print
  int m_verbosity;

  /// Whether to print
  bool m_print;

  bool m_show_clock;

  /// indent_str = m_indent_space*m_indent_level + m_indent_spaces
  int m_indent_space;
  int m_indent_level;
  int m_indent_spaces;

  // for paragraph writing
  int m_paragraph_width;
  JustificationType m_justification;

  std::chrono::steady_clock::time_point m_start_time;

  std::chrono::steady_clock::time_point m_lap_start_time;

  std::ostream *m_ostream;
};

/// \brief Print a list
///
/// - Prints each element in vector to a stringstream, then uses Log::verbatim
///   to print into the list.
/// - Indentation is set to the length of the "sep" string
///
/// Example, with initial indent of 2 spaces, and sep="-- ":
/// \code
/// A list:
///   -- first value
///   -- some value
///      that prints
///      on multiple lines
///   -- last value
/// \endcode
template <typename OutputIterator>
Log &Log::verbatim_list(OutputIterator begin, OutputIterator end,
                        std::string sep) {
  int n_indent_spaces = sep.size();

  bool indent_first_line = false;
  for (auto it = begin; it != end; ++it) {
    indent() << sep;
    std::stringstream ss;
    ss << *it;
    increase_indent_spaces(n_indent_spaces);
    verbatim(ss.str(), indent_first_line);
    decrease_indent_spaces(n_indent_spaces);
  }
  return *this;
}

/// \brief Write to Log, if verbosity level satisfied
///
/// If the Log's current verbosity level exceeds the Log's current required
/// verbosity level, then the write occurs; otherwise the write does not occur.
///
/// \relates Log
template <typename T>
Log &operator<<(Log &log, const T &msg_details) {
  if (log._print()) {
    static_cast<std::ostream &>(log) << msg_details;
  }
  return log;
}

/// \brief Write to Log, if verbosity level satisfied
Log &operator<<(Log &log, std::ostream &(*fptr)(std::ostream &));

/// \brief A Log whose underlying ostream* cannot be reset
///
/// \ingroup LogGroup
class FixedLog : public Log {
 public:
  explicit FixedLog(std::ostream &_ostream);
  FixedLog(FixedLog const &) = delete;
  FixedLog &operator=(FixedLog const &RHS) = delete;

 private:
  using Log::reset;
};

/// \brief Default global log for stream output
///
/// Initially this writes to `std::cout`, but it can be reset. Prefer using
/// `::log()`.
///
/// \relates Log
inline Log &default_log() {
  static Log log{std::cout};
  return log;
}

/// \brief Default global log for stream output of error messages
///
/// Initially this writes to `std::cout`, but it can be reset. Prefer using
/// `::err_log()`.
///
/// \relates Log
inline Log &default_err_log() {
  static Log log{std::cerr};
  return log;
}

/// \brief Resettable Log for stream output
///
/// Initially this writes to `std::cout`, but it can be reset.
///
/// \relates Log
inline Log &log() { return CASM::default_log(); }

/// \brief Resettable global Log for stream output of error messages
///
/// Initially this writes to `std::cerr`, but it can be reset.
///
//// \relates Log
inline Log &err_log() { return CASM::default_err_log(); }

/// \brief FixedLog to std::cout
///
/// \relates Log
inline Log &cout_log() {
  static FixedLog log{std::cout};
  return log;
}

/// \brief FixedLog to std::cerr
///
/// \relates Log
inline Log &cerr_log() {
  static FixedLog log{std::cerr};
  return log;
}

/// \brief FixedLog to null stream
///
/// \relates Log
inline Log &null_log() {
  static std::ostream nullout{nullptr};
  static FixedLog log{nullout};
  return log;
}

/// \brief Log to a stringstream
///
/// \ingroup LogGroup
class OStringStreamLog : public Log {
 public:
  /// \brief Construct a StringStreamLog
  ///
  /// \param verbosity The amount to be printed
  ///
  /// For verbosity:
  /// - 0: print nothing
  /// - 10: print all standard output
  /// - 100: print all possible output
  OStringStreamLog(int _verbosity = standard, bool _show_clock = false)
      : Log(std::cout, _verbosity, _show_clock) {
    reset(m_ss);
  }

  std::ostringstream &ss() { return m_ss; };

  const std::ostringstream &ss() const { return m_ss; };

 private:
  std::ostringstream m_ss;
};

/// \brief Reset where CASM::log() and CASM::err_log() direct output for the
///     scope of this object, then revert to their previous output stream.
///
/// For the life of ScopedLogging CASM::log() and CASM::err_log() provide
/// references to `new_log` and `new_err_log`, unless overridden by another
/// ScopedLogging. The references are reverted upon destruction.
///
/// \ingroup LogGroup
class ScopedLogging {
 public:
  ScopedLogging(Log &new_log, Log &new_err_log)
      : m_old_log(CASM::log()), m_old_err_log(CASM::err_log()) {
    CASM::log() = new_log;
    CASM::err_log() = new_err_log;
  }

  ~ScopedLogging() {
    CASM::log() = m_old_log;
    CASM::err_log() = m_old_err_log;
  }

  Log m_old_log;
  Log m_old_err_log;
};

/// \brief ScopedLogging, directing output to CASM::null_log()
///
/// For the life of ScopedNullLogging, CASM::log() and CASM::err_log() provide
/// references to CASM::null_log(), unless overridden by another ScopedLogging.
/// The references are reverted upon destruction.
///
/// \ingroup LogGroup
class ScopedNullLogging {
 public:
  ScopedNullLogging() : m_logging(null_log(), null_log()) {}

 private:
  ScopedLogging m_logging;
};

/// \brief ScopedLogging, directing output to a stringstream
///
/// For the life of ScopedStringStreamLogging CASM::log() and CASM::err_log()
/// provide references to OStringStreamLog. The string values can be obtained
/// from ScopedStringStreamLogging::ss() and
/// ScopedStringStreamLogging::err_ss(). The references are reverted upon
/// destruction.
///
/// \ingroup LogGroup
class ScopedStringStreamLogging {
 public:
  /// Construct scoped StringStreamLog
  ScopedStringStreamLogging(int _verbosity = Log::standard,
                            bool _show_clock = false)
      : m_ss_log(_verbosity, _show_clock),
        m_ss_err_log(_verbosity, _show_clock) {
    m_logging = notstd::make_unique<ScopedLogging>(m_ss_log, m_ss_err_log);
  }

  ~ScopedStringStreamLogging() { m_logging.reset(); }

  std::ostringstream &ss() { return m_ss_log.ss(); };

  const std::ostringstream &ss() const { return m_ss_log.ss(); };

  std::ostringstream &err_ss() { return m_ss_err_log.ss(); };

  const std::ostringstream &err_ss() const { return m_ss_err_log.ss(); };

 private:
  std::unique_ptr<ScopedLogging> m_logging;
  OStringStreamLog m_ss_log;
  OStringStreamLog m_ss_err_log;
};

}  // namespace CASM

#endif
