# example main
add_executable(siscone_main options.cpp main.cpp)
target_link_libraries(siscone_main PUBLIC siscone)

# example area
add_executable(siscone_area options.cpp area.cpp)
target_link_libraries(siscone_area PUBLIC siscone)

# example test
add_executable(siscone_test options.cpp test.cpp)
target_link_libraries(siscone_test PUBLIC siscone)

# example times
add_executable(times options.cpp times.cpp)
target_link_libraries(times PUBLIC siscone)

# example sample
add_executable(sample options.cpp sample.cpp)
target_link_libraries(sample PUBLIC siscone)

# example spherical
add_executable(spherical options.cpp spherical.cpp)
target_link_libraries(spherical PUBLIC siscone_spherical)

if (MSVC)
  # This lets us have linux-like getopt on Windows.
  # It is not marked required so that it's less difficult
  # to inject the package into cmake via other means.
  find_package(unofficial-getopt-win32)
  
  # The following defines silence warnings about sscanf and other
  # c functions that don't have buffer-overrun protection built into them.
  # Windows provides alternative implementations with such protections.
  # Siscone/fastjet likely do not need to consider such security issues for 
  # scrubbing input data, thus we suppress the warning.
  target_compile_definitions(siscone_main PUBLIC -D_CRT_SECURE_NO_WARNINGS)
  target_compile_definitions(siscone_area PUBLIC -D_CRT_SECURE_NO_WARNINGS)
  target_compile_definitions(siscone_test PUBLIC -D_CRT_SECURE_NO_WARNINGS)
  target_compile_definitions(times PUBLIC -D_CRT_SECURE_NO_WARNINGS)
  target_compile_definitions(sample PUBLIC -D_CRT_SECURE_NO_WARNINGS)
  target_compile_definitions(spherical PUBLIC -D_CRT_SECURE_NO_WARNINGS)

  target_link_libraries(siscone_main PRIVATE unofficial::getopt-win32::getopt)
  target_link_libraries(siscone_area PRIVATE unofficial::getopt-win32::getopt)
  target_link_libraries(siscone_test PRIVATE unofficial::getopt-win32::getopt)
  target_link_libraries(times PRIVATE unofficial::getopt-win32::getopt)
  target_link_libraries(sample PRIVATE unofficial::getopt-win32::getopt)
  target_link_libraries(spherical PRIVATE unofficial::getopt-win32::getopt)
endif()