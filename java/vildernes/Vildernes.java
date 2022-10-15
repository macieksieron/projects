import javax.swing.*;

public class Vildernes extends JFrame
{
	public Vildernes()
	{
		super("Vildernes");
		setResizable(false);
        setBounds(70,60,1300,700);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        Area area = new Area();
        getContentPane().add(area);
        setVisible(true);
	}
	
	public static void main(String[] args)
	{
		Vildernes Vildernes = new Vildernes();
	}

}
