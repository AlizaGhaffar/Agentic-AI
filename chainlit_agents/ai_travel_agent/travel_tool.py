from agents import function_tool

@function_tool
def get_flight(destination:str)->str:
    return f"flight founds to {destination}: PKR 40000 TO 750000"

@function_tool
def suggest_hotel(destintion:str)-> str:
    return f"hotels in {destintion}: pearl continental, marriot, local guest houses"
