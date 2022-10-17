import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class SimpleLogicCalculator extends JFrame implements ActionListener
{
	JPanel panel;
	String[] operators = new String[] {"∧", "∨", "→", "↔"};
	String[] values = new String[] {"0","1"};
	JLabel result;
	JComboBox<String> value,value2,operator;
	
	SimpleLogicCalculator()
	{
		super("Simple Logic Calculator");
		setBounds(550,225,400,400);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		panel = new JPanel();
		panel.setBackground(Color.PINK);
		getContentPane().add(panel);
		panel.setLayout(null);
		
		result = new JLabel("0");
		result.setOpaque(true);
		result.setBounds(175, 200, 30, 30);
		panel.add(result);
		
		value = new JComboBox<String>(values);
		value.setBounds(100, 150, 60, 30);
		panel.add(value);
		value.addActionListener(this);
		
		operator = new JComboBox<String>(operators);
		operator.setBounds(157, 150, 65, 30);
		panel.add(operator);
		operator.addActionListener(this);
		
		value2 = new JComboBox<String>(values);
		value2.setBounds(220, 150, 60, 30);
		panel.add(value2);
		value2.addActionListener(this);
		
		setVisible(true);
	}
	
	int OR(int p, int q)
	{
		if(p==1 || q==1)
			return 1;
		return 0;
	}
	
	int AND(int p, int q)
	{
		if(p==1 && q==1)
			return 1;
		return 0;
	}
	
	int IMPLICATION(int p, int q)
	{
		if(p==1 && q==0)
			return 0;
		return 1;
	}
	
	int IFF(int p, int q)
	{
		if(p==q)
			return 1;
		return 0;
	}
	
	public static void main(String[] args) 
	{
		SimpleLogicCalculator logic = new SimpleLogicCalculator();
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		
		int valueInt = Integer.parseInt((String)value.getSelectedItem());
		int value2Int = Integer.parseInt((String)value2.getSelectedItem());
		
		switch((String)operator.getSelectedItem())
		{
			case  "∧":
				result.setText(String.valueOf(AND(valueInt,value2Int)));
			break;
			case "∨":
				result.setText(String.valueOf(OR(valueInt,value2Int)));
			break;
			case "→":
				result.setText(String.valueOf(IMPLICATION(valueInt,value2Int)));
			break;
			case "↔":
				result.setText(String.valueOf(IFF(valueInt,value2Int)));
			break;
		}
	}
}
