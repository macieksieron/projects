import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.awt.geom.*;

class MyWindowAdapter extends WindowAdapter 
{
    public void windowClosing(WindowEvent e) 
    { 
        System.exit(0); 
    }
}

public class Edytor extends JFrame implements ActionListener
{
    MyJPanel panel;
    MenuBar menu;
    Menu select, options;
    MenuItem rectangle , ellipse , triangle , info , exit;
    Dialog infoDialog,instructionDialog;
    Button infoButton,instructionButton,dialogButton,dialogButton2;
    Label dialogText1,dialogText2,dialogText3,dialogText4;

    public Edytor() 
    {
        super("Editor");
        setBounds(100,100,1024,800); 
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
        getContentPane().setBackground(Color.WHITE);
    
        panel = new MyJPanel();
        add(panel);
        
        infoButton = new Button("Info");
        infoButton.addActionListener(this);
        dialogButton = new Button("Back");
        dialogButton.addActionListener(this);
        panel.add(infoButton);
      
        infoDialog = new Dialog(this,"Info",true);
        infoDialog.setSize(200,150);

        dialogText1 = new Label();
        dialogText2 = new Label();
        dialogText3 = new Label();

        dialogText1.setText("Simple Shapes Editor");
        dialogText2.setText("Author: Maciej Sieroń");
        dialogText3.setText("Version 1.0");
        
        infoDialog.setLayout(new FlowLayout(FlowLayout.CENTER));
        infoDialog.add(dialogText1);
        infoDialog.add(dialogText2);
        infoDialog.add(dialogText3);
        infoDialog.add(dialogButton);

        menu = new MenuBar();
        select = new Menu("Select");
        options = new Menu("Options");
        menu.add(select);
        menu.add(options);

        rectangle = new MenuItem("Rectangle");
        rectangle.addActionListener(this);
        triangle = new MenuItem("Triangle");
        triangle.addActionListener(this);
        ellipse = new MenuItem("Ellipse");
        ellipse.addActionListener(this);
        info = new MenuItem("Instruction");
        info.addActionListener(this);
        exit = new MenuItem("Exit");
        exit.addActionListener(this);

        select.add(rectangle);
        select.add(ellipse);
        select.add(triangle);

        options.add(info);
        options.add(exit);

        setMenuBar(menu);

        dialogButton2 = new Button("Back");
        dialogButton2.addActionListener(this);

        instructionDialog = new Dialog(this, "Instruction", true);
        instructionDialog.setSize(700,125);

        dialogText1 = new Label();
        dialogText2 = new Label();
        dialogText3 = new Label();
        dialogText4 = new Label();

        dialogText1.setText("To draw a figure, select the appropriate one from the 'Select' tab and drag the mouse on the screen.");
        dialogText2.setText("To select a figure as active, click on it with the mouse.");
        dialogText3.setText("To move active figure click and drag the mouse.");
        dialogText4.setText("To resize the active figure use scroll.");
        
        instructionDialog.setLayout(new FlowLayout(FlowLayout.CENTER));
        instructionDialog.add(dialogText1);
        instructionDialog.add(dialogText2);
        instructionDialog.add(dialogText3);
        instructionDialog.add(dialogText4);
        instructionDialog.add(dialogButton2);
    }

    public void actionPerformed(ActionEvent event)
    {
        if(event.getActionCommand().equals("Info")) 
            infoDialog.setVisible(true);
        else if(event.getActionCommand().equals("Back"))
        {
            infoDialog.setVisible(false);
            instructionDialog.setVisible(false);
        }
        else if(event.getActionCommand().equals("Exit"))
            System.exit(0);
        else if(event.getActionCommand().equals("Instruction"))
            instructionDialog.setVisible(true);
        else
        {
            panel.changeStr(event.getActionCommand());
            panel.repaint();
            panel.changeIsSwitched(true);
        }
    }

    public static void main(String[] args) 
    {
        Edytor Editor = new Edytor();
    }
}

