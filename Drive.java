package com.team766.robot.Actors.Drive;

//Put imports here
import lib.*;

public class Drive extends Actor{
	
	//Instantiate local instances of hardware here from the HardwareProvider instance

	private boolean commandFinished;
	private Message currentMessage;
	private SubActor currentCommand;
	
	public void init() {
		//Put all the messages this Actor will recieve and process here
		acceptableMessages = new Class[]{};

		//Instantiate variables below
		commandFinished = false;
	}

	public void iterate(){
		
		//Check for new messages
		if(newMessage()){
			stopCurrentCommand();
			commandFinished = false;
			
			currentMessage = readMessage();
			
			if(currentMessage == null)
				return;
				

			//Cascading if statments to determine which message was recieved
			/*
			if(currentMessage instanceof Message1){				
				//Do something
			}
			else if(currentMessage instanceof Message2)
				currentCommand = new Message2SubCommand(currentMessage);
			else if(currentMessage instanceof Message3)
				currentCommand = new Message3Command(currentMessage);
			*/

		}
					
		step();
		
		//Send Status update message for this Actor
		//sendMessage(new StatusUpdate(commandFinished, currentMessage, other variables...);

		//Update local variables
		//updateVariableX();
		
//		itsPerSec++;
	}
	
	public void run() {
		while(enabled){	
			iterate();
			sleep();
		}
		
		//Stop all processes
		stopCurrentCommand();
	}
	
	public void step(){
		if(currentCommand != null){
			if(currentCommand.isDone()){
				stopCurrentCommand();
			}else{
				currentCommand.update();
			}
		}
	}
	
	private void stopCurrentCommand(){
		if(currentCommand != null){
			currentCommand.stop();

			//Send update message that current message has finished being processed
			//sendMessage(new StatusUpdate(true, currentMessage, other variables...));
		}
		currentCommand = null;
		commandFinished = true;
	}
	
	
	// Methods to update local variables

	//Protected getter methods
	
	//Protected setter methods
	
	//Protected reset methods
	
}