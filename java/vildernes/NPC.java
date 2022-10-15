import javax.swing.*;

class NPC extends JLabel
{
	public NPC(int x, int y, int width, int height, String file)
	{
		setLocation(x,y);
		setSize(width, height);
		setIcon(new ImageIcon(Area.class.getResource(file)));
	}
}
