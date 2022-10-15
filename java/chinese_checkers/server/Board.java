import java.util.ArrayList;
import java.util.List;

public class Board 
{
	public List<Field> fields;
	public List<Field> corner1, corner2, corner3, corner4, corner5, corner6;	
	List<Player> players;	
	public int turn = 1;	
	
	public void generateEmptyBoard() // generator of constant board
	{
		fields = new ArrayList<Field>();
		
		Field field1 = new Field(475,15,525,55);
		
		Field field2 = new Field(450,50,500,90);
		Field field3 = new Field(500,50,550,90);
		
		Field field4 = new Field(425,85,475,125);
		Field field5 = new Field(475,85,525,125);
		Field field6 = new Field(525,85,575,125);
		
		Field field7 = new Field(400,120,450,160);
		Field field8 = new Field(450,120,500,160);
		Field field9 = new Field(500,120,550,160);
		Field field10 = new Field(550,120,600,160);
		
		Field field11 = new Field(225,155,275,195);
		Field field12 = new Field(175,155,225,195);
		Field field13 = new Field(275,155,325,195);
		Field field14 = new Field(325,155,375,195);
		Field field15 = new Field(375,155,425,195);
		Field field16 = new Field(425,155,475,195);
		Field field17 = new Field(475,155,525,195);
		Field field18 = new Field(525,155,575,195);
		Field field19 = new Field(575,155,625,195);
		Field field20 = new Field(625,155,675,195);
		Field field21 = new Field(675,155,725,195);
		Field field22 = new Field(725,155,775,195);
		Field field23 = new Field(775,155,825,195);
		
		Field field24 = new Field(200,190,250,230);
		Field field25 = new Field(250,190,300,230);
		Field field26 = new Field(300,190,350,230);
		Field field27 = new Field(350,190,400,230);
		Field field28 = new Field(400,190,450,230);
		Field field29 = new Field(450,190,500,230);
		Field field30 = new Field(500,190,550,230);
		Field field31 = new Field(550,190,600,230);
		Field field32 = new Field(600,190,650,230);
		Field field33 = new Field(650,190,700,230);
		Field field34 = new Field(700,190,750,230);
		Field field35 = new Field(750,190,800,230);
		
		Field field36 = new Field(225,225,275,265);
		Field field37 = new Field(275,225,325,265);
		Field field38 = new Field(325,225,375,265);
		Field field39 = new Field(375,225,425,265);
		Field field40 = new Field(425,225,475,265);
		Field field41 = new Field(475,225,525,265);
		Field field42 = new Field(525,225,575,265);
		Field field43 = new Field(575,225,625,265);
		Field field44 = new Field(625,225,675,265);
		Field field45 = new Field(675,225,725,265);
		Field field46 = new Field(725,225,775,265);
		
		Field field47 = new Field(250,260,300,300);
		Field field48 = new Field(300,260,350,300);
		Field field49 = new Field(350,260,400,300);
		Field field50 = new Field(400,260,450,300);
		Field field51 = new Field(450,260,500,300);
		Field field52 = new Field(500,260,550,300);
		Field field53 = new Field(550,260,600,300);
		Field field54 = new Field(600,260,650,300);
		Field field55 = new Field(650,260,700,300);
		Field field56 = new Field(700,260,750,300);
		
		Field field57 = new Field(275,295,325,335);
		Field field58 = new Field(325,295,375,335);
		Field field59 = new Field(375,295,425,335);
		Field field60 = new Field(425,295,475,335);
		Field field61 = new Field(475,295,525,335);
		Field field62 = new Field(525,295,575,335);
		Field field63 = new Field(575,295,625,335);
		Field field64 = new Field(625,295,675,335);
		Field field65 = new Field(675,295,725,335);
		
		Field field66 = new Field(250,330,300,370);
		Field field67 = new Field(300,330,350,370);
		Field field68 = new Field(350,330,400,370);
		Field field69 = new Field(400,330,450,370);
		Field field70 = new Field(450,330,500,370);
		Field field71 = new Field(500,330,550,370);
		Field field72 = new Field(550,330,600,370);
		Field field73 = new Field(600,330,650,370);
		Field field74 = new Field(650,330,700,370);
		Field field75 = new Field(700,330,750,370);

		Field field76 = new Field(225,365,275,405);
		Field field77 = new Field(275,365,325,405);
		Field field78 = new Field(325,365,375,405);
		Field field79 = new Field(375,365,425,405);
		Field field80 = new Field(425,365,475,405);
		Field field81 = new Field(475,365,525,405);
		Field field82 = new Field(525,365,575,405);
		Field field83 = new Field(575,365,625,405);
		Field field84 = new Field(625,365,675,405);
		Field field85 = new Field(675,365,725,405);
		Field field86 = new Field(725,365,775,405);
		
		Field field87 = new Field(200,400,250,440);
		Field field88 = new Field(250,400,300,440);
		Field field89 = new Field(300,400,350,440);
		Field field90 = new Field(350,400,400,440);
		Field field91 = new Field(400,400,450,440);
		Field field92 = new Field(450,400,500,440);
		Field field93 = new Field(500,400,550,440);
		Field field94 = new Field(550,400,600,440);
		Field field95 = new Field(600,400,650,440);
		Field field96 = new Field(650,400,700,440);
		Field field97 = new Field(700,400,750,440);
		Field field98 = new Field(750,400,800,440);
		
		Field field99 = new Field(175,435,225,475);
		Field field100 = new Field(225,435,275,475);
		Field field101 = new Field(275,435,325,475);
		Field field102 = new Field(325,435,375,475);
		Field field103 = new Field(375,435,425,475);
		Field field104 = new Field(425,435,475,475);
		Field field105 = new Field(475,435,525,475);
		Field field106 = new Field(525,435,575,475);
		Field field107 = new Field(575,435,625,475);
		Field field108 = new Field(625,435,675,475);
		Field field109 = new Field(675,435,725,475);
		Field field110 = new Field(725,435,775,475);
		Field field111 = new Field(775,435,825,475);

		Field field112 = new Field(400,470,450,510);
		Field field113 = new Field(450,470,500,510);
		Field field114 = new Field(500,470,550,510);
		Field field115 = new Field(550,470,600,510);
		
		Field field116 = new Field(425,505,475,545);
		Field field117 = new Field(475,505,525,545);
		Field field118 = new Field(525,505,575,545);
		
		Field field119 = new Field(450,540,500,580);
		Field field120 = new Field(500,540,550,580);
		
		Field field121 = new Field(475,575,525,615);
	
		field1.number=1;
		field2.number=2;
		field3.number=3;
		field4.number=4;
		field5.number=5;
		field6.number=6;
		field7.number=7;
		field8.number=8;
		field9.number=9;
		field10.number=10;
		field11.number=11;
		field12.number=12;
		field13.number=13;
		field14.number=14;
		field15.number=15;
		field16.number=16;
		field17.number=17;
		field18.number=18;
		field19.number=19;
		field20.number=20;
		field21.number=21;
		field22.number=22;
		field23.number=23;
		field24.number=24;
		field25.number=25;
		field26.number=26;
		field27.number=27;
		field28.number=28;
		field29.number=29;
		field30.number=30;
		field31.number=31;
		field32.number=32;
		field33.number=33;
		field34.number=34;
		field35.number=35;
		field36.number=36;
		field37.number=37;
		field38.number=38;
		field39.number=39;
		field40.number=40;
		field41.number=41;
		field42.number=42;
		field43.number=43;
		field44.number=44;
		field45.number=45;
		field46.number=46;
		field47.number=47;
		field48.number=48;
		field49.number=49;
		field50.number=50;
		field51.number=51;
		field52.number=52;
		field53.number=53;
		field54.number=54;
		field55.number=55;
		field56.number=56;
		field57.number=57;
		field58.number=58;
		field59.number=59;
		field60.number=60;
		field61.number=61;
		field62.number=62;
		field63.number=63;
		field64.number=64;
		field65.number=65;
		field66.number=66;
		field67.number=67;
		field68.number=68;
		field69.number=69;
		field70.number=70;
		field71.number=71;
		field72.number=72;
		field73.number=73;
		field74.number=74;
		field75.number=75;
		field76.number=76;
		field77.number=77;
		field78.number=78;
		field79.number=79;
		field80.number=80;
		field81.number=81;
		field82.number=82;
		field83.number=83;
		field84.number=84;
		field85.number=85;
		field86.number=86;
		field87.number=87;
		field88.number=88;
		field89.number=89;
		field90.number=90;
		field91.number=91;
		field92.number=92;
		field93.number=93;
		field94.number=94;
		field95.number=95;
		field96.number=96;
		field97.number=97;
		field98.number=98;
		field99.number=99;
		field100.number=100;
		field101.number=101;
		field102.number=102;
		field103.number=103;
		field104.number=104;
		field105.number=105;
		field106.number=106;
		field107.number=107;
		field108.number=108;
		field109.number=109;
		field110.number=110;
		field111.number=111;
		field112.number=112;
		field113.number=113;
		field114.number=114;
		field115.number=115;
		field116.number=116;
		field117.number=117;
		field118.number=118;
		field119.number=119;
		field120.number=120;
		field121.number=121;
		
		fields.add(field1);
		fields.add(field2);
		fields.add(field3);
		fields.add(field4);
		fields.add(field5);
		fields.add(field6);
		fields.add(field7);
		fields.add(field8);
		fields.add(field9);
		fields.add(field10);
		fields.add(field11);
		fields.add(field12);
		fields.add(field13);
		fields.add(field14);
		fields.add(field15);
		fields.add(field16);
		fields.add(field17);
		fields.add(field18);
		fields.add(field19);
		fields.add(field20);
		fields.add(field21);
		fields.add(field22);
		fields.add(field23);
		fields.add(field24);
		fields.add(field25);
		fields.add(field26);
		fields.add(field27);
		fields.add(field28);
		fields.add(field29);
		fields.add(field30);
		fields.add(field31);
		fields.add(field32);
		fields.add(field33);
		fields.add(field34);
		fields.add(field35);
		fields.add(field36);
		fields.add(field37);
		fields.add(field38);
		fields.add(field39);
		fields.add(field40);
		fields.add(field41);
		fields.add(field42);
		fields.add(field43);
		fields.add(field44);
		fields.add(field45);
		fields.add(field46);
		fields.add(field47);
		fields.add(field48);
		fields.add(field49);
		fields.add(field50);
		fields.add(field51);
		fields.add(field52);
		fields.add(field53);
		fields.add(field54);
		fields.add(field55);
		fields.add(field56);
		fields.add(field57);
		fields.add(field58);
		fields.add(field59);
		fields.add(field60);
		fields.add(field61);
		fields.add(field62);
		fields.add(field63);
		fields.add(field64);
		fields.add(field65);
		fields.add(field66);
		fields.add(field67);
		fields.add(field68);
		fields.add(field69);
		fields.add(field70);
		fields.add(field71);
		fields.add(field72);
		fields.add(field73);
		fields.add(field74);
		fields.add(field75);
		fields.add(field76);
		fields.add(field77);
		fields.add(field78);
		fields.add(field79);
		fields.add(field80);
		fields.add(field81);
		fields.add(field82);
		fields.add(field83);
		fields.add(field84);
		fields.add(field85);
		fields.add(field86);
		fields.add(field87);
		fields.add(field88);
		fields.add(field89);
		fields.add(field90);
		fields.add(field91);
		fields.add(field92);
		fields.add(field93);
		fields.add(field94);
		fields.add(field95);
		fields.add(field96);
		fields.add(field97);
		fields.add(field98);
		fields.add(field99);
		fields.add(field100);
		fields.add(field101);
		fields.add(field102);
		fields.add(field103);
		fields.add(field104);
		fields.add(field105);
		fields.add(field106);
		fields.add(field107);
		fields.add(field108);
		fields.add(field109);
		fields.add(field110);
		fields.add(field111);
		fields.add(field112);
		fields.add(field113);
		fields.add(field114);
		fields.add(field115);
		fields.add(field116);
		fields.add(field117);
		fields.add(field118);
		fields.add(field119);
		fields.add(field120);
		fields.add(field121);
	}
	
