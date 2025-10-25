# Coding AI Agent
This is a simple version of a coding AI Agent. It is written in python and tries to solve your coding challenges. The working directory is currently set to /calculator, so feel free to play around with it. 

## Security Disclaimer

This AI Agent is not secure! You should not just use it for actual coding tasks. When wanting to try it out, be sure to only ask it simpler requests, as this coding agent can create a python file and the contents of that file are unchecked! It can then also exectue that file afterwards, so be careful! 


## Behavior
The coding agent takes a prompt and will then create a plan to tackle your given problem, which is printed to the user. The coding agent has 4 functionalities: 
1. Listing the contents of a directory, 
2. Reading the content of a file
3. Write/overwrite files
4. Run pyhon files. 

It will then exectue its functionalities and optionally adapt its plan. Finally, once the Agent is done wth the task or cannot progress any further, it will print one final text prompt to the user. The coding agent is limited to a maximum of 20 iterations in order to prevent him from running for an extended period of time. 

# Credits
This was a guided project from boot.dev. Thus, the high-level ideas were given, but what I really enjoyed that solving the coding challenges was done on your own, where one needed to look up the docs and design certain behaviors oneself. 
