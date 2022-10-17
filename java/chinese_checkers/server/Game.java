import static java.lang.Math.pow;
import static java.lang.Math.sqrt;

import java.awt.Color;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.Random;

public class Game 
{
    int number_of_clients;	
    public ArrayList<Client> clients;
    public Board board;
    public int last_field=-1;	
    public ArrayList<Integer> winners;	 
    
    public void set(int number_of_clients,ArrayList<Client> clients,ArrayList<Player> players)
    {
        this.number_of_clients = number_of_clients;
        this.clients = clients;
        board = new Board(players);
        switch(number_of_clients)	// set target corner for every player depending on number of clients
        {

        case 2:
        	players.get(0).corner=board.corner4;
        	players.get(1).corner=board.corner1;
            break;
        case 3:
        	players.get(0).corner=board.corner4;
        	players.get(1).corner=board.corner6;
        	players.get(2).corner=board.corner2;
            break;
        case 4:
        	players.get(0).corner=board.corner5;
        	players.get(1).corner=board.corner6;
        	players.get(2).corner=board.corner2;
        	players.get(3).corner=board.corner3;
            break;
        case 6:
        	players.get(0).corner=board.corner4;
        	players.get(1).corner=board.corner5;
        	players.get(2).corner=board.corner6;
        	players.get(3).corner=board.corner1;
        	players.get(4).corner=board.corner2;
        	players.get(5).corner=board.corner3;
            break;
        }
        winners = new ArrayList<Integer>();	
    }

    public class Move 
    {
    	int from;
    	int to;
    	
    	public Move(int from, int to)
    	{
    		this.from = from;
    		this.to = to;
    	}
    }
    
    public class Client implements Runnable {
    	public Game game;
        int number; 
        Socket socket;
        Scanner input;
        PrintWriter output;
        public int number_of_clients;	
        public int currentPlayer;	
        
        public Client(Socket socket, int number) 
        {
            this.socket = socket;
            this.number = number;
        }
        
        public void move(int x, int y)	
    	{
            board.fields.get(y).player = board.fields.get(x).player;
            board.fields.get(x).player = new Player();
    	}
        
        public double d(double x, double y, double x1, double y1)  
    	{
    		return sqrt(pow(x1-x,2)+pow(y1-y,2));
    	}
    	 
    	public Field findField(double x, double y) // find field by coordinates
    	{
    		Player white = new Player();
    		Field field = new Field(0,0,0,0);
    		field.player=white;
    		 
            for(int i=0;i<board.fields.size();i++)
            {
                if(board.fields.get(i).middleX == x && board.fields.get(i).middleY == y)
                    return board.fields.get(i);
            }
            return field;
    	}
    	 
        public String isMoveLegal(int from, int to,int number)	// check if move is compliant with the rules
        {
        	boolean is_inside = false;	// is 'to-field' in target corner if 'for-field' is in target corner
        	for(int i=0;i<10;i++)
        	{
        		if(from+1==board.players.get(number-1).corner.get(i).number)	// if 'from-field' is in target corner..
        		{
        			for(int j=0;j<10;j++) // if 'to-field' is in target corner..
        			{
        				if(to+1==board.players.get(number-1).corner.get(j).number)
        				{
        					is_inside = true;		//.. set is-inside to true
        				}
        			}
        			if(is_inside==false)	// if 'to-field' is not in target corner and 'for-field' is in target corner..
        				return "0";	// return that move is not legal
        			is_inside=false;	//reset is_inside to default
        		}
        	}
        	// if it is this player's turn and he has his pawn on this field and he wants to move on empty field 
        	if(currentPlayer==number && board.fields.get(from).player.number == number && board.fields.get(from).player.color!=Color.WHITE 
        		&& board.fields.get(to).player.color==Color.WHITE)
        	{
        		// if we want to do legal move (without jump)
        		if(d(board.fields.get(to).middleX,board.fields.get(to).middleY,board.fields.get(from).middleX,board.fields.get(from).middleY)<=50)
        		{
        			return "1";
        		}
        		// if we want to do legal move (jump over other pawnO
        		else if(d(board.fields.get(to).middleX,board.fields.get(to).middleY,board.fields.get(from).middleX,board.fields.get(from).middleY)<=100
            		&& findField((board.fields.get(to).middleX+board.fields.get(from).middleX)/2,(board.fields.get(to).middleY+board.fields.get(from).middleY)/2).player.color!=Color.WHITE)
        		{
        			return "2";
        		}
        		// if move is illegal
        		else
        		{
        			return "0";
        		}
        	}
        	// if move is illegal
        	else
            {
            	return "0";
            }

        }
        
        public boolean doesPlayerWin(int number) 
        {
        	// for each field in target corner..
        	for(int i=0;i<10;i++)
        	{
        		// if this player has not pawn on this field then return false
        		if(board.players.get(number-1).corner.get(i).player.color!=board.players.get(number-1).color)
    				return false;
        	}
        	// if every field had pawn of this player return true
        	return true;
        }

        @Override
        public void run() 
        {
            try { 
                setup();
                processCommands();
            } catch (Exception e) {
                e.printStackTrace();
            } 
        }
        
        private void setup() throws IOException 
        {
            input = new Scanner(socket.getInputStream());
            output = new PrintWriter(socket.getOutputStream(), true);
            output.println(number_of_clients+"WELCOME PLAYER " + number);
            System.out.println("Player " + number + " has joined the game");
            if (number < number_of_clients) // if he is not last client who has to join..
                output.println("MESSAGE Waiting for opponents to connect"); 	// ..print info that he have to wait
            else // if he is last player to join..
            {
                Random rand = new Random();
                currentPlayer = rand.nextInt(number_of_clients)+1;	// ..choose random player to start
                System.out.println("The game has started");	
                
                System.out.println("Player " + currentPlayer + " starts");
                for(int i=0;i<clients.size();i++)	// for all clients..
                {
                    clients.get(i).currentPlayer=currentPlayer;	// ..set currentPlayer (who starts)
                    clients.get(i).output.println("TURN " + clients.get(i).currentPlayer); // send info to this client 
                    clients.get(i).output.println("MESSAGE Player " + clients.get(i).currentPlayer + " Turn"); // send message to client
                }
            }
        }

