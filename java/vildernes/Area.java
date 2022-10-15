import javax.swing.*;
import java.awt.event.*;
import java.awt.*;

class Area extends JPanel 
{	
	Player player;
	JLabel background,background2;
	String location = "grass";
	NPC tavern,innkeeper;
	
	public Area()
    {
        setLayout(null);
        
        Action upAction = new UpAction();
		Action downAction = new DownAction();
		Action leftAction = new LeftAction();
		Action rightAction = new RightAction();
		
        player = new Player(100,100);
		add(player);
		tavern = new NPC(570,-70,163,228,"tavern.png");
		add(tavern);
		
		player.getInputMap().put(KeyStroke.getKeyStroke('w'), "w");
		player.getInputMap().put(KeyStroke.getKeyStroke('s'), "s");
		player.getInputMap().put(KeyStroke.getKeyStroke('a'), "a");
		player.getInputMap().put(KeyStroke.getKeyStroke('d'), "d");
		player.getActionMap().put("w", upAction);
		player.getActionMap().put("s", downAction);
		player.getActionMap().put("a", leftAction);
		player.getActionMap().put("d", rightAction);
		
		setBackground();
    }
	
	public void paintComponent(Graphics g)
    { 
		super.paintComponent(g);
		switchArea();
    }
	
	void switchArea()
	{
		switch(location)
		{
			case "grass":
				tavern.setVisible(true);
				if(player.getX()<0)
				{
					player.setLocation(1237,player.getY());
					setNewBackground("sand.png");
					location = "sand";
				}
				if(player.getX()>1237)
				{
					player.setLocation(0,player.getY());
					setNewBackground("ice.png");
					location = "ice";
				}
					
				if(player.getY()<135 && player.getX()>520 && player.getX()<700)
				{
					player.setLocation(620,590);
					setNewBackground("wood.png");
					location = "tavern";
				}
				
				if(player.getY()<0)
					player.setLocation(player.getX(),0);
				if(player.getY()>590)
				{
					player.setLocation(player.getX(),0);
					setNewBackground("stone.png");
					location = "stone";
				}
			break;
			
			case "sand":
				tavern.setVisible(false);
				if(player.getX()>1237)
				{
					player.setLocation(0,player.getY());
					setNewBackground("grass.png");
					location = "grass";
				}
				if(player.getX()<0)
					player.setLocation(0,player.getY());
				if(player.getY()<0)
					player.setLocation(player.getX(),0);
				if(player.getY()>590)
					player.setLocation(player.getX(),590);
			break;
			
			case "stone":
				tavern.setVisible(false);
				if(player.getX()>1237)
					player.setLocation(1237,player.getY());
				if(player.getX()<0)
					player.setLocation(0,player.getY());
				if(player.getY()<0)
				{
					player.setLocation(player.getX(),590);
					setNewBackground("grass.png");
					location = "grass";
				}
				if(player.getY()>590)
					player.setLocation(player.getX(),590);
			break;
			
			case "ice":
				tavern.setVisible(false);
				if(player.getX()>1237)
					player.setLocation(1237,player.getY());
				if(player.getX()<0)
				{
					player.setLocation(1237,player.getY());
					setNewBackground("grass.png");
					location = "grass";
				}
				if(player.getY()<0)
					player.setLocation(player.getX(),0);
				if(player.getY()>590)
					player.setLocation(player.getX(),590);
			break;
			
			case "tavern":
				tavern.setVisible(false);
				if(player.getX()>1237)
					player.setLocation(1237,player.getY());
				if(player.getX()<0)
					player.setLocation(0,player.getY());
				if(player.getY()<0)
					player.setLocation(player.getX(),0);
				if(player.getY()>590)
				{
					player.setLocation(620,200);
					setNewBackground("grass.png");
					location = "grass";
				}
			break;
		}
		
	}
	
	void setNewBackground(String file)
	{
		background.setIcon(new ImageIcon(Area.class.getResource(file)));
		background2.setIcon(new ImageIcon(Area.class.getResource(file)));
	}
	
	void setBackground()
	{
		background = new JLabel();
		background2 = new JLabel();
		
		background.setBounds(0, 0, 1300, 700);
		background2.setBounds(650, 0, 1300, 700);
		background.setIcon(new ImageIcon(Area.class.getResource("grass.png")));
		background2.setIcon(new ImageIcon(Area.class.getResource("grass.png")));
		add(background);
		add(background2);	
		
	}
	
	public class UpAction extends AbstractAction
    {
		public void actionPerformed(ActionEvent e) 
		{
			player.setLocation(player.getX(), player.getY()-20);
		}		
		
	}
    
	public class DownAction extends AbstractAction
	{
		public void actionPerformed(ActionEvent e) 
		{
			player.setLocation(player.getX(), player.getY()+20);
		}		
	}
	
	public class LeftAction extends AbstractAction
	{
		public void actionPerformed(ActionEvent e) 
		{
			player.setLocation(player.getX()-20, player.getY());
		}		
	}
	
	public class RightAction extends AbstractAction
	{
		public void actionPerformed(ActionEvent e) 
		{
			player.setLocation(player.getX()+20, player.getY());
		}		
	} 
}
