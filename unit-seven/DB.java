package bd;

import java.sql.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;

import javax.swing.*;


public class DB {
	private Connection con = null;
	DB() throws SQLException{
		getConnection();
	}
	/***********************************           链接数据库          ***************************************/
    //定义MySQL的数据库驱动程序
	public void getConnection() throws SQLException{
		 try{
	            Class.forName("com.mysql.jdbc.Driver") ;
	            System.out.println("驱动加载成功");
	        	String url = "jdbc:mysql://localhost:3306/stuInfoManage";
	            String user = "root";
	            String password = "uonele";
	            con = DriverManager.getConnection(url, user, password);
	            System.out.println("数据库连接成功");
	        }catch(ClassNotFoundException e){
	            e.printStackTrace() ;
	        }
	}
	/***********************************          初始化学生信息表          ***************************************/
	public void initStuInfo(){         
		String sql = "create table stuInfo(stuID VARCHAR(15) PRIMARY KEY, name VARCHAR(10), className  VARCHAR(10),"+
			"physical INT(8), english  INT(8),math  INT(5))";
		try{ 
			Statement s=con.createStatement();
			s.executeUpdate(sql);
			s.close();
			System.out.println("初始化成功");
		}
		catch(Exception e){                                 //该表已存在
			System.out.println("初始化失败");
		}	
	}
/***********************************        查看数据库中有几张表          ***************************************/
	public void showTabels(){
		String sql = "show tables";
		try{
			Statement stmt = con.createStatement(ResultSet.TYPE_SCROLL_INSENSITIVE,ResultSet.CONCUR_READ_ONLY);
			ResultSet rs = stmt.executeQuery(sql);
			System.out.println("数据库stuInfiManage下的表有：");
			while(rs.next()){
				System.out.println(rs.getString(1));
			}
		}catch(SQLException ex){
			ex.printStackTrace();
			System.out.println(ex.getMessage());
		}
	}
	
	/*********************************增加学生,查重失败..代码写了，没效果*********************************/
	public void addStu(String stuID ,String name ,String className ,int physical ,int english ,int math) throws SQLException{
		String sql = "insert into stuInfo (stuID,name,className,physical,english,math) values('"+stuID+"','"+name+"','"+className+"','"+ physical+"','"+english+"','"+math+"') "; 
		try{
			Statement s=con.createStatement();
			ResultSet r=s.executeQuery("select * from stuInfo where stuID="+stuID);
		   	r.last();
		   	if(r.getRow()==1){
		   		JOptionPane.showMessageDialog( null ,"该学号的学生信息已存在");
		   		}
		   	else if(stuID.equals("")){
		   		JOptionPane.showMessageDialog( null ,"学号不能为空");
		   		}
		   	else{ 
		   		s.executeUpdate(sql);
		   		s.close();
				con.close();
				JOptionPane.showMessageDialog( null ,"<html>"+"学号:"+stuID+"<br>"
				        		   +"姓名:"+name+"<br>"
				        		   +"班级:"+className+"<br>"
				        		   +"大物:"+physical+"<br>"
				        		   +"英语:"+math+"<br>"
				        		   +"数学:"+math+"<br> 成功！" ) ; 
				}
		}catch(Exception e){
			System.out.println("try没执行！");
			}
	   }
	
    /***********************************           显示所有学生信息         ***************************************/
    public void displayAll() throws IOException{	
   	 	JFrame jf = new JFrame();
			JTextArea  jta;//文本区
			JScrollPane jspjta;//滚动
			jta=new JTextArea(20,30);//文本区
			jspjta=new JScrollPane(jta);//滚动面板 			
			jf.add(jspjta);
			jta.append("\tstuID \t name \t className \t physical \t english \t math\n");
			try {    
	              String sql = "select * from stuInfo";
	              Statement stmt = (Statement) con.createStatement();
	              ResultSet rs = stmt.executeQuery(sql);         	         
	              while(rs.next()){
	 	            	String stuID = rs.getString("stuID");
	 					String name = rs.getString("name");
	 					String className = rs.getString("className");
	 					int physical = rs.getInt("physical");
	 					int english = rs.getInt("english");
	 					int math = rs.getInt("math");
	 	            	  
	 	            	jta.append("\t"+stuID+"\t"); 
	 	            	jta.append(name+"\t");   
	 	            	jta.append(className+"\t");	
	 	            	jta.append(String.valueOf(physical)+"\t");	
	 	            	jta.append(String.valueOf(english)+"\t");  	
	 	            	jta.append(String.valueOf(math)+"\n");  
	              }	              
	    	 }catch (SQLException e) {
	    		 System.out.println("try没执行");
	             e.printStackTrace();
	         }			
			jf.setTitle("学生详细信息");
	        jf.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
	        jf.setVisible(true);
	        jf.setSize(650, 300);
	        //jf.pack(); 
		 }
	
