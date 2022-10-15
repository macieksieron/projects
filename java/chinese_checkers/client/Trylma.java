import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.awt.Color;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.swing.JFrame;

public class Trylma 
{
    public List<Player> players = new ArrayList<Player>(); 
	Player player1,player2,player3,player4,player5,player6;
    private Socket socket;
    private Scanner in;
    private PrintWriter out;
    JFrame frame;
    int finished = 0;
    int my_number;	
    Game panel;	
    
    public Trylma() throws Exception 
	{
    	player1 = new Player();	
		player2 = new Player();
		player3 = new Player();
		player4 = new Player();
		player5 = new Player();
		player6 = new Player();
		
		frame = new JFrame("Trylma");
		frame.setResizable(false);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.getContentPane().setBackground(Color.WHITE);
        
        // Setting number and color for players
		player1.setData(1,new Color(155,35,53));	
		player2.setData(2,new Color(0,152,116));
		player3.setData(3,new Color(251,152,51));
		player4.setData(4,new Color(91,94,166));
		player5.setData(5,new Color(173,167,89));
		player6.setData(6,new Color(21,52,120));
		
        socket = new Socket("127.0.0.1", 58901);
        in = new Scanner(socket.getInputStream());
        out = new PrintWriter(socket.getOutputStream(), true);

        frame.setBounds(100,100,700,680); 
        
        }
    
    public void play() throws Exception 
	{
	        try
			{
	            String response = in.nextLine();	 // last sign of 'WELCOME' message is unique number for every client         
	            char number = response.charAt(16); 	
	            frame.setTitle("Trylma: Player " + number);	 // first sign of 'WELCOME' message is number of players needed for this game
	            int number_of_players = Character.getNumericValue(response.charAt(0));  // set players list depending on number of players
	          
	            switch(number_of_players)	
	            {
	            case 2:
	            	players.add(player1);
	        		players.add(player2);
	        		break;
	            case 3:
	            	players.add(player1);
	        		players.add(player2);
	        		players.add(player3);
	        		break;
	            case 4:
	            	players.add(player1);
	        		players.add(player2);
	        		players.add(player3);
	        		players.add(player4);
	        		break;
	            case 6:
	            	players.add(player1);
	        		players.add(player2);
	        		players.add(player3);
	        		players.add(player4);
	        		players.add(player5);
	        		players.add(player6);
	        		break;
	            }
	            
	            Board board = new Board(players); 	// create board depending on players list
	            panel = new Game(board,out);
	            frame.add(panel);
	            frame.setVisible(true);
	            my_number = number;	// set my_number
	            panel.setMyNumber(my_number);	// send my_number to panel
	            panel.skip.setBackground(players.get(my_number-49).color);
	            
	            while (in.hasNextLine()) 
	            {
	                response = in.nextLine();
	                if (response.startsWith("MOVE"))	// when someone moves, but does not jump over other pawn 
	                {
	                	if(panel.isMuted==false && panel.board.turn==my_number-48)
	                		playSound("click.wav");
	                	int from = Integer.parseInt(response.substring(5,8));	// get "from-field" from MOVE message
	                	int to = Integer.parseInt(response.substring(9,12));	// get "for-field" from MOVE message
	                	panel.move(from,to); // move pawns on board
	                	panel.board.nextTurn();	// next player's turn
	                } 
	                else if (response.startsWith("STILL_")) // when someone jumps over other pawn
	                {
	                	if(panel.isMuted==false && panel.board.turn==my_number-48)
	                		playSound("click.wav");
	                	int from = Integer.parseInt(response.substring(11,14)); // get "from-field" from MOVE message
	                	int to = Integer.parseInt(response.substring(15,18));	// get "for-field" from MOVE message
	                	panel.move(from,to); // move pawns on board
	                } 
	                else if (response.startsWith("FINISH ")) // when someone finished the game
	                {
	                	int who = Integer.parseInt(Character.toString(response.charAt(7)));	// get info who finished
	                	finished++;	// increment variable with number of players which has finished
	                	panel.score.get(finished-1).setText(finished + ". place:    Player " + who); // print info, that someone has finished on score-board
	                
	                } 
	                else if (response.startsWith("MESSAGE")) // when server send us a message to print on screen
	                {
	                    panel.messege.setText(response.substring(8));	// get this message and print it
	                	
	                } 
	                else if (response.startsWith("WRONG")) // when someone do the wrong move
	                {
	                	if(panel.isMuted==false)	// play proper sound
	                		playSound("wrong.wav");
	                	
	                } 
	                else if (response.startsWith("TURN")) // when server want to set who starts the game
	                {
	                	panel.board.turn = Integer.parseInt(String.valueOf(response.charAt(5))); // get number from message and set turn to this number
	                
	                } 
	                else if (response.startsWith("SKIP")) // when someone skipped/end his turn
	                {
	                	if(panel.isMuted==false && panel.board.turn==my_number-48)
	                 		playSound("skip.wav");	// play proper sound
	                }
	            }
	            out.println("QUIT");	
	        } 
			catch (Exception e) 
			{
				e.printStackTrace();
			} 
			finally 
			{
			socket.close();
			frame.dispose();
			}
	}
    
    public void playSound(String soundName)	
	{
		try 
		{
			AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new File(soundName).getAbsoluteFile( ));
			Clip clip = AudioSystem.getClip( );
			clip.open(audioInputStream);
			clip.start( );
		}
		catch(Exception ex)
		{
			System.out.println("Error with playing sound.");
			ex.printStackTrace( );
		}
	}

    public static void main(String[] args) throws Exception {
        Trylma client = new Trylma();
        client.play();
    }
}
