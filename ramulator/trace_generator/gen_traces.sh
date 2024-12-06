#!/bin/bash

generate_hex_with_zeros() {
    iter=$1
    hex=""

    for i in {1..640}; do
        hex="$hex$(printf '%x' $((RANDOM % 16)))"
    done

    echo "$hex"
}

# IMPORTANT! Change this to the corresponding PIN_ROOT
export PIN_ROOT=./pin-3.7-97619-g0d0c92f4f-gcc-linux

# cd ../ramulator/trace_generator/
# dir=aescpu"$position"
# mkdir "$dir"

# for ((i = 1; i <= N; i++)); do
#     hex_input=$(generate_hex_with_zeros)
    
#     ./tracegenerator.sh -t "$dir"/"$i".out -mode cpu -paddr off -ifetch off -- ../../AES-Optimization/aes1r "$hex_input"
# done


# filename=$1
# iteration=$2
# bitvalue=$3

iteration=$1

for ((i = 0; i < 256; i++)); do
    filename=./all_tests/"$i"

    hex_input=$(generate_hex_with_zeros "$iteration")
    # echo "$hex_input"

    ./tracegenerator.sh -t "$filename".out -dcache off -mode cpu -paddr off -ifetch off -- ../../AES-Optimization/aesrand_in "$iteration" "$i" "$hex_input" > "$filename".log

    python3 ./clean_trace.py "$filename".out "$filename".trace

    # rm -r temp-"$filename".out
    rm -r "$filename".out
    echo $i done.

done

# ./tracegenerator.sh -t "$filename".out -dcache off -mode cpu -paddr off -ifetch off -- ../../AES-Optimization/aesrand "$iteration" "$bitvalue"> "$filename".log

# python3 ./clean_trace.py "$filename".out "$filename".trace

# # rm -r temp-"$filename".out
# rm -r ./all_tests/"$filename".out

# cd -

