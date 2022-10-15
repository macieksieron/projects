import java.awt.geom.Ellipse2D;


public class Field extends Ellipse2D.Double {

	public boolean isSelected = false;	
	public Player player = new Player();
	public double middleX, middleY;	// coordinates of the center of field

	public Field(double x, double y, double x1, double y1) {
		setFrameFromDiagonal(x, y, x1, y1);
		middleX = (x + x1) / 2;
		middleY = (y + y1) / 2;
	}

	public boolean isInside(double x, double y) {	// check if point (x,y) is inside a field
		return getBounds2D().contains(x, y);
	}

}