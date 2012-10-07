#export URL="http://oeffi-optimizer.appspot.com/locations"
export URL="http://localhost:8080/locations"
curl -X POST --data @location1.json $URL
curl -X POST --data @location2.json $URL
#curl -X POST --data @location3.json $URL
#curl -X POST --data @location4.json $URL
#curl -X POST --data @location5.json $URL
