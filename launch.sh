#!/bin/bash

./jython -Dpython.security.respectJavaAccessibility=false $@ 127.0.0.1 9090
