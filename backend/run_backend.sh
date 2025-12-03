#!/bin/bash

# This script runs the Quart backend server for BrainBatch.
# It assumes that all the required files and dependencies are already present.
# If you need debug features, you probably shouldn't use this script.

source .venv/bin/activate
cd ./scripts
hypercorn bb_quart_main:app