		/***********************************           传递sql并展示           ***************************************/
	public void usesql(String sql) throws SQLException{
			try{
	  			Statement s=con.createStatement();
	  			ResultSet r=s.executeQuery(sql);
	  			r.last();
	  		    int cc=r.getRow();
                if(cc==0){
                	 JOptionPane.showMessageDialog( null ,"未查询到相关信息！" ) ;
                	 }
                else{
                	r.beforeFirst();
                	while(r.next()){
	  				JOptionPane.showMessageDialog( null ,"<html>"+"stuID:"
	  					+r.getString	("stuID")+"<br>"
				         +"name:"+r.getString("name")+"<br>"
				         +"className:"+r.getString("className")+"<br>"
				         +"physical:"+r.getString("physical")+"<br>"
				         +"english:"+r.getString("english")+"<br>"
	  					 +"math:"+r.getString("math")+"<br> 已查询到相关记录！" ) ;
	  				}
                	System.out.println("查到了！");
                }
	  	   }
		 catch(Exception e){
			 System.out.println("try没执行，去瞅瞅吧！");
		 }
	}
		  /***********************************           按学号查找           ***************************************/
		  public void findByStuID(String stuID) throws Exception{
			  String sql = "select * from stuInfo   where stuID="+stuID;
		  	  usesql(sql);
	       }
	  /***********************************           按姓名查找          ***************************************/
	     public  void findByName(String name) throws Exception{	    
	    	 String sql = "select * from stuInfo   where name='"+name+"' ";
	    	 usesql(sql);
	    }
	public void delByStuID(String stuID) throws Exception{
		String sql = "delete from stuInfo where stuID="+stuID;
		try{
  			Statement s=con.createStatement();
  			s.executeUpdate(sql);
  			s.close();
  			 JOptionPane.showMessageDialog( null ,"删除成功！" ) ;
		}catch(Exception e){
			System.out.println("try没执行");
		}
	}
	String stuID;
	String name;
	String className;
	String physical;
	String english;
	String math;
	
	
	public void update() throws Exception{
		String stuIDTemp = JOptionPane.showInputDialog(null,"请输入想要查询的学号：");
		 String sql = "select * from stuInfo   where stuID="+stuIDTemp;
		try{
  			Statement s=con.createStatement();
  			ResultSet r=s.executeQuery(sql);
  			r.last();
  		    int cc=r.getRow();
            if(cc==0){
            	 JOptionPane.showMessageDialog( null ,"未查询到相关信息！" ) ;
            	 }
            else{
            	r.beforeFirst();
            	while(r.next()){
            		stuID = r.getString("stuID");
 					name = r.getString("name");
 					className = r.getString("className");
 					int phy = r.getInt("physical");
 					physical = Integer.toString(phy);
 					int eng = r.getInt("english");
 					english = Integer.toString(eng);
 					int ma = r.getInt("math");
 					math = Integer.toString(ma) ;
 					updateListener ul = new updateListener();
            		}
            	}
		}catch(Exception e){
            	e.printStackTrace();
            }
	}
	/***********************************            main             ******************************************/
    public static void main(String args[]) throws Exception{
       DB ct = new DB();
       ct.update();
       //ct.getConnection();
       // ct.initStuInfo();
       //ct.showTabels();
       //ct.displayAll();
       //ct.addStu("201416920414","yuyangyang","rj1403", 75, 75, 59); 
       //ct.addStu("201416920410" ,"zhangpin", "rj1403",85, 65, 63);
       //ct.addStu("201416920411" ,"wuwenle", "rj1403",95, 85, 93);
       //ct.addStu("201416920413" ,"dingming", "rj1403",90, 75, 53);
       //ct.findByStuID("201416920413");      //done
       //ct.findByName("wuwenle");    //try没执行
       //ct.delByStuID("201416920411");
       //ct.con.close();
    }
	class updateListener extends JFrame implements ActionListener         {
		Login lg = new Login();
		
