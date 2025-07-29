#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "PySysLinkBase::PySysLinkBase" for configuration "Debug"
set_property(TARGET PySysLinkBase::PySysLinkBase APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(PySysLinkBase::PySysLinkBase PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_DEBUG "CXX"
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libPySysLinkBase-0.1.0.a"
  )

list(APPEND _cmake_import_check_targets PySysLinkBase::PySysLinkBase )
list(APPEND _cmake_import_check_files_for_PySysLinkBase::PySysLinkBase "${_IMPORT_PREFIX}/lib/libPySysLinkBase-0.1.0.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
