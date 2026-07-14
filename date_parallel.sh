start_date="1997-01-01"
end_date=`date +%F`

# Loop and pipe to parallel
d="$start_date"
while [ "$d" != "$(date -I -d "$end_date + 1 day")" ]; do
    echo "$d"
    d=$(date -I -d "$d + 1 day")
done | parallel -j 8 "python Daily_parameters.py {}"
