import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

class MyJPanel extends JPanel implements KeyListener
{
    Random rand = new Random();
    
    int speed;      	// snake's speed
    int size = 20;      // snake's one piece size
    int lenght = 3;     // number of snake's pieces
    int apple_size = 10; // apple size
    int max_speed = 40;  // max snake's speed
    
    ArrayList<TurnPoint> turn_points = new ArrayList<>();	// list of TurnPoints
    ArrayList<SnakePiece> snake_pieces = new ArrayList<>();   // list of SnakePieces
    
    Apple apple; 
    
    MyJPanel()
    {
    	setBounds(10,10,780,560); 
    	setFocusable(true);
        addKeyListener(this);
        setBorder(BorderFactory.createLineBorder(Color.BLACK));
        setLayout(null);
        
        apple = new Apple(rand.nextInt(780-apple_size),rand.nextInt(550-apple_size),apple_size); 
        
        // set start position of snake with 'down' direction
        for(int i=0;i<lenght;i++)
        {
            snake_pieces.add(new SnakePiece(0,(lenght-1-i)*size, size, "down"));
        }
    }

    public void paintComponent(Graphics graphics) 
    {      
        super.paintComponent(graphics);
        Graphics2D My2DGraphics = (Graphics2D) graphics;

        My2DGraphics.setPaint(Color.RED);	
        My2DGraphics.fill(apple);						
        My2DGraphics.setPaint(Color.BLACK);		

        for(int i=0;i<lenght;i++) 
        {
            for(int j=0;j<turn_points.size();j++) 
            { 
            	// change snake's piece direction if hits a TurnPoint
                if(snake_pieces.get(i).x==turn_points.get(j).x && snake_pieces.get(i).y==turn_points.get(j).y)
                {
                    snake_pieces.get(i).direction = turn_points.get(j).direction;
                    // remove TurnPoint if whole snake changed direction
                    if(i==lenght-1)     
                    	turn_points.remove(j);
                }
            }

            snake_pieces.get(i).move();
            
            // what happens when snake goes out of the map
            if(snake_pieces.get(i).x < 0)
            	snake_pieces.get(i).x = 780-size;
            if(snake_pieces.get(i).x > 780-size)
            	snake_pieces.get(i).x = 0;
            if(snake_pieces.get(i).y < 0)
            	snake_pieces.get(i).y = 560-size;
            if(snake_pieces.get(i).y > 560-size)
            	snake_pieces.get(i).y = 0;;
           
            
            My2DGraphics.draw(snake_pieces.get(i));    
        }
        
        if(snake_pieces.get(0).OverlapsApple(apple))  // if snake eats an apple
        {
        	apple = new Apple(rand.nextInt(780-10),rand.nextInt(550-10),10); // change apple location
        	
        	// size up
            if(snake_pieces.get(lenght-1).direction == "down")
            	snake_pieces.add(new SnakePiece(snake_pieces.get(lenght-1).x,snake_pieces.get(lenght-1).y-size,size,"down"));  
            if(snake_pieces.get(lenght-1).direction == "up")
            	snake_pieces.add(new SnakePiece(snake_pieces.get(lenght-1).x,snake_pieces.get(lenght-1).y+size,size,"up")); 
            if(snake_pieces.get(lenght-1).direction == "right")                                                   
            	snake_pieces.add(new SnakePiece(snake_pieces.get(lenght-1).x-size,snake_pieces.get(lenght-1).y,size,"right")); 
            if(snake_pieces.get(lenght-1).direction == "left")
            	snake_pieces.add(new SnakePiece(snake_pieces.get(lenght-1).x+size,snake_pieces.get(lenght-1).y,size,"left")); 
            
            speed++;    // speed up snake
            lenght++;   // update length 
        }
        
        if(speed>max_speed)
        	speed--;

        // when snake eats one of itself's pieces
        for(int i=1;i<lenght;i++)
        {
            if(snake_pieces.get(0).Overlaps(snake_pieces.get(i)))
            {		
                    // GAME OVER
            		setBackground(Color.RED);
                	repaint();
            }
        }
        
        try
        {
        Thread.sleep(100-speed*2);
        }
        catch(InterruptedException ex)
        {
            Thread.currentThread().interrupt();
        }
        
        repaint();
    }

    public void keyPressed(KeyEvent e) //set turning points when pressing arrow keys
    {
        int keyCode = e.getKeyCode();
        switch(keyCode) 
        { 
            case KeyEvent.VK_UP:
                if(snake_pieces.get(0).direction!="down" && snake_pieces.get(0).direction!="up")
                	turn_points.add(new TurnPoint(snake_pieces.get(0).getX(), snake_pieces.get(0).getY(),"up"));
            break;
            case KeyEvent.VK_DOWN:
                if(snake_pieces.get(0).direction!="up" && snake_pieces.get(0).direction!="down")
                	turn_points.add(new TurnPoint(snake_pieces.get(0).getX(), snake_pieces.get(0).getY(),"down"));
            break;
            case KeyEvent.VK_RIGHT:
            	if(snake_pieces.get(0).direction!="left" && snake_pieces.get(0).direction!="right")
            		turn_points.add(new TurnPoint(snake_pieces.get(0).getX(), snake_pieces.get(0).getY(),"right"));
            break;
            case KeyEvent.VK_LEFT:
            	if(snake_pieces.get(0).direction!="right" && snake_pieces.get(0).direction!="left")
            		turn_points.add(new TurnPoint(snake_pieces.get(0).getX(), snake_pieces.get(0).getY(),"left"));
            break;
        }
    }  
    
    public void keyReleased(KeyEvent e) {}
    public void keyTyped(KeyEvent e) {} 
}