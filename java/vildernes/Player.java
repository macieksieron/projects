import javax.swing.*;

class Player extends JLabel
{
	public Player(int x, int y)
	{
		setLocation(x,y);
		setSize(63, 83);
		setIcon(new ImageIcon(Area.class.getResource("player.png")));
	}
}
