for f in $(ls data/*); do cat $f | go run calculate.go
done | sort -k2 -nr
