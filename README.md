# TODO
Create a well-designed database that would help in querying and reducting redundancy.
# Objective
Create a four-layered dictionary that would storage the whole data in this manner
```bash
{Layer 1 : [Layer 2 : [Layer 3 : [Layer 4]]]} // [] Indicates arrays, meaning more than 1 data value possible.
```
# Layer 1 
The four-year institutions you want to get transferred into // 9 UCs and 23 CSUs
```bash
{"UC Berkeley" : [Layer 2 : [Layer 3 : [Layer 4]]]}
```
# Layer 2
The Lower Division Courses offered at UCs/CSUs // NOT MAJORS
```bash
{"UC Berkeley" : ["EECS" : [Layer 3 : [Layer 4]]]} // INCORRECT
{"UC Berkeley" : ["MATH 1A" : [Layer 3 : [Layer 4]]]} // CORRECT
```
# Layer 3
The College that have articulation with Institution on Layer 1 (Generally Community Colleges)
```bash
{"UC Berkeley" : ["MATH 1A" : ["Sacramento City College" : [Layer 4]} // OR
{"UC Berkeley" : ["MATH 1A" : ["De Anza College" : [Layer 4]}
NOTE: If there exists no combination between two distnict colleges in Layer 1 and Layer 3, that does NOT NECCESSARILY mean that no articulation agreement exists.
Need to Think more about that.
```
# Layer 4
The Course offered at Community College (Layer 3) that articulates to the course listed at Layer 2. IF NO Course articulated then Layer 4 => null
```bash
{"UC Berkeley" : ["MATH 1A" : ["Sacramento City College" : ["MATH 400"]} // OR
{"UC Berkeley" : ["ENGLISH R1A" : ["De Anza College" : ["EWRT 1A","EWRT 1AH","ESL 5"]]]}
```
## Note 
1. The list on Layer 4 indicates ALL the different course articulated.<br>
2. In case of articulation in a series, we can get around it using a potential fifth layer.
## For Example:
 [Agreement](https://assist.org/transfer/results?year=74&institution=89&agreement=126&agreementType=from&view=agreement&viewBy=major&viewSendingAgreements=false&viewByKey=74%2F126%2Fto%2F89%2FMajor%2F9034e3b6-1889-4b83-aa31-42ed05015380) between UCD and SCC on Physics.
As the compeletion of 3 courses at SCC articulates to PHY 009A at UC Davis. We can create an additional layer 5:
```bash
{"UC Davis" : ["PHY 009A" : ["Sacramento City College" : [["PHY 410","PHY 420","PY 430"]]}
```
# Difference between fourth and potential fifth layer
All the courses in the fourth layer can be taken to complete the requirement, meaning
```bash
["CISP 400", "CISP 401"] means CISP 400 OR CISP 401
```
All the courses in the fifth layer needs to be done to complete the requirement, meaning
```bash
[["PHY 410","PHY 420","PY 430"]] meaning PHY 410 AND PHY 420 AND PHY 430
```
If incase there are 2 course combinations like MATH 1A AND 1B OR MATH 1C
THEN WE CAN USE LAYER 4 AND 5 AT THE SAME TIME
```bash
[["MATH 1A","MATH 1B"], "MATH 1C"]
```
# FOR EXAMPLE
The following is an example of all the things explained
```bash
{"UC Berkeley" : ["MATH 1A" : ["Sacramento City College" : "MATH 400", "De Anza College" : "MATH 1AH", "Some other College" : null], "MATH 1B" : ["Sacramento City College" : "MATH 401"]]
, "UC Davis" : ["PHY 009A":["Sacramento City College" : ["PHY 410","PHY 420","PY 430"]]]}
```
# Other Things to Consider
1. Some Colleges have more flexible course combinations.<br>
2. Figuring out logic for looping out the courses without redundency.
