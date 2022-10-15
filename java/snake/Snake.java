import javax.swing.*;

public class Snake extends JFrame 
{	
    public Snake() 
    {
        super("Snake");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(300,100,800,610);
	    setResizable(false);
	    setVisible(true);
        MyJPanel panel = new MyJPanel();
        add(panel);
    }
    
    public static void main(String[] args) 
    {
        Snake Snake = new Snake();
    }
}