		JTextField jtf1 = new JTextField();
		JTextField jtf2 = new JTextField() ;
		JTextField jtf3 = new JTextField() ;
		JTextField jtf4 = new JTextField() ;
		JTextField jtf5 = new JTextField() ;
		JTextField jtf6 = new JTextField() ;
		
		JLabel jlb1 = new JLabel("学号：") ;  
		JLabel jlb2 = new JLabel("姓名：") ;
		JLabel jlb3 = new JLabel("班级：") ;
		JLabel jlb4 = new JLabel("大物：") ;
		JLabel jlb5 = new JLabel("英语：") ;
		JLabel jlb6 = new JLabel("高数：") ;
		
		JButton btn = null ;
		
		updateListener(){
	        this.setTitle("请修改下列数据:") ;            
            this.setBounds(250, 100, 220,320) ;      
            this.setResizable(false);
            this.setLayout(null) ;
            this.setVisible(true);
            
            jlb1.setBounds(43,23,100,25) ;
            jlb2.setBounds(43,58,100,25) ;
	 		jlb3.setBounds(43,93,100,25) ;
	 		jlb4.setBounds(43,128,100,25) ;
	 		jlb5.setBounds(43,163,100,25) ;
	 		jlb6.setBounds(43,198,100,25) ;
	 		
	 		jtf1.setBounds(80,25,100,25) ;
	 		jtf2.setBounds(80,60,100,25) ;
	 		jtf3.setBounds(80,95,100,25) ;
	 		jtf4.setBounds(80,130,100,25) ;
	 		jtf5.setBounds(80,165,100,25) ;
	 		jtf6.setBounds(80,200,100,25) ;
	 		
	 		this.add(jtf1) ;
	 		this.add(jtf2) ;
	 		this.add(jtf3) ;
	 		this.add(jtf4) ;
	 		this.add(jtf5) ;
	 		this.add(jtf6) ;
	 		this.add(jlb1) ;
	 		this.add(jlb2) ;
	 		this.add(jlb3) ;
	 		this.add(jlb4) ;
	 		this.add(jlb5) ;
	 		this.add(jlb6) ;
	 		jtf1.setText(stuID);
	 		jtf2.setText(name);
	 		jtf3.setText(className);
	 		jtf4.setText(physical);
	 		jtf5.setText(english);
	 		jtf6.setText(math);
	 		
	 		btn = new JButton("修改") ;               		
	 		btn.setBounds(68,245,80,30) ;
	 		this.add(btn) ;             
	 		btn.addActionListener(this) ;
		}
		
		public void actionPerformed(ActionEvent e){
			
			DB db = null;
			try {
				db = new DB();
				String sql = "delete from stuInfo where stuID="+stuID;
	  			Statement s=con.createStatement();
	  			s.executeUpdate(sql);
	  			s.close();
			} catch (SQLException e2){
				e2.printStackTrace();
			}
	 		JButton btn=(JButton)e.getSource();
 			String stuID = jtf1.getText() ; 
			String name = jtf2.getText() ;
 			String classID = jtf3.getText() ;
 			
 			String physicalString = jtf4.getText() ;
 			int physical = Integer.parseInt(physicalString);
 			
 			String englishString = jtf5.getText() ;
 			int english = Integer.parseInt(englishString);
 			
 			String mathString = jtf6.getText() ;
 			int math = Integer.parseInt(mathString);
 			
 			try {
				db.addStu(stuID, name, classID, physical, english, math);
			} catch (SQLException e1) {
				e1.printStackTrace();
			}
		}
}
}
