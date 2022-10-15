import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.awt.geom.*;

public class MyJPanel extends JPanel
{
    Point2D[] points;
    MyRectangle[] rectangles;
    MyEllipse[] ellipses;
    MyTriangle[] triangles;
    public int howManyRectangles=0;
    public int howManyEllipses=0;
    public int howManyTriangles = 0;
    String str;
    boolean isSwitched = false;

    public void changeStr(String str)
    {
        this.str = str;
    }

    public void changeIsSwitched(boolean bool)
    {
        isSwitched = bool;
    }

    public MyJPanel()
    {
        setBackground(Color.WHITE);
        MyMouseAdapter mouseAdapter = new MyMouseAdapter();
        addMouseListener(mouseAdapter);
        addMouseMotionListener(mouseAdapter);
        addMouseWheelListener(new MyMouseWheelListener());

        points = new Point2D[2];
        rectangles = new MyRectangle[100];
        ellipses = new MyEllipse[100];
        triangles = new MyTriangle[100];
    } 

    @Override
    public void paintComponent(Graphics g) 
    {       
        super.paintComponent(g);
        Graphics2D My2DGraphics = (Graphics2D) g;
        My2DGraphics.setPaint(new Color(0, 0, 0));
        My2DGraphics.setStroke(new java.awt.BasicStroke(2));

        for(int i=0;i<howManyRectangles;i++)
        {
            if(rectangles[i].isSelected == true)
                My2DGraphics.setStroke(new java.awt.BasicStroke(4));
            My2DGraphics.draw(rectangles[i]);
            My2DGraphics.setStroke(new java.awt.BasicStroke(2));
        }

        for(int i=0;i<howManyEllipses;i++)
        {
            if(ellipses[i].isSelected == true)
                My2DGraphics.setStroke(new java.awt.BasicStroke(4));
            My2DGraphics.draw(ellipses[i]);
            My2DGraphics.setStroke(new java.awt.BasicStroke(2));
        }

        for(int i=0;i<howManyTriangles;i++)
        {
            if(triangles[i].isSelected == true)
                My2DGraphics.setStroke(new java.awt.BasicStroke(4));
            My2DGraphics.draw(triangles[i]);
            My2DGraphics.setStroke(new java.awt.BasicStroke(2));
        }

        switch(str)
        {
            case "Rectangle":
                if(isSwitched == false)
                {
                    MyRectangle rectangle = new MyRectangle(points[0], points[1]);
                    My2DGraphics.draw(rectangle);
                }
            break;

            case "Ellipse":
                if(isSwitched == false)
                {
                    MyEllipse ellipse = new MyEllipse(points[0], points[1]);
                    My2DGraphics.draw(ellipse); 
                }
            break;

            case "Triangle":
                if(isSwitched == false)
                {
                    Point2D point = new Point2D.Double(points[0].getX()-(points[1].getX()-points[0].getX()),points[1].getY());
                    MyTriangle triangle = new MyTriangle(points[0].getX(),points[0].getY(),points[1].getX(),points[1].getY(),point.getX(),point.getY());
                    My2DGraphics.draw(triangle);
                }
            break;
        }
    }
    
    private class MyMouseAdapter extends MouseAdapter 
    {
        private int x,y,dx,dy;
        
        @Override
        public void mousePressed(MouseEvent event) 
        {
            points[0] = event.getPoint();
            x = event.getX();
            y = event.getY();
        }

        @Override
        public void mouseClicked(MouseEvent event) 
        {
            for(int i=0;i<howManyRectangles;i++)
            {
                rectangles[i].isSelected = false;
            }

            for(int i=0;i<howManyRectangles;i++)
            {
                if(rectangles[i].isInside(event.getPoint().getX(),event.getPoint().getY())==true)
                {
                    rectangles[i].isSelected=true;
                }
            }

            for(int i=0;i<howManyEllipses;i++)
            {
                ellipses[i].isSelected = false;
            }

            for(int i=0;i<howManyEllipses;i++)
            {
                if(ellipses[i].isInside(event.getPoint().getX(),event.getPoint().getY())==true)
                {
                    ellipses[i].isSelected=true;
                }
            }

            for(int i=0;i<howManyTriangles;i++)
            {
                triangles[i].isSelected = false;
            }

            for(int i=0;i<howManyTriangles;i++)
            {
                if(triangles[i].isInside(event.getPoint().getX(),event.getPoint().getY())==true)
                {
                    triangles[i].isSelected=true;
                }
            }
            repaint();
        }

        @Override
        public void mouseReleased(MouseEvent event) 
        {
            if(str=="Rectangle")
            {
                MyRectangle rectangle = new MyRectangle(points[0], points[1]);
                rectangles[howManyRectangles]=rectangle;
                howManyRectangles++;
                repaint();
            }   

            if(str=="Ellipse")
            {                                                                   
                MyEllipse ellipse = new MyEllipse(points[0], points[1]);                              
                ellipses[howManyEllipses]=ellipse;
                howManyEllipses++;
                repaint();
            }

            if(str=="Triangle")
            {                                                                   
                Point2D point = new Point2D.Double(points[0].getX()-(points[1].getX()-points[0].getX()),points[1].getY());                                        
                MyTriangle triangle = new MyTriangle(points[0].getX(),points[0].getY(),points[1].getX(),points[1].getY(),point.getX(),point.getY());
                triangles[howManyTriangles] = triangle;
                howManyTriangles++;
                repaint();
            }

            str = "lalla";
        }

