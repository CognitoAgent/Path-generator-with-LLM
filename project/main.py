import openai
import os
import json
import sys
from coordObjects import Coordinate, CoordinatesResponse
from displayCoord import display3Views

openai.api_key = os.getenv('OPENAI_API_KEY')
CONVERSATION_FILE = "conversation.json"

lastGivenCoordinates = ""

def save_conversation(newMessage):
    conversation = load_conversation()
    conversation.append(newMessage)
    with open(CONVERSATION_FILE, "w") as f:
        json.dump(conversation, f, indent=2)

def load_conversation():
    if os.path.exists(CONVERSATION_FILE):
        with open(CONVERSATION_FILE, "r") as f:
            return json.load(f)
    else:

        developerMessage={"role": "system", "content": 
                "You are a geometric-shape generator; Generate a set of three-dimensional coordinates that form the requested shape."
                
                "General rules:"
                "1. Specify if the shape is two-dimensional or three-dimensional."
                "1.1 If the shape is two-dimensional, orient them parallel to the xz-plane (unless specified otherwise)."
                "1.2 If the shape is three-dimensional, ensure the base is parallel to the xy-plane (unless specified otherwise)."
                "2. If the shape is continuous, closed (i.e., has no distinct endpoints, like a circle or a polygon), ensure that the path is closed by making the last coordinate the same as the first coordinate."
                "4. For shapes that do not belong to a set of elementary (or fundamental) geometric shapes (fundamental geometric shapes are for example circle, triangle, rectangle, circle) we will call 'complex shapes'."
                "4.1 Example of complex shapes: star, heart, swirl, cross, arrow."
                "4.2 For complex shapes, provide a detailed set of coordinates that capture the shape's features (for example, petals or curves) rather than a basic outline."

                "5. Here's an example request: 'Generate coordinates for a 2D triangle, base parallel to the xz-plane'."
                "6. You can only use one rule from the 'Decision tree'. You must specify which rule you used in response!"
                

                "Decision tree:"
                "1. Try to identify or derive a suitable mathematical equation (parametric, polar, implicit, or piecewise) whose graph represents that shape."
                "1.2 If found, sample enough points from that equation to produce a smooth, recognizable outline."

                "2. Find analytic decomposition (lines, arcs, Béziers) and sample it."
                "2.1 For complex shapes, make sure they have their curves and points (for example, heart has symmetrical curves and point at a bottom)."
                "3. If first and second rule were both not applicable, give your own idea and then return coordinates from that idea"
                
                }
        conversation = [developerMessage]
        with open(CONVERSATION_FILE, "w") as f:
            json.dump(conversation, f, indent=2)
        
        return [developerMessage]
            

def storeAssistantMessage(response):
    global lastGivenCoordinates
    #store given coordinates in lastGivenCoordinates string
    sb = ""
    for step, coord in enumerate(response.pathCoord, start=0):
        sb = sb + f"({str(coord.xCoord)}, {str(coord.yCoord)}, {str(coord.zCoord)}), "

    lastGivenCoordinates = sb.rstrip(', ')  #update the global variable and remove trailing comma
    #we have now stored last given coordinates

    assistant_message = {
    "role": "assistant",
    "content": response.final_answer
    }
    save_conversation(assistant_message)
    return

def storeUserMessage(response):
    user_message = {
    "role": "user",
    "content": response + " These are the last received coordinates: "+lastGivenCoordinates
    }
    save_conversation(user_message)
    return

def getAssistantMessage():
    conversation = load_conversation()    
    completion = openai.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=conversation,
        response_format=CoordinatesResponse,
    )

    chatResponse = completion.choices[0].message.parsed
    storeAssistantMessage(chatResponse)
    return chatResponse

def printOutput(chatResponse):
    for step, coord in enumerate(chatResponse.pathCoord, start=0):
        print(f"Coordinate number {step}:")
        print(f"--({coord.xCoord}, {coord.yCoord}, {coord.zCoord}")
        print()

    print(f"Final answer from chatgpt: {chatResponse.final_answer}")
    return

if __name__=='__main__':
    load_conversation() #input developer's message

    print("Please input shape:")
    inputText = input() if sys.stdin.isatty() else sys.stdin.readline().strip()


    storeUserMessage(inputText)


    while True:
        chatResponse = getAssistantMessage()
        printOutput(chatResponse)
        display3Views(chatResponse.pathCoord)

        print("Would you like to modify the shape? (Type your modification or 'quit' to exit)")
        modification = input().strip() if sys.stdin.isatty() else sys.stdin.readline().strip()
        #script is being run interactively in a terminal (TTY); user is directly typing into terminal
        #or, reads line from a standard input stream directly, the input is directed or piped in

        if modification.lower() in ["quit", "exit"]:
            break

        storeUserMessage(modification)

    print("Exiting the program")






