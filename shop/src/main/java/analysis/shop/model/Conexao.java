package analysis.shop.model;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class Conexao {
    /* Banco de dados: `dbjava` */
    private Connection conexao;

    public Conexao() {
        try {
        	Class.forName("com.mysql.cj.jdbc.Driver");
        	conexao = DriverManager.getConnection( "jdbc:mysql://127.0.0.1:3306/customers?serverTimezone=UTC&useSSL=false&useUnicode=true&characterEncoding=UTF-8", "root", "admin");
        } catch (SQLException e) {
            throw new RuntimeException("Nao foi possivel efetuar uma conexao com o BD!");
        } catch (ClassNotFoundException e) {
            throw new RuntimeException("Nao foi possivel encontrar a classe referente! Verifique o driver!");
        }
    }

    public Connection getConexao() {
        return this.conexao;
    }

    public void closeConexao() {
        try {
            this.conexao.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}