	public void setCorners() // set which fields on board are corners
	{
		corner1 = new ArrayList<Field>();
		for(int i=0;i<10;i++)
		{
			corner1.add(fields.get(i));
		}
		
		corner2 = new ArrayList<Field>();
		corner2.add(fields.get(19));
		corner2.add(fields.get(20));
		corner2.add(fields.get(21));
		corner2.add(fields.get(22));
		corner2.add(fields.get(32));
		corner2.add(fields.get(33));
		corner2.add(fields.get(34));
		corner2.add(fields.get(44));
		corner2.add(fields.get(45));
		corner2.add(fields.get(55));
		
		corner3 = new ArrayList<Field>();
		corner3.add(fields.get(74));
		corner3.add(fields.get(84));
		corner3.add(fields.get(85));
		corner3.add(fields.get(95));
		corner3.add(fields.get(96));
		corner3.add(fields.get(97));
		corner3.add(fields.get(107));
		corner3.add(fields.get(108));
		corner3.add(fields.get(109));
		corner3.add(fields.get(110));
		
		corner4 = new ArrayList<Field>();
		for(int i=111;i<121;i++)
		{
			corner4.add(fields.get(i));
		}
		
		corner5 = new ArrayList<Field>();
		corner5.add(fields.get(98));
		corner5.add(fields.get(99));
		corner5.add(fields.get(100));
		corner5.add(fields.get(101));
		corner5.add(fields.get(86));
		corner5.add(fields.get(87));
		corner5.add(fields.get(88));
		corner5.add(fields.get(75));
		corner5.add(fields.get(76));
		corner5.add(fields.get(65));
		
		corner6 = new ArrayList<Field>();
		corner6.add(fields.get(10));
		corner6.add(fields.get(11));
		corner6.add(fields.get(12));
		corner6.add(fields.get(13));
		corner6.add(fields.get(23));
		corner6.add(fields.get(24));
		corner6.add(fields.get(25));
		corner6.add(fields.get(35));
		corner6.add(fields.get(36));
		corner6.add(fields.get(46));
	}
	
