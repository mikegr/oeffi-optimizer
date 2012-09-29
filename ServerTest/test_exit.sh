#export URL="http://oeffi-optimizer.appspot.com/location"
export URL="http://localhost:8080/exits"
curl -X POST --data @exit1.json $URL?location=9
curl -X POST --data @exit2.json $URL?location=9
#curl -X POST --data @location2.json $URL
#curl -X POST --data @location3.json $URL
#curl -X POST --data @location4.json $URL
#curl -X POST --data @location5.json $URL