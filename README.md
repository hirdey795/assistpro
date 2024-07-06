# [AssistPro](https://assistpro-test.vercel.app) 🌐
Comprehensive web tool designed to simplify the process of identifying class articulations across various colleges and universities. It is particularly useful for students planning to transfer and needing to find equivalent courses at their new institution.

P.S. I have it hosted on a vercel server right now for our demo front end, click the **AssistPro** header in blue.
# TODO:
- [ ] Update/Format Website with features, look into this [layout](https://github.com/hirdey795/assistpro/blob/main/Extra_README/README_LAYOUT.md)
- [x] Scrape all UNI/CSU Classes
- [ ] Return all classes from colleges which are available for the selected class that the user picked. (Frontend/Backend Communication)
- [x] Make scraping headless optional (not need window popup everytime we scrape)
- [ ] FastAPI / Flask ?

# DEMO OF SCRAPING
![GIF](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHRpbWw1em00MHh4OGxuYW9heHBkajg4eGxyNjZuZHB2N3Bpa2loNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QpDKozmCN3XGi2YHBV/giphy.gif)

# Use Case Scenario:

The JSON Object below showcases the differences of articulations, between Diablo Valley College (DVC) & Sacramento City College (SCC).

Let's say our client wants to transfer to UC Berkeley, they need to finish **COMPSCI 61C**.

We can see that SCC has **No Course Articulated** for **COMPSCI 61C**, whereas DVC has a course ,**COMSC 260**, articulated with UC Berkeley.

```js
{
    "('To: University of California, Berkeley', 'From: Diablo Valley College')": [
        "Electrical Engineering & Computer Sciences, Lower Division B.S.",
        {
            "MATH 1A": "MATH 192",
            ...
            "COMPSCI 61C": "COMSC 260"
        }
    ],
    "('To: University of California, Berkeley', 'From: Sacramento City College')": [
        "Electrical Engineering & Computer Sciences, Lower Division B.S.",
        {
            "MATH 1A": "MATH 400",
            ...
            "COMPSCI 61C": "No Course Articulated"
        }
    ]
}
```
Sample Data that is serving our front end inputs
```json
{
    "UC Berkeley": {
      "Aerospace Engineering": ["MATH 1A", "PHYSICS 7A", "ENGIN 7"],
      "Electrical Engineering": ["MATH 1B", "PHYSICS 7B", "EECS 16A"],
      "Computer Science": ["COMPSCI 61A", "COMPSCI 61B", "COMPSCI 70"]
    },
    "Stanford University": {
      "Biology": ["BIO 101", "BIO 102", "CHEM 121"],
      "Mechanical Engineering": ["ME 101", "ME 102", "PHYSICS 45"],
      "Psychology": ["PSYCH 1", "PSYCH 2", "STAT 101"]
    },
    "Harvard University": {
      "Economics": ["ECON 101", "ECON 102", "STAT 104"],
      "Political Science": ["POL 101", "POL 102", "HIST 105"],
      "Law": ["LAW 101", "LAW 102", "HIST 204"]
    },
    "Massachusetts Institute of Technology": {
      "Physics": ["PHYS 101", "PHYS 102", "MATH 111"],
      "Chemistry": ["CHEM 101", "CHEM 102", "BIO 103"],
      "Mathematics": ["MATH 101", "MATH 102", "MATH 201"]
    }
  }
```

# Intent To Use This Service
If you want to contribute to this, please let me know and send PRs. Please also credit us. Edward and Hirdeyjeet, for coming with this idea and web scraping software. Feel free to use our web scraper and if you have any problems, feel free to shoot one of us an email, or text on Linkedin.

# Installation

Create and activate python venv [Link to setting up a virtual environment](https://python.land/virtual-environments/virtualenv)


First type in terminal

```bash
python -m venv venv
```

Then
```bash
# For MAC OS
source venv/bin/activate

# For Windows
venv/Scripts/activate
```

Then install the requirements:
```bash
pip install -r requirements.txt
```

You can then run the main.py script by 
```bash
python main.py
```

# To run development website

## Install independencies

```bash
cd client
npm install
```

## Run server

```bash
npm run dev
```
