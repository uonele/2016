package bd;

import java.awt.*;
import java.awt.event.*;
import java.io.IOException;
import java.sql.*;

import javax.swing.*;
public class Login extends JFrame implements ActionListener{
	private Connection con = null;
	String account = "123";
	String password = "123";
	
	 /*以下是登陆界面的组件	 */
	JFrame jf = new JFrame(); 
	JButton login ;
	JTextField jt1,jt2;
	JLabel jl1,jl2,jl3;
	JPanel jp1,jp2,jp3 ,jp4;
	
	
	/*以下是登陆后的选择界面的组件*/
	Container c2 = getContentPane();
	JButton b1,b2,b3,b4,b5,b6,b7,b8;
	
	Login(){
	}
	/***********************************       初始化登陆界面         ***************************************/	
	public void initLogin(){
		Toolkit tk=Toolkit.getDefaultToolkit();
		jf.setLocation((tk.getScreenSize().width-getSize().width)/2,(tk.getScreenSize().height-getSize().height)/2);
		jf.setTitle("登陆");
    	jf.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    	jf.setSize(300,130);
    	jf.setVisible(true);
		Container c1=jf.getContentPane();
		
		c1.setLayout(new GridLayout(4,1));
		login = new JButton("登陆");
		jt1 = new JTextField(15);
		jt1.setEditable(true);
		
		jt2 = new JTextField(15);
		jt2.setEditable(true);
		
		jp1 = new JPanel();
		jp2 = new JPanel();
		jp3 = new JPanel();
		jp4 = new JPanel();
    	jl1 = new JLabel("账户密码:");
    	jl2 = new JLabel("确认密码:");
    	jl3 = new JLabel("");
    	
    	jp1.add(jl1);
    	jp1.add(jt1);
    	jp2.add(jl2);
    	jp2.add(jt2);
    	jp3.add(jl3);
    	jp4.add(login);
    	
    	c1.add(jp1);
    	c1.add(jp2);
    	c1.add(jp3);
    	c1.add(jp4);
    	login.addActionListener( this);
	}
	/***********************************     初始化登陆后的界面     ***************************************/
	public void initSecond() throws SQLException{
		c2.setLayout(null);
		final DB db = new DB();
		b1 = new JButton("显示已有学生信息");
		b1.setBounds(10,10,160,30);
		
		b2=new JButton("添加新的学生信息");
		b2.setBounds(10,45,160,30);
		
		b3=new JButton("修改已有学生信息");
		b3.setBounds(10,80,160,30);
		
		b4=new JButton("删除已有学生信息");
		b4.setBounds(10,115,160,30);
		
		b5=new JButton("按照学号查找学生");
		b5.setBounds(10,150,163,30);
		
		b6=new JButton("按照姓名查找学生");
		b6.setBounds(10,185,163,30);
		
		b7=new JButton("待定按钮");
		b7.setBounds(10,220,163,30);
		
		b8=new JButton("退出信息管理系统");
		b8.setBounds(10,255,163,30);
		
		b1.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent arg0) {
				try {
					db.displayAll();
				} catch (IOException e) {
					e.printStackTrace();
					System.out.println();
				}
			}
		}); 
		Listener Lis=new Listener();
		b2.addActionListener(Lis);
		b3.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				try {
					db.update();
				} catch (Exception e1) {
					e1.printStackTrace();
					System.out.println("再试试吧！try没执行");
				}
			}
		});
		b4.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent arg0) {
				String stuID = JOptionPane.showInputDialog(null,"请输入想要删除的学号：");
				try {
					db.delByStuID(stuID);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
		b5.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				String stuID = JOptionPane.showInputDialog(null,"请输入想要查询的学号：");
				try {
					db.findByStuID(stuID);
				} catch (Exception e1) {
					e1.printStackTrace();
				}
			}
		});
		b6.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e) {
				String name = JOptionPane.showInputDialog(null,"请输入想要查询的姓名：");
				try {
					db.findByName(name);
				} catch (Exception e2) {
					e2.printStackTrace();
				}
			}
		});
		b8.addActionListener(new ActionListener(){
			public void actionPerformed(final ActionEvent e){ 
				System.exit(0);                          //该按钮点击时，退出学籍管理系统
			}
		});
		c2.add(b1);                                //将按钮逐个添加到面板里
		c2.add(b2);
		c2.add(b3);
		c2.add(b4);
		c2.add(b5);
		c2.add(b6);
		c2.add(b7);
		c2.add(b8);
		this.setTitle("学生信息管理系统");
    	this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    	this.setSize(300,400);
    	this.setVisible(true);
    	
    	Toolkit tk=Toolkit.getDefaultToolkit();
		this.setLocation((tk.getScreenSize().width-getSize().width)/2,(tk.getScreenSize().height-getSize().height)/2);
	}
	
	/***********************************          登陆按钮的监听器           ***************************************/
	                                                                               /*自动被initFirst调用*/
	public void actionPerformed(ActionEvent e) {
		Object source = e.getSource();
		if(source == login){
			if(jt1.getText().equals(account) && jt2.getText().equals(password)){
				jl3.setForeground(Color.blue);
				jl3.setText("登陆成功！");
				try {
					initSecond();
				} catch (SQLException e1) {
					e1.printStackTrace();
				}
			}
			else
			{
				jl3.setForeground(Color.red);
				jl3.setText("账号密码不匹配，请检查后再试试");
			}
		}
	}
	
	/***********************************           增加学生的监听类    ***************************************/
	class Listener extends JFrame implements ActionListener         {
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
			
			Listener(){
				
		        this.setTitle("请输入数据:") ;            
	            this.setBounds(250, 100, 220,320) ;      
	            this.setResizable(false);
	            this.setLayout(null) ;
	            
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
		 		btn = new JButton("添加") ;               		
		 		btn.setBounds(68,245,80,30) ;
		 		this.add(btn) ;             
		 		btn.addActionListener(this) ;
			}
			
			public void actionPerformed(ActionEvent e){
				this.setVisible(true);
				DB db = null;
				try {
					db = new DB();
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
					  db.addStu(stuID,name,classID,physical,english,math);
					  this.setVisible(false);
				}
	 			catch (SQLException e1) {
				}
			}
	}
	/***********************************              main            ******************************************/
	public static void main(String[] args) throws SQLException {
		Login lg = new Login();
		lg.initLogin();
    //    lg.con.close();
	}
}
