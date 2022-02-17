for f in $(ls ~/Downloads/data.tar/*); do cat $f | go run calculate.go
done | sort -k2 -nr
