# Copyright (c) 2010-2011 Phorm, Inc.
# License: GNU LGPL v 3.0, see http://www.gnu.org/licenses/lgpl-3.0-standalone.html
# Authors: Andrey Skryabin <andrew@zmqmessage.org>, et al.
# CTA Authors: Jean Jacquemier <jean.jacquemier@lapp.in2p3.fr>, 
#              Dirk Hoffmann <hoffmann@cppm.in2p3.fr> 2016
# Find the zeromq includes and library
# $Id$
#
# ZEROMQ_INCLUDE_DIR - Where to find zeromq include sub-directory.
# ZEROMQ_LIBRARIES - List of libraries when using zeromq.
# ZEROMQ_FOUND - True if zeromq found.
IF (ZEROMQ_INCLUDE_DIR)
    # Already in cache, be silent.
    SET(ZEROMQ_FIND_QUIETLY TRUE)
ENDIF (ZEROMQ_INCLUDE_DIR)

FIND_PATH(ZEROMQ_INCLUDE_DIR zmq.h
    HINTS $ENV{ZMQ_ROOT_DIR} PATHS /usr/local  PATH_SUFFIXES include)

FIND_LIBRARY(ZEROMQ_LIBRARY NAMES zmq
    HINTS $ENV{ZMQ_ROOT_DIR} PATHS /usr/local PATH_SUFFIXES lib src/.libs)

# Handle the QUIETLY and REQUIRED arguments and set ZEROMQ_FOUND to
# TRUE if all listed variables are TRUE.
INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS( ZEROMQ DEFAULT_MSG 
    ZEROMQ_LIBRARY ZEROMQ_INCLUDE_DIR)

 
IF (ZEROMQ_FOUND)
    SET(ZEROMQ_LIBRARIES ${ZEROMQ_LIBRARY})
ENDIF(ZEROMQ_FOUND)

