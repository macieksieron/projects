import java.awt.Color;
import java.net.ServerSocket;
import java.util.Scanner;
import java.util.concurrent.Executor;
import java.util.concurrent.Executors;
import java.util.ArrayList;

public class Server {   

    static ArrayList<Game.Client> clients;  
    static Game.Client client1,client2,client3,client4,client5,client6; 
    static Game game;  
    static Player player1,player2,player3,player4,player5,player6;	
    static ArrayList<Player> players; 

    public static void main(String[] args) throws Exception 
    {	
    	
        clients = new ArrayList<Game.Client>();
        players = new ArrayList<Player>();
        Scanner scanner = new Scanner(System.in);
        
        player1 = new Player();
		player2 = new Player();
		player3 = new Player();
		player4 = new Player();
		player5 = new Player();
		player6 = new Player();
		
        player1.setData(1,new Color(155,35,53));
		player2.setData(2,new Color(0,152,116));
		player3.setData(3,new Color(251,152,51));
		player4.setData(4,new Color(91,94,166));
		player5.setData(5,new Color(173,167,89));
		player6.setData(6,new Color(21,52,120));
		
        try (ServerSocket listener = new ServerSocket(58901)) {
            System.out.print("Number of players: ");
            int number_of_clients = Integer.parseInt(scanner.nextLine());	// read number of players needed to start  
            System.out.println("Server is Running...");
            Executor pool = Executors.newFixedThreadPool(6);	
            while (true) {  
                game = new Game();
                switch(number_of_clients)	// wait for all clients depending on number of clients needed to start
                {								//  add them to clients list, create a proper list of players and send it to game with set function
                    case 2:
                        client1 = game.new Client(listener.accept(), 1);
                        pool.execute(client1);
                        client1.number_of_clients = number_of_clients;
                        clients.add(client1);
                    
                        client2 = game.new Client(listener.accept(), 2);
                        pool.execute(client2);
                        client2.number_of_clients=number_of_clients;
                        clients.add(client2); 
                        
                        players.add(player1);
                        players.add(player2);                       
                        
                        game.set(number_of_clients,clients,players);
                    break;
                    case 3:
                        client1 = game.new Client(listener.accept(), 1);
                        pool.execute(client1);
                        client1.number_of_clients = number_of_clients;
                        clients.add(client1);
                    
                        client2 = game.new Client(listener.accept(), 2);
                        pool.execute(client2);
                        client2.number_of_clients=number_of_clients;
                        clients.add(client2);
    
                        client3 = game.new Client(listener.accept(), 3);
                        pool.execute(client3);  
                        client3.number_of_clients=number_of_clients;
                        clients.add(client3);   
                    
                        players.add(player1);
                        players.add(player2);
                        players.add(player3);
                        
                        game.set(number_of_clients,clients,players);
                    break;
                    case 4:
                        client1 = game.new Client(listener.accept(), 1);
                        pool.execute(client1);
                        client1.number_of_clients = number_of_clients;
                        clients.add(client1);
                    
                        client2 = game.new Client(listener.accept(), 2);
                        pool.execute(client2);
                        client2.number_of_clients=number_of_clients;
                        clients.add(client2);
    
                        client3 = game.new Client(listener.accept(), 3);
                        pool.execute(client3);  
                        client3.number_of_clients=number_of_clients;
                        clients.add(client3);   

                        client4 = game.new Client(listener.accept(), 4);
                        pool.execute(client4);  
                        client4.number_of_clients=number_of_clients;
                        clients.add(client4);   
                    
                        players.add(player1);
                        players.add(player2);
                        players.add(player3);
                        players.add(player4);

                        game.set(number_of_clients,clients,players);
                    break;
                    case 6:
                        client1 = game.new Client(listener.accept(), 1);
                        pool.execute(client1);
                        client1.number_of_clients = number_of_clients;
                        clients.add(client1);
                    
                        client2 = game.new Client(listener.accept(), 2);
                        pool.execute(client2);
                        client2.number_of_clients=number_of_clients;
                        clients.add(client2);
    
                        client3 = game.new Client(listener.accept(), 3);
                        pool.execute(client3);  
                        client3.number_of_clients=number_of_clients;
                        clients.add(client3);   

                        client4 = game.new Client(listener.accept(), 4);
                        pool.execute(client4);  
                        client4.number_of_clients=number_of_clients;
                        clients.add(client4);   
                    
                        client5 = game.new Client(listener.accept(), 5);
                        pool.execute(client5);  
                        client5.number_of_clients=number_of_clients;
                        clients.add(client5);   

                        client6 = game.new Client(listener.accept(), 6);
                        pool.execute(client6);  
                        client6.number_of_clients=number_of_clients;
                        clients.add(client6); 

                        players.add(player1);
                        players.add(player2);
                        players.add(player3);
                        players.add(player4);
                        players.add(player5);
                        players.add(player6);

                        game.set(number_of_clients,clients,players);
                    break;
                }
            }
        }
    }
}

