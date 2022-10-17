import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.*;
import java.io.File;
import java.io.PrintWriter;
import java.util.ArrayList;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingConstants;
import javax.swing.JButton;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.Clip;
import javax.sound.sampled.AudioSystem;

public class Game extends JPanel implements ActionListener {
	public boolean isMuted = false;	
	public Board board;
	boolean anythingSelected = false;
	boolean anythingSelectedThisClick = false;
	int whichSelected;
	JLabel message;
	int my_number = 0; // unique number for each client
	PrintWriter out;
	public ArrayList<JLabel> score; // list of JLabels with informations who has already finished
	JButton mute;
	JButton skip;

	public Game(Board board, PrintWriter out) {
		this.out = out;
		setBackground(Color.LIGHT_GRAY);
		this.board = board;
		setLayout(null);

		message = new JLabel("", SwingConstants.CENTER); // label with communicates
		message.setBounds(200, 615, 300, 30);

		add(message);

		skip = new JButton("END OF TURN"); // button to skip/end turn
		skip.addActionListener(this);
		skip.setBounds(530, 590, 150, 50);
		skip.setOpaque(true);
		add(skip);

		mute = new JButton("SOUND ON"); // button to turn sound on/off
		mute.addActionListener(this);
		mute.setBounds(10, 615, 120, 30);
		add(mute);

		// 6 JLabels with info who has already finished the game
		JLabel first = new JLabel(""); 
		first.setBounds(6, 6, 150, 16);
		add(first);
		JLabel second = new JLabel("");
		second.setBounds(6, 23, 150, 16);
		add(second);
		JLabel third = new JLabel("");
		third.setBounds(6, 41, 150, 16);
		add(third);
		JLabel fourth = new JLabel("");
		fourth.setBounds(6, 59, 150, 16);
		add(fourth);
		JLabel fifth = new JLabel("");
		fifth.setBounds(6, 80, 150, 16);
		add(fifth);
		JLabel sixth = new JLabel("");
		sixth.setBounds(6, 98, 150, 16);
		add(sixth);

		score = new ArrayList<JLabel>(); // list of this JLabels ^
		score.add(first);
		score.add(second);
		score.add(third);
		score.add(fourth);
		score.add(fifth);
		score.add(sixth);

		MouseAdapter mouseAdapter = new MyMouseAdapter();
		addMouseListener(mouseAdapter);
	}

	public void playSound(String soundName) {	// play some sound file
		try {
			AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new File(soundName).getAbsoluteFile());
			Clip clip = AudioSystem.getClip();
			clip.open(audioInputStream);
			clip.start();
		} catch (Exception ex) {
			System.out.println("Error with playing sound.");
			ex.printStackTrace();
		}
	}

	public void move(int x, int y)
	{
		board.fields.get(y).player = board.fields.get(x).player;
		board.fields.get(x).player = new Player();
		repaint();
	}

	public void setMyNumber(int my_number){
		this.my_number = my_number - 48; // -48 because of ASCII value
	}

	public String formatToString(int pole) // for example: 3 -> 003, 27 -> 027
	{
		String formatted;
		if (pole < 10) {
			formatted = "00" + pole;
		} else if (pole < 100) {
			formatted = "0" + pole;
		} else {
			formatted = String.valueOf(pole);
		}
		return formatted;
	}

	@Override
	public void paintComponent(Graphics g) {
		super.paintComponent(g);
		Graphics2D My2DGraphics = (Graphics2D) g;
		My2DGraphics.setPaint(new Color(0, 0, 0));
		My2DGraphics.setStroke(new java.awt.BasicStroke(1));
		for (int i = 0; i < board.fields.size(); i++) // for every field on board
		{
			My2DGraphics.setPaint(board.fields.get(i).player.color); // set right color for field
			if (board.fields.get(i).isSelected == true) // if it is selected then make it black
				My2DGraphics.setPaint(Color.BLACK);
			My2DGraphics.fill(board.fields.get(i)); // paint it with right color
		}
	}

	private class MyMouseAdapter extends MouseAdapter {
		@Override
		public void mousePressed(MouseEvent event) {}

		@Override
		public void mouseClicked(MouseEvent event) {
			for (int i = 0; i < board.fields.size(); i++) // make all fields unselected on click
			
				board.fields.get(i).isSelected = false;
			

			for (int i = 0; i < board.fields.size(); i++) // for every field
			{
				// if we click on field and there is not selected field on board...
				if (anythingSelected == false
						&& board.fields.get(i).isInside(event.getPoint().getX(), event.getPoint().getY()) == true) {
					if (isMuted == false)
						playSound("resources/click.wav");
					board.fields.get(i).isSelected = true; // ..make this field selected
					anythingSelected = true; // something on board is selected now
					anythingSelectedThisClick = true; // something has been selected on this click
					whichSelected = i; // set which field has been selected
				}
				// if we click on field and there is selected field on board..
				else if (anythingSelected == true
						&& board.fields.get(i).isInside(event.getPoint().getX(), event.getPoint().getY()) == true) {
					// ..send info to server that you are trying to move
					out.println("MOVE " + formatToString(whichSelected) + " " + formatToString(i));

				}

			}

			if (anythingSelectedThisClick == false) // if you have not selected anything with this click..
				anythingSelected = false; // ...note that there is not selected field on board actually

			anythingSelectedThisClick = false; // reset this variable
			repaint();
		}

		@Override
		public void mouseDragged(MouseEvent event) {}

		@Override
		public void mouseReleased(MouseEvent event) {}
	}

	public void actionPerformed(ActionEvent event) {
		if (event.getActionCommand().equals("END OF TURN")) // if we click on 'END OF TURN' button
		{
			out.println("SKIP"); // send info to server that we skipped/end turn
		}
		if (event.getActionCommand().equals("SOUND ON")) {	// if we click on 'SOUND ON' button
			isMuted = true;	// turn sound off
			mute.setText("SOUND OFF");	// and change text on button
		}
		if (event.getActionCommand().equals("SOUND OFF")) {	// analogously 
			isMuted = false;
			mute.setText("SOUND ON");
		}
	}
}