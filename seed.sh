#!/bin/bash

for data in \
'{"locationName":"Eiffel Tower","city":"Paris","country":"France","visitDate":"2024-06-01","rating":5,"notes":"Iconic landmark"}' \
'{"locationName":"Louvre Museum","city":"Paris","country":"France","visitDate":"2024-06-02","rating":4,"notes":"Mona Lisa"}' \
'{"locationName":"Notre Dame","city":"Paris","country":"France","visitDate":"2024-06-03","rating":5,"notes":"Cathedral"}' \
'{"locationName":"Colosseum","city":"Rome","country":"Italy","visitDate":"2024-07-01","rating":4,"notes":"Ancient arena"}' \
'{"locationName":"Trevi Fountain","city":"Rome","country":"Italy","visitDate":"2024-07-02","rating":3,"notes":"Coins"}' \
'{"locationName":"Venice Canals","city":"Venice","country":"Italy","visitDate":"2024-07-03","rating":5,"notes":"Gondolas"}' \
'{"locationName":"Big Ben","city":"London","country":"UK","visitDate":"2024-08-01","rating":4,"notes":"Clock tower"}' \
'{"locationName":"Tower Bridge","city":"London","country":"UK","visitDate":"2024-08-02","rating":5,"notes":"Bridge"}' \
'{"locationName":"British Museum","city":"London","country":"UK","visitDate":"2024-08-03","rating":4,"notes":"History"}' \
'{"locationName":"Statue of Liberty","city":"New York","country":"USA","visitDate":"2024-09-01","rating":5,"notes":"Gift from France"}' \
'{"locationName":"Central Park","city":"New York","country":"USA","visitDate":"2024-09-02","rating":4,"notes":"Relaxing"}' \
'{"locationName":"Times Square","city":"New York","country":"USA","visitDate":"2024-09-03","rating":3,"notes":"Crowded"}' \
'{"locationName":"Golden Gate Bridge","city":"San Francisco","country":"USA","visitDate":"2024-10-01","rating":5,"notes":"Foggy view"}' \
'{"locationName":"Alcatraz","city":"San Francisco","country":"USA","visitDate":"2024-10-02","rating":4,"notes":"Prison island"}' \
'{"locationName":"Hollywood Sign","city":"Los Angeles","country":"USA","visitDate":"2024-11-01","rating":3,"notes":"Hike"}' \
'{"locationName":"Disneyland","city":"Los Angeles","country":"USA","visitDate":"2024-11-02","rating":5,"notes":"Theme park"}' \
'{"locationName":"Tokyo Tower","city":"Tokyo","country":"Japan","visitDate":"2024-12-01","rating":5,"notes":"Skyline"}' \
'{"locationName":"Shibuya Crossing","city":"Tokyo","country":"Japan","visitDate":"2024-12-02","rating":4,"notes":"Busy intersection"}' \
'{"locationName":"Mount Fuji","city":"Fujinomiya","country":"Japan","visitDate":"2024-12-03","rating":5,"notes":"Climb"}' \
'{"locationName":"Kyoto Temples","city":"Kyoto","country":"Japan","visitDate":"2024-12-04","rating":4,"notes":"Traditional"}'
do
  curl -s -X POST "http://127.0.0.1:8000/trips" \
    -H "Content-Type: application/json" \
    -d "$data" > /dev/null
done

echo "✅ Added 20 trips!"