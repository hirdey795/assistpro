# TODO
Create a well-designed database that would help in querying and reducting redundancy.
# Objective
Create a four-layered dictionary that would storage the whole data in this manner
```bash
{Layer 1 : [Layer 2 : [Layer 3 : [Layer 4]}
```
# Layer 1 
The four-year institutions you want to get transferred into // 9 UCs and 23 CSUs
```bash
{"UC Berkeley" : [Layer 2 : [Layer 3 : [Layer 4]}
```
# Layer 2
The Lower Division Courses offered at UCs/CSUs // NOT MAJORS
```bash
{"UC Berkeley" : ["EECS" : [Layer 3 : [Layer 4]} // INCORRECT
{"UC Berkeley" : ["MATH 1A" : [Layer 3 : [Layer 4]} // CORRECT
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
The Course offered at Community College (Layer 3) that articulates to the course listed at Layer 2.
```bash
{"UC Berkeley" : ["MATH 1A" : ["Sacramento City College" : ["MATH 400"]} // OR
{"UC Berkeley" : ["MATH 1A" : ["De Anza College" : [""]}
