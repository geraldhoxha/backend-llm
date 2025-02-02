## LLM service

### Run LLM test-to-image standalone
1. ```make buildall```
2. Use curl command to generate an image
   1. curl --header "Content-Type: application/json" --request POST --data '{"text": "**PROOMPT HERE**"}' http://MinikubeIP:30081/model/generate --output response.png