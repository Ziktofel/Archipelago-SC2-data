#!/bin/bash
set -e

# Cleanup
rm -rf target/

# Build the maps
pushd Maps/ArchipelagoCampaign
./build.sh
popd

# Create the target directory
mkdir -p target

# Copy maps
mkdir -p target/Maps/ArchipelagoCampaign/WoL
mkdir -p target/Maps/ArchipelagoCampaign/HotS
mkdir -p target/Maps/ArchipelagoCampaign/LotV
cp -- Maps/ArchipelagoCampaign/WoL_build/* target/Maps/ArchipelagoCampaign/WoL/
cp -- Maps/ArchipelagoCampaign/HotS_build/* target/Maps/ArchipelagoCampaign/HotS/
cp -- Maps/ArchipelagoCampaign/LotV_build/* target/Maps/ArchipelagoCampaign/LotV/

# Copy mods
mkdir -p target/Mods
cp -r -- Mods/* target/Mods
