#!/bin/bash
set -e
process_map() {
    map=$1
    mpqfile="$campaign"_build/$(sed "s/^$campaign\///g" <<< "$map")
    smpq -c $mpqfile
    pushd $map
        while read -r -d "" file ; do
            file=$(cut -c 3- <<< "$file")
            smpq -a ../../$mpqfile $file
        done <  <(find . -type f  -print0)
    popd
}
export -f process_map

for campaign in "WoL" "HotS" "LotV" "NCO"; do
    export campaign
    rm -rf "$campaign"_build
    mkdir -p "$campaign"_build
    parallel -j +0 process_map ::: "$campaign"/*.SC2Map
done
