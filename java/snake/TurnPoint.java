public class TurnPoint 
{	
	String direction;
	boolean isOn = true;
	double x,y;
	
	public TurnPoint(double x,double y,String direction)
	{
		this.x = x;
		this.y = y;
		this.direction = direction;
	}
	
	public String getDirection()
	{
		return direction;
	}
}