        @Override
        public void mouseDragged(MouseEvent event)
        {   
            doMove(event);
            isSwitched = false;
            points[1] = event.getPoint();
            repaint();
        }

        private void doMove(MouseEvent event)
        {
            dx = event.getX() - x;
            dy = event.getY() - y;
            
            for(int i=0;i<howManyRectangles;i++)
            {
                if(rectangles[i].isSelected == true && rectangles[i].isInside(x,y)==true) 
                {
                    rectangles[i].addX(dx);
                    rectangles[i].addY(dy);
                    repaint();
                }
            }

            for(int i=0;i<howManyEllipses;i++)
            {
                if(ellipses[i].isSelected == true && ellipses[i].isInside(x,y)==true)
                {
                    ellipses[i].addX(dx);
                    ellipses[i].addY(dy);
                    repaint();
                }
            }

            for(int i=0;i<howManyTriangles;i++)
            {
                if(triangles[i].isSelected == true && triangles[i].isInside(x,y)==true) 
                {
                    triangles[i].move(dx,dy);
                    repaint();
                }
            }

            x += dx;
            y += dy;
        }
    }

    private class MyMouseWheelListener implements MouseWheelListener {
        
        @Override
        public void mouseWheelMoved(MouseWheelEvent event) {
            doScale(event);
        }
        
        private void doScale(MouseWheelEvent event) {
            
            int x = event.getX();
            int y = event.getY();

            if (event.getScrollType() == MouseWheelEvent.WHEEL_UNIT_SCROLL) {

                for(int i=0;i<howManyRectangles;i++)
                {
                    if (rectangles[i].isInside(x, y) && rectangles[i].isSelected == true) 
                    {                
                        double value =  event.getWheelRotation() * 5f;
                        rectangles[i].addWidth(value);
                        rectangles[i].addHeight(value);
                        repaint();
                    }
                }   

                for(int i=0;i<howManyEllipses;i++)
                {
                    if (ellipses[i].isInside(x, y) && ellipses[i].isSelected == true) 
                    {                 
                        double value =  event.getWheelRotation() * 5f;
                        ellipses[i].addWidth(value);
                        ellipses[i].addHeight(value);
                        repaint();
                    }
                }

                for(int i=0;i<howManyTriangles;i++)
                {
                    if (triangles[i].isInside(x, y) && triangles[i].isSelected == true) 
                    {                 
                        double value =  event.getWheelRotation() * 5f;
                        triangles[i].changeSize(value);
                        repaint();
                    }
                }
                
            }            
        }
    }

    class MyEllipse extends Ellipse2D.Double
    {
        public boolean isSelected = false;

        public MyEllipse(Point2D p1, Point2D p2) 
        {
            setFrameFromDiagonal(p1,p2);
        }

        public boolean isInside(double x, double y) 
        {    
            return getBounds2D().contains(x, y);
        }

        public void addX(double x) 
        {  
            this.x += x;
        }

        public void addY(double y) 
        {         
            this.y += y;
        }

        public void addWidth(double w) 
        {    
            this.width += w;
        }

        public void addHeight(double h) 
        {     
            this.height += h;
        }
    }

    class MyRectangle extends Rectangle2D.Double
    {
        public boolean isSelected = false;

        public MyRectangle(Point2D p1,Point2D p2) 
        { 
            setFrameFromDiagonal(p1,p2);
        }

        public boolean isInside(double x, double y) 
        { 
            return getBounds2D().contains(x, y);
        }

        public void addX(double x) 
        {  
            this.x += x;
        }

        public void addY(double y) 
        {  
            this.y += y;
        }
        
        public void addWidth(double w) 
        {
            this.width += w;
        }
        
        public void addHeight(double h) 
        {     
            this.height += h;
        }
    }

    class MyTriangle extends Path2D.Double
    {
        private double x1, x2, x3;
        private double y1, y2, y3;
        public boolean isSelected = false;

        public MyTriangle(double x1,double y1,double x2,double y2,double x3,double y3)
        {
            this.x1 = x1;
            this.x2 = x2;
            this.x3 = x3;
            this.y1 = y1;
            this.y2 = y2;
            this.y3 = y3;
            build();
        }

        public void changeSize(double value)
        {
            y1 = y1 - value;
            x2 = x2 + value;
            y2 = y2 + value;
            x3 = x3 - value;
            y3 = y3 + value;
            build();
        }

        public void move(double x,double y)
        {
            x1 = x1 + x;
            y1 = y1 + y;
            x2 = x2 + x;
            y2 = y2 + y;
            x3 = x3 + x;
            y3 = y3 + y;
            build();
        }

        public void build()
        {
            reset();
            moveTo(x1,y1);
            lineTo(x2,y2);
            lineTo(x3,y3);
            lineTo(x1,y1);
            closePath();
            }

        public boolean isInside(double x, double y) 
        { 
            return contains(x, y);
        }

    }

}
