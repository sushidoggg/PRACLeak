for ((i = 0; i < 256; i++)); do
    ./ramulator2 -f all_test_yaml/"$i".yaml >> test.log
    echo Test $i done.
done