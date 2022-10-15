import java.awt.geom.Ellipse2D;

public class Field extends Ellipse2D.Double  
{
    public boolean isSelected = false;	
    public Player player = new Player();	
    public double middleX;	
	public double middleY;
    int number;	
    
    public Field(double x, double y, double x1, double y1) 
    {
        setFrameFromDiagonal(x,y,x1,y1);
        middleX = (x+x1)/2;
        middleY = (y+y1)/2;
    }

    public boolean isInside(double x, double y)	
    {    
        return getBounds2D().contains(x, y);
    }

}