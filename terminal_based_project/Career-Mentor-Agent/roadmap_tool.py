from agents import function_tool

@function_tool
def get_career_roadmap(field: str)-> str :
    maps={
        "software engineer":"learn python,DSA,web_dev,github, projects",
        "data scientist":"master python, pandas, ML, and realworld datasets",
        "graphic designer":"figma, photoshop, ui/ux design, portfolio ",
        "ai":"learn python, deep learning, transformers, and AI tools"
    }
    return maps.get(field.lower(),"no roadmap found for that field")