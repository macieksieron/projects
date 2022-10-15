import java.awt.geom.*;

public class SnakePiece extends Rectangle2D.Double
{
    String direction = "down";
    
    public SnakePiece(double x, double y, double size, String direction) 
    { 
        setFrame(x, y, size, size);
        this.direction = direction;
    }

    public void addX(double x) 
    {  
        this.x += x;
    }

    public void addY(double y) 
    {  
        this.y += y;
    }
    
    public boolean Overlaps(SnakePiece snake_piece) 
    {
        if(x < snake_piece.x + snake_piece.width && x + width > snake_piece.x && y < snake_piece.y + snake_piece.height && y + height > snake_piece.y)
            return true;
        else
            return false;
    }

    public boolean OverlapsApple(Apple apple) 
    {
        if(x < apple.getX() + apple.getWidth() && x + width > apple.getX() && y < apple.getY() + apple.getHeight() && y + height > apple.getY())
            return true;
        else
            return false;
    }

    public void move()
    {
        switch(direction)
        {
            case "up":
                addY(-width);
            break;
            case "down":
                addY(width);
            break;
            case "right":
                addX(width);
            break;
            case "left":
                addX(-width);
            break;
        }
    }
}