        private void processCommands() throws IOException 
        {
            while (input.hasNextLine()) 
            {
                String command = input.nextLine();
                if (command.startsWith("QUIT")) 
                    return;
                else if (command.startsWith("MOVE")) {	// client want to move

                    int from = Integer.parseInt(command.substring(5,8));	// get info about 'from-field'
	                int to = Integer.parseInt(command.substring(9,12));	// get info about 'for-field'
	                if(isMoveLegal(from,to,number)=="1" && last_field==-1) // if this move is legal and we have not JUMP in this turn (and do not JUMP now)
	                {
	                	move(from,to);	// move pawn 
	                    System.out.println("Player " + number + " moved from field " + from + " to field " + to);

	                    if(doesPlayerWin(number)==true)	// if player finieshed a game after this move
	                	{
	                    	winners.add(number);	// add him to list of winners
	                		System.out.println("Player " + number + " has finished game on " + winners.size() + ". place");
	                		for(int i=0;i<clients.size();i++)	// for each client..
	                		{
	                			clients.get(i).output.println("FINISH " + number);	// ..send info that he won
	                		}
	                		if(winners.size()==board.players.size()) // if everone has finished..
	                		{
	                			for(int i=0;i<clients.size();i++)	// ..for each client..
	    	                    {
	    	                        clients.get(i).output.println("MESSAGE GAME OVER");	// ..send info that game is over
	    	                    }
	                			
	                			for(int i=0;i<clients.size();i++)	// for each client
	    	                    {
	    	                        clients.get(i).output.println(command);	// send info where he moved
	    	                    }

	                			while(true)
	                			{
	                				
	                			}
	                		}
	                	}
	                    
	                    for(int i=0;i<clients.size();i++)	// for each client
	                    {
	                        clients.get(i).output.println(command);	// send info where he moved
	                    }

	                    int l = currentPlayer+1;		// next turn
	                    if(l==number_of_clients+1)		
	                        l=1;
	                    while(winners.contains(l)==true)	// if this player already finished his turn
	                    {
	                    	l++;
		                    if(l==number_of_clients+1)	
		                        l=1;
	                    }
	                 
	                    for(int i=0;i<clients.size();i++)	// for each client
	                    {
	                        clients.get(i).currentPlayer=l;	// set whose turn is now
	                        clients.get(i).output.println("MESSAGE Player " + clients.get(i).currentPlayer + " Turn");	// send message about it 
	                    }
	                    System.out.println("Player " + currentPlayer + " turn"); 
	                }
	                // if move is legal and we JUMP now (first time in this turn or with pawn we have jumped before in this turn)
	                else if(isMoveLegal(from,to,number)=="2" && (last_field==from || last_field==-1))
	                {
	                	move(from,to);	// move pawn
	                	last_field = to;	// set where we jumped 
	                    System.out.println("Player " + currentPlayer + " moved from field " + from + " to field " + to);
	                    
	                    if(doesPlayerWin(number)==true)	// if player finished after this jump
	                	{
	                    	winners.add(number);	// add him to list of winners
	                		System.out.println("Player " + number + " has finished game on " + winners.size() + ". place");
	                		for(int i=0;i<clients.size();i++)	// for each client
	                		{
	                			clients.get(i).output.println("FINISH " + number);	// send info about it
	                		}
	                		if(winners.size()==board.players.size())	// if everyone has finished
	                		{
	                			for(int i=0;i<clients.size();i++)	// for each client
	    	                    {
	    	                        clients.get(i).output.println("MESSAGE GAME OVER");	// send info that game is over
	    	                    }
	                			
	                			for(int i=0;i<clients.size();i++)	// for each client
	    	                    {
	    	                        clients.get(i).output.println(command);	// send info where he moved
	    	                    }
	                			while(true)
	                			{
	                				
	                			}
	                		}
	                	}
	                    
	                    //for each client
	                    for(int i=0;i<clients.size();i++)
	                    {
	                        clients.get(i).output.println("STILL_" + command);	// send info we JUMPED
	                    }
	                }
	                else {
	                	for(int i=0;i<clients.size();i++)
	                    {
	                        output.println("WRONG");	// send info about wrong move
	                    }
	                }
                }
                else if (command.startsWith("SKIP") && number==currentPlayer) // client want to skip/end turn
                {
                    for(int i=0;i<clients.size();i++)	//for each client
                    {
                        clients.get(i).output.println("SKIP");	// send info to do nextTurn() on his board
                    }
                    
                    last_field = -1;	// reset last_field to default

                    System.out.println("Player " + currentPlayer + " has ended his turn");
                    int l = currentPlayer+1;	// next turn
                    if(l==number_of_clients+1)
                        l=1;
                    
                    while(winners.contains(l)==true)	// if this player already finished skip his turn
                    {
                    	l++;
	                    if(l==number_of_clients+1)
	                        l=1;
                    }
                     
                    for(int i=0;i<clients.size();i++)	// for every client
                    {
                        clients.get(i).currentPlayer=l;		//set whose turn is now
                        clients.get(i).output.println("MESSAGE Player " + clients.get(i).currentPlayer + " Turn");	// and send communicate about it
                    } 
                    System.out.println("Player " + currentPlayer + " turn"); 
                }
            }
        }

    }
}

