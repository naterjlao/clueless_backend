#!/usr/bin/python3

# TODO import
import json
################################################################################
# File: clueless
# Language: python3
# Author: Nate Lao (nlao1@jh.edu)
# Date Created: 4/12/2020
# Description:
#          Listener thread to catch input data from stdin and print output to stdout.
#
# Detailed Description:
#
#          ############### Backend -> Serverside -> Frontend ###############
#          The JSON data that is sent to the ServerSide must be in the following
#          format:
#          {
#               playerID: "all" or <playerID>,
#               eventName: <string>,
#               payload: {}
#          }
#          Where:
#              -playerID : the target player ID string to be sent
#              -eventName : the string action that corresponds to the eventName
#                           signature expected by the player
#              -payload : a dictionary (JSON) to sent to the player(s)
#
#          ############### Frontend -> Serverside -> Backend ###############
#          The JSON data that is sent to the Backend (this) is expected to be in 
#          the following format:
#          {
#               playerID: <playerID>,
#               eventName: <string>,
#               payload: {}
#          }
#          Where:
#              -playerID : the player ID that sent the signal
#              -eventName : the string action that corresponds to the eventName
#                           signature made by the player
#              -payload : a dictionary (JSON) to sent to the player(s)
#
################################################################################

################################################################################
# AUXILIARY FUNCTIONS
################################################################################

# Shoots <sendData> for the <eventName> to Serverside for the lucky Client
# that is associated with <playerID>
def sendToPlayer(playerID,eventName,sendData):
    signal = {
        'playerID': playerID,
        'eventName': eventName,
        'payload':sendData
        }
    print(json.dumps(signal),flush=True) # Spit out to stdout!

# Shoots <sendData> for the <eventName> to Serverside for all Clients
def sendToAll(eventName,sendData):
    sendToPlayer("all",eventName,sendData)

# TODO this might be temporary
def nextTurn: # TODO
    pass
    
################################################################################
# INSTANCE VARIABLES
################################################################################

# Stores the player IDs that sent the request
playerIDs = []

#### TODO --- THIS IS TEMPORARY replace with actual game objects ----- #######
# Create variables that is stored at runtime for this process
position = {x:100,y:100}
current_turn = 0 # start at the first player
#### TODO --- THIS IS TEMPORARY replace with actual game objects ----- #######





################################################################################
# MAIN
################################################################################
if __name__ == "__main__": # Safeguard against accidental imports
    # Spinup a listener, this will be killed when the Serverside application is killed
    while True:
        # Raw signal from the ServerSide
        recieve = input()
        recieve = recieve.strip()
        data = json.loads(recieve) # data is coverted to a dictionary
        
        # Payload signal to the Clients
        send = {}
        
        ########## NOTE -- these might be temporary!!!! ##########
        # NOTE -- THESE CORRESPOND TO THE CLIENT -> SERVER eventName SIGNATURE in server.service.ts (frontend)
        # Handler for enteredGame()
        if data.eventName == "enteredGame":
            pass
            
        # Handler for move()
        elif data.eventName == "move":
            if data.payload == "left":
                position.x += position.x - 5
            if data.payload == "right":
                position.x += position.x + 5
            if data.payload == "up":
                position.y += position.y - 5
            if data.payload == "down":
                position.y += position.y + 5
            sendToAll('move',position)
                
        # Handler for endTurn()
        elif data.eventName == "pass_turn":
            pass
        
        # Handler for removeSocket()
        elif data.eventName == "disconnect":
            pass
        
        ########## NOTE -- these might be temporary!!!! ##########
