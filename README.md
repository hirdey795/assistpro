# [Assistpro](https://assistpro-test.vercel.app)
## AssistPro is a comprehensive web tool designed to simplify the process of identifying class articulations across various colleges and universities. It is particularly useful for students planning to transfer and needing to find equivalent courses at their new institution.

---

# TODO:
- [ ] Update/Format Website with features, look into this ![layout](https://github.com/hirdey795/assistpro/blob/main/Extra_README/README_LAYOUT.md)
- [x] Scrape all UNI/CSU Classes
- [ ] Return all classes from colleges which are available for the selected class that the user picked. (Frontend/Backend Communication)
- [x] Make scraping headless optional (not need window popup everytime we scrape)
- [ ] FastAPI / Flask ?

# [Website](https://assistpro-test.vercel.app)

# DEMO OF SCRAPING
![GIF](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcHRpbWw1em00MHh4OGxuYW9heHBkajg4eGxyNjZuZHB2N3Bpa2loNSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QpDKozmCN3XGi2YHBV/giphy.gif)

# Progress:

Got data for EECS Major articulation for UC Berkeley from Sacramento City College (SCC) compared to Diablo Valley College

Diablo Valley College has courses that articulates which SCC does not, therefore students can take theses classes to be more competitive

```json
{
    "('To: University of California, Berkeley', 'From: Diablo Valley College')": [
        "Electrical Engineering & Computer Sciences, Lower Division B.S.",
        {
            "MATH 1A": "MATH 192",
            "MATH 1B": "MATH 193",
            "MATH 53": "MATH 292",
            "MATH 54": "MATH 194",
            "PHYSICS 7A": "PHYS 130",
            "PHYSICS 7B": "PHYS 230",
            "ENGLISH R1A": "ENGL 122",
            "ENGLISH R1B": "ENGL 123",
            "ASTRON 7A": "No Course Articulated",
            "ASTRON 7B": "No Course Articulated",
            "BIOLOGY 1A": "BIOSC 130",
            "BIOLOGY 1B": "BIOSC 131",
            "CHEM 1A": "CHEM 120",
            "CHEM 1B": "CHEM 121",
            "CHEM 3A": "CHEM 226",
            "CHEM 3B": "CHEM 227",
            "MCELLBI 32": "BIOSC 120",
            "PHYSICS 7C": "PHYS 231",
            "COMPSCI 61A": "No Course Articulated",
            "COMPSCI 61B": "COMSC 210",
            "COMPSCI 61C": "COMSC 260",
            "COMPSCI 70": "This course must be taken at the university after transfer",
            "EECS 16A": "No Course Articulated",
            "EECS 16B": "No Course Articulated"
        }
    ],
    "('To: University of California, Berkeley', 'From: Sacramento City College')": [
        "Electrical Engineering & Computer Sciences, Lower Division B.S.",
        {
            "MATH 1A": "MATH 400",
            "MATH 1B": "MATH 401",
            "MATH 53": "MATH 402",
            "MATH 54": "MATH 420",
            "PHYSICS 7A": "PHYS 410",
            "PHYSICS 7B": "PHYS 420",
            "ENGLISH R1A": "ENGWR 300",
            "ENGLISH R1B": "ENGWR 301",
            "ASTRON 7A": "No Course Articulated",
            "ASTRON 7B": "No Course Articulated",
            "BIOLOGY 1A": "BIOL 402",
            "BIOLOGY 1B": "BIOL 412",
            "CHEM 1A": "CHEM 400",
            "CHEM 1B": "CHEM 401",
            "CHEM 3A": "CHEM 420",
            "CHEM 3B": "CHEM 421",
            "MCELLBI 32": "BIOL 430",
            "PHYSICS 7C": "PHYS 430",
            "COMPSCI 61A": "No Course Articulated",
            "COMPSCI 61B": "CISP 430",
            "COMPSCI 61C": "No Course Articulated",
            "COMPSCI 70": "This course must be taken at the university after transfer",
            "EECS 16A": "No Course Articulated",
            "EECS 16B": "No Course Articulated"
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

# To run website

## Install independencies

```bash
cd client
npm install
```

## Run server

```bash
npm run dev
```
