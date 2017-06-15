#!/bin/bash -e

rm -rf PySDL2-0.9.3
tar -xzf PySDL2-0.9.3.tar.gz
rm -f sdl2
ln -s PySDL2-0.9.3/sdl2