	public void setPlayers(List<Player> players)	// set pawns on board according to number of players
	{
		switch(players.size())
		{
		case 2:
			for(int i=0;i<corner1.size();i++)
			{
				corner1.get(i).player=players.get(0);
			}
			
			for(int i=0;i<corner4.size();i++)
			{
				corner4.get(i).player=players.get(1);
			}
			break;
		case 3:
			for(int i=0;i<corner1.size();i++)
			{
				corner1.get(i).player=players.get(0);
			}
			
			for(int i=0;i<corner3.size();i++)
			{
				corner3.get(i).player=players.get(1);
			}
			
			for(int i=0;i<corner5.size();i++)
			{
				corner5.get(i).player=players.get(2);
			}
			
			break;
		case 4:
			for(int i=0;i<corner2.size();i++)
			{
				corner2.get(i).player=players.get(0);
			}
			
			for(int i=0;i<corner3.size();i++)
			{
				corner3.get(i).player=players.get(1);
			}
			for(int i=0;i<corner5.size();i++)
			{
				corner5.get(i).player=players.get(2);
			}
			
			for(int i=0;i<corner6.size();i++)
			{
				corner6.get(i).player=players.get(3);
			}
			break;
		case 6:
			for(int i=0;i<corner1.size();i++)
			{
				corner1.get(i).player=players.get(0);
			}
		
			for(int i=0;i<corner2.size();i++)
			{
				corner2.get(i).player=players.get(1);
			}
		
			for(int i=0;i<corner3.size();i++)
			{
				corner3.get(i).player=players.get(2);
			}
		
			for(int i=0;i<corner4.size();i++)
			{
				corner4.get(i).player=players.get(3);
			}
		
			for(int i=0;i<corner5.size();i++)
			{
				corner5.get(i).player=players.get(4);
			}
		
			for(int i=0;i<corner6.size();i++)
			{
				corner6.get(i).player=players.get(5);
			}
			break;
		default:
			
			break;
		}
		
	}

	public Board(List<Player> players)	
	{
		this.players = players;
		generateEmptyBoard();
		setCorners();
		setPlayers(players);
	}
	
	public void nextTurn()	
	{
		turn++;
		if(turn > players.size())
			turn = 1;
	}
}
