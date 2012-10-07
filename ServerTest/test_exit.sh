#export URL="http://oeffi-optimizer.appspot.com/location"
#export URL="http://localhost:8080/exits"
export URL="http://oeffi-optimizer.appspot.com/exits"
#curl -X POST --data @exit1.json $URL?location=1
#curl -X POST --data @exit2.json $URL?location=1
curl -X POST --data @exit2.json http://oeffi-optimizer.appspot.com/exits?location=4001
#curl -X POST --data @location2.json $URL
#curl -X POST --data @location3.json $URL
#curl -X POST --data @location4.json $URL
#curl -X POST --data @location5.json $URL