import xmlrpc.client
#While loop to run the program
while(True):
    #Get the user's choice of action
    print("\n1 Write a new notebook entry\n2 Search for a notebook entry by topic\n3 Lookup data on wikipedia\n0 Quit\n")
    choice = input("Choose option: ")
    #Add a new note, ask for topic, note name and content.
    if(choice == "1"):
        topic = input("Give a topic for the entry: ")
        note = input("Give your note a name: ")
        content = input("Write the content for the entry: ")
        #Try to use the RPC save_note function
        try:
            with xmlrpc.client.ServerProxy("http://localhost:3000/") as proxy:
                if(proxy.save_note(topic, note, content)):
                    print("Note saved succesfully")
                else:
                    print("Something went wrong :/")
        except xmlrpc.client.Fault as err:
            print("Fault code: %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)

    #Search for notes by topic
    elif(choice == "2"):
        #Get the user's choice of topic
        searchable_topic = input("Give topic name to search: ")
        #Try to use the RPC search_by_topic function
        try:
            with xmlrpc.client.ServerProxy("http://localhost:3000/") as proxy:
                print(proxy.search_by_topic(searchable_topic))
        except xmlrpc.client.Fault as err:
            print("Fault code: %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)

    #Query wikipedia
    elif(choice == "3"):
         #Get the user's choice of searchterm
        searchable_topic = input("Give searchterm to search for from wikipedia: ")
        #Try to use the RPC query wikipedia api function
        try:
            with xmlrpc.client.ServerProxy("http://localhost:3000/") as proxy:
                result = proxy.query_wikipedia_api(searchable_topic)
                #The wikipedia api returns lists with lists
                #We want the first entries of the title list and the url list
                print(result[1][0], result[3][0],  "\n")
        except xmlrpc.client.Fault as err:
            print("Fault code: %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)

        if(result):
        #Check if the user wants to input the data to the database
            if(int(input("Do you want to save the result to the database?\n1 Yes \n0 No\nChoose option: "))):
                #If so, ask the user for a topic and use the RPC save_note function to save the data as a note
                topic = input("Give a topic name for the results: ")
                try:
                    with xmlrpc.client.ServerProxy("http://localhost:3000/") as proxy:
                        if(proxy.save_note(topic, result[1][0], result[3][0])):
                            print("Note saved succesfully")
                        else:
                            print("Something went wrong :/")
                except xmlrpc.client.Fault as err:
                    print("Fault code: %d" % err.faultCode)
                    print("Fault string: %s" % err.faultString)

    #Exit the program
    elif(choice == "0"):
        print("Exiting...")
        exit()
    #User gave wrong input
    else:
        print("Invalid input, try again.\n")