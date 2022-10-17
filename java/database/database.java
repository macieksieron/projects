// sudo /usr/local/mysql/support-files/mysql.server start

// javac -classpath resources/mysql-connector-java-8.0.27.jar database.java
// java -classpath resources/mysql-connector-java-8.0.27.jar database.java

// you have to manually add Viewer,Editor and Admin with proper previlages

import java.sql.*;  
import java.util.Scanner;

class database
{  
	static Scanner scan;
	static String id,name,surname,team,city,trainer,table,insert,update,user,password,league,stadium,salary;
	static int menu,columns,how;
	static Statement stmt;
	static ResultSet result_set;
	static Connection con;

    public static void main(String args[])
    {  
    	scan = new Scanner(System.in);
    	main_loop:while(true)
    	{
    		System.out.println("1.Log in");
    		System.out.println("2.Exit");
    		menu = scan.nextInt();
			System.out.println("---------------------");
			switch(menu)
			{
			case 1:
	    		System.out.print("user: ");
	    		user = scan.next();
	    		System.out.print("password: ");
	        	password = scan.next();
				try
	        	{  
	        		Class.forName("com.mysql.cj.jdbc.Driver");  
	        		con=DriverManager.getConnection("jdbc:mysql://localhost:3306/football",user,password);  
	        		stmt=con.createStatement(); 
	        	}
	        	catch(Exception e)
	        	{ 
	        		System.out.println("------------------------------------------");
	        		System.out.println(e);
	        		System.out.println("------------------------------------------");
	        		continue main_loop;
	        	} 
	        	try
	        	{
	        		table_loop:while(true)
	        		{
	        			System.out.println("---------------------");
	        			System.out.println("1.Cities");
	        			System.out.println("2.Leagues");
	        			System.out.println("3.Players");
	        			System.out.println("4.Stadiums");
	        			System.out.println("5.Teams");
	        			System.out.println("6.Trainers");
	        			System.out.println("7.Increase salary");
	        			System.out.println("8.Back");
	        			menu = scan.nextInt();
	        			System.out.println("---------------------");
	        			switch(menu)
	        			{
	        			case 1:
	        				table = "Cities";
	        				columns = 2;
	        				break;
	        			case 2:
	        				table = "Leagues";
	        				columns = 2;
	        				break;
	        			case 3:
	        				table = "Players";
	        				columns = 5;
	        				break;
	        			case 4:
	        				table = "Stadiums";
	        				columns = 4;
	        				break;
	        			case 5:
	        				table = "Teams";
	        				columns = 5;
	        				break;
	        			case 6:
	        				table = "Trainers";
	        				columns = 4;
	        				break;
	        			case 7:
		        			System.out.print("How much:");
		        			how = scan.nextInt();
		        			stmt.executeUpdate("CALL increase_salary(" + how + ")"); 
	        				continue table_loop;
	        			default:
	        				break table_loop;
	        			}
	        		
	        			query_loop:while(true)
	        			{
	        				try
	        				{
	        					System.out.println("---------------------");
	        					System.out.println("1.Show table");
	        					System.out.println("2.Insert row");
	        					System.out.println("3.Update row");
	        					System.out.println("4.Remove row");
	        					System.out.println("5.Back");            
	        					menu = scan.nextInt();
	        					System.out.println("---------------------");
	            
	        					switch(menu)
	        					{
	        					case 1:
	        						result_set = stmt.executeQuery("SELECT * FROM " + table);
	        						while(result_set.next())  
	        						{
	        							switch(columns)
	        							{
	        							case 2:
	        								System.out.println(result_set.getInt(1)+"  "+result_set.getString(2));
	        								break;
	        							case 3:
	        								System.out.println(result_set.getInt(1)+"  "+result_set.getString(2)+"  "+result_set.getString(3));
	        								break;
	        							case 4:
	        								System.out.println(result_set.getInt(1)+"  "+result_set.getString(2)+"  "+result_set.getString(3)+"  "+result_set.getString(4));
	        								break;
	        							case 5:
	        								System.out.println(result_set.getInt(1)+"  "+result_set.getString(2)+"  "+result_set.getString(3)+"  "+result_set.getString(4)+"  "+result_set.getString(5));
	        								break;
	        							}
	        						}
	        						break;
	        					case 2:
	        						System.out.print("id: ");
	        						id = scan.next();
	        						System.out.print("name: ");
	        						name = scan.next();
	        						switch(table)
	        						{
	        						case "Cities":
	        							insert = "INSERT INTO `Cities`(`ID`, `name`) VALUES ('"+ id + "', '" + name + "')";
	        							break;
	        						case "Leagues":
	        							insert = "INSERT INTO `Leagues`(`ID`, `name`) VALUES ('"+ id + "', '" + name + "')";
	        							break;
	        						case "Players":
	        							System.out.print("surname: ");
	        							surname = scan.next();
	        							System.out.print("team: ");
	        							team = scan.next();
	        							System.out.print("salary: ");
	        							salary = scan.next();
	        							insert = "INSERT INTO `Players`(`ID`, `name`, `surname`, `team`, `salary`) VALUES ('"+ id + "','" + name + "','" + surname + "','" + team + "','" + salary +"')";
	        							break;
	        						case "Stadiums":
	        							System.out.print("team: ");
	        							team = scan.next();
	        							System.out.print("city: ");
	        							league = scan.next();
	        							insert = "INSERT INTO `Stadiums`(`ID`, `name`, `team`, `city`) VALUES ('"+ id + "','" + name + "','" + team + "','" + city + "')";
	        							break;
	        						case "Teams":
	        							System.out.print("trainer: ");
	        							trainer = scan.next();
	        							System.out.print("league: ");
	        							league = scan.next();
	        							System.out.print("stadium: ");
	        							stadium = scan.next();
	        							insert = "INSERT INTO `Teams`(`ID`, `name`, `trainer`, `league`,`stadium`) VALUES ('"+ id + "','" + name + "','" + trainer +  "','" + league +  "','" + stadium  + "')";
	        							break;
	        						case "Trainers":
	        							System.out.print("surname: ");
	        							surname = scan.next();
	        							System.out.print("team: ");
	        							team = scan.next();
	        							insert = "INSERT INTO `Trainers`(`ID`, `name`, `surname`, `team`) VALUES ('"+ id + "','" + name + "','" + surname + "','" + team +"')";
	        							break;
	        						}
	        						stmt.executeUpdate(insert); 	
	        						break;
	        					case 3:
	        						System.out.print("id of row you wanna change: ");
	        						id = scan.next();
	        						System.out.print("new name: ");
	        						name = scan.next();
	        						switch(table)
	        						{
	        						case "Cities":
	        							update = "UPDATE `Cities` SET name = '" + name + "' WHERE ID = "+id;
	        							break;
	        						case "Leagues":
	        							update = "UPDATE `Leagues` SET name = '" + name + "' WHERE ID = "+id;
	        							break;
	        						case "Players":
	        							System.out.print("new surname: ");
	        							surname = scan.next();
	        							System.out.print("new team: ");
	        							team = scan.next();
	        							System.out.print("new salary: ");
	        							salary = scan.next();
	        							update = "UPDATE `Players` SET name = '" + name + "', surname = '"+ surname + "', team = '"+ team + "', salary = '"+ salary +"' WHERE ID = "+id;
	        							break;
	        						case "Stadiums":
	        							System.out.print("new team: ");
	        							team = scan.next();
	        							System.out.print("new city: ");
	        							city = scan.next();
	        							update = "UPDATE `Stadiums` SET name = '" + name + "', team = '"+ team + "', city = '"+ city +"' WHERE ID = "+id;
	        							break;
	        						case "Teams":
	        							System.out.print("new trainer: ");
	        							trainer = scan.next();
	        							System.out.print("new league: ");
	        							league = scan.next();
	        							System.out.print("new stadium: ");
	        							stadium = scan.next();
	        							update = "UPDATE `Teams` SET name = '" + name + "', trainer = '"+ trainer + "', league = '"+ league + "', stadium = '"+ stadium + "' WHERE ID = "+id;
	        							break;
	        						case "Trainers":
	        							System.out.print("new surname: ");
	        							surname = scan.next();
	        							System.out.print("new team: ");
	        							team = scan.next();
	        							update = "UPDATE `Trainers` SET name = '" + name + "', surname = '"+ surname + "', team = '"+ team +"' WHERE ID = "+id;
	        							break;
	        						}
	        						stmt.executeUpdate(update); 
	        						break;
	        					case 4:
	        						System.out.print("ID of producent you wanna remove:");
	        						id = scan.next();
	        						stmt.executeUpdate("DELETE FROM " + table + " WHERE ID="+id);
	        						break;
	        					default:
	        						break query_loop;
	        					}
	        				}
	        				catch(Exception e)
	        	        	{ 
	        					System.out.println("---------------------");
	        					System.out.println(e);
	        	        	}  
	        			}
	        		}
	        	}
	        	catch(Exception e)
	        	{ 
	        		System.out.println(e);
	        	}  
				break;
			case 2:
				System.out.println("Turning off..");
				System.out.println("---------------------");
				System.exit(0);
				break;
				
    	}
    }  
}
}