include_directories(${lib_SOURCE_DIR}/lib /usr/include)

#add_library(random ${LIBSRC})

add_executable(teste1 teste1.c)

target_link_libraries(teste1 random m)
