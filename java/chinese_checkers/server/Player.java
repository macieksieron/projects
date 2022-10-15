import java.awt.Color;
import java.util.List;
import java.util.ArrayList;

public class Player 
{
	public int number = 0;	
	public Color color = Color.WHITE;	
	public List<Field> corner = new ArrayList<Field>();	
	
	public void setData(int number, Color color)	
	{
		this.number=number;
		this.color = color;
	}
}
