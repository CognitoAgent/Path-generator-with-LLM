import subprocess
import os
import shutil
from driveService import DriveService
from sheetService import SheetService
import json
NRITERATIONS = 20

def getReplyFromConversation(index):
    with open("conversation.json", "r") as file:
        convo_data = json.load(file)

    assistant_messages = [msg["content"] for msg in convo_data if msg["role"] == "assistant"]
    
    if 0 <= index < len(assistant_messages):
        print('poruka, Vracamo '+assistant_messages[index])
        return assistant_messages[index]
    else:
        print('poruka, Vracamo none')
        return None #or maybe error?

class Tester:
    questions = []
    testName = ""
    idCounter = 0
    driveService = DriveService()
    sheetService = SheetService()
    mainFileName = ""

    def __init__(self, fileName):
        self.mainFileName = fileName
        

    def startNewSubprocess(self):
        env = os.environ.copy()
        env["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

        #start the target script with pipes for stdin and stdout
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.join(script_dir, self.mainFileName) #it makes sure it runs from the same folder

        self.process = subprocess.Popen(
            ['python', main_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  #text mode for easier string handling (no need for .encode/.decode)
            env=env
        )


    def cleanQuestions(self):
        self.questions.clear()

    def removeIfConversationFileExists(self):
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(scriptDir) #go one level up
        filePath = os.path.join(parentDir, "conversation.json")

        if os.path.exists(filePath):
            os.remove(filePath)
            print(f"T:{filePath} has been deleted.")
        else:
            print(f"T:{filePath} does not exist.")

    def removeIfConvImagesExists(self):
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        parentDir = os.path.dirname(scriptDir) #go one level up
        folderPath = os.path.join(parentDir, "convImages")

        if os.path.exists(folderPath) and os.path.isdir(folderPath):
            shutil.rmtree(folderPath)
            print(f"T:{folderPath} has been deleted.")
        else:
            print(f"T:{folderPath} does not exist.")

    def editGoogleSheet(self, iterNr):
        for counter, question in enumerate(self.questions, start=1):
            if(question != 'quit'):
                customName = str(self.testName) +'_Iter'+ str(iterNr) +'_Q'+ str(counter)
                imageLink = self.driveService.upload_image_to_folder('convImages/img'+str(counter)+'.png',customName)
                reply = getReplyFromConversation(counter-1)
                data = [self.testName, iterNr, counter, question, reply, imageLink]
                self.sheetService.updateWorksheet(data)


    def runTest(self):
        #if conversation.json file exists, delete it
        self.removeIfConversationFileExists()
        self.removeIfConvImagesExists()
        self.idCounter+=1

        self.startNewSubprocess()

        #communicate with the process line by line
        output = self.process.stdout.readline() #'Please input shape:'
        print(f"T:Received: {output.strip()}")
        for line in self.questions:
            print(f"T:Sending: {line}")
            self.process.stdin.write(line+ '\n')
            self.process.stdin.flush()

            if line.strip() != 'quit':
                #read one line of output in response
                output = self.process.stdout.readline()
                print(f"T:Received: {output.strip()}")

        #optionally, wait for the process to end
        self.process.wait()

    









if __name__=='__main__':
    
    with open('tests.txt', 'r') as file:
        addTestName = True
        for line in file:
            print("Line:"+line.strip())
            if not line.strip() or line.strip().startswith('//'):#comments
                continue
            elif line.strip()=='Test':
                tester = Tester('main.py')
                print('Created tester!')
                continue
            elif line.strip() == 'quit':
                tester.questions.append(line.strip())
                print('T:Found quit, the end of one test. Size of questions list:'+str(len(tester.questions)))
                #tester.questions.append('quit')
                
                for iter in range(NRITERATIONS):
                    tester.runTest()
                    tester.editGoogleSheet(iter+1)

                tester.cleanQuestions()
                addTestName = True
                
            elif addTestName:
                tester.testName = line.strip()
                addTestName = False
                tester.idCounter = 0
                #everything is on the same sheet
                
            elif line.strip()!='Test':
                tester.questions.append(line.strip())
                print('Line added to questions list')

    print('TESTING DONE')
    
